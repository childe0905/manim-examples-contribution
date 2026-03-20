from manim import *
import re

# ==================== 視覺常數定義 (Visual Constants) ====================
# 與加法版本共用，確保視覺風格一致

ROW_SPACING = 0.5           # 垂直間距
CHAR_BUFF = 0.15            # 字符間距
DOT_SHIFT = DOWN * 0.1      # 小數點偏移
ANSWER_Y_OFFSET = -0.6      # 答案行偏移
BORROW_Y_OFFSET = 0.3       # 借位標記偏移
NUMBER_START_Y = 1.5        # 數字初始位置


class VerticalDecimalSubtractionGolden(Scene):
    """
    【RAG 黃金範例】直式小數減法（含借位顯示）
    Golden Example for Vertical Decimal Subtraction with Borrowing Visualization
    
    核心教學特點 (Core Pedagogical Features)：
    1. 借位視覺化 (Borrowing Visualization): 
       - 被借位的數字：劃掉並顯示減 1 後的新值
       - 當前位：標示 "+10" 表示借來的 10
    2. 顏色語義化 (Color Coding): 
       - BLUE: 原始數字
       - YELLOW: 高亮當前計算位
       - RED: 劃掉的被借位數字
       - GREEN: 最終答案
    3. 小數點對齊 (Decimal Alignment): 與加法相同的對齊邏輯
    
    適用場景 (Use Cases)：
    - 小學數學：整數/小數減法
    - 借位教學：明確顯示「向前一位借 10」的過程
    """

    def __init__(self, num1=52.34, num2=17.68, segments=None, subtitles=None, **kwargs):
        """
        初始化參數
        
        Args:
            num1: 被減數 (Minuend, must be >= num2)
            num2: 減數 (Subtrahend)
            segments: 時間軸分段
            subtitles: 字幕文本列表
        """
        self.num1 = num1
        self.num2 = num2
        
        if segments is None:
            est_steps = 12  # 減法通常需要更多步驟（借位動畫）
            self.segments = [2.0] * est_steps
        else:
            self.segments = segments

        if subtitles is None:
            self.subtitles = [""] * len(self.segments)
        else:
            self.subtitles = subtitles
            
        super().__init__(**kwargs)

    def setup(self):
        """場景初始設置：固定字幕區域"""
        self.subtitle_area = Text(
            "", 
            font_size=32, 
            font="PingFang TC", 
            color=WHITE
        ).to_edge(DOWN, buff=0.4)
        self.add(self.subtitle_area)

    def create_wrapped_subtitle(self, text):
        """處理字幕換行與寬度限制"""
        parts = re.split(r'([。！？])', text)
        sentences = []
        
        if len(parts) > 1:
            for i in range(0, len(parts) - 1, 2):
                s = (parts[i] + parts[i+1]).strip()
                if s: 
                    sentences.append(s)
            if len(parts) % 2 == 1 and parts[-1].strip():
                sentences.append(parts[-1].strip())
        elif parts and parts[0]:
            sentences.append(parts[0])
        else:
            sentences = [""]
        
        wrapped_text = "\n".join(sentences)
        new_sub = Text(
            wrapped_text, 
            font_size=32, 
            font="PingFang TC", 
            color=WHITE, 
            line_spacing=0.8
        ).to_edge(DOWN, buff=0.4)
        
        if new_sub.get_width() > self.camera.frame_width * 0.9:
            new_sub.scale_to_fit_width(self.camera.frame_width * 0.9)
        
        return new_sub

    def play_step(self, step_index, animation, min_duration=0.5):
        """同步播放動畫與字幕"""
        try:
            duration = self.segments[step_index]
            text = self.subtitles[step_index]
        except IndexError:
            duration = 2.0
            text = ""
        
        new_sub = self.create_wrapped_subtitle(text)
        run_time = min(duration, min_duration)
        
        if animation:
            self.play(
                animation, 
                self.subtitle_area.animate.become(new_sub), 
                run_time=run_time
            )
        else:
            self.play(
                self.subtitle_area.animate.become(new_sub), 
                run_time=run_time
            )
            
        wait_time = duration - run_time
        if wait_time > 0:
            self.wait(wait_time)

    def construct(self):
        # ==================== 1. 數據預處理 ====================
        s1, s2 = str(self.num1), str(self.num2)
        dec1 = len(s1.split('.')[1]) if '.' in s1 else 0
        dec2 = len(s2.split('.')[1]) if '.' in s2 else 0
        max_dec = max(dec1, dec2)
        
        fmt = f"{{:.{max_dec}f}}"
        str1 = fmt.format(self.num1)
        str2 = fmt.format(self.num2)
        
        max_len = max(len(str1), len(str2))
        str1 = str1.rjust(max_len)
        str2 = str2.rjust(max_len)

        # ==================== 2. 構建視覺物件 ====================
        # RAG學習點：需要將每個數字存儲為獨立物件，方便後續修改（借位時劃掉）
        
        # 建立數字 1 的字符群組（使用列表方便後續替換）
        mob1_chars = [MathTex(c, font_size=60, color=BLUE) for c in str1]
        mob1 = VGroup(*mob1_chars)
        mob1.arrange(RIGHT, buff=CHAR_BUFF)
        if '.' in str1: 
            mob1[str1.find('.')].shift(DOT_SHIFT)
        
        mob2_chars = [MathTex(c, font_size=60, color=BLUE) for c in str2]
        mob2 = VGroup(*mob2_chars)
        mob2.arrange(RIGHT, buff=CHAR_BUFF)
        if '.' in str2: 
            mob2[str2.find('.')].shift(DOT_SHIFT)
        
        mob1.move_to(UP * NUMBER_START_Y)
        mob2.next_to(mob1, DOWN, buff=ROW_SPACING)
        mob2.align_to(mob1, RIGHT)

        # 減號與橫線
        minus = MathTex("-", font_size=60).next_to(mob2, LEFT, buff=0.5)
        line = Line(
            start=minus.get_left() + LEFT*0.2, 
            end=mob2.get_right() + RIGHT*0.2
        ).next_to(mob2, DOWN, buff=0.2)

        # ==================== 3. 動畫流程 ====================
        
        # --- Step 0: 顯示題目 ---
        problem = MathTex(f"{self.num1} - {self.num2} = ?", font_size=48)
        self.play_step(0, Write(problem), min_duration=1.0)

        # --- Step 1: 轉為直式 ---
        self.play_step(1, 
            AnimationGroup(
                FadeOut(problem),
                FadeIn(mob1),
                FadeIn(mob2),
                Write(minus),
                Create(line)
            ), 
            min_duration=1.5
        )

        # --- Step 2: 小數點對齊提示 ---
        dot_idx = str1.find('.')
        if dot_idx != -1:
            dot_visual = mob1[dot_idx]
            dashed_line = DashedLine(
                start=dot_visual.get_top() + UP*0.5,
                end=dot_visual.get_bottom() + DOWN*2.5,
                color=YELLOW
            )
            self.play_step(2, Create(dashed_line), min_duration=1.0)
            self.play(FadeOut(dashed_line), run_time=0.5)
        else:
            self.play_step(2, None, min_duration=0.5)

        # ==================== 4. 核心邏輯：逐位計算與借位 ====================
        # RAG學習點：減法需要「向前借位」的邏輯
        
        ans_mobs = []
        borrow_mobs = []  # 存儲借位標記（+10）
        
        # 將字串轉為數字陣列，方便借位時修改
        digits1 = list(str1)
        digits2 = list(str2)
        
        indices = list(range(len(str1)))[::-1]
        step_counter = 3
        
        for i in indices:
            char1 = digits1[i]
            char2 = digits2[i]
            
            # 跳過前導空格
            if char1 == ' ' and char2 == ' ':
                continue
                
            # --- 情況 A: 小數點 ---
            if char1 == '.' or char2 == '.':
                dot_mob = MathTex(".", font_size=60, color=GREEN)
                target_x = mob1[i].get_center()[0]
                dot_mob.move_to([target_x, line.get_center()[1] + ANSWER_Y_OFFSET, 0])
                dot_mob.shift(DOT_SHIFT)
                
                self.play_step(step_counter, FadeIn(dot_mob, shift=UP*0.2), min_duration=0.5)
                ans_mobs.append(dot_mob)
                step_counter += 1
                continue

            # --- 情況 B: 數字減法 ---
            val1 = int(char1) if char1 != ' ' else 0
            val2 = int(char2) if char2 != ' ' else 0
            
            # RAG學習點：處理借位邏輯
            if val1 < val2:
                # 需要借位！
                # 1. 找到前一個非小數點、非空格的數字
                borrow_idx = i - 1
                while borrow_idx >= 0 and (digits1[borrow_idx] in ['.', ' '] or int(digits1[borrow_idx]) == 0):
                    borrow_idx -= 1
                
                if borrow_idx >= 0:
                    # 2. 劃掉被借位的數字
                    old_digit = int(digits1[borrow_idx])
                    new_digit = old_digit - 1
                    
                    # 視覺效果：劃掉舊數字
                    cross_line = Line(
                        start=mob1_chars[borrow_idx].get_corner(DL),
                        end=mob1_chars[borrow_idx].get_corner(UR),
                        color=RED,
                        stroke_width=3
                    )
                    
                    # 新數字（較小字體，顯示在旁邊）
                    new_digit_mob = MathTex(str(new_digit), font_size=40, color=RED)
                    new_digit_mob.next_to(mob1_chars[borrow_idx], UP+LEFT, buff=0.1)
                    
                    self.play_step(step_counter, 
                        AnimationGroup(
                            Create(cross_line),
                            Write(new_digit_mob)
                        ),
                        min_duration=1.0
                    )
                    step_counter += 1
                    
                    # 3. 在當前位標示 "+10"
                    borrow_label = MathTex("+10", font_size=32, color=YELLOW)
                    target_x = mob1[i].get_center()[0]
                    borrow_label.move_to([
                        target_x + 0.5, 
                        mob1.get_top()[1] + BORROW_Y_OFFSET, 
                        0
                    ])
                    self.play_step(step_counter, Write(borrow_label), min_duration=0.8)
                    borrow_mobs.append(borrow_label)
                    step_counter += 1
                    
                    # 更新數值（加 10）
                    val1 += 10
                    # 更新 digits1 以防連續借位
                    digits1[borrow_idx] = str(new_digit)
            
            # 計算結果
            result_digit = val1 - val2
            
            # 建立答案數字
            digit_mob = MathTex(str(result_digit), font_size=60, color=GREEN)
            
            if char1 != ' ':
                target_x = mob1[i].get_center()[0]
            else:
                target_x = mob1[i+1].get_center()[0] - 0.6
                
            digit_mob.move_to([target_x, line.get_center()[1] + ANSWER_Y_OFFSET, 0])
            
            self.play_step(step_counter, FadeIn(digit_mob, shift=UP*0.2), min_duration=0.8)
            step_counter += 1
            
            ans_mobs.append(digit_mob)

        # --- Step Final: 框出答案 ---
        ans_mobs.reverse()
        full_ans_group = VGroup(*ans_mobs)
        box = SurroundingRectangle(full_ans_group, color=GREEN, buff=0.15)
        self.play_step(step_counter, Create(box), min_duration=1.0)
        
        self.wait(2)


# ==================== 使用範例 ====================
# 渲染命令：
# manim -pql VerticalDecimalSubtraction.py VerticalDecimalSubtractionGolden
#
# 自訂參數：
# scene = VerticalDecimalSubtractionGolden(num1=100.5, num2=37.8)
