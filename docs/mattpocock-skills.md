# mattpocock/skills - 実務エンジニア向け Agent Skills

> **対象ツール**: ツール横断（Claude Code ほか Agent Skills 対応ツール） ｜ **対象読者**: エンジニア ｜ **最終更新**: 2026-07-29

> [mattpocock/skills](https://github.com/mattpocock/skills) は、TypeScript教育者として知られる **Matt Pocock** 氏が実務で使うAgent Skills集です。「vibe coding」ではなく、要件の認識合わせ、仕様化、TDD、デバッグ、設計、レビューといったソフトウェア開発の基本を、小さく組み合わせ可能なSkillとしてエージェントへ与えます。

## このリポジトリの特徴

- Claude Code、Codexなど、Agent Skills形式に対応するコーディングエージェントで利用できる
- 巨大な開発フレームワークではなく、目的ごとに分割されたSkillを組み合わせる
- **ユーザー呼び出し**のSkillが処理を編成し、**モデル呼び出し**のSkillが再利用可能な規律を提供する
- `skills.sh` から編集可能なコピーとして導入する方法と、Claude Codeの管理プラグインとして購読する方法がある

> [!NOTE]
> 2026年7月時点では、以前の `to-prd` / `to-issues` を中心とした構成から、`to-spec` / `to-tickets` / `implement` / `wayfinder` などへ発展しています。

---

## インストール

### Agent Skills対応エージェント

```powershell
npx skills@latest add mattpocock/skills
```

導入時に `setup-matt-pocock-skills` を選択し、対象リポジトリで一度実行します。Issue tracker、トリアージ用ラベル、文書の保存先を設定します。

### Claude Codeプラグイン

```text
/plugin marketplace add mattpocock/skills
/plugin install mattpocock-skills@mattpocock
```

シェルから導入する場合：

```powershell
claude plugin marketplace add mattpocock/skills
claude plugin install mattpocock-skills@mattpocock
```

| 導入方法 | 特徴 |
|----------|------|
| `npx skills` | プロジェクトへコピーされ、自分向けに編集できる。Codexなどにも導入可能 |
| Claude Codeプラグイン | 読み取り専用の管理された一式として更新を追従する |

---

## 設計思想：4つの失敗モード

| 失敗モード | 問題 | 対応 |
|------------|------|------|
| **Misalignment** | 開発者の意図とエージェントの理解がずれる | `grill-me` / `grill-with-docs` で着手前に質問を重ねる |
| **Excessive Verbosity** | 用語が揃わず説明が長くなる | `CONTEXT.md` とドメインモデルで共通言語を作る |
| **Broken Code** | 実行時のフィードバックがなく壊れたコードを作る | `tdd` / `diagnosing-bugs` で検証ループを回す |
| **Architectural Decay** | 高速な変更で設計の劣化も加速する | `to-spec` / `codebase-design` / `improve-codebase-architecture` を使う |

---

## Engineering Skills

### ユーザー呼び出し

ユーザーが明示的に起動し、複数の作業を編成するSkillです。

| Skill | 用途 |
|-------|------|
| **ask-matt** | 現在の状況に適したSkillや進め方を案内する |
| **grill-with-docs** | 深掘り質問を行い、用語集、`CONTEXT.md`、ADRも更新する |
| **triage** | Issueを役割ベースの状態機械でトリアージする |
| **improve-codebase-architecture** | コードベースの改善候補をHTMLレポートで示し、対象を深掘りする |
| **setup-matt-pocock-skills** | Issue tracker、ラベル、文書構成をリポジトリへ設定する |
| **to-spec** | 現在の会話を仕様へ整理し、Issue trackerへ公開する |
| **to-tickets** | 計画や仕様を、依存関係を持つtracer-bullet型チケットへ分解する |
| **implement** | 仕様やチケットを実装し、合意した境界でTDDとコードレビューを回す |
| **wayfinder** | 1セッションでは収まらない大規模作業を調査チケットの地図にする |

### モデル呼び出し

ユーザーからの明示指定に加え、タスクに合えばモデルが自動選択できるSkillです。

| Skill | 用途 |
|-------|------|
| **prototype** | 設計上の問いに答えるため、使い捨ての実行可能プロトタイプを作る |
| **diagnosing-bugs** | 再現→最小化→仮説→計測→修正→回帰テストの順で診断する |
| **research** | 信頼度の高い一次情報を調査し、引用付きMarkdownとして記録する |
| **tdd** | red-green-refactorを垂直スライス単位で進める |
| **domain-modeling** | 用語、境界条件、エッジケースを通してドメインモデルを更新する |
| **codebase-design** | 小さなインターフェースの背後に多くの振る舞いを持つ深いモジュールを設計する |
| **code-review** | StandardsとSpecの2軸を別々にレビューする |
| **resolving-merge-conflicts** | merge / rebaseの競合を、両側の意図と一次情報からhunk単位で解決する |

---

## Productivity Skills

### ユーザー呼び出し

| Skill | 用途 |
|-------|------|
| **grill-me** | 計画や設計の意思決定を、分岐が解決するまで質問で詰める |
| **handoff** | 現在の会話を、別エージェントが継続できるhandoff文書へ圧縮する |
| **teach** | ディレクトリを状態保存に使い、複数セッションで概念を教える |
| **writing-great-skills** | 予測可能なSkillを書くための語彙と設計原則を提供する |

### モデル呼び出し

| Skill | 用途 |
|-------|------|
| **grilling** | `grill-me` / `grill-with-docs` が共通利用する深掘り質問ループ |

---

## 推奨ワークフロー

```text
grill-with-docs
  ↓ 要件・用語・判断を整理
to-spec
  ↓ 会話を仕様化
to-tickets
  ↓ 依存関係を持つ実装単位へ分解
implement
  ├─ tdd
  ├─ diagnosing-bugs
  └─ code-review
```

大規模で不確実性が高い作業では、最初に `wayfinder` を使い、`research` で調査結果を一次情報付きで蓄積します。

---

## 他のSkill集との違い

| | **mattpocock/skills** | **[anthropics/skills](anthropics-skills.md)** | **[superpowers](superpowers.md)** |
|--|----------------------|----------------------------------------------|-----------------------------------|
| 主眼 | 実務開発プロセスを小さなSkillとして構成 | 文書・表計算・デザイン等の成果物作成 | SDLC全体に規律を強制するフレームワーク |
| 代表例 | grill-with-docs / to-spec / implement / code-review | docx / pdf / pptx / xlsx | brainstorming / TDD / systematic-debugging |
| カスタマイズ | コピーして改変しやすい | 公式Skillを用途別に利用 | 定められた開発フローを強く適用 |
| 対応 | skills.sh対応エージェント、Claude Codeプラグイン | 主にClaude環境 | Claude Code、Codex、Copilot CLI等 |

---

## 参考リンク

- [mattpocock/skills](https://github.com/mattpocock/skills) — 公式リポジトリ
- [skills.sh: mattpocock/skills](https://skills.sh/mattpocock/skills) — Skill一覧と導入
- [Matt Pocock](https://www.mattpocock.com/) — 作者
- [2026年7月版 Skills最新動向](skills-ecosystem-2026.md)
- [Anthropic公式Skills](anthropics-skills.md) / [superpowers](superpowers.md)

---

> **更新基準日：2026年7月22日**。本ページは公式リポジトリのREADMEとSkill定義を元にした日本語解説です。
