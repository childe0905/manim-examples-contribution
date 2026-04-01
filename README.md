# Manim Examples Contribution

這個專案用來收集高品質的 K12 Manim 教學動畫範例。所有範例都會進入 RAG 知識庫，幫助系統生成更穩定的數學動畫腳本。

---

## 第一步：下載專案與環境設定

**1. 下載專案**
```bash
git clone https://github.com/childe0905/manim-examples-contribution.git
cd manim-examples-contribution
```

**2. 安裝必要套件**
```bash
pip install manim
```

可選：建議使用虛擬環境
```bash
python -m venv venv
source venv/bin/activate
```

---

## 第二步：開始製作動畫

1. 先讀 `WORK_ASSIGNMENT.md`，確認你被分配到的題目。
2. 再讀 `CONTRIBUTOR_GUIDE.md`，確認格式規則與品質要求。
3. 到對應資料夾建立你的 `.py` 檔案。
4. 完成後先自己用 `manim -pql` 測試。

目前這一輪主要新增的資料夾：

- `fractions/`：分數 area model、條帶比較、局部填色
- `measurement/`：面積、周長、切割重組、格線面積
- `statistics/`：長條圖、直方圖、圓餅圖、盒鬚圖

> 測試指令：
> ```bash
> manim -pql YourFile.py YourSceneName
> ```

---

## 第三步：這一輪的重點

這次不是單純補更多幾何題，而是要補強系統較弱的視覺模式：

- 區域填色
- 面積切割與重組
- 規則排列的圖表區塊
- 同一單位的等分與比例對應

請優先讓圖形本身說話，不要把重心放在大量文字說明。

---

## 第四步：如何上傳

當你完成一個或多個檔案，且本機 render 成功後，再進行提交：

**1. 加入暫存區**
```bash
git add .
```

**2. Commit**
```bash
git commit -m "Add: complete FractionAdditionAreaModel example"
```

**3. Push**
```bash
git push origin main
```

如果遇到 `rejected`：
```bash
git pull --rebase
git push origin main
```

---

## 交付前自檢

- `manim -pql` 可以成功 render
- 檔名與 class 名一致
- 有 docstring
- 有 `[VISUAL REASONING]`
- 只有一個 `Scene`
- 沒有標籤重疊或圖形超出畫面
- 至少有一個清楚的填色區域

完成後把檔案 push 到 GitHub 即可。
