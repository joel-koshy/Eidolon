"""
Video Improver with Mobject Overlap Detection

Final integrated system:
1. Renders video at each iteration
2. Analyzes mobject overlaps (fast, accurate)
3. Uses Gemini to fix overlaps
4. Shows video after rendering
"""

import os
import sys
import json
import time
import subprocess
import shutil
from pathlib import Path
from typing import Dict, Optional

import google.generativeai as genai

from utils import (
    validate_python_syntax,
    validate_manim_structure,
    clean_code_from_response,
    save_iteration,
    find_rendered_video,
    create_summary_report,
    print_progress
)

from overlap_detector_scene import analyze_scene_with_overlap_detection
from render_cache import RenderCache


class MobjectVideoImprover:
    """Video improver using mobject overlap detection."""
    
    def __init__(
        self,
        script_path: str = "test.py",
        max_iterations: int = 5,
        target_score: float = 8.0,
        scene_name: str = "IntegralExplanation"
    ):
        """
        Initialize the mobject video improver.
        
        Args:
            script_path: Path to the Manim script
            max_iterations: Maximum number of improvement iterations
            target_score: Target quality score (0-10)
            scene_name: Name of the Manim scene class
        """
        self.script_path = Path(script_path)
        self.max_iterations = max_iterations
        self.target_score = target_score
        self.scene_name = scene_name
        
        # Setup directories
        self.base_dir = self.script_path.parent
        self.iterations_dir = self.base_dir / "iterations"
        self.rendered_videos_dir = self.base_dir / "rendered_videos"
        self.prompts_dir = self.base_dir / "prompts"
        self.media_dir = self.base_dir / "media"
        
        # Ensure directories exist
        self.iterations_dir.mkdir(exist_ok=True)
        self.rendered_videos_dir.mkdir(exist_ok=True)
        
        # Initialize render cache
        self.render_cache = RenderCache(str(self.base_dir / "render_cache"))
        
        # Setup Gemini
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError(
                "GEMINI_API_KEY not found in environment variables. "
                "Run setup_api.py first or set the environment variable."
            )
        
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-2.5-flash')
        
        # Load code improvement prompt
        self.improvement_prompt = self._load_prompt("code_improvement_prompt.txt")
        
        print("✓ Mobject VideoImprover initialized")
        print(f"  Script: {self.script_path}")
        print(f"  Scene: {self.scene_name}")
        print(f"  Max iterations: {self.max_iterations}")
        print(f"  Target score: {self.target_score}/10")
        print(f"  Analysis: MOBJECT OVERLAP DETECTION (fast + accurate)")
    
    def _load_prompt(self, filename: str) -> str:
        """Load a prompt template from file."""
        prompt_path = self.prompts_dir / filename
        if not prompt_path.exists():
            raise FileNotFoundError(f"Prompt template not found: {prompt_path}")
        
        with open(prompt_path, 'r', encoding='utf-8') as f:
            return f.read()
    
    def render_video(self, current_code: str) -> Optional[str]:
        """Render the Manim video (with caching)."""
        print("\n📹 Checking render cache...")
        
        # Check cache first
        cached_video = self.render_cache.get_cached_video(current_code, self.scene_name)
        if cached_video:
            return cached_video
        
        print("  Rendering video...")
        
        try:
            cmd = ["manim", "-pql", str(self.script_path), self.scene_name]
            
            print(f"  Running: {' '.join(cmd)}")
            
            result = subprocess.run(
                cmd,
                cwd=str(self.base_dir),
                capture_output=True,
                text=True
            )
            
            if result.returncode != 0:
                print(f"✗ Rendering failed:")
                print(result.stderr)
                return None
            
            # Find the rendered video
            video_path = find_rendered_video(str(self.media_dir))
            
            if video_path:
                print(f"✓ Video rendered: {video_path}")
                # Cache the rendered video
                self.render_cache.store_cached_video(current_code, self.scene_name, video_path)
                return video_path
            else:
                print("✗ Could not find rendered video")
                return None
                
        except Exception as e:
            print(f"✗ Rendering failed: {e}")
            return None
    
    def analyze_overlaps(self) -> Dict:
        """
        Analyze mobject overlaps in the scene.
        
        Returns:
            Analysis feedback as dictionary
        """
        print("\n🔍 Analyzing mobject overlaps...")
        
        try:
            feedback = analyze_scene_with_overlap_detection(
                str(self.script_path),
                self.scene_name
            )
            
            return feedback
            
        except Exception as e:
            print(f"✗ Analysis failed: {e}")
            return {
                'overall_score': 5.0,
                'is_satisfactory': False,
                'total_overlaps': 0,
                'error': str(e)
            }
    
    def improve_code(self, current_code: str, feedback: Dict, iteration: int) -> Optional[str]:
        """
        Generate improved Manim code based on overlap feedback.
        
        Args:
            current_code: Current Manim script code
            feedback: Overlap analysis feedback dictionary
            iteration: Current iteration number
            
        Returns:
            Improved code or None if generation failed
        """
        print("\n🔧 Generating improved code with Gemini...")
        
        try:
            # Format the improvement prompt with overlap analysis results
            priority_improvements = "\n".join([
                f"{i+1}. {item}"
                for i, item in enumerate(feedback.get("priority_improvements", []))
            ])
            
            # Create detailed feedback text from overlap analysis
            detailed_feedback = f"""
IMPORTANT: Make MINIMAL changes to fix overlaps. Only modify spacing/positioning, do not refactor unrelated code.

MOBJECT OVERLAP ANALYSIS RESULTS:
- Overall Score: {feedback.get('overall_score', 0)}/10
- Total Overlaps: {feedback.get('total_overlaps', 0)}
- Critical Overlaps: {feedback.get('critical_overlaps', 0)}
- Warning Overlaps: {feedback.get('warning_overlaps', 0)}
- Minor Overlaps: {feedback.get('minor_overlaps', 0)}

DETECTED OVERLAP ISSUES:
"""
            
            for issue in feedback.get('detailed_issues', [])[:10]:  # Limit to first 10
                detailed_feedback += f"\n[{issue['severity'].upper()}] {issue['mobject1']} overlaps {issue['mobject2']} by {issue['overlap']}\n"
                detailed_feedback += f"  At timestamp: {issue['timestamp']:.1f}s\n"
                detailed_feedback += f"  Fix: {issue['suggestion']}\n"
            
            prompt = self.improvement_prompt.format(
                iteration=iteration,
                previous_score=feedback.get("overall_score", 0),
                feedback=detailed_feedback,
                priority_improvements=priority_improvements,
                current_code=current_code
            )
            
            # Generate improved code
            response = self.model.generate_content(
                prompt,
                request_options={"timeout": 120}
            )
            
            # Extract code from response
            improved_code = clean_code_from_response(response.text)
            
            # Validate syntax
            is_valid, error = validate_python_syntax(improved_code)
            if not is_valid:
                print(f"✗ Generated code has syntax errors: {error}")
                return None
            
            # Validate Manim structure
            is_valid, error = validate_manim_structure(improved_code)
            if not is_valid:
                print(f"✗ Generated code missing required structure: {error}")
                return None
            
            print("✓ Improved code generated and validated")
            
            return improved_code
            
        except Exception as e:
            print(f"✗ Code improvement failed: {e}")
            return None
    
    def open_video(self, video_path: str):
        """Open video in default player."""
        try:
            print(f"\n🎬 Opening video: {video_path}")
            if sys.platform == "win32":
                os.startfile(video_path)
            elif sys.platform == "darwin":  # macOS
                subprocess.run(["open", video_path])
            else:  # Linux
                subprocess.run(["xdg-open", video_path])
        except Exception as e:
            print(f"  Could not open video automatically: {e}")
            print(f"  Please open manually: {video_path}")
    
    def run(self) -> Dict:
        """
        Run the improvement loop.
        
        Returns:
            Summary report dictionary
        """
        print("\n" + "=" * 70)
        print("  🚀 STARTING MOBJECT OVERLAP VIDEO IMPROVEMENT")
        print("=" * 70)
        
        # Read initial code
        with open(self.script_path, 'r', encoding='utf-8') as f:
            current_code = f.read()
        
        for iteration in range(1, self.max_iterations + 1):
            print_progress(iteration, 0, self.max_iterations)
            
            # Render video (with caching)
            video_path = self.render_video(current_code)
            if not video_path:
                print("⚠️  Rendering failed, stopping iteration")
                break
            
            # Copy video to rendered_videos folder
            video_copy = self.rendered_videos_dir / f"video_iteration_{iteration:02d}.mp4"
            shutil.copy2(video_path, video_copy)
            print(f"  Saved video to: {video_copy}")
            
            # Open video for viewing
            self.open_video(str(video_copy))
            
            # Analyze overlaps
            feedback = self.analyze_overlaps()
            if not feedback:
                print("⚠️  Analysis failed, stopping iteration")
                break
            
            # Save iteration
            save_iteration(
                iteration,
                current_code,
                video_path,
                feedback,
                str(self.iterations_dir)
            )
            
            # Check if satisfactory
            score = feedback.get("overall_score", 0)
            is_satisfactory = feedback.get("is_satisfactory", False)
            
            print_progress(iteration, score, self.max_iterations)
            
            if is_satisfactory or score >= self.target_score:
                print("🎉 Target quality achieved!")
                print(f"   Final score: {score}/10")
                print(f"   No critical overlaps detected!")
                break
            
            # Check if this is the last iteration
            if iteration >= self.max_iterations:
                print("⚠️  Maximum iterations reached")
                break
            
            # Generate improved code
            improved_code = self.improve_code(current_code, feedback, iteration)
            if not improved_code:
                print("⚠️  Code improvement failed, stopping iteration")
                break
            
            # Update script file
            with open(self.script_path, 'w', encoding='utf-8') as f:
                f.write(improved_code)
            
            current_code = improved_code
            print(f"✓ Script updated for next iteration")
            
            # Brief pause
            time.sleep(2)
        
        # Generate summary report
        summary = create_summary_report(str(self.iterations_dir))
        
        print("\n" + "=" * 70)
        print("  📊 IMPROVEMENT SUMMARY")
        print("=" * 70)
        print(f"  Total iterations: {summary['total']}")
        print(f"  Final score: {summary['final_score']:.1f}/10")
        print(f"  Improvement: +{summary['improvement']:.1f}")
        print(f"  Satisfied: {summary['satisfied']}")
        print("=" * 70)
        
        return summary


