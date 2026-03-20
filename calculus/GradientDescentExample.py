from manim import *
import numpy as np

class GradientDescentExample(ThreeDScene):
    """
    Synthesized from Manimator's 'Gradient Descent' plan.
    Demonstrates finding minimum on a 3D surface.
    """
    def construct(self):
        # 1. Setup 3D Scene
        axes = ThreeDAxes(
            x_range=[-3, 3, 1],
            y_range=[-3, 3, 1],
            z_range=[-1, 5, 1],
            x_length=6,
            y_length=6,
            z_length=4
        )
        self.set_camera_orientation(phi=60 * DEG, theta=-45 * DEG)
        
        # Loss function: L(x, y) = x^2 + y^2
        surface = Surface(
            lambda u, v: np.array([
                u,
                v,
                0.5 * (u**2 + v**2)
            ]),
            u_range=[-2.5, 2.5],
            v_range=[-2.5, 2.5],
            resolution=(30, 30),
            should_make_jagged=True
        )
        
        surface.set_style(fill_opacity=0.7, stroke_color=BLUE_A, stroke_width=0.5)
        surface.set_fill_by_checkerboard(BLUE, BLUE_E)

        title = Text("Gradient Descent", font_size=40).to_corner(UL)
        self.add_fixed_in_frame_mobjects(title)
        
        self.play(Create(axes), Create(surface), Write(title))
        self.wait(1)

        # 2. Gradient Descent Algorithm
        # Start point (high loss)
        start_x, start_y = 2.0, 2.0
        learning_rate = 0.2
        iterations = 8
        
        points = []
        curr_x, curr_y = start_x, start_y
        
        for _ in range(iterations):
            # z = 0.5*(x^2 + y^2)
            curr_z = 0.5 * (curr_x**2 + curr_y**2)
            points.append([curr_x, curr_y, curr_z])
            
            # Gradient: (x, y)
            grad_x, grad_y = curr_x, curr_y
            
            # Update
            curr_x -= learning_rate * grad_x
            curr_y -= learning_rate * grad_y

        # Visualizing the path
        path_dots = VGroup()
        path_lines = VGroup()
        
        prev_dot = None
        
        formula = MathTex(
            "\\theta_{new} = \\theta_{old} - \\alpha \\nabla L(\\theta)"
        ).to_corner(DL).scale(0.7)
        self.add_fixed_in_frame_mobjects(formula)
        self.play(Write(formula))

        for i, point in enumerate(points):
            dot = Dot3D(point=axes.c2p(*point), color=RED, radius=0.1)
            path_dots.add(dot)
            
            self.play(FadeIn(dot, scale=0.5), run_time=0.5)
            
            if prev_dot:
                line = Line3D(prev_dot.get_center(), dot.get_center(), color=YELLOW)
                path_lines.add(line)
                self.play(Create(line), run_time=0.3)
            
            prev_dot = dot
            
            if i == 0:
                label = Text("Start", font_size=20).next_to(title, DOWN)
                self.add_fixed_in_frame_mobjects(label)
                self.wait(0.5)
                self.remove(label)

        # 3. Rotate to show minimum
        self.move_camera(phi=75 * DEG, theta=-135 * DEG, run_time=3)
        
        min_label = Text("Global Minimum", font_size=24, color=GREEN)
        min_label.to_corner(DR)
        self.add_fixed_in_frame_mobjects(min_label)
        self.play(Indicate(path_dots[-1], color=GREEN))
        self.wait(2)

        # Cleanup
        self.play(FadeOut(VGroup(axes, surface, path_dots, path_lines)))
        self.play(FadeOut(title), FadeOut(formula), FadeOut(min_label))
