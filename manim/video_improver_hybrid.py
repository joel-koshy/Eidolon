"""
Hybrid Video Improver - Code Analysis First

This version uses STATIC CODE ANALYSIS instead of video rendering for speed:
1. Analyze code directly (no rendering needed - instant!)
2. Use Gemini to fix code based on static analysis
3. Only render final video to verify

Benefits:
- 10x faster (no rendering between iterations)
- Cheaper (smaller API calls)
- More precise (exact line numbers and issues)
- Better for overlap detection
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

from code_analyzer import analyze_manim_code


class HybridVideoImprover:
    """Orchestrates the hybrid improvement process using code analysis."""
    
    def __init__(
        self,
        script_path: str = "test.py",
        max_iterations: int = 5,
        target_score: float = 8.0,
        use_docker: bool = True,
        render_final_only: bool = True
    ):
        """
        Initialize the hybrid video improver.
        
        Args:
            script_path: Path to the Manim script
            max_iterations: Maximum number of improvement iterations
            target_score: Target quality score (0-10)
            use_docker: Whether to use Docker for rendering
            render_final_only: Only render after final iteration (much faster)
        """
        self.script_path = Path(script_path)
        self.max_iterations = max_iterations
        self.target_score = target_score
        self.use_docker = use_docker
        self.render_final_only = render_final_only
        
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
        
        # Load code improvement prompt
        self.improvement_prompt = self._load_prompt("code_improvement_prompt.txt")
        
        print("✓ Hybrid VideoImprover initialized")
        print(f"  Script: {self.script_path}")
        print(f"  Max iterations: {self.max_iterations}")
        print(f"  Target score: {self.target_score}/10")
        print(f"  Analysis mode: CODE ANALYSIS (fast)")
        print(f"  Render mode: {'Final only' if self.render_final_only else 'Every iteration'}")
    
    def _load_prompt(self, filename: str) -> str:
        """Load a prompt template from file."""
        prompt_path = self.prompts_dir / filename
        if not prompt_path.exists():
            raise FileNotFoundError(f"Prompt template not found: {prompt_path}")
        
        with open(prompt_path, 'r', encoding='utf-8') as f:
            return f.read()
    
    def render_video(self) -> Optional[str]:
        """Render the Manim video using local installation."""
        print("\n📹 Rendering video...")
        
        try:
            cmd = ["manim", "-pql", str(self.script_path), "IntegralExplanation"]
            
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
                return video_path
            else:
                print("✗ Could not find rendered video")
                return None
                
        except Exception as e:
            print(f"✗ Rendering failed: {e}")
            return None
    
    def analyze_code(self, code: str) -> Dict:
        """
        Analyze code statically for issues.
        
        Args:
            code: Python code as string
            
        Returns:
            Analysis feedback as dictionary
        """
        print("\n🔍 Analyzing code (static analysis)...")
        
        try:
            feedback = analyze_manim_code(code)
            
            print(f"✓ Analysis complete")
            print(f"  Overall score: {feedback.get('overall_score', 0)}/10")
            print(f"  Issues found: {feedback.get('total_issues', 0)}")
            print(f"    - Critical: {feedback.get('critical_issues', 0)}")
            print(f"    - Warnings: {feedback.get('warnings', 0)}")
            print(f"    - Info: {feedback.get('info_items', 0)}")
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
            # Format the improvement prompt with code analysis results
            priority_improvements = "\n".join([
                f"{i+1}. {item}"
                for i, item in enumerate(feedback.get("priority_improvements", []))
            ])
            
            # Create detailed feedback text from code analysis
            detailed_feedback = f"""
CODE ANALYSIS RESULTS:
- Overall Score: {feedback.get('overall_score', 0)}/10
- Total Issues: {feedback.get('total_issues', 0)}
- Critical: {feedback.get('critical_issues', 0)}
- Warnings: {feedback.get('warnings', 0)}
- Info: {feedback.get('info_items', 0)}

DETAILED ISSUES:
"""
            for issue in feedback.get('detailed_issues', []):
                detailed_feedback += f"\nLine {issue['line']} [{issue['severity'].upper()}] {issue['category']}:\n"
                detailed_feedback += f"  Problem: {issue['description']}\n"
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
    
    def run(self) -> Dict:
        """
        Run the hybrid improvement loop.
        
        Returns:
            Summary report dictionary
        """
        print("\n" + "=" * 70)
        print("  🚀 STARTING HYBRID VIDEO IMPROVEMENT")
        print("  (Code Analysis Mode - Super Fast!)")
        print("=" * 70)
        
        # Read initial code
        with open(self.script_path, 'r', encoding='utf-8') as f:
            current_code = f.read()
        
        for iteration in range(1, self.max_iterations + 1):
            print_progress(iteration, 0, self.max_iterations)
            
            # Analyze code (NO RENDERING!)
            feedback = self.analyze_code(current_code)
            if not feedback:
                print("⚠️  Analysis failed, stopping iteration")
                break
            
            # Save iteration (without video for now)
            save_iteration(
                iteration,
                current_code,
                "",  # No video path yet
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
                
                # Render final video
                if not self.render_final_only or iteration == 1:
                    print("\n📹 Rendering final video...")
                    video_path = self.render_video()
                    if video_path:
                        # Copy to rendered_videos
                        video_copy = self.rendered_videos_dir / f"video_final.mp4"
                        shutil.copy2(video_path, video_copy)
                        print(f"  ✓ Final video: {video_copy}")
                break
            
            # Check if this is the last iteration
            if iteration >= self.max_iterations:
                print("⚠️  Maximum iterations reached")
                # Render final attempt
                print("\n📹 Rendering final video...")
                video_path = self.render_video()
                if video_path:
                    video_copy = self.rendered_videos_dir / f"video_final.mp4"
                    shutil.copy2(video_path, video_copy)
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
            time.sleep(1)
        
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
        description="Hybrid AI-Powered Manim Video Improvement (Code Analysis Mode)"
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
        "--render-all",
        action="store_true",
        help="Render video at each iteration (slower)"
    )
    
    args = parser.parse_args()
    
    try:
        improver = HybridVideoImprover(
            script_path=args.script,
            max_iterations=args.max_iterations,
            target_score=args.target_score,
            use_docker=False,
            render_final_only=not args.render_all
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
