from manim import *
import numpy as np

class TriangleInequality(Scene):
    """
    展示三角形不等式定理：任兩邊之和必大於第三邊
    採用失敗(無法閉合)與成功(完美閉合)的對比動畫。
    """
    def construct(self):
        # [VISUAL REASONING]
        # 1. Goal: 視覺化證實長度 2+3<6 無法構成三角形，而 4+5>6 可以。
        # 2. Layout:
        #    - 將基準邊 c 固定在下方中心。
        #    - 用 Rotate 動畫真實模擬圓規畫弧與木棍揮擺的軌跡。
        #    - 說明文字放置在螢幕最下方，結論用來替換頂端的副標題。

        title = Text("三角形不等式", font_size=40, t2c={"不等式": RED}).to_edge(UP, buff=0.2)
        subtitle = Text("三條隨機長度的線段，一定能拼成三角形嗎？", font_size=28, color=YELLOW).next_to(title, DOWN, buff=0.15)
        self.play(Write(title), Write(subtitle))

        # 基礎底邊 c = 6
        vC_L = np.array([-3, -1.5, 0])
        vC_R = np.array([ 3, -1.5, 0])
        
        line_c = Line(vC_L, vC_R, stroke_width=6, color=WHITE)
        label_c = Text("c = 6", font_size=24).next_to(line_c, DOWN, buff=0.15)
        self.play(Create(line_c), Write(label_c))

        # ========== Phase 1: Failure (2 + 3 < 6) ==========
        line_a = Line(vC_L, vC_L + [2, 0, 0], stroke_width=6, color=RED)
        label_a = Text("a = 2", font_size=24, color=RED).next_to(line_a, UP, buff=0.1)
        
        line_b = Line(vC_R, vC_R + [-3, 0, 0], stroke_width=6, color=BLUE)
        label_b = Text("b = 3", font_size=24, color=BLUE).next_to(line_b, UP, buff=0.1)
        
        self.play(Create(line_a), Write(label_a), Create(line_b), Write(label_b))
        
        txt_fail = Text("試錯 1：2 + 3 < 6，我們搖擺試試看...", font_size=28).move_to(DOWN * 3.0)
        self.play(Write(txt_fail))
        
        # 畫圓規輔助軌跡 (虛線圓弧感) 向上揮動 60度 (PI/3)
        arc_a = Arc(radius=2, arc_center=vC_L, start_angle=0, angle=PI/2.5, color=RED, stroke_opacity=0.5)
        arc_b = Arc(radius=3, arc_center=vC_R, start_angle=PI, angle=-PI/2.5, color=BLUE, stroke_opacity=0.5)
        
        self.play(FadeOut(VGroup(label_a, label_b)))
        
        self.play(
            Rotate(line_a, angle=PI/2.5, about_point=vC_L),
            Rotate(line_b, angle=-PI/2.5, about_point=vC_R),
            Create(arc_a), Create(arc_b),
            run_time=2
        )
        self.wait(0.5)
        
        # 放下
        self.play(
            Rotate(line_a, angle=-PI/2.5, about_point=vC_L),
            Rotate(line_b, angle=PI/2.5, about_point=vC_R),
            FadeOut(VGroup(arc_a, arc_b)),
            run_time=1.5
        )
        
        txt_fail2 = Text("結論：長度不足碰不到！無法閉合形成三角形！", font_size=28, color=RED).move_to(txt_fail)
        self.play(ReplacementTransform(txt_fail, txt_fail2))
        self.wait(1.5)

        # ========== Phase 2: Success (4 + 5 > 6) ==========
        txt_succ = Text("試錯 2：將長度增加為 (4 與 5) 試試看！", font_size=28, color=GREEN).move_to(txt_fail)
        self.play(ReplacementTransform(txt_fail2, txt_succ))
        
        new_line_a = Line(vC_L, vC_L + [4, 0, 0], stroke_width=8, color=RED)
        new_line_b = Line(vC_R, vC_R + [-5, 0, 0], stroke_width=8, color=BLUE)
        
        # 標出新長度
        nlbl_a = Text("a = 4", font_size=24, color=RED).next_to(new_line_a, UP, buff=0.1)
        nlbl_b = Text("b = 5", font_size=24, color=BLUE).next_to(new_line_b, UP, buff=0.1)

        self.play(
            ReplacementTransform(line_a, new_line_a),
            ReplacementTransform(line_b, new_line_b)
        )
        self.play(FadeIn(VGroup(nlbl_a, nlbl_b)))
        self.wait(1)
        
        # 數學計算交叉點
        # 以 vC_L 為原點 (0,0), a=4, b=5, c=6.
        # x_c = (16 + 36 - 25) / 12 = 27 / 12 = 2.25
        # y_c = sqrt(16 - 2.25^2) = 3.307189
        x_c = 2.25
        y_c = np.sqrt(16 - 2.25**2)
        
        I = vC_L + np.array([x_c, y_c, 0])
        theta_a = np.arctan2(y_c, x_c)
        theta_b = np.arctan2(y_c, x_c - 6) # 會在第二象限
        
        arc_a_succ = Arc(radius=4, arc_center=vC_L, start_angle=0, angle=theta_a, color=RED, stroke_opacity=0.6)
        arc_b_succ = Arc(radius=5, arc_center=vC_R, start_angle=PI, angle=theta_b - PI, color=BLUE, stroke_opacity=0.6)
        
        self.play(FadeOut(VGroup(nlbl_a, nlbl_b)))
        self.play(
            Rotate(new_line_a, angle=theta_a, about_point=vC_L),
            Rotate(new_line_b, angle=theta_b - PI, about_point=vC_R),
            Create(arc_a_succ), Create(arc_b_succ),
            run_time=2,
            rate_func=smooth
        )
        
        # 打上交叉亮點
        dot_I = Dot(I, color=YELLOW, radius=0.08)
        self.play(FadeIn(dot_I))
        self.play(Indicate(dot_I, scale_factor=2.0))
        
        txt_succ_2 = Text("結論：完美閉合交匯！成功產生了三角形！", font_size=28, color=GREEN).move_to(txt_fail)
        self.play(ReplacementTransform(txt_succ, txt_succ_2))
        self.wait(1)
        
        # ========== Phase 3: Definition ==========
        # 我們直接把 subtitle 替換成大總結定理
        self.play(FadeOut(VGroup(arc_a_succ, arc_b_succ)))
        
        final_box = Text("定理：任兩邊長度之和 必大於 第三邊 (a + b > c)", font_size=32, color=GREEN).next_to(title, DOWN, buff=0.4)
        box = SurroundingRectangle(final_box, color=GREEN, buff=0.2)
        
        self.play(
            ReplacementTransform(subtitle, final_box),
            Create(box)
        )
        self.play(Indicate(final_box, color=YELLOW), Indicate(new_line_a, color=YELLOW), Indicate(new_line_b, color=YELLOW))
        self.wait(3)
