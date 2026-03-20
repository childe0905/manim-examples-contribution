from manim import *
import numpy as np

class FourierSeriesExample(Scene):
    """
    Synthesized from Manimator's 'Fourier Transform' plan.
    Demonstrates decomposition of a signal into sine waves.
    """
    def construct(self):
        # 1. Introduction
        title = Text("Fourier Transform: Decomposition", font_size=40, color=BLUE)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(1)

        # 2. Complex Signal (Time Domain)
        axes = Axes(
            x_range=[0, 10, 1],
            y_range=[-3, 3, 1],
            x_length=10,
            y_length=4,
            axis_config={"color": GREY}
        ).shift(DOWN * 0.5)
        
        labels = axes.get_axis_labels(x_label="Time (t)", y_label="Amplitude")
        self.play(Create(axes), Write(labels))

        # Function: f(t) = sin(t) + 0.5*sin(3t) + 0.3*sin(5t)
        def complex_signal(t):
            return np.sin(t) + 0.5 * np.sin(3 * t) + 0.3 * np.sin(5 * t)

        signal_graph = axes.plot(complex_signal, color=WHITE)
        signal_label = MathTex("f(t) = \\sum A_n \\sin(n \\omega t)").next_to(signal_graph, UP, buff=0.5)
        
        self.play(Create(signal_graph), Write(signal_label))
        self.wait(2)

        # 3. Decomposition Animation
        # Identify components
        comp1 = axes.plot(lambda t: np.sin(t), color=RED).set_opacity(0.5)
        comp2 = axes.plot(lambda t: 0.5 * np.sin(3 * t), color=GREEN).set_opacity(0.5)
        comp3 = axes.plot(lambda t: 0.3 * np.sin(5 * t), color=YELLOW).set_opacity(0.5)

        self.play(
            FadeOut(signal_graph),
            ReplacementTransform(signal_graph.copy(), comp1),
            ReplacementTransform(signal_graph.copy(), comp2),
            ReplacementTransform(signal_graph.copy(), comp3),
            run_time=2
        )
        self.wait(2)

        # 4. Frequency Domain Representation (Concept)
        # Shift time domain up
        time_group = VGroup(axes, labels, comp1, comp2, comp3, signal_label)
        self.play(time_group.animate.shift(UP * 2 + LEFT * 2).scale(0.7))

        # Frequency axes
        freq_axes = Axes(
            x_range=[0, 6, 1],
            y_range=[0, 1.5, 0.5],
            x_length=5,
            y_length=3,
            axis_config={"color": GREY}
        ).next_to(time_group, DOWN, buff=1).align_to(time_group, LEFT)
        
        freq_labels = freq_axes.get_axis_labels(x_label="Frequency (\\omega)", y_label="Magnitude")
        
        # Frequency bars
        bar1 = Line(freq_axes.c2p(1, 0), freq_axes.c2p(1, 1), color=RED, stroke_width=8)
        bar2 = Line(freq_axes.c2p(3, 0), freq_axes.c2p(3, 0.5), color=GREEN, stroke_width=8)
        bar3 = Line(freq_axes.c2p(5, 0), freq_axes.c2p(5, 0.3), color=YELLOW, stroke_width=8)

        self.play(Create(freq_axes), Write(freq_labels))
        self.play(
            TransformFromCopy(comp1, bar1),
            TransformFromCopy(comp2, bar2),
            TransformFromCopy(comp3, bar3),
            run_time=2
        )

        formula = MathTex(
            "\\hat{f}(\\xi) = \\int_{-\\infty}^{\\infty} f(t) e^{-2\\pi i \\xi t} dt"
        ).scale(0.8).next_to(freq_axes, RIGHT, buff=1)
        
        self.play(Write(formula))
        self.wait(3)

        # Cleanup
        self.play(FadeOut(VGroup(time_group, freq_axes, freq_labels, bar1, bar2, bar3, formula, title)))
