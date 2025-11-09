"""
Mobject Overlap Detector

Hooks into Manim's rendering to capture actual mobject positions and detect overlaps.
This provides pixel-perfect collision detection without analyzing video frames.
"""

import numpy as np
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
import json


@dataclass
class BoundingBox:
    """Represents a 2D bounding box for a mobject."""
    x_min: float
    x_max: float
    y_min: float
    y_max: float
    mobject_name: str
    mobject_type: str
    center: Tuple[float, float]
    
    def overlaps_with(self, other: 'BoundingBox', threshold: float = 0.1) -> bool:
        """Check if this bounding box overlaps with another."""
        # Add small threshold to avoid detecting touching edges as overlaps
        x_overlap = (self.x_min < other.x_max - threshold and 
                     self.x_max > other.x_min + threshold)
        y_overlap = (self.y_min < other.y_max - threshold and 
                     self.y_max > other.y_min + threshold)
        return x_overlap and y_overlap
    
    def overlap_area(self, other: 'BoundingBox') -> float:
        """Calculate the area of overlap with another bounding box."""
        if not self.overlaps_with(other):
            return 0.0
        
        x_overlap = min(self.x_max, other.x_max) - max(self.x_min, other.x_min)
        y_overlap = min(self.y_max, other.y_max) - max(self.y_min, other.y_min)
        return x_overlap * y_overlap
    
    def area(self) -> float:
        """Calculate the area of this bounding box."""
        return (self.x_max - self.x_min) * (self.y_max - self.y_min)
    
    def overlap_percentage(self, other: 'BoundingBox') -> float:
        """Calculate what percentage of this box overlaps with another."""
        overlap = self.overlap_area(other)
        if overlap == 0:
            return 0.0
        return (overlap / self.area()) * 100


@dataclass
class OverlapIssue:
    """Represents a detected overlap between two mobjects."""
    mobject1: str
    mobject2: str
    overlap_percentage: float
    severity: str  # 'critical', 'warning', 'minor'
    timestamp: float
    suggestion: str


