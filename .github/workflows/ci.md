# Agentic Workflow: CI（継続的インテグレーション）

## 目的

Pull Requestに対して自動でコード品質チェックを行い、
マージ前に問題がないことを確認する。
自動マージの前提条件となる必須チェックを提供する。

## トリガー

- Pull Requestが新規作成されたとき（`opened`）
- Pull RequestにコミットがPushされたとき（`synchronize`）
- Pull Requestが再オープンされたとき（`reopened`）
- `main` ブランチへPushされたとき（`push`）— README の CI バッジが `main` の状態を示すために必要

## 実行内容

### lint ジョブ

1. リポジトリをチェックアウトする
2. Python 3.12 をセットアップする
3. `scripts/*.py` の構文チェック（`py_compile`）を実行する
4. `scripts/known-files.json` のJSON形式が正しいか検証する
5. `python3 scripts/check_links.py` で内部リンクを検証する
6. `python3 scripts/check_catalog_counts.py` で README / docs の件数表記を検証する

### build ジョブ

1. リポジトリをチェックアウトする
2. Python 3.12 をセットアップする
3. `pip install requests` で依存関係をインストールする
4. 以下のファイルが存在することを確認する：
   - `README.md`
   - `docs/copilot/instructions.md`
   - `docs/copilot/agents.md`
   - `docs/copilot/prompts.md`
   - `scripts/known-files.json`

### test ジョブ

1. リポジトリをチェックアウトする
2. Python 3.12 をセットアップする
3. `pip install requests` で依存関係をインストールする
4. `DRY_RUN=true` で `scripts/check_upstream_updates.py` を実行し、
   スクリプトが正常に動作することを確認する（実際のIssue作成は行わない）

## 必要な権限

各ジョブで最小権限の原則に従い `contents: read` のみを付与する。

## コンパイル済みファイル

このファイルをコンパイルすると `.github/workflows/ci.yml` が生成される。

```yaml
name: CI

on:
  pull_request:
    types:
      - opened
      - synchronize
      - reopened
  push:
    branches:
      - main

jobs:
  lint:
    name: lint
    runs-on: ubuntu-latest
    permissions:
      contents: read
    steps:
      - name: リポジトリをチェックアウト
        uses: actions/checkout@v5

      - name: Python セットアップ
        uses: actions/setup-python@v6
        with:
          python-version: '3.12'

      - name: Python 構文チェック
        run: |
          python -m py_compile scripts/*.py
          echo "Python 構文チェック OK"

      - name: JSON 形式チェック
        run: |
          python3 - << 'EOF'
          import json
          with open('scripts/known-files.json') as f:
              json.load(f)
          print('JSON 形式チェック OK')
          EOF

      - name: 内部リンクチェック
        run: python3 scripts/check_links.py

      - name: 件数表記チェック
        run: python3 scripts/check_catalog_counts.py

  build:
    name: build
    runs-on: ubuntu-latest
    permissions:
      contents: read
    steps:
      - name: リポジトリをチェックアウト
        uses: actions/checkout@v5

      - name: Python セットアップ
        uses: actions/setup-python@v6
        with:
          python-version: '3.12'

      - name: 依存関係のインストール
        run: pip install requests

      - name: ファイル構造の確認
        run: |
          test -f README.md || (echo "README.md が存在しません" && exit 1)
          test -f docs/copilot/instructions.md || (echo "docs/copilot/instructions.md が存在しません" && exit 1)
          test -f docs/copilot/agents.md || (echo "docs/copilot/agents.md が存在しません" && exit 1)
          test -f docs/copilot/prompts.md || (echo "docs/copilot/prompts.md が存在しません" && exit 1)
          test -f docs/business/use-cases.md || (echo "docs/business/use-cases.md が存在しません" && exit 1)
          test -f docs/business/office-work.md || (echo "docs/business/office-work.md が存在しません" && exit 1)
          test -f docs/business/financial-services.md || (echo "docs/business/financial-services.md が存在しません" && exit 1)
          test -f scripts/known-files.json || (echo "scripts/known-files.json が存在しません" && exit 1)
          echo "ファイル構造チェック OK"

  test:
    name: test
    runs-on: ubuntu-latest
    permissions:
      contents: read
    steps:
      - name: リポジトリをチェックアウト
        uses: actions/checkout@v5

      - name: Python セットアップ
        uses: actions/setup-python@v6
        with:
          python-version: '3.12'

      - name: 依存関係のインストール
        run: pip install requests

      - name: スクリプトのドライランテスト
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          UPSTREAM_REPO: github/awesome-copilot
          TRACKED_DIRS: instructions,agents,prompts
          TRACKED_FILE: scripts/known-files.json
          DRY_RUN: 'true'
        run: |
          python scripts/check_upstream_updates.py
          echo "スクリプトのドライランテスト OK"
```
