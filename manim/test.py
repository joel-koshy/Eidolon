from manim import *

class IntegralExplanation(Scene):
    def construct(self):
        # ==========================================
        # Scene 1 & 2: The Problem and The Big Idea
        # ==========================================

        # Create axes
        axes = Axes(
            x_range=[0, 6, 1],
            y_range=[0, 8, 1],
            x_length=10,
            y_length=6,
            axis_config={"color": BLUE},
        ).add_coordinates()

        # Define the function
        def func(x):
            return x**2 / 5 + 2  # A simple parabola

        # Create the graph
        graph = axes.plot(func, color=WHITE, x_range=[1, 5])
        graph_label = axes.get_graph_label(graph, label="f(x)")

        # VO: "How do we find the exact area under this curve?"
        self.play(Create(axes), Create(graph), Write(graph_label))
        self.wait(1)

        # Show the area
        area = axes.get_area(graph, x_range=[1, 5], color=BLUE, opacity=0.5)
        area_text = Text("How to find this area?").to_corner(UP + LEFT)
        
        self.play(Create(area), Write(area_text))
        self.wait(2)
        
        # ==========================================
        # Scene 3: A Rough Start (4 rectangles)
        # ==========================================
        
        # VO: "So, let's *try* to fill this shape with rectangles."
        rects_few = axes.get_riemann_rectangles(
            graph, 
            x_range=[1, 5], 
            dx=1.0,  # dx=1.0 gives 4 rectangles
            input_sample_type="left",
            color=(TEAL, RED_B)
        )
        
        approx_text_1 = Text("Approximate with rectangles").to_corner(UP + LEFT)
        self.play(
            FadeOut(area),
            ReplacementTransform(area_text, approx_text_1),
            Create(rects_few)
        )
        
        # VO: "As you can see... it's not very good."
        error_text = Text("Lots of error...", color=RED).next_to(approx_text_1, DOWN)
        self.play(Write(error_text))
        self.wait(2)

        # ==========================================
        # Scene 4: Getting Better (10 rectangles)
        # ==========================================

        # VO: "But what if we use *more* rectangles?"
        rects_more = axes.get_riemann_rectangles(
            graph, 
            x_range=[1, 5], 
            dx=0.4,  # dx=0.4 gives 10 rectangles
            input_sample_type="left",
            color=(TEAL, ORANGE)
        )
        
        approx_text_2 = Text("Use *more* rectangles").to_corner(UP + LEFT)
        self.play(
            FadeOut(rects_few),
            FadeIn(rects_more),
            ReplacementTransform(VGroup(approx_text_1, error_text), approx_text_2)
        )
        self.wait(2)

        # ==========================================
        # Scene 5: The "Limit" (50 rectangles)
        # ==========================================
        
        # VO: "Let's keep going. We'll use more... and more..."
        rects_many = axes.get_riemann_rectangles(
            graph, 
            x_range=[1, 5], 
            dx=0.08,  # dx=0.08 gives 50 rectangles
            input_sample_type="left",
            color=(TEAL_A, GREEN)
        )
        
        approx_text_3 = Text("Infinitely many, infinitely thin...").to_corner(UP + LEFT)
        
        self.play(
            FadeOut(rects_more),
            FadeIn(rects_many),
            ReplacementTransform(approx_text_2, approx_text_3)
        )
        self.wait(2)

        # VO: "...our approximation becomes... *exact*."
        exact_text = Text("The *exact* area").to_corner(UP + LEFT)
        
        self.play(
            FadeOut(rects_many),
            FadeIn(area), # Bring back the smooth area
            ReplacementTransform(approx_text_3, exact_text)
        )
        self.wait(2)

        # ==========================================
        # Scene 6 & 7: The Notation & Conclusion
        # ==========================================
        
        # VO: "This process... is called integration."
        integral_symbol = MathTex(r"\int_{1}^{5} f(x) \,dx")
        integral_symbol.scale(1.5)
        integral_symbol.move_to(axes.c2p(3, 4.5)) # Center it on the graph

        self.play(Write(integral_symbol))
        self.wait(1)

        # VO: "This symbol... is a stretched-out 'S', for 'Sum'."
        self.play(Indicate(integral_symbol[0][0], color=YELLOW)) # Highlight the integral sign
        self.wait(1)

        # VO: "...and this dx represents the *infinitely thin* width..."
        self.play(Indicate(integral_symbol[0][6:8], color=YELLOW)) # Highlight the 'dx'
        self.wait(1)

        # Final scene
        final_text = Text("Integral = Exact Area").to_corner(UP + LEFT)
        self.play(
            ReplacementTransform(exact_text, final_text)
        )
        self.wait(3)
        
        # Fade out everything
        self.play(
            FadeOut(axes),
            FadeOut(graph),
            FadeOut(graph_label),
            FadeOut(area),
            FadeOut(integral_symbol),
            FadeOut(final_text)
        )
        self.wait()