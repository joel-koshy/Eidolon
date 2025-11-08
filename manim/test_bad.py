from manim import *

class IntegralExplanation(Scene):
    def construct(self):
        # --- SEVERE PROBLEM 1: Three texts at EXACT same position ---
        # Fixed by positioning texts vertically relative to each other
        # and animating them sequentially.
        text1 = Text("First Title", font_size=48, color=BLUE).to_edge(UP)
        text2 = Text("Second Title", font_size=48, color=RED).next_to(text1, DOWN, buff=0.5)
        text3 = Text("Third Title", font_size=48, color=GREEN).next_to(text2, DOWN, buff=0.5)
        
        self.play(Write(text1))
        self.wait(1) # Added wait to allow reading of the first title
        self.play(Write(text2))
        self.wait(1) # Added wait to allow reading of the second title
        self.play(Write(text3))
        self.wait(2)
        
        # --- SEVERE PROBLEM 2: Four shapes at EXACT same spot ---
        # Fixed by positioning shapes in a grid-like arrangement to prevent overlaps.
        # Original: c1, c2, s1, s2 all at ORIGIN.
        c1 = Circle(radius=1.5, color=RED).shift(LEFT * 3 + UP * 1)
        c2 = Circle(radius=1.3, color=BLUE).shift(RIGHT * 3 + UP * 1)
        s1 = Square(side_length=2, color=GREEN).shift(LEFT * 3 + DOWN * 2)
        s2 = Square(side_length=1.5, color=YELLOW).shift(RIGHT * 3 + DOWN * 2)
        
        # Fade out all titles before bringing in shapes
        self.play(FadeOut(text1, text2, text3))
        self.play(Create(c1))
        self.play(Create(c2))
        self.play(Create(s1))
        self.play(Create(s2))
        self.wait(2)
        
        # --- SEVERE PROBLEM 3: Bottom text pile-up ---
        # Fixed by positioning texts vertically, stacking upwards from the bottom edge.
        # Original: b1, b2, b3 all at to_edge(DOWN).
        b1 = Text("Bottom 1", font_size=36).to_edge(DOWN)
        b2 = Text("Bottom 2", font_size=36).next_to(b1, UP, buff=0.5)
        b3 = Text("Bottom 3", font_size=36).next_to(b2, UP, buff=0.5)
        
        self.play(Write(b1))
        self.play(Write(b2))
        self.play(Write(b3))
        self.wait(2)
        
        # Clear all mobjects from the scene
        self.play(*[FadeOut(mob) for mob in self.mobjects])
        self.wait()