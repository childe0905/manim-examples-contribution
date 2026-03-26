from manim import *
import numpy as np


class DistanceFormula(Scene):
    """
    透過座標平面上兩點，建立直角三角形（3-4-5 勾股數），
    並用畢氏定理推導出距離公式：d = √((x₂-x₁)² + (y₂-y₁)²)
    """

    def construct(self):
        # [VISUAL REASONING]
        # 1. Goal: 讓學生看到距離公式是畢氏定理的直接應用，結果為整數更直觀
        # 2. Layout（防重疊設計）：
        #    - NumberPlane 全螢幕置中，x 從 -7 到 7
        #    - 【左半邊 x < -0.5】三角形：A(-5,-1.5), B(-2,2.5), C(-2,-1.5)
        #      所有點標籤和 Brace 都在 x < -0.5 內，不越界
        #    - 【右半邊 x > 1.0】公式推導：col_x=4.0，用 scale 控制寬度
        #    - 加虛線分隔線於 x=0 視覺隔離

        # --- 座標系（全螢幕，不平移） ---
        plane = NumberPlane(
            x_range=[-7, 7, 1],
            y_range=[-4, 4, 1],
            background_line_style={"stroke_opacity": 0.4},
        )
        self.play(Create(plane), run_time=1.5)

        # --- 兩點（左半邊，3-4-5 直角三角形） ---
        # A(-5,-1.5), B(-2, 2.5) → Δx=3, Δy=4, d=5
        A = plane.c2p(-5, -1.5)
        B = plane.c2p(-2,  2.5)
        C = plane.c2p(-2, -1.5)   # 直角在 C（B 的 x、A 的 y）

        dot_A = Dot(A, color=YELLOW)
        dot_B = Dot(B, color=YELLOW)
        # 標籤方向：A 往左下、B 往左上，確保不超過 x=-1.5
        label_A = MathTex(r"A(-5,\ -1.5)", font_size=26).next_to(dot_A, DL, buff=0.12)
        label_B = MathTex(r"B(-2,\ 2.5)", font_size=26).next_to(dot_B, UL, buff=0.12)

        self.play(FadeIn(dot_A, dot_B), Write(label_A), Write(label_B))
        self.wait(0.4)

        # --- 斜邊 ---
        hyp = Line(A, B, color=WHITE, stroke_width=3)
        label_d = MathTex(r"d\ =\ ?", font_size=28, color=WHITE).next_to(
            hyp.get_center(), LEFT, buff=0.25
        )
        self.play(Create(hyp), Write(label_d))
        self.wait(0.4)

        # --- 水平邊（Δx=3）與垂直邊（Δy=4） ---
        h_line = Line(A, C, color=BLUE, stroke_width=3)
        v_line = Line(C, B, color=GREEN, stroke_width=3)
        right_angle = RightAngle(h_line, v_line, length=0.25, color=WHITE)

        self.play(Create(h_line), Create(v_line), Create(right_angle))
        self.wait(0.3)

        # --- Brace 標示（Δy 放左側，Δx 放下側，皆不越過 x=-1） ---
        brace_x = Brace(h_line, DOWN, color=BLUE, buff=0.1)
        brace_x_lbl = MathTex(r"\Delta x = 3", font_size=28, color=BLUE)
        brace_x.put_at_tip(brace_x_lbl)

        brace_y = Brace(v_line, RIGHT, color=GREEN, buff=0.1)  # 右側空白區，不碰斜邊
        brace_y_lbl = MathTex(r"\Delta y = 4", font_size=28, color=GREEN)
        brace_y.put_at_tip(brace_y_lbl)

        self.play(FadeIn(brace_x), Write(brace_x_lbl))
        self.wait(0.2)
        self.play(FadeIn(brace_y), Write(brace_y_lbl))
        self.wait(0.5)

        # --- 分隔虛線（x=0） ---
        divider = DashedLine(
            start=[0, 3.8, 0], end=[0, -3.8, 0],
            color=GREY, stroke_opacity=0.5
        )
        self.play(Create(divider))

        # --- 右半邊公式推導區 ---
        # col_x=3.5，font_size 控小避免超出右緣
        col_x = 3.5

        section_title = Text("距離公式推導", font_size=24, color=GREY_A).move_to([col_x, 3.2, 0])
        self.play(Write(section_title))

        # Step 1：畢氏定理
        step1 = MathTex(
            r"d^2 = (\Delta x)^2 + (\Delta y)^2",
            font_size=30
        ).move_to([col_x, 2.1, 0])

        # Step 2：開根號
        step2 = MathTex(
            r"d = \sqrt{(\Delta x)^2 + (\Delta y)^2}",
            font_size=30
        ).move_to([col_x, 2.1, 0])

        # Step 3：一般式（拆成兩行顯示避免溢出）
        step3 = MathTex(
            r"d = \sqrt{(x_2-x_1)^2+(y_2-y_1)^2}",
            font_size=28, color=YELLOW
        ).move_to([col_x, 2.1, 0])
        box = SurroundingRectangle(step3, color=YELLOW, buff=0.18)

        # Step 4：代入本例
        verify = MathTex(
            r"= \sqrt{3^2+4^2} = \sqrt{25} = 5",
            font_size=30, color=GREEN_B
        ).move_to([col_x, 0.7, 0])
        verify_box = SurroundingRectangle(verify, color=GREEN_B, buff=0.15)

        self.play(Write(step1))
        self.wait(0.7)
        self.play(TransformMatchingTex(step1, step2))
        self.wait(0.7)
        self.play(TransformMatchingTex(step2, step3))
        self.play(Create(box))
        self.wait(0.5)

        self.play(Write(verify))
        self.play(Create(verify_box))
        self.wait(2)
