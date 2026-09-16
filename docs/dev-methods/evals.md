# Skill / エージェントの評価（evals） — 変更時の回帰と本番品質を分けて測る

> **対象ツール**: ツール横断（GitHub Copilot・Claude Code・Codex・本番エージェント基盤ほか） ｜ **実行環境**: CLI（ターミナル）/ Cloud ｜ **対象読者**: エンジニア ｜ **最終更新**: 2026-09-17

> [Skill / Plugin のセキュリティ](skill-security.md)は「**導入前**に入れてよいものか」を扱います。このページはその先、「**変更した Skill / Plugin が効いているか**」と「**本番エージェントが目的を達成しているか**」を測る話です。両者は対象と実行頻度が異なります。

---

## 1. 最初に分ける — 回帰評価・本番品質・インフラ監視

「エージェントの評価」には、少なくとも次の 3 つがあります。観測に同じ trace を使う場合でも、問いと合格条件は同じではありません。

| 区分 | 確認する問い | 主な評価対象 | 実行する時点 |
|------|-------------|-------------|-------------|
| **Skill / Plugin の回帰評価** | 変更によって期待した挙動になったか | 発火、手順、出力、tool の利用・順序、生成ファイル | 導入前後、変更時、CI |
| **本番エージェントの品質評価** | 実際の利用で目的を達成し続けているか | goal completion、helpfulness / correctness、tool 選択・引数、routing / trajectory | リリース前の履歴評価、本番 traffic の継続評価、障害調査 |
| **インフラ・実行時監視** | 実行基盤が正常か | latency、error、timeout、throttling、権限、リソース | 本番稼働中 |

