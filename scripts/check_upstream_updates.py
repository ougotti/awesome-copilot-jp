#!/usr/bin/env python3
"""
awesome-copilot の upstream リポジトリで、ファイルの追加・削除がないかチェックするスクリプト。

GitHub Actions ワークフロー (.github/workflows/check-upstream-updates.yml) から呼び出されます。
追加または削除が見つかった場合は:
  - GitHub Actions output に has_new_files / has_removed_files を設定
  - new_files_report.json に詳細（ディレクトリごとの new / removed）を書き出す

prompts は upstream で skills/ へ移行済みのため、known-files.json の `<名前>.prompt.md` は
`skills/<名前>/SKILL.md` があれば存在するとみなします（新しい Skill は追加として報告しません）。
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

# known-files.json のキーのうち、upstream では skills/<名前>/ として存在するもの
SKILL_BACKED_DIRS = {"prompts": ".prompt.md"}


def github_api_get(path: str) -> list | None:
    """ディレクトリの内容を返す。404 のときは None（削除の判定に使わない）。"""
    url = f"https://api.github.com/repos/{UPSTREAM_REPO}/contents/{path}"
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
            print(f"[WARNING] Directory not found (404): {path} - skipping", file=sys.stderr)
            return None
        else:
            print(f"[ERROR] GitHub API request failed: {e.code} {e.reason} (path={path})", file=sys.stderr)
            sys.exit(1)


def fetch_filenames(directory: str) -> list[str] | None:
    """upstream リポジトリのディレクトリにあるファイル名一覧を取得（404 なら None）"""
    items = github_api_get(directory)
    if items is None:
        return None
    return sorted(
        item["name"]
        for item in items
        if item["type"] == "file" and item["name"].endswith(".md")
    )


def fetch_skill_names() -> set[str] | None:
    items = github_api_get("skills")
    if items is None:
        return None
    return {item["name"] for item in items if item["type"] == "dir"}


def load_known_files() -> dict[str, list[str]]:
    """追跡済みファイル一覧を読み込む"""
    tracked_path = Path(TRACKED_FILE)
    if tracked_path.exists():
        with tracked_path.open(encoding="utf-8") as f:
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
    report: dict[str, dict[str, list[str]]] = {}
    total_new = 0
    total_removed = 0
    skill_names: set[str] | None = None

    for directory in TRACKED_DIRS:
        print(f"\n[{directory}] Fetching file list...")
        known_files = sorted(set(known.get(directory, [])))

        if directory in SKILL_BACKED_DIRS:
            suffix = SKILL_BACKED_DIRS[directory]
            if skill_names is None:
                skill_names = fetch_skill_names()
            if skill_names is None:
                added, removed = [], []
            else:
                added = []
                removed = [f for f in known_files if f.removesuffix(suffix) not in skill_names]
            upstream_label = "skills/ で照合"
        else:
            upstream_files = fetch_filenames(directory)
            if upstream_files is None:
                added, removed = [], []
                upstream_label = "404"
            else:
                added = [f for f in upstream_files if f not in known_files]
                removed = [f for f in known_files if f not in set(upstream_files)]
                upstream_label = f"{len(upstream_files)} files"

        report[directory] = {"new": added, "removed": removed}
        total_new += len(added)
        total_removed += len(removed)

        print(f"  Upstream: {upstream_label}")
        print(f"  Known:    {len(known_files)} files")
        print(f"  New:      {len(added)} files")
        for f in added:
            print(f"    + {f}")
        print(f"  Removed:  {len(removed)} files")
        for f in removed:
            print(f"    - {f}")

    print(f"\n{'='*50}")
    print(f"Total new files: {total_new} / removed files: {total_removed}")

    # 結果を出力
    with open("new_files_report.json", "w") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)

    set_output("has_new_files", "true" if total_new > 0 else "false")
    set_output("has_removed_files", "true" if total_removed > 0 else "false")
    if total_new or total_removed:
        print("Changes found! Issue will be created.")
    else:
        print("No changes found.")


if __name__ == "__main__":
    main()
