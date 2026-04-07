from manim import *

class EquivalentFractionsAreaModel(Scene):
    """
    用同樣大小的長方形或條帶，展示 1/2 = 2/4 = 4/8。
    強調「切分」的過程、數值邏輯 (分母分子同乘2)，並在最後引導互動。
    """

    def construct(self):
        # [VISUAL REASONING]
        # 1. Goal: 展示等值分數 1/2 = 2/4 = 4/8 的「切分」與「擴分」關聯
        # 2. Layout: 上中下三層展示三個等長度的矩形條帶
        # 3. Highlight: 填色總長度一致，並明確標示等式之間的乘法關係

        title = Text("等值分數", font_size=40).to_edge(UP, buff=0.3)
        self.play(Write(title))

        bar_width = 4
        bar_height = 0.8
        
        colors = [BLUE, TEAL, GREEN]
        
        # 定義生成矩形條帶的幫助函數
        def get_fraction_bar(parts, filled, color):
            bar = VGroup()
            pw = bar_width / parts
            for i in range(parts):
                rect = Rectangle(width=pw, height=bar_height, color=WHITE, stroke_width=2)
                if i < filled:
                    rect.set_fill(color, opacity=0.7)
                else:
                    rect.set_fill(color, opacity=0.1)
                bar.add(rect)
            bar.arrange(RIGHT, buff=0)
            return bar

        # 1. 第一層：1/2
        bar1 = get_fraction_bar(2, 1, colors[0])
        bar1.shift(UP * 1.5)
        label1 = MathTex(r"\frac{1}{2}").next_to(bar1, LEFT, buff=0.5)
        
        self.play(Create(bar1), Write(label1))
        self.wait(1)

        # 2. 第二層：從 1/2 切分變成 2/4
        bar2_initial = get_fraction_bar(2, 1, colors[1]).next_to(bar1, DOWN, buff=0.8)
        label2_initial = MathTex(r"\frac{1}{2}").next_to(bar2_initial, LEFT, buff=0.5)
        
        self.play(Create(bar2_initial), Write(label2_initial))
        self.wait(0.5)
        
        # 畫切線（將每塊切半）
        cut_lines_2 = VGroup()
        for rect in bar2_initial:
            line = DashedLine(
                start=rect.get_top(),
                end=rect.get_bottom(),
                color=YELLOW, stroke_width=4
            )
            cut_lines_2.add(line)
        
        bar2_final = get_fraction_bar(4, 2, colors[1]).move_to(bar2_initial)
        label2_final = MathTex(r"\frac{2}{4}").move_to(label2_initial)
        
        self.play(Create(cut_lines_2))
        self.wait(0.5)
        # 用動畫呈現分裂
        self.play(
            ReplacementTransform(bar2_initial, bar2_final),
            FadeOut(cut_lines_2),
            Transform(label2_initial, label2_final)
        )
        self.wait(1)

        # 3. 第三層：從 2/4 切分變成 4/8
        bar3_initial = get_fraction_bar(4, 2, colors[2]).next_to(bar2_final, DOWN, buff=0.8)
        label3_initial = MathTex(r"\frac{2}{4}").next_to(bar3_initial, LEFT, buff=0.5)
        
        self.play(Create(bar3_initial), Write(label3_initial))
        self.wait(0.5)
        
        cut_lines_3 = VGroup()
        for rect in bar3_initial:
            line = DashedLine(
                start=rect.get_top(),
                end=rect.get_bottom(),
                color=YELLOW, stroke_width=4
            )
            cut_lines_3.add(line)
            
        bar3_final = get_fraction_bar(8, 4, colors[2]).move_to(bar3_initial)
        label3_final = MathTex(r"\frac{4}{8}").move_to(label3_initial)
        
        self.play(Create(cut_lines_3))
        self.wait(0.5)
        self.play(
            ReplacementTransform(bar3_initial, bar3_final),
            FadeOut(cut_lines_3),
            Transform(label3_initial, label3_final)
        )
        self.wait(1)

        # 4. 強調填色的總長度一模一樣
        filled_parts = VGroup(bar1[0], bar2_final[:2], bar3_final[:4])
        highlight_box = SurroundingRectangle(filled_parts, color=YELLOW, buff=0.1, stroke_width=4)
        
        summary_text = Text("相同的面積，不同的名稱。", font_size=24, color=YELLOW)
        summary_text.next_to(highlight_box, UP, buff=0.2)
        
        self.play(Create(highlight_box), Write(summary_text))
        
        # 閃爍一次
        self.play(FadeOut(highlight_box), FadeOut(summary_text), run_time=0.5)
        self.play(FadeIn(highlight_box), FadeIn(summary_text), run_time=0.5)
        self.wait(2)

        # 5. 數值邏輯關聯與總結等式
        # 清除上方圖形，留下文字與最後算式
        self.play(
            FadeOut(bar1), FadeOut(label1),
            FadeOut(bar2_final), FadeOut(label2_initial),
            FadeOut(bar3_final), FadeOut(label3_initial),
            FadeOut(highlight_box), FadeOut(summary_text)
        )

        eq_group = VGroup()
        f1 = MathTex(r"\frac{1}{2}", font_size=60)
        eq1 = MathTex("=", font_size=60)
        f2 = MathTex(r"\frac{2}{4}", font_size=60)
        eq2 = MathTex("=", font_size=60)
        f3 = MathTex(r"\frac{4}{8}", font_size=60)
        
        eq_group.add(f1, eq1, f2, eq2, f3)
        eq_group.arrange(RIGHT, buff=1.0).move_to(ORIGIN).shift(UP * 0.5)
        
        self.play(Write(eq_group))
        
        # 加入箭頭標示擴分
        # 上方的 x2 (分子1->2)
        arrow_num1 = CurvedArrow(f1.get_top() + UP*0.2, f2.get_top() + UP*0.2, angle=-PI/2, color=YELLOW)
        m2_1 = MathTex(r"\times 2", font_size=30, color=YELLOW).next_to(arrow_num1, UP, buff=0.1)
        # 下方的 x2 (分母2->4)
        arrow_den1 = CurvedArrow(f1.get_bottom() + DOWN*0.2, f2.get_bottom() + DOWN*0.2, angle=PI/2, color=YELLOW)
        m2_2 = MathTex(r"\times 2", font_size=30, color=YELLOW).next_to(arrow_den1, DOWN, buff=0.1)
        
        # 上方的 x2 (分子2->4)
        arrow_num2 = CurvedArrow(f2.get_top() + UP*0.2, f3.get_top() + UP*0.2, angle=-PI/2, color=YELLOW)
        m2_3 = MathTex(r"\times 2", font_size=30, color=YELLOW).next_to(arrow_num2, UP, buff=0.1)
        # 下方的 x2 (分母4->8)
        arrow_den2 = CurvedArrow(f2.get_bottom() + DOWN*0.2, f3.get_bottom() + DOWN*0.2, angle=PI/2, color=YELLOW)
        m2_4 = MathTex(r"\times 2", font_size=30, color=YELLOW).next_to(arrow_den2, DOWN, buff=0.1)

        self.play(Create(arrow_num1), Create(arrow_den1), Write(m2_1), Write(m2_2))
        self.wait(0.5)
        self.play(Create(arrow_num2), Create(arrow_den2), Write(m2_3), Write(m2_4))
        self.wait(2)

        # 6. 互動問題
        q_text = VGroup(
            Text("如果是 ", font_size=36),
            MathTex(r"\frac{8}{16}", font_size=48, color=TEAL),
            Text(" 的圖形會長什麼樣子呢？", font_size=36)
        ).arrange(RIGHT, buff=0.2).next_to(eq_group, DOWN, buff=2.0)
        
        self.play(Write(q_text))
        self.wait(4)
