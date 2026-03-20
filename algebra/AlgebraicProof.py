from manim import *

class AlgebraicProof(Scene):
    def construct(self):
        # 1. 參數設定
        # 設定 a 和 b 的長度比例,例如 3:1
        a = 3
        b = 1
        side_length = a + b
        
        # 2. 構建幾何區塊
        # 創建一個大正方形框架,之後隱藏或作為背景
        frame = Square(side_length=side_length, color=WHITE)
        
        # 區塊 1: a^2 (左上)
        square_a = Square(side_length=a, fill_color=BLUE_C, fill_opacity=0.6)
        square_a.align_to(frame, UL)
        
        # 區塊 2: b^2 (右下)
        square_b = Square(side_length=b, fill_color=RED_C, fill_opacity=0.6)
        square_b.align_to(frame, DR)
        
        # 區塊 3 & 4: ab (右上與左下)
        rect_ab1 = Rectangle(width=b, height=a, fill_color=GREEN_C, fill_opacity=0.6)
        rect_ab1.next_to(square_a, RIGHT, buff=0)
        
        rect_ab2 = Rectangle(width=a, height=b, fill_color=GREEN_C, fill_opacity=0.6)
        rect_ab2.next_to(square_a, DOWN, buff=0)
        
        # 組合所有區塊
        parts = VGroup(square_a, square_b, rect_ab1, rect_ab2)
        
        # 3. 添加邊長標註 (Braces)
        # 左側標註 a 和 b
        brace_left_a = Brace(square_a, LEFT)
        text_left_a = brace_left_a.get_text("a")
        
        brace_left_b = Brace(rect_ab2, LEFT)
        text_left_b = brace_left_b.get_text("b")
        
        # 上方標註 a 和 b
        brace_top_a = Brace(square_a, UP)
        text_top_a = brace_top_a.get_text("a")
        
        brace_top_b = Brace(rect_ab1, UP)
        text_top_b = brace_top_b.get_text("b")
        
        # 4. 添加面積文字
        tex_a2 = MathTex("a^2").move_to(square_a)
        tex_b2 = MathTex("b^2").move_to(square_b)
        tex_ab1 = MathTex("ab").move_to(rect_ab1)
        tex_ab2 = MathTex("ab").move_to(rect_ab2)
        
        # 5. 動畫序列
        # Step 1: 展示整體邊長 (a+b)
        total_brace = Brace(frame, LEFT)
        total_text = total_brace.get_text("a+b")
        
        self.play(Create(frame))
        self.play(FadeIn(total_brace), Write(total_text))
        self.wait(1)
        
        # Step 2: 分割展示
        self.play(
            ReplacementTransform(total_brace, VGroup(brace_left_a, brace_left_b)),
            ReplacementTransform(total_text, VGroup(text_left_a, text_left_b)),
            FadeIn(brace_top_a), Write(text_top_a),
            FadeIn(brace_top_b), Write(text_top_b)
        )
        
        # Step 3: 填充顏色並顯示各塊面積
        self.play(FadeIn(parts))
        self.play(Write(tex_a2), Write(tex_b2), Write(tex_ab1), Write(tex_ab2))
        self.wait(1)
        
        # Step 4: 公式推導 - 視覺化重組
        # 將圖形稍微左移,右側留出空間寫公式
        all_mobjects = VGroup(frame, parts, brace_left_a, text_left_a, brace_left_b, text_left_b, 
                             brace_top_a, text_top_a, brace_top_b, text_top_b, 
                             tex_a2, tex_b2, tex_ab1, tex_ab2)
        
        self.play(all_mobjects.animate.scale(0.8).to_edge(LEFT))
        
        # 初始公式
        eq1 = MathTex("(a+b)^2", "=", "?")
        eq1.to_edge(RIGHT).shift(LEFT)
        self.play(Write(eq1))
        self.wait()
        
        # 展開公式
        eq2 = MathTex("(a+b)^2", "=", "a^2", "+", "b^2", "+", "2ab")
        eq2.to_edge(RIGHT).shift(LEFT)
        
        # 關鍵動畫：將圖形中的面積文字 "飛" 到公式對應位置
        # 使用 TransformFromCopy 保留原圖形文字
        self.play(
            TransformMatchingTex(eq1, eq2, transform_mismatches=True),
            run_time=1
        )
        
        # 高亮強調：讓圖形中的區塊與公式中的項依序閃爍
        self.play(Indicate(square_a), Indicate(eq2[2]), run_time=1.5) # a^2
        self.play(Indicate(square_b), Indicate(eq2[4]), run_time=1.5) # b^2
        self.play(Indicate(VGroup(rect_ab1, rect_ab2)), Indicate(eq2[6]), run_time=1.5) # 2ab
        
        self.wait(2)
