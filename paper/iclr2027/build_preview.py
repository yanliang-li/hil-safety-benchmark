"""Render the current PDF for VS Code's built-in Markdown preview."""
from __future__ import annotations

import hashlib
import json
import re
import subprocess
from datetime import datetime, timezone
from pathlib import Path


HERE = Path(__file__).resolve().parent


def main():
    pdf = HERE / "main.pdf"
    output = HERE / "preview/pages"
    output.mkdir(parents=True, exist_ok=True)
    info = subprocess.check_output(["pdfinfo", str(pdf)], text=True)
    count = int(re.search(r"^Pages:\s+(\d+)", info, re.MULTILINE).group(1))
    subprocess.run(
        ["pdftoppm", "-png", "-r", "140", str(pdf), str(output / "page")],
        check=True,
    )
    width = len(str(count))
    pages = [output / f"page-{i:0{width}d}.png" for i in range(1, count + 1)]
    for page in pages:
        assert page.read_bytes()[:8] == b"\x89PNG\r\n\x1a\n", page
    # Remove only old generated page images when the PDF page count changes.
    for page in output.glob("page-*.png"):
        if page not in pages:
            page.unlink()
    digest = hashlib.sha256(pdf.read_bytes()).hexdigest()
    lines = [
        "# ICLR 2027 初稿 · 逐页预览",
        "",
        "**在 VS Code 中打开本文件后，按 Ctrl+Shift+V；Mac 按 Cmd+Shift+V。**",
        "也可以在右上角选择“打开预览”。无需 PDF 扩展。",
        "",
        f"下方是当前 [main.pdf](main.pdf) 的全部 {count} 页，直接由 PDF 渲染，保持原排版。",
        "这是页面图像预览；需要搜索正文时可打开 [纯文本版本](main.txt)。",
        "",
        " · ".join(f"[第 {i} 页](#第-{i}-页)" for i in range(1, count + 1)),
        "",
    ]
    for i, page in enumerate(pages, 1):
        lines += [
            f"## 第 {i} 页",
            "",
            f"![论文第 {i} 页]({page.relative_to(HERE).as_posix()})",
            "",
        ]
    lines += [
        "---",
        "",
        "论文重新编译后，在项目根目录运行：",
        "",
        "    python3 paper/iclr2027/build_preview.py",
        "",
        f"对应 PDF SHA-256：{digest}",
        "",
        "快捷键依据：[VS Code Markdown 文档](https://code.visualstudio.com/docs/languages/markdown)。",
        "",
    ]
    (HERE / "VIEW_PAPER.md").write_text("\n".join(lines))
    manifest = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "pdf_sha256": digest,
        "page_count": count,
        "render_dpi": 140,
        "pages": [
            {
                "path": page.relative_to(HERE).as_posix(),
                "sha256": hashlib.sha256(page.read_bytes()).hexdigest(),
            }
            for page in pages
        ],
    }
    (HERE / "preview/manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    print(f"Generated VIEW_PAPER.md with all {count} pages.")


if __name__ == "__main__":
    main()
