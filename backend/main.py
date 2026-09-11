from fastapi import FastAPI, Depends
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

# Import our database connection and models
from database import engine, Base, get_db
import models

# Automatically create the 'scans' table in the cloud if it doesn't exist yet
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ScanData(BaseModel):
    id: str
    height_cm: float
    status: str
    timestamp: str

@app.get("/")
def home():
    return {"message": "Poshan-Vision API is running and Cloud DB is active!"}

@app.post("/api/sync")
async def sync_data(scans: list[ScanData], db: Session = Depends(get_db)):
    print("\n" + "="*50)
    print(f"🚀 INCOMING SYNC: Processing {len(scans)} scans from mobile app...")
    
    saved_count = 0
    for scan in scans:
        # Check if this scan ID already exists in the cloud to prevent duplicates
        existing_scan = db.query(models.DBScan).filter(models.DBScan.id == scan.id).first()
        
        if not existing_scan:
            # Create a new database row object
            db_scan = models.DBScan(
                id=scan.id,
                height_cm=scan.height_cm,
                status=scan.status,
                timestamp=scan.timestamp
            )
            db.add(db_scan)
            saved_count += 1
            print(f" ✅ Saved to Cloud DB -> Baby ID: {scan.id} | Height: {scan.height_cm}cm")
        else:
            print(f" ⚠️ Skipped -> Baby ID: {scan.id} (Already exists in database)")
            
    # Permanently save changes to the PostgreSQL cloud database
    db.commit()
    print("="*50 + "\n")
    
    return {"message": "Sync Successful", "scans_processed": saved_count}