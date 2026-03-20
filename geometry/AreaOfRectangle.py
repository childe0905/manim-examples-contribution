from manim import *

class AreaOfRectangle(Scene):
    """
    Derives the area formula (Length x Width) using a grid method.
    """
    def construct(self):
        # [VISUAL REASONING]
        # 1. Pedagogical Goal: Show that Area = sum of unit squares.
        # 2. Layout: Grid rectangle in center, formula derived on side.
        
        title = Text("Area of Rectangle").to_edge(UP)
        self.play(Write(title))

        # Parameters
        width = 5
        height = 3
        sq_size = 1.0

        # Create the grid
        grid = VGroup()
        for h in range(height):
            for w in range(width):
                sq = Square(side_length=sq_size, color=BLUE, fill_opacity=0.2)
                # Position logic: center the grid
                # (w * sq_size) is x offset, (h * sq_size) is y offset
                # We need to center the whole group later, so relative pos is fine
                sq.move_to([w * sq_size, h * sq_size, 0])
                grid.add(sq)
        
        grid.move_to(ORIGIN)
        self.play(Create(grid, run_time=2))

        # Label Dimensions
        brace_w = Brace(grid, direction=DOWN)
        label_w = brace_w.get_text(str(width))
        
        brace_h = Brace(grid, direction=LEFT)
        label_h = brace_h.get_text(str(height))
        
        self.play(GrowFromCenter(brace_w), Write(label_w))
        self.play(GrowFromCenter(brace_h), Write(label_h))
        self.wait()

        # Count squares visual cue
        count_text = Text("Count Squares:", font_size=24).to_corner(UL).shift(DOWN)
        self.play(Write(count_text))
        
        counter = Integer(0).next_to(count_text, RIGHT)
        self.add(counter)

        # Highlight squares one by one (fast)
        for sq in grid:
            self.play(sq.animate.set_fill(YELLOW, 0.6), counter.animate.increment_value(1), run_time=0.1)
        
        self.wait(0.5)

        # Derive Formula
        formula = MathTex(r"\text{Area} = \text{Width} \times \text{Height}").to_edge(UP).shift(DOWN)
        calc = MathTex(f"\\text{{Area}} = {width} \\times {height} = {width*height}").next_to(formula, DOWN)
        
        self.play(Write(formula))
        self.play(Write(calc))
        
        # Final Box
        self.play(grid.animate.set_color(GREEN))
        self.wait(2)
