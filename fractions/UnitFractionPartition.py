from manim import *

class UnitFractionPartition(Scene):
    """
    展示單位分數的基本概念 1/2, 1/3, 1/4
    """

    def construct(self):
        # [VISUAL REASONING]
        # 1. Goal: 建立單位分數 (1/n) 的核心概念。
        # 2. Layout: 畫面中央一個寬度為 8 的長方形，用來代表「一個完整的單位」。
        # 3. Highlight: 連續展示切分成 2份、3份、4份，並且每次「只取 1 份」（填色）。

        title = Text("單位分數的基本概念", font_size=40).to_edge(UP, buff=0.3)
        self.play(Write(title))

        bar_width = 8
        bar_height = 1.2
        bar_center = UP * 0.5
        
        # 建立底層外框
        base_rect = Rectangle(width=bar_width, height=bar_height, color=WHITE, stroke_width=2).move_to(bar_center)
        self.play(Create(base_rect))
        
        caption = Text("一個完整的單位", font_size=36).next_to(base_rect, DOWN, buff=0.8)
        self.play(Write(caption))
        self.wait(1)
        
        def show_fraction(n, color):
            group = VGroup()
            for _ in range(n):
                rect = Rectangle(width=bar_width/n, height=bar_height, color=WHITE, stroke_width=2)
                group.add(rect)
            group.arrange(RIGHT, buff=0).move_to(bar_center)
            
            # 從左到右畫出格子
            self.play(Create(group), run_time=1)
            
            # 填色第一格
            self.play(group[0].animate.set_fill(color, opacity=0.8))
            
            # 更新字樣
            new_caption = Text(f"切分 {n} 等份，取其中 1 份", font_size=36).move_to(caption)
            frac_label = MathTex(rf"\frac{{1}}{{{n}}}", font_size=60).next_to(new_caption, DOWN, buff=0.3)
            
            self.play(
                Transform(caption, new_caption),
                FadeIn(frac_label, shift=DOWN)
            )
            self.wait(1.5)
            
            return group, frac_label

        # 1/2
        g2, l2 = show_fraction(2, BLUE)
        self.play(FadeOut(g2), FadeOut(l2))
        
        # 1/3
        g3, l3 = show_fraction(3, GREEN)
        self.play(FadeOut(g3), FadeOut(l3))
        
        # 1/4
        g4, l4 = show_fraction(4, ORANGE)
        
        # 結論
        conclusion = Text("這類分子為 1 的分數，我們稱為『單位分數』", font_size=36, color=YELLOW).to_edge(DOWN, buff=0.4)
        self.play(Write(conclusion))

        self.wait(3)
