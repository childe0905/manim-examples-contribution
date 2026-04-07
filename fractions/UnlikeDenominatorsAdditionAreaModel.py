from manim import *

class UnlikeDenominatorsAdditionAreaModel(Scene):
    """
    展示異分母分數加法 1/2 + 1/3 = 5/6
    """

    def construct(self):
        # [VISUAL REASONING]
        # 1. Goal: 教授異分母加法 1/2 + 1/3 = 5/6
        # 2. Layout: 上中下三條等長（寬度6）的矩形條帶
        # 3. Highlight: 展示擴分（畫虛線1/6切割）後將下方與上方的色塊往下移動到結果區的過程拼湊出 5/6

        title = Text("異分母分數加法", font_size=40).to_edge(UP, buff=0.3)
        self.play(Write(title))

        bar_width = 6
        bar_height = 0.8
        
        # 建立上方條帶 1/2
        top_group = VGroup()
        for _ in range(2):
            rect = Rectangle(width=bar_width/2, height=bar_height, color=WHITE, stroke_width=2)
            top_group.add(rect)
        top_group.arrange(RIGHT, buff=0)
        
        # 建立中間條帶 1/3
        mid_group = VGroup()
        for _ in range(3):
            rect = Rectangle(width=bar_width/3, height=bar_height, color=WHITE, stroke_width=2)
            mid_group.add(rect)
        mid_group.arrange(RIGHT, buff=0)
        
        # 建立下方條帶 6 份 (總和)
        bot_group = VGroup()
        for _ in range(6):
            rect = Rectangle(width=bar_width/6, height=bar_height, color=WHITE, stroke_width=2)
            bot_group.add(rect)
        bot_group.arrange(RIGHT, buff=0)
        
        # 排列三者
        bars = VGroup(top_group, mid_group, bot_group).arrange(DOWN, buff=0.6).move_to(UP * 0.5)
        
        # 1. 顯示 1/2 + 1/3 的原貌
        self.play(Create(top_group), Create(mid_group))
        
        label_top = MathTex(r"\frac{1}{2}", font_size=48).next_to(top_group, LEFT, buff=0.5)
        label_mid = MathTex(r"\frac{1}{3}", font_size=48).next_to(mid_group, LEFT, buff=0.5)
        self.play(Write(label_top), Write(label_mid))

        self.play(
            top_group[0].animate.set_fill(BLUE, opacity=0.7),
            mid_group[0].animate.set_fill(GREEN, opacity=0.7)
        )
        self.wait(1)

        # 2. 通分並畫切分線
        # Top bar (1/2 -> 3/6): 畫2條線，將原有的2格皆切為3份 -> 總格變成6
        # Mid bar (1/3 -> 2/6): 畫3條線，將原有的3格皆切為2份 -> 總格變成6
        top_cuts = VGroup()
        cell_w = bar_width / 6
        start_x = top_group.get_left()[0]
        # 刀痕 x_pos: 1, 2, 4, 5
        for i in [1, 2, 4, 5]:
            x_pos = start_x + i * cell_w
            p_top = np.array([x_pos, top_group.get_top()[1], 0])
            p_bot = np.array([x_pos, top_group.get_bottom()[1], 0])
            line = DashedLine(p_top + UP * 0.1, p_bot + DOWN * 0.1, color=YELLOW, stroke_width=2)
            top_cuts.add(line)
            
        mid_cuts = VGroup()
        # 刀痕 x_pos: 1, 3, 5
        for i in [1, 3, 5]:
            x_pos = start_x + i * cell_w
            p_top = np.array([x_pos, mid_group.get_top()[1], 0])
            p_bot = np.array([x_pos, mid_group.get_bottom()[1], 0])
            line = DashedLine(p_top + UP * 0.1, p_bot + DOWN * 0.1, color=YELLOW, stroke_width=2)
            mid_cuts.add(line)
            
        self.play(Create(top_cuts), Create(mid_cuts), run_time=2)
        
        # 更新 Labels
        label_top_new = MathTex(r"\frac{3}{6}", font_size=48).move_to(label_top)
        label_mid_new = MathTex(r"\frac{2}{6}", font_size=48).move_to(label_mid)
        
        self.play(Transform(label_top, label_top_new), Transform(label_mid, label_mid_new))
        self.wait(1)

        # 3. 相加，將色塊移到最下方
        self.play(Create(bot_group))
        
        # 建立獨立的小色塊模擬掉落搬移 (3個BLUE 2個GREEN 的 1/6)
        moved_parts = VGroup()
        anims = []
        # 前 3 個 BLUE
        for i in range(3):
            rect = Rectangle(width=cell_w, height=bar_height, color=WHITE, stroke_width=2).set_fill(BLUE, opacity=0.7)
            # 將其移動到上方 top_group 內部剛好對應的位置建立
            rect.move_to(np.array([start_x + (i + 0.5) * cell_w, top_group.get_center()[1], 0]))
            moved_parts.add(rect)
            # 計畫移動到下方 bot_group
            anims.append(rect.animate.move_to(bot_group[i].get_center()))
            
        # 接著 2 個 GREEN
        for j in range(2):
            i = j + 3 # 移到 bot_group 的第 3, 4 格
            rect = Rectangle(width=cell_w, height=bar_height, color=WHITE, stroke_width=2).set_fill(GREEN, opacity=0.7)
            rect.move_to(np.array([start_x + (j + 0.5) * cell_w, mid_group.get_center()[1], 0]))
            moved_parts.add(rect)
            anims.append(rect.animate.move_to(bot_group[i].get_center()))

        self.add(moved_parts)
        # 隱藏原有的塗滿大色塊，因為它們已經被 moved_parts 覆蓋了 (看起來像從那裡直接拿出來)
        self.play(
            top_group[0].animate.set_fill(opacity=0),
            mid_group[0].animate.set_fill(opacity=0),
            run_time=0.1
        )
        
        self.play(*anims, run_time=2)
        self.wait(0.5)
        
        label_bot = MathTex(r"\frac{5}{6}", font_size=48).next_to(bot_group, LEFT, buff=0.5)
        self.play(Write(label_bot))
        self.wait(1)

        # 4. 結末算式
        eq_group = VGroup(
            MathTex(r"\frac{1}{2}", font_size=44),
            MathTex("+", font_size=44),
            MathTex(r"\frac{1}{3}", font_size=44),
            MathTex("=", font_size=44),
            MathTex(r"\frac{3}{6}", font_size=44),
            MathTex("+", font_size=44),
            MathTex(r"\frac{2}{6}", font_size=44),
            MathTex("=", font_size=44),
            MathTex(r"\frac{5}{6}", font_size=44, color=YELLOW)
        ).arrange(RIGHT, buff=0.3).next_to(bars, DOWN, buff=0.8)
        
        self.play(Write(eq_group))
        self.wait(2)
