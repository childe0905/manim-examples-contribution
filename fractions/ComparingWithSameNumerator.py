from manim import *

class ComparingWithSameNumerator(Scene):
    """
    展示同分子分數比較 1/3 vs 1/4
    """

    def construct(self):
        # [VISUAL REASONING]
        # 1. Goal: 教授同分子比較 1/3 > 1/4
        # 2. Layout: 左右各一個圓(代表披薩)，左邊切3份，右邊切4份
        # 3. Highlight: 抽出左右的一塊，旋轉並將頂點重合於中央下方，直截了當地展示面積與角度的差異

        title = Text("同分子分數比較", font_size=40).to_edge(UP, buff=0.3)
        self.play(Write(title))

        radius = 1.5
        left_center = LEFT * 3.5 + UP * 1.0
        right_center = RIGHT * 3.5 + UP * 1.0
        
        # 建立左邊的圓 1/3
        left_circle = Circle(radius=radius, color=WHITE).move_to(left_center)
        left_slices = VGroup()
        for i in range(3):
            angle = 2 * PI / 3
            start_angle = PI/2 + i * angle # 從正上方開始
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
            
        # 建立右邊的圓 1/4
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

        # Labels
        label_left = MathTex(r"\frac{1}{3}", font_size=60).next_to(left_circle, DOWN, buff=0.5)
        label_right = MathTex(r"\frac{1}{4}", font_size=60).next_to(right_circle, DOWN, buff=0.5)
        
        self.play(Write(label_left), Write(label_right))
        
        # 填色 1/3 (第一塊)
        self.play(left_slices[0].animate.set_fill(BLUE, opacity=0.8))
        # 填色 1/4 (第一塊)
        self.play(right_slices[0].animate.set_fill(GREEN, opacity=0.8))
        self.wait(1)

        # 抽出動畫
        pulled_left = left_slices[0].copy()
        pulled_right = right_slices[0].copy()
        self.add(pulled_left, pulled_right)
        
        # 將它們拉出來並旋轉，讓它們有一邊貼齊水平線 (轉 -PI/2)
        # sector的頂點就是其圓心 get_arc_center()
        self.play(
            pulled_left.animate.shift(DOWN * 0.5),
            pulled_right.animate.shift(DOWN * 0.5)
        )
        self.play(
            Rotate(pulled_left, angle=-PI/2, about_point=pulled_left.get_arc_center()),
            Rotate(pulled_right, angle=-PI/2, about_point=pulled_right.get_arc_center())
        )
        self.wait(0.5)

        # 將兩個扇形的圓心頂點對齊在中間下方
        target_vertex = DOWN * 1.0
        shift_left = target_vertex - pulled_left.get_arc_center()
        shift_right = target_vertex - pulled_right.get_arc_center()
        
        # 將綠色設為半透明，蓋到藍色上面，清楚看出藍色大於綠色
        self.play(
            pulled_left.animate.shift(shift_left),
            pulled_right.animate.shift(shift_right).set_fill(GREEN, opacity=0.6)
        )
        self.wait(1)
        
        # 結尾算式
        eq_group = VGroup(
            MathTex(r"\frac{1}{3}", font_size=60),
            MathTex(">", font_size=60, color=YELLOW),
            MathTex(r"\frac{1}{4}", font_size=60)
        ).arrange(RIGHT, buff=0.5).to_edge(DOWN, buff=1.5)
        
        self.play(
            Transform(label_left, eq_group[0]),
            Transform(label_right, eq_group[2]),
            Write(eq_group[1])
        )

        # 結論文字
        conclusion = Text("切越多份，單份越小", font_size=36, color=YELLOW).next_to(eq_group, DOWN, buff=0.3)
        self.play(Write(conclusion))

        self.wait(3)
