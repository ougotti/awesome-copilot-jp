#!/usr/bin/env bash
# smoke.sh — awesome-copilot-jp の全スクリプトを順に実行し、終了コードを返す
# 使用例: bash .claude/skills/run-awesome-copilot-jp/smoke.sh

set -euo pipefail

ROOT="$(cd "$(dirname "$0")/../../.." && pwd)"
cd "$ROOT"

echo "=== [1/4] 内部リンクチェック ==="
python3 scripts/check_links.py

echo ""
echo "=== [2/4] Upstream 更新チェック (github/awesome-copilot) ==="
python3 scripts/check_upstream_updates.py

echo ""
echo "=== [3/4] Anthropic Skills 更新チェック ==="
python3 scripts/check_anthropics_skills_updates.py

echo ""
echo "=== [4/4] Financial Services 更新チェック ==="
python3 scripts/check_financial_services_updates.py

echo ""
echo "=== ワークフロー .md → .yml コンパイル ==="
bash scripts/compile-workflows.sh

echo ""
echo "All checks passed."
