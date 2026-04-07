from manim import *

class FractionMultiplicationAreaModel(Scene):
    """
    展示分數乘法面積模型 2/3 * 3/4 = 6/12 (包含約分展現)
    """

    def construct(self):
        title = Text("分數乘法面積模型", font_size=40).to_edge(UP, buff=0.1)
        self.play(Write(title))

        # 【修正 1】縮小正方形並重置於中央偏下，確保跟上面有足夠的空隙
        square_size = 3.6
        square = Square(side_length=square_size, color=WHITE, stroke_width=2).move_to(DOWN * 0.6)
        self.play(Create(square))
        self.wait(0.5)

        # 直切分成 3 等份，填滿左邊 2 份
        cols = VGroup()
        for i in range(3):
            col = Rectangle(width=square_size/3, height=square_size, color=WHITE, stroke_width=1.5)
            cols.add(col)
        cols.arrange(RIGHT, buff=0).move_to(square.get_center())
        
        self.play(Create(cols))
        
        # 填色前 2 列 (2/3)
        self.play(
            cols[0].animate.set_fill(BLUE, opacity=0.5),
            cols[1].animate.set_fill(BLUE, opacity=0.5)
        )
        
        # 大括號與長度標示
        brace_top = Brace(VGroup(cols[0], cols[1]), UP)
        label_top = MathTex(r"\text{Length} = \frac{2}{3}", font_size=44, color=BLUE).next_to(brace_top, UP, buff=0.25)
        
        self.play(FadeIn(brace_top), Write(label_top))
        self.play(Indicate(VGroup(cols[0], cols[1]), color=BLUE))
        self.wait(1)

        # 橫切分成 4 等份，填滿上面 3 份
        rows = VGroup()
        for i in range(4):
            row = Rectangle(width=square_size, height=square_size/4, color=WHITE, stroke_width=1.5)
            rows.add(row)
        rows.arrange(DOWN, buff=0).move_to(square.get_center())
        
        self.play(Create(rows))
        
        # 填色前 3 列 -> opacity 疊加自然呈現混色
        self.play(
            rows[0].animate.set_fill(YELLOW, opacity=0.5),
            rows[1].animate.set_fill(YELLOW, opacity=0.5),
            rows[2].animate.set_fill(YELLOW, opacity=0.5)
        )
        
        brace_left = Brace(VGroup(rows[0], rows[1], rows[2]), LEFT)
        label_left = MathTex(r"\text{Width} = \frac{3}{4}", font_size=44, color=YELLOW).next_to(brace_left, LEFT, buff=0.25)
        
        self.play(FadeIn(brace_left), Write(label_left))
        self.play(Indicate(VGroup(rows[0], rows[1], rows[2]), color=YELLOW))
        self.wait(1)

        # Highlight the overlap 交疊區塊 (2x3=6格)
        overlap_cells = VGroup()
        for r in range(3): 
            for c in range(2): 
                w = square_size/3
                h = square_size/4
                x_pos = cols[c].get_center()[0]
                y_pos = rows[r].get_center()[1]
                # 空心綠色外框強調疊加區
                cell = Rectangle(width=w, height=h, color=GREEN, stroke_width=4, fill_opacity=0).move_to(np.array([x_pos, y_pos, 0]))
                overlap_cells.add(cell)
        
        self.play(Create(overlap_cells), run_time=1.5)
        self.play(Indicate(overlap_cells, color=GREEN, scale_factor=1.05))
        self.wait(1)

        # Equation
        # 重新把中間步驟補回去，補足學生視覺化推演
        eq_group = VGroup(
            MathTex(r"\frac{2}{3}", color=BLUE),
            MathTex(r"\times"),
            MathTex(r"\frac{3}{4}", color=YELLOW),
            MathTex(r"="),
            MathTex(r"\frac{2 \times 3}{3 \times 4}"),
            MathTex(r"="),
            MathTex(r"\frac{6}{12}", color=GREEN)
        ).arrange(RIGHT, buff=0.25).scale(1.1).to_edge(DOWN, buff=0.3)
        
        # 【修正 2】 改用 ReplacementTransform 解決 shift 不同步脫節的 BUG
        self.play(
            ReplacementTransform(label_top.copy(), eq_group[0]),
            Write(eq_group[1]),
            ReplacementTransform(label_left.copy(), eq_group[2])
        )
        self.wait(0.5)
        self.play(Write(eq_group[3]), Write(eq_group[4]))
        self.wait(0.5)
        self.play(Write(eq_group[5]), Write(eq_group[6]))
        self.wait(1)

        # 約分動畫 (Transform overlap 6 cells to 1/2 rectangle)
        half_rect = Rectangle(
            width=square_size/2, height=square_size, 
            color=GREEN, stroke_width=4
        ).set_fill(GREEN, opacity=0.6).move_to(square.get_center() + LEFT * square_size/4)
        
        eq_simplify = VGroup(
            MathTex(r"="),
            MathTex(r"\frac{1}{2}", color=GREEN)
        ).scale(1.1).arrange(RIGHT, buff=0.25).next_to(eq_group, RIGHT, buff=0.25)
        
        shift_amount = LEFT * (eq_simplify.width / 2)
        
        self.play(
            eq_group.animate.shift(shift_amount),
            Transform(overlap_cells, half_rect),
            # 退去原本長條顏色的干擾
            cols[0].animate.set_fill(opacity=0),
            cols[1].animate.set_fill(opacity=0),
            rows[0].animate.set_fill(opacity=0),
            rows[1].animate.set_fill(opacity=0),
            rows[2].animate.set_fill(opacity=0),
        )
        eq_simplify.shift(shift_amount)
        self.play(Write(eq_simplify))

        self.wait(3)
