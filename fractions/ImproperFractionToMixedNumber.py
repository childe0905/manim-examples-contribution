from manim import *

class ImproperFractionToMixedNumber(Scene):
    """
    展示假分數轉帶分數 5/4 = 1 1/4
    """

    def construct(self):
        # [VISUAL REASONING]
        # 1. Goal: 假分數轉帶分數 5/4 -> 1 1/4
        # 2. Layout: 左右各一個圓，分成 4 等份。
        # 3. Highlight: 依序填滿 5 份 1/4。滿了的一整個圓退掉切割線，顯示為整數 1。

        title = Text("假分數轉帶分數", font_size=40).to_edge(UP, buff=0.3)
        self.play(Write(title))

        # 一開始顯示假分數 5/4
        init_frac = MathTex(r"\frac{5}{4}", font_size=72).next_to(title, DOWN, buff=0.5)
        self.play(Write(init_frac))
        self.wait(1)

        radius = 1.3
        left_center = LEFT * 2.5 + UP * 0.3
        right_center = RIGHT * 2.5 + UP * 0.3
        
        # 建立左邊的圓 (4等分)
        left_circle = Circle(radius=radius, color=WHITE).move_to(left_center)
        left_slices = VGroup()
        for i in range(4):
            angle = 2 * PI / 4
            start_angle = PI/2 + i * angle
            sector = AnnularSector(
                inner_radius=0,
                outer_radius=radius,
                angle=angle,
                start_angle=start_angle,
                color=WHITE,
                stroke_width=2,
                fill_opacity=0
            ).shift(left_center)
            left_slices.add(sector)
            
        # 建立右邊的圓 (4等分)
        right_circle = Circle(radius=radius, color=WHITE).move_to(right_center)
        right_slices = VGroup()
        for i in range(4):
            angle = 2 * PI / 4
            start_angle = PI/2 + i * angle
            sector = AnnularSector(
                inner_radius=0,
                outer_radius=radius,
                angle=angle,
                start_angle=start_angle,
                color=WHITE,
                stroke_width=2,
                fill_opacity=0
            ).shift(right_center)
            right_slices.add(sector)
            
        self.play(Create(left_slices), Create(left_circle))
        self.play(Create(right_slices), Create(right_circle))
        self.wait(1)

        # 逐片填色 (5片)
        fill_anims = []
        for i in range(4):
            fill_anims.append(left_slices[i].animate.set_fill(BLUE, opacity=0.8))
        
        # 依序塗左邊4片
        for anim in fill_anims:
            self.play(anim, run_time=0.4)
            
        # 塗右邊1片
        self.play(right_slices[0].animate.set_fill(BLUE, opacity=0.8), run_time=0.4)
        self.wait(1)

        # 把左邊滿4分的切割線消除，變成一個完整的整數1
        filled_left_circle = Circle(radius=radius, color=WHITE).move_to(left_center).set_fill(BLUE, opacity=0.8)
        
        # 同時寫出 1 與 1/4
        label_1 = MathTex("1", font_size=60).next_to(left_circle, DOWN, buff=0.3)
        label_1_4 = MathTex(r"\frac{1}{4}", font_size=60).next_to(right_circle, DOWN, buff=0.3)
        
        self.play(
            Transform(left_slices, filled_left_circle),
            Write(label_1),
            Write(label_1_4)
        )
        self.wait(1)

        # 在底下秀出完整算式 5/4 = 1 1/4
        eq_group = VGroup(
            MathTex(r"\frac{5}{4}", font_size=60),
            MathTex("=", font_size=60),
            MathTex(r"1\frac{1}{4}", font_size=60, color=YELLOW)
        ).arrange(RIGHT, buff=0.5).to_edge(DOWN, buff=0.8)
        
        # 從上方的 5/4 飛下來變身，並將 1 與 1/4 組合成最終的帶分數
        self.play(
            Transform(init_frac.copy(), eq_group[0]),
            Write(eq_group[1]),
            Transform(VGroup(label_1, label_1_4), eq_group[2])
        )

        conclusion = Text("滿 4 份即可換成 1 個完整單位", font_size=32, color=YELLOW).next_to(eq_group, UP, buff=0.4)
        self.play(Write(conclusion))

        self.wait(3)
