# 仕様駆動開発（SDD） — 仕様を実行可能な入力にする

> **対象ツール**: ツール横断（GitHub Copilot・Claude Code・Cursor・Codex・Kiro など） ｜ **実行環境**: CLI / IDE ｜ **対象読者**: エンジニア ｜ **最終更新**: 2026-09-18

> このページは GitHub Spec Kit を中心に、OpenSpec・BMAD Method・Kiro Specsとの選び方を整理します。コマンド名・生成物・対応エージェントは変わるため、導入時は各公式ドキュメントを確認してください。以下の `状態` は公式発表に明示された成熟度だけを記し、明記がないものは `—` とします。

---

## SDD とは何か

**仕様駆動開発（Spec-Driven Development, SDD）**は、仕様を先に書き、それを実装の入力にする開発手法です。spec-kit の解説文書は次のように定義しています。

> Specifications don't serve code—code serves specifications.（仕様がコードに従うのではなく、コードが仕様に従う）

従来、PRD や設計ドキュメントは実装を導くための「添え物」で、コードが真実であり、仕様はコードに追いつけないまま陳腐化していきました。SDD はこの上下関係を反転させます。**仕様と実装計画そのものを実行可能にする**ことで、仕様とコードの間のギャップを「埋める」のではなく「なくす」という考え方です。

AI コーディングエージェントの力を借りて初めて現実的になった手法である点も押さえておく必要があります。仕様を理解し、精密な実装計画を生成し、そこからコードを作る一連の作業を、構造化された手順なしに AI に丸投げすると混乱を招きます。SDD はその構造（仕様 → 計画 → タスク → 実装）を提供します。

## GitHub Spec Kit のワークフロー

