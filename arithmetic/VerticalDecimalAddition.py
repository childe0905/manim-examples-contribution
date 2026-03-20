from manim import *
import re

# ==================== 視覺常數定義 (Visual Constants) ====================
# RAG學習點：提取魔術數字為語義化常數，提升代碼可讀性與可維護性

# 垂直間距：數字行之間的距離 (Vertical spacing between number rows)
ROW_SPACING = 0.5

# 字符間距：同一數字內各位數的間隔 (Character spacing within a number)
CHAR_BUFF = 0.15

# 小數點偏移：小數點視覺位置微調 (Decimal point visual adjustment)
DOT_SHIFT = DOWN * 0.1

# 答案行偏移：答案與橫線的垂直距離 (Answer row offset from horizontal line)
ANSWER_Y_OFFSET = -0.6

# 進位數字偏移：進位標記在數字上方的距離 (Carry digit vertical offset)
CARRY_Y_OFFSET = 0.3

# 數字初始位置：第一個數字的垂直位置 (Initial position of first number)
NUMBER_START_Y = 1.5


class VerticalDecimalAdditionGolden(Scene):
    """
    【RAG 黃金範例】直式小數加法（含進位顯示）
    Golden Example for Vertical Decimal Addition with Carry-over Visualization
    
    核心教學特點 (Core Pedagogical Features)：
    1. 小數點對齊 (Decimal Alignment): 使用虛線標示對齊基準
    2. 逐位計算 (Digit-by-Digit): 由右向左，符合數學計算邏輯
    3. 進位視覺化 (Carry Visualization): 紅色小字顯示進位數字
    4. 顏色語義化 (Color Coding): GREEN=答案, RED=進位, YELLOW=提示
    
    適用場景 (Use Cases)：
    - 小學數學：整數/小數加法
    - 任意精度：自動處理不同位數
    - 字幕同步：支援外部時間軸控制
    """

    def __init__(self, num1=19.95, num2=3.17, segments=None, subtitles=None, **kwargs):
        """
        初始化參數 (Initialization Parameters)
        
        Args:
            num1, num2: 加法運算元 (Operands for addition)
            segments: 時間軸分段 (Timeline segments for synchronization)
            subtitles: 字幕文本列表 (Subtitle text list)
        """
        self.num1 = num1
        self.num2 = num2
        
        # Fallback 機制：如果沒有外部劇本，使用預設時間分配
        if segments is None:
            est_steps = 10  # 題目 + 排列 + 線 + 多位計算 + 總結
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
            font="PingFang TC",  # 中文字體支援
            color=WHITE
        ).to_edge(DOWN, buff=0.4)
        self.add(self.subtitle_area)

    def create_wrapped_subtitle(self, text):
        """
        處理字幕換行與寬度限制
        RAG學習點：防止長字幕超出螢幕範圍
        """
        # 按標點符號分割句子
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
        
        # 自動縮放過寬的字幕
        if new_sub.get_width() > self.camera.frame_width * 0.9:
            new_sub.scale_to_fit_width(self.camera.frame_width * 0.9)
        
        return new_sub

    def play_step(self, step_index, animation, min_duration=0.5):
        """
        同步播放動畫與字幕
        
        NOTE: 在實際 JSON-driven 系統中，應替換為：
        - self.add_sound(audio_file)
        - self.play(animation)
        - self.wait(remaining_duration)
        """
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
        # ==================== 1. 數據預處理 (Data Preprocessing) ====================
        # RAG學習點：處理小數點對齊的核心邏輯
        
        # 將數字轉為字串並補零，確保小數點後位數一致
        s1, s2 = str(self.num1), str(self.num2)
        dec1 = len(s1.split('.')[1]) if '.' in s1 else 0
        dec2 = len(s2.split('.')[1]) if '.' in s2 else 0
        max_dec = max(dec1, dec2)
        
        # 統一格式化：例如 19.5 → 19.50（與 3.17 對齊）
        fmt = f"{{:.{max_dec}f}}"
        str1 = fmt.format(self.num1)
        str2 = fmt.format(self.num2)
        
        # 右對齊 padding：確保個位數對齊
        # +1 是為了留空間給可能的進位（例如 99+1=100）
        max_len = max(len(str1), len(str2)) + 1
        str1 = str1.rjust(max_len)  # 例如 "19.50" → " 19.50"
        str2 = str2.rjust(max_len)  # 例如 " 3.17"

        # ==================== 2. 構建視覺物件 (Visual Construction) ====================
        # RAG學習點：字符級 VGroup 實現精確對齊
        
        # 建立數字 1 的字符群組（每個字符獨立，方便後續定位）
        mob1 = VGroup(*[MathTex(c, font_size=60) for c in str1])
        mob1.arrange(RIGHT, buff=CHAR_BUFF)
        
        # 修正小數點位置（往下微移，避免與數字齊平）
        if '.' in str1: 
            mob1[str1.find('.')].shift(DOT_SHIFT)
        
        # 建立數字 2 的字符群組
        mob2 = VGroup(*[MathTex(c, font_size=60) for c in str2])
        mob2.arrange(RIGHT, buff=CHAR_BUFF)
        if '.' in str2: 
            mob2[str2.find('.')].shift(DOT_SHIFT)
        
        # 垂直排列：mob1 在上，mob2 在下
        mob1.move_to(UP * NUMBER_START_Y)
        mob2.next_to(mob1, DOWN, buff=ROW_SPACING)
        
        # RAG學習點：使用 align_to 確保「個位數對齊」（靠右對齊）
        mob2.align_to(mob1, RIGHT)

        # 加號與橫線
        plus = MathTex("+", font_size=60).next_to(mob2, LEFT, buff=0.5)
        line = Line(
            start=plus.get_left() + LEFT*0.2, 
            end=mob2.get_right() + RIGHT*0.2
        ).next_to(mob2, DOWN, buff=0.2)

        # ==================== 3. 動畫流程 (Animation Sequence) ====================
        
        # --- Step 0: 顯示題目（橫式表示法） ---
        problem = MathTex(f"{self.num1} + {self.num2} = ?", font_size=48)
        self.play_step(0, Write(problem), min_duration=1.0)

        # --- Step 1: 轉換為直式 ---
        self.play_step(1, 
            AnimationGroup(
                FadeOut(problem),
                FadeIn(mob1),
                FadeIn(mob2),
                Write(plus),
                Create(line)
            ), 
            min_duration=1.5
        )

        # --- Step 2: 小數點對齊提示（教學輔助線） ---
        # RAG學習點：使用虛線標示「為什麼要對齊」
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
            # 如果沒有小數點，跳過此步驟
            self.play_step(2, None, min_duration=0.5)

        # ==================== 4. 核心邏輯：逐位計算與進位 ====================
        # RAG學習點：由右向左遍歷，模擬手算過程
        
        ans_mobs = []  # 存儲答案的各位數字
        carry = 0      # 進位標記
        carry_mobs = []  # 存儲進位視覺物件（用於最後清除）
        
        # 反向索引（從字串末尾開始）
        indices = list(range(len(str1)))[::-1]
        step_counter = 3  # 從第3步開始接續
        
        for i in indices:
            char1 = str1[i]
            char2 = str2[i]
            
            # 跳過前導空格（但保留位置）
            if char1 == ' ' and char2 == ' ' and carry == 0:
                continue
                
            # --- 情況 A: 小數點直接複製 ---
            if char1 == '.' or char2 == '.':
                dot_mob = MathTex(".", font_size=60, color=GREEN)
                target_x = mob1[i].get_center()[0]
                dot_mob.move_to([target_x, line.get_center()[1] + ANSWER_Y_OFFSET, 0])
                dot_mob.shift(DOT_SHIFT)
                
                self.play_step(step_counter, FadeIn(dot_mob, shift=UP*0.2), min_duration=0.5)
                ans_mobs.append(dot_mob)
                step_counter += 1
                continue

            # --- 情況 B: 數字加法計算 ---
            val1 = int(char1) if char1 != ' ' else 0
            val2 = int(char2) if char2 != ' ' else 0
            
            # 計算當前位：原數字 + 進位
            total = val1 + val2 + carry
            current_digit = total % 10  # 個位數
            new_carry = total // 10     # 十位數（進位）
            
            # 建立答案數字（綠色標示正確結果）
            digit_mob = MathTex(str(current_digit), font_size=60, color=GREEN)
            
            # RAG學習點：使用上方數字的 x 座標定位，確保對齊
            if char1 != ' ':
                target_x = mob1[i].get_center()[0]
            else:
                # Fallback：如果上方是空格（進位導致的擴充），向左推算
                target_x = mob1[i+1].get_center()[0] - 0.6
                
            digit_mob.move_to([target_x, line.get_center()[1] + ANSWER_Y_OFFSET, 0])
            
            anims = [FadeIn(digit_mob, shift=UP*0.2)]
            
            # --- 處理進位視覺化 (Carry Visualization) ---
            # RAG學習點：進位數字用小紅字顯示在「下一位」的上方
            if new_carry > 0:
                carry_mob = MathTex(str(new_carry), font_size=36, color=RED)
                
                # 計算進位顯示位置（下一位的上方）
                if i > 0:
                    target_carry_x = mob1[i-1].get_center()[0]
                    
                    # 特殊處理：如果前一位是小數點，再往左跨一位
                    if i > 1 and str1[i-1] == '.':
                        target_carry_x = mob1[i-2].get_center()[0]
                    
                    carry_mob.move_to([
                        target_carry_x, 
                        mob1.get_top()[1] + CARRY_Y_OFFSET, 
                        0
                    ])
                    anims.append(Write(carry_mob))
                    carry_mobs.append(carry_mob)  # 記錄進位物件
            
            # 播放計算動畫
            self.play_step(step_counter, AnimationGroup(*anims), min_duration=0.8)
            step_counter += 1
            
            ans_mobs.append(digit_mob)
            carry = new_carry

        # --- Step Final: 框出最終答案（教學強調） ---
        # 反轉 ans_mobs 順序（因為我們是由右向左生成的）
        ans_mobs.reverse()
        full_ans_group = VGroup(*ans_mobs)
        box = SurroundingRectangle(full_ans_group, color=GREEN, buff=0.15)
        self.play_step(step_counter, Create(box), min_duration=1.0)
        
        self.wait(2)


# ==================== 使用範例 (Usage Example) ====================
# 渲染命令：
# manim -pql VerticalDecimalAddition.py VerticalDecimalAdditionGolden
#
# 自訂參數：
# 在 Scene 中使用：scene = VerticalDecimalAdditionGolden(num1=123.45, num2=67.89)
