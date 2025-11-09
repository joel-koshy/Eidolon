from manim import *

class KrebsCycleExplanation(Scene):
    def construct(self):
        # Title
        title = Text("The Krebs Cycle", font_size=56, weight=BOLD, color=BLUE)
        subtitle = Text("Also known as the Citric Acid Cycle", font_size=32, color=GRAY)
        subtitle.next_to(title, DOWN, buff=0.3)
        
        self.play(Write(title))
        self.play(FadeIn(subtitle))
        self.wait(2)
        self.play(FadeOut(title), FadeOut(subtitle))
        
        # Introduction
        self.show_introduction()
        
        # Overview of the cycle
        self.show_overview()
        
        # Step-by-step reactions
        self.show_step1_acetyl_coa()
        self.show_step2_isomerization()
        self.show_step3_oxidative_decarboxylation()
        self.show_step4_second_decarboxylation()
        self.show_step5_substrate_phosphorylation()
        self.show_step6_oxidation()
        self.show_step7_hydration()
        self.show_step8_final_oxidation()
        
        # Energy summary
        self.show_energy_summary()
        
        # Final summary
        self.show_final_summary()
    
    def show_introduction(self):
        """Introduce the Krebs Cycle"""
        section_title = Text("What is the Krebs Cycle?", font_size=44, color=BLUE)
        section_title.to_edge(UP)
        self.play(Write(section_title))
        
        # Key points
        points = VGroup(
            Text("• Central metabolic pathway in cellular respiration", font_size=28),
            Text("• Occurs in the mitochondrial matrix", font_size=28),
            Text("• Completes the oxidation of glucose", font_size=28),
            Text("• Produces ATP, NADH, and FADH₂", font_size=28)
        )
        points.arrange(DOWN, aligned_edge=LEFT, buff=0.5)
        points.next_to(section_title, DOWN, buff=1)
        
        for point in points:
            self.play(FadeIn(point), run_time=0.7)
            self.wait(0.5)
        
        self.wait(2)
        self.play(FadeOut(section_title), FadeOut(points))
    
    def show_overview(self):
        """Show cycle overview"""
        section_title = Text("The Cycle Overview", font_size=44, color=BLUE)
        section_title.to_edge(UP)
        self.play(Write(section_title))
        
        # Input and output
        input_label = Text("Input:", font_size=32, color=GREEN)
        input_label.shift(LEFT * 3 + UP * 1)
        
        input_items = VGroup(
            Text("Acetyl-CoA (2C)", font_size=26),
            Text("3 NAD⁺", font_size=26),
            Text("1 FAD", font_size=26),
            Text("1 ADP + Pi", font_size=26)
        )
        input_items.arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        input_items.next_to(input_label, DOWN, buff=0.5)
        
        output_label = Text("Output:", font_size=32, color=RED)
        output_label.shift(RIGHT * 3 + UP * 1)
        
        output_items = VGroup(
            Text("2 CO₂", font_size=26),
            Text("3 NADH", font_size=26),
            Text("1 FADH₂", font_size=26),
            Text("1 ATP/GTP", font_size=26)
        )
        output_items.arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        output_items.next_to(output_label, DOWN, buff=0.5)
        
        # Arrow
        arrow = Arrow(
            start=input_items.get_right() + RIGHT * 0.3,
            end=output_items.get_left() + LEFT * 0.3,
            color=YELLOW,
            buff=0.5
        )
        
        self.play(Write(input_label))
        self.play(FadeIn(input_items))
        self.play(GrowArrow(arrow))
        self.play(Write(output_label))
        self.play(FadeIn(output_items))
        self.wait(3)
        
        self.play(*[FadeOut(mob) for mob in self.mobjects])
    
    def show_step1_acetyl_coa(self):
        """Step 1: Acetyl-CoA + Oxaloacetate → Citrate"""
        section_title = Text("Step 1: Formation of Citrate", font_size=40, color=BLUE)
        section_title.to_edge(UP)
        self.play(Write(section_title))
        
        # Reaction equation
        reaction = MathTex(
            r"\text{Acetyl-CoA (2C)} + \text{Oxaloacetate (4C)} \rightarrow \text{Citrate (6C)} + \text{CoA}",
            font_size=30
        )
        reaction.next_to(section_title, DOWN, buff=0.8)
        self.play(Write(reaction))
        
        # Enzyme
        enzyme = Text("Enzyme: Citrate Synthase", font_size=26, color=YELLOW)
        enzyme.next_to(reaction, DOWN, buff=0.8)
        self.play(FadeIn(enzyme))
        
        # Visual representation
        acetyl_box = self.create_molecule_box("Acetyl-CoA", "2C", GREEN)
        acetyl_box.shift(LEFT * 3 + DOWN * 1)
        
        oxalo_box = self.create_molecule_box("Oxaloacetate", "4C", BLUE)
        oxalo_box.next_to(acetyl_box, RIGHT, buff=1)
        
        citrate_box = self.create_molecule_box("Citrate", "6C", ORANGE)
        citrate_box.shift(RIGHT * 3 + DOWN * 1)
        
        plus_sign = MathTex("+", font_size=48)
        plus_sign.move_to((acetyl_box.get_center() + oxalo_box.get_center()) / 2)
        
        arrow = Arrow(
            start=oxalo_box.get_right() + RIGHT * 0.2,
            end=citrate_box.get_left() + LEFT * 0.2,
            color=WHITE
        )
        
        self.play(FadeIn(acetyl_box), Write(plus_sign), FadeIn(oxalo_box))
        self.wait(1)
        self.play(GrowArrow(arrow))
        self.play(FadeIn(citrate_box))
        self.wait(2)
        
        self.play(*[FadeOut(mob) for mob in self.mobjects])
    
    def show_step2_isomerization(self):
        """Step 2: Citrate → Isocitrate"""
        section_title = Text("Step 2: Isomerization", font_size=40, color=BLUE)
        section_title.to_edge(UP)
        self.play(Write(section_title))
        
        reaction = MathTex(
            r"\text{Citrate (6C)} \rightarrow \text{Isocitrate (6C)}",
            font_size=32
        )
        reaction.next_to(section_title, DOWN, buff=0.8)
        self.play(Write(reaction))
        
        enzyme = Text("Enzyme: Aconitase", font_size=26, color=YELLOW)
        enzyme.next_to(reaction, DOWN, buff=0.6)
        self.play(FadeIn(enzyme))
        
        explanation = Text(
            "Rearrangement of hydroxyl group position",
            font_size=24,
            color=GRAY
        )
        explanation.next_to(enzyme, DOWN, buff=0.6)
        self.play(FadeIn(explanation))
        self.wait(2)
        
        self.play(*[FadeOut(mob) for mob in self.mobjects])
    
    def show_step3_oxidative_decarboxylation(self):
        """Step 3: Isocitrate → α-Ketoglutarate"""
        section_title = Text("Step 3: First Oxidative Decarboxylation", font_size=40, color=BLUE)
        section_title.to_edge(UP)
        self.play(Write(section_title))
        
        reaction = MathTex(
            r"\text{Isocitrate (6C)} + \text{NAD}^+ \rightarrow \alpha\text{-Ketoglutarate (5C)} + \text{CO}_2 + \text{NADH}",
            font_size=28
        )
        reaction.next_to(section_title, DOWN, buff=0.8)
        self.play(Write(reaction))
        
        enzyme = Text("Enzyme: Isocitrate Dehydrogenase", font_size=26, color=YELLOW)
        enzyme.next_to(reaction, DOWN, buff=0.8)
        self.play(FadeIn(enzyme))
        
        # Key products
        products = VGroup(
            Text("✓ First CO₂ released", font_size=26, color=RED),
            Text("✓ First NADH produced", font_size=26, color=GREEN)
        )
        products.arrange(DOWN, aligned_edge=LEFT, buff=0.4)
        products.next_to(enzyme, DOWN, buff=0.8)
        
        for product in products:
            self.play(FadeIn(product), run_time=0.7)
        
        self.wait(2)
        self.play(*[FadeOut(mob) for mob in self.mobjects])
    
    def show_step4_second_decarboxylation(self):
        """Step 4: α-Ketoglutarate → Succinyl-CoA"""
        section_title = Text("Step 4: Second Oxidative Decarboxylation", font_size=38, color=BLUE)
        section_title.to_edge(UP)
        self.play(Write(section_title))
        
        reaction = MathTex(
            r"\alpha\text{-Ketoglutarate (5C)} + \text{NAD}^+ + \text{CoA} \rightarrow \text{Succinyl-CoA (4C)} + \text{CO}_2 + \text{NADH}",
            font_size=26
        )
        reaction.next_to(section_title, DOWN, buff=0.8)
        self.play(Write(reaction))
        
        enzyme = Text("Enzyme: α-Ketoglutarate Dehydrogenase Complex", font_size=24, color=YELLOW)
        enzyme.next_to(reaction, DOWN, buff=0.8)
        self.play(FadeIn(enzyme))
        
        # Key products
        products = VGroup(
            Text("✓ Second CO₂ released", font_size=26, color=RED),
            Text("✓ Second NADH produced", font_size=26, color=GREEN)
        )
        products.arrange(DOWN, aligned_edge=LEFT, buff=0.4)
        products.next_to(enzyme, DOWN, buff=0.8)
        
        for product in products:
            self.play(FadeIn(product), run_time=0.7)
        
        self.wait(2)
        self.play(*[FadeOut(mob) for mob in self.mobjects])
    
    def show_step5_substrate_phosphorylation(self):
        """Step 5: Succinyl-CoA → Succinate"""
        section_title = Text("Step 5: Substrate-Level Phosphorylation", font_size=38, color=BLUE)
        section_title.to_edge(UP)
        self.play(Write(section_title))
        
        reaction = MathTex(
            r"\text{Succinyl-CoA} + \text{GDP} + \text{Pi} \rightarrow \text{Succinate} + \text{GTP} + \text{CoA}",
            font_size=28
        )
        reaction.next_to(section_title, DOWN, buff=0.8)
        self.play(Write(reaction))
        
        enzyme = Text("Enzyme: Succinyl-CoA Synthetase", font_size=26, color=YELLOW)
        enzyme.next_to(reaction, DOWN, buff=0.8)
        self.play(FadeIn(enzyme))
        
        note = Text(
            "GTP ≈ ATP (energy equivalent)",
            font_size=26,
            color=GREEN
        )
        note.next_to(enzyme, DOWN, buff=0.8)
        self.play(FadeIn(note))
        self.wait(2)
        
        self.play(*[FadeOut(mob) for mob in self.mobjects])
    
    def show_step6_oxidation(self):
        """Step 6: Succinate → Fumarate"""
        section_title = Text("Step 6: Oxidation", font_size=40, color=BLUE)
        section_title.to_edge(UP)
        self.play(Write(section_title))
        
        reaction = MathTex(
            r"\text{Succinate} + \text{FAD} \rightarrow \text{Fumarate} + \text{FADH}_2",
            font_size=32
        )
        reaction.next_to(section_title, DOWN, buff=0.8)
        self.play(Write(reaction))
        
        enzyme = Text("Enzyme: Succinate Dehydrogenase", font_size=26, color=YELLOW)
        enzyme.next_to(reaction, DOWN, buff=0.8)
        self.play(FadeIn(enzyme))
        
        note = Text(
            "✓ FADH₂ produced (not NADH)",
            font_size=26,
            color=GREEN
        )
        note.next_to(enzyme, DOWN, buff=0.8)
        self.play(FadeIn(note))
        self.wait(2)
        
        self.play(*[FadeOut(mob) for mob in self.mobjects])
    
    def show_step7_hydration(self):
        """Step 7: Fumarate → Malate"""
        section_title = Text("Step 7: Hydration", font_size=40, color=BLUE)
        section_title.to_edge(UP)
        self.play(Write(section_title))
        
        reaction = MathTex(
            r"\text{Fumarate} + \text{H}_2\text{O} \rightarrow \text{Malate}",
            font_size=32
        )
        reaction.next_to(section_title, DOWN, buff=0.8)
        self.play(Write(reaction))
        
        enzyme = Text("Enzyme: Fumarase", font_size=26, color=YELLOW)
        enzyme.next_to(reaction, DOWN, buff=0.8)
        self.play(FadeIn(enzyme))
        
        explanation = Text(
            "Addition of water across the double bond",
            font_size=24,
            color=GRAY
        )
        explanation.next_to(enzyme, DOWN, buff=0.6)
        self.play(FadeIn(explanation))
        self.wait(2)
        
        self.play(*[FadeOut(mob) for mob in self.mobjects])
    
    def show_step8_final_oxidation(self):
        """Step 8: Malate → Oxaloacetate"""
        section_title = Text("Step 8: Final Oxidation", font_size=40, color=BLUE)
        section_title.to_edge(UP)
        self.play(Write(section_title))
        
        reaction = MathTex(
            r"\text{Malate} + \text{NAD}^+ \rightarrow \text{Oxaloacetate} + \text{NADH}",
            font_size=32
        )
        reaction.next_to(section_title, DOWN, buff=0.8)
        self.play(Write(reaction))
        
        enzyme = Text("Enzyme: Malate Dehydrogenase", font_size=26, color=YELLOW)
        enzyme.next_to(reaction, DOWN, buff=0.8)
        self.play(FadeIn(enzyme))
        
        note = Text(
            "✓ Third NADH produced",
            font_size=26,
            color=GREEN
        )
        note.next_to(enzyme, DOWN, buff=0.6)
        self.play(FadeIn(note))
        
        cycle_note = Text(
            "→ Regenerates Oxaloacetate to continue the cycle!",
            font_size=26,
            color=ORANGE
        )
        cycle_note.next_to(note, DOWN, buff=0.6)
        self.play(FadeIn(cycle_note))
        self.wait(2)
        
        self.play(*[FadeOut(mob) for mob in self.mobjects])
    
    def show_energy_summary(self):
        """Show energy yield summary"""
        section_title = Text("Energy Yield Per Cycle", font_size=44, color=BLUE)
        section_title.to_edge(UP)
        self.play(Write(section_title))
        
        # Energy products
        products = VGroup(
            Text("3 NADH  →  7.5 ATP (via electron transport)", font_size=28, color=GREEN),
            Text("1 FADH₂  →  1.5 ATP (via electron transport)", font_size=28, color=GREEN),
            Text("1 GTP/ATP  →  1 ATP (direct)", font_size=28, color=GREEN)
        )
        products.arrange(DOWN, aligned_edge=LEFT, buff=0.6)
        products.shift(UP * 0.5)
        
        for product in products:
            self.play(FadeIn(product), run_time=0.8)
        
        # Total
        divider = Line(LEFT * 4, RIGHT * 4, color=WHITE)
        divider.next_to(products, DOWN, buff=0.6)
        self.play(Create(divider))
        
        total = Text("Total: ~10 ATP per Acetyl-CoA", font_size=36, weight=BOLD, color=YELLOW)
        total.next_to(divider, DOWN, buff=0.6)
        self.play(Write(total))
        self.wait(3)
        
        self.play(*[FadeOut(mob) for mob in self.mobjects])
    
    def show_final_summary(self):
        """Final summary"""
        title = Text("Krebs Cycle: Key Takeaways", font_size=44, weight=BOLD, color=BLUE)
        title.to_edge(UP)
        self.play(Write(title))
        
        summary_points = VGroup(
            Text("1. Completes glucose oxidation (started in glycolysis)", font_size=26),
            Text("2. Each glucose produces 2 Acetyl-CoA → 2 cycles", font_size=26),
            Text("3. Produces electron carriers (NADH, FADH₂) for ETC", font_size=26),
            Text("4. Releases 2 CO₂ per cycle (carbon waste)", font_size=26),
            Text("5. Central hub connecting carbs, fats, and proteins", font_size=26)
        )
        summary_points.arrange(DOWN, aligned_edge=LEFT, buff=0.5)
        summary_points.next_to(title, DOWN, buff=1)
        
        for point in summary_points:
            self.play(FadeIn(point), run_time=0.7)
        
        self.wait(3)
        
        # Final equation
        final = MathTex(
            r"\text{Glucose} \rightarrow 2\text{ Acetyl-CoA} \rightarrow 2 \times \text{Krebs Cycle} \rightarrow \text{Energy!}",
            font_size=30,
            color=YELLOW
        )
        final.next_to(summary_points, DOWN, buff=1)
        self.play(Write(final))
        self.wait(3)
    
    def create_molecule_box(self, name, carbons, color):
        """Create a box representing a molecule"""
        box = Rectangle(width=2.5, height=1.2, color=color, fill_opacity=0.2)
        name_text = Text(name, font_size=22)
        carbon_text = Text(carbons, font_size=20, color=color)
        carbon_text.next_to(name_text, DOWN, buff=0.2)
        
        group = VGroup(name_text, carbon_text)
        group.move_to(box.get_center())
        
        return VGroup(box, group)
