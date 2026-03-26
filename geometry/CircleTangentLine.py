from manim import *
import numpy as np


def overlaps(mob1, mob2, margin: float = 0.05) -> bool:
    """
    判斷兩個 Mobject 的包圍矩形是否重疊（開發時用來偵測佈局衝突）。
    margin：允許的最小間距（預設 0.05 個 Manim 單位）。

    用法範例：
        assert not overlaps(label_T1, prop1_indicator), \
            "label_T1 與 prop1_indicator 重疊，請調整位置！"
    """
    l1, r1 = mob1.get_left()[0],  mob1.get_right()[0]
    b1, t1 = mob1.get_bottom()[1], mob1.get_top()[1]
    l2, r2 = mob2.get_left()[0],  mob2.get_right()[0]
    b2, t2 = mob2.get_bottom()[1], mob2.get_top()[1]
    x_overlap = (l1 - margin < r2) and (r1 + margin > l2)
    y_overlap = (b1 - margin < t2) and (t1 + margin > b2)
    return x_overlap and y_overlap


class CircleTangentLine(Scene):
    """
    圓的切線性質示範：過圓外一點作兩條切線，
    動態展示「切線 ⊥ 半徑」，並指出兩切線等長。
    """

    def construct(self):
        # [VISUAL REASONING]
        # 1. Goal: 讓學生直觀理解切線的兩大性質：切線⊥半徑、過外點兩切線等長
        # 2. Layout:
        #    - 圓心 O = (-1.5, 0)，半徑 r = 2，藍色
        #    - 外部點 P = (4.5, 0)，在右側，距圓心 d=6
        #    - 切點 T1（上）和 T2（下）由公式精確算出
        #    - label_T1 → UL 方向（圓外左上），prop1_indicator → UR 方向（圓外右上）
        #      兩者方向相反，不重疊
        #    - 性質說明放在畫面下方
        #    - overlaps() 在 play 前驗證所有標籤不碰撞

        # --- 幾何量 ---
        O = np.array([-1.5, 0, 0])
        P = np.array([4.5, 0, 0])
        r = 2.0
        d = np.linalg.norm(P - O)   # = 6

        tx = r**2 / d                               # ≈ 0.667
        ty = r * np.sqrt(d**2 - r**2) / d           # ≈ 1.886
        T1 = O + np.array([tx, ty, 0])
        T2 = O + np.array([tx, -ty, 0])

        # --- 標題 ---
        title = Text("圓的切線性質", font_size=34, color=WHITE).to_edge(UP, buff=0.3)
        self.play(Write(title))
        self.wait(0.3)

        # --- 圓與圓心 ---
        circle = Circle(radius=r, color=BLUE, stroke_width=3).move_to(O)
        dot_O = Dot(O, color=WHITE, radius=0.07)
        label_O = MathTex(r"O", font_size=28).next_to(dot_O, DL, buff=0.1)
        self.play(Create(circle), FadeIn(dot_O), Write(label_O))
        self.wait(0.3)

        # --- 外部點 P ---
        dot_P = Dot(P, color=YELLOW, radius=0.09)
        label_P = MathTex(r"P", font_size=28, color=YELLOW).next_to(dot_P, UR, buff=0.1)
        self.play(FadeIn(dot_P), Write(label_P))
        self.wait(0.3)

        # --- 輔助線：OP 連線（虛線） ---
        line_OP = DashedLine(O, P, color=GREY, stroke_opacity=0.6)
        self.play(Create(line_OP))
        self.wait(0.2)

        # ===================== 第一條切線（上） =====================
        dot_T1 = Dot(T1, color=GREEN, radius=0.08)
        # label_T1 放 UL（圓外左上）
        label_T1 = MathTex(r"T_1", font_size=26, color=GREEN).next_to(dot_T1, UL, buff=0.12)

        radius_1 = Line(O, T1, color=ORANGE, stroke_width=2.5)
        tangent_1 = Line(P, T1, color=GREEN, stroke_width=3)
        label_r1 = MathTex(r"r", font_size=24, color=ORANGE).next_to(
            radius_1.get_center(), UL, buff=0.08
        )

        self.play(Create(radius_1), Write(label_r1))
        self.play(Create(tangent_1), FadeIn(dot_T1), Write(label_T1))
        self.wait(0.2)

        # 直角符號
        r1_from_T1 = Line(T1, O)
        t1_from_T1 = Line(T1, P)
        ra1 = RightAngle(r1_from_T1, t1_from_T1, length=0.22, color=YELLOW)
        self.play(Create(ra1))

        # prop1_indicator 放 UR 方向（與 label_T1 的 UL 相反，不重疊）
        prop1_indicator = MathTex(
            r"OT_1 \perp PT_1", font_size=26, color=YELLOW
        ).next_to(dot_T1, UR, buff=0.15)

        # ── overlap 偵測（開發期 assert） ──
        assert not overlaps(label_T1, prop1_indicator), \
            "label_T1 與 prop1_indicator 重疊！請調整方向或 buff。"
        assert not overlaps(prop1_indicator, title), \
            "prop1_indicator 與 title 重疊！請調整位置。"

        self.play(Write(prop1_indicator))
        self.wait(0.5)
        self.play(FadeOut(prop1_indicator))

        # ===================== 第二條切線（下） =====================
        dot_T2 = Dot(T2, color=RED, radius=0.08)
        label_T2 = MathTex(r"T_2", font_size=26, color=RED).next_to(dot_T2, DL, buff=0.1)

        radius_2 = Line(O, T2, color=ORANGE, stroke_width=2.5)
        tangent_2 = Line(P, T2, color=RED, stroke_width=3)

        self.play(Create(radius_2))
        self.play(Create(tangent_2), FadeIn(dot_T2), Write(label_T2))
        self.wait(0.2)

        r2_from_T2 = Line(T2, O)
        t2_from_T2 = Line(T2, P)
        ra2 = RightAngle(r2_from_T2, t2_from_T2, length=0.22, color=YELLOW)
        self.play(Create(ra2))
        self.wait(0.4)

        # ===================== 性質說明（下方） =====================
        prop1_row = VGroup(
            Text("性質 1：", font_size=26, color=YELLOW),
            MathTex(r"OT_1 \perp PT_1,\quad OT_2 \perp PT_2", font_size=26, color=YELLOW),
        ).arrange(RIGHT, buff=0.1)

        prop2_row = VGroup(
            Text("性質 2：", font_size=26, color=GREEN_B),
            MathTex(r"|PT_1| = |PT_2| = \sqrt{|OP|^2 - r^2}", font_size=26, color=GREEN_B),
        ).arrange(RIGHT, buff=0.1)

        prop_box = VGroup(prop1_row, prop2_row).arrange(DOWN, aligned_edge=LEFT, buff=0.25)
        prop_box.to_edge(DOWN, buff=0.45)

        self.play(Write(prop1_row))
        self.wait(0.5)

        self.play(
            tangent_1.animate.set_stroke(color=GREEN_B, width=5),
            tangent_2.animate.set_stroke(color=GREEN_B, width=5),
        )
        self.play(Write(prop2_row))
        self.wait(2)
