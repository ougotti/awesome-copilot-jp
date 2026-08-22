#!/usr/bin/env python3
"""
docs/ 配下のページの「最終更新」ヘッダーが古くなっていないかを点検するスクリプト。

GitHub Actions ワークフロー (.github/workflows/check-page-freshness.yml) から月次で呼び出されます。
しきい値（既定 45 日）を超えたページがあった場合は:
  - GitHub Actions output に has_stale_pages=true を設定
  - freshness_report.json に一覧（パス・最終更新日・経過日数）を書き出す

環境変数:
  FRESHNESS_DAYS   しきい値（日数。既定: 45）
  BASE_DATE        起点の日付（YYYY-MM-DD。既定: 実行日。テスト用）
  DOCS_DIR         走査対象ディレクトリ（既定: docs）
"""

import json
import os
import re
import sys
from datetime import date, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOCS_DIR = ROOT / os.environ.get("DOCS_DIR", "docs")
THRESHOLD_DAYS = int(os.environ.get("FRESHNESS_DAYS", "45"))
# 「**最終更新**: 2026-08-22」形式のヘッダーから日付を取る
UPDATED_RE = re.compile(r"\*\*最終更新\*\*\s*[:：]\s*(\d{4})-(\d{2})-(\d{2})")


def base_date() -> date:
    raw = os.environ.get("BASE_DATE", "")
    if raw:
        return datetime.strptime(raw, "%Y-%m-%d").date()
    return date.today()


def find_updated(path: Path) -> date | None:
    # ヘッダーはページ冒頭にあるため、先頭 20 行だけを見る
    with path.open(encoding="utf-8") as f:
        for _, line in zip(range(20), f):
            m = UPDATED_RE.search(line)
            if m:
                return date(int(m.group(1)), int(m.group(2)), int(m.group(3)))
    return None


def set_output(name: str, value: str):
    output_file = os.environ.get("GITHUB_OUTPUT")
    if output_file:
        with open(output_file, "a") as f:
            f.write(f"{name}={value}\n")
    else:
        print(f"::set-output name={name}::{value}")


def main() -> int:
    today = base_date()
    stale: list[dict] = []
    missing: list[str] = []
    checked = 0

    for path in sorted(DOCS_DIR.rglob("*.md")):
        checked += 1
        updated = find_updated(path)
        rel = path.relative_to(ROOT).as_posix()
        if updated is None:
            missing.append(rel)
            continue
        days = (today - updated).days
        if days > THRESHOLD_DAYS:
            stale.append({"path": rel, "updated": updated.isoformat(), "days": days})

    stale.sort(key=lambda item: item["days"], reverse=True)

    print(f"チェック対象: {checked} ファイル（しきい値: {THRESHOLD_DAYS} 日 / 起点: {today}）")
    for item in stale:
        print(f"  [STALE] {item['path']} — {item['updated']}（{item['days']} 日経過）")
    for rel in missing:
        print(f"  [NO HEADER] {rel} — 「最終更新」ヘッダーが見つかりません")

    with open("freshness_report.json", "w") as f:
        json.dump(
            {
                "base_date": today.isoformat(),
                "threshold_days": THRESHOLD_DAYS,
                "stale": stale,
                "missing_header": missing,
            },
            f,
            ensure_ascii=False,
            indent=2,
        )

    has_stale = bool(stale or missing)
    set_output("has_stale_pages", "true" if has_stale else "false")
    if not has_stale:
        print("鮮度チェック OK（しきい値超のページはありません）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
