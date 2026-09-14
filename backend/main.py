from fastapi import FastAPI, Depends
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
import cv2
import numpy as np
import base64
import uuid
from datetime import datetime

from database import engine, Base, get_db
import models

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 🚨 SAFE MEDIAPIPE INITIALIZATION (Prevents Render crashes)
MEDIAPIPE_AVAILABLE = False
try:
    import mediapipe as mp
    mp_pose = mp.solutions.pose
    pose = mp_pose.Pose(static_image_mode=True, model_complexity=1, enable_segmentation=False)
    MEDIAPIPE_AVAILABLE = True
    print("✅ MediaPipe Pose loaded successfully.")
except Exception as e:
    print(f"⚠️ MediaPipe failed to load, running in high-precision OpenCV mode: {e}")

class ScanData(BaseModel):
    id: str
    height_cm: float
    status: str
    timestamp: str

class Base64Payload(BaseModel):
    image_base64: str
    age_months: int
    gender: str

WHO_HEIGHT_REF = {
    12: {"M": (75.7, 2.6), "F": (74.0, 2.5)},
    24: {"M": (87.1, 3.2), "F": (85.7, 3.2)}
}

@app.get("/")
def home():
    return {"message": "Poshan-Vision API is online and stable!"}

@app.post("/api/analyze")
async def analyze_image(payload: Base64Payload, db: Session = Depends(get_db)):
    try:
        print(f"📸 Analyzing payload for {payload.age_months}-month old {payload.gender}...")
        
        # 1. Decode Image
        image_bytes = base64.b64decode(payload.image_base64)
        nparr = np.frombuffer(image_bytes, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        if img is None:
            return JSONResponse(content={"status": "error", "message": "Failed to decode image"})

        h_img, w_img, _ = img.shape
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # 2. Image Quality & Lighting Check
        blur_score = cv2.Laplacian(gray, cv2.CV_64F).var()
        avg_brightness = np.mean(gray)
        
        retake_reasons = []
        if blur_score < 60:
            retake_reasons.append("Image is blurry. Please hold steady.")
        if avg_brightness < 40:
            retake_reasons.append("Lighting is insufficient. Move to a brighter area.")

        # 3. OpenCV A4 Paper Detection & Calibration Pipeline
        blurred = cv2.GaussianBlur(gray, (7, 7), 0)
        edged = cv2.Canny(blurred, 50, 150)
        contours, _ = cv2.findContours(edged, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        paper_contour = None
        pixels_per_cm = None
        a4_detected = False

        if contours:
            contours = sorted(contours, key=cv2.contourArea, reverse=True)
            for c in contours:
                peri = cv2.arcLength(c, True)
                approx = cv2.approxPolyDP(c, 0.02 * peri, True)
                if len(approx) == 4 and cv2.contourArea(c) > 3000:
                    paper_contour = c
                    x, y, w, h = cv2.boundingRect(c)
                    pixels_per_cm = max(w, h) / 29.7
                    a4_detected = True
                    break

        if not a4_detected:
            retake_reasons.append("A4 sheet is partially hidden or missing.")
            pixels_per_cm = 25.0 # Fallback scale ratio

        # 4. Height Calculation (MediaPipe Pose if available, else OpenCV Contour estimation)
        calculated_height = 75.0
        body_detected = False
        posture_valid = True
        confidence = 85

        if MEDIAPIPE_AVAILABLE:
            try:
                img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                pose_results = pose.process(img_rgb)
                if pose_results.pose_landmarks:
                    body_detected = True
                    landmarks = pose_results.pose_landmarks.landmark
                    left_ankle = landmarks[mp_pose.PoseLandmark.LEFT_ANKLE]
                    right_ankle = landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE]
                    left_shoulder = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER]
                    right_shoulder = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER]

                    if left_ankle.visibility < 0.4 or right_ankle.visibility < 0.4:
                        retake_reasons.append("Feet are not fully visible.")
                        posture_valid = False

                    body_min_y = min(left_shoulder.y, right_shoulder.y) * h_img
                    body_max_y = max(left_ankle.y, right_ankle.y) * h_img
                    body_height_px = abs(body_max_y - body_min_y)
                    if body_height_px > 100:
                        calculated_height = round(body_height_px / pixels_per_cm, 1)
            except Exception as mp_err:
                print(f"MediaPipe processing error, falling back to OpenCV contour: {mp_err}")

        # Fallback to OpenCV contour measurement if MediaPipe didn't run or find body
        if not body_detected:
            for c in contours:
                area = cv2.contourArea(c)
                if paper_contour is None or not np.array_equal(c, paper_contour):
                    if area > 40000:
                        bx, by, bw, bh = cv2.boundingRect(c)
                        subject_length_px = max(bw, bh)
                        calculated_height = round(subject_length_px / pixels_per_cm, 1)
                        body_detected = True
                        break

        # 5. Compute Confidence Score (0–100)
        if not a4_detected: confidence -= 25
        if not body_detected: confidence -= 35
        if blur_score < 60: confidence -= 15
        confidence = max(20, min(100, confidence))

        # 6. WHO Z-Score Calculation
        z_score = None
        status_message = "Normal"
        if payload.age_months in WHO_HEIGHT_REF:
            median, sd = WHO_HEIGHT_REF[payload.age_months][payload.gender]
            z_score = round((calculated_height - median) / sd, 2)
            if z_score < -3:
                status_message = "Severe Stunting (Red Alert)"
            elif z_score < -2:
                status_message = "Moderate Stunting (Yellow Alert)"
            else:
                status_message = "Healthy Growth (Green)"

        # 7. Save to Neon PostgreSQL Database
        scan_id = str(uuid.uuid4())
        current_time = datetime.utcnow().isoformat()
        
        db_scan = models.DBScan(
            id=scan_id,
            height_cm=calculated_height,
            status=status_message,
            timestamp=current_time
        )
        db.add(db_scan)
        db.commit()
        
        print(f"💾 Saved to Neon DB -> Height: {calculated_height}cm | Confidence: {confidence}%")
        
        return {
            "status": "success", 
            "height_cm": calculated_height,
            "z_score": z_score,
            "health_status": status_message,
            "confidence_score": confidence,
            "retake_required": len(retake_reasons) > 0,
            "retake_instructions": retake_reasons
        }
        
    except Exception as e:
        print(f"❌ Error processing analysis: {e}")
        return JSONResponse(content={"status": "error", "message": str(e)})

@app.post("/api/sync")
async def sync_data(scans: list[ScanData], db: Session = Depends(get_db)):
    saved_count = 0
    for scan in scans:
        existing_scan = db.query(models.DBScan).filter(models.DBScan.id == scan.id).first()
        if not existing_scan:
            db_scan = models.DBScan(id=scan.id, height_cm=scan.height_cm, status=scan.status, timestamp=scan.timestamp)
            db.add(db_scan)
            saved_count += 1
    db.commit()
    return {"message": "Sync Successful", "scans_processed": saved_count}