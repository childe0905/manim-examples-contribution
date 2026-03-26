from manim import *
import numpy as np


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


class LineEquationGraph(Scene):
    """
    直線方程式與幾何圖形：
    展示 y = mx + c 的圖形，利用 ValueTracker 動態展示
    m (斜率) 和 c (y截距) 對圖形的影響。
    """

    def construct(self):
        # [VISUAL REASONING]
        # 1. Goal: 讓學生直觀看到 y=mx+c 中，c 控制上下平移，m 控制傾斜度。
        # 2. Layout:
        #    - 座標系 (NumberPlane) 置中，範圍涵蓋整個畫面。
        #    - 公式框放在左上角（或不受直線干擾的角落）。
        #    - 使用 ValueTracker 儲存 m 和 c 的即時數值。
        #    - always_redraw 自動更新直線、公式文字與 y 截距點。

        # --- 1. 建立座標系 ---
        plane = NumberPlane(
            x_range=[-7, 7, 1],
            y_range=[-4, 4, 1],
            background_line_style={"stroke_opacity": 0.4}
        )
        axes_labels = plane.get_axis_labels(x_label="x", y_label="y")
        self.play(DrawBorderThenFill(plane), Write(axes_labels))
        self.wait(0.5)

        # --- 2. 設定動態變數 (ValueTracker) ---
        tracker_m = ValueTracker(1.0)
        tracker_c = ValueTracker(0.0)

        # --- 3. 繪製動態直線 ---
        # 根據 m 和 c，畫出跨越畫面的直線
        line = always_redraw(
            lambda: plane.plot(
                lambda x: tracker_m.get_value() * x + tracker_c.get_value(),
                color=YELLOW, stroke_width=4
            )
        )

        # --- 4. 繪製 y 截距點與標籤 ---
        # 標示 (0, c) 的位置
        intercept_dot = always_redraw(
            lambda: Dot(
                plane.c2p(0, tracker_c.get_value()), 
                color=RED, radius=0.08
            )
        )
        
        # 截距座標文字
        intercept_label = always_redraw(
            lambda: Text(
                f"(0, {tracker_c.get_value():.1f})", 
                font_size=18, color=RED
            ).next_to(intercept_dot.get_center(), DR, buff=0.1)
        )

        # --- 5. 動態方程式說明框 ---
        # 放在畫面左上角
        def get_equation_text():
            m = tracker_m.get_value()
            c = tracker_c.get_value()
            # 格式化公式字串，處理正負號
            sign = "+" if c >= 0 else "-"
            # 當 m=1 或 m=-1 時，精簡顯示
            m_str = f"{m:.1f}"
            c_str = f"{abs(c):.1f}"
            return Text(
                f"y = {m_str}x {sign} {c_str}", 
                font_size=28, color=YELLOW
            )

        eq_text = always_redraw(lambda: get_equation_text().to_corner(UL, buff=0.5))
        
        # 參數說明面板
        panel_m = always_redraw(
            lambda: Text(f"斜率 m = {tracker_m.get_value():.1f}", font_size=24, color=WHITE)
                    .next_to(eq_text, DOWN, aligned_edge=LEFT, buff=0.2)
        )
        panel_c = always_redraw(
            lambda: Text(f"y截距 c = {tracker_c.get_value():.1f}", font_size=24, color=RED)
                    .next_to(panel_m, DOWN, aligned_edge=LEFT, buff=0.15)
        )

        # 初始繪製
        self.play(
            Create(line),
            FadeIn(intercept_dot), 
            Write(intercept_label),
            Write(eq_text),
            Write(panel_m),
            Write(panel_c)
        )
        self.wait(1)

        # --- overlaps 檢查（靜態時間點） ---
        # 確保資訊面板不會跟 y 軸標籤重疊
        assert not overlaps(eq_text, axes_labels), "方程式與座標軸標籤重疊！"

        # --- 6. 動畫展示 1：改變 y 截距 (c)，直線上下平移 ---
        # c: 0 -> 2 -> -3 -> 1
        self.play(tracker_c.animate.set_value(2.0), run_time=1.5)
        self.wait(0.5)
        self.play(tracker_c.animate.set_value(-3.0), run_time=2)
        self.wait(0.5)
        self.play(tracker_c.animate.set_value(1.0), run_time=1.5)
        self.wait(1)

        # --- 7. 動畫展示 2：改變斜率 (m)，直線旋轉 ---
        # m: 1 -> 3 -> -1 -> 0.5
        self.play(tracker_m.animate.set_value(3.0), run_time=1.5)
        self.wait(0.5)
        self.play(tracker_m.animate.set_value(-1.0), run_time=2)
        self.wait(0.5)
        self.play(tracker_m.animate.set_value(0.5), run_time=1.5)
        self.wait(2)
