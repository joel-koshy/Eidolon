from fastapi import FastAPI, Form, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import List
from uuid import uuid4
from src.worker import process_prompt
from pathlib import Path

app = FastAPI(title="Eidolon Queue Handler")

# Add CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

# In-memory "database" for demo
jobs = {}

class GenerateRequest(BaseModel):
    prompt: str

@app.get("/")
def root():
    return {"status": "Eidolon Queue Handler running", "version": "1.0.0"}

@app.post("/api/generate-video")
def generate(prompt: str = Form(...), files: List[UploadFile] = File(default=[])):
    print("Received generate request:", prompt)
    job_id = str(uuid4())
    jobs[job_id] = {
        "status": "queued",
        "progress": 0,
        "message": "Added to queue",
        "prompt": prompt
    }

    # TODO: Handle file uploads if needed
    # For now, just process the prompt
    
    # Enqueue Celery task
    process_prompt.delay(job_id, prompt)

    return {"video_id": job_id, "status": "queued", "message": "Video generation started"}

@app.get("/api/queue-status/{job_id}")
def status(job_id: str):
    if job_id in jobs:
        return jobs[job_id]
    return {"error": "Job not found"}

@app.get("/api/video/{job_id}")
def get_video(job_id: str):
    video_path = Path(f"/shared/videos/{job_id}.mp4")
    if video_path.exists():
        return FileResponse(video_path, media_type="video/mp4", filename=f"eidolon_{job_id}.mp4")
    return {"error": "Video not found"}

