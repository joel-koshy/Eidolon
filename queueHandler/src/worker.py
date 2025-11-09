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
    
    system_prompt = """You are an expert Manim developer specializing in creating clear, educational animations with excellent visual hierarchy and readability.

CRITICAL DESIGN PRINCIPLES:
1. SPACING & LAYOUT: Use generous buffers (buff=0.7 to 1.5) to prevent overlapping
2. VISUAL HIERARCHY: Use font sizes strategically:
   - Titles: font_size=48-56
   - Main content: font_size=36-42
   - Annotations/labels: font_size=28-32
3. POSITIONING: Space elements with clear visual breathing room
4. COLOR CONTRAST: Use high-contrast colors (avoid yellow on white, use WHITE, BLUE, GREEN, RED, ORANGE)
5. MATHEMATICAL ACCURACY: Ensure all mathematical notation is precise and properly formatted

REQUIREMENTS:
1. Create a Scene class that inherits from Scene
2. Implement a construct() method with well-spaced animations
3. Use descriptive variable names and comments
4. Include step-by-step explanations with Text and MathTex
5. Position elements with sufficient spacing (buff >= 0.7)
6. Add appropriate wait() calls (1-2 seconds between major transitions)
7. Make it visually clean and professional
8. Scale objects appropriately (.scale(0.7) to .scale(1.2) as needed)

VALID MANIM METHODS:
- Positioning: .move_to(ORIGIN), .move_to(UP*2), .shift(DOWN*1.5), .next_to(obj, DOWN, buff=0.8), .to_edge(UP, buff=0.5), .to_corner(UL, buff=0.3)
- Scaling: .scale(0.8), .scale_to_fit_width(6), .scale_to_fit_height(4)
- Text/Math: Text("Hello", font_size=42), MathTex(r"\frac{1}{2}", font_size=48) — ALWAYS use raw strings (r"") for MathTex
- Axes: axes = Axes(x_range=[0, 10], y_range=[0, 10], x_length=8, y_length=6)
- Plotting: axes.plot(lambda x: np.sin(x), color=BLUE)
- Labels: axes.get_axis_labels(x_label="x", y_label="y")
- Grouping: VGroup(obj1, obj2).arrange(DOWN, buff=0.8)

DO NOT USE (these methods don't exist):
- .to_center() (use .move_to(ORIGIN) instead)
- .point_from_midpoint() (doesn't exist on Circle)
- axes.x_axis.number_to_value (doesn't exist)
- Non-existent NumberLine or Axes attributes

LAYOUT BEST PRACTICES:
- Always add buff parameter to .next_to() with value >= 0.7
- Position titles at .to_edge(UP, buff=0.5) or .to_corner(UL, buff=0.5)
- Keep text concise (< 60 characters per line)
- Group related objects with VGroup and use .arrange() for consistent spacing
- Test that no elements overlap by using proper positioning

Return ONLY the Python code, no explanations or markdown."""
    
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
