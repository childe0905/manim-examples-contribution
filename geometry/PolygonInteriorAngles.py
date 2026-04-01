from manim import *
import numpy as np

class PolygonInteriorAngles(Scene):
    """
    展示多邊形內角和公式的推導：透過對角線將 n 邊形切割成 (n-2) 個三角形。
    """
    def construct(self):
        # [VISUAL REASONING]
        # 1. Goal: 視覺化五邊形切割成 3 個三角形，推導內角和公式為 180*(n-2)。
        # 2. Layout: 
        #    - 將正五邊形置於畫面左側，利用旋轉確保基準頂點在正上方。
        #    - 右側依序出現推導文字，採用純 Text 避免 Latex 中文編譯失敗。
        #    - 動態填色三角形強調 (n-2) 的數量概念。

        title = Text("多邊形內角和公式", font_size=40, t2c={"內角和": GREEN}).to_edge(UP, buff=0.2)
        subtitle = Text("任何多邊形都能從單一頂點出發，被切割成多個三角形", font_size=24, color=YELLOW).next_to(title, DOWN, buff=0.15)
        self.play(Write(title), Write(subtitle))

        # 建立正五邊形並旋轉 PI/2 讓 vertex 0 精準在正上方
        pentagon = RegularPolygon(n=5, radius=2.5, color=WHITE).rotate(PI/2).shift(LEFT * 3 + DOWN * 0.5)
        self.play(Create(pentagon), run_time=1.5)
        
        # 取得頂點
        vertices = pentagon.get_vertices()
        if len(vertices) > 5:
            vertices = vertices[:5]
            
        v0 = vertices[0]
        
        # 標示基準頂點
        dot0 = Dot(v0, color=RED, radius=0.08)
        lbl0 = Text("出發頂點", font_size=20, color=RED).next_to(v0, LEFT, buff=0.15)
        self.play(FadeIn(dot0), Write(lbl0))
        
        # 從 v0 連接非相鄰頂點：v2, v3
        diag1 = DashedLine(v0, vertices[2], color=YELLOW, stroke_width=4)
        diag2 = DashedLine(v0, vertices[3], color=YELLOW, stroke_width=4)
        
        # 標示出 3 個三角形的物件
        colors = [RED, BLUE, GREEN]
        tris = VGroup()
        for i in range(3):
            t = Polygon(vertices[0], vertices[i+1], vertices[i+2], color=colors[i], fill_opacity=0.4).set_stroke(width=0)
            tris.add(t)
        
        # 準備右側文字說明
        txt1 = Text("以正五邊形為例：", font_size=30)
        txt2 = Text("發射對角線，可切出 3 個完全貼合的三角形", font_size=24)
        txt3 = Text("📝 這 3 個三角形內角剛好填滿了五邊形內角", font_size=20, color=GREY)
        txt4 = Text("內角和 = 180° × 3 個 = 540°", font_size=32, color=BLUE_B)
        txt5 = Text("也就是 180° × (5 - 2) = 540°", font_size=36, color=YELLOW)
        
        texts = VGroup(txt1, txt2, txt3, txt4, txt5).arrange(DOWN, buff=0.4, aligned_edge=LEFT).shift(RIGHT * 3 + DOWN * 0.3)

        self.play(Write(txt1))
        self.wait(0.5)
        
        # 依序飛出對角線與三角形
        self.play(Write(txt2))
        self.play(Create(diag1), Create(diag2), run_time=1.5)
        
        for i, tri in enumerate(tris):
            self.play(FadeIn(tri), run_time=0.5)
            center = tri.get_center()
            t_180 = Text("180°", font_size=24).move_to(center)
            self.play(Write(t_180), run_time=0.4)
            self.play(Indicate(tri, color=YELLOW), run_time=0.5)
        
        self.play(Write(txt3))
        self.wait(1)
        self.play(Write(txt4))
        self.wait(1)
        self.play(Write(txt5))
        self.wait(1.5)

        # 結論：推廣到 n 邊形
        conc1 = Text("推廣至任意 n 邊形：", font_size=32)
        conc2 = Text("內角和 = 180° × (n - 2)", font_size=40, color=GREEN)
        conc_grp = VGroup(conc1, conc2).arrange(DOWN, buff=0.4).move_to(texts)
        box = SurroundingRectangle(conc_grp, color=GREEN, buff=0.3)
        
        # 淡出詳細運算並給出最終總結公式
        self.play(
            FadeOut(texts), 
            ReplacementTransform(txt5.copy(), conc_grp), 
            Create(box),
            run_time=1.5
        )
        self.play(Indicate(conc_grp, color=GREEN, scale_factor=1.1))
        self.wait(3)
