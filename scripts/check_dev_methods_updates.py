#!/usr/bin/env python3
"""
手動追従になっている upstream リポジトリで、スキル・拡張の追加・削除がないかチェックするスクリプト。

対象は `TARGETS` に定義した 5 リポジトリで、それぞれ対応する docs ページを持ちます。
GitHub Actions ワークフロー (.github/workflows/check-dev-methods-updates.yml) から呼び出されます。

追加または削除が見つかった場合は:
  - GitHub Actions output に has_new_items / has_removed_items を設定
  - dev_methods_report.json に詳細（リポジトリ・対応 docs・追加 / 削除パス）を書き出す

監視パスの取得が 404 になった対象は、削除を判定しません（構成変更で全件を削除扱いにしないため）。

環境変数:
  TRACKED_FILE   追跡リストの JSON（既定: scripts/known-files.json）
  TARGET_KEYS    カンマ区切りで対象を絞り込む（既定: 全対象）
  GITHUB_TOKEN   GitHub API のレート制限緩和に使用
"""

import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path

# 監視対象。key は known-files.json のキー、docs は更新先ページ。
# depth=2 を指定すると「カテゴリ/名前」の 2 階層をたどる。
TARGETS = [
    # openai/skills は 2026-06-22 に deprecated。後継の openai/plugins を監視する。
    {
        "key": "openai_plugins",
        "repo": "openai/plugins",
        "paths": ["plugins"],
        "docs": "docs/codex/catalog.md",
        "label": "Codex カタログ（openai/plugins）",
    },
    {
        "key": "mattpocock_skills",
        "repo": "mattpocock/skills",
        "paths": ["skills/engineering", "skills/productivity"],
        "docs": "docs/dev-methods/mattpocock-skills.md",
        "label": "mattpocock/skills 解説",
    },
    {
        "key": "superpowers_skills",
        "repo": "obra/superpowers",
        "paths": ["skills"],
        "docs": "docs/dev-methods/superpowers.md",
        "label": "superpowers 解説",
    },
    {
        "key": "vercel_agent_skills",
        "repo": "vercel-labs/agent-skills",
        "paths": ["skills"],
        "docs": "docs/dev-methods/skills-sh.md",
        "label": "skills.sh ガイド（Vercel 公式 Skill 集）",
    },
    # AI-DLC は v2（2026-06-15〜）で旧 extensions を廃止し、core/ 配下へ再編した。
    {
        "key": "aidlc_skills",
        "repo": "awslabs/aidlc-workflows",
        "paths": ["core/skills"],
        "docs": "docs/dev-methods/aidlc-workflows.md",
        "label": "AI-DLC ワークフロー解説",
    },
]

TRACKED_FILE = os.environ.get("TRACKED_FILE", "scripts/known-files.json")
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN", "")


def github_api_get(repo: str, path: str) -> list | None:
    url = f"https://api.github.com/repos/{repo}/contents/{path}"
    req = urllib.request.Request(url)
    req.add_header("Accept", "application/vnd.github+json")
    req.add_header("X-GitHub-Api-Version", "2022-11-28")
    if GITHUB_TOKEN:
        req.add_header("Authorization", f"Bearer {GITHUB_TOKEN}")

    try:
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode())
            return data if isinstance(data, list) else []
    except urllib.error.HTTPError as e:
        if e.code == 404:
            print(f"[WARNING] Not found (404): {repo}/{path} - skipping", file=sys.stderr)
            return None
        print(
            f"[ERROR] GitHub API request failed: {e.code} {e.reason} ({repo}/{path})",
            file=sys.stderr,
        )
        sys.exit(1)


def list_dirs(repo: str, path: str, depth: int) -> list[str] | None:
    """指定パス配下のディレクトリを depth 階層までたどり、リポジトリルートからのパスで返す（404 なら None）。"""
    items = github_api_get(repo, path)
    if items is None:
        return None
    found: list[str] = []
    for item in items:
        if item["type"] != "dir":
            continue
        child = f"{path}/{item['name']}"
        if depth <= 1:
            found.append(child)
        else:
            found.extend(list_dirs(repo, child, depth - 1) or [])
    return found


def load_known() -> dict:
    p = Path(TRACKED_FILE)
    if p.exists():
        with p.open() as f:
            return json.load(f)
    return {}


def set_output(name: str, value: str):
    output_file = os.environ.get("GITHUB_OUTPUT")
    if output_file:
        with open(output_file, "a") as f:
            f.write(f"{name}={value}\n")
    else:
        print(f"::set-output name={name}::{value}")


def main():
    only = {k.strip() for k in os.environ.get("TARGET_KEYS", "").split(",") if k.strip()}
    known = load_known()
    report: dict[str, dict] = {}
    total_new = 0
    total_removed = 0

    for target in TARGETS:
        if only and target["key"] not in only:
            continue

        print(f"\n=== {target['repo']} ({target['key']}) ===")
        upstream: list[str] = []
        missing_paths: list[str] = []
        for path in target["paths"]:
            dirs = list_dirs(target["repo"], path, target.get("depth", 1))
            if dirs is None:
                missing_paths.append(path)
            else:
                upstream.extend(dirs)
        upstream = sorted(upstream)

        known_items = set(known.get(target["key"], []))
        added = [p for p in upstream if p not in known_items]
        if missing_paths:
            print(f"  [WARNING] 404 のため削除を判定しません: {', '.join(missing_paths)}")
            removed: list[str] = []
        else:
            removed = sorted(p for p in known_items if p not in set(upstream))

        print(
            f"  Upstream: {len(upstream)} / Known: {len(known_items)} / New: {len(added)} / Removed: {len(removed)}"
        )
        for p in added:
            print(f"    + {p}")
        for p in removed:
            print(f"    - {p}")

        report[target["key"]] = {
            "repo": target["repo"],
            "docs": target["docs"],
            "label": target["label"],
            "new": added,
            "removed": removed,
        }
        total_new += len(added)
        total_removed += len(removed)

    with open("dev_methods_report.json", "w") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)

    print(f"\n{'=' * 50}\nTotal new items: {total_new} / removed items: {total_removed}")
    set_output("has_new_items", "true" if total_new > 0 else "false")
    set_output("has_removed_items", "true" if total_removed > 0 else "false")


if __name__ == "__main__":
    main()
