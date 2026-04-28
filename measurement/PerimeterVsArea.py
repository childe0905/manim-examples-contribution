from manim import *
import numpy as np

class PerimeterVsArea(Scene):
    """
    用同一個 L 形圖形對比周長與面積的概念：
    先高亮內部區域展示面積，再高亮邊界展示周長，最後對照兩者差異。
    """

    def construct(self):
        # [VISUAL REASONING]
        # 1. Goal: 讓學生理解面積（內部覆蓋量）與周長（邊界總長）的差異。
        # 2. Layout: 標題固定頂部；L 形置於左半部中下方；
        #            公式與對照文字在右側，三區不重疊。
        # 3. Highlight: 面積用黃色半透明填色；周長用綠色粗邊框描繪；
        #               最終對比時兩者分別標色。

        UNIT = 0.7
        ORIGIN_PT = np.array([-3.5, -2.2, 0])
        TEXT_X = 3.2

        # ── 0. 標題 ──────────────────────────────────────────────────
        title = Title("Perimeter vs Area (L-Shape)")
        self.play(Write(title))

        # ── 1. 繪製 L 形 ────────────────────────────────────────────
        raw_pts = [
            [0, 0], [4, 0], [4, 2],
            [2, 2], [2, 4], [0, 4],
        ]
        pts = [ORIGIN_PT + np.array([x * UNIT, y * UNIT, 0])
               for x, y in raw_pts]

        l_shape = Polygon(*pts, color=BLUE, fill_opacity=0.15,
                          stroke_width=2)
        self.play(DrawBorderThenFill(l_shape))
        self.wait(0.5)

        # ── 2. 高亮內部 → 面積 ──────────────────────────────────────
        area_label = Text("Area", font_size=30, color=YELLOW)
        area_label.move_to([TEXT_X, 1.5, 0])

        area_fill = l_shape.copy().set_fill(YELLOW, opacity=0.6)
        area_fill.set_stroke(YELLOW, width=2)

        self.play(Write(area_label))
        self.play(FadeIn(area_fill))
        self.wait(0.5)

        area_formula = MathTex(
            r"A = 4 \times 4 - 2 \times 2 = ", r"12",
        ).scale(0.75).move_to([TEXT_X, 0.6, 0])
        area_formula[1].set_color(YELLOW)
        self.play(Write(area_formula))
        self.wait(1)

        # ── 3. 淡出面積填色，高亮邊界 → 周長 ────────────────────────
        self.play(FadeOut(area_fill))

        # 用粗邊框描繪周長
        perimeter_outline = l_shape.copy()
        perimeter_outline.set_fill(opacity=0)
        perimeter_outline.set_stroke(GREEN, width=6)

        peri_label = Text("Perimeter", font_size=30, color=GREEN)
        peri_label.move_to([TEXT_X, -0.4, 0])

        self.play(Write(peri_label), Create(perimeter_outline))
        self.wait(0.5)

        # 標示各段邊長
        edges = [
            (pts[0], pts[1], DOWN),   # 底 4
            (pts[1], pts[2], RIGHT),  # 右下 2
            (pts[2], pts[3], UP),     # 中橫 2
            (pts[3], pts[4], RIGHT),  # 中直 2
            (pts[4], pts[5], UP),     # 頂 2
            (pts[5], pts[0], LEFT),   # 左 4
        ]
        lengths = ["4", "2", "2", "2", "2", "4"]
        edge_labels = VGroup(*[
            Text(l, font_size=20, color=GREEN).next_to(
                Line(a, b), d, buff=0.12)
            for (a, b, d), l in zip(edges, lengths)
        ])
        self.play(FadeIn(edge_labels))
        self.wait(0.5)

        peri_formula = MathTex(
            r"P = 4{+}2{+}2{+}2{+}2{+}4 = ", r"16",
        ).scale(0.75).move_to([TEXT_X, -1.3, 0])
        peri_formula[1].set_color(GREEN)
        self.play(Write(peri_formula))
        self.wait(1)

        # ── 4. 對照結論 ─────────────────────────────────────────────
        compare = VGroup(
            MathTex(r"\text{Area} = 12", color=YELLOW),
            MathTex(r"\text{Perimeter} = 16", color=GREEN),
        ).arrange(DOWN, buff=0.3).scale(0.8).move_to([TEXT_X, -2.6, 0])

        self.play(
            FadeOut(area_label), FadeOut(peri_label),
            FadeOut(area_formula), FadeOut(peri_formula),
            FadeIn(compare),
        )
        self.play(Indicate(compare[0], color=YELLOW),
                  Indicate(compare[1], color=GREEN))
        self.wait(2)
