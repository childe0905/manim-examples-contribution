from manim import *
import numpy as np

class RectangleAreaArrayModel(Scene):
    """
    用 4×3 方格陣列展示長方形面積等於列數乘以行數的教學動畫。
    格子依序逐行出現，並以 Brace 分別標示 columns（4）與 rows（3），
    最後呈現 4 × 3 = 12 的面積公式。
    """

    def construct(self):
        # [VISUAL REASONING]
        # 1. Goal: 讓學生直觀看到「面積 = 行數 × 列數」而非死記公式。
        # 2. Layout: 方格陣列置於畫面中央，columns Brace 在下方，
        #            rows Brace 在右方，公式在上方標題下方逐步呈現。
        # 3. Highlight: 格子逐行以 LaggedStart 出現，columns/rows 用不同顏色
        #               Brace 標示，最後公式中的數字與 Brace 同步顏色強調。

        COLS = 4
        ROWS = 3
        CELL = 0.9          # 每個方格的邊長
        COL_COLOR = BLUE
        ROW_COLOR = GREEN

        # ── 0. 標題 ──────────────────────────────────────────────────────────
        title = Title("Rectangle Area = columns × rows")
        self.play(Write(title))

        # ── 1. 建立方格陣列（置中） ───────────────────────────────────────────
        grid = VGroup()
        for row in range(ROWS):
            for col in range(COLS):
                cell = Square(
                    side_length=CELL,
                    color=WHITE,
                    fill_color=BLUE,
                    fill_opacity=0.35,
                    stroke_width=2,
                )
                # 計算每格的位置：以畫面中央為原點排列
                cell.move_to(
                    np.array([
                        (col - (COLS - 1) / 2) * CELL,
                        (row - (ROWS - 1) / 2) * -CELL,   # 往下為正 row
                        0,
                    ])
                )
                grid.add(cell)

        # 整體下移一點，留出標題空間
        grid.shift(DOWN * 0.5)

        # 逐行（row 為單位）以 LaggedStart 出現
        row_groups = [
            VGroup(*[grid[r * COLS + c] for c in range(COLS)])
            for r in range(ROWS)
        ]
        for row_grp in row_groups:
            self.play(
                LaggedStart(
                    *[DrawBorderThenFill(cell) for cell in row_grp],
                    lag_ratio=0.15,
                    run_time=0.7,
                )
            )
        self.wait(0.5)

        # ── 2. Brace 標示 columns（下方，藍色） ──────────────────────────────
        bottom_left  = grid[COLS * (ROWS - 1)].get_corner(DL)   # 左下角格子
        bottom_right = grid[COLS * ROWS - 1].get_corner(DR)      # 右下角格子

        brace_col = BraceBetweenPoints(bottom_left, bottom_right, direction=DOWN)
        brace_col.set_color(COL_COLOR)
        label_col = brace_col.get_tex(r"4\ \text{columns}").set_color(COL_COLOR)

        self.play(Create(brace_col), Write(label_col))

        # ── 3. Brace 標示 rows（右方，綠色） ─────────────────────────────────
        top_right    = grid[COLS - 1].get_corner(UR)             # 右上角格子
        bottom_right2 = grid[COLS * ROWS - 1].get_corner(DR)     # 右下角格子

        brace_row = BraceBetweenPoints(top_right, bottom_right2, direction=RIGHT)
        brace_row.set_color(ROW_COLOR)
        label_row = brace_row.get_tex(r"3\ \text{rows}").set_color(ROW_COLOR)

        self.play(Create(brace_row), Write(label_row))
        self.wait(0.8)

        # ── 4. 高亮最後一行格子，強調「數格子」的概念 ───────────────────────
        self.play(
            *[cell.animate.set_fill(YELLOW, opacity=0.7) for cell in row_groups[-1]],
            run_time=0.6,
        )
        self.play(
            *[cell.animate.set_fill(BLUE, opacity=0.35) for cell in row_groups[-1]],
            run_time=0.4,
        )
        self.wait(0.3)

        # ── 5. 推導公式 ─────────────────────────────────────────────────────
        formula = MathTex(
            r"\text{Area}",
            r"=",
            r"\underbrace{4}_{\text{col}}",
            r"\times",
            r"\underbrace{3}_{\text{row}}",
            r"=",
            r"12",
        ).scale(0.9).next_to(title, DOWN, buff=0.35)

        formula[2].set_color(COL_COLOR)    # 4 同藍色
        formula[4].set_color(ROW_COLOR)    # 3 同綠色
        formula[6].set_color(YELLOW)       # 12 黃色強調

        self.play(Write(formula))
        self.play(Indicate(formula[6], color=YELLOW, scale_factor=1.3))
        self.wait(2)
