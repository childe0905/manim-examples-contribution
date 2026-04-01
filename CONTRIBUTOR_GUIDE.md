# Manim 圖形範例撰寫指南

## 你要做什麼？

幫忙寫 K12 教學用的 Manim 動畫程式碼。每個 `.py` 檔就是一個教學動畫，會被送進 RAG 知識庫，讓系統更會生成圖形教學腳本。

---

## 環境準備

```bash
pip install manim
manim --version
```

---

## 檔案要放哪？

```
knowledge_base/examples/
├── fractions/      ← 分數 area model、分數比較、單位分數
├── measurement/    ← 面積、周長、格線面積、切割重組
├── statistics/     ← 長條圖、直方圖、圓餅圖、盒鬚圖
├── geometry/       ← 幾何圖形與幾何性質
├── algebra/        ← 代數與函數圖
├── calculus/       ← 微積分
└── arithmetic/     ← 算術
```

**檔名規則**：使用 `PascalCase.py`，例如 `TriangleArea.py`、`BarChart.py`

---

## 範例模板

```python
from manim import *
import numpy as np

class YourSceneName(Scene):
    """
    一句話描述這個動畫的教學目標。
    """

    def construct(self):
        # [VISUAL REASONING]
        # 1. Goal: 這支動畫要教什麼
        # 2. Layout: 物件怎麼擺，觀眾視線怎麼走
        # 3. Highlight: 哪一塊區域或哪一個量要被強調

        title = Tex(r"Your Title").to_edge(UP)
        self.play(Write(title))

        # 建立主要圖形
        # ...

        # 加標籤
        # ...

        # 動畫演示
        # ...

        self.wait(2)
```

---

## 必須遵守

1. `class` 必須繼承 `Scene` 或 `ThreeDScene`
2. 要有 docstring，說明教學目標
3. 要有 `[VISUAL REASONING]` 註解
4. 一個檔案只放一個 `Scene`
5. 只能使用 `manim` 和 `numpy`
6. 寫完一定要自己驗證：
   ```bash
   manim -pql YourFile.py YourSceneName
   ```

---

## 這一輪的品質要求

這一輪的任務重點是補強區域型視覺表達，請盡量滿足以下條件：

1. 至少有一個明確的填色區域
2. 至少有一次區域高亮、變色、分割或重組
3. 圖形的比例與對齊要清楚，不要太依賴文字解釋
4. 優先使用簡單且可辨識的圖形：長方形、方格、三角形、圓、條帶、扇形

---

## 請避免

- 不要 `import` 第三方套件
- 不要寫互動滑桿
- 不要做多個案例切換
- 不要在一個檔案放第二個 Scene
- 不要把題目做成自由發揮的大專題
- 不要超過 150 行，合理範圍建議 50 到 110 行
- 不要使用 hardcoded 絕對路徑
- 不要加 `if __name__ == "__main__"`

---

## 避免題目做模糊

如果題目描述不夠明確，請遵守這些縮限規則：

1. 比較型題目只做一組固定數值
2. 圖表題請用固定的小型資料集
3. 面積題優先用基本圖形，不要自行升級成複雜不規則圖形
4. 座標題如果沒有特別要求，請以數格子與面積視覺化為主，不要做完整公式推導
5. 統計題重點是圖形與標示，不要求完整理論講解

---

## 目前最缺什麼？

### 最優先

- `fractions/`
  - 等值分數
  - 分數加減的 area model
  - 單位分數
  - 假分數與帶分數

- `measurement/`
  - 三角形面積
  - 複合圖形面積
  - 周長與面積比較
  - 格線面積
  - 圓面積切割重組

- `statistics/`
  - 長條圖
  - 直方圖
  - 圓餅圖
  - 盒鬚圖
  - 平均數視覺化

### 次優先

- `geometry/`：補轉換、對稱、切割證明
- `calculus/`：黎曼和、曲線下面積
- `algebra/`：函數轉換、二次函數

---

## 常用 Manim API 速查

```python
# 基本圖形
Circle(radius=1, color=BLUE, fill_opacity=0.5)
Rectangle(width=3, height=2, fill_opacity=0.5)
Square(side_length=2, fill_opacity=0.5)
Polygon(p1, p2, p3, ...)
Line(start, end)
DashedLine(start, end)
Dot(point)
Sector(outer_radius=2, angle=PI/3)

# 文字
Text("Label")
Tex(r"\frac{1}{2}")
MathTex(r"A = \frac{1}{2}bh")

# 分組與排列
VGroup(a, b, c)
group.arrange(RIGHT, buff=0.5)
group.arrange(DOWN, buff=0.4)

# 位置
mob.to_edge(UP)
mob.next_to(other, DOWN)
mob.move_to(ORIGIN)
mob.shift(RIGHT * 2)

# 座標系
Axes(x_range=[0, 10, 1], y_range=[0, 10, 1])
NumberPlane()

# 動畫
Create(mobject)
Write(mobject)
FadeIn(mobject)
Transform(old, new)
ReplacementTransform(old, new)
Indicate(mobject)
FadeToColor(mobject, YELLOW)
```

---

## 驗證你的程式碼

```bash
manim -pql YourFile.py YourSceneName
```

**確認清單：**

- [ ] `manim -pql` 可以成功 render
- [ ] 畫面內沒有標籤重疊
- [ ] 圖形沒有超出畫面
- [ ] class 名稱與檔名一致
- [ ] 有 docstring
- [ ] 有 `[VISUAL REASONING]`
- [ ] 有清楚的區域填色或高亮設計

寫完後直接提交到 GitHub。
