from manim import *

class SlopeIntercept(Scene):
    """
    Explores y = mx + b. Changing m (slope) and b (intercept).
    """
    def construct(self):
        # [VISUAL REASONING]
        # 1. Goal: Graph linear function.
        # 2. Layout: Axes on left/center, Equation on top right, ValueTrackers.
        
        ax = Axes(
            x_range=[-5, 5, 1],
            y_range=[-5, 5, 1],
            x_length=6, y_length=6,
            axis_config={"include_numbers": True}
        ).to_edge(LEFT)
        
        self.play(Create(ax))

        # Initial values
        m = ValueTracker(1)
        b = ValueTracker(0)

        # Dynamic Function Graph
        # graph is always updated based on m and b
        def get_line():
            return ax.plot(lambda x: m.get_value() * x + b.get_value(), color=YELLOW)

        line = always_redraw(get_line)
        self.add(line)

        # Equation Label
        # y = {m}x + {b}
        # This is tricky with MathTex and dynamic values.
        # We use DecimalNumber for updating values.
        
        eq_text = MathTex("y = ").to_edge(UR).shift(DOWN)
        m_decimal = DecimalNumber(1, num_decimal_places=1).next_to(eq_text, RIGHT)
        x_text = MathTex("x + ").next_to(m_decimal, RIGHT)
        b_decimal = DecimalNumber(0, num_decimal_places=1).next_to(x_text, RIGHT)
        
        eq_group = VGroup(eq_text, m_decimal, x_text, b_decimal)
        self.add(eq_group)
        
        m_decimal.add_updater(lambda d: d.set_value(m.get_value()))
        b_decimal.add_updater(lambda d: d.set_value(b.get_value()))
        
        # Explanatory Text
        hint = Text("Slope (m)", font_size=24, color=YELLOW).next_to(eq_group, UP)
        self.play(Write(hint))

        # Animate Slope (m)
        self.play(m.animate.set_value(3), run_time=2) # Steeper
        self.play(m.animate.set_value(-2), run_time=2) # Negative slope
        self.wait()
        
        # Animate Intercept (b)
        hint2 = Text("Y-Intercept (b)", font_size=24, color=RED).next_to(eq_group, UP)
        self.play(Transform(hint, hint2))
        
        self.play(b.animate.set_value(2), run_time=2) # Shift Up
        self.play(b.animate.set_value(-3), run_time=2) # Shift Down
        
        self.wait(2)
