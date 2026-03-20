from manim import *
import numpy as np

class PythagoreanTheorem(Scene):
    """
    Visual demonstration of a^2 + b^2 = c^2 using square areas.
    """
    def construct(self):
        # [VISUAL REASONING]
        # 1. Goal: Visually prove Pythagoras using square areas.
        # 2. Layout: Triangle in center-left, squares grow from each side.
        
        title = Tex(r"Pythagorean Theorem: $a^2 + b^2 = c^2$").to_edge(UP)
        self.play(Write(title))

        # Define 3-4-5 Triangle (scaled for screen)
        a, b, c = 3, 4, 5
        scale = 0.6
        
        # Build clean right triangle using Lines
        line_a = Line(ORIGIN, RIGHT * a * scale, color=BLUE, stroke_width=6)
        line_b = Line(ORIGIN, UP * b * scale, color=RED, stroke_width=6)
        line_c = Line(line_a.get_end(), line_b.get_end(), color=GREEN, stroke_width=6)
        
        triangle = VGroup(line_a, line_b, line_c)
        triangle.move_to(ORIGIN)  # Center the triangle
        
        self.play(Create(triangle))
        
        # Label sides
        lbl_a = MathTex("a", color=BLUE).next_to(line_a, DOWN)
        lbl_b = MathTex("b", color=RED).next_to(line_b, LEFT)
        lbl_c = MathTex("c", color=GREEN).next_to(line_c.get_center(), UR, buff=0.2)
        
        self.play(Write(lbl_a), Write(lbl_b), Write(lbl_c))
        self.wait()

        # Create Squares on a and b (easy positioning)
        sq_a = Square(side_length=a * scale, color=BLUE, fill_opacity=0.3, stroke_width=3)
        sq_a.next_to(line_a, DOWN, buff=0)
        
        sq_b = Square(side_length=b * scale, color=RED, fill_opacity=0.3, stroke_width=3)
        sq_b.next_to(line_b, LEFT, buff=0)
        
        self.play(Create(sq_a), Create(sq_b))
        
        # Labels for a^2 and b^2
        tex_a = MathTex("a^2", color=BLUE).move_to(sq_a.get_center())
        tex_b = MathTex("b^2", color=RED).move_to(sq_b.get_center())
        
        self.play(Write(tex_a), Write(tex_b))
        self.wait()

        # Square on hypotenuse c (using Polygon for precise positioning)
        # Strategy: One edge of square lies on hypotenuse, extending outward (away from right angle)
        
        # Get vertices of the hypotenuse line
        start_c = line_c.get_start()  # Bottom-right corner of triangle
        end_c = line_c.get_end()      # Top-left corner of triangle
        
        # Vector along hypotenuse (from start to end)
        hyp_vec = end_c - start_c
        
        # Vector perpendicular to hypotenuse (pointing away from right angle)
        # Rotate hypotenuse vector by 90 degrees clockwise (to point outward)
        perp_vec = np.array([hyp_vec[1], -hyp_vec[0], 0])
        # Normalize to unit length, then scale to square side length
        perp_vec = perp_vec / np.linalg.norm(perp_vec) * c * scale
        
        # 4 corners of the square:
        # Two corners are the hypotenuse endpoints, two are offset by perpendicular vector
        v1 = start_c
        v2 = end_c
        v3 = end_c + perp_vec
        v4 = start_c + perp_vec
        
        sq_c = Polygon(v1, v2, v3, v4, color=GREEN, fill_opacity=0.3, stroke_width=3)
        
        self.play(Create(sq_c))
        
        # Label c^2
        tex_c = MathTex("c^2", color=GREEN).move_to(sq_c.get_center())
        self.play(Write(tex_c))
        
        # Final emphasis
        self.play(
            sq_a.animate.set_fill(opacity=0.5),
            sq_b.animate.set_fill(opacity=0.5),
            sq_c.animate.set_fill(opacity=0.5)
        )
        
        self.wait(2)
