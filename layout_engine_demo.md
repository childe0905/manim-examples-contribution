# Golden Example: Using the Constraint Layout Engine

This example demonstrates how to use the `utils.layout_engine` module to position objects dynamically without manual coordinate tweaking. This is the preferred method for complex scenes to avoid overlap.

## Problem

Arrange a Title, a Main Equation, and a Description such that:

1. Title is at the top.
2. Equation is centered below the title.
3. Description is below the equation.
4. All elements are horizontally centered.
5. Guaranteed 1.0 unit padding between elements.

## Solution

```python
from manim import *
from utils.layout_engine import LayoutEngine, LayoutObject

class ConstraintLayoutScene(Scene):
    def construct(self):
        # 1. Create content (initially at ORIGIN)
        title = Text("The Pythagorean Theorem", font_size=48)
        equation = MathTex("a^2 + b^2 = c^2", font_size=64)
        desc = Text("Relates the sides of a right triangle.", font_size=36)

        # 2. Add to Scene (for visualization)
        self.add(title, equation, desc)

        # 3. initialize Layout Engine
        layout = LayoutEngine()
        
        # 4. Register objects
        obj_title = LayoutObject(title, "title")
        obj_eq = LayoutObject(equation, "eq")
        obj_desc = LayoutObject(desc, "desc")

        layout.add(obj_title)
        layout.add(obj_eq)
        layout.add(obj_desc)

        # 5. Define Constraints
        
        # Vertical Arrangement
        # Title is fixed at UP*3 (optional anchor)
        # But let's use relative positioning:
        
        # Title matches Scene Top? No, let's fix title.
        title.to_edge(UP)
        # Update layout variable to match current position? 
        # No, better to constrain title.top == frame_top - 1.0
        # For simplicity, we can let title stay put and align others relative to it.
        
        # Equation BELOW Title with 1.0 buffer
        layout.next_to(obj_eq, obj_title, direction='DOWN', buff=1.0)
        
        # Description BELOW Equation with 0.8 buffer
        layout.next_to(obj_desc, obj_eq, direction='DOWN', buff=0.8)
        
        # Horizontal Center Alignment
        # All objects share the same Center X
        layout.align_to(obj_eq, obj_title, 'CENTER_X')
        layout.align_to(obj_desc, obj_title, 'CENTER_X')

        # 6. Solve and Apply
        layout.solve()
        
        # 7. Animate (optional)
        self.play(Write(title), Write(equation), Write(desc))
        self.wait()
```

## Key API Methods

- `LayoutObject(mobject, name)`: Wraps a Mobject.
- `layout.add(obj)`: Registers the object.
- `layout.next_to(objA, objB, direction, buff)`: Adds `A.edge == B.edge +/- buff` constraint.
- `layout.align_to(objA, objB, direction)`: Adds `A.edge == B.edge` constraint.
- `layout.solve()`: Calculates and applies positions to Mobjects.