**GitHub Spec Kit**（[github/spec-kit](https://github.com/github/spec-kit)、MIT ライセンス）は、SDD を具体的なコマンド列として実装した拡張可能な process harness です。主要なコーディングエージェントを広くカバーしています。対応エージェントの一覧は `specify integration list` または [公式の対応表](https://github.github.io/spec-kit/reference/integrations.html) で確認してください（件数は変わりやすいため本文には書きません）。

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

既存projectへ導入する場合は、greenfieldと同じ前提で初期化せず、[公式のexisting-project guide](https://github.github.com/spec-kit/guides/existing-projects.html)から始めます。既存のarchitecture、規約、テスト、未完了作業を先に把握し、最初のfeatureを小さく限定してください。

## リポジトリに何ができるか

`specify init <project> --integration <agent>` を実行すると、選んだエージェント向けのコマンドファイルとディレクトリ構成が生成されます。テンプレートは 4 段階の優先順位で解決されます。

| 優先度 | 層 | 場所 |
|---|---|---|
| 高 | プロジェクトローカルの上書き | `.specify/templates/overrides/` |
| ↓ | プリセット（用語・テンプレートの差し替え） | `.specify/presets/templates/` |
| ↓ | Extension（機能追加） | `.specify/extensions/templates/` |
| 低 | spec-kit コア（組み込みの SDD コマンド・テンプレート） | `.specify/templates/` |

**このガイドが扱う `AGENTS.md`（[コーディングエージェントの選び方](coding-agents.md)）との関係は、spec-kit の公式ドキュメントに明示的な記述が見当たりませんでした。** 断定を避け、両者は別のファイルとして併存する、という事実だけをここに書きます。

## 近い4者は同じ種類ではない

4者はいずれも実装前の意図を構造化しますが、**方法論、CLI / framework、製品組み込み機能が混在しています**。まず提供形態を分けてください。

| 選択肢 | 提供元 / 表記 | 公開形態・license・状態 | 何であるか | 主な開始単位 | coding agentとの関係 |
|---|---|---|---|---|---|
| **GitHub Spec Kit** | GitHub / Official | OSS・MIT・`—` | SDDをcoreに持つCLI / process harness | feature、bug、idea | agent別integrationとgeneric integrationを持つ。特定のagentに固定しない |
| **OpenSpec** | Fission AI / Community | OSS・MIT・`—` | change deltaを管理する軽量なspec framework / CLI | change | 対応tool向けにSkills / commandsを生成。成果物はplain Markdown |
| **BMAD Method** | BMAD community / Community | OSS・MIT・`—` | Agile AI-driven SDLC方法論 + Skills / Agents | intent、change、epic、project | Skills対応のcoding toolで使う。成果物は持ち出せるが、進行コマンドとmoduleはBMAD固有 |
| **Kiro Specs** | Kiro / Official | Kiro製品機能・license `—`・状態 `—` | IDE / CLI / Webに組み込まれたSpec機能 | feature、bug、Quick Spec session | Kiro内のworkflow。独立したOSS frameworkではない |

`—` は未提供という意味ではなく、公式ページでこの機能単位のGA / Preview表記を確認できなかったことを示します。OSSの更新度や製品全体の成熟度を推測で置き換えていません。

拡張の名前も互換ではありません。Spec Kitの **preset / extension / workflow / bundle** はprocessの構成要素、OpenSpecの **schema** はchangeが生成するartifactと依存順、BMADの **module / agent customization** は方法論の役割や専門領域、Kiroの **product settings / steering / hooks** はKiro内の動作設定です。同じ「カスタマイズ」でも、そのまま相互移植できる単位ではありません。

### flow・成果物・承認・同期を同じ粒度で見る

| 選択肢 | 基本flow | 主な成果物 / source of truth | 人が確認する境界 | 実装後の同期・回帰防止 |
|---|---|---|---|---|
| **Spec Kit** | Specify → Plan → Tasks → Implement → Converge | featureごとの `spec.md`・`plan.md`・`tasks.md` とproject constitution | Clarify / checklist / cross-artifact analysisを必要に応じて挟み、実装前に仕様品質を確認 | `converge`が実装と成果物の差を検出し、残作業を`tasks.md`へ追記。bug fixingは検証結果も残す |
| **OpenSpec** | Explore → Propose → Review → Apply → Archive | change folderの`proposal.md`・`specs/`・任意の`design.md`・`tasks.md`。現行仕様は`openspec/specs/` | codeを書く前にplain Markdownを直接編集するかagentへ修正を依頼 | Archive時にdelta requirementsをmain specsへmergeし、change folderを日付付きarchiveへ移動。履歴を削除しない |
| **BMAD** | intentの明確化 → 必要な調査・brief / PRFAQ / PRD / UX / architecture → SPEC → story / Build → review / test / retrospective | 規模に応じた文書群、`SPEC.md`、epicでは`stories.yaml`など。組織では既存PRDをownerにできる | 固定の一律gateではなく、規模・risk・組織のsign-offに応じて文書とcheckpointを増やす | 1回のBuild sessionを実装単位にし、epicはstoryへ分割。review、E2E test、retrospectiveまで方法論の範囲に含む |
| **Kiro Specs** | Featureは Requirements → Design → Tasks、または Design → Requirements → Tasks。Bugfix / Quickも選択可能 | Kiroがrepo内に作る`requirements.md`・`design.md`・`tasks.md`、Bugfixは`bugfix.md` | 標準Feature / Bugfixはphaseごとに確認。Quick Specは最初の質問後、phase間のapproval gateを省略 | Featureは反復更新。Bugfixはcurrent / expected / unchanged behaviorとproperty-based regression testを計画。共通のarchive mergeやconvergence commandはない |

### OpenSpec — change deltaをmain specsへ戻す

OpenSpecの特徴は、進行中の変更と現在の仕様を分けることです。`openspec/changes/<change>/`でproposal、delta requirements、design、tasksをreviewし、実装後のarchiveでdeltaを`openspec/specs/`へmergeします。変更フォルダー自体も日付付きarchiveへ移るため、「いま正しい仕様」と「なぜ変わったか」を別の場所で追えます。

既定のschemaは `proposal → specs → design → tasks` ですが、[custom schema](https://openspec.dev/docs/customize-schemas)で成果物、依存順、templateを変えられます。Presetでprocess全体の見え方を変えるSpec Kitとは違い、OpenSpecでは**changeが生成するartifact graph**を定義する拡張です。

### BMAD Method — work sizeに合わせて計画量を変える

BMADはspec作成だけの道具ではありません。まずintentが十分に明確かを見て、足りなければideation、research、brief / PRFAQ / PRD、UX、architectureなど必要な活動だけを選びます。明確になったintentを`bmad-spec`へ渡し、1回のBuild sessionに収まればそのまま実装し、epicならstoryへ分解し、複数epicのprojectなら共有contextとcoordinationを追加します。

つまり「すべての案件で重い工程を通す」のではなく、risk、曖昧さ、architectureへの影響、team間調整に応じて深さを変える方法論です。明白で低riskな小修正にはBMAD自体が不要な場合もある、と公式ガイドも案内しています。

### Kiro Specs — 製品内でFeature / Bugfix / Quickを選ぶ

KiroのFeature Specsは、振る舞いから始める **Requirements-First** と、architecture・algorithm・非機能制約から始める **Design-First** を分けます。前者の`requirements.md`はEARS形式を使います。開始後にflowを切り替えるのではなく、必要なら別Specを作成します。

- **Feature Spec**: 要件や設計を反復し、phaseごとにreviewしたい機能開発。
- **Quick Spec**: よく理解した変更向け。最初にscope・constraint・edge caseを答え、`requirements.md`・`design.md`・`tasks.md`を一度に作る。phase間のapproval gateはない。
- **Bugfix Spec**: `bugfix.md`へcurrent / expected / unchanged behaviorを書き、`design.md`でroot causeと修正案を整理する。tasksには再現、修正、非退行を確かめるproperty-based testを含める。

Kiro Specsの成果物はrepoに残せますが、workflowの実行、承認UI、agentとの連携はKiro製品の機能です。他のagentで同じMarkdownを読むことと、Kiro Specs自体が可搬なframeworkであることは別です。

## どれを選ぶか

| 状況 | 最初に試す候補 | 判断理由 |
|---|---|---|
| **小さく明確な変更** | 既存agent + 最小限のissue / test。構造が必要ならSpec Kit、OpenSpec、Kiro Quick Spec | 方法論を導入する費用が変更自体を上回らないようにする。BMADも明白な低risk変更には不要としている |
| **brownfieldで仕様を継続管理したい** | OpenSpec | change deltaをreviewし、archive時にmain specsへ反映するため、現在仕様と変更履歴の境界が明確 |
| **複数epic・複数teamを含むSDLC全体** | BMAD Method | intent形成、調査、PRD、UX、architecture、story、Build、review、test、retrospectiveまで規模に応じて広げられる |
| **すでにKiroを使い、製品内の承認UIも使いたい** | Kiro Specs | Feature / Bugfix / QuickをKiro内で選び、EARS、phase approval、実装taskまで一続きに扱える |

Spec Kitはその中間に置きやすい選択肢です。agentを固定せず、feature単位の標準processと明示的なconvergenceを揃えたい場合に向きます。bug fixingやidea assessmentはcore SDDの必須phaseではなく、独立したopt-in extensionです。

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

## AI-DLCは別系統のライフサイクル実装

[AI-DLC Workflows](aidlc-workflows.md)（AWS Labs）も、要件や設計を実装前に確認し、AIエージェントの作業を構造化します。Spec Kitが仕様を実装の中心に置くのに対し、AI-DLCは初期化から運用までのライフサイクル全体を扱います。両者は対象が重なりますが、同じ手法や公式な連携機能ではありません。

| 軸 | GitHub Spec Kit | AI-DLC |
|---|---|---|
| 提供元 | GitHub | AWS Labs |
| 単位 | 機能（feature）ごとに `specify → plan → tasks → implement` | 5フェーズ、33ステージと複数のワークフロープロファイル |
| 起動方法 | CLI (`specify init`) でエージェント別ファイルを生成し、スラッシュコマンドで進める | `aidlc config`でハーネスを設定し、`/aidlc`または`$aidlc`で開始 |
| 拡張性 | プリセット・Extension・Community Bundle による差し替えが前提 | ステージ、エージェント、ルール、知識、プラグインを変更可能 |
| 進行の確認 | `/speckit.converge` が明示的な「Converged」判定を出す | 成果物、永続状態、監査履歴、人の承認ゲートで確認 |

**選び方の軸は「仕様変更の管理方法を選ぶのか、開発ライフサイクル全体の実行系を選ぶのか」です。** 上の4者比較は主に仕様とcoding agentの進め方を見ています。着想から運用までの工程、専門agent、承認、監査履歴を一つの実行系で扱いたい場合はAI-DLCも候補になります。AI-DLCは4者の別名や上位版ではなく別系統であり、併用する公式手順も確認できていないため、先に一方を小さく試してください。

---

## 関連ドキュメント

- [AI-DLC Workflows](aidlc-workflows.md) — AWS Labsによる5フェーズの適応型ワークフロー
- [コーディングエージェントの選び方](coding-agents.md) — `AGENTS.md` など、エージェント横断の設定ファイルの位置づけ
- [Skill / Plugin のセキュリティ](skill-security.md) — spec-kit が生成するコマンドファイル・スクリプトを導入する前に確認すること

## 参考リンク

- [github/spec-kit](https://github.com/github/spec-kit) — リポジトリ本体（公式・MIT）
- [spec-driven.md](https://github.com/github/spec-kit/blob/main/spec-driven.md) — SDD 方法論の解説文書（公式）
- [Supported AI Coding Agent Integrations](https://github.github.io/spec-kit/reference/integrations.html) — 対応エージェントの一覧（公式・随時更新）
- [Spec Kit Documentation](https://github.github.io/spec-kit/) — コマンドリファレンス・Extension・Preset・Community Bundle（公式）
- [Adopting Spec Kit in an Existing Project](https://github.github.com/spec-kit/guides/existing-projects.html) — 既存projectへ段階的に導入する手順（公式）
- [OpenSpec Quickstart](https://openspec.dev/docs/quickstart) — changeの提案からarchiveまで（プロジェクト公式）
- [OpenSpec Schemas](https://openspec.dev/docs/customize-schemas) — artifact、依存順、templateの変更（プロジェクト公式）
- [Fission-AI/OpenSpec](https://github.com/Fission-AI/OpenSpec) — リポジトリ本体（Community・MIT）
- [Choose a Planning Path](https://docs.bmad-method.org/plan/choose-a-planning-path/) — intentとwork sizeによる計画経路（プロジェクト公式）
- [Skills and Agents](https://docs.bmad-method.org/reference/skills-and-agents/) — BMADのSkills / Agents（プロジェクト公式）
- [bmad-code-org/BMAD-METHOD](https://github.com/bmad-code-org/BMAD-METHOD) — リポジトリ本体（Community・MIT）
- [Kiro Feature Specs](https://kiro.dev/docs/specs/feature-specs/) — Requirements-First / Design-First（公式）
- [Kiro Bugfix Specs](https://kiro.dev/docs/specs/bugfix-specs/) — root causeとregression prevention（公式）
- [Kiro Quick Spec](https://kiro.dev/docs/specs/quick-spec/) — approval gateを省略するsession mode（公式）
- [EARS: Easy Approach to Requirements Syntax](https://alistairmavin.com/ears/) — 提唱者 Alistair Mavin による公式解説（一次情報・2009 年発表）
