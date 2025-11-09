"""
AI-Powered Manim Video Iterative Improvement System

This script orchestrates an iterative loop:
1. Render video from Manim script
2. Analyze video quality with Gemini Pro
3. Get AI-generated improvements to the script
4. Re-render and repeat until quality threshold is met
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
    extract_json_from_text,
    clean_code_from_response,
    save_iteration,
    find_rendered_video,
    create_summary_report,
    print_progress
)


class VideoImprover:
    """Orchestrates the iterative video improvement process."""
    
    def __init__(
        self,
        script_path: str = "test.py",
        max_iterations: int = 5,
        target_score: float = 8.0,
        use_docker: bool = True
    ):
        """
        Initialize the video improver.
        
        Args:
            script_path: Path to the Manim script
            max_iterations: Maximum number of improvement iterations
            target_score: Target quality score (0-10)
            use_docker: Whether to use Docker for rendering (True) or local Manim (False)
        """
        self.script_path = Path(script_path)
        self.max_iterations = max_iterations
        self.target_score = target_score
        self.use_docker = use_docker
        
        # Setup directories
        self.base_dir = self.script_path.parent
        self.iterations_dir = self.base_dir / "iterations"
        self.rendered_videos_dir = self.base_dir / "rendered_videos"
        self.prompts_dir = self.base_dir / "prompts"
        self.media_dir = self.base_dir / "media"
        
        # Ensure directories exist
        self.iterations_dir.mkdir(exist_ok=True)
        self.rendered_videos_dir.mkdir(exist_ok=True)
        
        # Setup Gemini
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError(
                "GEMINI_API_KEY not found in environment variables. "
                "Run setup_api.py first or set the environment variable."
            )
        
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-2.5-flash')
        
        # Load prompts
        self.analysis_prompt = self._load_prompt("video_analysis_prompt.txt")
        self.improvement_prompt = self._load_prompt("code_improvement_prompt.txt")
        
        print("✓ VideoImprover initialized")
        print(f"  Script: {self.script_path}")
        print(f"  Max iterations: {self.max_iterations}")
        print(f"  Target score: {self.target_score}/10")
        print(f"  Rendering mode: {'Docker' if self.use_docker else 'Local'}")
    
    def _load_prompt(self, filename: str) -> str:
        """Load a prompt template from file."""
        prompt_path = self.prompts_dir / filename
        if not prompt_path.exists():
            raise FileNotFoundError(f"Prompt template not found: {prompt_path}")
        
        with open(prompt_path, 'r', encoding='utf-8') as f:
            return f.read()
    
    def render_video(self) -> Optional[str]:
        """
        Render the Manim video using Docker or local installation.
        
        Returns:
            Path to rendered video or None if rendering failed
        """
        print("\n📹 Rendering video...")
        
        try:
            if self.use_docker:
                return self._render_with_docker()
            else:
                return self._render_local()
        except Exception as e:
            print(f"✗ Rendering failed: {e}")
            return None
    
    def _render_with_docker(self) -> Optional[str]:
        """Render video using Docker container."""
        # Build command to run Manim in Docker
        cmd = [
            "docker", "run", "--rm",
            "-v", f"{self.base_dir.absolute()}:/manim",
            "manim-container",  # Assumes you've built the Docker image with this name
            "manim", "-pql", "test.py", "IntegralExplanation"
        ]
        
        print(f"  Running: {' '.join(cmd)}")
        
        result = subprocess.run(
            cmd,
            cwd=str(self.base_dir),
            capture_output=True,
            text=True
        )
        
        if result.returncode != 0:
            print(f"✗ Docker rendering failed:")
            print(result.stderr)
            return None
        
        # Find the rendered video
        video_path = find_rendered_video(str(self.media_dir))
        
        if video_path:
            print(f"✓ Video rendered: {video_path}")
            return video_path
        else:
            print("✗ Could not find rendered video")
            return None
    
    def _render_local(self) -> Optional[str]:
        """Render video using local Manim installation."""
        cmd = ["manim", "-pql", str(self.script_path), "IntegralExplanation"]
        
        print(f"  Running: {' '.join(cmd)}")
        
        result = subprocess.run(
            cmd,
            cwd=str(self.base_dir),
            capture_output=True,
            text=True
        )
        
        if result.returncode != 0:
            print(f"✗ Local rendering failed:")
            print(result.stderr)
            return None
        
        # Find the rendered video
        video_path = find_rendered_video(str(self.media_dir))
        
        if video_path:
            print(f"✓ Video rendered: {video_path}")
            return video_path
        else:
            print("✗ Could not find rendered video")
            return None
    
    def analyze_video(self, video_path: str) -> Optional[Dict]:
        """
        Analyze video quality using Gemini Pro.
        
        Args:
            video_path: Path to video file
            
        Returns:
            Analysis feedback as dictionary or None if analysis failed
        """
        print("\n🔍 Analyzing video with Gemini Pro...")
        
        try:
            # Upload video file
            print("  Uploading video to Gemini...")
            video_file = genai.upload_file(path=video_path)
            
            # Wait for video to be processed
            while video_file.state.name == "PROCESSING":
                print("  Processing video...")
                time.sleep(2)
                video_file = genai.get_file(video_file.name)
            
            if video_file.state.name == "FAILED":
                raise Exception("Video processing failed")
            
            print("  Generating analysis...")
            
            # Generate analysis
            response = self.model.generate_content(
                [video_file, self.analysis_prompt],
                request_options={"timeout": 120}
            )
            
            # Extract JSON from response
            feedback = extract_json_from_text(response.text)
            
            if not feedback:
                print("✗ Failed to parse feedback JSON")
                print(f"  Raw response: {response.text[:200]}...")
                return None
            
            print(f"✓ Analysis complete")
            print(f"  Overall score: {feedback.get('overall_score', 0)}/10")
            print(f"  Satisfactory: {feedback.get('is_satisfactory', False)}")
            
            return feedback
            
        except Exception as e:
            print(f"✗ Analysis failed: {e}")
            return None
    
    def improve_code(self, current_code: str, feedback: Dict, iteration: int) -> Optional[str]:
        """
        Generate improved Manim code based on feedback.
        
        Args:
            current_code: Current Manim script code
            feedback: Analysis feedback dictionary
            iteration: Current iteration number
            
        Returns:
            Improved code or None if generation failed
        """
        print("\n🔧 Generating improved code with Gemini...")
        
        try:
            # Format the improvement prompt
            priority_improvements = "\n".join([
                f"{i+1}. {item}"
                for i, item in enumerate(feedback.get("priority_improvements", []))
            ])
            
            prompt = self.improvement_prompt.format(
                iteration=iteration,
                previous_score=feedback.get("overall_score", 0),
                feedback=json.dumps(feedback, indent=2),
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
                print("  Attempting to fix...")
                # Could add retry logic here
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
    
    def run(self) -> Dict:
        """
        Run the iterative improvement loop.
        
        Returns:
            Summary report dictionary
        """
        print("\n" + "=" * 70)
        print("  🚀 STARTING ITERATIVE VIDEO IMPROVEMENT")
        print("=" * 70)
        
        # Read initial code
        with open(self.script_path, 'r', encoding='utf-8') as f:
            current_code = f.read()
        
        for iteration in range(1, self.max_iterations + 1):
            print_progress(iteration, 0, self.max_iterations)
            
            # Render video
            video_path = self.render_video()
            if not video_path:
                print("⚠️  Rendering failed, stopping iteration")
                break
            
            # Copy video to rendered_videos folder
            video_copy = self.rendered_videos_dir / f"video_iteration_{iteration:02d}.mp4"
            shutil.copy2(video_path, video_copy)
            print(f"  Saved video to: {video_copy}")
            
            # Analyze video
            feedback = self.analyze_video(video_path)
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
            
            # Brief pause between iterations
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
        description="AI-Powered Manim Video Iterative Improvement"
    )
    parser.add_argument(
        "--script",
        default="test.py",
        help="Path to Manim script (default: test.py)"
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
    parser.add_argument(
        "--no-docker",
        action="store_true",
        help="Use local Manim instead of Docker"
    )
    
    args = parser.parse_args()
    
    try:
        improver = VideoImprover(
            script_path=args.script,
            max_iterations=args.max_iterations,
            target_score=args.target_score,
            use_docker=not args.no_docker
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
