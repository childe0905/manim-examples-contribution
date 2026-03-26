from manim import *
import numpy as np
import math


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


class CircleAreaSectors(Scene):
    """
    圓面積推導：參考開源連續切分法，無對白、最精簡的方式展示 n 趨近無限大時的極限狀態。
    """

    def construct(self):
        # [VISUAL REASONING]
        # 1. Goal: 結合開源腳本的連續切片技術，提供無廢話、超緊湊的圓面積視覺推導
        # 2. Layout:
        #    - 左方圓形，右方上下交錯排成的「近似矩形」
        #    - 平滑地讓扇形數量 n 增加，直觀看見近似矩形「變平」的過程
        #    - 極佳標出「高 = r」、「底 = πr」，得出面積 πr²

        radius = 1.6
        circle_pos = np.array([-3.5, 0.5, 0])
        rect_pos = np.array([2.0, 0.5, 0])

        title = Text("圓面積公式推導", font_size=32).to_edge(UP, buff=0.25)
        self.play(Write(title))

        # --- 1. 定義切割函數 ---
        def create_sects_and_rect(n):
            """
            產生圓上的切片 (circle_sects) 與排列成矩形的切片 (rect_sects)
            並返回： (circle_sects, rect_sects)
            """
            dth = TAU / n
            # 在圓上
            c_sects = VGroup()
            for i in range(n):
                s = AnnularSector(
                    inner_radius=0, outer_radius=radius,
                    angle=dth, start_angle=PI/2 + i * dth,
                    fill_opacity=0.88, stroke_width=0.8,
                    color=BLUE_D if i % 2 == 0 else TEAL
                ).set_stroke(WHITE, width=0.8)
                c_sects.add(s)
            
            # 因為所有的 Sector 的尖端都在原點，現在 c_sects 組成了一個完整的圓
            # 我們把它平移到左邊指定的位置
            c_sects.shift(circle_pos)

            # 排成矩形
            # 參考開源代码：偶數朝上，奇數朝下
            topp = []
            bot = []
            for i in range(n):
                temp = c_sects[i].copy().move_to(ORIGIN)
                # 將每個切片轉回朝向 0 度，以方便重新排列
                temp.rotate(-i * dth, about_point=ORIGIN)
                
                half_dth = dth / 2
                if i < math.floor(n / 2):
                    # 頂部
                    temp.rotate(3 * PI / 2 - half_dth, about_point=ORIGIN)
                    topp.append(temp)
                else:
                    # 底部
                    temp.rotate(PI / 2 - half_dth, about_point=ORIGIN)
                    bot.append(temp)
            
            topsects = VGroup(*topp).arrange(RIGHT, buff=0)
            botsects = VGroup(*bot).arrange(LEFT, buff=0)
            
            # 對齊
            botsects.shift(DOWN * radius * 0.5)
            # 依賴數量，讓 topsects 交錯在 botsects 上方
            topsects.next_to(botsects.get_right(), buff=0, aligned_edge=DOWN)
            # 這裡微調：開源指令用了 LEFT*5，但我們只要交錯。
            # 直接使用 arrange 後將左右平移植回中心
            
            # 重新計算完美的矩形交錯
            # 使用我們原版的排列邏輯更加工整
            unit_w = radius * np.pi / n
            total_w = n * unit_w
            r_sects = VGroup()
            for i in range(n):
                color = BLUE_D if i % 2 == 0 else TEAL
                rs = Sector(radius=radius, angle=dth, start_angle=0,
                            fill_color=color, fill_opacity=0.88,
                            stroke_color=WHITE, stroke_width=0.8)
                x = (i + 0.5) * unit_w - total_w / 2
                if i % 2 == 0:
                    rs.rotate(3 * PI / 2 - half_dth, about_point=ORIGIN)
                    rs.shift([x, radius / 2, 0])
                else:
                    rs.rotate(PI / 2 - half_dth, about_point=ORIGIN)
                    rs.shift([x, -radius / 2, 0])
                r_sects.add(rs)
            r_sects.move_to(rect_pos)
            
            return c_sects, r_sects

        # --- 第一階段：畫圓，n=8 時切開移過去 ---
        n_init = 8
        c_sects, r_sects = create_sects_and_rect(n_init)
        
        lbl_r = MathTex(r"r", font_size=28, color=YELLOW).next_to(circle_pos+np.array([radius/2, 0, 0]), UP, buff=0.1)
        r_line = Line(circle_pos, circle_pos+np.array([radius, 0, 0]), color=YELLOW)
        
        self.play(FadeIn(c_sects), Create(r_line), Write(lbl_r))
        self.wait(0.5)
        
        n_label = MathTex(rf"n = {n_init}", font_size=28).next_to(rect_pos, UP, buff=1.2)
        self.play(ReplacementTransform(c_sects.copy(), r_sects), Write(n_label), run_time=1.5)
        self.wait(0.5)

        # --- 第二階段：平滑增加 n (UpdateFromAlphaFunc) ---
        target_n = 60
        old_n_val = [n_init] # pointer for updating label
        
        def update_n(mob, alpha):
            current_n = int(interpolate(n_init, target_n, alpha))
            # 確保是偶數
            if current_n % 2 != 0:
                current_n += 1
            if current_n != old_n_val[0]:
                _, new_r_sects = create_sects_and_rect(current_n)
                mob.become(new_r_sects)
                n_label.become(MathTex(rf"n = \infty", font_size=28).next_to(rect_pos, UP, buff=1.2))
                old_n_val[0] = current_n

        self.play(
            UpdateFromAlphaFunc(r_sects, update_n),
            run_time=3.5, rate_func=rate_functions.smooth
        )
        n_label.become(MathTex(r"n \to \infty", font_size=28).next_to(rect_pos, UP, buff=1.2))
        self.wait(0.5)

        # --- 第三階段：標示「底」、「高」，推導極限公式 ---
        # r_sects 已經更新為 n=60，近似完美矩形
        brace_bot = Brace(r_sects, DOWN, color=YELLOW, buff=0.15)
        lbl_bot = MathTex(r"\pi r", font_size=28, color=YELLOW)
        brace_bot.put_at_tip(lbl_bot)

        # 圓周長一半
        circum_text = MathTex(r"= \frac{1}{2} \cdot 2\pi r", font_size=24, color=GREY_A).next_to(lbl_bot, DOWN, buff=0.1)

        brace_right = Brace(r_sects, RIGHT, color=GREEN_B, buff=0.1)
        lbl_right = MathTex(r"r", font_size=28, color=GREEN_B)
        brace_right.put_at_tip(lbl_right)
        
        # 開發檢查
        assert not overlaps(lbl_bot, title)
        assert not overlaps(lbl_right, n_label)

        self.play(FadeIn(brace_bot), Write(lbl_bot), Write(circum_text))
        self.play(FadeIn(brace_right), Write(lbl_right))
        self.wait(1)

        # 結論： A = pi r * r = pi r^2，中文字使用 Text() 避開 LaTeX 編譯錯誤
        formula = VGroup(
            MathTex("A = ", font_size=32, color=YELLOW),
            Text("底", font_size=24, color=YELLOW),
            MathTex(r" \times ", font_size=32, color=YELLOW),
            Text("高", font_size=24, color=YELLOW),
            MathTex(r" = \pi r \times r = \pi r^2", font_size=32, color=YELLOW)
        ).arrange(RIGHT, buff=0.1).to_edge(DOWN, buff=0.6)
        
        self.play(Write(formula))
        self.play(Create(SurroundingRectangle(formula, color=YELLOW, buff=0.15)))
        self.wait(2)
