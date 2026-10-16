#!/usr/bin/env python3
"""
anthropics/financial-services リポジトリで、エージェント／プラグインの
追加・削除がないかチェックするスクリプト。

GitHub Actions ワークフロー (.github/workflows/check-financial-services-updates.yml) から呼び出されます。
追加または削除が見つかった場合は:
  - GitHub Actions output に has_new_items / has_removed_items を設定
  - financial_services_report.json に詳細を書き出す
"""

import json
import os
import sys
import urllib.request
import urllib.error
from pathlib import Path


UPSTREAM_REPO = "anthropics/financial-services"
TRACKED_FILE = os.environ.get("TRACKED_FILE", "scripts/known-files.json")
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN", "")

# 監視対象: (known-files.json のキー, リポジトリ内ディレクトリ, 表示名)
WATCHED_DIRS = [
    ("financial_services_agents", "plugins/agent-plugins", "エージェント"),
    ("financial_services_vertical", "plugins/vertical-plugins", "垂直プラグイン"),
    ("financial_services_partner", "plugins/partner-built", "パートナー提供プラグイン"),
]


def github_api_get(path: str) -> list | dict:
    url = f"https://api.github.com/repos/{UPSTREAM_REPO}/contents/{path}"
    req = urllib.request.Request(url)
    req.add_header("Accept", "application/vnd.github+json")
    req.add_header("X-GitHub-Api-Version", "2022-11-28")
    if GITHUB_TOKEN:
        req.add_header("Authorization", f"Bearer {GITHUB_TOKEN}")

    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        print(f"[ERROR] GitHub API request failed: {e.code} {e.reason} (path={path})", file=sys.stderr)
        sys.exit(1)


def fetch_dir_names(path: str) -> list[str]:
    """指定ディレクトリ配下のサブディレクトリ名一覧を取得"""
    items = github_api_get(path)
    return sorted(item["name"] for item in items if item["type"] == "dir")


def load_known(key: str) -> list[str]:
    """追跡済みアイテム一覧を known-files.json から読み込む"""
    path = Path(TRACKED_FILE)
    if path.exists():
        with path.open() as f:
            data = json.load(f)
            return data.get(key, [])
    return []


def set_output(name: str, value: str):
    """GitHub Actions の output を設定"""
    output_file = os.environ.get("GITHUB_OUTPUT")
    if output_file:
        with open(output_file, "a") as f:
            f.write(f"{name}={value}\n")
    else:
        print(f"::set-output name={name}::{value}")


def main():
    print(f"Checking upstream: https://github.com/{UPSTREAM_REPO}")

    report = {}
    total_new = 0
    total_removed = 0

    for key, dir_path, label in WATCHED_DIRS:
        upstream = fetch_dir_names(dir_path)
        known = set(load_known(key))
        new_items = [s for s in upstream if s not in known]
        removed_items = sorted(s for s in known if s not in set(upstream))

        print(f"\n[{label}] {dir_path}/")
        print(
            f"  Upstream: {len(upstream)} / Known: {len(known)} / New: {len(new_items)} / Removed: {len(removed_items)}"
        )
        for s in new_items:
            print(f"  + {s}")
        for s in removed_items:
            print(f"  - {s}")

        report[key] = {"dir": dir_path, "label": label, "new": new_items, "removed": removed_items}
        total_new += len(new_items)
        total_removed += len(removed_items)

    with open("financial_services_report.json", "w") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)

    set_output("has_new_items", "true" if total_new else "false")
    set_output("has_removed_items", "true" if total_removed else "false")
    if total_new or total_removed:
        print(f"\n{total_new} new / {total_removed} removed item(s) found! Issue will be created.")
    else:
        print("\nNo changes found.")


if __name__ == "__main__":
    main()
