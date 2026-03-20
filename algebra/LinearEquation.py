from manim import *

class LinearEquation(Scene):
    """
    Solves 3x + 5 = 14 using the balance scale method.
    """
    def construct(self):
        # [VISUAL REASONING]
        # 1. Goal: Solving equation steps.
        # 2. Layout: Equation centered. Operations indicated by arrows/colors.

        eq_str = r"3x + 5 = 14"
        eq = MathTex("3x", "+", "5", "=", "14")
        eq.scale(1.5)
        self.play(Write(eq))
        self.wait()

        # Step 1: Subtract 5
        # Visual hint: show -5 on both sides
        hint_left = MathTex("-5", color=RED).next_to(eq[2], DOWN)
        hint_right = MathTex("-5", color=RED).next_to(eq[4], DOWN)
        
        self.play(FadeIn(hint_left), FadeIn(hint_right))
        self.wait()
        
        # Animate subtraction
        new_eq = MathTex("3x", "=", "9")
        new_eq.scale(1.5)
        
        self.play(
            Transform(eq[0], new_eq[0]), # 3x -> 3x
            FadeOut(eq[1]), # +
            FadeOut(eq[2]), # 5
            Transform(eq[3], new_eq[1]), # = -> =
            Transform(eq[4], new_eq[2]), # 14 -> 9
            FadeOut(hint_left),
            FadeOut(hint_right)
        )
        self.wait()

        # Step 2: Divide by 3 (using fraction notation)
        hint_div = MathTex(r"\div 3", color=YELLOW).next_to(new_eq, RIGHT, buff=1)
        self.play(Write(hint_div))
        self.wait()
        
        # Show as fractions: 3x/3 = 9/3
        frac_eq = MathTex(r"\frac{3x}{3}", "=", r"\frac{9}{3}")
        frac_eq.scale(1.5)
        
        self.play(
            Transform(eq[0], frac_eq[0]),  # 3x -> 3x/3
            Transform(eq[3], frac_eq[1]),  # = -> =
            Transform(eq[4], frac_eq[2]),  # 9 -> 9/3
            FadeOut(hint_div)
        )
        self.wait()
        
        # Show cancellation: draw lines through the 3s
        # Index into the fraction components
        # frac_eq[0] is "\frac{3x}{3}", we want to cross out both 3s
        # frac_eq[2] is "\frac{9}{3}", we want to cross out the bottom 3
        
        # Create cancellation lines (start as WHITE)
        cancel_left_num = Line(
            frac_eq[0].get_left() + LEFT * 0.1,
            frac_eq[0].get_right() + RIGHT * 0.1,
            color=WHITE, stroke_width=3
        ).move_to(frac_eq[0])
        
        cancel_right_denom = Line(
            frac_eq[2].get_left() + LEFT * 0.1,
            frac_eq[2].get_right() + RIGHT * 0.1,
            color=WHITE, stroke_width=3
        ).move_to(frac_eq[2])
        
        # Create LEFT line (white)
        self.play(Create(cancel_left_num))
        
        # Change LEFT line to red (cancellation effect)
        self.play(cancel_left_num.animate.set_color(RED))
        
        # Create RIGHT line (white)
        self.play(Create(cancel_right_denom))
        
        # Change RIGHT line to red (cancellation effect)
        self.play(cancel_right_denom.animate.set_color(RED))
        self.wait()
        
        # Final result: x = 3
        final_eq = MathTex("x", "=", "3")
        final_eq.scale(1.5)
        
        self.play(
            Transform(eq[0], final_eq[0]),  # 3x/3 -> x
            Transform(eq[3], final_eq[1]),  # = -> =
            Transform(eq[4], final_eq[2]),  # 9/3 -> 3
            FadeOut(cancel_left_num),
            FadeOut(cancel_right_denom)
        )
        
        # Highlight result
        box = SurroundingRectangle(VGroup(eq[0], eq[3], eq[4]), color=GREEN, buff=0.2)
        
        self.play(Create(box))
        self.wait(2)

