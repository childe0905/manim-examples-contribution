# 📋 Manim 圖形範例 — 工作分配表

> **目標**：3 個人在 **一週內** 各產出 **6–8 個** 高品質 Manim 動畫腳本（共約 20 個）
> **截止日**：2026/03/27（四）
> **格式要求**：請務必先讀 [`CONTRIBUTOR_GUIDE.md`](file:///Users/liaozhenting/Desktop/LLManim_Agent/knowledge_base/CONTRIBUTOR_GUIDE.md)

---

## 現況分析

| 資料夾 | 現有數量 | 覆蓋度 | 急迫度 |
|--------|---------|--------|--------|
| `geometry/` | 13 個 | 偏基礎，缺三角形進階、圓進階、3D、座標幾何 | 🔴 最急 |
| `statistics/` | 0 個 | 完全空白 | 🔴 最急 |
| `calculus/` | 4 個 | 有切線、梯度下降、傅立葉，缺黎曼和/積分面積 | 🟡 |
| `algebra/` | 10 個 | 相對充足 | 🟢 |
| `arithmetic/` | 6 個 | 相對充足 | 🟢 |

---

## 👤 成員 A — 三角形 & 多邊形專家

> **負責資料夾**：`geometry/`
> **產出目標**：6–8 個 `.py` 檔

### 必做（6 個）

| # | 檔名建議 | 內容描述 | 難度 | 預估行數 |
|---|---------|---------|------|---------|
| A1 | `TriangleCongruenceSSS.py` | 三角形全等判定 SSS：建兩個三角形，逐邊高亮對應相等邊，最後疊合 | ⭐⭐ | 60–80 |
| A2 | `TriangleCongruenceSAS.py` | SAS 全等：高亮兩邊一夾角，旋轉平移使兩三角形重合 | ⭐⭐ | 60–80 |
| A3 | `TriangleCenters.py` | 展示外心、內心、重心的位置：畫三角形 → 逐一畫出三條中線/角平分線/垂直平分線 → 標示交點 | ⭐⭐⭐ | 100–130 |
| A4 | `PolygonInteriorAngles.py` | 正多邊形內角和公式 `(n-2)×180°`：從三角形到六邊形，分割對角線展示三角形數量 | ⭐⭐ | 70–90 |
| A5 | `ParallelogramArea.py` | 平行四邊形面積 = 底 × 高：剪一角拼成矩形的動畫變換 | ⭐⭐ | 60–80 |
| A6 | `TrapezoidArea.py` | 梯形面積公式推導：兩個相同梯形拼成平行四邊形 | ⭐⭐ | 60–80 |

### 加分（選做 2 個）

| # | 檔名建議 | 內容描述 | 難度 |
|---|---------|---------|------|
| A7 | `TriangleInequality.py` | 三角不等式視覺化：拖動邊長滑桿展示何時能/不能構成三角形 | ⭐⭐⭐ |
| A8 | `ExteriorAngleTheorem.py` | 外角定理：外角 = 兩個不相鄰內角之和 | ⭐⭐ |

### 技術提示
```python
# 建三角形常用
triangle = Polygon(
    np.array([-2, -1, 0]),
    np.array([2, -1, 0]),
    np.array([0, 2, 0]),
    color=BLUE, fill_opacity=0.2
)

# 重心 = 三頂點座標平均
centroid = (v1 + v2 + v3) / 3

# 角度標記
angle = Angle(line1, line2, radius=0.5, color=YELLOW)
angle_label = MathTex(r"\alpha").move_to(angle.point_from_proportion(0.5))
```

---

## 👤 成員 B — 圓 & 座標幾何專家

> **負責資料夾**：`geometry/`
> **產出目標**：6–8 個 `.py` 檔

### 必做（6 個）

| # | 檔名建議 | 內容描述 | 難度 | 預估行數 |
|---|---------|---------|------|---------|
| B1 | `CircleTangentLine.py` | 圓的切線性質：過外點畫兩條切線，標示切線 ⊥ 半徑 | ⭐⭐ | 60–80 |
| B2 | `InscribedAngle.py` | 圓心角 vs 圓周角：同弧上的圓心角 = 2× 圓周角，動態展示 | ⭐⭐⭐ | 80–100 |
| B3 | `CircleAreaSectors.py` | 圓面積 = πr²：將圓切成越來越多扇形，排成近似矩形 | ⭐⭐⭐ | 90–120 |
| B4 | `DistanceFormula.py` | 座標平面上兩點距離公式推導：畫直角三角形 → 畢氏定理 → √((x₂-x₁)²+(y₂-y₁)²) | ⭐⭐ | 70–90 |
| B5 | `MidpointFormula.py` | 中點公式視覺化：兩點連線 → 標中點座標 → 展示公式 | ⭐⭐ | 50–70 |
| B6 | `LineEquationGraph.py` | 斜截式 y=mx+b：用滑桿改變 m 和 b，展示直線變化 | ⭐⭐⭐ | 80–100 |

### 加分（選做 2 個）

| # | 檔名建議 | 內容描述 | 難度 |
|---|---------|---------|------|
| B7 | `CyclicQuadrilateral.py` | 圓內接四邊形：對角互補的動態展示 | ⭐⭐⭐ |
| B8 | `ChordAngleTheorem.py` | 弦切角定理視覺化 | ⭐⭐⭐ |

### 技術提示
```python
# 圓上的點
def point_on_circle(center, radius, angle):
    return center + np.array([
        np.cos(angle) * radius,
        np.sin(angle) * radius,
        0
    ])

# 切線（垂直於半徑）
radius_vec = point - center
tangent_dir = np.array([-radius_vec[1], radius_vec[0], 0])
tangent_line = Line(point - tangent_dir, point + tangent_dir)

# 直角標記
right_angle = RightAngle(line1, line2, length=0.3, color=WHITE)

# NumberPlane 適合座標幾何
plane = NumberPlane(x_range=[-5,5], y_range=[-4,4])
```

---

## 👤 成員 C — 3D 幾何 & 統計圖表專家

> **負責資料夾**：`geometry/` + `statistics/`
> **產出目標**：6–8 個 `.py` 檔

### 必做 — 3D 幾何（3 個）

| # | 檔名建議 | 內容描述 | 難度 | 預估行數 |
|---|---------|---------|------|---------|
| C1 | `CubeNet.py` | 立方體展開圖：6 個正方形攤平 → 折回成立方體 | ⭐⭐⭐ | 100–130 |
| C2 | `PrismVolume.py` | 棱柱體積 = 底面積 × 高：動態展示底面積和高度標籤 | ⭐⭐ | 70–90 |
| C3 | `SphereCrossSection.py` | 球體切面：用平面切球，展示不同位置的圓形截面大小變化 | ⭐⭐⭐ | 90–120 |

### 必做 — 統計圖表（3 個）

| # | 檔名建議 | 內容描述 | 難度 | 預估行數 |
|---|---------|---------|------|---------|
| C4 | `BarChart.py` | 長條圖：用 `BarChart` 類別，逐條動畫出現，加標題和數值標籤 | ⭐⭐ | 50–70 |
| C5 | `Histogram.py` | 直方圖/頻率分佈：生成一組資料 → 畫出頻率分佈長條 → 加上平均數虛線 | ⭐⭐ | 60–80 |
| C6 | `NormalDistribution.py` | 常態分佈曲線：畫鐘形曲線 → 標示 μ、σ → 著色 68-95-99.7 區域 | ⭐⭐⭐ | 80–100 |

### 加分（選做 2 個）

| # | 檔名建議 | 內容描述 | 難度 |
|---|---------|---------|------|
| C7 | `BoxPlot.py` | 盒鬚圖：展示 Q1/Q2/Q3/IQR 的計算過程 | ⭐⭐⭐ |
| C8 | `PyramidVolume.py` | 棱錐體積 = ⅓ 底面積 × 高：三個棱錐拼成棱柱 | ⭐⭐⭐ |

### 技術提示
```python
# === 3D 場景 ===
class YourScene(ThreeDScene):
    def construct(self):
        self.set_camera_orientation(phi=75*DEGREES, theta=-45*DEGREES)

        # 3D 物件
        cube = Cube(side_length=2, fill_opacity=0.3)
        prism = Prism(dimensions=[2, 1, 3])
        sphere = Sphere(radius=1.5)
        surface = Surface(
            lambda u, v: np.array([u, v, u**2 + v**2]),
            u_range=[-2, 2], v_range=[-2, 2]
        )

        # 相機動畫
        self.begin_ambient_camera_rotation(rate=0.2)
        self.move_camera(phi=60*DEGREES, theta=30*DEGREES)

# === 統計圖表 ===
# BarChart
chart = BarChart(
    values=[3, 5, 2, 8, 4],
    bar_names=["A", "B", "C", "D", "E"],
    y_range=[0, 10, 2],
    bar_colors=[BLUE, GREEN, RED, YELLOW, PURPLE]
)

# 手動畫直方圖（用 Rectangle）
bars = VGroup()
for i, freq in enumerate(frequencies):
    bar = Rectangle(
        width=bin_width, height=freq * scale,
        color=BLUE, fill_opacity=0.6
    )
    bar.move_to(axes.c2p(bin_edges[i] + bin_width/2, freq/2))
    bars.add(bar)
```

---

## 📅 時程 & 交付流程

```
Day 1 (3/20 四)  環境設定 + 讀 CONTRIBUTOR_GUIDE.md + 各自完成第 1 個
Day 2-3          完成第 2–4 個（每完成一個就先傳出來確認能 render）
Day 4-5          完成第 5–6 個 + 加分題
Day 6 (3/26 三)  全部交付，統一 review
Day 7 (3/27 四)  修正 + ingest 進 RAG
```

### 交付方式
1. 每完成一個 `.py` 就先自己跑 `manim -pql YourFile.py YourSceneName` 確認能 render
2. 把 `.py` 檔傳給我（LINE / Git / 隨便），附上一張 render 截圖
3. 我統一 review 後放進 `knowledge_base/` 對應資料夾

### 命名規則
- 檔名：`PascalCase.py`（如 `TriangleCenters.py`）
- Class 名：跟檔名一樣（如 `class TriangleCenters(Scene):`）
- **不要用中文檔名**

---

## ⚡ 品質紅線（不符合就打回重做）

1. ❌ `manim -pql` 跑不過 → 打回
2. ❌ 沒有 docstring → 打回
3. ❌ 沒有 `[VISUAL REASONING]` 註解 → 打回
4. ❌ 物件超出畫面 / 標籤重疊 → 打回
5. ❌ 超過 150 行且沒有合理理由 → 打回

---

## ❓ FAQ

**Q: 我不會 Manim 怎麼辦？**
A: 先讀 `CONTRIBUTOR_GUIDE.md` 的 API 速查表，再看 `geometry/` 裡現有的範例，照著改就好。

**Q: 我不確定要做的題目的數學對不對？**
A: 先 Google 確認公式，重點是「動畫有教學效果」，不是寫論文。

**Q: 座標算不出來怎麼辦？**
A: 用 `numpy` 算。不確定的話，先在紙上畫草圖標座標，再轉成程式碼。

**Q: 3D 場景渲染很慢？**
A: 用 `-pql`（低畫質）開發，最後再用 `-pqh` 確認。3D 場景 render 確實比較久，正常。
