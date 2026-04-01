from manim import *
import numpy as np
from manim.utils.space_ops import line_intersection

class TriangleCenters(Scene):
    """
    展示三角形的三心（外心、內心、重心）的幾何建構過程。
    """
    def construct(self):
        # [VISUAL REASONING]
        # 1. Goal: 依序展示外心（中垂線）、內心（角平分線）、重心（中線）。
        # 2. Layout: 
        #    - 大三角形固定在畫面中央。
        #    - 上方顯示正在繪製的三心名稱與定義。
        #    - 畫出建構線，標示交點與特徵圓，再淡出以保持畫面整潔，過渡到下一個。

        title = Text("三角形的三心", font_size=40).to_edge(UP, buff=0.2)
        subtitle = Text("即將展示：外心、內心、重心", font_size=28, color=YELLOW).next_to(title, DOWN, buff=0.15)
        self.play(Write(title), Write(subtitle))

        # 定義一個銳角三角形，讓三心都在內部或合理範圍
        vA = np.array([0, 2.0, 0])
        vB = np.array([-3, -1.5, 0])
        vC = np.array([2.5, -1.5, 0])

        tri = Polygon(vA, vB, vC, color=WHITE, stroke_width=4)
        labels = VGroup(
            MathTex("A").next_to(vA, UP),
            MathTex("B").next_to(vB, DL),
            MathTex("C").next_to(vC, DR)
        )
        self.play(Create(tri), Write(labels))

        def get_intersect(p1, d1, p2, d2):
            return line_intersection([p1, p1+d1], [p2, p2+d2])

        def show_center(name, desc, lines, center_pt, curr_sub, circle=None):
            new_sub = Text(f"{name}: {desc}", font_size=28, color=YELLOW).move_to(curr_sub)
            self.play(ReplacementTransform(curr_sub, new_sub))
            
            self.play(*[Create(l) for l in lines], run_time=1.5)
            
            dot = Dot(center_pt, color=RED)
            lbl = Text(name, font_size=24, color=RED).next_to(dot, UR, buff=0.1)
            self.play(FadeIn(dot), Write(lbl))
            
            if circle is not None:
                self.play(Create(circle))
                self.wait(2)
                self.play(FadeOut(VGroup(*lines, dot, lbl, circle)))
            else:
                self.wait(2)
                self.play(FadeOut(VGroup(*lines, dot, lbl)))
            return new_sub

        # 計算線段向量與長度
        dAB, dBC, dCA = (vB-vA), (vC-vB), (vA-vC)
        midAB, midBC, midCA = (vA+vB)/2, (vB+vC)/2, (vC+vA)/2

        # --- 1. 外心 (Circumcenter) ---
        pAB = np.array([-dAB[1], dAB[0], 0]); pAB /= np.linalg.norm(pAB)
        pBC = np.array([-dBC[1], dBC[0], 0]); pBC /= np.linalg.norm(pBC)
        pCA = np.array([-dCA[1], dCA[0], 0]); pCA /= np.linalg.norm(pCA)
        
        circumcenter = get_intersect(midAB, pAB, midBC, pBC)
        cc_r = np.linalg.norm(circumcenter - vA)
        
        # 中垂線 (往兩側延伸)
        l1 = Line(midAB - pAB*3, midAB + pAB*3, color=BLUE_C, stroke_opacity=0.5)
        l2 = Line(midBC - pBC*3, midBC + pBC*3, color=BLUE_C, stroke_opacity=0.5)
        l3 = Line(midCA - pCA*3, midCA + pCA*3, color=BLUE_C, stroke_opacity=0.5)
        
        cc_circ = Circle(radius=cc_r, color=BLUE).move_to(circumcenter)
        subtitle = show_center("外心", "三邊「中垂線」的交點 (外接圓圓心)", [l1, l2, l3], circumcenter, subtitle, cc_circ)

        # --- 2. 內心 (Incenter) ---
        dirA = dAB/np.linalg.norm(dAB) - dCA/np.linalg.norm(dCA)
        dirB = dBC/np.linalg.norm(dBC) - dAB/np.linalg.norm(dAB)
        dirC = dCA/np.linalg.norm(dCA) - dBC/np.linalg.norm(dBC)
        
        incenter = get_intersect(vA, dirA, vB, dirB)
        in_r = abs(np.dot(incenter - vA, pAB))
        
        # 角平分線 (從頂點畫到對邊)
        intA = get_intersect(vA, dirA, vB, dBC)
        intB = get_intersect(vB, dirB, vC, dCA)
        intC = get_intersect(vC, dirC, vA, dAB)
        
        il1 = Line(vA, intA, color=GREEN_C, stroke_opacity=0.5)
        il2 = Line(vB, intB, color=GREEN_C, stroke_opacity=0.5)
        il3 = Line(vC, intC, color=GREEN_C, stroke_opacity=0.5)
        
        in_circ = Circle(radius=in_r, color=GREEN).move_to(incenter)
        subtitle = show_center("內心", "三個「角平分線」的交點 (內切圓圓心)", [il1, il2, il3], incenter, subtitle, in_circ)

        # --- 3. 重心 (Centroid) ---
        centroid = (vA + vB + vC) / 3
        
        ml1 = Line(vA, midBC, color=PURPLE_C, stroke_opacity=0.5)
        ml2 = Line(vB, midCA, color=PURPLE_C, stroke_opacity=0.5)
        ml3 = Line(vC, midAB, color=PURPLE_C, stroke_opacity=0.5)
        
        subtitle = show_center("重心", "三頂點到對邊「中點」的連線交點", [ml1, ml2, ml3], centroid, subtitle)

        # 結尾打完收工
        final_text = Text("三心各自代表三角形不同的完美對稱點！", font_size=32, color=GREEN).move_to(subtitle)
        self.play(ReplacementTransform(subtitle, final_text))
        self.wait(3)