def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="AI-Powered Manim Video Improvement with Mobject Overlap Detection"
    )
    parser.add_argument(
        "--script",
        default="test.py",
        help="Path to Manim script (default: test.py)"
    )
    parser.add_argument(
        "--scene",
        default="IntegralExplanation",
        help="Scene class name (default: IntegralExplanation)"
    )
    parser.add_argument(
        "--max-iterations",
        type=int,
        default=5,
        help="Maximum number of iterations (default: 5)"
    )
    parser.add_argument(
        "--target-score",
        type=float,
        default=8.0,
        help="Target quality score 0-10 (default: 8.0)"
    )
    
    args = parser.parse_args()
    
    try:
        improver = MobjectVideoImprover(
            script_path=args.script,
            max_iterations=args.max_iterations,
            target_score=args.target_score,
            scene_name=args.scene
        )
        
        summary = improver.run()
        
        # Save summary to file
        summary_path = Path("iterations") / "summary.json"
        with open(summary_path, 'w') as f:
            json.dump(summary, f, indent=2)
        
        print(f"\n✓ Summary saved to: {summary_path}")
        
        # Exit with appropriate code
        sys.exit(0 if summary['satisfied'] else 1)
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Process interrupted by user")
        sys.exit(130)
    except Exception as e:
        print(f"\n✗ Fatal error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
