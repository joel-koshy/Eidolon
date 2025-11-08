from manim import *
import numpy as np

class CNNMathematicalExplanation(Scene):
    def construct(self):
        # Title
        title = Text("Convolutional Neural Networks", font_size=48, weight=BOLD)
        subtitle = Text("A Complete Mathematical Explanation", font_size=32)
        subtitle.next_to(title, DOWN)
        
        self.play(Write(title))
        self.play(FadeIn(subtitle))
        self.wait(2)
        self.play(FadeOut(title), FadeOut(subtitle))
        
        # Part 1: Input Image Representation
        self.show_input_representation()
        
        # Part 2: Convolution Operation Mathematics
        self.show_convolution_math()
        
        # Part 3: Activation Functions
        self.show_activation_functions()
        
        # Part 4: Pooling Operations
        self.show_pooling_operations()
        
        # Part 5: Multiple Layers and Feature Maps
        self.show_feature_maps()
        
        # Part 6: Backpropagation Mathematics
        self.show_backpropagation()
        
        # Final Summary
        self.show_summary()

    def show_input_representation(self):
        """Show how images are represented as matrices"""
        section_title = Text("1. Input Image Representation", font_size=40, color=BLUE)
        section_title.to_edge(UP)
        self.play(Write(section_title))
        
        # Create a sample image grid
        image_label = Text("Input Image (Grayscale)", font_size=28)
        image_label.next_to(section_title, DOWN, buff=0.5)
        
        # 5x5 grid with values
        image_values = np.random.randint(0, 256, size=(5, 5))
        image_grid = self.create_matrix_grid(image_values, cell_size=0.6)
        image_grid.next_to(image_label, DOWN, buff=0.5)
        
        # Mathematical notation
        math_notation = MathTex(
            r"I \in \mathbb{R}^{H \times W}",
            font_size=36
        )
        math_notation.next_to(image_grid, DOWN, buff=0.8)
        
        explanation = Text(
            "Each pixel has intensity value 0-255",
            font_size=24,
            color=GRAY
        )
        explanation.next_to(math_notation, DOWN, buff=0.5)
        
        self.play(FadeIn(image_label))
        self.play(Create(image_grid))
        self.play(Write(math_notation))
        self.play(FadeIn(explanation))
        self.wait(2)
        
        self.play(
            FadeOut(section_title),
            FadeOut(image_label),
            FadeOut(image_grid),
            FadeOut(math_notation),
            FadeOut(explanation)
        )

    def show_convolution_math(self):
        """Show detailed convolution mathematics"""
        section_title = Text("2. Convolution Operation", font_size=40, color=BLUE)
        section_title.to_edge(UP)
        self.play(Write(section_title))
        
        # Convolution formula
        conv_formula = MathTex(
            r"(I * K)_{i,j} = \sum_{m=0}^{k_h-1} \sum_{n=0}^{k_w-1} I_{i+m, j+n} \cdot K_{m,n}",
            font_size=32
        )
        conv_formula.next_to(section_title, DOWN, buff=0.5)
        
        self.play(Write(conv_formula))
        self.wait(2)
        
        # Example with numbers
        example_label = Text("Example: 3×3 Kernel on 5×5 Image", font_size=28)
        example_label.next_to(conv_formula, DOWN, buff=0.8)
        self.play(FadeIn(example_label))
        
        # Create input region (3x3)
        input_values = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
        input_grid = self.create_matrix_grid(input_values, cell_size=0.5)
        input_grid.shift(LEFT * 3 + DOWN * 1)
        
        input_label = Text("Input Region", font_size=24)
        input_label.next_to(input_grid, UP, buff=0.3)
        
        # Create kernel (3x3)
        kernel_values = np.array([[1, 0, -1], [1, 0, -1], [1, 0, -1]])
        kernel_grid = self.create_matrix_grid(kernel_values, cell_size=0.5, color=YELLOW)
        kernel_grid.next_to(input_grid, RIGHT, buff=1.5)
        
        kernel_label = Text("Kernel (Filter)", font_size=24)
        kernel_label.next_to(kernel_grid, UP, buff=0.3)
        
        # Multiplication symbol
        mult_symbol = MathTex(r"\odot", font_size=48)
        mult_symbol.move_to((input_grid.get_right() + kernel_grid.get_left()) / 2)
        
        self.play(
            Create(input_grid),
            FadeIn(input_label),
            Write(mult_symbol),
            Create(kernel_grid),
            FadeIn(kernel_label)
        )
        self.wait(1)
        
        # Show calculation
        calculation = MathTex(
            r"&= (1)(1) + (2)(0) + (3)(-1) \\",
            r"&+ (4)(1) + (5)(0) + (6)(-1) \\",
            r"&+ (7)(1) + (8)(0) + (9)(-1) \\",
            r"&= 1 + 0 - 3 + 4 + 0 - 6 + 7 + 0 - 9 \\",
            r"&= -6",
            font_size=28
        )
        calculation.next_to(kernel_grid, RIGHT, buff=1.2)
        
        self.play(Write(calculation))
        self.wait(3)
        
        # Result
        result_box = Rectangle(width=1.2, height=1.2, color=GREEN, fill_opacity=0.3)
        result_value = Text("-6", font_size=36, color=GREEN)
        result_value.move_to(result_box)
        result_group = VGroup(result_box, result_value)
        result_group.next_to(calculation, DOWN, buff=0.5)
        
        result_label = Text("Output Value", font_size=24)
        result_label.next_to(result_group, DOWN, buff=0.3)
        
        self.play(Create(result_box), Write(result_value), FadeIn(result_label))
        self.wait(2)
        
        self.play(*[FadeOut(mob) for mob in self.mobjects])

    def show_activation_functions(self):
        """Show activation functions and their mathematics"""
        section_title = Text("3. Activation Functions", font_size=40, color=BLUE)
        section_title.to_edge(UP)
        self.play(Write(section_title))
        
        # ReLU
        relu_title = Text("ReLU (Rectified Linear Unit)", font_size=32, color=YELLOW)
        relu_title.next_to(section_title, DOWN, buff=0.5)
        
        relu_formula = MathTex(
            r"f(x) = \max(0, x) = \begin{cases} x & \text{if } x > 0 \\ 0 & \text{if } x \leq 0 \end{cases}",
            font_size=32
        )
        relu_formula.next_to(relu_title, DOWN, buff=0.5)
        
        # ReLU graph
        axes = Axes(
            x_range=[-3, 3, 1],
            y_range=[-1, 3, 1],
            x_length=5,
            y_length=3,
            tips=False
        )
        axes.next_to(relu_formula, DOWN, buff=0.5)
        
        relu_graph = axes.plot(lambda x: max(0, x), color=YELLOW, x_range=[-3, 3])
        
        graph_label = Text("ReLU introduces non-linearity", font_size=24, color=GRAY)
        graph_label.next_to(axes, DOWN, buff=0.5)
        
        self.play(Write(relu_title))
        self.play(Write(relu_formula))
        self.play(Create(axes), Create(relu_graph))
        self.play(FadeIn(graph_label))
        self.wait(2)
        
        # Derivative
        derivative_label = Text("Derivative (for backpropagation):", font_size=28)
        derivative_label.next_to(graph_label, DOWN, buff=0.5)
        
        derivative_formula = MathTex(
            r"f'(x) = \begin{cases} 1 & \text{if } x > 0 \\ 0 & \text{if } x \leq 0 \end{cases}",
            font_size=32
        )
        derivative_formula.next_to(derivative_label, DOWN, buff=0.3)
        
        self.play(FadeIn(derivative_label))
        self.play(Write(derivative_formula))
        self.wait(2)
        
        self.play(*[FadeOut(mob) for mob in self.mobjects])

    def show_pooling_operations(self):
        """Show max pooling mathematics"""
        section_title = Text("4. Pooling Operations", font_size=40, color=BLUE)
        section_title.to_edge(UP)
        self.play(Write(section_title))
        
        pool_title = Text("Max Pooling (2×2)", font_size=32, color=YELLOW)
        pool_title.next_to(section_title, DOWN, buff=0.5)
        self.play(Write(pool_title))
        
        # Formula
        pool_formula = MathTex(
            r"P_{i,j} = \max_{m,n \in \text{pool}} I_{i+m, j+n}",
            font_size=36
        )
        pool_formula.next_to(pool_title, DOWN, buff=0.5)
        self.play(Write(pool_formula))
        
        # Example
        example_label = Text("Example: 4×4 → 2×2", font_size=28)
        example_label.next_to(pool_formula, DOWN, buff=0.5)
        self.play(FadeIn(example_label))
        
        # Input 4x4
        input_4x4 = np.array([[1, 3, 2, 4], [5, 6, 1, 2], [7, 2, 8, 3], [1, 4, 5, 9]])
        input_grid = self.create_matrix_grid(input_4x4, cell_size=0.5)
        input_grid.shift(LEFT * 3 + DOWN * 1.5)
        
        input_label = Text("Input (4×4)", font_size=24)
        input_label.next_to(input_grid, UP, buff=0.3)
        
        self.play(Create(input_grid), FadeIn(input_label))
        
        # Highlight 2x2 regions and show max
        regions = [
            (0, 0, 6), (0, 2, 4),
            (2, 0, 8), (2, 2, 9)
        ]
        
        arrow = Arrow(start=RIGHT, end=LEFT, color=WHITE).scale(0.8)
        arrow.next_to(input_grid, RIGHT, buff=0.5)
        
        # Output 2x2
        output_2x2 = np.array([[6, 4], [8, 9]])
        output_grid = self.create_matrix_grid(output_2x2, cell_size=0.7, color=GREEN)
        output_grid.next_to(arrow, RIGHT, buff=0.5)
        
        output_label = Text("Output (2×2)", font_size=24)
        output_label.next_to(output_grid, UP, buff=0.3)
        
        self.play(FadeIn(arrow))
        self.play(Create(output_grid), FadeIn(output_label))
        self.wait(2)
        
        explanation = Text(
            "Reduces spatial dimensions, retains important features",
            font_size=24,
            color=GRAY
        )
        explanation.next_to(output_grid, DOWN, buff=0.8)
        self.play(FadeIn(explanation))
        self.wait(2)
        
        self.play(*[FadeOut(mob) for mob in self.mobjects])

    def show_feature_maps(self):
        """Show multiple feature maps concept"""
        section_title = Text("5. Multiple Filters → Feature Maps", font_size=40, color=BLUE)
        section_title.to_edge(UP)
        self.play(Write(section_title))
        
        explanation = Text("Each filter detects different features", font_size=28)
        explanation.next_to(section_title, DOWN, buff=0.5)
        self.play(FadeIn(explanation))
        
        # Show 3 different kernels
        kernel1_label = Text("Vertical Edges", font_size=24, color=RED)
        kernel1_values = np.array([[-1, 0, 1], [-1, 0, 1], [-1, 0, 1]])
        kernel1 = self.create_matrix_grid(kernel1_values, cell_size=0.4, color=RED)
        kernel1.shift(LEFT * 4 + DOWN * 1)
        kernel1_label.next_to(kernel1, UP, buff=0.3)
        
        kernel2_label = Text("Horizontal Edges", font_size=24, color=GREEN)
        kernel2_values = np.array([[-1, -1, -1], [0, 0, 0], [1, 1, 1]])
        kernel2 = self.create_matrix_grid(kernel2_values, cell_size=0.4, color=GREEN)
        kernel2.shift(DOWN * 1)
        kernel2_label.next_to(kernel2, UP, buff=0.3)
        
        kernel3_label = Text("Diagonal", font_size=24, color=YELLOW)
        kernel3_values = np.array([[0, 1, 1], [-1, 0, 1], [-1, -1, 0]])
        kernel3 = self.create_matrix_grid(kernel3_values, cell_size=0.4, color=YELLOW)
        kernel3.shift(RIGHT * 4 + DOWN * 1)
        kernel3_label.next_to(kernel3, UP, buff=0.3)
        
        self.play(
            Create(kernel1), FadeIn(kernel1_label),
            Create(kernel2), FadeIn(kernel2_label),
            Create(kernel3), FadeIn(kernel3_label)
        )
        self.wait(2)
        
        # Output feature maps
        output_label = Text("→ 3 Feature Maps (Channels)", font_size=28, color=BLUE)
        output_label.next_to(kernel2, DOWN, buff=1.2)
        self.play(FadeIn(output_label))
        self.wait(2)
        
        self.play(*[FadeOut(mob) for mob in self.mobjects])

    def show_backpropagation(self):
        """Show backpropagation mathematics"""
        section_title = Text("6. Backpropagation Through Convolution", font_size=40, color=BLUE)
        section_title.to_edge(UP)
        self.play(Write(section_title))
        
        # Loss function
        loss_label = Text("Loss Function (e.g., Cross-Entropy):", font_size=28)
        loss_label.next_to(section_title, DOWN, buff=0.5)
        
        loss_formula = MathTex(
            r"\mathcal{L} = -\sum_{i} y_i \log(\hat{y}_i)",
            font_size=36
        )
        loss_formula.next_to(loss_label, DOWN, buff=0.3)
        
        self.play(FadeIn(loss_label))
        self.play(Write(loss_formula))
        self.wait(1)
        
        # Gradient computation
        grad_label = Text("Gradient w.r.t. Kernel Weights:", font_size=28)
        grad_label.next_to(loss_formula, DOWN, buff=0.8)
        
        grad_formula = MathTex(
            r"\frac{\partial \mathcal{L}}{\partial K_{m,n}} = \sum_{i,j} \frac{\partial \mathcal{L}}{\partial O_{i,j}} \cdot I_{i+m, j+n}",
            font_size=32
        )
        grad_formula.next_to(grad_label, DOWN, buff=0.3)
        
        self.play(FadeIn(grad_label))
        self.play(Write(grad_formula))
        self.wait(2)
        
        # Weight update
        update_label = Text("Weight Update (Gradient Descent):", font_size=28)
        update_label.next_to(grad_formula, DOWN, buff=0.8)
        
        update_formula = MathTex(
            r"K_{m,n}^{new} = K_{m,n}^{old} - \eta \cdot \frac{\partial \mathcal{L}}{\partial K_{m,n}}",
            font_size=32
        )
        update_formula.next_to(update_label, DOWN, buff=0.3)
        
        self.play(FadeIn(update_label))
        self.play(Write(update_formula))
        self.wait(2)
        
        # Learning rate note
        lr_note = Text("η = learning rate (e.g., 0.001)", font_size=24, color=GRAY)
        lr_note.next_to(update_formula, DOWN, buff=0.5)
        self.play(FadeIn(lr_note))
        self.wait(2)
        
        self.play(*[FadeOut(mob) for mob in self.mobjects])

    def show_summary(self):
        """Show final summary"""
        title = Text("CNN Architecture Summary", font_size=44, weight=BOLD, color=BLUE)
        title.to_edge(UP)
        self.play(Write(title))
        
        summary_points = VGroup(
            Text("1. Input: Image matrix (H × W × C)", font_size=28),
            Text("2. Convolution: Extract local features", font_size=28),
            Text("3. Activation: Introduce non-linearity (ReLU)", font_size=28),
            Text("4. Pooling: Reduce dimensions", font_size=28),
            Text("5. Repeat: Stack multiple layers", font_size=28),
            Text("6. Flatten: Convert to vector", font_size=28),
            Text("7. Dense Layers: Classification", font_size=28),
            Text("8. Backpropagation: Learn optimal filters", font_size=28)
        )
        
        summary_points.arrange(DOWN, aligned_edge=LEFT, buff=0.4)
        summary_points.next_to(title, DOWN, buff=0.8)
        
        for point in summary_points:
            self.play(FadeIn(point), run_time=0.5)
        
        self.wait(3)
        
        # Final formula
        final_formula = MathTex(
            r"Y = f(\text{Dense}(\text{Flatten}(\text{Pool}(\text{ReLU}(I * K)))))",
            font_size=32,
            color=YELLOW
        )
        final_formula.next_to(summary_points, DOWN, buff=1)
        
        self.play(Write(final_formula))
        self.wait(3)

    def create_matrix_grid(self, values, cell_size=0.5, color=WHITE):
        """Create a grid displaying matrix values"""
        rows, cols = values.shape
        grid = VGroup()
        
        for i in range(rows):
            for j in range(cols):
                cell = Square(side_length=cell_size, color=color)
                cell.shift(RIGHT * j * cell_size + DOWN * i * cell_size)
                
                value_text = Text(str(values[i, j]), font_size=20)
                value_text.move_to(cell.get_center())
                
                grid.add(VGroup(cell, value_text))
        
        grid.move_to(ORIGIN)
        return grid
