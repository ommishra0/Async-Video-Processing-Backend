import subprocess
import os
from .celery_app import celery_app
from .database import SessionLocal
from .models import VideoJob

@celery_app.task(name="process_video_task")
def process_video_task(job_id: str, input_path: str, output_path: str):
    db = SessionLocal()
    try:
        # Simulate resizing using FFmpeg
        # Command: ffmpeg -i input.mp4 -vf scale=640:-1 output.mp4
        command = [
            "ffmpeg",
            "-i", input_path,
            "-vf", "scale=640:-1",
            "-y",  # Overwrite output
            output_path
        ]
        
        result = subprocess.run(command, capture_output=True, text=True)
        
        job = db.query(VideoJob).filter(VideoJob.id == job_id).first()
        if result.returncode == 0:
            job.status = "Completed"
            job.output_path = output_path
        else:
            job.status = "Failed"
            print(f"FFmpeg error: {result.stderr}")
            
        db.commit()
    except Exception as e:
        print(f"Task error: {e}")
        job = db.query(VideoJob).filter(VideoJob.id == job_id).first()
        if job:
            job.status = "Failed"
            db.commit()
    finally:
        db.close()
