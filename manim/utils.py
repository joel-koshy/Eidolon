"""
Utility functions for the video improvement system.
"""

import os
import re
import ast
import json
import shutil
from pathlib import Path
from datetime import datetime
from typing import Dict, Optional, Tuple


def validate_python_syntax(code: str) -> Tuple[bool, Optional[str]]:
    """
    Validate Python code syntax.
    
    Args:
        code: Python code as string
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    try:
        ast.parse(code)
        return True, None
    except SyntaxError as e:
        return False, f"Syntax error at line {e.lineno}: {e.msg}"
    except Exception as e:
        return False, str(e)


def validate_manim_structure(code: str) -> Tuple[bool, Optional[str]]:
    """
    Validate that code has required Manim structure.
    
    Args:
        code: Python code as string
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    # Check for required imports
    if "from manim import" not in code and "import manim" not in code:
        return False, "Missing 'from manim import *' or 'import manim'"
    
    # Check for class definition
    if "class IntegralExplanation" not in code:
        return False, "Missing 'class IntegralExplanation'"
    
    # Check for construct method
    if "def construct(self)" not in code:
        return False, "Missing 'def construct(self)' method"
    
    return True, None


def extract_json_from_text(text: str) -> Optional[Dict]:
    """
    Extract JSON from text that might contain markdown code blocks or other formatting.
    
    Args:
        text: Text potentially containing JSON
        
    Returns:
        Parsed JSON dict or None if extraction fails
    """
    # Try direct JSON parse
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass
    
    # Try to extract from code block
    json_pattern = r'```(?:json)?\s*(\{.*?\})\s*```'
    match = re.search(json_pattern, text, re.DOTALL)
    if match:
        try:
            return json.loads(match.group(1))
        except json.JSONDecodeError:
            pass
    
    # Try to find JSON object in text
    brace_pattern = r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}'
    matches = re.finditer(brace_pattern, text, re.DOTALL)
    for match in matches:
        try:
            return json.loads(match.group(0))
        except json.JSONDecodeError:
            continue
    
    return None


def clean_code_from_response(text: str) -> str:
    """
    Extract clean Python code from Gemini response that might include markdown or other formatting.
    
    Args:
        text: Response text from Gemini
        
    Returns:
        Clean Python code
    """
    # Remove markdown code blocks if present
    code_block_pattern = r'```python\s*(.*?)\s*```'
    match = re.search(code_block_pattern, text, re.DOTALL)
    if match:
        return match.group(1).strip()
    
    # If no code block, assume entire response is code
    return text.strip()


def save_iteration(
    iteration_num: int,
    code: str,
    video_path: str,
    feedback: Dict,
    base_dir: str
) -> str:
    """
    Save iteration data (code, video, feedback) to organized structure.
    
    Args:
        iteration_num: Iteration number
        code: Python code as string
        video_path: Path to rendered video
        feedback: Feedback dictionary from analysis
        base_dir: Base directory for iterations
        
    Returns:
        Path to iteration directory
    """
    # Create iteration directory
    iter_dir = Path(base_dir) / f"iteration_{iteration_num:02d}"
    iter_dir.mkdir(parents=True, exist_ok=True)
    
    # Save code
    code_path = iter_dir / "test.py"
    with open(code_path, 'w', encoding='utf-8') as f:
        f.write(code)
    
    # Copy video if it exists
    if os.path.exists(video_path):
        video_dest = iter_dir / f"video_v{iteration_num:02d}.mp4"
        shutil.copy2(video_path, video_dest)
    
    # Save feedback
    feedback_path = iter_dir / "feedback.json"
    with open(feedback_path, 'w', encoding='utf-8') as f:
        json.dump(feedback, f, indent=2)
    
    # Save metadata
    metadata = {
        "iteration": iteration_num,
        "timestamp": datetime.now().isoformat(),
        "score": feedback.get("overall_score", 0),
        "is_satisfactory": feedback.get("is_satisfactory", False)
    }
    metadata_path = iter_dir / "metadata.json"
    with open(metadata_path, 'w', encoding='utf-8') as f:
        json.dump(metadata, f, indent=2)
    
    return str(iter_dir)


def find_rendered_video(media_dir: str, scene_name: str = "IntegralExplanation") -> Optional[str]:
    """
    Find the most recently rendered video in Manim's media directory.
    
    Args:
        media_dir: Path to media directory
        scene_name: Name of the scene class
        
    Returns:
        Path to video file or None if not found
    """
    media_path = Path(media_dir)
    
    # Manim typically outputs to media/videos/[script_name]/[quality]/[scene_name].mp4
    # Search for any MP4 files
    video_files = list(media_path.rglob(f"*{scene_name}*.mp4"))
    
    if not video_files:
        # Try finding any MP4
        video_files = list(media_path.rglob("*.mp4"))
    
    if not video_files:
        return None
    
    # Return most recent
    video_files.sort(key=lambda p: p.stat().st_mtime, reverse=True)
    return str(video_files[0])


def create_summary_report(iterations_dir: str) -> Dict:
    """
    Create a summary report of all iterations.
    
    Args:
        iterations_dir: Path to iterations directory
        
    Returns:
        Summary dictionary
    """
    iterations_path = Path(iterations_dir)
    
    if not iterations_path.exists():
        return {"iterations": [], "total": 0}
    
    iterations = []
    for iter_dir in sorted(iterations_path.glob("iteration_*")):
        metadata_path = iter_dir / "metadata.json"
        if metadata_path.exists():
            with open(metadata_path, 'r') as f:
                iterations.append(json.load(f))
    
    summary = {
        "iterations": iterations,
        "total": len(iterations),
        "final_score": iterations[-1]["score"] if iterations else 0,
        "improvement": iterations[-1]["score"] - iterations[0]["score"] if len(iterations) > 1 else 0,
        "satisfied": iterations[-1]["is_satisfactory"] if iterations else False
    }
    
    return summary


def print_progress(iteration: int, score: float, max_iterations: int):
    """
    Print formatted progress information.
    
    Args:
        iteration: Current iteration number
        score: Current quality score
        max_iterations: Maximum number of iterations
    """
    bar_length = 40
    filled = int(bar_length * (score / 10))
    bar = "█" * filled + "░" * (bar_length - filled)
    
    print()
    print("=" * 70)
    print(f"  ITERATION {iteration}/{max_iterations}")
    print(f"  Quality Score: {score:.1f}/10")
    print(f"  Progress: [{bar}] {score*10:.0f}%")
    print("=" * 70)
    print()
