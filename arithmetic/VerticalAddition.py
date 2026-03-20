from manim import *

class VerticalAddition(Scene):
    """
    Demonstrates vertical addition with carry-over (28 + 35) for elementary students.
    """
    def construct(self):
        # [VISUAL REASONING]
        # 1. Pedagogical Goal: Illustrate column addition with carry-over.
        # 2. Layout Strategy: Title at top, calculation centered, hints on right.
        # 3. Anti-Overlap Check: Uses VGroup for stability.
        # 4. Animation Flow: Write numbers -> Add units (show carry) -> Add tens -> Final result.

        # Setup Scene
        title = Text("Vertical Addition: 28 + 35", font_size=40).to_edge(UP)
        self.play(Write(title))

        # Create Digits
        t1, u1 = Text("2"), Text("8")
        t2, u2 = Text("3"), Text("5")
        operator = Text("+")
        line = Line(start=LEFT, end=RIGHT).scale(1.5)
        
        # Group numbers
        num1_grp = VGroup(t1, u1).arrange(RIGHT, buff=0.3)
        num2_grp = VGroup(t2, u2).arrange(RIGHT, buff=0.3)
        
        # Vertical alignment
        num2_grp.next_to(num1_grp, DOWN, buff=0.5)
        operator.next_to(num2_grp, LEFT, buff=0.5)
        line.next_to(num2_grp, DOWN, buff=0.2).align_to(operator, LEFT)

        calculation = VGroup(num1_grp, num2_grp, operator, line).move_to(ORIGIN)
        
        self.play(Write(calculation))
        self.wait(1)

        # Step 1: Add Units Column (8 + 5 = 13)
        # Dim tens column
        self.play(
            t1.animate.set_opacity(0.3),
            t2.animate.set_opacity(0.3),
            operator.animate.set_opacity(0.3)
        )
        
        # Show calculation hint
        units_hint = MathTex("8 + 5 = 13", color=YELLOW).next_to(calculation, RIGHT, buff=2)
        self.play(Write(units_hint))
        
        # Place result digit '3'
        res_unit = Text("3", color=YELLOW).next_to(line, DOWN, buff=0.5).align_to(u2, RIGHT)
        self.play(Write(res_unit))
        
        # Carry the '1' (create explicit Text object to avoid indexing issues)
        carry_one = Text("1", color=RED, font_size=30).next_to(t1, UP, buff=0.2)
        self.play(
            FadeIn(carry_one, shift=DOWN * 0.3),
            FadeOut(units_hint)
        )
        self.wait(0.5)

        # Step 2: Add Tens Column (1 + 2 + 3 = 6)
        # Restore tens, dim units
        self.play(
            t1.animate.set_opacity(1),
            t2.animate.set_opacity(1),
            operator.animate.set_opacity(1),
            u1.animate.set_opacity(0.3),
            u2.animate.set_opacity(0.3),
            res_unit.animate.set_opacity(0.3)
        )

        tens_hint = MathTex("1 + 2 + 3 = 6", color=YELLOW).next_to(calculation, RIGHT, buff=2)
        tens_hint[0][0].set_color(RED)
        self.play(Write(tens_hint))

        res_tens = Text("6", color=YELLOW).next_to(line, DOWN, buff=0.5).align_to(t2, RIGHT)
        self.play(Write(res_tens))
        self.wait(1)

        # Final Result
        self.play(FadeOut(tens_hint), FadeOut(carry_one))
        
        # Restore all opacity and colors
        self.play(
            u1.animate.set_opacity(1),
            u2.animate.set_opacity(1),
            res_unit.animate.set_opacity(1).set_color(WHITE),
            res_tens.animate.set_color(WHITE)
        )

        final_box = SurroundingRectangle(VGroup(res_tens, res_unit), color=GREEN, buff=0.2)
        self.play(Create(final_box))
        self.wait(2)
