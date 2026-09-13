import cv2
import numpy as np
import mediapipe as mp
import math

mp_pose = mp.solutions.pose
pose = mp_pose.Pose(static_image_mode=True, min_detection_confidence=0.5)

def calculate_height_from_image(image_path):
    image = cv2.imread(image_path)
    if image is None: return "Error: Image not found."
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    edges = cv2.Canny(blurred, 50, 150)
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    contours = sorted(contours, key=cv2.contourArea, reverse=True)
    a4_pixel_length = None
    
    for cnt in contours:
        peri = cv2.arcLength(cnt, True)
        approx = cv2.approxPolyDP(cnt, 0.02 * peri, True)
        if len(approx) == 4:
            rect = cv2.minAreaRect(approx)
            a4_pixel_length = max(rect[1][0], rect[1][1])
            break
            
    if not a4_pixel_length: return "Error: Could not detect A4 paper corners."
    pixels_per_cm = a4_pixel_length / 29.7
    
    results = pose.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    if not results.pose_landmarks: return "Error: Could not detect pose."
        
    landmarks = results.pose_landmarks.landmark
    h, w, _ = image.shape
    
    nose = landmarks[mp_pose.PoseLandmark.NOSE.value]
    left_heel = landmarks[mp_pose.PoseLandmark.LEFT_HEEL.value]
    right_heel = landmarks[mp_pose.PoseLandmark.RIGHT_HEEL.value]
    
    heel_y = (left_heel.y + right_heel.y) / 2
    heel_x = (left_heel.x + right_heel.x) / 2
    
    pixel_distance = math.sqrt(((nose.x - heel_x) * w) ** 2 + ((nose.y - heel_y) * h) ** 2)
    return round(pixel_distance / pixels_per_cm, 1)