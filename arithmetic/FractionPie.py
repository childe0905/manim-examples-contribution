from manim import *

class FractionPie(Scene):
    """
    Visualizes fractions using a pie chart (pizza) metaphor for elementary students.
    """
    def construct(self):
        # [VISUAL REASONING]
        # 1. Pedagogical Goal: Explain fractions as parts of a whole.
        # 2. Layout Strategy: Center circle, text labels on side.
        # 3. Anti-Overlap: Keep text away from circle radius.
        
        title = Text("Understanding Fractions: 1/4").to_edge(UP)
        self.play(Write(title))

        # Create a circle (pizza)
        circle = Circle(radius=2, color=WHITE, stroke_width=4)
        self.play(Create(circle))
        
        # Label: Whole
        whole_label = Text("1 Whole", font_size=36).next_to(circle, DOWN)
        self.play(Write(whole_label))
        self.wait(1)
        self.play(FadeOut(whole_label))

        # Cut into 4 pieces
        lines = VGroup(
            Line(UP * 2, DOWN * 2),
            Line(LEFT * 2, RIGHT * 2)
        ).move_to(circle.get_center())
        
        self.play(Create(lines))
        self.wait()
        
        # Create 4 sectors (wedges) to emphasize equal parts
        sectors = VGroup(*[
            Sector(
                outer_radius=2,
                angle=TAU / 4,
                start_angle=i * TAU / 4,
                color=BLUE,
                fill_opacity=0.0,
                stroke_width=0
            ).move_to(circle.get_center())
            for i in range(4)
        ])
        
        # Highlight each sector briefly to show "4 equal parts"
        for i, sector in enumerate(sectors):
            self.play(sector.animate.set_fill(BLUE, 0.4), run_time=0.3)
            self.play(sector.animate.set_fill(BLUE, 0.0), run_time=0.2)
        
        # Now keep one quarter highlighted (representing 1/4)
        wedge = sectors[0].copy().set_fill(ORANGE, 0.7)
        self.play(FadeIn(wedge))
        
        # Label the fraction
        fraction = MathTex(r"\frac{1}{4}").scale(2).next_to(circle, RIGHT, buff=1.5)
        arrow = Arrow(fraction.get_left(), wedge.get_center(), buff=0.3, color=YELLOW)
        
        self.play(Write(fraction), GrowArrow(arrow))
        
        explanation = Text(
            "1 part out of 4 equal parts",
            font_size=24,
            color=YELLOW
        ).next_to(fraction, DOWN)
        self.play(Write(explanation))
        
        self.wait(2)
