from manim import *
import numpy as np

class ExteriorAngleTheorem(Scene):
    """
    展示外角定理：三角形的外角等於兩個內對角的和。
    過幾何扇形的複製與搬移完美吻合外角空間。
    """
    def construct(self):
        # [VISUAL REASONING]
        # 1. Goal: 視覺化證實 外角γ_ext = 內對角 α + β。
        # 2. Layout:
        #    - 使用堅實的平面座標：A=(-1, 1.5), B=(-3.5, -1), C=(0.5, -1)
        #    - 延伸 BC 形成平角外角。
        #    - 對 A 與 B 構造 Sector，作為彩色積木。
        #    - 將這兩塊 Sector 用 path_arc 的平滑曲線轉移到 C 上填滿外角！

        title = Text("外角定理", font_size=40, t2c={"外角定理": GREEN}).to_edge(UP, buff=0.2)
        subtitle = Text("三角形的任何一「外角」，必然等於兩個不相鄰的「內對角」和", font_size=28, color=YELLOW).next_to(title, DOWN, buff=0.15)
        self.play(Write(title), Write(subtitle))

        # 定義頂點
        vA = np.array([-1.0,  1.5, 0])
        vB = np.array([-3.5, -1.0, 0])
        vC = np.array([ 0.5, -1.0, 0])
        vD = np.array([ 3.5, -1.0, 0]) # 延長線末端

        # 計算每一個角的確切起點與大小，以符合 Sector 用法
        # angle_B (B點的內角): 夾於 BC (0度) 與 BA 之間
        angle_B = np.arctan2(vA[1]-vB[1], vA[0]-vB[0])  # ~45度
        
        # angle_A (A點的內角): 夾於 AB (-135度) 與 AC (-59度) 之間
        angle_AB = np.arctan2(vB[1]-vA[1], vB[0]-vA[0])
        angle_AC = np.arctan2(vC[1]-vA[1], vC[0]-vA[0])
        angle_A = angle_AC - angle_AB
        
        # 外角 (C點的外角): 夾於 CD (0度) 與 CA 之間
        angle_ext = np.arctan2(vA[1]-vC[1], vA[0]-vC[0])

        # 畫出基本圖形與連線
        line_BD = Line(vB, vD, color=WHITE, stroke_width=6)
        line_CA = Line(vC, vA, color=WHITE, stroke_width=6)
        line_AB = Line(vA, vB, color=WHITE, stroke_width=6)
        self.play(Create(line_BD), Create(line_CA), Create(line_AB))

        # 創造上方的內對角 alpha 與 beta
        r_A, r_B = 0.8, 0.8
        
        sector_A = Sector(start_angle=angle_AB, angle=angle_A, color=RED).set_fill(opacity=0.6).scale(r_A).shift(vA)
        lbl_A = Text("α", font_size=24).move_to(
            vA + r_A * 0.65 * np.array([np.cos(angle_AB + angle_A/2), np.sin(angle_AB + angle_A/2), 0])
        )
        group_A = VGroup(sector_A, lbl_A)

        sector_B = Sector(start_angle=0, angle=angle_B, color=BLUE).set_fill(opacity=0.6).scale(r_B).shift(vB)
        lbl_B = Text("β", font_size=24).move_to(
            vB + r_B * 0.65 * np.array([np.cos(angle_B/2), np.sin(angle_B/2), 0])
        )
        group_B = VGroup(sector_B, lbl_B)

        self.play(FadeIn(group_A), FadeIn(group_B))
        
        # 標示出目標外角
        arc_ext = Arc(arc_center=vC, radius=1.0, start_angle=0, angle=angle_ext, color=YELLOW, stroke_width=4)
        lbl_ext = Text("外角", font_size=24, color=YELLOW).next_to(vC + [1.1, 0.3, 0], RIGHT, buff=0.1)
        self.play(Create(arc_ext), Write(lbl_ext))
        self.wait(1)

        txt1 = Text("將兩個「內對角」平行搬移到「外角」的空間中", font_size=28).move_to(DOWN * 2.2)
        self.play(Write(txt1))

        # ====== 複製與位移動畫 ======
        # 定義移動後的最終目標 Sector
        # β 的目標：原封不動移動到 C (start_angle: 0, angle: angle_B)
        target_sector_B = Sector(start_angle=0, angle=angle_B, color=BLUE).set_fill(opacity=0.6).scale(r_B).shift(vC)
        target_lbl_B = Text("β", font_size=24).move_to(
            vC + r_B * 0.65 * np.array([np.cos(angle_B/2), np.sin(angle_B/2), 0])
        )
        target_grp_B = VGroup(target_sector_B, target_lbl_B)

        # α 的目標：放置在 β 的上方 (start_angle: angle_B, angle: angle_A)
        target_sector_A = Sector(start_angle=angle_B, angle=angle_A, color=RED).set_fill(opacity=0.6).scale(r_A).shift(vC)
        target_lbl_A = Text("α", font_size=24).move_to(
            vC + r_A * 0.65 * np.array([np.cos(angle_B + angle_A/2), np.sin(angle_B + angle_A/2), 0])
        )
        target_grp_A = VGroup(target_sector_A, target_lbl_A)

        # 抽出兩份複製物作為動畫執行本體
        moving_A = group_A.copy()
        moving_B = group_B.copy()

        # 開始飛行
        self.play(
            Transform(moving_B, target_grp_B, path_arc=-PI/6),
            run_time=2
        )
        self.play(
            Transform(moving_A, target_grp_A, path_arc=PI/3),
            run_time=2
        )
        self.wait(1)

        # 結論：剛好填滿
        txt2 = Text("一分不差，完美地填滿了這塊外角！", font_size=28, color=GREEN).move_to(txt1)
        self.play(FadeOut(txt1))
        self.play(Write(txt2))
        
        self.play(Indicate(moving_A), Indicate(moving_B), Indicate(lbl_ext))
        self.wait(1)

        eq1 = Text("故得出重要結論：", font_size=26)
        eq2 = Text("外角大小 = 內對角 α + 內對角 β", font_size=36, color=YELLOW)
        eq_group = VGroup(eq1, eq2).arrange(DOWN, buff=0.35).move_to(DOWN * 3.2)
        box = SurroundingRectangle(eq2, color=GREEN, buff=0.15)

        self.play(FadeIn(eq_group), Create(box))
        self.wait(3)
