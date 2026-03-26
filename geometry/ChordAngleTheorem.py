from manim import *
import numpy as np


def overlaps(mob1, mob2, margin: float = 0.05) -> bool:
    """
    判斷兩個 Mobject 包圍矩形是否重疊（開發期佈局偵測）。
    用法：assert not overlaps(a, b)
    """
    l1, r1 = mob1.get_left()[0],  mob1.get_right()[0]
    b1, t1 = mob1.get_bottom()[1], mob1.get_top()[1]
    l2, r2 = mob2.get_left()[0],  mob2.get_right()[0]
    b2, t2 = mob2.get_bottom()[1], mob2.get_top()[1]
    return (l1 - margin < r2) and (r1 + margin > l2) and \
           (b1 - margin < t2) and (t1 + margin > b2)


class ChordAngleTheorem(Scene):
    """
    弦切角定理：展示弦切角 (弦與過端點切線的夾角) 等於同弦所對應的圓周角。
    """

    def construct(self):
        # [VISUAL REASONING]
        # 1. Goal: 直觀展示過 A 點的切線與弦 AB 的夾角（弦切角）= 圓周角 ∠ACB。
        # 2. Layout:
        #    - A 固定在圓的底部 (-90°)，讓切線保持水平，便於觀察。
        #    - B 和 C 使用 ValueTracker 動態控制角度。
        #    - 右側或上方放置標題與方程式：弦切角 = 圓周角。

        # 基本參數設定
        R = 2.2
        origin = np.array([-1.8, -0.6, 0])
        
        # 動態變數：B 點角度與 C 點角度
        # A 點設定在 -90 度 (-PI/2)
        angle_A = -PI / 2
        tracker_B = ValueTracker(PI / 6)  # 初始 B 點在 30 度
        tracker_C = ValueTracker(5 * PI / 6)  # 初始 C 點在 150 度

        title = Text("弦切角定理", font_size=36, color=YELLOW).to_edge(UP, buff=0.3)
        subtitle = Text("弦切角 = 所對應的圓周角", font_size=28, color=WHITE).next_to(title, DOWN, buff=0.2)
        self.play(Write(title), Write(subtitle))

        # --- 第一階段：畫圓、A 點、切線 ---
        circle = Circle(radius=R, color=BLUE_B, stroke_width=2.5).move_to(origin)
        dot_O = Dot(origin, color=WHITE, radius=0.06)
        label_O = MathTex("O", font_size=26).next_to(dot_O, DOWN, buff=0.1)
        
        # A 點固定在正下方
        pos_A = origin + np.array([R * np.cos(angle_A), R * np.sin(angle_A), 0])
        dot_A = Dot(pos_A, color=RED, radius=0.08)
        label_A = MathTex("A", font_size=28, color=RED).next_to(dot_A, DOWN, buff=0.15)
        
        # 切線 L (過 A 的水平線)
        tan_left = pos_A + np.array([-R*1.5, 0, 0])
        tan_right = pos_A + np.array([R*1.5, 0, 0])
        tangent_line = Line(tan_left, tan_right, color=YELLOW, stroke_width=2)
        label_L = MathTex("L", font_size=28, color=YELLOW).next_to(tangent_line, LEFT, buff=0.15)

        self.play(
            Create(circle), FadeIn(dot_O), Write(label_O),
            FadeIn(dot_A), Write(label_A),
            Create(tangent_line), Write(label_L)
        )
        self.wait(0.5)

        # --- 第二階段：動態產生 B, C 以及相關線段與角度 ---
        def get_pos(theta):
            return origin + np.array([R * np.cos(theta), R * np.sin(theta), 0])

        dot_B = always_redraw(lambda: Dot(get_pos(tracker_B.get_value()), color=GREEN, radius=0.08))
        label_B = always_redraw(
            lambda: MathTex("B", font_size=28, color=GREEN)
            .move_to(get_pos(tracker_B.get_value()) + 0.35 * normalize(get_pos(tracker_B.get_value()) - origin))
        )
        chord_AB = always_redraw(lambda: Line(pos_A, get_pos(tracker_B.get_value()), color=GREEN))

        dot_C = always_redraw(lambda: Dot(get_pos(tracker_C.get_value()), color=ORANGE, radius=0.08))
        label_C = always_redraw(
            lambda: MathTex("C", font_size=28, color=ORANGE)
            .move_to(get_pos(tracker_C.get_value()) + 0.35 * normalize(get_pos(tracker_C.get_value()) - origin))
        )
        line_CA = always_redraw(lambda: Line(get_pos(tracker_C.get_value()), pos_A, color=ORANGE))
        line_CB = always_redraw(lambda: Line(get_pos(tracker_C.get_value()), get_pos(tracker_B.get_value()), color=ORANGE))

        self.play(FadeIn(dot_B), Write(label_B), Create(chord_AB))
        self.play(FadeIn(dot_C), Write(label_C), Create(line_CA), Create(line_CB))
        self.wait(0.5)

        # 弦切角的表示法
        # 由於 L 水平通過 A，右邊的部分從 A 到 tan_right，我們可以構造一條不可見的線來產生角度
        # 為了使用 Manim 的 Angle，我們用 Line(pos_A, tan_right)
        line_tan_right = Line(pos_A, tan_right)
        
        def get_chord_angle():
            # Angle 介於 tangent (水平向右) 與 弦 AB
            l_ab = Line(pos_A, get_pos(tracker_B.get_value()))
            arc = Angle(line_tan_right, l_ab, radius=0.6, color=YELLOW)
            # Label
            mp = arc.point_from_proportion(0.5)
            direction = normalize(mp - pos_A)
            lbl = MathTex(r"\theta", font_size=24, color=YELLOW).move_to(mp + direction * 0.25)
            return VGroup(arc, lbl)
            
        chord_angle_group = always_redraw(get_chord_angle)

        def get_inscribed_angle():
            # Angle 介於 CA 和 CB 之間 (交點為 C)
            pos_c = get_pos(tracker_C.get_value())
            # Line 要從頂點出發才能正確顯示 Angle
            l_ca = Line(pos_c, pos_A)
            l_cb = Line(pos_c, get_pos(tracker_B.get_value()))
            # 確保 Angle 畫在內部（通常直接傳兩邊即可，如果方向反了會畫劣角）
            # 因為 C 在優弧，角度應為 銳角/鈍角
            ang = Angle(l_ca, l_cb, radius=0.6, color=ORANGE)
            # Label
            mp = ang.point_from_proportion(0.5)
            direction = normalize(mp - pos_c)
            lbl = MathTex(r"\theta", font_size=24, color=ORANGE).move_to(mp + direction * 0.25)
            return VGroup(ang, lbl)

        inscribed_angle_group = always_redraw(get_inscribed_angle)

        self.play(FadeIn(chord_angle_group))
        self.wait(0.5)
        self.play(FadeIn(inscribed_angle_group))
        self.wait(1)

        # 動態公式板 (位於右側)
        panel = VGroup(
            Text("弦切角 = ", font_size=26, color=YELLOW),
            VGroup(
                MathTex(r"\angle(", font_size=26, color=YELLOW),
                Text("切線", font_size=22, color=YELLOW),
                MathTex(", AB)", font_size=26, color=YELLOW)
            ).arrange(RIGHT, buff=0.1)
        ).arrange(RIGHT).to_edge(RIGHT, buff=0.8).shift(UP*1)
        
        panel2 = VGroup(
            Text("圓周角 = ", font_size=26, color=ORANGE),
            MathTex(r"\angle ACB", font_size=26, color=ORANGE),
        ).arrange(RIGHT).next_to(panel, DOWN, aligned_edge=LEFT, buff=0.5)

        # 開發期檢查：這兩個 panel 不會跟圓或標題重疊
        assert not overlaps(panel, circle), "公式與圓形重疊！"
        assert not overlaps(panel, title), "公式與標題重疊！"

        self.play(FadeIn(panel))
        self.play(FadeIn(panel2))
        self.wait(1)
        
        conclusion = Text("兩者恆相等", font_size=28, color=RED).next_to(panel2, DOWN, buff=0.6)
        VGroup(panel, panel2, conclusion).arrange(DOWN, aligned_edge=LEFT, buff=0.4).to_edge(RIGHT, buff=0.8).shift(UP*0.5)
        self.play(Write(conclusion))

        # --- 第三階段：動畫！展示 B 點移動，theta 角一起變化 ---
        # B 從 PI/6 (30度) 移到 PI/2 (90度)
        self.play(tracker_B.animate.set_value(PI / 2), run_time=2.5)
        self.wait(0.5)
        # B 移到 -PI/6 (-30度)
        self.play(tracker_B.animate.set_value(-PI / 6), run_time=2.5)
        self.wait(0.5)
        # B 移回 PI/6
        self.play(tracker_B.animate.set_value(PI / 6), run_time=1.5)
        self.wait(1)

        # --- 第四階段：展示 C 點移動，圓周角位置變換但 theta 不變 ---
        # C 必須保持在優弧 AB 上（這裡確保它在 > PI/6 且 < 3*PI/2，因為 A 是 -PI/2）
        # 移動 C 到 PI (180度)
        self.play(tracker_C.animate.set_value(PI), run_time=2.5)
        self.wait(0.5)
        # 移動 C 到 PI/3 (60度)
        self.play(tracker_C.animate.set_value(PI / 3), run_time=2.5)
        self.wait(2)
