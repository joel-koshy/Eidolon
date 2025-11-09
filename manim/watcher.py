import time
import subprocess
import shutil
from pathlib import Path
import re

SCRIPTS_DIR = Path("/shared/scripts")
VIDEOS_DIR = Path("/shared/videos")

SCRIPTS_DIR.mkdir(parents=True, exist_ok=True)
VIDEOS_DIR.mkdir(parents=True, exist_ok=True)

print("🎬 Manim watcher started — waiting for scripts...")
print(f"   Watching: {SCRIPTS_DIR}")
print(f"   Output: {VIDEOS_DIR}")

while True:
    for script_file in SCRIPTS_DIR.glob("*.txt"):
        job_id = script_file.stem
        output_file = VIDEOS_DIR / f"{job_id}.mp4"
        prompt = script_file.read_text()

        if not output_file.exists():
            print(f"🌀 Rendering {script_file.name} ...")
            try:
                # Extract scene name from code
                code = script_file.read_text()
                scene_match = re.search(r'class\s+(\w+)\s*\(\s*Scene\s*\)', code)
                scene_name = scene_match.group(1) if scene_match else None
                
                if not scene_name:
                    print(f"❌ No Scene class found in {script_file}")
                    script_file.unlink(missing_ok=True)
                    continue
                
                print(f"   Scene: {scene_name}")
                
                # Render with Manim (without preview to avoid xdg-open error)
                result = subprocess.run(
                    ["manim", "-ql", str(script_file), scene_name, "-o", f"{job_id}.mp4", "--disable_caching"],
                    capture_output=True,
                    text=True
                )
                
                if result.returncode != 0:
                    print(f"❌ Manim render failed: {result.stderr}")
                    script_file.unlink(missing_ok=True)
                    continue
                
                # Find and move rendered video
                media_dir = Path("/manim/media/videos")
                rendered_videos = list(media_dir.glob(f"**/{job_id}.mp4"))
                
                if rendered_videos:
                    shutil.move(str(rendered_videos[0]), str(output_file))
                    print(f"✅ Finished {job_id}, saved to {output_file}")
                else:
                    print(f"⚠️ Video rendered but not found")
                
                script_file.unlink(missing_ok=True)  # remove after rendering
                
            except subprocess.CalledProcessError as e:
                print(f"❌ Rendering failed for {script_file}: {e}")
                script_file.unlink(missing_ok=True)
            except Exception as e:
                print(f"❌ Error processing {script_file}: {e}")
                script_file.unlink(missing_ok=True)

    time.sleep(2)
