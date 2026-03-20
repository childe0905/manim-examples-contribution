"""
Manim 範例品質自動審核腳本
==========================
用法：
    python knowledge_base/review_submissions.py                    # 審核整個 knowledge_base
    python knowledge_base/review_submissions.py path/to/file.py    # 審核單一檔案
    python knowledge_base/review_submissions.py --render            # 含 render 測試（較慢）

審核項目：
    1. AST 語法檢查（能不能 parse）
    2. Scene 類別繼承檢查
    3. Docstring 存在性
    4. [VISUAL REASONING] 註解
    5. 行數範圍（20–150 行）
    6. Import 規範（只允許 manim, numpy, math）
    7. Manim render 測試（--render 開啟）
    8. 輸出影片截圖供人工目視確認
"""

import ast
import sys
import os
import subprocess
import json
from pathlib import Path
from dataclasses import dataclass, field
from typing import Optional

# ─── 設定 ──────────────────────────────────────────────────────────────────────

ALLOWED_IMPORTS = {"manim", "numpy", "np", "math"}
MIN_LINES = 20
MAX_LINES = 150
SCENE_BASE_CLASSES = {"Scene", "ThreeDScene", "MovingCameraScene", "ZoomedScene"}

# ─── 資料結構 ──────────────────────────────────────────────────────────────────

@dataclass
class ReviewResult:
    filepath: str
    passed: bool = True
    errors: list = field(default_factory=list)
    warnings: list = field(default_factory=list)
    info: list = field(default_factory=list)
    scene_classes: list = field(default_factory=list)
    line_count: int = 0
    render_ok: Optional[bool] = None

    def add_error(self, msg):
        self.errors.append(msg)
        self.passed = False

    def add_warning(self, msg):
        self.warnings.append(msg)

    def add_info(self, msg):
        self.info.append(msg)


# ─── 審核邏輯 ──────────────────────────────────────────────────────────────────

def check_syntax(filepath: Path, result: ReviewResult):
    """Check 1: 能不能被 Python AST parse"""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            source = f.read()
        tree = ast.parse(source)
        return tree, source
    except SyntaxError as e:
        result.add_error(f"❌ 語法錯誤：{e.msg} (line {e.lineno})")
        return None, None


def check_scene_classes(tree: ast.AST, result: ReviewResult):
    """Check 2: 是否有繼承 Scene 的 class"""
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            base_names = []
            for base in node.bases:
                if isinstance(base, ast.Name):
                    base_names.append(base.id)
                elif isinstance(base, ast.Attribute):
                    base_names.append(base.attr)

            if any(name in SCENE_BASE_CLASSES for name in base_names):
                result.scene_classes.append(node.name)

    if not result.scene_classes:
        result.add_error("❌ 找不到繼承 Scene 的 class（RAG 系統不會讀取此檔案）")


def check_docstring(tree: ast.AST, result: ReviewResult):
    """Check 3: Scene class 是否有 docstring"""
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            base_names = [b.id for b in node.bases if isinstance(b, ast.Name)]
            if any(name in SCENE_BASE_CLASSES for name in base_names):
                docstring = ast.get_docstring(node)
                if not docstring:
                    result.add_error(f"❌ class `{node.name}` 缺少 docstring")
                elif len(docstring.strip()) < 10:
                    result.add_warning(f"⚠️  class `{node.name}` 的 docstring 太短（<10 字元），請描述教學目標")


def check_visual_reasoning(source: str, result: ReviewResult):
    """Check 4: 是否有 [VISUAL REASONING] 註解"""
    if "[VISUAL REASONING]" not in source:
        result.add_error("❌ 缺少 `[VISUAL REASONING]` 註解（請描述佈局邏輯）")


def check_line_count(source: str, result: ReviewResult):
    """Check 5: 行數是否在合理範圍"""
    lines = source.strip().split("\n")
    result.line_count = len(lines)

    if result.line_count < MIN_LINES:
        result.add_warning(f"⚠️  只有 {result.line_count} 行，可能太簡單（建議 ≥{MIN_LINES} 行）")
    elif result.line_count > MAX_LINES:
        result.add_warning(f"⚠️  有 {result.line_count} 行，可能太長（建議 ≤{MAX_LINES} 行）")
    else:
        result.add_info(f"📏 {result.line_count} 行 ✓")


def check_imports(tree: ast.AST, result: ReviewResult):
    """Check 6: 是否只 import 允許的套件"""
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                top_module = alias.name.split(".")[0]
                if top_module not in ALLOWED_IMPORTS:
                    result.add_warning(f"⚠️  非標準 import: `{alias.name}`（只建議用 manim/numpy/math）")

        elif isinstance(node, ast.ImportFrom):
            if node.module:
                top_module = node.module.split(".")[0]
                if top_module not in ALLOWED_IMPORTS:
                    result.add_warning(f"⚠️  非標準 import: `from {node.module}`（只建議用 manim/numpy/math）")


