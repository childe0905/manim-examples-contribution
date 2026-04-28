from manim import *
import numpy as np

class CuboidSurfaceAreaNet(ThreeDScene):
    """
    用長方體（寬=3, 高=2, 深=1）展示表面積：
    先以 3D 旋轉展示立體，再展開成十字形展開圖，標出各面面積。
    """

    def construct(self):
        # [VISUAL REASONING]
        # 1. Goal: 展示長方體 6 個面展開成 net，計算表面積。
        # 2. Layout: 3D 長方體在左側旋轉，展開後移到左下，右側顯示公式。
        # 3. Highlight: 三對相對的面分別用同色系區分。

        UNIT = 0.6
        w, h, d = 3, 2, 1
        w_v, h_v, d_v = w * UNIT, h * UNIT, d * UNIT

        # 相對面同色：前後(藍), 上下(綠), 左右(黃)
        COLORS = [BLUE, GREEN, YELLOW, YELLOW, GREEN, BLUE]
        NAMES = ["Front", "Top", "Right", "Left", "Bottom", "Back"]

        # ── 0. 標題 ──────────────────────────────────────────────────
        self.set_camera_orientation(phi=65 * DEGREES, theta=-40 * DEGREES)
        title = Title("Surface Area of a Cuboid (Net)")
        self.add_fixed_in_frame_mobjects(title)
        self.play(Write(title))

        # ── 1. 建立 3D 長方體 ──────────────────────────────────────
        front = Rectangle(width=w_v, height=h_v, fill_color=COLORS[0], fill_opacity=0.7, stroke_color=WHITE, stroke_width=2)
        top = Rectangle(width=w_v, height=d_v, fill_color=COLORS[1], fill_opacity=0.7, stroke_color=WHITE, stroke_width=2)
        top.rotate(PI / 2, axis=RIGHT).shift(UP * h_v / 2 + OUT * d_v / 2)
        right_f = Rectangle(width=d_v, height=h_v, fill_color=COLORS[2], fill_opacity=0.7, stroke_color=WHITE, stroke_width=2)
        right_f.rotate(PI / 2, axis=UP).shift(RIGHT * w_v / 2 + OUT * d_v / 2)
        left_f = Rectangle(width=d_v, height=h_v, fill_color=COLORS[3], fill_opacity=0.7, stroke_color=WHITE, stroke_width=2)
        left_f.rotate(PI / 2, axis=UP).shift(LEFT * w_v / 2 + OUT * d_v / 2)
        bottom = Rectangle(width=w_v, height=d_v, fill_color=COLORS[4], fill_opacity=0.7, stroke_color=WHITE, stroke_width=2)
        bottom.rotate(PI / 2, axis=RIGHT).shift(DOWN * h_v / 2 + OUT * d_v / 2)
        back = Rectangle(width=w_v, height=h_v, fill_color=COLORS[5], fill_opacity=0.7, stroke_color=WHITE, stroke_width=2)
        back.shift(OUT * d_v)

        cuboid = VGroup(back, left_f, bottom, front, right_f, top)
        self.play(FadeIn(cuboid))

        # 3D 邊長標示
        lbl_w = Text("3", font_size=22, color=YELLOW).next_to(front, DOWN, buff=0.1).shift(OUT * 0.05)
        lbl_h = Text("2", font_size=22, color=YELLOW).next_to(front, LEFT, buff=0.1).shift(OUT * 0.05)
        lbl_d = Text("1", font_size=22, color=YELLOW).rotate(PI / 2, axis=RIGHT).rotate(PI / 2, axis=UP).next_to(right_f, DOWN, buff=0.1).shift(IN * d_v / 2)
        edge_lbls = VGroup(lbl_w, lbl_h, lbl_d)
        self.play(FadeIn(edge_lbls))

        # ── 2. 旋轉展示 ─────────────────────────────────────────────
        self.begin_ambient_camera_rotation(rate=0.3)
        self.wait(3)
        self.stop_ambient_camera_rotation()
        self.play(FadeOut(edge_lbls))
        self.wait(0.2)

        # ── 3. 展開前將長方體移至左下方 ─────────────────────────────
        OFFSET = np.array([-2.5, -1.0, 0])
        self.play(cuboid.animate.shift(OFFSET), run_time=1)
        self.wait(0.2)

        # ── 4. 展開動畫 ─────────────────────────────────────────────
        self.play(
            top.animate.rotate(-PI / 2, axis=RIGHT, about_point=OFFSET + [0, h_v / 2, 0]),
            bottom.animate.rotate(PI / 2, axis=RIGHT, about_point=OFFSET + [0, -h_v / 2, 0]),
            right_f.animate.rotate(PI / 2, axis=UP, about_point=OFFSET + [w_v / 2, 0, 0]),
            left_f.animate.rotate(-PI / 2, axis=UP, about_point=OFFSET + [-w_v / 2, 0, 0]),
            run_time=2,
        )
        self.play(
            back.animate.rotate(-PI / 2, axis=RIGHT, about_point=OFFSET + [0, h_v / 2, 0])
                        .rotate(-PI / 2, axis=RIGHT, about_point=OFFSET + [0, h_v / 2 + d_v, 0]),
            run_time=1.5,
        )

        # ── 5. 俯瞰相機 ─────────────────────────────────────────────
        self.move_camera(phi=0, theta=-PI / 2, run_time=1.5)
        self.wait(0.3)

        # ── 6. 面名與尺寸標籤 ───────────────────────────────────────
        faces = [front, top, right_f, left_f, bottom, back]
        labels = VGroup()
        for name, face in zip(NAMES, faces):
            lbl = Text(name, font_size=16, color=WHITE).move_to(face.get_center())
            labels.add(lbl)
        self.add_fixed_in_frame_mobjects(labels)

        # 把尺寸標籤放在展開圖的「最外側邊緣」避免和面名重疊
        dim_w = Text("3", font_size=20, color=YELLOW).next_to(bottom, DOWN, buff=0.1)
        dim_h = Text("2", font_size=20, color=YELLOW).next_to(left_f, LEFT, buff=0.1)
        dim_d1 = Text("1", font_size=20, color=YELLOW).next_to(left_f, UP, buff=0.1)
        dim_d2 = Text("1", font_size=20, color=YELLOW).next_to(top, LEFT, buff=0.1)
        dims = VGroup(dim_w, dim_h, dim_d1, dim_d2)
        self.add_fixed_in_frame_mobjects(dims)
        self.play(FadeIn(labels), FadeIn(dims))
        self.wait(0.5)

        # ── 7. 右側計算區 ───────────────────────────────────────────
        TEXT_X = 3.0
        c_fb = MathTex(r"\text{Front/Back: } 3 \times 2 = 6", color=BLUE).scale(0.7).move_to([TEXT_X, 1.2, 0])
        c_tb = MathTex(r"\text{Top/Bottom: } 3 \times 1 = 3", color=GREEN).scale(0.7).move_to([TEXT_X, 0.6, 0])
        c_lr = MathTex(r"\text{Left/Right: } 2 \times 1 = 2", color=YELLOW).scale(0.7).move_to([TEXT_X, 0.0, 0])
        
        formula = MathTex(
            r"SA &= 2 \times (6 + 3 + 2) \\ &= ", r"22"
        ).scale(0.85).move_to([TEXT_X, -1.0, 0])
        formula[1].set_color(YELLOW)

        self.add_fixed_in_frame_mobjects(c_fb, c_tb, c_lr, formula)
        self.play(Write(c_fb))
        self.play(Write(c_tb))
        self.play(Write(c_lr))
        self.play(Write(formula))
        self.play(Indicate(formula[1], color=YELLOW))
        self.wait(2)
