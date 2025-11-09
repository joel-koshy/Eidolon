"""
Eidolon Backend API Server
FastAPI server that integrates:
- Manim video generation
- AI voiceover with ElevenLabs
- RAG-based Q&A chat
- Queue management
"""

from fastapi import FastAPI, UploadFile, File, Form, BackgroundTasks, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import List, Optional
import os
import sys
import json
import uuid
import shutil
from pathlib import Path
from datetime import datetime
import google.generativeai as genai

# Add parent directory to path to import manim modules
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'manim'))

# Import our Manim systems
from video_improver_mobject import MobjectVideoImprover
from voiceover_generator import VoiceoverGenerator

# Initialize FastAPI
app = FastAPI(title="Eidolon API", version="1.0.0")

# CORS middleware for Next.js frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],  # Next.js dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

# Configuration
UPLOAD_DIR = Path("uploads")
OUTPUT_DIR = Path("outputs")
SCRIPTS_DIR = Path("generated_scripts")
UPLOAD_DIR.mkdir(exist_ok=True)
OUTPUT_DIR.mkdir(exist_ok=True)
SCRIPTS_DIR.mkdir(exist_ok=True)

# API Keys from environment
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not set")

# Initialize Gemini
genai.configure(api_key=GEMINI_API_KEY)
gemini_model = genai.GenerativeModel("gemini-2.0-flash-exp")

# In-memory queue (in production, use Redis or database)
video_queue = {}

# ==================== MODELS ====================

class VideoRequest(BaseModel):
    prompt: str
    topic: Optional[str] = None

class QueueStatus(BaseModel):
    id: str
    status: str  # queued, generating_code, rendering, adding_voiceover, complete, error
    progress: int  # 0-100
    message: str
    video_url: Optional[str] = None
    script: Optional[str] = None
    error: Optional[str] = None

class ChatMessage(BaseModel):
    video_id: str
    message: str
    history: List[dict] = []

# ==================== HELPERS ====================

def update_queue_status(video_id: str, status: str, progress: int, message: str, **kwargs):
    """Update queue item status"""
    if video_id not in video_queue:
        video_queue[video_id] = {}
    
    video_queue[video_id].update({
        "status": status,
        "progress": progress,
        "message": message,
        "updated_at": datetime.now().isoformat(),
        **kwargs
    })

def generate_manim_code(prompt: str, resources: List[str] = None) -> str:
    """Generate Manim code from prompt using Gemini"""
    
    # Build prompt for code generation
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
- Grouping: VGroup(obj1, obj2).arrange(DOWN, buff=0.8)

