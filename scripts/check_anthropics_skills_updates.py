#!/usr/bin/env python3
"""
anthropics/skills リポジトリで、スキルの追加・削除がないかチェックするスクリプト。

GitHub Actions ワークフロー (.github/workflows/check-anthropics-skills-updates.yml) から呼び出されます。
追加または削除が見つかった場合は:
  - GitHub Actions output に has_new_skills / has_removed_skills を設定
  - anthropics_skills_report.json に詳細を書き出す
"""

import json
import os
import sys
import urllib.request
import urllib.error
from pathlib import Path


UPSTREAM_REPO = "anthropics/skills"
SKILLS_DIR = "skills"
TRACKED_FILE = os.environ.get("TRACKED_FILE", "scripts/known-files.json")
TRACKED_KEY = "anthropics_skills"
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
        print(f"[ERROR] GitHub API request failed: {e.code} {e.reason} (path={path})", file=sys.stderr)
        sys.exit(1)


def fetch_skill_names() -> list[str]:
    """upstream リポジトリの skills/ ディレクトリにあるスキル名（サブディレクトリ）一覧を取得"""
    items = github_api_get(SKILLS_DIR)
    return sorted(item["name"] for item in items if item["type"] == "dir")


def load_known_skills() -> list[str]:
    """追跡済みスキル一覧を known-files.json から読み込む"""
    path = Path(TRACKED_FILE)
    if path.exists():
        with path.open() as f:
            data = json.load(f)
            return data.get(TRACKED_KEY, [])
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
    print(f"Skills directory: {SKILLS_DIR}/")

    upstream_skills = fetch_skill_names()
    known_skills = set(load_known_skills())

    new_skills = [s for s in upstream_skills if s not in known_skills]
    removed_skills = sorted(s for s in known_skills if s not in set(upstream_skills))

    print(f"\nUpstream: {len(upstream_skills)} skills")
    print(f"Known:    {len(known_skills)} skills")
    print(f"New:      {len(new_skills)} skills")
    for s in new_skills:
        print(f"  + {s}")
    print(f"Removed:  {len(removed_skills)} skills")
    for s in removed_skills:
        print(f"  - {s}")

    with open("anthropics_skills_report.json", "w") as f:
        json.dump({"new_skills": new_skills, "removed_skills": removed_skills}, f, ensure_ascii=False, indent=2)

    set_output("has_new_skills", "true" if new_skills else "false")
    set_output("has_removed_skills", "true" if removed_skills else "false")
    if new_skills or removed_skills:
        print("\nChanges found! Issue will be created.")
    else:
        print("\nNo changes found.")


if __name__ == "__main__":
    main()
