from manim import *

class ComparingWithSameDenominator(Scene):
    """
    展示同分母分數比較 3/8 vs 5/8
    """

    def construct(self):
        # [VISUAL REASONING]
        # 1. Goal: 教授同分母比較 3/8 < 5/8
        # 2. Layout: 上下各一個長條，切分為8等分。上方填滿3格，下方填滿5格。
        # 3. Highlight: 畫出虛線幫助輔助視覺比較長度。

        title = Text("同分母分數比較", font_size=40).to_edge(UP, buff=0.3)
        self.play(Write(title))

        bar_width = 8
        bar_height = 1.0
        
        # 建立上方條帶 3/8
        top_group = VGroup()
        for i in range(8):
            rect = Rectangle(width=bar_width/8, height=bar_height, color=WHITE, stroke_width=2)
            top_group.add(rect)
        top_group.arrange(RIGHT, buff=0)
        
        # 建立下方條帶 5/8
        bot_group = VGroup()
        for i in range(8):
            rect = Rectangle(width=bar_width/8, height=bar_height, color=WHITE, stroke_width=2)
            bot_group.add(rect)
        bot_group.arrange(RIGHT, buff=0)
        
        # 排列
        bars = VGroup(top_group, bot_group).arrange(DOWN, buff=1.0).move_to(ORIGIN)
        
        self.play(Create(top_group), Create(bot_group))
        
        label_top = MathTex(r"\frac{3}{8}", font_size=50).next_to(top_group, LEFT, buff=0.5)
        label_bot = MathTex(r"\frac{5}{8}", font_size=50).next_to(bot_group, LEFT, buff=0.5)
        self.play(Write(label_top), Write(label_bot))
        self.wait(1)

        # 填色 3/8
        top_anims = []
        for i in range(3):
            top_anims.append(top_group[i].animate.set_fill(BLUE, opacity=0.8))
        self.play(*top_anims, run_time=1.5)
        
        # 填色 5/8
        bot_anims = []
        for i in range(5):
            bot_anims.append(bot_group[i].animate.set_fill(GREEN, opacity=0.8))
        self.play(*bot_anims, run_time=1.5)
        self.wait(1)

        # 畫虛線輔助比較
        # 從上方第3格的右邊界往下畫到下方
        x_pos_3 = top_group[2].get_right()[0]
        y_top = top_group.get_top()[1] + 0.2
        y_bot = bot_group.get_bottom()[1] - 0.2
        
        dash_line = DashedLine(
            start=np.array([x_pos_3, y_top, 0]),
            end=np.array([x_pos_3, y_bot, 0]),
            color=YELLOW,
            stroke_width=4
        )
        self.play(Create(dash_line))
        self.wait(0.5)

        # 把超出的兩格輕輕閃爍強調
        # bot_group 第 4, 5 格是 超出的部分 (index 3 and 4)
        extra_parts = VGroup(bot_group[3], bot_group[4])
        self.play(Indicate(extra_parts, color=YELLOW, scale_factor=1.1))
        self.wait(1)

        # 結尾算式大於符號
        eq_group = VGroup(
            MathTex(r"\frac{3}{8}", font_size=50),
            MathTex("<", font_size=50, color=YELLOW),
            MathTex(r"\frac{5}{8}", font_size=50)
        ).arrange(RIGHT, buff=0.5).to_edge(DOWN, buff=1.2)
        
        # 用 copy，讓原本的 label 留在原位比較好
        self.play(
            Transform(label_top.copy(), eq_group[0]),
            Transform(label_bot.copy(), eq_group[2]),
            Write(eq_group[1])
        )

        # 結論文字
        conclusion = Text("分母相同，分子越大，分數越大", font_size=36, color=YELLOW).next_to(eq_group, DOWN, buff=0.3)
        self.play(Write(conclusion))

        self.wait(3)
