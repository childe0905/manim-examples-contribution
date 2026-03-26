from manim import *
import numpy as np


class MidpointFormula(Scene):
    """
    在座標平面上取兩點，連線後標示中點，
    並動態展示中點公式：M = ((x₁+x₂)/2, (y₁+y₂)/2)
    """

    def construct(self):
        # [VISUAL REASONING]
        # 1. Goal: 讓學生直觀理解「中點就是兩點的平均值」
        # 2. Layout（防重疊）：
        #    - NumberPlane 全螢幕置中
        #    - 【左半邊 x < 0】圖形：兩點 A(-5,-2) 和 B(-1,3)，中點 M
        #      - 所有點、線、標籤都在 x < 0 的範圍內
        #      - 輔助的水平/垂直虛線從兩點延伸標示 x、y 座標
        #    - 【右半邊 x > 0.5】文字：中點公式推導與代入計算
        #    - 虛線分隔線於 x=0

        # --- 座標系（全螢幕） ---
        plane = NumberPlane(
            x_range=[-7, 7, 1],
            y_range=[-4, 4, 1],
            background_line_style={"stroke_opacity": 0.4},
        )
        self.play(Create(plane), run_time=1.5)

        # --- 兩點（左半邊） ---
        # A(-5, -2)、B(-1, 3) → 中點 M = (-3, 0.5)
        A = plane.c2p(-5, -2)
        B = plane.c2p(-1,  3)
        M = plane.c2p(-3, 0.5)   # 中點

        dot_A = Dot(A, color=YELLOW, radius=0.08)
        dot_B = Dot(B, color=YELLOW, radius=0.08)
        label_A = MathTex(r"A(-5,\ -2)", font_size=26).next_to(dot_A, DL, buff=0.12)
        label_B = MathTex(r"B(-1,\ 3)", font_size=26).next_to(dot_B, UL, buff=0.12)

        self.play(FadeIn(dot_A, dot_B), Write(label_A), Write(label_B))
        self.wait(0.4)

        # --- 連線 AB ---
        line_AB = Line(A, B, color=WHITE, stroke_width=2.5)
        self.play(Create(line_AB))
        self.wait(0.3)

        # --- 標示中點 M ---
        dot_M = Dot(M, color=RED, radius=0.1)
        label_M = MathTex(r"M\ =\ ?", font_size=28, color=RED).next_to(dot_M, RIGHT, buff=0.15)
        self.play(FadeIn(dot_M), Write(label_M))
        self.wait(0.4)

        # --- 輔助虛線（幫助理解「x 取平均」的視覺） ---
        # 從 A 和 B 分別往下/往左畫虛線到 x 軸和 y 軸
        h_dash_A = DashedLine(
            plane.c2p(-5, -2), plane.c2p(-5, 0), color=BLUE, stroke_opacity=0.6
        )
        h_dash_B = DashedLine(
            plane.c2p(-1, 3), plane.c2p(-1, 0), color=BLUE, stroke_opacity=0.6
        )
        v_dash_A = DashedLine(
            plane.c2p(-5, 0), plane.c2p(0, 0), color=BLUE, stroke_opacity=0.3
        )
        h_dash_M = DashedLine(
            plane.c2p(-3, 0.5), plane.c2p(-3, 0), color=RED, stroke_opacity=0.7
        )

        self.play(
            Create(h_dash_A), Create(h_dash_B),
            run_time=0.8
        )
        self.wait(0.2)

        # --- x 軸上標示 x₁, x₂, 和 xm ---
        tick_x1 = MathTex(r"x_1{=}{-5}", font_size=22, color=BLUE).next_to(
            plane.c2p(-5, 0), DOWN, buff=0.15
        )
        tick_x2 = MathTex(r"x_2{=}{-1}", font_size=22, color=BLUE).next_to(
            plane.c2p(-1, 0), DOWN, buff=0.15
        )
        self.play(Write(tick_x1), Write(tick_x2))
        self.wait(0.3)

        self.play(Create(h_dash_M))
        tick_xm = MathTex(r"x_M{=}{-3}", font_size=22, color=RED).next_to(
            plane.c2p(-3, 0), DOWN, buff=0.15
        )
        self.play(Write(tick_xm))
        self.wait(0.3)

        # --- 更新 M 標籤（顯示計算後座標） ---
        label_M_final = MathTex(r"M(-3,\ 0.5)", font_size=26, color=RED).next_to(
            dot_M, RIGHT, buff=0.15
        )
        self.play(ReplacementTransform(label_M, label_M_final))
        self.wait(0.3)

        # --- 分隔虛線 ---
        divider = DashedLine(
            start=[0, 3.8, 0], end=[0, -3.8, 0],
            color=GREY, stroke_opacity=0.5
        )
        self.play(Create(divider))

        # --- 右半邊：公式推導 ---
        col_x = 3.5

        title = Text("中點公式", font_size=26, color=GREY_A).move_to([col_x, 3.2, 0])
        self.play(Write(title))

        # Step 1：文字敘述「x 坐標取平均」
        desc = MathTex(
            r"x_M = \frac{x_1 + x_2}{2},\quad y_M = \frac{y_1 + y_2}{2}",
            font_size=30, color=YELLOW
        ).move_to([col_x, 2.1, 0])
        box = SurroundingRectangle(desc, color=YELLOW, buff=0.2)

        self.play(Write(desc))
        self.play(Create(box))
        self.wait(0.6)

        # Step 2：代入本例
        calc_x = MathTex(
            r"x_M = \frac{-5 + (-1)}{2} = \frac{-6}{2} = -3",
            font_size=28, color=BLUE_B
        ).move_to([col_x, 0.9, 0])

        calc_y = MathTex(
            r"y_M = \frac{-2 + 3}{2} = \frac{1}{2} = 0.5",
            font_size=28, color=GREEN_B
        ).move_to([col_x, 0.0, 0])

        result = MathTex(
            r"\therefore\ M = (-3,\ 0.5)",
            font_size=30, color=RED
        ).move_to([col_x, -1.0, 0])
        result_box = SurroundingRectangle(result, color=RED, buff=0.18)

        self.play(Write(calc_x))
        self.wait(0.5)
        self.play(Write(calc_y))
        self.wait(0.5)
        self.play(Write(result))
        self.play(Create(result_box))
        self.wait(2)
