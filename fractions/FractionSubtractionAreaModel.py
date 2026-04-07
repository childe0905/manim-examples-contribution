from manim import *

class FractionSubtractionAreaModel(Scene):
    """
    展示同分母分數減法 3/5 - 1/5 = 2/5
    """

    def construct(self):
        # [VISUAL REASONING]
        # 1. Goal: 教授同分母減法 3/5 - 1/5 = 2/5
        # 2. Layout: 畫面中央有一個拆成 5 格的橫條帶，下方是減法算式
        # 3. Highlight: 從原有的 3/5 中分離出 1/5 往下移動並變灰淡化，保留剩下的 2/5 並用框強調

        title = Text("同分母分數減法", font_size=40).to_edge(UP, buff=0.5)
        self.play(Write(title))

        bar_width = 5
        bar_height = 1.0
        parts = 5
        
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
        f1 = MathTex(r"\frac{3}{5}", font_size=60)
        minus = MathTex("-", font_size=60)
        f2 = MathTex(r"\frac{1}{5}", font_size=60)
        eq = MathTex("=", font_size=60)
        f3 = MathTex(r"\frac{2}{5}", font_size=60)
        
        eq_group.add(f1, minus, f2, eq, f3)
        eq_group.arrange(RIGHT, buff=0.5).next_to(bar_group, DOWN, buff=1.5)

        # 1. 填入 3/5 (藍色)
        self.play(
            bar_group[0].animate.set_fill(BLUE, opacity=0.7),
            bar_group[1].animate.set_fill(BLUE, opacity=0.7),
            bar_group[2].animate.set_fill(BLUE, opacity=0.7),
            Write(f1)
        )
        self.wait(1)

        # 2. 扣除 1/5：從第三個方塊中分離出來
        # 為了產生「拿走」的效果，我們複製第三個色塊，並向下移動、淡化
        self.play(Write(minus))
        
        # 複製要被減掉的那一塊
        removed_rect = bar_group[2].copy()
        self.add(removed_rect)
        
        self.play(
            removed_rect.animate.shift(DOWN * 1.5 + RIGHT * 1.0).set_fill(GRAY, opacity=0.3).set_stroke(opacity=0.3),
            bar_group[2].animate.set_fill(opacity=0),
            Write(f2)
        )
        self.wait(1)

        # 3. 剩下 2/5
        self.play(Write(eq), Write(f3))
        self.wait(0.5)

        # 使用黃色框強調剩下的 2/5
        filled_parts = VGroup(bar_group[0], bar_group[1])
        highlight_box = SurroundingRectangle(filled_parts, color=YELLOW, buff=0.1, stroke_width=4)
        
        self.play(Create(highlight_box))
        
        # 淡出被拿走的方塊
        self.play(FadeOut(removed_rect))
        
        self.wait(2)
