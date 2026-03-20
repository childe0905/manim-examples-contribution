from manim import *
import numpy as np

class AdditionScene(Scene):
    def construct(self):
        equation = MathTex("2", "+", "3", "=", "5")
        equation.scale(2)
        
        # Display addition
        self.play(Write(equation[0:3]))
        self.wait(1)
        self.play(Write(equation[3:5]))
        self.wait(2)

class RiemannRectanglesExample(Scene):
    def construct(self):
        ax = Axes(
            x_range=[0, 5],
            y_range=[0, 6],
            x_length=7,
            y_length=5,
            axis_config={"include_tip": True}
        )
        labels = ax.get_axis_labels(x_label="x", y_label="f(x)")
        
        # Define a function
        curve = ax.plot(lambda x: 0.1 * x**3 - 0.5 * x**2 + 3, color=BLUE)
        
        # Create Riemann rectangles
        rects = ax.get_riemann_rectangles(
            curve, 
            x_range=[0.5, 4.5], 
            dx=0.5, 
            stroke_width=1, 
            fill_opacity=0.5
        )
        
        self.add(ax, labels)
        self.play(Create(curve))
        self.play(Create(rects))
        self.wait(2)

class ComplexTransformationExample(Scene):
    def construct(self):
        plane = ComplexPlane().add_coordinates()
        self.add(plane)
        
        # A simple shape to transform
        square = Square(side_length=2, color=YELLOW).shift(UP + RIGHT)
        self.play(Create(square))
        self.wait(1)
        
        # Apply the complex transformation z^2
        self.play(
            square.animate.apply_complex_function(lambda z: z**2),
            run_time=3
        )
        self.wait(2)

class FourierSeriesExample(Scene):
    def construct(self):
        # A simplified visualization of a square wave construction
        axes = Axes(x_range=[0, 10, 1], y_range=[-2, 2, 1], x_length=10)
        
        # First harmonic (Sine wave)
        f1 = axes.plot(lambda x: np.sin(x), color=RED)
        t1 = Text("Harmonic 1", color=RED).to_edge(UP)
        
        # Sum of first two harmonics
        f2 = axes.plot(lambda x: np.sin(x) + (1/3) * np.sin(3*x), color=YELLOW)
        t2 = Text("Harmonic 1 + 3", color=YELLOW).to_edge(UP)
        
        # Approaching square wave
        f3 = axes.plot(lambda x: sum((1/n) * np.sin(n*x) for n in range(1, 10, 2)), color=GREEN)
        t3 = Text("Harmonic Sum (n=1 to 9)", color=GREEN).to_edge(UP)

        self.add(axes)
        self.play(Create(f1), Write(t1))
        self.wait(1)
        self.play(Transform(f1, f2), Transform(t1, t2))
        self.wait(1)
        self.play(Transform(f1, f3), Transform(t1, t3))
        self.wait(2)
