# 📐 Manim 圖形範例撰寫指南（給協作夥伴）

## 你要做什麼？

幫忙寫 Manim 動畫程式碼，每個檔案 = **一個教學動畫**。
你寫好的 `.py` 會被自動吃進 RAG 知識庫，讓 AI 生成更好的圖形動畫。

---

## 環境準備

```bash
pip install manim
```

驗證安裝：
```bash
manim --version
```

---

## 檔案要放哪？

```
knowledge_base/
├── geometry/       ← 幾何圖形（三角形、圓、多邊形、座標幾何...）
├── algebra/        ← 代數（方程式、矩陣、函數圖...）
├── calculus/       ← 微積分（導數、積分、極限...）
├── arithmetic/     ← 算術（分數、加減乘除...）
└── statistics/     ← 統計（長條圖、圓餅圖、迴歸...）
```

**檔名規則**：`PascalCase`，用英文描述內容，例如 `TriangleCongruence.py`、`CircleAreaProof.py`

---

## 範例模板（直接抄改）

```python
from manim import *
import numpy as np  # 如果需要數學運算才加

class YourSceneName(Scene):
    """
    一句話描述這個動畫在教什麼。
    """
    def construct(self):
        # [VISUAL REASONING]
        # 1. Goal: 這個動畫的教學目標
        # 2. Layout: 物件的空間配置

        # --- 標題 ---
        title = Tex(r"你的標題").to_edge(UP)
        self.play(Write(title))

        # --- 主要圖形 ---
        # 建立圖形物件
        # ...

        # --- 標籤與註解 ---
        # 用 MathTex / Tex / Text 標記
        # ...

        # --- 動畫演示 ---
        # 變換、高亮、移動...
        # ...

        self.wait(2)
```

---

## 重要規則 ⚠️

### 必須遵守
1. **Class 必須繼承 `Scene`**（或 `ThreeDScene`），否則不會被 RAG 系統讀取
2. **加上 docstring**：描述動畫教學目標
3. **加上 `[VISUAL REASONING]` 註解**：寫清楚佈局邏輯
4. **程式碼必須能跑**：寫完請自己 render 驗證
   ```bash
   manim -pql YourFile.py YourSceneName
   ```
5. **一個檔案一個 Scene**（方便管理）

### 請避免
- ❌ 不要 `import` 奇怪的第三方套件（只用 `manim` 和 `numpy`）
- ❌ 不要寫太長（控制在 50–150 行內）
- ❌ 不要有 hardcode 的絕對路徑
- ❌ 不要用 `if __name__ == "__main__"`，不需要

---

## 我們缺什麼？（優先寫這些）

### 🔴 最缺：幾何圖形 (`geometry/`)
| 主題 | 範例建議 |
|------|---------|
| 三角形 | 全等判定（SSS/SAS/ASA）、外心內心重心、三角不等式 |
| 圓 | 圓與切線、弦切角、圓內接四邊形、扇形面積 |
| 多邊形 | 正多邊形內角和、多邊形面積分割 |
| 座標幾何 | 距離公式推導、中點公式、直線方程圖示 |
| 面積/體積 | 梯形面積、平行四邊形、棱柱/棱錐體積 |
| 變換 | 平移/旋轉/對稱/縮放的視覺化 |
| 3D 幾何 | 立方體展開圖、球體切面、三視圖 |

### 🟡 次要：其他
- `statistics/`：目前是空的，直方圖、盒鬚圖、常態分布都歡迎
- `calculus/`：黎曼和、旋轉體積、泰勒展開
- `algebra/`：二次函數頂點式、不等式圖示

---

## 常用 Manim API 速查

```python
# 基本圖形
Circle(radius=1, color=BLUE)
Square(side_length=2)
Triangle()
Polygon(p1, p2, p3, ...)
Line(start, end)
Arrow(start, end)
DashedLine(start, end)
Dot(point)
Arc(radius, start_angle, angle)
Angle(line1, line2)  # 角度標示

# 文字
Text("中文也行")
Tex(r"LaTeX 公式 $x^2$")
MathTex(r"a^2 + b^2 = c^2")

# 標註
Brace(mobject, direction=DOWN)
brace.get_text("label")

# 座標系
Axes(x_range=[...], y_range=[...])
NumberPlane()
axes.plot(lambda x: np.sin(x))

# 動畫
Create(mobject)           # 描邊出現
Write(mobject)            # 書寫出現
FadeIn(mobject)           # 淡入
GrowFromCenter(mobject)   # 從中心長出
Transform(old, new)       # 變形
ReplacementTransform(old, new)
mob.animate.shift(RIGHT)  # 移動
mob.animate.set_color(RED)
mob.animate.scale(2)

# 分組
VGroup(a, b, c)
group.arrange(RIGHT, buff=0.5)

# 位置
mob.to_edge(UP)
mob.to_corner(UL)
mob.next_to(other, DOWN)
mob.move_to(ORIGIN)
mob.shift(RIGHT * 2)

# 3D（繼承 ThreeDScene）
Surface(lambda u, v: ..., u_range, v_range)
self.set_camera_orientation(phi=75*DEGREES, theta=-45*DEGREES)
```

---

## 驗證你的程式碼

```bash
# 快速低畫質預覽（推薦開發中用）
manim -pql YourFile.py YourSceneName

# 高畫質輸出
manim -pqh YourFile.py YourSceneName
```

**確認清單：**
- [ ] `manim -pql` 可以成功 render
- [ ] 動畫邏輯正確（標籤沒有重疊、物件沒超出畫面）
- [ ] Class 有 docstring
- [ ] 有 `[VISUAL REASONING]` 註解
- [ ] 檔案放在正確的資料夾

寫完把 `.py` 檔傳給我就好，我會統一 ingest 進 RAG 🚀
