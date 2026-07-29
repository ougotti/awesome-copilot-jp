#!/usr/bin/env python3
"""
README.md・CHANGELOG.md と docs/ 配下の Markdown 内部リンク
（相対リンク・アンカー）が壊れていないかを検証するスクリプト。

CI (.github/workflows/ci.yml) から呼び出されます。
外部 URL（http/https）はチェック対象外です。
"""

import re
import sys
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LINK_RE = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
HEADING_RE = re.compile(r"^#{1,6}\s+(.*)$")


def slugify(text: str) -> str:
    """GitHub (github-slugger) 風のアンカー slug を生成（日本語対応の簡易版）。

    GitHub は「小文字化 → 許可文字以外を削除 → 空白をハイフンに変換」の順で処理し、
    先頭/末尾のトリムは行わない。そのため絵文字 + 空白で始まる見出し
    （例: `## 🚀 タイトル`）は先頭にハイフンが付いた slug になる。
    """
    # raw 見出しの前後空白のみトリムしてから小文字化
    text = text.strip().lower()
    # インラインコードのバッククォートを除去
    text = text.replace("`", "")
    # 単語文字（Unicode 文字・数字）・空白・ハイフン・アンダースコア以外を削除
    # （記号・絵文字・句読点が対象。絵文字削除で残る空白はこの後ハイフン化される）
    out = [ch for ch in text if ch.isalnum() or ch in (" ", "-", "_")]
    # 空白をハイフンに変換（先頭/末尾はトリムしない＝GitHub の挙動に合わせる）
    return "".join(out).replace(" ", "-")


def collect_headings(path: Path) -> set[str]:
    slugs: set[str] = set()
    in_code = False
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip().startswith("```"):
            in_code = not in_code
            continue
        if in_code:
            continue
        m = HEADING_RE.match(line)
        if m:
            slugs.add(slugify(m.group(1)))
    return slugs


def iter_md_files() -> list[Path]:
    files = [ROOT / "README.md", ROOT / "CHANGELOG.md"]
    files += sorted((ROOT / "docs").rglob("*.md"))
    return [f for f in files if f.exists()]


def main() -> int:
    md_files = iter_md_files()
    heading_cache: dict[Path, set[str]] = {}
    errors: list[str] = []

    for md in md_files:
        in_code = False
        for lineno, line in enumerate(md.read_text(encoding="utf-8").splitlines(), 1):
            if line.strip().startswith("```"):
                in_code = not in_code
                continue
            if in_code:
                continue
            for target in LINK_RE.findall(line):
                target = target.strip()
                # 外部リンク・mailto・画像データはスキップ
                if target.startswith(("http://", "https://", "mailto:", "#!", "data:")):
                    continue

                rel = md.relative_to(ROOT)

                if target.startswith("#"):
                    # 同一ファイル内アンカー
                    anchor = target[1:]
                    slugs = heading_cache.setdefault(md, collect_headings(md))
                    if slugify(anchor) not in slugs:
                        errors.append(f"{rel}:{lineno} 壊れたアンカー: {target}")
                    continue

                # 相対ファイルリンク（アンカー付きも分解）
                file_part, _, anchor = target.partition("#")
                if not file_part:
                    continue
                dest = (md.parent / file_part).resolve()
                if not dest.exists():
                    errors.append(f"{rel}:{lineno} 壊れたリンク: {target}")
                    continue
                if anchor and dest.suffix == ".md":
                    slugs = heading_cache.setdefault(dest, collect_headings(dest))
                    if slugify(anchor) not in slugs:
                        errors.append(f"{rel}:{lineno} 壊れたアンカー: {target}")

    print(f"チェック対象: {len(md_files)} ファイル")
    if errors:
        print(f"\n{len(errors)} 件のリンクエラー:")
        for e in errors:
            print(f"  - {e}")
        return 1

    print("内部リンクチェック OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
