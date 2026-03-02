#!/usr/bin/env python3
"""
awesome-copilot の upstream リポジトリに新規ファイルが追加されていないかチェックするスクリプト。

GitHub Actions ワークフロー (.github/workflows/check-upstream-updates.yml) から呼び出されます。
新規ファイルが見つかった場合は:
  - GitHub Actions output に has_new_files=true を設定
  - new_files_report.json に詳細を書き出す
"""

import json
import os
import sys
import urllib.request
import urllib.error
from pathlib import Path


UPSTREAM_REPO = os.environ.get("UPSTREAM_REPO", "github/awesome-copilot")
TRACKED_DIRS = os.environ.get("TRACKED_DIRS", "instructions,agents,prompts").split(",")
TRACKED_FILE = os.environ.get("TRACKED_FILE", "scripts/known-files.json")
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN", "")


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
        if e.code == 404:
            print(f"[WARNING] Directory not found (404): {path} - skipping", file=sys.stderr)
            return []
        else:
            print(f"[ERROR] GitHub API request failed: {e.code} {e.reason} (path={path})", file=sys.stderr)
            sys.exit(1)


def fetch_filenames(directory: str) -> list[str]:
    """upstream リポジトリのディレクトリにあるファイル名一覧を取得"""
    items = github_api_get(directory)
    return sorted(
        item["name"]
        for item in items
        if item["type"] == "file" and item["name"].endswith(".md")
    )


def load_known_files() -> dict[str, list[str]]:
    """追跡済みファイル一覧を読み込む"""
    tracked_path = Path(TRACKED_FILE)
    if tracked_path.exists():
        with tracked_path.open() as f:
            return json.load(f)
    return {d: [] for d in TRACKED_DIRS}


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
    print(f"Directories: {', '.join(TRACKED_DIRS)}")

    known = load_known_files()
    new_files: dict[str, list[str]] = {}
    total_new = 0

    for directory in TRACKED_DIRS:
        print(f"\n[{directory}] Fetching file list...")
        upstream_files = fetch_filenames(directory)
        known_files = set(known.get(directory, []))

        added = [f for f in upstream_files if f not in known_files]
        new_files[directory] = added
        total_new += len(added)

        print(f"  Upstream: {len(upstream_files)} files")
        print(f"  Known:    {len(known_files)} files")
        print(f"  New:      {len(added)} files")
        for f in added:
            print(f"    + {f}")

    print(f"\n{'='*50}")
    print(f"Total new files: {total_new}")

    # 結果を出力
    with open("new_files_report.json", "w") as f:
        json.dump(new_files, f, ensure_ascii=False, indent=2)

    if total_new > 0:
        set_output("has_new_files", "true")
        print("New files found! Issue will be created.")
    else:
        set_output("has_new_files", "false")
        print("No new files found.")


if __name__ == "__main__":
    main()
