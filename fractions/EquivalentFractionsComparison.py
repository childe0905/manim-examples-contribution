from manim import *

class EquivalentFractionsComparison(Scene):
    """
    展示擴分比較 1/2 與 3/8 -> 4/8 與 3/8
    """

    def construct(self):
        # [VISUAL REASONING]
        # 1. Goal: 教授擴分比較 1/2 > 3/8
        # 2. Layout: 畫面中央有上下排列兩條等長度的矩形條帶
        # 3. Highlight: 畫出切分的虛線，展示 1/2 變成 4/8，最後比較大小並標示

        title = Text("擴分比較", font_size=40).to_edge(UP, buff=0.5)
        self.play(Write(title))

        bar_width = 8
        bar_height = 0.8
        
        # 建立上方條帶 1/2
        top_group = VGroup()
        for _ in range(2):
            rect = Rectangle(width=bar_width/2, height=bar_height, color=WHITE, stroke_width=2)
            top_group.add(rect)
        top_group.arrange(RIGHT, buff=0)
        
        # 建立下方條帶 3/8
        bot_group = VGroup()
        for _ in range(8):
            rect = Rectangle(width=bar_width/8, height=bar_height, color=WHITE, stroke_width=2)
            bot_group.add(rect)
        bot_group.arrange(RIGHT, buff=0)
        
        # 兩者對齊
        bars = VGroup(top_group, bot_group).arrange(DOWN, buff=1.5).move_to(UP * 0.5)
        
        self.play(Create(top_group), Create(bot_group))
        self.wait(1)

        # Labels
        label_top = MathTex(r"\frac{1}{2}", font_size=48).next_to(top_group, LEFT, buff=0.5)
        label_bot = MathTex(r"\frac{3}{8}", font_size=48).next_to(bot_group, LEFT, buff=0.5)
        
        self.play(Write(label_top), Write(label_bot))
        
        # 1. 填色 1/2
        self.play(
            top_group[0].animate.set_fill(BLUE, opacity=0.7)
        )
        self.wait(0.5)
        
        # 2. 填色 3/8
        self.play(
            bot_group[0].animate.set_fill(GREEN, opacity=0.7),
            bot_group[1].animate.set_fill(GREEN, opacity=0.7),
            bot_group[2].animate.set_fill(GREEN, opacity=0.7)
        )
        self.wait(1)

        # 3. 擴分：將上面的 1/2 切成 4/8
        # 我們要在上方內部畫出額外的分隔線，使其與下方的 1/8 大小相同
        cut_lines = VGroup()
        cell_w = bar_width / 8
        start_x = top_group.get_left()[0]
        
        for i in [1, 2, 3, 5, 6, 7]:
            x_pos = start_x + i * cell_w
            p_top = np.array([x_pos, top_group.get_top()[1], 0])
            p_bot = np.array([x_pos, top_group.get_bottom()[1], 0])
            line = DashedLine(p_top + UP * 0.1, p_bot + DOWN * 0.1, color=YELLOW, stroke_width=2)
            cut_lines.add(line)
            
        self.play(Create(cut_lines), run_time=2)
        
        # 更新標籤 1/2 -> 4/8
        label_top_new = MathTex(r"\frac{4}{8}", font_size=48).move_to(label_top)
        self.play(Transform(label_top, label_top_new))
        self.wait(1)

        # 4. 垂直比較線
        p1 = np.array([start_x + 4 * cell_w, top_group.get_top()[1] + 0.4, 0])
        p2 = np.array([p1[0], bot_group.get_bottom()[1] - 0.4, 0])
        compare_line = DashedLine(p1, p2, color=YELLOW, stroke_width=4)
        
        self.play(Create(compare_line))
        self.wait(1)

        # 5. 結尾算式
        eq_group = VGroup(
            MathTex(r"\frac{1}{2} = \frac{4}{8}", font_size=60),
            MathTex(">", font_size=60, color=YELLOW),
            MathTex(r"\frac{3}{8}", font_size=60)
        ).arrange(RIGHT, buff=0.5).next_to(bars, DOWN, buff=0.8)
        
        self.play(Write(eq_group))
        self.wait(2)
