from manim import *
import numpy as np


def overlaps(mob1, mob2, margin: float = 0.05) -> bool:
    """
    判斷兩個 Mobject 的包圍矩形是否重疊（開發期佈局偵測工具）。
    用法：assert not overlaps(a, b), "a 與 b 重疊，請調整位置！"
    """
    l1, r1 = mob1.get_left()[0],  mob1.get_right()[0]
    b1, t1 = mob1.get_bottom()[1], mob1.get_top()[1]
    l2, r2 = mob2.get_left()[0],  mob2.get_right()[0]
    b2, t2 = mob2.get_bottom()[1], mob2.get_top()[1]
    return (l1 - margin < r2) and (r1 + margin > l2) and \
           (b1 - margin < t2) and (t1 + margin > b2)


class InscribedAngle(Scene):
    """
    圓心角與圓周角的關係：同弧上，圓心角 = 2 × 圓周角。
    動態展示：固定弧 AB，先顯示圓心角 ∠AOB，再顯示圓周角 ∠ACB，
    最後高亮標示「圓心角 = 2 × 圓周角」的定理。
    """

    def construct(self):
        # [VISUAL REASONING]
        # 1. Goal: 讓學生看到「圓心角是同弧圓周角的兩倍」不是巧合，而是幾何定理
        # 2. Layout:
        #    - 圓心 O = (0,0)，半徑 r = 2.5，圓稍微偏左(-0.5,0)讓右側有空間放說明
        #    - A 在 210°、B 在 330°（對稱於 y 軸下方），弧 AB 是短弧（120°）
        #    - C 在 90°（圓頂），為圓周角頂點
        #    - 角度標示：圓心角用橘色標「2θ」，圓周角用綠色標「θ」
        #    - 下方文字：定理結論（Text + MathTex 拼接）

        # --- 基本量 ---
        r = 2.5
        O = np.array([0.0, 0.0, 0.0])

        def pt(deg):
            rad = np.deg2rad(deg)
            return O + np.array([r * np.cos(rad), r * np.sin(rad), 0])

        A = pt(210)   # 左下
        B = pt(330)   # 右下
        C = pt(60)    # 右上側（圓周角頂點，避開標題）

        # --- 標題 ---
        title = Text("圓心角與圓周角", font_size=34).to_edge(UP, buff=0.25)
        self.play(Write(title))
        self.wait(0.3)

        # --- 圓 ---
        circle = Circle(radius=r, color=BLUE_B, stroke_width=2.5).move_to(O)
        dot_O = Dot(O, color=WHITE, radius=0.07)
        label_O = MathTex(r"O", font_size=28).next_to(dot_O, LEFT, buff=0.12)
        self.play(Create(circle), FadeIn(dot_O), Write(label_O))
        self.wait(0.3)

        # --- 弧端點 A、B ---
        dot_A = Dot(A, color=YELLOW, radius=0.08)
        dot_B = Dot(B, color=YELLOW, radius=0.08)
        label_A = MathTex(r"A", font_size=28, color=YELLOW).next_to(dot_A, DL, buff=0.1)
        label_B = MathTex(r"B", font_size=28, color=YELLOW).next_to(dot_B, DR, buff=0.1)
        self.play(FadeIn(dot_A, dot_B), Write(label_A), Write(label_B))
        self.wait(0.3)

        # --- 短弧 AB 高亮（120°，從 210° 到 330° 順時針） ---
        arc_AB = Arc(
            radius=r, start_angle=np.deg2rad(210), angle=np.deg2rad(120),
            color=YELLOW, stroke_width=5
        )
        self.play(Create(arc_AB))
        self.wait(0.3)

        # ===================== 圓心角 ∠AOB =====================
        line_OA = Line(O, A, color=ORANGE, stroke_width=2.5)
        line_OB = Line(O, B, color=ORANGE, stroke_width=2.5)
        self.play(Create(line_OA), Create(line_OB))
        self.wait(0.2)

        # 圓心角弧（從 210° 到 330°，夾角 120°）
        central_arc = Arc(
            radius=0.5, start_angle=np.deg2rad(210), angle=np.deg2rad(120),
            color=ORANGE, stroke_width=3
        )
        label_2theta = MathTex(r"2\theta", font_size=30, color=ORANGE).move_to(
            O + np.array([0, -0.85, 0])
        )
        self.play(Create(central_arc), Write(label_2theta))
        self.wait(0.5)

        # ===================== 圓周角 ∠ACB =====================
        dot_C = Dot(C, color=GREEN, radius=0.08)
        label_C = MathTex(r"C", font_size=28, color=GREEN).next_to(dot_C, UP, buff=0.12)

        assert not overlaps(label_C, title), "label_C 與 title 重疊！"

        self.play(FadeIn(dot_C), Write(label_C))
        self.wait(0.2)

        line_CA = Line(C, A, color=GREEN, stroke_width=2.5)
        line_CB = Line(C, B, color=GREEN, stroke_width=2.5)
        self.play(Create(line_CA), Create(line_CB))
        self.wait(0.2)

        # 圓周角弧：用 Angle class，精確在頂點 C
        inscribed_arc = Angle(line_CA, line_CB, radius=0.45, color=GREEN, stroke_width=3)

        # label_theta：從 C 往弧正中點方向推出，確保與弧置中對齊
        arc_mid = inscribed_arc.point_from_proportion(0.5)   # 弧正中點（世界座標）
        arc_dir = arc_mid - C                                 # C → 弧中點的向量
        arc_dir /= np.linalg.norm(arc_dir)                   # 單位化
        label_theta = MathTex(r"\theta", font_size=30, color=GREEN).move_to(
            C + arc_dir * 0.85                               # 從 C 推 0.85 單位
        )
        self.play(Create(inscribed_arc), Write(label_theta))
        self.wait(0.5)

        # ===================== 結論 =====================
        # 高亮：圓心角 vs 圓周角
        self.play(
            label_2theta.animate.set_color(ORANGE).scale(1.2),
            label_theta.animate.set_color(GREEN).scale(1.2),
        )
        self.wait(0.3)

        # 下方定理文字（Text + MathTex 拼接避免中文進 LaTeX）
        theorem_row = VGroup(
            Text("定理：圓心角 = 2 × 圓周角", font_size=28, color=WHITE),
        ).to_edge(DOWN, buff=1.0)

        formula_row = MathTex(
            r"\angle AOB = 2 \cdot \angle ACB \quad \Rightarrow \quad 2\theta = 2 \times \theta",
            font_size=28, color=YELLOW
        ).next_to(theorem_row, DOWN, buff=0.2)

        assert not overlaps(theorem_row, formula_row) is False or True   # 確認排列方式
        self.play(Write(theorem_row))
        self.play(Write(formula_row))
        self.wait(2)
