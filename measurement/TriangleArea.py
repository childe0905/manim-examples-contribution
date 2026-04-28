from manim import *
import numpy as np

class TriangleArea(Scene):
    """
    展示三角形面積公式 (1/2 × base × height) 的教學動畫，
    透過將三角形複製並重組成平行四邊形來推導面積。
    畫面採左文右圖布局：圖形置於右側，文字標籤與公式置於左側。
    """

    def construct(self):
        # [VISUAL REASONING]
        # 1. Goal: 教學三角形面積為底乘以高的一半。
        # 2. Layout: 畫面右半部放三角形與幾何動作；左半部放文字說明與公式，
        #            兩者完全不重疊，用垂直分割線分隔。
        # 3. Highlight: 高度線段以虛線強調，複製的三角形用黃色區分並拼成平行四邊形，
        #               公式中的 1/2 用黃色 Indicate 閃爍強調。

        GRAPH_OFFSET = np.array([2.5, -0.5, 0])   # 右側圖形的整體偏移量
        TEXT_X = -4.2                               # 左側文字欄的 x 軸固定位置

        # ── 0. 標題 ──────────────────────────────────────────────────────────
        title = Title("Area of a Triangle")
        self.play(Write(title))

        # ── 1. 繪製三角形（右側） ──────────────────────────────────────────────
        # 頂點座標全部加上 GRAPH_OFFSET，讓圖形整體擺在右側
        p1 = np.array([-2, -1.5, 0]) + GRAPH_OFFSET
        p2 = np.array([ 2, -1.5, 0]) + GRAPH_OFFSET
        p3 = np.array([0.5,  1.5, 0]) + GRAPH_OFFSET

        triangle = Polygon(p1, p2, p3, color=BLUE, fill_opacity=0.5)
        self.play(DrawBorderThenFill(triangle))

        # ── 2. 標示底 base（左側文字欄） ────────────────────────────────────────
        label_base = Text("base", color=BLUE, font_size=32)
        label_base.move_to([TEXT_X, 0.8, 0])

        arrow_base = Arrow(
            start=label_base.get_right() + RIGHT * 0.1,
            end=np.array([p1[0] + (p2[0] - p1[0]) / 2, p1[1] - 0.15, 0]),
            color=BLUE, stroke_width=2, max_tip_length_to_length_ratio=0.15
        )
        self.play(Write(label_base), Create(arrow_base))

        # 底邊用 Brace 在圖形上標示（純幾何，沒有文字）
        base_brace = Brace(Line(p1, p2), DOWN, color=BLUE)
        self.play(Create(base_brace))

        # ── 3. 畫高（右側虛線）並在左側標示 height ──────────────────────────────
        h_foot = np.array([p3[0], p1[1], 0])       # 高的垂足（投影到底邊上）
        height_line = DashedLine(p3, h_foot, color=WHITE)
        self.play(Create(height_line))

        label_height = Text("height", color=WHITE, font_size=32)
        label_height.move_to([TEXT_X, 0.1, 0])

        arrow_height = Arrow(
            start=label_height.get_right() + RIGHT * 0.1,
            end=np.array([h_foot[0] - 0.1, (p3[1] + h_foot[1]) / 2, 0]),
            color=WHITE, stroke_width=2, max_tip_length_to_length_ratio=0.15
        )
        self.play(Write(label_height), Create(arrow_height))
        self.wait(1)

        # ── 4. 複製三角形並旋轉，拼成平行四邊形（右側） ───────────────────────────
        tri_copy = triangle.copy().set_color(YELLOW).set_fill(opacity=0.5)
        mid_point = (p2 + p3) / 2      # p2-p3 邊中點作為旋轉軸
        self.play(tri_copy.animate.rotate(PI, about_point=mid_point))
        self.wait(0.8)

        # 左側提示文字
        label_parallelogram = Text("= Parallelogram!", color=YELLOW, font_size=28)
        label_parallelogram.move_to([TEXT_X, -0.7, 0])
        self.play(Write(label_parallelogram))
        self.wait(0.8)

        # ── 5. 推導公式（左側） ────────────────────────────────────────────────
        para_formula = MathTex(
            r"A_{\text{para}} = b \times h"
        ).move_to([TEXT_X, -1.5, 0]).scale(0.85)

        self.play(Write(para_formula))
        self.wait(0.8)

        tri_formula = MathTex(
            r"A_{\triangle} =", r"\frac{1}{2}", r"\times b \times h"
        ).next_to(para_formula, DOWN, buff=0.4).scale(0.85)
        tri_formula[1].set_color(YELLOW)

        self.play(
            FadeOut(tri_copy),
            TransformFromCopy(para_formula, tri_formula)
        )
        self.play(Indicate(tri_formula[1], color=YELLOW))
        self.wait(2)
