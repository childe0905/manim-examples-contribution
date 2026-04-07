from manim import *

class FractionAdditionAreaModel(Scene):
    """
    展示同分母分數加法 3/8 + 4/8 = 7/8
    """

    def construct(self):
        # [VISUAL REASONING]
        # 1. Goal: 教授同分母加法 3/8 + 4/8 = 7/8
        # 2. Layout: 畫面中央有一個寬度較大、有 8 格的橫條帶，下方有算式動態出現
        # 3. Highlight: 加上去的 4/8 與原有的 3/8 顏色不同，並用一個黃色框強調結果總和 7/8

        title = Text("同分母分數加法", font_size=40).to_edge(UP, buff=0.5)
        self.play(Write(title))

        bar_width = 6
        bar_height = 1.0
        parts = 8
        
        # 建立外框和格子
        bar_group = VGroup()
        for _ in range(parts):
            rect = Rectangle(
                width=bar_width/parts, 
                height=bar_height,
                color=WHITE,
                stroke_width=2
            )
            bar_group.add(rect)
        bar_group.arrange(RIGHT, buff=0).move_to(UP * 0.5)

        self.play(Create(bar_group))
        self.wait(1)

        # 建立算式的各個部分，準備放在長條下方
        eq_group = VGroup()
        f1 = MathTex(r"\frac{3}{8}", font_size=60)
        plus = MathTex("+", font_size=60)
        f2 = MathTex(r"\frac{4}{8}", font_size=60)
        eq = MathTex("=", font_size=60)
        f3 = MathTex(r"\frac{7}{8}", font_size=60)
        
        eq_group.add(f1, plus, f2, eq, f3)
        eq_group.arrange(RIGHT, buff=0.5).next_to(bar_group, DOWN, buff=1.5)

        # 1. 填入 3/8 (藍色)
        self.play(
            *[bar_group[i].animate.set_fill(BLUE, opacity=0.7) for i in range(3)],
            Write(f1)
        )
        self.wait(1)

        # 2. 填入 4/8 (綠色)
        self.play(Write(plus))
        self.play(
            *[bar_group[i].animate.set_fill(TEAL, opacity=0.7) for i in range(3, 7)],
            Write(f2)
        )
        self.wait(1)

        # 3. 得出 7/8
        self.play(Write(eq), Write(f3))
        self.wait(0.5)

        # 使用黃色框強調結果
        filled_parts = VGroup(*[bar_group[i] for i in range(7)])
        highlight_box = SurroundingRectangle(filled_parts, color=YELLOW, buff=0.1, stroke_width=4)
        
        self.play(Create(highlight_box))
        self.wait(2)
