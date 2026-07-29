#!/usr/bin/env python3
"""
README.md と docs/ 配下の件数表記が scripts/known-files.json と一致するか検証する。

CI (.github/workflows/ci.yml) から呼び出されます。
"""

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
KNOWN_FILES = ROOT / "scripts" / "known-files.json"


def load_counts() -> dict[str, int]:
    with KNOWN_FILES.open(encoding="utf-8") as f:
        known = json.load(f)
    return {
        "instructions": len(known["instructions"]),
        "agents": len(known["agents"]),
        "prompts": len(known["prompts"]),
    }


def extract(path: Path, pattern: str, label: str) -> str | None:
    text = path.read_text(encoding="utf-8")
    match = re.search(pattern, text, re.MULTILINE)
    if not match:
        print(f"[ERROR] {path.relative_to(ROOT)} で {label} の件数表記を見つけられませんでした。")
        return None
    return match.group(1)


def main() -> int:
    counts = load_counts()
    checks = [
        (
            ROOT / "README.md",
            r"\| \*\*\[Instructions 一覧\]\(docs/copilot/instructions\.md\)\*\* \| [^\n]+ \| ([0-9]+ 件) \|",
            "README の Instructions",
            f"{counts['instructions']} 件",
        ),
        (
            ROOT / "README.md",
            r"\| \*\*\[Agents 一覧\]\(docs/copilot/agents\.md\)\*\* \| [^\n]+ \| ([0-9]+ 件) \|",
            "README の Agents",
            f"{counts['agents']} 件",
        ),
        (
            ROOT / "README.md",
            r"\| \*\*\[Prompts / Skills 一覧\]\(docs/copilot/prompts\.md\)\*\* \| [^\n]+ \| ([0-9]+ 件) \|",
            "README の Prompts / Skills",
            f"{counts['prompts']} 件",
        ),
        (
            ROOT / "docs" / "copilot" / "instructions.md",
            r"\*\*([0-9]+ 個の Instructions)\*\*",
            "docs/copilot/instructions.md のヘッダー",
            f"{counts['instructions']} 個の Instructions",
        ),
        (
            ROOT / "docs" / "copilot" / "instructions.md",
            r"Instructions は \*\*([0-9]+ ファイル)\*\* あり",
            "docs/copilot/instructions.md のまとめ",
            f"{counts['instructions']} ファイル",
        ),
        (
            ROOT / "docs" / "copilot" / "agents.md",
            r"\*\*([0-9]+ 個の Agents)\*\*",
            "docs/copilot/agents.md のヘッダー",
            f"{counts['agents']} 個の Agents",
        ),
        (
            ROOT / "docs" / "copilot" / "agents.md",
            r"Agents は \*\*([0-9]+ ファイル)\*\* あり",
            "docs/copilot/agents.md のまとめ",
            f"{counts['agents']} ファイル",
        ),
        (
            ROOT / "docs" / "copilot" / "prompts.md",
            r"\*\*([0-9]+ 個の Skills（旧 Prompts）)\*\*",
            "docs/copilot/prompts.md のヘッダー",
            f"{counts['prompts']} 個の Skills（旧 Prompts）",
        ),
        (
            ROOT / "docs" / "copilot" / "prompts.md",
            r"Prompts は \*\*([0-9]+ ファイル)\*\* あり",
            "docs/copilot/prompts.md のまとめ",
            f"{counts['prompts']} ファイル",
        ),
    ]

    errors = 0
    for path, pattern, label, expected in checks:
        actual = extract(path, pattern, label)
        if actual is None:
            errors += 1
            continue
        if actual != expected:
            print(f"[ERROR] {label}: expected '{expected}', got '{actual}'")
            errors += 1

    if errors:
        print(f"\n件数表記チェック NG: {errors} 件")
        return 1

    print(
        "件数表記チェック OK "
        f"(instructions={counts['instructions']}, agents={counts['agents']}, prompts={counts['prompts']})"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
