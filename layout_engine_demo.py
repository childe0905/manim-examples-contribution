from manim import *
from utils.layout_engine import LayoutEngine, LayoutObject

class ConstraintLayoutScene(Scene):
    """
    Demonstrates how to use the Constraint Layout Engine to position objects.
    
    Problem:
    Arrange a Title, a Main Equation, and a Description such that:
    1. Title is at the top.
    2. Equation is centered below the title.
    3. Description is below the equation.
    4. All elements are horizontally centered.
    5. Guaranteed 1.0 unit padding between elements.
    """
    def construct(self):
        # 1. Create content (initially at ORIGIN)
        title = Text("The Pythagorean Theorem", font_size=48)
        equation = MathTex("a^2 + b^2 = c^2", font_size=64)
        desc = Text("Relates the sides of a right triangle.", font_size=36)

        # 2. Add to Scene (for visualization)
        self.add(title, equation, desc)

        # 3. Initialize Layout Engine
        layout = LayoutEngine()
        
        # 4. Register objects
        obj_title = LayoutObject(title, "title")
        obj_eq = LayoutObject(equation, "eq")
        obj_desc = LayoutObject(desc, "desc")

        layout.add(obj_title)
        layout.add(obj_eq)
        layout.add(obj_desc)

        # 5. Define Constraints
        
        # Title matches Scene Top? No, let's fix title.
        title.to_edge(UP)
        
        # Equation BELOW Title with 1.0 buffer
        layout.next_to(obj_eq, obj_title, direction='DOWN', buff=1.0)
        
        # Description BELOW Equation with 0.8 buffer
        layout.next_to(obj_desc, obj_eq, direction='DOWN', buff=0.8)
        
        # Horizontal Center Alignment
        layout.align_to(obj_eq, obj_title, 'CENTER_X')
        layout.align_to(obj_desc, obj_title, 'CENTER_X')

        # 6. Solve and Apply
        layout.solve()
        
        # 7. Animate (optional)
        self.play(Write(title), Write(equation), Write(desc))
        self.wait()
