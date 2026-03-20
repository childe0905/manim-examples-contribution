from manim import *

class SineWaveConstruction(Scene):
    def construct(self):
        self.camera.background_color = "#1e1e1e"
        
        # 1. 佈局設定
        # 左側放單位圓,右側放坐標軸
        unit_circle_center = LEFT * 3
        radius = 1.5
        
        # 2. 創建單位圓系統
        circle = Circle(radius=radius, color=WHITE).move_to(unit_circle_center)
        # 圓心十字線
        circle_axes = VGroup(
            Line(LEFT*radius*1.2, RIGHT*radius*1.2),
            Line(DOWN*radius*1.2, UP*radius*1.2)
        ).move_to(unit_circle_center).set_stroke(width=1)
        
        # 3. 創建右側函數坐標系
        axes = Axes(
            x_range=[0, 2*PI + 0.5, PI/2],
            y_range=[-1.5, 1.5, 1],
            x_length=7,
            y_length=4,
            axis_config={"color": GREY},
            tips=False
        ).to_edge(RIGHT)
        
        # 添加坐標軸標籤
        x_label = axes.get_x_axis_label("x")
        y_label = axes.get_y_axis_label("\\sin(x)")
        
        # 4. 核心驅動器：角度 Theta
        theta = ValueTracker(0)
        
        # 5. 定義動態物件
        
        # A. 單位圓上的動點 P
        def get_circle_point():
            return circle.get_center() + np.array([
                np.cos(theta.get_value()) * radius,
                np.sin(theta.get_value()) * radius,
                0
            ])
            
        point_on_circle = always_redraw(lambda: Dot(
            point=get_circle_point(), 
            color=RED
        ))
        
        # B. 圓心到 P 的半徑向量
        radius_line = always_redraw(lambda: Line(
            circle.get_center(), 
            point_on_circle.get_center(), 
            color=YELLOW
        ))
        
        # C. 角度標示 (Arc)
        angle_arc = always_redraw(lambda: Arc(
            radius=0.4,
            start_angle=0,
            angle=theta.get_value(),
            color=ORANGE,
            arc_center=circle.get_center()
        ))
        
        # D. 函數圖像上的對應點 Q
        def get_graph_point():
            # x 軸對應角度值,y 軸對應 sin 值
            angle = theta.get_value()
            return axes.c2p(angle, np.sin(angle))
            
        point_on_graph = always_redraw(lambda: Dot(
            point=get_graph_point(),
            color=RED
        ))
        
        # E. 關鍵視覺化：投影連接線 (Projection Line)
        # 連接 P 和 Q,展示高度相等
        projection_line = always_redraw(lambda: DashedLine(
            start=point_on_circle.get_center(),
            end=point_on_graph.get_center(),
            color=BLUE_A,
            stroke_width=2
        ))
        
        # F. 軌跡生成 (Traced Path)
        # 注意：TracedPath 需要一個返回點座標的函數
        trace = TracedPath(point_on_graph.get_center, dissipating_time=None, stroke_color=RED, stroke_width=4)
        
        # 6. 動畫執行
        self.add(circle, circle_axes, axes, x_label, y_label)
        self.add(point_on_circle, radius_line, angle_arc)
        self.add(point_on_graph, projection_line, trace)
        
        # 播放 0 到 2pi 的過程
        self.play(theta.animate.set_value(2 * PI), run_time=6, rate_func=linear)
        self.wait()
