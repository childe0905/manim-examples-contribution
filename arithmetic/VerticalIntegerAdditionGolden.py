from manim import *

class CorrectVerticalAddition(Scene):
    """
    完美示範：5304 + 3538 的直式加法
    Perfect Demo: Vertical Addition with Carry Visualization
    
    這是一個「黃金標準」範例，展示：
    1. 字符級 VGroup 拆分
    2. 右對齊 (align_to RIGHT)
    3. 逐位計算（從右到左）
    4. 進位視覺化（紅色小字）
    """
    
    def construct(self):
        # ==================== 場景設置 ====================
        self.camera.background_color = BLACK
        
        # 標題（正確的 buff）
        title = Text("整數加法：5304 + 3538", font_size=36, color=WHITE)
        title.to_edge(UP, buff=0.5)  # ✅ 正確：buff=0.5
        self.add(title)
        
        # ==================== 數字拆分與對齊 ====================
        # ✅ 關鍵技術：字符級 VGroup
        str1 = "5304"
        str2 = "3538"
        
        # 建立第一個數字（每個字符是獨立的 MathTex）
        mob1 = VGroup(*[MathTex(c, font_size=60, color=BLUE) for c in str1])
        mob1.arrange(RIGHT, buff=0.2)
        
        # 建立第二個數字
        mob2 = VGroup(*[MathTex(c, font_size=60, color=BLUE) for c in str2])
        mob2.arrange(RIGHT, buff=0.2)
        
        # ✅ 關鍵技術：垂直堆疊 + 右對齊
        mob1.move_to(UP * 1.0)
        mob2.next_to(mob1, DOWN, buff=0.5)
        mob2.align_to(mob1, RIGHT)  # 個位數對齊
        
        # 加號（在第二個數字的左側）
        plus_sign = MathTex("+", font_size=60, color=BLUE)
        plus_sign.next_to(mob2, LEFT, buff=0.3)
        
        # 橫線
        line = Line(
            start=plus_sign.get_left() + LEFT * 0.2,
            end=mob2.get_right() + RIGHT * 0.2,
            color=WHITE
        )
        line.next_to(mob2, DOWN, buff=0.2)
        
        # ==================== 動畫：顯示題目 ====================
        self.play(
            FadeIn(mob1),
            FadeIn(mob2),
            Write(plus_sign),
            Create(line),
            run_time=2
        )
        self.wait(1)
        
        # ==================== 逐位計算（從右到左）====================
        ans_mobs = []  # 存儲答案的各位數字
        carry = 0      # 進位
        carry_mobs = []  # 進位視覺物件
        
        # 從右到左遍歷
        for i in reversed(range(len(str1))):
            # 獲取當前位的數字
            val1 = int(str1[i])
            val2 = int(str2[i])
            
            # 高亮當前計算的兩個數字
            self.play(
                Circumscribe(mob1[i], color=YELLOW),
                Circumscribe(mob2[i], color=YELLOW),
                run_time=0.8
            )
            
            # 計算總和
            total = val1 + val2 + carry
            current_digit = total % 10  # 個位數
            new_carry = total // 10     # 進位
            
            # 建立答案數字（綠色）
            digit_mob = MathTex(str(current_digit), font_size=60, color=GREEN)
            
            # 定位：使用上方數字的 x 座標
            target_x = mob1[i].get_center()[0]
            digit_mob.move_to([target_x, line.get_center()[1] - 0.6, 0])
            
            # 顯示答案數字
            self.play(FadeIn(digit_mob, shift=UP * 0.2), run_time=0.6)
            ans_mobs.append(digit_mob)
            
            # 如果有進位，顯示紅色小字
            if new_carry > 0:
                carry_mob = MathTex(str(new_carry), font_size=36, color=RED)
                
                # 進位顯示在「下一位」的上方
                if i > 0:
                    next_x = mob1[i - 1].get_center()[0]
                    carry_mob.move_to([next_x, mob1.get_top()[1] + 0.3, 0])
                    
                    self.play(Write(carry_mob), run_time=0.5)
                    carry_mobs.append(carry_mob)
            
            carry = new_carry
            self.wait(0.5)
        
        # ==================== 最終：框出答案 ====================
        ans_mobs.reverse()  # 反轉順序（因為我們是從右到左生成的）
        full_answer = VGroup(*ans_mobs)
        answer_box = SurroundingRectangle(full_answer, color=GREEN, buff=0.15)
        
        self.play(Create(answer_box), run_time=1)
        self.wait(2)


# ==================== 使用說明 ====================
# 渲染這個場景：
# manim -pql stable_outputs/整數加法：5304_+_3538.py CorrectVerticalAddition
#
# 或者直接在終端機執行：
# manim -pql correct_vertical_addition_demo.py CorrectVerticalAddition
