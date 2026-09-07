# 仕様駆動開発（SDD） — 仕様を実行可能な入力にする

> **対象ツール**: ツール横断（GitHub Copilot・Claude Code・Cursor・Codex ほか多数のエージェントに対応） ｜ **実行環境**: CLI（ターミナル） ｜ **対象読者**: エンジニア ｜ **最終更新**: 2026-09-07

> このページは [github/spec-kit](https://github.com/github/spec-kit) のスナップショットです。コマンド名・生成されるディレクトリ構成・対応エージェントの一覧はバージョンで変わります。導入時は必ず [公式リポジトリ](https://github.com/github/spec-kit) と [公式ドキュメント](https://github.github.io/spec-kit/) を確認してください。実行環境は Python 3.11+ と [uv](https://docs.astral.sh/uv/)（または pipx）が前提の CLI です。

---

## SDD とは何か

**仕様駆動開発（Spec-Driven Development, SDD）**は、仕様を先に書き、それを実装の入力にする開発手法です。spec-kit の解説文書は次のように定義しています。

> Specifications don't serve code—code serves specifications.（仕様がコードに従うのではなく、コードが仕様に従う）

従来、PRD や設計ドキュメントは実装を導くための「添え物」で、コードが真実であり、仕様はコードに追いつけないまま陳腐化していきました。SDD はこの上下関係を反転させます。**仕様と実装計画そのものを実行可能にする**ことで、仕様とコードの間のギャップを「埋める」のではなく「なくす」という考え方です。

AI コーディングエージェントの力を借りて初めて現実的になった手法である点も押さえておく必要があります。仕様を理解し、精密な実装計画を生成し、そこからコードを作る一連の作業を、構造化された手順なしに AI に丸投げすると混乱を招きます。SDD はその構造（仕様 → 計画 → タスク → 実装）を提供します。

## GitHub Spec Kit のワークフロー

**GitHub Spec Kit**（[github/spec-kit](https://github.com/github/spec-kit)、MIT ライセンス）は、SDD を具体的なコマンド列として実装したツールキットです。2026 年に v1.0.0 に達し、主要なコーディングエージェントを広くカバーしています。対応エージェントの一覧は `specify integration list` または [公式の対応表](https://github.github.io/spec-kit/reference/integrations.html) で確認してください（件数は変わりやすいため本文には書きません）。

コア・ワークフローは次の順で進みます。

| # | コマンド | 役割 |
|---|---------|------|
| 0 | `/speckit.constitution` | プロジェクトの統治原則・開発ガイドラインを作成（プロジェクトにつき 1 回） |
| 1 | `/speckit.specify` | 何を作るか（**what** / **why**）を記述する。技術スタックには触れない |
| 2 | `/speckit.plan` | 技術スタックとアーキテクチャを決める |
| 3 | `/speckit.tasks` | 実装計画から実行可能なタスク一覧を作る |
| 4 | `/speckit.implement` | タスクをすべて実行して機能を作る |
| 5 | `/speckit.converge` | 実装を仕様・計画・タスクと照合し、残作業を新規タスクとして追加する |

`4` と `5` は **Converged** と判定されるまで繰り返します。

補助コマンドとして、`/speckit.clarify`（`/speckit.plan` の前に未確定な部分を明確化）・`/speckit.analyze`（`/speckit.tasks` の後、`/speckit.implement` の前にアーティファクト間の整合性を分析）・`/speckit.checklist`（要件の完全性・明確性・一貫性を検証するチェックリストを生成する、「英語のための単体テスト」）があります。

エージェントによってコマンドの呼び出し方が異なります。多くのエージェントは `/speckit.*` のスラッシュコマンドを公開しますが、一部は別の呼び出し方（skills mode でのコマンド名、CLI 独自のエージェント選択方法など）を使います。導入するエージェントでの正確な呼び出し方は、[公式の対応表](https://github.github.io/spec-kit/reference/integrations.html) を確認してください。

> spec-kit は**バグ修正**（`assess → fix → test`）と**アイデア評価**（`intake → research → define → shape → decide`）用の opt-in extension も同梱しています。いずれも `specify extension add <name>` で追加するオプトイン機能で、コア・ワークフローとは別に案内されています。

## リポジトリに何ができるか

`specify init <project> --integration <agent>` を実行すると、選んだエージェント向けのコマンドファイルとディレクトリ構成が生成されます。テンプレートは 4 段階の優先順位で解決されます。

| 優先度 | 層 | 場所 |
|---|---|---|
| 高 | プロジェクトローカルの上書き | `.specify/templates/overrides/` |
| ↓ | プリセット（用語・テンプレートの差し替え） | `.specify/presets/templates/` |
| ↓ | Extension（機能追加） | `.specify/extensions/templates/` |
| 低 | spec-kit コア（組み込みの SDD コマンド・テンプレート） | `.specify/templates/` |

**このガイドが扱う `AGENTS.md`（[コーディングエージェントの選び方](coding-agents.md)）との関係は、spec-kit の公式ドキュメントに明示的な記述が見当たりませんでした。** 断定を避け、両者は別のファイルとして併存する、という事実だけをここに書きます。

## 受け入れ基準の書き方 — EARS

仕様のうち「システムはどう振る舞うべきか」を曖昧さなく書く手法として、**EARS（Easy Approach to Requirements Syntax）**が事実上の標準になっています。EARS は Rolls-Royce の Alistair Mavin らが航空機エンジンの制御システム向け要件を分析する中で開発し、2009 年に発表した記法です（[提唱者による公式解説](https://alistairmavin.com/ears/)を一次情報として確認）。

基本構造は次の 1 文型に統一されています。

```text
While <任意の事前条件>, when <任意のトリガー>, the <システム名> shall <システムの応答>
```

代表的なパターンは 5 つです。

| パターン | キーワード | 例 |
|---|---|---|
| Ubiquitous（恒常要件） | なし | The mobile phone shall have a mass of less than XX grams. |
| Event-driven（イベント駆動） | When | When "mute" is selected, the laptop shall suppress all audio output. |
| State-driven（状態駆動） | While | While in low-power mode, the device shall … |
| Optional feature（オプション機能） | Where | Where the car has a sunroof, the car shall have a sunroof control panel on the driver door. |
| Unwanted behaviour（望まない挙動） | If / Then | If an invalid credit card number is entered, then the website shall display "please re-enter credit card details". |

**EARS 自体は spec-kit 固有の記法ではありません。** spec-kit の README・解説文書には EARS への直接の言及は見当たりませんでしたが、`/speckit.checklist` が目指す「曖昧さのない受け入れ基準」を書く際の実務的な選択肢として、多くのチームが EARS を使っています。

## AI-DLC との関係 — どちらを選ぶか

[AI-DLC ワークフロー](aidlc-workflows.md)（AWS Labs）も、AI エージェントに構造化された手順を強制するという点で SDD と同じ問題意識を持っています。**AI-DLC は SDD の実装の 1 つ**という位置づけで捉えると読みやすくなります。両者の違いは次の軸に整理できます。

| 軸 | GitHub Spec Kit | AI-DLC |
|---|---|---|
| 提供元 | GitHub（コミュニティ主導） | AWS Labs |
| 単位 | 機能（feature）ごとに `specify → plan → tasks → implement` | プロジェクトの複雑さに応じて自動的に適応する 3 フェーズ（Inception / Construction / Operations） |
| 起動方法 | CLI (`specify init`) でエージェント別ファイルを生成し、スラッシュコマンドで進める | チャットに「Using AI-DLC, …」と書くだけで起動 |
| 拡張性 | プリセット・Extension・Community Bundle による差し替えが前提 | ルールファイルによる問題行動の抑制が中心 |
| 収束の確認 | `/speckit.converge` が明示的な「Converged」判定を出す | 明示的な収束コマンドは確認できていない |

**選び方の軸は「仕様を書く単位をどこに置くか」です。** 機能単位で仕様・計画・タスクを積み重ね、`/speckit.converge` で明示的に収束を確認したいなら spec-kit、既存のプロジェクト全体に対して「着想 → 設計実装 → 運用」という 3 段階のフェーズ管理をルールファイルで強制したいなら AI-DLC が近い選択です。両方を同じプロジェクトで併用する場合の一次情報は確認できていないため、本文では扱いません。

---

## 関連ドキュメント

- [AI-DLC ワークフロー](aidlc-workflows.md) — AWS Labs による SDD の実装。3 フェーズの適応型ワークフロー
- [コーディングエージェントの選び方](coding-agents.md) — `AGENTS.md` など、エージェント横断の設定ファイルの位置づけ
- [Skill / Plugin のセキュリティ](skill-security.md) — spec-kit が生成するコマンドファイル・スクリプトを導入する前に確認すること

## 参考リンク

- [github/spec-kit](https://github.com/github/spec-kit) — リポジトリ本体（公式・MIT）
- [spec-driven.md](https://github.com/github/spec-kit/blob/main/spec-driven.md) — SDD 方法論の解説文書（公式）
- [Supported AI Coding Agent Integrations](https://github.github.io/spec-kit/reference/integrations.html) — 対応エージェントの一覧（公式・随時更新）
- [Spec Kit Documentation](https://github.github.io/spec-kit/) — コマンドリファレンス・Extension・Preset・Community Bundle（公式）
- [EARS: Easy Approach to Requirements Syntax](https://alistairmavin.com/ears/) — 提唱者 Alistair Mavin による公式解説（一次情報・2009 年発表）
