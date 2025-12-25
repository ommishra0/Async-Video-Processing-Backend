from fastapi import FastAPI, UploadFile, File, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import shutil
import os
import uuid
from .database import engine, Base, get_db
from .models import VideoJob
from .tasks import process_video_task

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Async Video Processor")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For development; restrict this in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "uploads"
PROCESSED_DIR = "processed"

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(PROCESSED_DIR, exist_ok=True)

@app.post("/upload")
async def upload_video(file: UploadFile = File(...), db: Session = Depends(get_db)):
    job_id = str(uuid.uuid4())
    file_extension = os.path.splitext(file.filename)[1]
    input_filename = f"{job_id}{file_extension}"
    input_path = os.path.join(UPLOAD_DIR, input_filename)
    output_filename = f"resized_{job_id}{file_extension}"
    output_path = os.path.join(PROCESSED_DIR, output_filename)

    with open(input_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Create job in database
    db_job = VideoJob(id=job_id, filename=file.filename)
    db.add(db_job)
    db.commit()
    db.refresh(db_job)

    # Trigger background task
    process_video_task.delay(job_id, input_path, output_path)

    return {"job_id": job_id, "status": "Processing"}

@app.get("/status/{job_id}")
async def get_status(job_id: str, db: Session = Depends(get_db)):
    job = db.query(VideoJob).filter(VideoJob.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    return {
        "job_id": job.id,
        "status": job.status,
        "filename": job.filename,
        "output_path": job.output_path,
        "created_at": job.created_at,
        "updated_at": job.updated_at
    }

@app.get("/jobs")
async def list_jobs(db: Session = Depends(get_db)):
    jobs = db.query(VideoJob).order_by(VideoJob.created_at.desc()).all()
    return jobs

@app.get("/")
async def root():
    return {"message": "Welcome to Async Video Processor API"}
