import time
import subprocess
from pathlib import Path


print("Hello")

SCRIPTS_DIR = Path("/shared/scripts")
VIDEOS_DIR = Path("/shared/videos")

SCRIPTS_DIR.mkdir(parents=True, exist_ok=True)
VIDEOS_DIR.mkdir(parents=True, exist_ok=True)

print("🎬 Manim watcher started — waiting for scripts...")

while True:
    for script_file in SCRIPTS_DIR.glob("*.py"):
        job_id = script_file.stem
        output_file = VIDEOS_DIR / f"{job_id}.mp4"

        if not output_file.exists():
            print(f"🌀 Rendering {script_file.name} ...")
            try:
                # Call the render method
                # Here for teammate
                
                print(f"✅ Finished {job_id}, saved to {output_file}")
                script_file.unlink(missing_ok=True)  # remove after rendering
            except subprocess.CalledProcessError as e:
                print(f"Rendering failed for {script_file}: {e}")

    time.sleep(2)