DO NOT USE (these methods don't exist):
- .to_center() (use .move_to(ORIGIN) instead)
- .point_from_midpoint() (doesn't exist on Circle)
- Non-existent methods or attributes

LAYOUT BEST PRACTICES:
- Always add buff parameter to .next_to() with value >= 0.7
- Position titles at .to_edge(UP, buff=0.5)
- Keep text concise (< 60 characters per line)
- Group related objects with VGroup and use .arrange() for consistent spacing
- Test that no elements overlap by using proper positioning

Return ONLY the Python code, no explanations or markdown."""

    if resources:
        system_prompt += f"\n\nRESOURCE CONTEXT:\n{chr(10).join(resources)}"
    
    full_prompt = f"{system_prompt}\n\nUSER PROMPT: {prompt}\n\nGenerate complete Manim code:"
    
    response = gemini_model.generate_content(full_prompt)
    code = response.text.strip()
    
    # Clean up markdown code blocks if present
    if code.startswith("```python"):
        code = code[9:]
    if code.startswith("```"):
        code = code[3:]
    if code.endswith("```"):
        code = code[:-3]
    
    return code.strip()

async def process_video_generation(video_id: str, prompt: str, resource_files: List[str]):
    """Background task to generate video with voiceover"""
    try:
        # Step 1: Generate Manim code
        update_queue_status(video_id, "generating_code", 10, "Generating Manim animation code...")
        
        # Read resource files if provided
        resources = []
        for file_path in resource_files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    resources.append(f.read()[:5000])  # Limit to 5000 chars per file
            except:
                pass
        
        manim_code = generate_manim_code(prompt, resources if resources else None)
        
        # Save generated script
        script_path = SCRIPTS_DIR / f"{video_id}.py"
        with open(script_path, 'w', encoding='utf-8') as f:
            f.write(manim_code)
        
        update_queue_status(video_id, "rendering", 30, "Rendering Manim animation...", script=manim_code)
        
        # Step 2: Render video with overlap detection
        # Extract scene name from code
        import re
        scene_match = re.search(r'class\s+(\w+)\s*\(\s*Scene\s*\)', manim_code)
        scene_name = scene_match.group(1) if scene_match else None
        
        if not scene_name:
            raise ValueError("No Scene class found in generated code")
        
        # Render video using manim CLI
        import subprocess
        render_cmd = [
            "manim",
            "-pqh",  # Production quality high (1080p)
            "--fps", "60",  # 60fps for smoother animations
            str(script_path),
            scene_name
        ]
        
        result = subprocess.run(
            render_cmd,
            cwd=str(SCRIPTS_DIR),
            capture_output=True,
            text=True
        )
        
        if result.returncode != 0:
            raise Exception(f"Manim render failed: {result.stderr}")
        
        # Find rendered video
        video_pattern = f"**/{scene_name}.mp4"
        rendered_videos = list((SCRIPTS_DIR / "media").glob(video_pattern))
        
        if not rendered_videos:
            raise Exception("Rendered video not found")
        
        source_video = rendered_videos[0]
        
        update_queue_status(video_id, "adding_voiceover", 70, "Adding AI voiceover narration...")
        
        # Step 3: Add voiceover (only if ElevenLabs API key is set)
        final_video_path = OUTPUT_DIR / f"{video_id}.mp4"
        
        if ELEVENLABS_API_KEY:
            try:
                voiceover_gen = VoiceoverGenerator()
                final_video = voiceover_gen.generate_voiceover_for_video(
                    script_path=str(script_path),
                    video_path=str(source_video),
                    output_dir=str(OUTPUT_DIR / f"{video_id}_voiceover")
                )
                
                # Copy final video to output
                if final_video and Path(final_video).exists():
                    shutil.copy(final_video, final_video_path)
                else:
                    # Voiceover failed, use video without voiceover
                    shutil.copy(source_video, final_video_path)
            except Exception as vo_error:
                print(f"Voiceover failed: {vo_error}, using video without voiceover")
                shutil.copy(source_video, final_video_path)
        else:
            # No ElevenLabs key, use video without voiceover
            shutil.copy(source_video, final_video_path)
        
        update_queue_status(
            video_id,
            "complete",
            100,
            "Video generation complete!",
            video_url=f"/api/video/{video_id}",
            script=manim_code
        )
        
    except Exception as e:
        update_queue_status(
            video_id,
            "error",
            0,
            f"Error: {str(e)}",
            error=str(e)
        )

# ==================== ENDPOINTS ====================

@app.get("/")
async def root():
    return {"status": "Eidolon API running", "version": "1.0.0"}

@app.post("/api/generate-video")
async def generate_video(
    background_tasks: BackgroundTasks,
    prompt: str = Form(...),
    files: List[UploadFile] = File(default=[])
):
    """Generate a Manim video with voiceover from prompt"""
    
    # Generate unique video ID
    video_id = str(uuid.uuid4())
    
    # Save uploaded files
    saved_files = []
    for file in files:
        file_path = UPLOAD_DIR / f"{video_id}_{file.filename}"
        with open(file_path, "wb") as f:
            shutil.copyfileobj(file.file, f)
        saved_files.append(str(file_path))
    
    # Initialize queue status
    update_queue_status(video_id, "queued", 0, "Added to queue")
    
    # Add to background processing
    background_tasks.add_task(process_video_generation, video_id, prompt, saved_files)
    
    return {
        "video_id": video_id,
        "status": "queued",
        "message": "Video generation started"
    }

@app.get("/api/queue-status/{video_id}")
async def get_queue_status(video_id: str):
    """Get status of video generation"""
    if video_id not in video_queue:
        raise HTTPException(status_code=404, detail="Video not found in queue")
    
    return video_queue[video_id]

@app.get("/api/video/{video_id}")
async def get_video(video_id: str):
    """Download generated video"""
    video_path = OUTPUT_DIR / f"{video_id}.mp4"
    
    if not video_path.exists():
        raise HTTPException(status_code=404, detail="Video not found")
    
    return FileResponse(
        video_path,
        media_type="video/mp4",
        filename=f"eidolon_{video_id}.mp4"
    )

@app.post("/api/chat")
async def chat(message: ChatMessage):
    """RAG-based chat about the video and resources"""
    
    video_id = message.video_id
    
    # Get video script and resources
    script_path = SCRIPTS_DIR / f"{video_id}.py"
    
    if not script_path.exists():
        raise HTTPException(status_code=404, detail="Video script not found")
    
    with open(script_path, 'r', encoding='utf-8') as f:
        script_content = f.read()
    
    # Build context with script and resources
    context = f"VIDEO SCRIPT:\n{script_content}\n\n"
    
    # Add uploaded resources if available
    resource_files = list(UPLOAD_DIR.glob(f"{video_id}_*"))
    for res_file in resource_files:
        try:
            with open(res_file, 'r', encoding='utf-8') as f:
                context += f"RESOURCE ({res_file.name}):\n{f.read()[:3000]}\n\n"
        except:
            pass
    
    # Build chat prompt with history
    chat_history = "\n".join([
        f"{'User' if msg['role'] == 'user' else 'Assistant'}: {msg['content']}"
        for msg in message.history
    ])
    
    prompt = f"""You are a helpful AI assistant explaining a Manim educational video.

CONTEXT:
{context}

CHAT HISTORY:
{chat_history}

USER QUESTION: {message.message}

Provide a clear, helpful answer based on the video content and resources. Be educational and friendly."""
    
    response = gemini_model.generate_content(prompt)
    
    return {
        "response": response.text.strip(),
        "video_id": video_id
    }

@app.get("/api/queue")
async def get_all_queue():
    """Get all queue items (for debugging)"""
    return video_queue

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
