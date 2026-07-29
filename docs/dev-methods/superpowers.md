# obra/superpowers — コーディングエージェント向けスキルフレームワーク

> **対象ツール**: ツール横断（Claude Code・Codex・Cursor・GitHub Copilot CLI ほか） ｜ **対象読者**: エンジニア ｜ **最終更新**: 2026-07-29

> [obra/superpowers](https://github.com/obra/superpowers) は Jesse Vincent 氏が開発した、AI コーディングエージェントに**ソフトウェア開発ライフサイクル（SDLC）の規律**を組み込むオープンソースのスキルフレームワークです。Claude Code、Codex、Cursor、GitHub Copilot CLI など多数のツールに対応しています。

## superpowers とは

superpowers は、AI コーディングエージェントが「すぐに実装しようとする」「テストを省略する」「設計なしに進める」といった問題行動を、**スキル（ルール集）によって構造的に防ぐ**フレームワークです。

コーディングエージェントが新しいタスクを受け取ると、いきなりコードを書き始めるのではなく、

1. まず要件を深掘りし
2. 設計を確認してもらい
3. 詳細な実装計画を立てた上で
4. テスト駆動開発の作法に従って実装を進める

という流れを**スキルが自動的に強制します**。主要なスキルには「Iron Law（鉄の掟）」と呼ばれる厳守ルールが明示されており、エージェントが段取りを飛ばすことを防ぎます。

| 項目 | 内容 |
|-----|------|
| **作者** | Jesse Vincent（[Prime Radiant](https://primeradiant.com)） |
| **リポジトリ** | [github.com/obra/superpowers](https://github.com/obra/superpowers) |
| **ライセンス** | MIT |
| **対応ツール** | Claude Code、Codex CLI/App、Cursor、Gemini CLI、OpenCode、GitHub Copilot CLI、Factory Droid |

---

## インストール方法

### Claude Code

**公式マーケットプレイスから（推奨）**

```
/plugin install superpowers@claude-plugins-official
```

**Superpowers マーケットプレイスから**

```
/plugin marketplace add obra/superpowers-marketplace
/plugin install superpowers@superpowers-marketplace
```

インストール後は `/reload-plugins` で有効化します。

### Codex CLI

```
/plugins
```

を実行してプラグイン検索インターフェースを開き、`superpowers` を検索して `Install Plugin` を選択します。

### Codex App

Codex アプリのサイドバーから `Plugins` → `Coding` セクションの `Superpowers` → `+` でインストールします。

### Cursor

```
/add-plugin superpowers
```

またはプラグインマーケットプレイスで "superpowers" を検索してインストールします。

### GitHub Copilot CLI

```
copilot plugin marketplace add obra/superpowers-marketplace
copilot plugin install superpowers@superpowers-marketplace
```

### Gemini CLI

```
gemini extensions install https://github.com/obra/superpowers
```

### OpenCode

```
Fetch and follow instructions from https://raw.githubusercontent.com/obra/superpowers/refs/heads/main/.opencode/INSTALL.md
```

---

## 基本ワークフロー

superpowers を導入すると、コーディングエージェントは以下のフローを自動で実行します。

```
brainstorming
    ↓ 要件・設計の確認
using-git-worktrees
    ↓ ワークスペース準備
writing-plans
    ↓ 詳細な実装計画
subagent-driven-development または executing-plans
    ↓ タスク実行（並列対応）
test-driven-development
    ↓ TDD で実装
requesting-code-review
    ↓ コードレビュー
finishing-a-development-branch
    ↓ ブランチのマージ・整理
```

各ステップは**エージェントが自動で判断して適用**します。ユーザーが「このスキルを使って」と指示する必要はありません。

---

## スキル一覧

superpowers には 14 のスキルが含まれており、テスト・デバッグ・コラボレーション・メタの 4 カテゴリに分類されます。

### テスト（Testing）

#### test-driven-development — テスト駆動開発

| 項目 | 内容 |
|-----|------|
| **機能** | RED-GREEN-REFACTOR サイクルの厳守 |
| **発動タイミング** | 実装フェーズ全体を通じて自動適用 |

**ワークフロー：**

```
RED：失敗するテストを書く → テストが失敗することを確認
GREEN：テストを通す最小限のコードを書く → テストが通ることを確認
REFACTOR：コードを整理・改善 → テストが引き続き通ることを確認
→ コミット
```

**Iron Law（鉄の掟）：**
- テストなしのコードは書かない
- テストが実際に失敗することを確認してから実装する
- テストより先に書いてしまったコードは削除する

---

### デバッグ（Debugging）

#### systematic-debugging — 体系的デバッグ

| 項目 | 内容 |
|-----|------|
| **機能** | 4 フェーズによる根本原因究明プロセスの強制 |
| **発動タイミング** | エラー・バグ発生時 |

**4 フェーズ：**

| フェーズ | 内容 |
|--------|------|
| **1. 再現** | バグを確実に再現するテストケースを作成 |
| **2. 仮説** | 原因の仮説を複数立てる |
| **3. 検証** | 仮説を一つずつ検証（最も単純なものから） |
| **4. 修正** | 根本原因を特定してから修正を実施 |

**Iron Law：** 推測で修正しない。必ず根本原因を特定してから対処する。

---

#### verification-before-completion — 完了前検証

| 項目 | 内容 |
|-----|------|
| **機能** | 「完了」宣言前に動作を必ず検証 |
| **発動タイミング** | タスク完了宣言の直前 |

**検証内容：**
- 指定された検証コマンドをすべて実行
- テストが全て通ることを確認
- 手動で動作確認が必要な場合は明示的にユーザーへ依頼

**Iron Law：** 検証なしに「完了しました」と言わない。

---

### コラボレーション（Collaboration）

#### brainstorming — ブレインストーミング

| 項目 | 内容 |
|-----|------|
| **機能** | 要件・設計の深掘りと確認 |
| **発動タイミング** | 実装開始前に自動適用 |

コーディングエージェントがソクラテス式の質問を通じて、ユーザーの真の要件を引き出します。設計をセクション単位で提示してユーザーに確認を求めます。確認が取れた設計は設計ドキュメントとして保存されます。

**Iron Law：** 設計の承認なしに実装に進まない。

---

#### writing-plans — 実装計画の作成

| 項目 | 内容 |
|-----|------|
| **機能** | 詳細な実装タスク分解 |
| **発動タイミング** | 設計承認後に自動適用 |

承認された設計をもとに、2〜5 分単位のタスクに分解します。各タスクには正確なファイルパス、完全なコード、検証ステップが含まれます。

**Iron Law：** 曖昧なタスクは作らない。経験の浅いエンジニアでも迷わず実行できる粒度に分解する。

---

#### executing-plans — 計画の実行

| 項目 | 内容 |
|-----|------|
| **機能** | バッチ実行と人間によるチェックポイント |
| **発動タイミング** | 計画作成後に適用（subagent-driven-development の代替） |

タスクをバッチで実行しつつ、定期的に人間へ確認を求めます。

---

#### subagent-driven-development — サブエージェント駆動開発

| 項目 | 内容 |
|-----|------|
| **機能** | タスクごとにサブエージェントを起動し、2 段階レビューで高速反復 |
| **発動タイミング** | 計画作成後に適用（executing-plans の代替） |

各タスクに専用のサブエージェントを割り当て、**仕様準拠レビュー → コード品質レビュー**の 2 段階でレビューします。並列実行にも対応しており、Claude が数時間にわたって自律的に作業を続けることが可能です。

---

#### dispatching-parallel-agents — 並列エージェントの管理

| 項目 | 内容 |
|-----|------|
| **機能** | 複数サブエージェントの並列ワークフロー管理 |
| **発動タイミング** | 並列化可能なタスクが存在する場合 |

独立したタスクを複数のサブエージェントに並列配布し、結果を集約します。

---

#### requesting-code-review — コードレビューの依頼

| 項目 | 内容 |
|-----|------|
| **機能** | レビュー前チェックリストの実施と構造的なレビュー依頼 |
| **発動タイミング** | タスク間やブランチ完成後 |

実装計画との差分を確認し、問題を重大度別に報告します。Critical な問題は前進をブロックします。

---

#### receiving-code-review — コードレビューへの対応

| 項目 | 内容 |
|-----|------|
| **機能** | レビューフィードバックへの一貫した対応プロセス |
| **発動タイミング** | コードレビューフィードバック受領後 |
このスキルの詳細な手順は公式リポジトリ（https://github.com/obra/superpowers）のドキュメントを参照してください。
---

#### using-git-worktrees — Git ワークツリーの活用

| 項目 | 内容 |
|-----|------|
| **機能** | 隔離されたワークスペースの確保とテストベースラインの確認 |
| **発動タイミング** | 設計承認後、実装開始前 |

新しいブランチ上にワークツリーを作成し、プロジェクトセットアップを実行、クリーンなテストベースラインを確認します。

---

#### finishing-a-development-branch — ブランチの完了処理

| 項目 | 内容 |
|-----|------|
| **機能** | テスト確認後のマージ/PR/保留/破棄の選択と後片付け |
| **発動タイミング** | タスクが全て完了した時点 |

テストを最終確認し、マージ・PR 作成・保留・破棄の選択肢をユーザーに提示した後、ワークツリーを片付けます。

---

### メタ（Meta）

#### using-superpowers — superpowers の使い方

| 項目 | 内容 |
|-----|------|
| **機能** | スキルシステムへの入門ガイド |
| **発動タイミング** | 初回起動時・スキル確認時 |
入門としては公式リポジトリ（https://github.com/obra/superpowers）の README と各スキル定義を参照してください。
---

#### writing-skills — スキルの作成

| 項目 | 内容 |
|-----|------|
| **機能** | superpowers のベストプラクティスに従った新スキルの設計・テスト・最適化 |
| **発動タイミング** | 新しいカスタムスキルを作成する際 |
カスタムスキル作成の詳細は公式リポジトリ（https://github.com/obra/superpowers）内のガイドを参照してください。
---

## スキルの自動適用の仕組み

superpowers のスキルは**エージェントがタスクの前に自動でチェック**し、関連するものを適用します。ユーザーが「このスキルを使って」と指示する必要はありません。

```
エージェントがタスクを受け取る
    ↓
利用可能なスキルを確認
    ↓
関連するスキルを自動選択・適用
    ↓
スキルに定義されたワークフローに従って実行
```

---

## 設計思想（Philosophy）

| 原則 | 内容 |
|-----|------|
| **テスト駆動開発** | 常にテストを先に書く |
| **体系的 > アドホック** | 推測ではなくプロセスで進める |
| **複雑性の削減** | シンプルさを最重要目標とする |
| **エビデンス優先** | 「完了した」と言う前に必ず検証する |

---

## 参考リンク

- [obra/superpowers — GitHub](https://github.com/obra/superpowers) — 公式リポジトリ・インストール手順
- [superpowers リリースアナウンス](https://blog.fsck.com/2025/10/09/superpowers/) — 作者による解説記事
- [Claude Code に superpowers を入れて、エージェントが「考えてから書く」ようになった](https://blog.serverworks.co.jp/claude-code-superpowers) — サーバーワークス Tech ブログ（日本語）
- [Discord コミュニティ](https://discord.gg/35wsABTejz) — サポート・情報交換

---

> **注意**: superpowers は Anthropic・OpenAI・GitHub が公式に提供するものではなく、Jesse Vincent 氏および Prime Radiant によるコミュニティプロジェクトです。Anthropic 公式スキルについては [Anthropic 公式スキル](../claude-code/official-skills.md) を参照してください。
