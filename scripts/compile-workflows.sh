#!/usr/bin/env bash
# compile-workflows.sh
#
# 使い方:
#   bash scripts/compile-workflows.sh
#
# 概要:
#   .github/workflows/*.md ファイル内の ```yaml コードブロックを抽出し、
#   同名の .yml ファイルとして出力する。
#
# gh コマンドからの呼び出し例:
#   gh extension exec scripts/compile-workflows.sh
#   または
#   gh api ... (gh CLI 経由で実行)

set -euo pipefail

WORKFLOWS_DIR="$(cd "$(dirname "$0")/.." && pwd)/.github/workflows"

echo "ワークフローコンパイルを開始します..."
echo "対象ディレクトリ: ${WORKFLOWS_DIR}"
echo ""

compiled=0
skipped=0

for md_file in "${WORKFLOWS_DIR}"/*.md; do
  [ -f "${md_file}" ] || continue

  base="$(basename "${md_file}" .md)"
  yml_file="${WORKFLOWS_DIR}/${base}.yml"

  # ```yaml〜``` ブロックを抽出（最初のブロックのみ）
  yaml_content="$(python3 -c "
import re, pathlib, sys
text = pathlib.Path('${md_file}').read_text(encoding='utf-8')
match = re.search(r'\`\`\`(?:ya?ml)[ \t]*\r?\n(.*?)\`\`\`', text, re.DOTALL)
if match:
    print(match.group(1), end='')
")"

  if [ -z "${yaml_content}" ]; then
    echo "[SKIP] ${base}.md: yaml コードブロックが見つかりません"
    skipped=$((skipped + 1))
    continue
  fi

  printf '%s' "${yaml_content}" > "${yml_file}"
  echo "[OK]   ${base}.md → ${base}.yml"
  compiled=$((compiled + 1))
done

echo ""
echo "完了: ${compiled} ファイルをコンパイル、${skipped} ファイルをスキップ"
