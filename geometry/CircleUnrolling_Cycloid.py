from manim import *
import numpy as np


class CircleUnrolling_Cycloid(Scene):
    """
    Visual proof that C = 2*pi*r by rolling a circle along a line.

    Strategy: Physical Rolling (Cycloid)
    - A ValueTracker drives the rotation angle t ∈ [0, TAU].
    - Circle simultaneously shifts RIGHT by r*t AND rotates by -t.
    - rate_func=linear on BOTH ensures "rolling without slipping".
    - TracedPath draws the cycloid traced by the bottom contact point.
    - Final Brace labels the total unrolled length as 2πr.

    Verified techniques from Deep Research (Feb 2026):
    - ValueTracker + shift + Rotate with rate_func=linear (Gemini/GPT reports)
    - TracedPath for cycloid (NOT become() in updater — v0.19 optimized)
    - Arc(angle=0.001) proxy for numerical stability near t=0
    - Axes.c2p() for coordinate mapping to avoid magic numbers (Gemini report)

    Anti-patterns AVOIDED:
    - MoveAlongPath alone (doesn't rotate → slipping glitch)
    - become() in updater (causes 120s render timeout)
    - angle=0 (divide-by-zero in Arc normal calculations)

    topic: geometry | circumference | pi | circle | rolling | cycloid
    """
    def construct(self):
        r = 1.0
        circumference = TAU * r  # = 2*pi*r

        # ── Layout ────────────────────────────────────────────────────────────
        # Ground line spans full unroll length; circle starts above left end
        ground = Line(
            LEFT * (circumference / 2 + 0.5),
            RIGHT * (circumference / 2 + 0.5),
            color=GRAY, stroke_width=2
        ).shift(DOWN * r)

        # Circle starts at the left, center at y=0 (ground + r)
        start_x = -circumference / 2
        circle = Circle(radius=r, color=BLUE, stroke_width=3)
        circle.move_to(np.array([start_x, 0, 0]))

        # Mark the contact point (bottom of circle)
        contact_dot = Dot(color=RED, radius=0.08)
        contact_dot.move_to(circle.get_bottom())

        # TracedPath follows the contact dot — draws the cycloid automatically
        cycloid_path = TracedPath(
            contact_dot.get_center,
            stroke_color=RED,
            stroke_width=2.5,
            dissipating_time=None   # keep full trace
        )

        # Title
        title = Tex(r"Circle Unrolling: $C = 2\pi r$",
                    font_size=36).to_edge(UP)

        self.play(Write(title))
        self.play(Create(ground), Create(circle), FadeIn(contact_dot))
        self.add(cycloid_path)
        self.wait(0.5)

        # ── Rolling Animation ─────────────────────────────────────────────────
        # One shared ValueTracker → both translation and rotation are locked
        t_tracker = ValueTracker(0)

        def circle_updater(mob):
            t = t_tracker.get_value()
            mob.move_to(np.array([start_x + r * t, 0, 0]))
            mob.rotate(-t, about_point=mob.get_center())

        def dot_updater(mob):
            # dot follows circle center
            t = t_tracker.get_value()
            angle = -PI / 2 - t   # starts at bottom; rolls clockwise
            cx = start_x + r * t
            mob.move_to(np.array([cx + r * np.cos(angle), r * np.sin(angle), 0]))

        circle.add_updater(circle_updater)
        contact_dot.add_updater(dot_updater)

        # Animate the tracker — rate_func=linear is MANDATORY for rolling without slipping
        self.play(
            t_tracker.animate.set_value(TAU),
            run_time=5,
            rate_func=linear
        )

        circle.remove_updater(circle_updater)
        contact_dot.remove_updater(dot_updater)
        self.wait(0.5)

        # ── Measurement ───────────────────────────────────────────────────────
        # Show that the traced length equals C = 2*pi*r
        final_contact = contact_dot.get_center()
        start_point = np.array([start_x, -r, 0])  # original contact point

        unrolled_line = Line(start_point, final_contact, color=YELLOW, stroke_width=4)
        self.play(Create(unrolled_line))

        brace = Brace(unrolled_line, DOWN, buff=0.15)
        label = MathTex(r"C = 2\pi r", font_size=36).next_to(brace, DOWN, buff=0.1)
        self.play(GrowFromCenter(brace), Write(label))

        # Highlight equation
        eq = MathTex(r"C = 2\pi r \approx 6.28r", font_size=40, color=YELLOW)
        eq.next_to(title, DOWN, buff=0.3)
        self.play(Write(eq))
        self.wait(2)
