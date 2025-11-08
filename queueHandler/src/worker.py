from src.celeryconfig import celery_app
import time

@celery_app.task(bind=True, max_retries=3)
def process_prompt(self, job_id: str, prompt: str):
    try:
        # Simulate processing time
        print(f"Processing job {job_id}: {prompt}")
        time.sleep(5)  # replace with real LLM + Manim rendering
        result_path = f"/videos/{job_id}.mp4"
        return {"status": "completed", "video_path": result_path}
    except Exception as e:
        self.retry(exc=e, countdown=10)
