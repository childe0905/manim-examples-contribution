from manim import *
import numpy as np


class CircleUnrolling_ArcPeel(Scene):
    """
    Visual proof that C = 2*pi*r by "peeling" the circle's arc into a line.

    Strategy: Topological Rectification (Arc-Peel)
    - A ValueTracker controls the remaining arc angle (TAU → 0.01).
    - always_redraw redraws both the shrinking arc and the growing line each frame.
    - The line grows from the circle's bottom toward the right.
    - Avoid angle=0 exactly → use 0.01 as proxy (near-zero is numerically stable).
    - Cleanup redrawables at the end; display static final state with Brace.

    Verified techniques from Deep Research (Feb 2026):
    - always_redraw for both arc and line (Copilot/GPT reports)
    - Near-zero proxy 0.01 instead of 0 (Gemini "Rectification Pattern")
    - ValueTracker.animate.set_value(0.01) with rate_func=linear
    - FadeOut redrawable mobjects, self.add() static finals for clean finish

    Anti-patterns AVOIDED:
    - Transform(Arc, Line) with mismatched point counts (path-jumping glitch)
    - become() in updater (120s timeout risk)
    - angle=0 in Arc(...) (divide-by-zero in normal/center calculations)

    topic: geometry | circumference | pi | circle | arc | unrolling | morphing
    """
    def construct(self):
        r = 1.5
        circumference = TAU * r  # = 2*pi*r

        # ── Setup ─────────────────────────────────────────────────────────────
        title = Tex(r"Circle Unrolling: Arc Peeling Method",
                    font_size=34).to_edge(UP)

        # Static circle (ghost reference, fades out)
        ghost_circle = Circle(radius=r, color=GRAY, stroke_width=1.5, stroke_opacity=0.4)
        ghost_circle.move_to(UP * 0.5)
        circle_center = ghost_circle.get_center()

        # Ground line below circle
        ground = Line(
            LEFT * 0.3,
            RIGHT * (circumference + 0.5),
            color=GRAY, stroke_width=2
        ).next_to(ghost_circle, DOWN, buff=0).shift(DOWN * r)
        ground_y = ground.get_y()

        # Starting label
        circ_label = MathTex(r"C = ?", font_size=36).next_to(ghost_circle, LEFT, buff=0.3)

        self.play(Write(title))
        self.play(Create(ghost_circle), Create(ground), Write(circ_label))
        self.wait(0.5)

        # ── Peel Animation ────────────────────────────────────────────────────
        angle_tracker = ValueTracker(TAU)

        # The remaining arc (shrinks from a full circle to near-zero)
        peeling_arc = always_redraw(lambda: Arc(
            radius=r,
            start_angle=-PI / 2 + (TAU - angle_tracker.get_value()),
            angle=angle_tracker.get_value(),
            color=BLUE,
            arc_center=circle_center,
            stroke_width=3
        ))

        # The unrolled line (grows from circle bottom toward the right)
        # Length = circumference * fraction already unrolled
        unrolled_fraction = always_redraw(lambda: Line(
            start=circle_center + DOWN * r,   # bottom of circle
            end=circle_center + DOWN * r + RIGHT * r * (TAU - angle_tracker.get_value()),
            color=YELLOW,
            stroke_width=3
        ))

        self.add(peeling_arc, unrolled_fraction)
        self.remove(ghost_circle)   # hide ghost (arc covers it)

        # Animate — rate_func=linear for smooth, uniform peel
        # Stop at 0.01, NOT 0 (numerically stable proxy for "fully unrolled")
        self.play(
            angle_tracker.animate.set_value(0.01),
            FadeOut(circ_label),
            run_time=5,
            rate_func=linear
        )
        self.wait(0.3)

        # ── Final Static State ────────────────────────────────────────────────
        # Remove always_redraw objects; replace with clean static versions
        final_line = Line(
            circle_center + DOWN * r,
            circle_center + DOWN * r + RIGHT * circumference,
            color=YELLOW, stroke_width=4
        )
        self.remove(peeling_arc, unrolled_fraction)
        self.add(final_line)

        # Show measurement
        brace = Brace(final_line, DOWN, buff=0.15, color=WHITE)
        brace_label = MathTex(r"C = 2\pi r", font_size=36).next_to(brace, DOWN, buff=0.1)
        self.play(GrowFromCenter(brace), Write(brace_label))

        # Show a diameter line for comparison
        diameter_line = Line(
            circle_center + LEFT * r,
            circle_center + RIGHT * r,
            color=GREEN, stroke_width=3
        )
        d_label = MathTex("d = 2r", color=GREEN, font_size=32).next_to(diameter_line, UP)
        self.play(Create(diameter_line), Write(d_label))

        # Final equation
        eq = MathTex(r"C = \pi \cdot d = 2\pi r", font_size=40, color=YELLOW)
        eq.to_edge(DOWN, buff=1.2)
        self.play(Write(eq))
        self.wait(2)
