from manim import *
import numpy as np

class SurfaceAreaNet(ThreeDScene):
    """
    用邊長 2 的立方體展示表面積：先以 3D 旋轉展示立體，
    再將六個面動畫展開成十字形展開圖，標出表面積。
    """

    def construct(self):
        # [VISUAL REASONING]
        # 1. Goal: 展示立方體 6 個面如何展開成 net，表面積 = 6s²。
        # 2. Layout: 3D 立方體先旋轉展示（含邊長標示），
        #            展開後 net 靠左、計算公式在右側。
        # 3. Highlight: 6 面用 6 色區分，展開動畫保留顏色對應。

        s = 1.2
        COLORS = [BLUE, GREEN, YELLOW, RED_C, ORANGE, TEAL]
        NAMES = ["Front", "Top", "Right", "Left", "Bottom", "Back"]

        # ── 0. 標題 ──────────────────────────────────────────────────
        self.set_camera_orientation(phi=65 * DEGREES, theta=-40 * DEGREES)
        title = Title("Surface Area of a Cube (Net)")
        self.add_fixed_in_frame_mobjects(title)
        self.play(Write(title))

        # ── 1. 建立 3D 立方體（前面 z=0，往後延伸 z=s）────────────
        front = Square(s, fill_color=COLORS[0], fill_opacity=0.7,
                       stroke_color=WHITE, stroke_width=2)

        top = Square(s, fill_color=COLORS[1], fill_opacity=0.7,
                     stroke_color=WHITE, stroke_width=2)
        top.rotate(PI / 2, axis=RIGHT).shift(UP * s / 2 + OUT * s / 2)

        right_f = Square(s, fill_color=COLORS[2], fill_opacity=0.7,
                         stroke_color=WHITE, stroke_width=2)
        right_f.rotate(PI / 2, axis=UP).shift(RIGHT * s / 2 + OUT * s / 2)

        left_f = Square(s, fill_color=COLORS[3], fill_opacity=0.7,
                        stroke_color=WHITE, stroke_width=2)
        left_f.rotate(PI / 2, axis=UP).shift(LEFT * s / 2 + OUT * s / 2)

        bottom = Square(s, fill_color=COLORS[4], fill_opacity=0.7,
                        stroke_color=WHITE, stroke_width=2)
        bottom.rotate(PI / 2, axis=RIGHT).shift(DOWN * s / 2 + OUT * s / 2)

        back = Square(s, fill_color=COLORS[5], fill_opacity=0.7,
                      stroke_color=WHITE, stroke_width=2)
        back.shift(OUT * s)

        cube = VGroup(back, left_f, bottom, front, right_f, top)
        self.play(FadeIn(cube))

        # 3D 邊長標示
        edge_lbl = Text("2", font_size=22, color=WHITE)
        edge_lbl.rotate(PI / 2, axis=RIGHT)
        edge_lbl.next_to(front, DOWN, buff=0.1).shift(OUT * 0.05)
        self.play(FadeIn(edge_lbl))

        # ── 2. 旋轉展示立體感 ───────────────────────────────────────
        self.begin_ambient_camera_rotation(rate=0.3)
        self.wait(3)
        self.stop_ambient_camera_rotation()
        self.play(FadeOut(edge_lbl))
        self.wait(0.2)

        # ── 3. 展開前將立方體移至左下方，避免展開時擋到標題 ─────────
        OFFSET = np.array([-2.5, -1.0, 0])
        self.play(cube.animate.shift(OFFSET), run_time=1)
        self.wait(0.2)

        # ── 4. 展開動畫：各面繞鉸鍊邊旋轉攤平至 z=0 ───────────────
        self.play(
            top.animate.rotate(-PI / 2, axis=RIGHT,
                               about_point=OFFSET + [0, s / 2, 0]),
            bottom.animate.rotate(PI / 2, axis=RIGHT,
                                  about_point=OFFSET + [0, -s / 2, 0]),
            right_f.animate.rotate(PI / 2, axis=UP,
                                   about_point=OFFSET + [s / 2, 0, 0]),
            left_f.animate.rotate(-PI / 2, axis=UP,
                                  about_point=OFFSET + [-s / 2, 0, 0]),
            run_time=2,
        )
        # Back 從 top 的上邊繼續展開
        self.play(
            back.animate.rotate(-PI / 2, axis=RIGHT,
                                about_point=OFFSET + [0, s / 2, 0])
                        .rotate(-PI / 2, axis=RIGHT,
                                about_point=OFFSET + [0, 3 * s / 2, 0]),
            run_time=1.5,
        )

        # ── 5. 轉正相機，俯瞰展開圖 ────────────────────────────────
        self.move_camera(phi=0, theta=-PI / 2, run_time=1.5)
        self.wait(0.3)

        # ── 6. 面名標籤 ─────────────────────────────────────────────
        faces = [front, top, right_f, left_f, bottom, back]
        labels = VGroup()
        for name, face in zip(NAMES, faces):
            lbl = Text(name, font_size=14, color=WHITE)
            lbl.move_to(face.get_center())
            labels.add(lbl)
        self.add_fixed_in_frame_mobjects(labels)
        self.play(FadeIn(labels))

        # 展開圖邊長標示 "2"
        dim_h = Text("2", font_size=18, color=WHITE)
        dim_h.next_to(front, DOWN, buff=0.08)
        dim_v = Text("2", font_size=18, color=WHITE)
        dim_v.next_to(front, LEFT, buff=0.08)
        dims = VGroup(dim_h, dim_v)
        self.add_fixed_in_frame_mobjects(dims)
        self.play(FadeIn(dims))
        self.wait(0.5)

        # ── 7. 右側計算區 ───────────────────────────────────────────
        TEXT_X = 3.0
        calc1 = MathTex(r"\text{Each face} = 2 \times 2 = 4"
                        ).scale(0.7).move_to([TEXT_X, 1.0, 0])
        calc2 = MathTex(r"\text{6 faces total}"
                        ).scale(0.7).move_to([TEXT_X, 0.2, 0])
        formula = MathTex(
            r"SA = 6 \times 4 = ", r"24"
        ).scale(0.85).move_to([TEXT_X, -0.8, 0])
        formula[1].set_color(YELLOW)

        self.add_fixed_in_frame_mobjects(calc1, calc2, formula)
        self.play(Write(calc1))
        self.play(Write(calc2))
        self.play(Write(formula))
        self.play(Indicate(formula[1], color=YELLOW))
        self.wait(2)
