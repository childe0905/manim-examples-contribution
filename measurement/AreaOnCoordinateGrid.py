from manim import *
import numpy as np

class AreaOnCoordinateGrid(Scene):
    """
    在格線上畫矩形拼接圖形（左 2×3 + 右下 2×2），
    透過數單位格的方式計算總面積。
    """

    def construct(self):
        # [VISUAL REASONING]
        # 1. Goal: 用數格子的方法直觀求出組合圖形的面積。
        # 2. Layout: 標題頂部；格線與圖形置於左側偏中；
        #            計算公式與結果在右側。
        # 3. Highlight: 左區塊格子用藍色填色，右區塊用綠色填色，
        #               總面積用黃色強調。

        UNIT = 0.7
        GRID_ORIGIN = np.array([-4.0, -2.5, 0])
        TEXT_X = 3.5

        # ── 0. 標題 ──────────────────────────────────────────────────
        title = Title("Area on a Coordinate Grid")
        self.play(Write(title))

        # ── 1. 畫格線 ───────────────────────────────────────────────
        grid_lines = VGroup()
        for i in range(6):  # 垂直線 x=0..5
            grid_lines.add(Line(
                GRID_ORIGIN + np.array([i * UNIT, 0, 0]),
                GRID_ORIGIN + np.array([i * UNIT, 4 * UNIT, 0]),
                stroke_width=1, color=GRAY,
            ))
        for j in range(5):  # 水平線 y=0..4
            grid_lines.add(Line(
                GRID_ORIGIN + np.array([0, j * UNIT, 0]),
                GRID_ORIGIN + np.array([5 * UNIT, j * UNIT, 0]),
                stroke_width=1, color=GRAY,
            ))
        self.play(Create(grid_lines))

        # ── 2. 畫組合圖形外框 ───────────────────────────────────────
        # 左 2×3 + 右下 2×2，頂點順序：
        shape_raw = [
            [0, 0], [4, 0], [4, 2], [2, 2], [2, 3], [0, 3],
        ]
        shape_pts = [GRID_ORIGIN + np.array([x * UNIT, y * UNIT, 0])
                     for x, y in shape_raw]
        outline = Polygon(*shape_pts, color=WHITE, stroke_width=3,
                          fill_opacity=0)
        self.play(Create(outline))
        self.wait(0.5)

        # ── 3. 逐格填色 — 左區塊 (2×3 = 6 格，藍色) ────────────────
        left_squares = VGroup()
        for row in range(3):
            for col in range(2):
                sq = Square(side_length=UNIT, fill_color=BLUE,
                            fill_opacity=0.5, stroke_width=1,
                            stroke_color=WHITE)
                sq.move_to(GRID_ORIGIN + np.array([
                    (col + 0.5) * UNIT, (row + 0.5) * UNIT, 0]))
                left_squares.add(sq)

        self.play(LaggedStart(*[FadeIn(s) for s in left_squares],
                              lag_ratio=0.1))

        count_left = MathTex(r"A_1 = 2 \times 3 = 6", color=BLUE
                             ).scale(0.8).move_to([TEXT_X, 0.8, 0])
        self.play(Write(count_left))
        self.wait(0.5)

        # ── 4. 逐格填色 — 右區塊 (2×2 = 4 格，綠色) ────────────────
        right_squares = VGroup()
        for row in range(2):
            for col in range(2):
                sq = Square(side_length=UNIT, fill_color=GREEN,
                            fill_opacity=0.5, stroke_width=1,
                            stroke_color=WHITE)
                sq.move_to(GRID_ORIGIN + np.array([
                    (col + 2 + 0.5) * UNIT, (row + 0.5) * UNIT, 0]))
                right_squares.add(sq)

        self.play(LaggedStart(*[FadeIn(s) for s in right_squares],
                              lag_ratio=0.1))

        count_right = MathTex(r"A_2 = 2 \times 2 = 4", color=GREEN
                              ).scale(0.8).move_to([TEXT_X, -0.1, 0])
        self.play(Write(count_right))
        self.wait(0.5)

        # ── 5. 總面積 ───────────────────────────────────────────────
        total = MathTex(
            r"A_{\text{total}} = 6 + 4 = ", r"10"
        ).scale(0.85).move_to([TEXT_X, -1.2, 0])
        total[1].set_color(YELLOW)

        self.play(Write(total))
        self.play(Indicate(total[1], color=YELLOW))
        self.wait(2)
