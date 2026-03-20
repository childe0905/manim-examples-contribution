# Manim Examples Contribution 🚀

這是一個用來收集高品質 Manim 圖形程式碼範例的專案。所有範例都會被送入 RAG 知識庫，讓 AI 生成更好的動畫腳本。

---

## 🛠️ 第一步：下載專案與環境設定

**1. 下載專案到你的電腦**
打開終端機 (Terminal / PowerShell)，執行：
```bash
git clone https://github.com/childe0905/manim-examples-contribution.git
cd manim-examples-contribution
```

**2. 安裝必要的套件**
```bash
pip install manim
```
*(可選：建議使用虛擬環境 `python -m venv venv`)*

---

## ✏️ 第二步：開始製作動畫

1. 打開 `WORK_ASSIGNMENT.md` 看看你被分配到的題目。
2. 打開 `CONTRIBUTOR_GUIDE.md`，把裡面的「程式碼模板」複製起來。
3. 到對應的資料夾（例如 `geometry/` 或 `algebra/`），建立你的 `.py` 檔案。
4. 開始寫程式碼！

> 💡 **測試你的動畫：**
> 在終端機執行以下指令預覽（`YourFile.py` 替換成你的檔名，`YourSceneName` 替換成你的類別名稱）：
> ```bash
> manim -pql YourFile.py YourSceneName
> ```

---

## 📤 第三步：如何上傳（繳交作業）

當你寫好一個或多個檔案，且在本機用 `manim -pql` 測試能成功渲染後，照著以下步驟上傳：

**1. 把所有改動加入暫存區**
```bash
git add .
```

**2. 寫下你做了什麼 (Commit)**
告訴大家你這次上傳了哪個範例：
```bash
git commit -m "Add: 完成 TriangleCongruence 範例"
```

**3. 推送到 GitHub (Push)**
```bash
git push origin main
```

*(如果推上去遇到衝突 `rejected`，請先執行 `git pull --rebase`，沒有問題後再做一次 `git push`)*

🎉 **完成！你的程式碼已經成功繳交了！**
