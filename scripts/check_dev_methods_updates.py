#!/usr/bin/env python3
"""
手動追従になっている upstream リポジトリに新規スキル・拡張が追加されていないかチェックするスクリプト。

対象は `TARGETS` に定義した 5 リポジトリで、それぞれ対応する docs ページを持ちます。
GitHub Actions ワークフロー (.github/workflows/check-dev-methods-updates.yml) から呼び出されます。

新規追加が見つかった場合は:
  - GitHub Actions output に has_new_items=true を設定
  - dev_methods_report.json に詳細（リポジトリ・対応 docs・新規パス）を書き出す

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
# depth=2 は「カテゴリ/名前」の 2 階層をたどる（AI-DLC の extensions が該当）。
TARGETS = [
    {
        "key": "openai_skills",
        "repo": "openai/skills",
        "paths": ["skills/.system", "skills/.curated", "skills/.experimental"],
        "docs": "docs/codex/catalog.md",
        "label": "Codex Agent Skills カタログ",
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
    {
        "key": "aidlc_extensions",
        "repo": "awslabs/aidlc-workflows",
        "paths": ["aidlc-rules/aws-aidlc-rule-details/extensions"],
        "depth": 2,
        "docs": "docs/dev-methods/aidlc-workflows.md",
        "label": "AI-DLC ワークフロー解説",
    },
]

TRACKED_FILE = os.environ.get("TRACKED_FILE", "scripts/known-files.json")
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN", "")


def github_api_get(repo: str, path: str) -> list:
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
            return []
        print(
            f"[ERROR] GitHub API request failed: {e.code} {e.reason} ({repo}/{path})",
            file=sys.stderr,
        )
        sys.exit(1)


def list_dirs(repo: str, path: str, depth: int) -> list[str]:
    """指定パス配下のディレクトリを depth 階層までたどり、リポジトリルートからのパスで返す。"""
    found: list[str] = []
    for item in github_api_get(repo, path):
        if item["type"] != "dir":
            continue
        child = f"{path}/{item['name']}"
        if depth <= 1:
            found.append(child)
        else:
            found.extend(list_dirs(repo, child, depth - 1))
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

    for target in TARGETS:
        if only and target["key"] not in only:
            continue

        print(f"\n=== {target['repo']} ({target['key']}) ===")
        upstream: list[str] = []
        for path in target["paths"]:
            upstream.extend(list_dirs(target["repo"], path, target.get("depth", 1)))
        upstream = sorted(upstream)

        known_items = set(known.get(target["key"], []))
        added = [p for p in upstream if p not in known_items]

        print(f"  Upstream: {len(upstream)} / Known: {len(known_items)} / New: {len(added)}")
        for p in added:
            print(f"    + {p}")

        report[target["key"]] = {
            "repo": target["repo"],
            "docs": target["docs"],
            "label": target["label"],
            "new": added,
        }
        total_new += len(added)

    with open("dev_methods_report.json", "w") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)

    print(f"\n{'=' * 50}\nTotal new items: {total_new}")
    set_output("has_new_items", "true" if total_new > 0 else "false")


if __name__ == "__main__":
    main()
