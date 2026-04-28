from manim import *
import numpy as np

class CompositeArea(Scene):
    """
    展示 L 形複合圖形的面積計算：將 L 形拆成兩個長方形，
    分別算出面積後再相加，得到總面積。
    """

    def construct(self):
        # [VISUAL REASONING]
        # 1. Goal: 教學如何將複合圖形拆解成基本圖形來計算面積。
        # 2. Layout: 標題固定在頂部；L 形圖形置於畫面左半部中下方；
        #            公式與標籤置於右側，三區分開不重疊。
        #            L 形由外框 4×4 挖掉右上角 2×2 形成。
        # 3. Highlight: 拆分後的兩塊長方形分別用藍色與綠色填色，
        #               最終面積加總用黃色強調。

        UNIT = 0.7                                      # 每格邊長（縮放因子）
        ORIGIN_PT = np.array([-3.5, -2.5, 0])           # 圖形左下角位置
        TEXT_X = 3.2                                     # 右側文字欄 x 位置

        # ── 0. 標題 ──────────────────────────────────────────────────
        title = Title("Area of a Composite Shape (L-Shape)")
        self.play(Write(title))

        # ── 1. 繪製 L 形 ────────────────────────────────────────────
        # L 形頂點（外框 4×4 挖掉右上角 2×2）
        # 頂點順序：左下 → 右下 → 右中 → 中中 → 中上 → 左上
        raw_pts = [
            [0, 0], [4, 0], [4, 2],
            [2, 2], [2, 4], [0, 4],
        ]
        pts = [ORIGIN_PT + np.array([x * UNIT, y * UNIT, 0])
               for x, y in raw_pts]

        l_shape = Polygon(*pts, color=BLUE, fill_opacity=0.3, stroke_width=3)
        self.play(DrawBorderThenFill(l_shape))

        # 在各邊標示尺寸
        dim_labels = VGroup(
            Text("4", font_size=22, color=WHITE).next_to(
                Line(pts[0], pts[1]), DOWN, buff=0.15),
            Text("2", font_size=22, color=WHITE).next_to(
                Line(pts[1], pts[2]), RIGHT, buff=0.15),
            Text("2", font_size=22, color=WHITE).next_to(
                Line(pts[2], pts[3]), UP, buff=0.15),
            Text("2", font_size=22, color=WHITE).next_to(
                Line(pts[3], pts[4]), RIGHT, buff=0.15),
            Text("2", font_size=22, color=WHITE).next_to(
                Line(pts[4], pts[5]), UP, buff=0.15),
            Text("4", font_size=22, color=WHITE).next_to(
                Line(pts[5], pts[0]), LEFT, buff=0.15),
        )
        self.play(FadeIn(dim_labels))
        self.wait(1)

        # ── 2. 拆分成兩個長方形 ─────────────────────────────────────
        # 垂直分割線 x=2，從 (2,0) 到 (2,2)（(2,2)→(2,4) 已是 L 形邊界）
        split_bottom = ORIGIN_PT + np.array([2 * UNIT, 0, 0])
        split_line = DashedLine(pts[3], split_bottom, color=YELLOW)
        self.play(Create(split_line))

        # 左側長方形 (2×4) — 藍色
        rl_pts = [pts[0], split_bottom, pts[4], pts[5]]
        rect_left = Polygon(*rl_pts, color=BLUE, fill_opacity=0.5,
                            stroke_width=2)

        # 右側長方形 (2×2) — 綠色
        rr_pts = [split_bottom, pts[1], pts[2], pts[3]]
        rect_right = Polygon(*rr_pts, color=GREEN, fill_opacity=0.5,
                             stroke_width=2)

        label_split = Text("Split into 2 rectangles",
                           font_size=26, color=YELLOW)
        label_split.move_to([TEXT_X, 1.8, 0])

        self.play(
            FadeOut(l_shape),
            DrawBorderThenFill(rect_left),
            DrawBorderThenFill(rect_right),
            Write(label_split),
        )
        self.wait(1)

        # ── 3. 標示各區塊面積（右側） ───────────────────────────────
        area_left = MathTex(
            r"A_1 = 2 \times 4 = 8", color=BLUE
        ).scale(0.8).move_to([TEXT_X, 0.6, 0])

        area_right = MathTex(
            r"A_2 = 2 \times 2 = 4", color=GREEN
        ).scale(0.8).move_to([TEXT_X, -0.2, 0])

        self.play(Indicate(rect_left, color=BLUE), Write(area_left))
        self.wait(0.5)

        self.play(Indicate(rect_right, color=GREEN), Write(area_right))
        self.wait(1)

        # ── 4. 加總面積 ─────────────────────────────────────────────
        total = MathTex(
            r"A_{\text{total}} = 8 + 4 = ", r"12", color=WHITE
        ).scale(0.85).move_to([TEXT_X, -1.3, 0])
        total[1].set_color(YELLOW)

        self.play(Write(total))
        self.play(Indicate(total[1], color=YELLOW))
        self.wait(2)
