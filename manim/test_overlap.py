from manim import *
import numpy as np

class IntegralExplanation(Scene):
    def construct(self):
        # PROBLEM 1: Multiple texts at same position
        # Fix: Position title1 with a buffer from the top edge.
        # Then, position title2 below title1 with a buffer to prevent overlap.
        title1 = Text("Understanding Calculus", font_size=48, color=BLUE).to_edge(UP, buff=0.5)
        title2 = Text("Mathematical Concepts", font_size=44, color=RED).next_to(title1, DOWN, buff=0.5)
        
        self.play(Write(title1))
        self.wait(1)
        self.play(Write(title2))
        self.wait(2)
        
        # PROBLEM 2: Overlapping conclusion texts
        # Fix: Position conclusion1 with a buffer from the bottom edge.
        # Then, position conclusion2 above conclusion1 with a buffer to prevent overlap.
        conclusion1 = Text("Mathematical Beauty", font_size=36).to_edge(DOWN, buff=0.5)
        conclusion2 = Text("Geometric Elegance", font_size=32).next_to(conclusion1, UP, buff=0.5)
        
        self.play(Write(conclusion1))
        self.wait(1)
        self.play(Write(conclusion2))
        self.wait(2)
        
        # PROBLEM 3: Objects at same center position (implied by 12.0s critical overlaps)
        # Fix: Move circle to the left and square to the right to prevent overlap.
        self.play(FadeOut(title1), FadeOut(title2), FadeOut(conclusion1), FadeOut(conclusion2))
        circle = Circle(radius=1, color=RED).shift(LEFT * 1.5) # Shift left to separate
        square = Square(side_length=2, color=BLUE).shift(RIGHT * 1.5) # Shift right to separate
        
        self.play(Create(circle))
        self.play(Create(square))
        self.wait(2)
        
        # Cleanup
        self.play(*[FadeOut(mob) for mob in self.mobjects])
        self.wait()