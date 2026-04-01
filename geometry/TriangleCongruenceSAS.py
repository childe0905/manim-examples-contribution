from manim import *
import numpy as np

class TriangleCongruenceSAS(Scene):
    """
    展示兩個三角形 SAS (Side-Angle-Side) 全等判定的動畫，包含邊角強調與推導。
    """
    def construct(self):
        # [VISUAL REASONING]
        # 縮小三角形尺寸並提高整體重心，以避免文字與圖形重疊
        # 條件文字放置於下半段，並預留邊界避免被播放器擋住

        title = Text("SAS 三角形全等判定", font_size=40, t2c={"SAS": RED, "全等": GREEN}).to_edge(UP, buff=0.2)
        subtitle = Text("若兩組「對應邊」與其「夾角」相等，則兩三角形全等", font_size=28, color=YELLOW).next_to(title, DOWN, buff=0.15)
        self.play(Write(title), Write(subtitle))

        # 定義稍微小一點的頂點，避免旋轉時碰到下方文字
        vA = np.array([-0.5, 1.2, 0])
        vB = np.array([-2.0, -0.5, 0])
        vC = np.array([1.0, -0.5, 0])

        # 提高 y 軸基準 (UP * 0.8)
        tri_a = Polygon(vA, vB, vC, color=BLUE, fill_opacity=0.2).shift(LEFT * 2.5 + UP * 0.8)
        tri_b = tri_a.copy().set_color(GREEN).shift(RIGHT * 5.5).rotate(PI/4)

        va = tri_a.get_vertices()
        vb = tri_b.get_vertices()

        # 標籤，buff=0.1
        labels_a = VGroup(
            MathTex("A").next_to(va[0], UP, buff=0.1),
            MathTex("B").next_to(va[1], DL, buff=0.1),
            MathTex("C").next_to(va[2], DR, buff=0.1)
        )
        labels_b = VGroup(
            MathTex("D").next_to(vb[0], UR, buff=0.1),
            MathTex("E").next_to(vb[1], DL, buff=0.1),
            MathTex("F").next_to(vb[2], DR, buff=0.1)
        )
        self.play(Create(tri_a), Write(labels_a), Create(tri_b), Write(labels_b))

        cond1 = MathTex(r"\because \overline{AB} = \overline{DE}", color=RED)
        cond2 = MathTex(r"\quad \angle A = \angle D", color=YELLOW)
        cond3 = MathTex(r"\quad \overline{AC} = \overline{DF}", color=PURPLE)
        
        # 將條件公式釘在畫面 y = -1.5 的位置，確保不干涉上面圖形與下面空間
        conditions = VGroup(cond1, cond2, cond3).arrange(RIGHT, buff=0.5).move_to(DOWN * 1.5)

        def make_tick(l, n, color=WHITE):
            c, ang = l.get_center(), l.get_angle() + PI/2
            tks = VGroup()
            offs = np.linspace(-0.08*(n-1), 0.08*(n-1), n) if n > 1 else [0]
            v = np.array([np.cos(l.get_angle()), np.sin(l.get_angle()), 0])
            for off in offs:
                tks.add(Line(UP, DOWN).scale(0.12).set_angle(ang).move_to(c + v*off).set_color(color).set_stroke(width=4))
            return tks

        # Step 1
        ea1 = Line(va[0], va[1], color=RED, stroke_width=6)
        eb1 = Line(vb[0], vb[1], color=RED, stroke_width=6)
        ta1, tb1 = make_tick(ea1, 1), make_tick(eb1, 1)
        self.play(Create(ea1), Create(eb1), Write(ta1), Write(tb1), Write(cond1), run_time=0.8)

        # Step 2
        line_a_b = Line(va[0], va[1])
        line_a_c = Line(va[0], va[2])
        line_b_e = Line(vb[0], vb[1])
        line_b_f = Line(vb[0], vb[2])
        
        ang_a = Angle(line_a_b, line_a_c, radius=0.5, color=YELLOW, stroke_width=5)
        ang_d = Angle(line_b_e, line_b_f, radius=0.5, color=YELLOW, stroke_width=5)
        dot_a = Dot(ang_a.point_from_proportion(0.5), radius=0.04, color=YELLOW)
        dot_d = Dot(ang_d.point_from_proportion(0.5), radius=0.04, color=YELLOW)
        
        self.play(Create(ang_a), Create(ang_d), FadeIn(dot_a), FadeIn(dot_d), Write(cond2), run_time=0.8)

        # Step 3
        ea2 = Line(va[0], va[2], color=PURPLE, stroke_width=6)
        eb2 = Line(vb[0], vb[2], color=PURPLE, stroke_width=6)
        ta2, tb2 = make_tick(ea2, 2), make_tick(eb2, 2)
        self.play(Create(ea2), Create(eb2), Write(ta2), Write(tb2), Write(cond3), run_time=0.8)

        # 結論放在條件下方，間距加寬
        conc = MathTex(
            r"\therefore \triangle ", "A", "B", "C", 
            r" \cong \triangle ", "D", "E", "F", 
            r" \text{ (SAS)}"
        )
        desc = Text("兩邊一夾角相同，就能決定唯一一個完美的三角形", font_size=24, color=GREY)
        conc_grp = VGroup(conc, desc).arrange(DOWN, buff=0.15).next_to(conditions, DOWN, buff=0.4)
        
        self.play(Write(conc_grp))

        for i in range(3):
            self.play(
                Indicate(labels_a[i], color=YELLOW, scale_factor=1.5),
                Indicate(labels_b[i], color=YELLOW, scale_factor=1.5),
                Indicate(conc[i+1], color=YELLOW, scale_factor=1.5),
                Indicate(conc[i+5], color=YELLOW, scale_factor=1.5),
                run_time=0.6
            )
        self.wait(0.5)

        target_tri = tri_a.copy().set_color(GREEN).set_fill(opacity=0.6)
        target_labels = labels_a.copy().set_color(GREEN)
        
        self.play(
            ReplacementTransform(tri_b, target_tri), 
            ReplacementTransform(labels_b, target_labels),
            FadeOut(VGroup(eb1, eb2, tb1, tb2, ang_d, dot_d)), 
            run_time=2, path_arc=PI/4
        )
        self.play(Indicate(target_tri, color=YELLOW))
        
        # 最後總結安全落在邊緣內側
        sum_txt = Text("結論：只要具有兩邊一夾角的分毫不差，即可證明全等", font_size=32, color=GREEN).to_edge(DOWN, buff=0.5)
        self.play(ReplacementTransform(conc_grp, sum_txt), FadeOut(conditions))
        self.wait(3)
