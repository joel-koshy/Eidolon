from fastapi import FastAPI
from pydantic import BaseModel
from uuid import uuid4
from src.worker import process_prompt

app = FastAPI()

# In-memory "database" for demo
jobs = {}

class GenerateRequest(BaseModel):
    prompt: str

@app.post("/generate")
def generate(req: GenerateRequest):
    print("Received generate request:", req.prompt)
    job_id = str(uuid4())
    jobs[job_id] = {"status": "queued", "prompt": req.prompt}

    # Enqueue Celery task
    process_prompt.delay(job_id, req.prompt)

    return {"job_id": job_id, "status": "queued"}

@app.get("/status/{job_id}")
def status(job_id: str):
    if job_id in jobs:
        return jobs[job_id]
    return {"error": "Job not found"}

