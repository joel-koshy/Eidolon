from src.celeryconfig import celery_app
import time

from pathlib import Path
import time

SCRIPTS_DIR = Path("/shared/scripts")
VIDEOS_DIR = Path("/shared/videos")
SCRIPTS_DIR.mkdir(parents=True, exist_ok=True)
VIDEOS_DIR.mkdir(parents=True, exist_ok=True)

@celery_app.task(bind=True, max_retries=3)
def process_prompt(self, job_id: str, prompt: str):
    try:
        # Simulate processing time
        manim_code = f""
        print(f"Processing job {job_id}: {prompt}")

        script_path = SCRIPTS_DIR / f"{job_id}.py"
        script_path.write_text(manim_code)

        # Save the Manim script for the renderer to pick up
        script_path.write_text(manim_code)

        result_path = f"/videos/{job_id}.mp4"
        return {"status": "completed", "video_path": result_path}
    except Exception as e:
        self.retry(exc=e, countdown=10)
