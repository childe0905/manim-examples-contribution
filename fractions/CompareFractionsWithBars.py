from manim import *

class CompareFractionsWithBars(Scene):
    """
    用同長度條帶比較 2/3 和 3/5。
    """

    def construct(self):
        # [VISUAL REASONING]
        # 1. Goal: 教授分數比較 2/3 > 3/5
        # 2. Layout: 畫面中央有上下排列的兩條等長度、寬度為 4 的矩形條帶
        # 3. Highlight: 畫出一條垂直虛線幫助對齊比較，最後標示出大於符號

        title = Text("分數比較", font_size=40).to_edge(UP, buff=0.5)
        self.play(Write(title))

        bar_width = 6  # 稍微放大寬度讓視覺更清楚
        bar_height = 0.8
        
        # 建立上方條帶 2/3
        top_group = VGroup()
        for _ in range(3):
            rect = Rectangle(width=bar_width/3, height=bar_height, color=WHITE, stroke_width=2)
            top_group.add(rect)
        top_group.arrange(RIGHT, buff=0)
        
        # 建立下方條帶 3/5
        bot_group = VGroup()
        for _ in range(5):
            rect = Rectangle(width=bar_width/5, height=bar_height, color=WHITE, stroke_width=2)
            bot_group.add(rect)
        bot_group.arrange(RIGHT, buff=0)
        
        # 兩者對齊
        bars = VGroup(top_group, bot_group).arrange(DOWN, buff=1.5).move_to(UP * 0.5)
        
        self.play(Create(top_group), Create(bot_group))
        self.wait(1)

        # Labels
        label_top = MathTex(r"\frac{2}{3}", font_size=48).next_to(top_group, LEFT, buff=0.5)
        label_bot = MathTex(r"\frac{3}{5}", font_size=48).next_to(bot_group, LEFT, buff=0.5)
        
        self.play(Write(label_top), Write(label_bot))
        
        # 1. 填色 2/3
        self.play(
            top_group[0].animate.set_fill(BLUE, opacity=0.7),
            top_group[1].animate.set_fill(BLUE, opacity=0.7)
        )
        self.wait(0.5)
        
        # 2. 填色 3/5
        self.play(
            bot_group[0].animate.set_fill(GREEN, opacity=0.7),
            bot_group[1].animate.set_fill(GREEN, opacity=0.7),
            bot_group[2].animate.set_fill(GREEN, opacity=0.7)
        )
        self.wait(1)

        # 3. 垂直虛線比較長度
        # 從上方 2/3 的結束邊緣畫出虛線
        p1 = top_group[1].get_corner(UR) + UP * 0.4
        p2 = np.array([p1[0], bot_group.get_bottom()[1] - 0.4, 0])
        compare_line = DashedLine(p1, p2, color=YELLOW, stroke_width=4)
        
        self.play(Create(compare_line))
        self.wait(1)

        # 4. 結尾算式
        eq_group = VGroup(
            MathTex(r"\frac{2}{3}", font_size=60),
            MathTex(">", font_size=60, color=YELLOW),
            MathTex(r"\frac{3}{5}", font_size=60)
        ).arrange(RIGHT, buff=0.5).next_to(bars, DOWN, buff=1.5)
        
        self.play(Write(eq_group))
        self.wait(2)