class MobjectAnalyzer:
    """Analyzes mobjects in a Manim scene for overlaps."""
    
    def __init__(self):
        self.bounding_boxes: List[BoundingBox] = []
        self.overlap_issues: List[OverlapIssue] = []
        self.current_timestamp = 0.0
    
    def get_bounding_box(self, mobject, name: str = None) -> BoundingBox:
        """
        Extract bounding box from a Manim mobject.
        
        Args:
            mobject: Manim mobject
            name: Optional name for the mobject
            
        Returns:
            BoundingBox object
        """
        try:
            # Get all points that define the mobject
            points = mobject.get_all_points()
            
            if len(points) == 0:
                # No points, use center and estimate size
                center = mobject.get_center()
                return BoundingBox(
                    x_min=center[0] - 0.1,
                    x_max=center[0] + 0.1,
                    y_min=center[1] - 0.1,
                    y_max=center[1] + 0.1,
                    mobject_name=name or str(type(mobject).__name__),
                    mobject_type=type(mobject).__name__,
                    center=(center[0], center[1])
                )
            
            # Calculate bounding box from points
            x_coords = points[:, 0]
            y_coords = points[:, 1]
            
            x_min, x_max = float(np.min(x_coords)), float(np.max(x_coords))
            y_min, y_max = float(np.min(y_coords)), float(np.max(y_coords))
            
            center = mobject.get_center()
            
            return BoundingBox(
                x_min=x_min,
                x_max=x_max,
                y_min=y_min,
                y_max=y_max,
                mobject_name=name or str(type(mobject).__name__),
                mobject_type=type(mobject).__name__,
                center=(float(center[0]), float(center[1]))
            )
            
        except Exception as e:
            print(f"Warning: Could not get bounding box for {name}: {e}")
            return None
    
    def analyze_scene_mobjects(self, scene, timestamp: float = 0.0) -> List[OverlapIssue]:
        """
        Analyze all mobjects in a scene for overlaps.
        
        Args:
            scene: Manim Scene object
            timestamp: Current animation timestamp
            
        Returns:
            List of detected overlap issues
        """
        self.current_timestamp = timestamp
        self.bounding_boxes = []
        issues = []
        
        # Get all mobjects currently in the scene
        mobjects = scene.mobjects
        
        # Extract bounding boxes for all visible mobjects
        for i, mob in enumerate(mobjects):
            # Skip if mobject is not visible or has no points
            try:
                if hasattr(mob, 'get_opacity') and mob.get_opacity() == 0:
                    continue
                
                name = getattr(mob, 'name', None) or f"{type(mob).__name__}_{i}"
                bbox = self.get_bounding_box(mob, name)
                
                if bbox and bbox.area() > 0.01:  # Ignore very small objects
                    self.bounding_boxes.append(bbox)
            except Exception as e:
                continue
        
        # Check for overlaps between all pairs of bounding boxes
        for i, bbox1 in enumerate(self.bounding_boxes):
            for j, bbox2 in enumerate(self.bounding_boxes[i+1:], i+1):
                overlap_pct = bbox1.overlap_percentage(bbox2)
                
                if overlap_pct > 5:  # More than 5% overlap
                    # Determine severity
                    if overlap_pct > 50:
                        severity = 'critical'
                    elif overlap_pct > 20:
                        severity = 'warning'
                    else:
                        severity = 'minor'
                    
                    # Generate suggestion
                    suggestion = self._generate_suggestion(bbox1, bbox2, overlap_pct)
                    
                    issue = OverlapIssue(
                        mobject1=bbox1.mobject_name,
                        mobject2=bbox2.mobject_name,
                        overlap_percentage=overlap_pct,
                        severity=severity,
                        timestamp=timestamp,
                        suggestion=suggestion
                    )
                    issues.append(issue)
        
        self.overlap_issues.extend(issues)
        return issues
    
    def _generate_suggestion(self, bbox1: BoundingBox, bbox2: BoundingBox, overlap_pct: float) -> str:
        """Generate a helpful suggestion for fixing the overlap."""
        # Determine relative positions
        dx = bbox2.center[0] - bbox1.center[0]
        dy = bbox2.center[1] - bbox1.center[1]
        
        if abs(dx) > abs(dy):
            # Horizontal overlap
            direction = "right" if dx > 0 else "left"
            return f"Move {bbox2.mobject_name} further {direction}, or use .next_to() with larger buff parameter"
        else:
            # Vertical overlap
            direction = "up" if dy > 0 else "down"
            return f"Move {bbox2.mobject_name} further {direction}, or adjust vertical spacing"
    
    def generate_report(self) -> Dict:
        """
        Generate a comprehensive overlap report.
        
        Returns:
            Dictionary with analysis results
        """
        # Count issues by severity
        critical_count = sum(1 for i in self.overlap_issues if i.severity == 'critical')
        warning_count = sum(1 for i in self.overlap_issues if i.severity == 'warning')
        minor_count = sum(1 for i in self.overlap_issues if i.severity == 'minor')
        
        # Calculate score
        base_score = 10.0
        score = base_score - (critical_count * 2) - (warning_count * 0.8) - (minor_count * 0.3)
        score = max(0, min(10, score))
        
        # Group issues by type
        issues_by_severity = {
            'critical': [],
            'warning': [],
            'minor': []
        }
        
        for issue in self.overlap_issues:
            issues_by_severity[issue.severity].append({
                'mobject1': issue.mobject1,
                'mobject2': issue.mobject2,
                'overlap_percentage': round(issue.overlap_percentage, 1),
                'timestamp': issue.timestamp,
                'suggestion': issue.suggestion
            })
        
        # Priority improvements
        priority_improvements = []
        for issue in sorted(self.overlap_issues, 
                          key=lambda x: (x.severity != 'critical', -x.overlap_percentage))[:3]:
            priority_improvements.append(issue.suggestion)
        
        return {
            'overall_score': round(score, 1),
            'is_satisfactory': score >= 8.0 and critical_count == 0,
            'analysis_type': 'mobject_overlap_detection',
            'total_overlaps': len(self.overlap_issues),
            'critical_overlaps': critical_count,
            'warning_overlaps': warning_count,
            'minor_overlaps': minor_count,
            'total_mobjects_analyzed': len(self.bounding_boxes),
            'issues_by_severity': issues_by_severity,
            'priority_improvements': priority_improvements,
            'detailed_issues': [
                {
                    'severity': i.severity,
                    'mobject1': i.mobject1,
                    'mobject2': i.mobject2,
                    'overlap': f"{i.overlap_percentage:.1f}%",
                    'timestamp': i.timestamp,
                    'suggestion': i.suggestion
                }
                for i in self.overlap_issues
            ]
        }


def analyze_scene_for_overlaps(scene) -> Dict:
    """
    Convenience function to analyze a scene for overlaps.
    
    Args:
        scene: Manim Scene object
        
    Returns:
        Analysis report dictionary
    """
    analyzer = MobjectAnalyzer()
    analyzer.analyze_scene_mobjects(scene)
    return analyzer.generate_report()


# Test function
if __name__ == "__main__":
    print("Mobject Analyzer - Use this with a Manim scene")
    print("Example usage:")
    print("  from mobject_analyzer import MobjectAnalyzer")
    print("  analyzer = MobjectAnalyzer()")
    print("  issues = analyzer.analyze_scene_mobjects(self)")
    print("  report = analyzer.generate_report()")
