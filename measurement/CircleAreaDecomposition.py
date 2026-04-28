from manim import *
import numpy as np

class CircleAreaDecomposition(Scene):
    """
    把圓切成扇形，再上下交錯排列成近似長方形，
    展示圓面積公式 A = πr² 的直觀推導。
    """

    def construct(self):
        # [VISUAL REASONING]
        # 1. Goal: 用扇形重排法直觀理解圓面積 = πr²。
        # 2. Layout: 標題頂部；圓形與扇形重排分左右擺放；
        #            公式置於底部。
        # 3. Highlight: 扇形用藍黃交替填色，
        #               最終長方形的寬(πr)與高(r)用白色標線強調。

        R = 1.5  # 畫面用半徑（規格半徑 2，縮小以適配畫面）

        # ── 0. 標題 ──────────────────────────────────────────────────
        title = Title("Circle Area by Decomposition")
        self.play(Write(title))

        # ── 1. 畫圓並切成 8 份 ──────────────────────────────────────
        circle_center = LEFT * 3.5 + DOWN * 0.3
        circle = Circle(radius=R, color=BLUE, fill_opacity=0.3)
        circle.move_to(circle_center)
        self.play(Create(circle))

        n = 8
        sectors = self._make_sectors(n, R, circle_center)
        cut_lines = VGroup(*[
            Line(circle_center,
                 circle_center + R * np.array([np.cos(i * TAU / n),
                                               np.sin(i * TAU / n), 0]),
                 stroke_width=1, color=WHITE)
            for i in range(n)
        ])
        self.play(Create(cut_lines))
        self.play(FadeOut(circle), FadeOut(cut_lines), FadeIn(sectors))
        self.wait(0.5)

        # ── 2. 重排 8 份扇形 ────────────────────────────────────────
        target_8 = self._make_rearranged(n, R, RIGHT * 1.5 + DOWN * 0.3)
        self.play(ReplacementTransform(sectors, target_8), run_time=1.5)

        label_8 = Text("8 sectors", font_size=24, color=WHITE)
        label_8.next_to(target_8, UP, buff=0.3)
        self.play(Write(label_8))
        self.wait(1)

        # ── 3. 切成 16 份並重排 ─────────────────────────────────────
        self.play(FadeOut(target_8), FadeOut(label_8))

        n2 = 16
        sectors_16 = self._make_sectors(n2, R, circle_center)
        self.play(FadeIn(sectors_16))
        self.wait(0.3)

        target_16 = self._make_rearranged(n2, R, RIGHT * 1.5 + DOWN * 0.3)
        self.play(ReplacementTransform(sectors_16, target_16), run_time=1.5)

        label_16 = Text("16 sectors → rectangle", font_size=24, color=WHITE)
        label_16.next_to(target_16, UP, buff=0.3)
        self.play(Write(label_16))
        self.wait(0.8)

        # ── 4. 標示寬(πr)與高(r)，推導公式 ─────────────────────────
        rect_box = target_16.copy()
        bb = rect_box.get_critical_point(DL)
        bt = rect_box.get_critical_point(UL)
        br = rect_box.get_critical_point(DR)

        brace_w = Brace(Line(bb, br), DOWN, color=WHITE)
        brace_h = Brace(Line(bb, bt), LEFT, color=WHITE)
        lbl_w = MathTex(r"\pi r", font_size=30).next_to(brace_w, DOWN, buff=0.15)
        lbl_h = MathTex(r"r", font_size=30).next_to(brace_h, LEFT, buff=0.15)

        self.play(Create(brace_w), Write(lbl_w),
                  Create(brace_h), Write(lbl_h))
        self.wait(0.5)

        formula = MathTex(
            r"A \approx \pi r \times r = ", r"\pi r^2"
        ).scale(0.85).to_edge(DOWN, buff=0.5)
        formula[1].set_color(YELLOW)
        self.play(Write(formula))
        self.play(Indicate(formula[1], color=YELLOW))
        self.wait(2)

    # ── helpers ──────────────────────────────────────────────────────
    def _make_sectors(self, n, r, center):
        """建立 n 個扇形組成的圓，交替藍黃配色。"""
        angle = TAU / n
        return VGroup(*[
            Sector(radius=r, angle=angle, start_angle=i * angle,
                   fill_color=BLUE if i % 2 == 0 else YELLOW,
                   fill_opacity=0.6, stroke_color=WHITE, stroke_width=1
                   ).shift(center)
            for i in range(n)
        ])

    def _make_rearranged(self, n, r, center):
        """將 n 個扇形上下交錯排列成近似長方形。"""
        angle = TAU / n
        chord = 2 * r * np.sin(angle / 2)
        group = VGroup()
        for i in range(n):
            s = Sector(radius=r, angle=angle, start_angle=0,
                       fill_color=BLUE if i % 2 == 0 else YELLOW,
                       fill_opacity=0.6, stroke_color=WHITE, stroke_width=1)
            if i % 2 == 0:  # 尖端朝上
                s.rotate(PI / 2 - angle / 2)
                s.shift(UP * 0)
            else:            # 尖端朝下
                s.rotate(-PI / 2 - angle / 2)
                s.shift(DOWN * 0)
            s.move_to(np.array([i * chord / 2, 0, 0]))
            group.add(s)
        group.move_to(center)
        return group
