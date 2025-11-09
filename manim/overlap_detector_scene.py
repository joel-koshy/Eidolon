"""
Overlap Detector Scene Wrapper

This wraps a Manim scene to automatically detect overlaps during rendering.
"""

import sys
import os
import importlib.util
import json
from pathlib import Path

from manim import *
from mobject_analyzer import MobjectAnalyzer


def analyze_scene_with_overlap_detection(script_path: str, scene_name: str = "IntegralExplanation") -> dict:
    """
    Run a Manim scene and detect overlaps at the final state.
    
    Args:
        script_path: Path to the Manim script
        scene_name: Name of the scene class
        
    Returns:
        Overlap analysis report
    """
    print(f"\n🔍 Analyzing mobject overlaps in {script_path}...")
    
    # Import the script module
    spec = importlib.util.spec_from_file_location("manim_script", script_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules["manim_script"] = module
    spec.loader.exec_module(module)
    
    # Get the scene class
    SceneClass = getattr(module, scene_name)
    
    # Create a modified scene that captures mobject states
    class AnalyzingScene(SceneClass):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.mobject_analyzer = MobjectAnalyzer()
            self.overlap_snapshots = []
        
        def wait(self, duration=1, **kwargs):
            """Override wait to capture mobject states."""
            # Capture current state before waiting
            self._capture_mobject_state()
            super().wait(duration, **kwargs)
        
        def play(self, *args, **kwargs):
            """Override play to capture mobject states after animations."""
            super().play(*args, **kwargs)
            # Capture state after animation
            self._capture_mobject_state()
        
        def _capture_mobject_state(self):
            """Capture current mobject positions and check for overlaps."""
            try:
                issues = self.mobject_analyzer.analyze_scene_mobjects(
                    self, 
                    timestamp=self.renderer.time
                )
                if issues:
                    self.overlap_snapshots.append({
                        'timestamp': self.renderer.time,
                        'issues': len(issues),
                        'critical': sum(1 for i in issues if i.severity == 'critical')
                    })
            except Exception as e:
                print(f"Warning: Could not capture mobject state: {e}")
    
    # Render the scene (without actual video output, just construct)
    try:
        print("  Constructing scene...")
        
        # Create a minimal config for analysis
        config.dry_run = True  # Don't actually render
        config.write_to_movie = False
        
        scene = AnalyzingScene()
        scene.render()
        
        # Generate final report
        report = scene.mobject_analyzer.generate_report()
        report['snapshots_analyzed'] = len(scene.overlap_snapshots)
        
        print(f"✓ Analysis complete")
        print(f"  Mobjects analyzed: {report['total_mobjects_analyzed']}")
        print(f"  Overlaps found: {report['total_overlaps']}")
        print(f"    - Critical: {report['critical_overlaps']}")
        print(f"    - Warnings: {report['warning_overlaps']}")
        print(f"    - Minor: {report['minor_overlaps']}")
        print(f"  Overall score: {report['overall_score']}/10")
        
        return report
        
    except Exception as e:
        print(f"✗ Analysis failed: {e}")
        import traceback
        traceback.print_exc()
        return {
            'overall_score': 0,
            'is_satisfactory': False,
            'error': str(e),
            'total_overlaps': 0
        }


# CLI interface
if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Analyze Manim scene for mobject overlaps")
    parser.add_argument("script", help="Path to Manim script")
    parser.add_argument("--scene", default="IntegralExplanation", help="Scene class name")
    parser.add_argument("--output", help="Output JSON file for report")
    
    args = parser.parse_args()
    
    report = analyze_scene_with_overlap_detection(args.script, args.scene)
    
    if args.output:
        with open(args.output, 'w') as f:
            json.dump(report, f, indent=2)
        print(f"\n✓ Report saved to: {args.output}")
    else:
        print("\n" + "="*70)
        print("OVERLAP DETECTION REPORT")
        print("="*70)
        print(json.dumps(report, indent=2))
