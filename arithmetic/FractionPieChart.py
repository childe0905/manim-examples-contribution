from manim import *

class ElementaryFractionLesson(Scene):
    def construct(self):
        # 1. 場景初始化與標題
        # 使用深灰色背景,減少螢幕眩光,符合兒童護眼設計
        self.camera.background_color = "#2D3436"
        
        title = Text("認識分數：部分與整體的關係", font_size=40, weight=BOLD)
        title.to_edge(UP)
        self.play(Write(title))

        # 2. 定義數值驅動器
        # fraction_value 從 0 開始,將動態變化到 1
        fraction_value = ValueTracker(0)

        # 3. 創建圓形底圖 (代表整體 "1")
        # 使用虛線外框表示容器概念
        circle_outline = Circle(radius=2, color=WHITE, stroke_opacity=0.5, stroke_width=2)
        
        # 4. 創建動態扇形 (Sector)
        # 使用 always_redraw 確保扇形隨數值實時變化
        pie_slice = always_redraw(lambda: Sector(
            radius=2,
            start_angle=90 * DEGREES, # 從正上方 12 點鐘方向開始
            angle=-360 * DEGREES * fraction_value.get_value(), # 負號代表順時針方向
            color=BLUE_E,
            fill_opacity=0.8
        ))

        # 5. 創建動態標籤系統
        # 標籤 1: 顯示百分比 (例如 25.0%)
        percent_label = always_redraw(lambda: DecimalNumber(
            fraction_value.get_value() * 100,
            unit="\\%",
            num_decimal_places=1,
            color=YELLOW,
            font_size=36
        ).next_to(pie_slice, DOWN, buff=0.5))

        # 標籤 2: 顯示分數 (例如 1/4)
        # 這裡需要根據數值動態切換 LaTeX 字串,展示特定分數點
        def get_fraction_tex():
            val = fraction_value.get_value()
            # 利用 numpy 的 isclose 處理浮點數精度問題
            if np.isclose(val, 0.25, atol=0.01):
                return MathTex(r"\\frac{1}{4}", font_size=48)
            elif np.isclose(val, 0.5, atol=0.01):
                return MathTex(r"\\frac{1}{2}", font_size=48)
            elif np.isclose(val, 0.75, atol=0.01):
                return MathTex(r"\\frac{3}{4}", font_size=48)
            elif np.isclose(val, 1.0, atol=0.01):
                return MathTex(r"\\frac{4}{4} = 1", font_size=48)
            else:
                # 非特定分數時顯示小數
                return DecimalNumber(val, num_decimal_places=2, font_size=36)

        fraction_tex = always_redraw(lambda: get_fraction_tex().move_to(ORIGIN))

        # 6. 動畫編排
        self.add(circle_outline, pie_slice, percent_label, fraction_tex)
        
        # 階段演示：從 0 -> 1/4
        self.play(fraction_value.animate.set_value(0.25), run_time=2, rate_func=smooth)
        self.wait(0.5)
        
        # 從 1/4 -> 1/2
        self.play(fraction_value.animate.set_value(0.5), run_time=2, rate_func=smooth)
        self.wait(0.5)
        
        # 從 1/2 -> 3/4
        self.play(fraction_value.animate.set_value(0.75), run_time=2, rate_func=smooth)
        self.wait(0.5)
        
        # 從 3/4 -> 1
        self.play(fraction_value.animate.set_value(1), run_time=2, rate_func=smooth)
        self.wait(1)

        # 額外演示：連續變化,強調分數的連續性
        self.play(fraction_value.animate.set_value(0), run_time=3, rate_func=linear)
