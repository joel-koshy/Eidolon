from manim import *
import numpy as np

class IntegralExplanation(Scene):
    def construct(self):
        # PROBLEM 1: Multiple texts at same position (complete overlap)
        title1 = Text("Understanding Calculus", font_size=48, color=BLUE).to_edge(UP)
        # Fix: Position title2 relative to title1 to avoid overlap.
        title2 = Text("Mathematical Concepts", font_size=44, color=RED).next_to(title1, DOWN, buff=SMALL_BUFF)
        
        self.play(Write(title1))
        self.wait(1)
        self.play(Write(title2))
        self.wait(2)
        
        # PROBLEM 2: Text too close to other elements
        subtitle = Text("Introduction to Derivatives", font_size=36, color=GREEN)
        subtitle.to_edge(UP) # Place subtitle at the top
        
        self.play(FadeOut(title1), FadeOut(title2))
        self.play(Write(subtitle))
        self.wait(1)
        
        # PROBLEM 3: Axes and labels overlapping
        axes = Axes(
            x_range=[-3, 3, 1],
            y_range=[-2, 2, 1],
            x_length=8,
            y_length=5,
            axis_config={"color": BLUE}
        )
        # Fix: Position axes below the subtitle to avoid overlap.
        axes.next_to(subtitle, DOWN, buff=MED_BUFF)
        
        # PROBLEM 4: Labels with no spacing (not explicitly listed as critical overlap, so minimal change)
        x_label = Text("x", font_size=32).next_to(axes.x_axis, RIGHT)
        y_label = Text("y", font_size=32).next_to(axes.y_axis, UP)
        
        self.play(Create(axes), Write(x_label), Write(y_label))
        self.wait(1)
        
        # PROBLEM 5: Function and explanation overlapping
        graph = axes.plot(lambda x: x**2, color=YELLOW)
        equation = MathTex(r"f(x) = x^2", font_size=40)
        equation.move_to(ORIGIN) # Center position
        
        explanation = Text("This is a parabola", font_size=32, color=ORANGE)
        # Fix: Position explanation below the equation to avoid overlap.
        explanation.next_to(equation, DOWN, buff=MED_BUFF)
        
        self.play(Create(graph))
        self.play(Write(equation))
        self.wait(1)
        self.play(Write(explanation))
        self.wait(2)
        
        # PROBLEM 6: Multiple objects at center (not explicitly listed as critical overlap, so minimal change)
        circle = Circle(radius=1, color=RED).move_to(ORIGIN)
        square = Square(side_length=2, color=BLUE).move_to(ORIGIN)
        triangle = Triangle().move_to(ORIGIN)
        
        self.play(FadeOut(graph), FadeOut(equation), FadeOut(explanation))
        self.play(Create(circle))
        self.play(Create(square))
        self.play(Create(triangle))
        self.wait(2)
        
        # PROBLEM 7: Bottom text too close
        conclusion1 = Text("Mathematical Beauty", font_size=36).to_edge(DOWN)
        # Fix: Position conclusion2 above conclusion1 to avoid overlap.
        conclusion2 = Text("Geometric Elegance", font_size=32).next_to(conclusion1, UP, buff=SMALL_BUFF)
        
        self.play(Write(conclusion1))
        self.wait(1)
        self.play(Write(conclusion2))
        self.wait(2)
        
        # Cleanup
        self.play(*[FadeOut(mob) for mob in self.mobjects])
        self.wait()