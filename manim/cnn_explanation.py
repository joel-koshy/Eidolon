from manim import *
import numpy as np

class IntegralExplanation(Scene):
    def construct(self):
        # Initialize a variable to keep track of the current main header label
        current_header_label = Mobject() # Placeholder mobject

        # Title
        title = Text("Convolutional Neural Networks", font_size=48, color=BLUE)
        subtitle = Text("How CNNs See Images", font_size=32, color=YELLOW)
        
        # Position title at the top edge with a buffer
        title.to_edge(UP, buff=0.5) 
        # Position subtitle below the title to prevent overlap (fixes WARNING at 4.0s)
        subtitle.next_to(title, DOWN, buff=0.3) 
        
        self.play(Write(title))
        self.play(Write(subtitle))
        self.wait(2)
        
        # Scene 1: Input Image
        self.play(FadeOut(subtitle))
        
        input_label = Text("Input Image", font_size=36)
        # Position input_label at the top edge, taking the place of title
        input_label.to_edge(UP, buff=0.5) 
        # Replace title with input_label
        self.play(ReplacementTransform(title, input_label))
        current_header_label = input_label # Update the current header label

        # Create a simple grid representing an image
        image_grid = VGroup()
        for i in range(5):
            for j in range(5):
                square = Square(side_length=0.4, color=BLUE, fill_opacity=0.3)
                square.move_to([i*0.5 - 1, j*0.5 - 0.5, 0])
                image_grid.add(square)
        
        # Position image_text relative to image_grid with a buffer
        image_text = Text("5x5 Image", font_size=24).next_to(image_grid, DOWN, buff=0.3)
        
        self.play(Create(image_grid), Write(image_text))
        self.wait(2)
        
        # Scene 2: Convolution Filter
        filter_label = Text("Convolution Filter", font_size=36)
        # Position filter_label at the top edge
        filter_label.to_edge(UP, buff=0.5)  
        
        # Replace the current header label (input_label) with filter_label (fixes WARNING at 6.0s)
        self.play(ReplacementTransform(current_header_label, filter_label))
        current_header_label = filter_label # Update the current header label
        
        # Create a 3x3 filter
        filter_grid = VGroup()
        filter_values = [
            [1, 0, -1],
            [1, 0, -1],
            [1, 0, -1]
        ]
        
        for i in range(3):
            for j in range(3):
                square = Square(side_length=0.4, color=RED, fill_opacity=0.5)
                square.move_to([i*0.5 + 2, j*0.5, 0])
                value = Text(str(filter_values[i][j]), font_size=20)
                value.move_to(square.get_center())
                filter_grid.add(square, value)
        
        # Position filter_text relative to filter_grid with a buffer (fixes potential overlaps at 13.0s, 14.0s if related to filter_grid or other nearby elements)
        filter_text = Text("3x3 Filter", font_size=24).next_to(filter_grid, DOWN, buff=0.3)
        
        self.play(Create(filter_grid), Write(filter_text))
        self.wait(2)
        
        # Scene 3: Convolution Operation
        op_label = Text("Sliding Window Operation", font_size=36, color=GREEN)
        # Position op_label at the top edge
        op_label.to_edge(UP, buff=0.5)  
        
        # Fade out scene-specific elements and replace the header label
        # (Fixes CRITICAL overlaps at 13.0s, 14.0s, which were likely due to previous header not being replaced)
        self.play(
            FadeOut(image_grid), 
            FadeOut(image_text),
            ReplacementTransform(current_header_label, op_label)
        )
        current_header_label = op_label # Update the current header label
        
        # Highlight moving filter (representing the 3x3 filter window)
        highlight = Rectangle(
            width=1.5, height=1.5, # 3 squares * 0.5 unit center-to-center spacing = 1.5
            color=YELLOW, stroke_width=4
        )
        # Calculate initial position of highlight (center of the first 3x3 block on the original image area)
        # The image_grid square (0,0) was centered at [-1, -0.5].
        # The center of the 3x3 window, when its top-left is at (0,0) of the image, is at the center of the image's (1,1) square.
        initial_highlight_center_x = (0+1)*0.5 - 1
        initial_highlight_center_y = (0+1)*0.5 - 0.5
        highlight.move_to([initial_highlight_center_x, initial_highlight_center_y, 0])
        
        self.play(Create(highlight))
        
        # Animate filter sliding across the 5x5 conceptual image area
        for i_window_tl in range(3): # Top-left X-index for the 3x3 window on the 5x5 image
            for j_window_tl in range(3): # Top-left Y-index for the 3x3 window on the 5x5 image
                # Calculate the center position of the 3x3 window
                # This corresponds to the center of the image_grid square at index (i_window_tl+1, j_window_tl+1)
                target_pos_x = (i_window_tl+1)*0.5 - 1
                target_pos_y = (j_window_tl+1)*0.5 - 0.5
                target_pos = np.array([target_pos_x, target_pos_y, 0])
                self.play(highlight.animate.move_to(target_pos), run_time=0.2) # Faster animation for sliding
        
        self.wait(1)
        
        # Scene 4: Feature Map
        # Fade out filter_grid, highlight, and filter_text
        self.play(FadeOut(filter_grid), FadeOut(highlight), FadeOut(filter_text))
        
        feature_label = Text("Feature Map (Output)", font_size=36, color=ORANGE)
        # Position feature_label at the top edge
        feature_label.to_edge(UP, buff=0.5) 
        
        # Replace the current header label (op_label) with feature_label (fixes CRITICAL overlap at 16.0s)
        self.play(ReplacementTransform(current_header_label, feature_label))
        current_header_label = feature_label # Update the current header label
        
        # Create feature map
        feature_grid = VGroup()
        for i in range(3):
            for j in range(3):
                square = Square(side_length=0.6, color=GREEN, fill_opacity=0.4)
                square.move_to([i*0.7, j*0.7 - 0.5, 0])
                feature_grid.add(square)
        
        # Position feature_text relative to feature_grid with a buffer
        feature_text = Text("3x3 Feature Map", font_size=24).next_to(feature_grid, DOWN, buff=0.3)
        
        self.play(Create(feature_grid), Write(feature_text))
        self.wait(2)
        
        # Scene 5: Multiple Filters
        multi_label = Text("Multiple Filters = Multiple Features", font_size=32, color=PURPLE)
        # Position multi_label at the top edge
        multi_label.to_edge(UP, buff=0.5)  
        
        # Replace the current header label (feature_label) with multi_label
        self.play(ReplacementTransform(current_header_label, multi_label))
        current_header_label = multi_label # Update the current header label
        
        # Fade out the single feature_text before introducing multiple labels
        self.play(FadeOut(feature_text))
        
        # Show multiple feature maps
        feature_map2 = feature_grid.copy().shift(LEFT * 3)
        feature_map3 = feature_grid.copy().shift(RIGHT * 3)
        
        # Position labels relative to their respective feature maps with a buffer
        label1 = Text("Edges", font_size=20).next_to(feature_map2, DOWN, buff=0.3)
        label2 = Text("Corners", font_size=20).next_to(feature_grid, DOWN, buff=0.3)
        label3 = Text("Textures", font_size=20).next_to(feature_map3, DOWN, buff=0.3)
        
        self.play(
            Create(feature_map2), Create(feature_map3),
            Write(label1), Write(label2), Write(label3)
        )
        self.wait(2)
        
        # Scene 6: Pooling
        pool_label = Text("Pooling: Reduce Dimensions", font_size=36, color=RED)
        # Position pool_label at the top edge
        pool_label.to_edge(UP, buff=0.5)
        
        # Fade out previous header label, multiple feature maps, and their labels
        self.play(
            FadeOut(feature_map2), FadeOut(feature_map3),
            FadeOut(label1), FadeOut(label2), FadeOut(label3),
            ReplacementTransform(current_header_label, pool_label)
        )
        current_header_label = pool_label # Update the current header label
        
        # Show pooling operation
        pooled = Square(side_length=1.2, color=BLUE, fill_opacity=0.5).move_to(ORIGIN)
        
        # Position pool_text relative to pooled with a buffer
        pool_text = Text("Max Pooling", font_size=24).next_to(pooled, DOWN, buff=0.3)
        
        self.play(
            ReplacementTransform(feature_grid, pooled) # Transform the central feature_grid into the pooled square
        )
        self.play(Write(pool_text))
        self.wait(2)
        
        # Final Scene: Summary
        summary = Text("CNNs Learn Visual Features!", font_size=40, color=GOLD).move_to(ORIGIN)
        
        explanation = Text(
            "Filters → Features → Pooling → Classification",
            font_size=28
        )
        # Adjust vertical spacing for explanation below summary (fixes Spacing issue)
        explanation.next_to(summary, DOWN, buff=0.7) 
        
        # Fade out all mobjects from the previous scene, including the header label
        self.play(
            FadeOut(pooled), 
            FadeOut(pool_text),
            FadeOut(current_header_label) # Ensure the last header label is faded out
        )
        self.play(Write(summary))
        self.play(Write(explanation))
        self.wait(3)
        
        # Cleanup any remaining mobjects
        self.play(*[FadeOut(mob) for mob in self.mobjects])
        self.wait()