"""
Static Code Analyzer for Manim Scripts

Analyzes Manim code to detect potential issues WITHOUT rendering:
- Overlapping text/objects
- Poor positioning choices
- Timing issues
- Readability problems
- Code structure issues
"""

import ast
import re
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass


@dataclass
class CodeIssue:
    """Represents a detected issue in the code."""
    severity: str  # 'critical', 'warning', 'info'
    category: str  # 'overlap', 'positioning', 'timing', 'readability'
    line_number: int
    description: str
    suggestion: str


class ManimCodeAnalyzer:
    """Analyzes Manim code for potential visual and structural issues."""
    
    def __init__(self, code: str):
        self.code = code
        self.lines = code.split('\n')
        self.issues: List[CodeIssue] = []
        
        # Parse the AST
        try:
            self.tree = ast.parse(code)
        except SyntaxError as e:
            self.tree = None
            self.issues.append(CodeIssue(
                severity='critical',
                category='syntax',
                line_number=e.lineno or 0,
                description=f"Syntax error: {e.msg}",
                suggestion="Fix syntax errors before analyzing"
            ))
    
    def analyze(self) -> Dict:
        """Run all analysis checks and return results."""
        if not self.tree:
            return self._format_results()
        
        # Run all checks
        self._check_text_positioning()
        self._check_font_sizes()
        self._check_wait_times()
        self._check_color_choices()
        self._check_scene_complexity()
        self._check_animation_timing()
        self._check_object_lifecycle()
        self._check_positioning_patterns()
        
        return self._format_results()
    
    def _check_text_positioning(self):
        """Check for text positioned in similar locations (potential overlap)."""
        text_positions = []
        
        for node in ast.walk(self.tree):
            if isinstance(node, ast.Call):
                # Check for Text() objects
                if (hasattr(node.func, 'id') and node.func.id == 'Text') or \
                   (hasattr(node.func, 'attr') and node.func.attr in ['to_edge', 'to_corner', 'next_to']):
                    
                    line_num = node.lineno
                    
                    # Check for .to_edge(UP) or .to_corner(UP + LEFT)
                    if hasattr(node.func, 'attr'):
                        if node.func.attr in ['to_edge', 'to_corner']:
                            text_positions.append((line_num, node.func.attr))
        
        # Check for multiple texts using same positioning
        position_counts = {}
        for line_num, position in text_positions:
            key = f"{position}"
            if key not in position_counts:
                position_counts[key] = []
            position_counts[key].append(line_num)
        
        for position, lines in position_counts.items():
            if len(lines) > 2:
                self.issues.append(CodeIssue(
                    severity='warning',
                    category='overlap',
                    line_number=lines[-1],
                    description=f"Multiple text objects using {position} positioning (potential overlap)",
                    suggestion=f"Consider using different positions or clearing previous text for lines: {lines}"
                ))
    
    def _check_font_sizes(self):
        """Check for font sizes that might be too small or too large."""
        for line_num, line in enumerate(self.lines, 1):
            # Look for font_size parameter
            if 'font_size' in line:
                match = re.search(r'font_size\s*=\s*(\d+)', line)
                if match:
                    size = int(match.group(1))
                    
                    if size < 24:
                        self.issues.append(CodeIssue(
                            severity='warning',
                            category='readability',
                            line_number=line_num,
                            description=f"Font size {size} is very small (may be hard to read)",
                            suggestion="Consider using font_size >= 32 for better readability"
                        ))
                    elif size > 72:
                        self.issues.append(CodeIssue(
                            severity='info',
                            category='readability',
                            line_number=line_num,
                            description=f"Font size {size} is very large (may overflow screen)",
                            suggestion="Consider using font_size <= 64 unless emphasizing"
                        ))
    
    def _check_wait_times(self):
        """Check for wait times that might be too short or too long."""
        for line_num, line in enumerate(self.lines, 1):
            if 'self.wait(' in line:
                match = re.search(r'self\.wait\((\d+(?:\.\d+)?)\)', line)
                if match:
                    wait_time = float(match.group(1))
                    
                    if wait_time < 0.5:
                        self.issues.append(CodeIssue(
                            severity='info',
                            category='timing',
                            line_number=line_num,
                            description=f"Very short wait time ({wait_time}s) - animation may feel rushed",
                            suggestion="Consider wait times of at least 1-2 seconds for viewer comprehension"
                        ))
                    elif wait_time > 5:
                        self.issues.append(CodeIssue(
                            severity='warning',
                            category='timing',
                            line_number=line_num,
                            description=f"Very long wait time ({wait_time}s) - may feel slow",
                            suggestion="Consider breaking long waits into smaller segments with visual cues"
                        ))
    
    def _check_color_choices(self):
        """Check for potentially problematic color combinations."""
        problematic_colors = {
            'YELLOW': ['WHITE', 'LIGHT_GRAY'],
            'WHITE': ['YELLOW', 'LIGHT_GRAY'],
            'BLUE': ['BLACK'],
        }
        
        colors_used = []
        for line_num, line in enumerate(self.lines, 1):
            if 'color=' in line or 'color =' in line:
                for color in problematic_colors.keys():
                    if color in line:
                        colors_used.append((line_num, color))
        
        # Check for potential contrast issues
        for i, (line1, color1) in enumerate(colors_used):
            for line2, color2 in colors_used[i+1:i+3]:  # Check next 2 colors
                if color2 in problematic_colors.get(color1, []):
                    self.issues.append(CodeIssue(
                        severity='info',
                        category='readability',
                        line_number=line2,
                        description=f"Color {color2} near {color1} may have poor contrast",
                        suggestion=f"Consider using higher contrast colors between lines {line1} and {line2}"
                    ))
    
    def _check_scene_complexity(self):
        """Check if scene has too many objects created without cleanup."""
        create_count = 0
        fadeout_count = 0
        
        for line in self.lines:
            if 'Create(' in line or 'Write(' in line:
                create_count += 1
            if 'FadeOut(' in line:
                fadeout_count += 1
        
        if create_count - fadeout_count > 10:
            self.issues.append(CodeIssue(
                severity='warning',
                category='complexity',
                line_number=len(self.lines),
                description=f"Scene creates {create_count} objects but only fades out {fadeout_count}",
                suggestion="Consider fading out objects when no longer needed to reduce visual clutter"
            ))
    
    def _check_animation_timing(self):
        """Check for animations with very short or missing run_time."""
        for line_num, line in enumerate(self.lines, 1):
            if 'self.play(' in line and 'run_time' not in line:
                # Check if it's a complex animation
                if 'ReplacementTransform' in line or 'VGroup' in line:
                    self.issues.append(CodeIssue(
                        severity='info',
                        category='timing',
                        line_number=line_num,
                        description="Complex animation without explicit run_time",
                        suggestion="Consider adding run_time parameter for better control"
                    ))
    
    def _check_object_lifecycle(self):
        """Check for objects that are created but never displayed."""
        created_objects = set()
        used_objects = set()
        
        for node in ast.walk(self.tree):
            if isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name):
                        created_objects.add(target.id)
            
            if isinstance(node, ast.Call):
                if hasattr(node.func, 'attr') and node.func.attr in ['play', 'add']:
                    for arg in node.args:
                        if isinstance(arg, ast.Name):
                            used_objects.add(arg.id)
        
        unused = created_objects - used_objects
        # Filter out common variables
        unused = {obj for obj in unused if obj not in ['self', 't', 'x', 'y', 'i']}
        
        if unused:
            self.issues.append(CodeIssue(
                severity='info',
                category='optimization',
                line_number=0,
                description=f"Objects created but never displayed: {', '.join(list(unused)[:5])}",
                suggestion="Remove unused objects or add them to the scene"
            ))
    
    def _check_positioning_patterns(self):
        """Check for common positioning mistakes."""
        for line_num, line in enumerate(self.lines, 1):
            # Check for objects positioned at ORIGIN without explicit placement
            if '.move_to(ORIGIN)' in line:
                self.issues.append(CodeIssue(
                    severity='info',
                    category='positioning',
                    line_number=line_num,
                    description="Object explicitly moved to ORIGIN (center)",
                    suggestion="Consider if this is intentional - may overlap with other centered objects"
                ))
            
            # Check for next_to without buffer
            if 'next_to(' in line and 'buff=' not in line:
                if 'Text' in self.lines[line_num - 1] if line_num > 0 else False:
                    self.issues.append(CodeIssue(
                        severity='info',
                        category='positioning',
                        line_number=line_num,
                        description="Using next_to without explicit buffer",
                        suggestion="Consider adding buff parameter for better spacing (e.g., buff=0.5)"
                    ))
    
    def _format_results(self) -> Dict:
        """Format analysis results into a structured dictionary."""
        # Calculate score based on issues
        critical_count = sum(1 for i in self.issues if i.severity == 'critical')
        warning_count = sum(1 for i in self.issues if i.severity == 'warning')
        info_count = sum(1 for i in self.issues if i.severity == 'info')
        
        # Score calculation
        base_score = 10.0
        score = base_score - (critical_count * 2) - (warning_count * 0.5) - (info_count * 0.1)
        score = max(0, min(10, score))  # Clamp between 0 and 10
        
        # Group issues by category
        issues_by_category = {}
        for issue in self.issues:
            if issue.category not in issues_by_category:
                issues_by_category[issue.category] = []
            issues_by_category[issue.category].append({
                'severity': issue.severity,
                'line': issue.line_number,
                'description': issue.description,
                'suggestion': issue.suggestion
            })
        
        # Priority improvements
        priority_improvements = []
        for issue in sorted(self.issues, key=lambda x: (x.severity != 'critical', x.severity != 'warning')):
            if len(priority_improvements) < 3:
                priority_improvements.append(issue.suggestion)
        
        return {
            'overall_score': round(score, 1),
            'is_satisfactory': score >= 8.0,
            'analysis_type': 'static_code_analysis',
            'total_issues': len(self.issues),
            'critical_issues': critical_count,
            'warnings': warning_count,
            'info_items': info_count,
            'issues_by_category': issues_by_category,
            'priority_improvements': priority_improvements,
            'detailed_issues': [
                {
                    'severity': i.severity,
                    'category': i.category,
                    'line': i.line_number,
                    'description': i.description,
                    'suggestion': i.suggestion
                }
                for i in self.issues
            ]
        }


def analyze_manim_code(code: str) -> Dict:
    """
    Analyze Manim code for potential issues.
    
    Args:
        code: Manim Python code as string
        
    Returns:
        Analysis results dictionary
    """
    analyzer = ManimCodeAnalyzer(code)
    return analyzer.analyze()


# Test function
if __name__ == "__main__":
    # Test with sample code
    test_code = """
from manim import *

class TestScene(Scene):
    def construct(self):
        text1 = Text("Hello", font_size=20).to_edge(UP)
        text2 = Text("World", font_size=80).to_edge(UP)
        self.play(Write(text1))
        self.wait(0.1)
        self.play(Write(text2))
        self.wait(10)
    """
    
    results = analyze_manim_code(test_code)
    
    import json
    print(json.dumps(results, indent=2))
