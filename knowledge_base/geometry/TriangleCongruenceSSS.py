from manim import *
import numpy as np

class TriangleCongruenceSSS(Scene):
    """
    展示兩個三角形 SSS (Side-Side-Side) 全等判定的動畫，包含頂點標記、對應關係強調與延伸測驗。
    """
    def construct(self):
        # [VISUAL REASONING]
        # 1. Goal: 透過頂點標記、等長撇號與邏輯條件證明 SSS 全等。
        # 2. Layout: 
        #    - 上方顯示文字解說，下方推導過程。
        #    - 加入頂點對應順序的閃爍強調 (Tex 分離字串技術)。
        #    - 結尾加入 SSA 與 AAA 的反例測驗，加深概念。

        # 可以用 self.add_sound("bgm.mp3") 加入背景輕快音樂！但這裡先純渲染動畫。

        # --- 1. 標題與基礎建設 ---
        title = Text("SSS 三角形全等判定", font_size=40, t2c={"SSS": RED, "全等": GREEN}).to_edge(UP, buff=0.2)
        subtitle = Text("若三個「對應邊」皆等長，則兩個三角形完全一樣", font_size=28, color=YELLOW).next_to(title, DOWN, buff=0.15)
        self.play(Write(title), Write(subtitle))

        v1, v2, v3 = np.array([-1, 1, 0]), np.array([-2, -1, 0]), np.array([1.5, -1, 0])

        tri_a = Polygon(v1, v2, v3, color=BLUE, fill_opacity=0.2).shift(LEFT * 3 + UP * 0.5)
        tri_b = Polygon(v1, v2, v3, color=GREEN, fill_opacity=0.2).shift(RIGHT * 3 + UP * 0.5).rotate(-PI/6)

        # 頂點標籤 (A,B,C) 與 (D,E,F)
        labels_a = VGroup(
            MathTex(r"A").next_to(tri_a.get_vertices()[0], UP, buff=0.1),
            MathTex(r"B").next_to(tri_a.get_vertices()[1], DL, buff=0.1),
            MathTex(r"C").next_to(tri_a.get_vertices()[2], DR, buff=0.1)
        )
        labels_b = VGroup(
            MathTex(r"D").next_to(tri_b.get_vertices()[0], UP, buff=0.1),
            MathTex(r"E").next_to(tri_b.get_vertices()[1], DL, buff=0.1),
            MathTex(r"F").next_to(tri_b.get_vertices()[2], DR, buff=0.1)
        )
        self.play(Create(tri_a), Write(labels_a), Create(tri_b), Write(labels_b))

        # --- 2. 邊長高亮與邏輯證明 ---
        colors = [RED, YELLOW, PURPLE]
        va, vb = tri_a.get_vertices(), tri_b.get_vertices()
        edges_a, edges_b, ticks_a, ticks_b = [], [], VGroup(), VGroup()
        
        conditions = VGroup(
            MathTex(r"\because \overline{AB} = \overline{DE}", color=RED),
            MathTex(r"\quad \overline{BC} = \overline{EF}", color=YELLOW),
            MathTex(r"\quad \overline{AC} = \overline{DF}", color=PURPLE)
        ).arrange(RIGHT, buff=0.5).to_edge(DOWN, buff=1.5)
        
        for i in range(3):
            ea = Line(va[i], va[(i+1)%3], color=colors[i], stroke_width=6)
            eb = Line(vb[i], vb[(i+1)%3], color=colors[i], stroke_width=6)
            edges_a.append(ea); edges_b.append(eb)
            
            # 製作撇號 (Tick Marks)
            def make_ticks(l, n):
                c, ang = l.get_center(), l.get_angle() + PI/2
                tks = VGroup()
                offs = np.linspace(-0.08*(n-1), 0.08*(n-1), n) if n > 1 else [0]
                v = np.array([np.cos(l.get_angle()), np.sin(l.get_angle()), 0])
                for off in offs:
                    tks.add(Line(UP, DOWN).scale(0.12).set_angle(ang).move_to(c + v*off).set_color(WHITE))
                return tks

            ta, tb = make_ticks(ea, i+1), make_ticks(eb, i+1)
            ticks_a.add(ta); ticks_b.add(tb)

            self.play(Create(ea), Create(eb), Write(ta), Write(tb), Write(conditions[i]), run_time=0.8)
        self.wait(0.5)

        # --- 3. 疊合動畫與頂點對應 ---
        target_tri = tri_a.copy().set_color(GREEN).set_fill(opacity=0.6)
        target_labels = labels_a.copy().set_color(GREEN)
        
        subtitle_2 = Text("三角形支架最穩固：三邊長一固定，形狀就唯一確定！", font_size=26, color=YELLOW).move_to(subtitle)
        self.play(ReplacementTransform(subtitle, subtitle_2))
        
        self.play(
            Transform(tri_b, target_tri), Transform(labels_b, target_labels),
            FadeOut(ticks_b), FadeOut(VGroup(*edges_b)), run_time=2, path_arc=PI/4
        )
        self.play(Indicate(tri_b, color=YELLOW))
        
        # 拆解寫入全等結論，方便針對個別字母閃爍
        conc = MathTex(
            r"\therefore \triangle ", "A", "B", "C", 
            r" \cong \triangle ", "D", "E", "F", 
            r" \text{ (SSS)}"
        )
        desc = Text("符號 ≅ 代表形狀與大小完全相同（全等）", font_size=24, color=GREY).next_to(conc, DOWN)
        conc_grp = VGroup(conc, desc).next_to(conditions, DOWN, buff=0.2)
        
        self.play(Write(conc), Write(desc))
        
        # 閃爍強調頂點對應順序
        for idx in range(3):
            self.play(
                Indicate(labels_a[idx], color=YELLOW, scale_factor=1.5),
                Indicate(labels_b[idx], color=YELLOW, scale_factor=1.5),
                Indicate(conc[idx+1], color=YELLOW, scale_factor=1.5), # A, B, C
                Indicate(conc[idx+5], color=YELLOW, scale_factor=1.5), # D, E, F
                run_time=0.8
            )
            
        sum_txt = Text("結論：只要三組對應邊相等，兩個三角形就一模一樣！", font_size=32, color=GREEN).to_edge(DOWN)
        self.play(ReplacementTransform(conc_grp, sum_txt), FadeOut(conditions))
        self.wait(3)