このページの 2〜5 節は **Skill / Plugin の回帰評価**を詳しく扱い、6 節で**本番エージェントの品質評価**を選ぶ軸を整理します。インフラ監視と trace の取得方法は [AI エージェントの実行基盤（ハーネス）](harness.md#動かした後に何が見えるか--opentelemetry-genai-semantic-conventions) を参照してください。インフラのメトリクスが正常でも、誤った tool 選択や目的未達は起こり得るため、品質評価の代わりにはなりません。

## 2. Skill / Plugin をなぜ測るのか

Skill は増やすほどコンテキストを圧迫し、意図しないものが選ばれることがあります（[skills.sh ガイド「選ぶときの注意」](skills-sh.md#選ぶときの注意)で触れている問題の裏返しです）。増やした・変更した分だけ、それが実際に効いているかを確認する側の設計も必要になります。

「効いている」は当たり前には成立しません。SkillsBench（[arXiv:2602.12670](https://arxiv.org/abs/2602.12670)）は、複数タスク・複数ドメイン・複数の model-harness 構成で Curated Skills の効果を計測し、**平均では成功率が改善する一方、ドメインや構成によって効果の大きさは大きくばらつき、改善が乏しい構成もある**と報告しています。「Skill を入れれば必ず伸びる」とは言えません。具体的な数値はアブストラクトで直接確認してください（取得日: 2026-09-07）。

## 3. Skill / Plugin の退行パターン

Skill を追加・変更したときに起きる失敗は、だいたい次の型に収まります。

| パターン | 内容 |
|---------|------|
| ① 発火しない | 呼ぶべき場面でエージェントが Skill を選ばない |
| ② 過剰に発火する | 関係のない場面でも Skill を選んでしまう（false positive） |
| ③ 必要な手順を飛ばす | 発火はするが、途中のステップを省略する |
| ④ 余計なファイルを残す | 作業後の後始末ができていない |

①②は多くの場合、`description` の書き方に起因します。OpenAI の解説記事は次のように述べています。

> The name and description matter more than they might seem. They're the primary signals Codex uses to decide _whether_ to invoke the skill at all.

逆に `description` が曖昧・広すぎると、「隣接する要求にも意図せず一致してしまい、Codex が積極的すぎる選択をする」（過剰発火）という指摘もあります。`description` の具体的な書き方（良い例・悪い例）は [Codex スキルカタログ「`description` の書き方」](../codex/catalog.md#description-の書き方)にすでにまとまっているため、ここでは重複させず、**その書き方が自動選択の精度をどれだけ左右するか**という評価側の理由づけだけを補います。

## 4. Skill / Plugin を測る最小手順

OpenAI の解説記事は 8 段階の手順を示していますが、最小限に絞ると次の流れになります。

1. **成功の定義を先に決める** — 結果（outcome）・手順（process）・スタイル（style）・効率（efficiency）のどれを測るかを決めておく
2. **実際に起きた失敗を題材にタスクを作る** — 10〜20 件程度で十分。明示的な呼び出し・暗黙的な呼び出し・**呼ばれてはいけない場面（ネガティブコントロール）**を混ぜる
3. **同一ケース・同一モデル・同一試行回数で「Skill あり / なし」を比較する** — 変更の因果効果を見るには、この対照が要る
4. **決定論的な採点を基本にする** — テキスト一致、JSON 検証、ファイル存在確認、スクリプトによるオラクル判定。スタイルなど自動判定しにくい部分だけ、構造化ルーブリックや LLM ジャッジを補助的に使う
5. **変更のたびに回す** — 一度きりの計測ではなく、Skill を変更するたびに同じタスク集合で再実行する

LangChain の解説記事（“Evaluating Skills”, Robert Xu, 2026-03-05）は、自社のタスクで Claude Code を Skill なし / ありで比較したところ「Skill なしでは完了率が低く、Skill ありで大きく改善した」と報告しています（対象タスクやモデルの詳細は記事に明記されていないため、数値の一般化はできません）。同記事は判定に `trajectory_evaluator.py` という構造化出力（JSON）を期待値と照合するスクリプトを使い、Skill 呼び出しの有無・完了ステップ数・ターン数・実行時間を追跡しています。

## 5. 道具 — 「実行基盤のハーネス」と「評価用ハーネス」を区別する

[AI エージェントの実行基盤（ハーネス）](harness.md)でいう「ハーネス」は、**エージェントを動かす裏側の仕組み**（ツール呼び出し・状態管理・ループ制御）を指します。このページで扱う「eval harness」は同じ単語を使いますが指すものが違い、**変更前後の実行結果を集めて採点する測定用の実行環境**です。前者はエージェントを動かすための土台、後者はその土台の上で「変えた結果どうなったか」を記録・採点するための足場です。両方が「ハーネス」と呼ばれるため、文脈で区別してください。

| 道具 | 位置づけ | 提供元 | 状態 | 前提・注意 |
|------|---------|-------|------|-----------|
| Codex `codex exec --json` / `--output-schema` | 実行トレース（JSONL）の取得と構造化出力での採点をビルトインで提供 | Official（OpenAI） | GA | 利用するモデルの料金・利用枠に従う |
| Claude Code `claude plugin eval` | Plugin あり / なしの反復実行、grader による採点、JSON / HTML report をビルトインで提供 | Official（Anthropic） | GA | 2.1.269 以降。server-side の利用可否に従う |
| [adewale/skill-eval-harness](https://github.com/adewale/skill-eval-harness) | 同一ケース・同一モデル・同一試行回数で Skill あり / なしを比較し、決定論的に採点する | Community | Experimental | 利用する各 CLI とモデルの料金・利用枠に従う |

`skill-eval-harness` は Claude・Codex・Gemini・Mistral Vibe・Pi・Jetty（と検証用のスタブランナー）に対応し、MIT ライセンスで公開されています。採点はテキスト一致・正規表現・JSON 検証・ファイル存在確認・スクリプトオラクルによる決定論的な方式が基本で、モデル呼び出しを伴う LLM ジャッジは任意機能として用意されています。テストケースに含めた正解が実行ログへ漏れていないかを検知する "leakage lint" を持ち、再現性を損なわないための工夫になっています。

### Claude Code 組み込みの `plugin eval`

`claude plugin eval init` は Plugin の `evals/` に case と grader の草案を作り、`claude plugin eval .` が suite を実行します。各 case は既定で Plugin あり / なしをそれぞれ 3 回実行し、両者の score と差分 `Δ` を出します。「Claude 自体が解けただけ」を Plugin の効果と数えないための baseline です。

| grader | 確認すること |
|--------|-------------|
| `regex` | 最終応答、trace、生成ファイルの内容が pattern に一致するか |
| `tool_used` / `tool_order` | Skill や別の tool を呼んだか、順序を守ったか |
| `file_exists` | 指定した成果物を新規作成したか |
| `llm` / `baseline` | 決定論的に書けない品質を rubric または基準 transcript と比較できるか |

結果は JSON と HTML report に残り、threshold 未達を終了コード 1 として CI の gate にできます。ただしモデル呼び出しは利用枠または API 料金を消費し、LLM judge は結果が揺れます。まず `regex`、tool、file の grader を置き、必要な部分だけ LLM judge にします。

実行ごとに一時的な home / workspace / Claude Code 設定を使い、個人の `CLAUDE.md`、memory、他の Plugin や MCP server は読み込みません。Bash、Write、Edit、WebFetch などは `--allow-tools` で明示的に許可します。一方、対象 Plugin の hooks と、起動を許した実 MCP server は agent の sandbox 外で動き得るため、**eval の合格を安全性の証明にはできません**。

`claude plugin validate` は manifest や frontmatter の**構造検査**です。`plugin eval` は prompt から始まる**挙動と退行の検査**であり、置き換え関係ではありません。

## 6. 本番エージェントの品質を継続評価する

本番では、固定した少数のテストケースに合格するだけでなく、利用者の表現、データ、tool の応答、会話の長さが変わっても品質を保てるかを見ます。最初に次の単位を決めます。

| 評価単位 | 例 | 向いている採点 |
|---------|----|---------------|
| 応答 | 回答は正確で役に立ったか | rubric、参照回答との比較、人の確認 |
| tool call | 適切な tool と引数を選んだか | tool 名・引数の検証、実行結果との照合 |
| session / trajectory | 最終目的を達成し、妥当な経路を通ったか | goal completion、経路・routing の検証 |

評価のかけ方は、**on-demand / batch** と **online** に分けると選びやすくなります。前者は選んだ履歴や障害事例を再評価し、修正の確認やリリース判定に使います。後者は本番 interaction の一部または全部を継続的に採点し、時間経過による品質低下や特定パターンの失敗を検知します。

最小構成は、次の順序です。

1. 業務上の成功を goal completion として定義し、tool 選択・正確さ・応答品質などの補助指標を決める
2. 同意・個人情報・保存期間を確認し、評価へ渡せる trace / transcript の範囲を決める
3. 既知の失敗を on-demand で採点し、人の判定と evaluator のずれを確認する
4. 本番では対象を sampling して継続評価し、model・prompt・tool・route の版ごとに推移を見る
5. 閾値低下を自動停止へ直結させず、代表例を人が確認してから原因別にテストケースへ戻す

LLM-as-a-Judge の score は evaluator の model や prompt でも変わります。sampling した非同期評価は、評価対象外の interaction を保証せず、問題のある応答を利用者へ返す前に止める guardrail にもなりません。評価費用、機密情報、誤判定を含めて運用してください。

### AWS 固有の実装例 — Amazon Bedrock AgentCore Evaluations

> **提供元**: Official（AWS） ｜ **状態**: GA ｜ **確認日**: 2026-09-17

Amazon Bedrock AgentCore Evaluations は、2026-03-31 に GA となった AWS のサービスです。OpenTelemetry / OpenInference で取得した trace を共通形式へ変換し、組み込みまたは custom evaluator で採点します。AgentCore Runtime 内だけでなく、外部でホストしたエージェントも対象にできます。公式文書では、end-to-end の goal attainment、tool の正確さ、独自の品質指標を評価対象として挙げています。

- **Online evaluation** — 監視する data source、evaluator、parameter を設定して本番 traffic を継続評価する
- **On-demand evaluation** — 指定した span / trace だけを採点し、報告された問題や修正後の挙動を調べる
- **組み込み / custom evaluator** — helpfulness などの組み込み evaluator と、業務固有の evaluator を使い分ける

AWS の本番監視例では、AgentCore Evaluations による品質評価と AWS DevOps Agent によるインフラ調査を 2 層として組み合わせています。これは AWS サービスを使った構成例であり、すべてのエージェント基盤が同じ機能や統合を持つという意味ではありません。他の基盤へ適用するときは、同じ製品名ではなく「品質」と「インフラを別の問いとして測る」という区分だけを持ち込みます。

## 7. 人が見る範囲

自動採点で代替できるのは「決められた基準に対して合っているか」までです。**基準そのものが正しいか**、**スタイルや業務判断が妥当か**は、自動採点の外に残ります。[生成AIを業務で安全に使う「出力を受け取った後に確認すること」](../business/safety.md#出力を受け取った後に確認すること)が挙げる数値・固有名詞・事実・抜け漏れ・体裁の確認は、Skill の出力と本番エージェントの応答についても同じように人の目が必要です。evals は「毎回人が全部読む」手間を減らす仕組みであって、その確認をゼロにする仕組みではありません。

---

## 関連ドキュメント

- [Skill / Plugin のセキュリティ](skill-security.md) — **導入前**に入れてよいかを判断する軸（このページは**導入後**）
- [AI エージェントの実行基盤（ハーネス）](harness.md) — 「ハーネス」という同じ語が指す、動かす側の仕組み
- [skills.sh ガイド](skills-sh.md) — Skill を増やしすぎない選び方
- [Codex スキルカタログ](../codex/catalog.md) — `description` の書き方の具体例
- [生成AIを業務で安全に使う](../business/safety.md) — 出力を受け取った後に人が確認する項目
- [長時間タスクの信頼性設計](agent-reliability.md) — 「性能を測る」評価とは別軸の、「実行中の故障にどう耐えるか」という設計

## 参考リンク

- [Testing Agent Skills Systematically with Evals](https://developers.openai.com/blog/eval-skills) — 8 段階の評価手順（OpenAI 公式）
- [Evaluating Skills](https://www.langchain.com/blog/evaluating-skills) — Robert Xu、2026-03-05（LangChain 公式）
- [adewale/skill-eval-harness](https://github.com/adewale/skill-eval-harness) — 決定論的な採点を行う比較用ハーネス（Community・MIT）
- [Test plugins with evals](https://code.claude.com/docs/en/plugin-evals) — suite、baseline、grader、JSON / HTML report、分離と CI（Anthropic 公式）
- [Claude Code v2.1.269](https://github.com/anthropics/claude-code/releases/tag/v2.1.269) — `claude plugin eval` の追加（Anthropic 公式・2026-09-11）
- [SkillsBench: Benchmarking How Well Agent Skills Work Across Diverse Tasks](https://arxiv.org/abs/2602.12670) — arXiv:2602.12670、2026-02-13 投稿
- [Evaluate agent performance with Amazon Bedrock AgentCore Evaluations](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/evaluations.html) — 対象、telemetry、評価方式（AWS 公式）
- [Amazon Bedrock AgentCore Evaluations is now generally available](https://aws.amazon.com/about-aws/whats-new/2026/03/agentcore-evaluations-generally-available/) — 2026-03-31 の GA 発表（AWS 公式）
- [How AgentCore Evaluations works](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/how-it-works-evaluations.html) — goal attainment、tool の正確さ、AgentCore 外のエージェント対応（AWS 公式）
- [Online evaluation](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/online-evaluations.html) / [On-demand evaluation](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/on-demand-evaluations.html) — 継続評価と指定 trace の評価（AWS 公式）
- [Monitoring production agent lifecycle with AWS DevOps Agent and AgentCore Evaluations](https://aws.amazon.com/blogs/machine-learning/monitoring-production-agent-lifecycle-with-aws-devops-agent-and-agentcore-evaluations/) — 品質評価とインフラ監視を分けた AWS 構成例（AWS 公式、2026-09-11）
