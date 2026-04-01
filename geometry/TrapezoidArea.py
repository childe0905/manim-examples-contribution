from manim import *
import numpy as np

class TrapezoidArea(Scene):
    """
    展示梯形面積公式推導：倒放複製並拼接成大平行四邊形
    """
    def construct(self):
        # [VISUAL REASONING]
        # 1. Goal: 將梯形複製並旋轉180度，無縫拼接成巨大的平行四邊形，推導面積除以二的由來。
        # 2. Layout:
        #    - 將梯形放在左側中上方，底部空間預留為數學推演區塊。
        #    - 梯形的右斜邊中點做為旋轉錨點，展示數學幾何中的點對稱對接。
        #    - Text 使用原生中文渲染避免 Latex 報錯。

        title = Text("梯形面積公式", font_size=40, t2c={"面積公式": GREEN}).to_edge(UP, buff=0.2)
        subtitle = Text("利用「複製與旋轉」將梯形轉化為平行四邊形", font_size=24, color=YELLOW).next_to(title, DOWN, buff=0.15)
        self.play(Write(title), Write(subtitle))

        # 定義梯形頂點 (基底 y=0.0 保留充足下方空間)
        # 底 b = 3.0, 上底 a = 1.5, 高 h = 2.5
        vA = np.array([-2.75, -0.7, 0])
        vB = np.array([ 0.25, -0.7, 0])
        vC = np.array([-0.25,  1.8, 0])
        vD = np.array([-1.75,  1.8, 0])

        trap1 = Polygon(vA, vB, vC, vD, color=BLUE_B, fill_opacity=0.4)
        self.play(Create(trap1), run_time=1.5)

        # 標示原本的上底、下底、高
        brace_top = Brace(Line(vD, vC), direction=UP, color=WHITE)
        val_top = Text("上底 a", font_size=24, color=YELLOW).next_to(brace_top, UP, buff=0.1)

        brace_bot = Brace(Line(vA, vB), direction=DOWN, color=WHITE)
        val_bot = Text("下底 b", font_size=24, color=GREEN).next_to(brace_bot, DOWN, buff=0.1)

        # 畫高
        E = np.array([vD[0], vA[1], 0])
        line_h = DashedLine(vD, E, color=RED, stroke_width=4)
        brace_h = Brace(line_h, direction=LEFT, color=WHITE)
        val_h = Text("高 h", font_size=24, color=RED).next_to(brace_h, LEFT, buff=0.1)

        self.play(
            FadeIn(brace_top), Write(val_top),
            FadeIn(brace_bot), Write(val_bot),
            Create(line_h), FadeIn(brace_h), Write(val_h)
        )
        self.wait(1)

        txt1 = Text("複製一個完全相同的梯形", font_size=28).move_to(DOWN * 2.3)
        self.play(Write(txt1))
        
        # 複製出第二個梯形
        trap2 = trap1.copy().set_color(YELLOW).set_fill(opacity=0.6)
        self.play(FadeIn(trap2))
        self.wait(0.5)

        txt2 = Text("以斜邊中點為軸，旋轉 180° 並拼接！", font_size=28, color=YELLOW).move_to(txt1)
        self.play(ReplacementTransform(txt1, txt2))

        # 展現中點並旋轉 (中點為 B 與 C 的連線)
        mid_BC = (vB + vC) / 2
        dot_mid = Dot(mid_BC, color=RED, radius=0.08)
        self.play(FadeIn(dot_mid))
        
        # 進行 180度 完美旋轉合併
        self.play(
            Rotate(trap2, angle=PI, about_point=mid_BC),
            run_time=2
        )
        self.play(FadeOut(dot_mid))
        self.wait(1)

        txt3 = Text("拼合成一個「大平行四邊形」！", font_size=30, color=BLUE_A).move_to(txt1)
        self.play(ReplacementTransform(txt2, txt3))

        # 標示這時候擴大出的新底邊 (旋轉過後的上底)
        vD_prime = 2 * mid_BC - vD  # 利用點對稱算出旋轉後 vD 的位置
        brace_new_bot = Brace(Line(vB, vD_prime), direction=DOWN, color=WHITE)
        val_new_bot = Text("上底 a", font_size=24, color=YELLOW).next_to(brace_new_bot, DOWN, buff=0.1)
        
        self.play(FadeIn(brace_new_bot), Write(val_new_bot))
        self.wait(1)
        
        # 將兩個底邊大括號融合成一個大底邊大括號
        brace_total = Brace(Line(vA, vD_prime), direction=DOWN, color=GREEN_C)
        val_total = Text("總底邊 = (上底 a) + (下底 b)", font_size=26, color=GREEN_C).next_to(brace_total, DOWN, buff=0.1)
        
        self.play(
            ReplacementTransform(VGroup(brace_bot, brace_new_bot), brace_total),
            ReplacementTransform(VGroup(val_bot, val_new_bot), val_total)
        )
        
        # 閃爍巨大的平行四邊形
        self.play(Indicate(VGroup(trap1, trap2), color=GREEN))
        self.wait(1)

        # 消除文字，推導演進最終公式
        self.play(FadeOut(txt3))
        
        eq1 = Text("巨型平行四邊形面積 = 原本兩倍大 = 總底 × 高", font_size=30)
        eq2 = Text("因為原本梯形只要這圖形的一半...", font_size=22, color=GREY)
        eq3 = Text("梯形面積 = (上底 + 下底) × 高 ÷ 2", font_size=40, color=YELLOW)
        
        eq_group = VGroup(eq1, eq2, eq3).arrange(DOWN, buff=0.25).move_to(DOWN * 2.8)
        box = SurroundingRectangle(eq_group, color=GREEN, buff=0.3)
        
        self.play(Write(eq1))
        self.wait(0.5)
        self.play(Write(eq2))
        self.wait(1)
        self.play(Write(eq3), Create(box))
        
        # 視覺連結文字到幾何
        self.play(Indicate(val_total, color=YELLOW), Indicate(val_h, color=YELLOW), run_time=1.5)
        self.wait(3)
