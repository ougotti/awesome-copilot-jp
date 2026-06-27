---
name: run-awesome-copilot-jp
description: run, test, check links, verify scripts, smoke test awesome-copilot-jp documentation repo
---

# run-awesome-copilot-jp

ドキュメントリポジトリ。アプリサーバーや GUI はなく、CI で実行される Python スクリプト群とワークフローコンパイラが「動かすもの」。

ドライバー: `.claude/skills/run-awesome-copilot-jp/smoke.sh`（Python 3 のみ必要、追加インストール不要）

## Prerequisites

Python 3 と bash のみ。外部パッケージ不要（stdlib のみ使用）。

```bash
python3 --version   # 3.8+ で動作確認済み
```

ネットワーク接続が必要（upstream GitHub リポジトリへ API アクセス）。

## Run（エージェントパス）

```bash
bash .claude/skills/run-awesome-copilot-jp/smoke.sh
```

以下を順に実行して標準出力に結果を表示、すべて成功なら exit 0:

1. 内部リンクチェック — README.md と docs/*.md のリンク・アンカーを検証
2. Upstream 更新チェック — github/awesome-copilot との差分を検出
3. Anthropic Skills 更新チェック — anthropics/skills との差分を検出
4. Financial Services 更新チェック — anthropics/financial-services との差分を検出
5. ワークフローコンパイル — .github/workflows/*.md → *.yml を生成

## スクリプト個別実行

```bash
# 内部リンクのみ（最速）
python3 scripts/check_links.py

# upstream 差分確認
python3 scripts/check_upstream_updates.py
python3 scripts/check_anthropics_skills_updates.py
python3 scripts/check_financial_services_updates.py

# .md → .yml コンパイル
bash scripts/compile-workflows.sh
```

## Gotchas

- `check_upstream_updates.py` は `prompts/` ディレクトリを参照するが、upstream では `skills/` にリネームされており **404 が出ても正常終了**。警告として表示されるだけ。
- 更新チェックスクリプトは新ファイルを検出すると「New files found!」と表示するが、これはエラーではなく情報通知。exit 0 で終了する。
- `known-files.json` に登録済みファイル数より upstream の実ファイル数が少ない場合がある（upstream でリネーム・削除が起きた場合）。これも警告のみ。

## Troubleshooting

| 症状 | 原因・対処 |
|------|----------|
| `ConnectionError` / `URLError` | ネットワーク未接続。GitHub API へのアクセスが必要 |
| `FileNotFoundError: known-files.json` | リポジトリルートで実行していない。`cd` でルートへ移動 |
| `yaml コードブロックが見つかりません` | .github/workflows/*.md に ```yaml ブロックがない。正常スキップ |
