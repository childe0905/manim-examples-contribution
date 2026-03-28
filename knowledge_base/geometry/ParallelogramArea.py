from manim import *
import numpy as np

class ParallelogramArea(Scene):
    """
    用「割補法」動畫完美展示平行四邊形面積公式的由來
    """
    def construct(self):
        # [VISUAL REASONING]
        # 1. Goal: 透過將平行四邊形突出的直角三角形切下並平移，組合成大家熟悉的矩形，證明 面積 = 底x高。
        # 2. Layout: 
        #    - 圖形偏畫面上方與中央，將視覺重心留出下方空間給說明文字。
        #    - 使用 Brace (大括號) 動態跟隨底邊的變化，保持視覺引導不斷裂。
        #    - 割補過程設計了一點拋物線軌跡 (path_arc)，增加靈動感。

        title = Text("平行四邊形面積公式", font_size=40, t2c={"面積公式": GREEN}).to_edge(UP, buff=0.2)
        subtitle = Text("利用「割補法」將平行四邊形轉化為矩形", font_size=28, color=YELLOW).next_to(title, DOWN, buff=0.15)
        self.play(Write(title), Write(subtitle))

        # 定義頂點 (整體圖形稍微向上平移，預留下方區域給數學文字)
        vA = np.array([-2.5,  0.0, 0])
        vB = np.array([ 1.5,  0.0, 0])
        vC = np.array([ 2.5,  2.5, 0])
        vD = np.array([-1.5,  2.5, 0])
        E  = np.array([-1.5,  0.0, 0]) # 從 D 往下作的垂足

        # 主體平行四邊形
        pg_full = Polygon(vA, vB, vC, vD, color=BLUE_B, fill_opacity=0.3)
        self.play(Create(pg_full), run_time=1.5)

        # 標出底與高
        brace_b = Brace(Line(vA, vB), direction=DOWN, color=WHITE)
        val_b = Text("底 (Base)", font_size=24, color=GREEN).next_to(brace_b, DOWN, buff=0.1)
        
        # 畫出高 (虛線)
        line_h = DashedLine(vD, E, color=RED, stroke_width=4)
        brace_h = Brace(line_h, direction=LEFT, color=WHITE)
        val_h = Text("高 (Height)", font_size=24, color=RED).next_to(brace_h, LEFT, buff=0.1)

        self.play(FadeIn(brace_b), Write(val_b))
        self.play(Create(line_h), FadeIn(brace_h), Write(val_h))
        self.wait(1)

        # 準備割補法的碎片（用重疊取代原圖形以便切分）
        tri_left = Polygon(vA, E, vD, color=YELLOW, fill_opacity=0.6).set_stroke(width=0)
        pg_rest = Polygon(E, vB, vC, vD, color=BLUE_C, fill_opacity=0.6).set_stroke(width=0)
        
        # 無縫切換為碎拚圖
        self.add(tri_left, pg_rest)
        self.remove(pg_full)
        self.play(FadeIn(tri_left))
        # 淡出原本輔助看高的虛線，因為左邊已經變成純黃色直角三角形了
        self.play(FadeOut(line_h))
        self.wait(0.5)

        # 秀出互動引導文字
        txt1 = Text("將左側凸出的直角三角形「切下」", font_size=28).move_to(DOWN * 1.5)
        txt2 = Text("並「平移」到右側的缺口！", font_size=28, color=YELLOW).next_to(txt1, DOWN, buff=0.15)
        self.play(Write(txt1))
        self.play(Write(txt2))
        self.wait(0.5)

        # 移動左側三角形到右邊
        # 平移向量 = 底邊長度向量 = vB - vA
        shift_vec = vB - vA
        self.play(
            tri_left.animate.shift(shift_vec),
            run_time=2,
            path_arc=PI/6  # 小拋物線移動，增加動感
        )
        
        # 原本底邊長度是 vA 到 vB，新的底邊是 E 到 E + shift_vec
        new_brace_b = Brace(Line(E, E + shift_vec), direction=DOWN, color=WHITE)
        new_val_b = Text("底 (Base)", font_size=24, color=GREEN).next_to(new_brace_b, DOWN, buff=0.1)
        
        self.play(
            ReplacementTransform(brace_b, new_brace_b),
            ReplacementTransform(val_b, new_val_b)
        )
        # 用閃爍強調這是一塊拼圖
        self.play(Indicate(tri_left, color=GREEN), Indicate(pg_rest, color=GREEN))
        self.wait(1)

        # 清除舊說明，開始公式推導
        self.play(FadeOut(VGroup(txt1, txt2)))
        
        eq1 = Text("拼合後成為一個完美的「矩形」", font_size=32)
        eq2 = Text("平行四邊形面積 = 重組後的矩形面積", font_size=32)
        eq3 = Text("面積 = 底 × 高", font_size=42, color=YELLOW)
        
        eq_group = VGroup(eq1, eq2, eq3).arrange(DOWN, buff=0.3).move_to(DOWN * 2.5)
        box = SurroundingRectangle(eq_group, color=GREEN, buff=0.3)
        
        self.play(Write(eq1))
        self.wait(0.5)
        self.play(Write(eq2))
        self.wait(0.5)
        self.play(Write(eq3), Create(box))
        
        # 同步閃爍下方數值與這公式
        self.play(
            Indicate(new_val_b, color=YELLOW, scale_factor=1.2),
            Indicate(val_h, color=YELLOW, scale_factor=1.2),
            run_time=1.5
        )
        self.wait(3)
