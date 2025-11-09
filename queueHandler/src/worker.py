from src.celeryconfig import celery_app
import time
from pathlib import Path
import os
import google.generativeai as genai

SCRIPTS_DIR = Path("/shared/scripts")
VIDEOS_DIR = Path("/shared/videos")
SCRIPTS_DIR.mkdir(parents=True, exist_ok=True)
VIDEOS_DIR.mkdir(parents=True, exist_ok=True)

# Initialize Gemini
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
    gemini_model = genai.GenerativeModel("gemini-2.0-flash-exp")
else:
    gemini_model = None

def generate_manim_code(prompt: str) -> str:
    """Generate Manim code from prompt using Gemini"""
    if not gemini_model:
        return f"""from manim import *

class DemoScene(Scene):
    def construct(self):
        text = Text("No Gemini API key configured")
        self.play(Write(text))
        self.wait(2)
"""
    
    system_prompt = """You are an expert Manim developer. Generate clean, working Manim code for educational animations.

REQUIREMENTS:
1. Create a Scene class that inherits from Scene
2. Implement a construct() method with the animation
3. Use clear variable names and comments
4. Include step-by-step explanations with Text, MathTex
5. Use proper positioning (next_to, shift, to_edge)
6. Add appropriate wait() calls between animations
7. Make it educational and visually appealing
8. Use colors effectively (BLUE, RED, GREEN, YELLOW, PURPLE, etc.)

VALID METHODS:
- .move_to(ORIGIN), .shift(UP), .shift(DOWN * 2)
- .next_to(obj, DOWN, buff=0.5)
- .to_edge(UP), .to_corner(UL)

DO NOT USE:
- .to_center() (doesn't exist)
- Non-numeric buffs (use buff=0.5, buff=1.0, etc.)

Return ONLY the Python code, no explanations."""
    
    full_prompt = f"{system_prompt}\n\nUSER PROMPT: {prompt}\n\nGenerate complete Manim code:"
    
    response = gemini_model.generate_content(full_prompt)
    code = response.text.strip()
    
    # Clean up markdown code blocks
    if code.startswith("```python"):
        code = code[9:]
    if code.startswith("```"):
        code = code[3:]
    if code.endswith("```"):
        code = code[:-3]
    
    return code.strip()

@celery_app.task(bind=True, max_retries=3)
def process_prompt(self, job_id: str, prompt: str):
    try:
        print(f"Processing job {job_id}: {prompt}")
        
        # Generate Manim code with Gemini
        manim_code = generate_manim_code(prompt)
        print(f"Generated code for {job_id}")

        # Save the Manim script for the renderer to pick up
        script_path = SCRIPTS_DIR / f"{job_id}.py"
        script_path.write_text(manim_code)
        print(f"Saved script to {script_path}")

        result_path = f"/shared/videos/{job_id}.mp4"
        return {"status": "completed", "video_path": result_path}
    except Exception as e:
        print(f"Error processing {job_id}: {e}")
        self.retry(exc=e, countdown=10)
