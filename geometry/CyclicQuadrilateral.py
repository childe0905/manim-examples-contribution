from manim import *
import numpy as np


class CyclicQuadrilateral(Scene):
    """
    圓內接四邊形對角互補 (對角和為 180 度)。
    動態展示任意圓內接四邊形中，兩組對角各自相加皆為 180°。
    """

    def construct(self):
        # [VISUAL REASONING]
        # 1. Goal: 讓學生直觀看到圓內接四邊形對角互補定理在「任意形狀」下都成立
        # 2. Layout: 圓與四邊形置左，公式面板置右（RIGHT * 3.5）；分兩階段展示 AC 對角與 BD 對角
        # 3. ValueTracker 驅動四頂點位置，DecimalNumber updater 即時更新角度數值
        R = 2.4
        # 圓心微微偏左，留給右邊足夠空間
        origin = np.array([-2.5, -0.2, 0])

        # 頂點：逆時針 A -> B -> C -> D
        tracker_A = ValueTracker(PI * 0.8)   # 左上
        tracker_B = ValueTracker(PI * 1.3)   # 左下
        tracker_C = ValueTracker(PI * 1.8)   # 右下
        tracker_D = ValueTracker(PI * 0.3)   # 右上

        def get_pos(theta):
            return origin + np.array([R * np.cos(theta), R * np.sin(theta), 0])

        title = Text("圓內接四邊形對角互補", font_size=36, color=YELLOW).to_edge(UP, buff=0.3)
        self.play(Write(title))

        # --- 1. 畫圓與頂點 ---
        circle = Circle(radius=R, color=BLUE_B, stroke_width=2.5).move_to(origin)
        dot_O = Dot(origin, color=WHITE, radius=0.06)
        
        self.play(Create(circle), FadeIn(dot_O))

        dot_A = always_redraw(lambda: Dot(get_pos(tracker_A.get_value()), color=RED))
        dot_B = always_redraw(lambda: Dot(get_pos(tracker_B.get_value()), color=BLUE_C))
        dot_C = always_redraw(lambda: Dot(get_pos(tracker_C.get_value()), color=GREEN))
        dot_D = always_redraw(lambda: Dot(get_pos(tracker_D.get_value()), color=ORANGE))

        label_A = always_redraw(lambda: MathTex("A", font_size=28, color=RED)
                                .move_to(get_pos(tracker_A.get_value()) + 0.3 * normalize(get_pos(tracker_A.get_value()) - origin)))
        label_B = always_redraw(lambda: MathTex("B", font_size=28, color=BLUE_C)
                                .move_to(get_pos(tracker_B.get_value()) + 0.3 * normalize(get_pos(tracker_B.get_value()) - origin)))
        label_C = always_redraw(lambda: MathTex("C", font_size=28, color=GREEN)
                                .move_to(get_pos(tracker_C.get_value()) + 0.3 * normalize(get_pos(tracker_C.get_value()) - origin)))
        label_D = always_redraw(lambda: MathTex("D", font_size=28, color=ORANGE)
                                .move_to(get_pos(tracker_D.get_value()) + 0.3 * normalize(get_pos(tracker_D.get_value()) - origin)))
        
        # --- 2. 畫出四邊形 ---
        quad = always_redraw(lambda: Polygon(
            get_pos(tracker_A.get_value()),
            get_pos(tracker_B.get_value()),
            get_pos(tracker_C.get_value()),
            get_pos(tracker_D.get_value()),
            color=YELLOW, stroke_width=2.5, fill_color=YELLOW, fill_opacity=0.1
        ))

        self.play(
            FadeIn(dot_A, dot_B, dot_C, dot_D),
            Write(VGroup(label_A, label_B, label_C, label_D)),
            Create(quad)
        )
        self.wait(0.5)

        # --- 3. 角度動態計算與標示 ---
        def get_internal_angle(t_curr, t_prev, t_next):
            pc = get_pos(t_curr.get_value())
            pp = get_pos(t_prev.get_value())
            pn = get_pos(t_next.get_value())
            v1 = pp - pc
            v2 = pn - pc
            ang1 = np.arctan2(v1[1], v1[0])
            ang2 = np.arctan2(v2[1], v2[0])
            diff = (ang2 - ang1) % TAU
            if diff > PI:
                diff = TAU - diff
            return diff

        def get_angle_A_val(): return get_internal_angle(tracker_A, tracker_B, tracker_D)
        def get_angle_B_val(): return get_internal_angle(tracker_B, tracker_C, tracker_A)
        def get_angle_C_val(): return get_internal_angle(tracker_C, tracker_D, tracker_B)
        def get_angle_D_val(): return get_internal_angle(tracker_D, tracker_A, tracker_C)

        def get_safe_angle_arc(t_curr, t_prev, t_next, radius, color):
            pc = get_pos(t_curr.get_value())
            pp = get_pos(t_prev.get_value())
            pn = get_pos(t_next.get_value())
            vp = pp - pc
            vn = pn - pc
            ang_p = np.arctan2(vp[1], vp[0])
            ang_n = np.arctan2(vn[1], vn[0])
            diff = (ang_n - ang_p) % TAU
            if diff < PI:
                start = ang_p
                angle = diff
            else:
                start = ang_n
                angle = TAU - diff
            return Arc(radius=radius, start_angle=start, angle=angle, arc_center=pc, color=color, stroke_width=3)

        # -------------------------------------------------------------------
        # 第一階段：專注於 A 和 C 這組對角
        # -------------------------------------------------------------------
        angle_arc_A = get_safe_angle_arc(tracker_A, tracker_B, tracker_D, 0.45, RED)
        angle_arc_C = get_safe_angle_arc(tracker_C, tracker_D, tracker_B, 0.45, GREEN)

        self.play(FadeIn(angle_arc_A), FadeIn(angle_arc_C))

        panel_layout_AC = VGroup(
            MathTex(r"\angle A = ", font_size=36, color=RED),
            DecimalNumber(0, num_decimal_places=1, unit=r"^{\circ}", font_size=36, color=RED),
            MathTex(r"\angle C = ", font_size=36, color=GREEN),
            DecimalNumber(0, num_decimal_places=1, unit=r"^{\circ}", font_size=36, color=GREEN),
        ).arrange_in_grid(rows=2, cols=2, col_alignments="rl", col_buff=0.3)

        sum_panel_ac = VGroup(
            MathTex(r"\angle A + \angle C =", font_size=40),
            MathTex(r"180^{\circ}", font_size=40, color=YELLOW)
        ).arrange(RIGHT)

        group_AC = VGroup(panel_layout_AC, sum_panel_ac).arrange(DOWN, buff=0.8)
        # 右半邊空白中心約在 RIGHT * 3.5
        group_AC.move_to(RIGHT * 3.5 + DOWN * 0.2)

        self.play(FadeIn(panel_layout_AC))
        self.play(Write(sum_panel_ac))
        self.play(Create(SurroundingRectangle(sum_panel_ac, color=YELLOW, buff=0.15)))
        self.wait(0.5)

        dec_A = panel_layout_AC[1]
        dec_C = panel_layout_AC[3]
        dec_A.add_updater(lambda d: d.set_value(np.degrees(get_angle_A_val())))
        dec_C.add_updater(lambda d: d.set_value(np.degrees(get_angle_C_val())))
        
        angle_arc_A.add_updater(lambda mob: mob.become(get_safe_angle_arc(tracker_A, tracker_B, tracker_D, 0.45, RED)))
        angle_arc_C.add_updater(lambda mob: mob.become(get_safe_angle_arc(tracker_C, tracker_D, tracker_B, 0.45, GREEN)))

        # 動畫：橫向拉扯，讓 A 和 C 極大變化
        self.play(tracker_A.animate.set_value(PI * 0.95), tracker_D.animate.set_value(PI * 0.1), run_time=2.5)
        self.wait(1)

        # 解除綁定並淡出階段一的元素
        dec_A.clear_updaters()
        dec_C.clear_updaters()
        angle_arc_A.clear_updaters()
        angle_arc_C.clear_updaters()
        # 注意此處淡出 SurroundingRectangle 也要囊括 (但由於它沒被放入 group_AC，可以在 play 時手動捕捉所有畫面元素)
        # 用 FadeOut 將右側所有面板、A C 兩角度弧都隱藏
        ac_rect = self.mobjects[-1]  # The SurroundingRectangle was the last added
        self.play(
            FadeOut(group_AC), FadeOut(ac_rect),
            FadeOut(angle_arc_A), FadeOut(angle_arc_C)
        )
        self.wait(0.5)

        # -------------------------------------------------------------------
        # 第二階段：專注於 B 和 D 這組對角
        # -------------------------------------------------------------------
        # 這裡必須重新抓取最新的 tracker 狀態以產生乾淨的角度弧，防止從舊位置瞬間跳換
        angle_arc_B = get_safe_angle_arc(tracker_B, tracker_C, tracker_A, 0.45, BLUE_C)
        angle_arc_D = get_safe_angle_arc(tracker_D, tracker_A, tracker_C, 0.45, ORANGE)

        self.play(FadeIn(angle_arc_B), FadeIn(angle_arc_D))

        panel_layout_BD = VGroup(
            MathTex(r"\angle B = ", font_size=36, color=BLUE_C),
            DecimalNumber(0, num_decimal_places=1, unit=r"^{\circ}", font_size=36, color=BLUE_C),
            MathTex(r"\angle D = ", font_size=36, color=ORANGE),
            DecimalNumber(0, num_decimal_places=1, unit=r"^{\circ}", font_size=36, color=ORANGE),
        ).arrange_in_grid(rows=2, cols=2, col_alignments="rl", col_buff=0.3)

        sum_panel_bd = VGroup(
            MathTex(r"\angle B + \angle D =", font_size=40),
            MathTex(r"180^{\circ}", font_size=40, color=YELLOW)
        ).arrange(RIGHT)

        group_BD = VGroup(panel_layout_BD, sum_panel_bd).arrange(DOWN, buff=0.8)
        # 完全相同的右半邊置中位置
        group_BD.move_to(RIGHT * 3.5 + DOWN * 0.2)

        self.play(FadeIn(panel_layout_BD))
        self.play(Write(sum_panel_bd))
        self.play(Create(SurroundingRectangle(sum_panel_bd, color=YELLOW, buff=0.15)))
        self.wait(0.5)

        dec_B = panel_layout_BD[1]
        dec_D = panel_layout_BD[3]
        dec_B.add_updater(lambda d: d.set_value(np.degrees(get_angle_B_val())))
        dec_D.add_updater(lambda d: d.set_value(np.degrees(get_angle_D_val())))
        
        # 動態補上角度追蹤 updater
        angle_arc_B.add_updater(lambda mob: mob.become(get_safe_angle_arc(tracker_B, tracker_C, tracker_A, 0.45, BLUE_C)))
        angle_arc_D.add_updater(lambda mob: mob.become(get_safe_angle_arc(tracker_D, tracker_A, tracker_C, 0.45, ORANGE)))

        # 動畫：縱向拉扯與恢復，讓 B 和 D 極大變化
        self.play(tracker_B.animate.set_value(PI * 1.5), tracker_C.animate.set_value(PI * 1.7), run_time=2.5)
        self.wait(0.5)
        self.play(
            tracker_A.animate.set_value(PI * 0.6),
            tracker_B.animate.set_value(PI * 1.1),
            tracker_C.animate.set_value(PI * 1.8),
            tracker_D.animate.set_value(PI * 0.4),
            run_time=3
        )
        self.wait(2)