def check_render(filepath: Path, scene_classes: list, result: ReviewResult):
    """Check 7: 能不能 manim -ql render（低畫質快速測試）"""
    if not scene_classes:
        result.add_info("⏭️  跳過 render 測試（沒有 Scene class）")
        return

    scene_name = scene_classes[0]  # 測第一個 Scene
    cmd = ["manim", "-ql", "--disable_caching", str(filepath), scene_name]

    try:
        proc = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=120,
            cwd=filepath.parent,
        )
        if proc.returncode == 0:
            result.render_ok = True
            result.add_info(f"🎬 Render 成功：`{scene_name}`")

            # 找到輸出的影片/圖片路徑
            for line in proc.stderr.split("\n"):
                if "File ready at" in line:
                    result.add_info(f"📂 {line.strip()}")
        else:
            result.render_ok = False
            # 擷取最後幾行錯誤
            err_lines = proc.stderr.strip().split("\n")[-5:]
            err_msg = "\n    ".join(err_lines)
            result.add_error(f"❌ Render 失敗：\n    {err_msg}")

    except subprocess.TimeoutExpired:
        result.render_ok = False
        result.add_error("❌ Render 超時（>120 秒），可能是無窮迴圈或效能問題")
    except FileNotFoundError:
        result.add_warning("⚠️  找不到 `manim` 指令，跳過 render 測試")


# ─── 主流程 ────────────────────────────────────────────────────────────────────

def review_file(filepath: Path, do_render: bool = False) -> ReviewResult:
    """對單一 .py 檔執行完整審核"""
    result = ReviewResult(filepath=str(filepath))

    # 1. 語法
    tree, source = check_syntax(filepath, result)
    if tree is None:
        return result

    # 2–6. 靜態檢查
    check_scene_classes(tree, result)
    check_docstring(tree, result)
    check_visual_reasoning(source, result)
    check_line_count(source, result)
    check_imports(tree, result)

    # 7. Render 測試
    if do_render:
        check_render(filepath, result.scene_classes, result)

    return result


def print_result(result: ReviewResult):
    """格式化輸出審核結果"""
    status = "✅ PASS" if result.passed else "❌ FAIL"
    print(f"\n{'='*60}")
    print(f"📄 {result.filepath}")
    print(f"   狀態: {status}  |  行數: {result.line_count}  |  Scene: {', '.join(result.scene_classes) or 'N/A'}")

    if result.render_ok is not None:
        render_status = "✅" if result.render_ok else "❌"
        print(f"   Render: {render_status}")

    for err in result.errors:
        print(f"   {err}")
    for warn in result.warnings:
        print(f"   {warn}")
    for info in result.info:
        print(f"   {info}")


def print_summary(results: list):
    """輸出總結報告"""
    total = len(results)
    passed = sum(1 for r in results if r.passed)
    failed = total - passed

    print(f"\n{'='*60}")
    print(f"📊 審核總結")
    print(f"   總計: {total} 個檔案")
    print(f"   ✅ 通過: {passed}")
    print(f"   ❌ 未通過: {failed}")

    if failed > 0:
        print(f"\n   需要修正的檔案：")
        for r in results:
            if not r.passed:
                print(f"   - {r.filepath}")
                for err in r.errors:
                    print(f"     {err}")

    print(f"{'='*60}\n")


def main():
    do_render = "--render" in sys.argv
    args = [a for a in sys.argv[1:] if a != "--render"]

    if args:
        # 審核指定檔案
        targets = [Path(a) for a in args]
    else:
        # 審核整個 knowledge_base
        kb_dir = Path(__file__).parent
        targets = sorted(kb_dir.rglob("*.py"))
        # 排除自己和 __pycache__
        targets = [
            t for t in targets
            if "__pycache__" not in str(t)
            and t.name != "review_submissions.py"
            and t.name != "layout_engine_demo.py"
        ]

    if not targets:
        print("找不到要審核的 .py 檔案")
        sys.exit(1)

    print(f"🔍 開始審核 {len(targets)} 個檔案" + (" (含 render 測試)" if do_render else ""))

    results = []
    for filepath in targets:
        result = review_file(filepath, do_render=do_render)
        print_result(result)
        results.append(result)

    print_summary(results)

    # 回傳非 0 exit code 如果有失敗
    if any(not r.passed for r in results):
        sys.exit(1)


if __name__ == "__main__":
    main()
