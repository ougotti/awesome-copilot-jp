# Skill / エージェントの評価（evals） — 入れた後に効いているかを測る

> **対象ツール**: ツール横断（GitHub Copilot・Claude Code・Codex ほか） ｜ **実行環境**: CLI（ターミナル） ｜ **対象読者**: エンジニア ｜ **最終更新**: 2026-09-07

> [Skill / Plugin のセキュリティ](skill-security.md)は「**導入前**に入れてよいものか」を扱います。このページはその先、「**導入後に実際に効いているか**」を測る話です。両者は別軸で、片方をやれば済むわけではありません。

---

## 1. なぜ測るのか

Skill は増やすほどコンテキストを圧迫し、意図しないものが選ばれることがあります（[skills.sh ガイド「選ぶときの注意」](skills-sh.md#選ぶときの注意)で触れている問題の裏返しです）。増やした・変更した分だけ、それが実際に効いているかを確認する側の設計も必要になります。

「効いている」は当たり前には成立しません。SkillsBench（[arXiv:2602.12670](https://arxiv.org/abs/2602.12670)）は、複数タスク・複数ドメイン・複数の model-harness 構成で Curated Skills の効果を計測し、**平均では成功率が改善する一方、ドメインや構成によって効果の大きさは大きくばらつき、改善が乏しい構成もある**と報告しています。「Skill を入れれば必ず伸びる」とは言えません。具体的な数値はアブストラクトで直接確認してください（取得日: 2026-09-07）。

## 2. 退行の典型パターン

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

## 3. 測り方の最小手順

OpenAI の解説記事は 8 段階の手順を示していますが、最小限に絞ると次の流れになります。

1. **成功の定義を先に決める** — 結果（outcome）・手順（process）・スタイル（style）・効率（efficiency）のどれを測るかを決めておく
2. **実際に起きた失敗を題材にタスクを作る** — 10〜20 件程度で十分。明示的な呼び出し・暗黙的な呼び出し・**呼ばれてはいけない場面（ネガティブコントロール）**を混ぜる
3. **同一ケース・同一モデル・同一試行回数で「Skill あり / なし」を比較する** — 変更の因果効果を見るには、この対照が要る
4. **決定論的な採点を基本にする** — テキスト一致、JSON 検証、ファイル存在確認、スクリプトによるオラクル判定。スタイルなど自動判定しにくい部分だけ、構造化ルーブリックや LLM ジャッジを補助的に使う
5. **変更のたびに回す** — 一度きりの計測ではなく、Skill を変更するたびに同じタスク集合で再実行する

LangChain の解説記事（“Evaluating Skills”, Robert Xu, 2026-03-05）は、自社のタスクで Claude Code を Skill なし / ありで比較したところ「Skill なしでは完了率が低く、Skill ありで大きく改善した」と報告しています（対象タスクやモデルの詳細は記事に明記されていないため、数値の一般化はできません）。同記事は判定に `trajectory_evaluator.py` という構造化出力（JSON）を期待値と照合するスクリプトを使い、Skill 呼び出しの有無・完了ステップ数・ターン数・実行時間を追跡しています。

## 4. 道具 — 「実行基盤のハーネス」と「評価用ハーネス」を区別する

[AI エージェントの実行基盤（ハーネス）](harness.md)でいう「ハーネス」は、**エージェントを動かす裏側の仕組み**（ツール呼び出し・状態管理・ループ制御）を指します。このページで扱う「eval harness」は同じ単語を使いますが指すものが違い、**変更前後の実行結果を集めて採点する測定用の実行環境**です。前者はエージェントを動かすための土台、後者はその土台の上で「変えた結果どうなったか」を記録・採点するための足場です。両方が「ハーネス」と呼ばれるため、文脈で区別してください。

| 道具 | 位置づけ | 提供元 | 状態 |
|------|---------|-------|------|
| Codex `codex exec --json` / `--output-schema` | 実行トレース（JSONL）の取得と構造化出力での採点をビルトインで提供 | Official（OpenAI） | GA |
| [adewale/skill-eval-harness](https://github.com/adewale/skill-eval-harness) | 同一ケース・同一モデル・同一試行回数で Skill あり / なしを比較し、決定論的に採点する | Community | — |

`skill-eval-harness` は Claude・Codex・Gemini・Mistral Vibe・Pi・Jetty（と検証用のスタブランナー）に対応し、MIT ライセンスで公開されています。採点はテキスト一致・正規表現・JSON 検証・ファイル存在確認・スクリプトオラクルによる決定論的な方式が基本で、モデル呼び出しを伴う LLM ジャッジは任意機能として用意されています。テストケースに含めた正解が実行ログへ漏れていないかを検知する "leakage lint" を持ち、再現性を損なわないための工夫になっています。

## 5. 人が見る範囲

自動採点で代替できるのは「決められた基準に対して合っているか」までです。**基準そのものが正しいか**、**スタイルや業務判断が妥当か**は、自動採点の外に残ります。[生成AIを業務で安全に使う「出力を受け取った後に確認すること」](../business/safety.md#出力を受け取った後に確認すること)が挙げる数値・固有名詞・事実・抜け漏れ・体裁の確認は、Skill の出力についても同じように人の目が必要です。evals は「毎回人が全部読む」手間を減らす仕組みであって、その確認をゼロにする仕組みではありません。

---

## 関連ドキュメント

- [Skill / Plugin のセキュリティ](skill-security.md) — **導入前**に入れてよいかを判断する軸（このページは**導入後**）
- [AI エージェントの実行基盤（ハーネス）](harness.md) — 「ハーネス」という同じ語が指す、動かす側の仕組み
- [skills.sh ガイド](skills-sh.md) — Skill を増やしすぎない選び方
- [Codex スキルカタログ](../codex/catalog.md) — `description` の書き方の具体例
- [生成AIを業務で安全に使う](../business/safety.md) — 出力を受け取った後に人が確認する項目

## 参考リンク

- [Testing Agent Skills Systematically with Evals](https://developers.openai.com/blog/eval-skills) — 8 段階の評価手順（OpenAI 公式）
- [Evaluating Skills](https://www.langchain.com/blog/evaluating-skills) — Robert Xu、2026-03-05（LangChain 公式）
- [adewale/skill-eval-harness](https://github.com/adewale/skill-eval-harness) — 決定論的な採点を行う比較用ハーネス（Community・MIT）
- [SkillsBench: Benchmarking How Well Agent Skills Work Across Diverse Tasks](https://arxiv.org/abs/2602.12670) — arXiv:2602.12670、2026-02-13 投稿
