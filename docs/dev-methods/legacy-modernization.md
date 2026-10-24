# レガシーのモダナイゼーションをエージェントで進める

> **対象ツール**: ツール横断（GitHub Copilot・Claude Code・AWS Transform ほか） ｜ **実行環境**: CLI / IDE / Cloud ｜ **対象読者**: 既存システムの移行を計画する開発者・アーキテクト・プロジェクトの責任者 ｜ **最終更新**: 2026-10-24

> COBOL から Java へ、古い Java から新しい版へ、といった移行にコーディングエージェントを使う手順が、Microsoft・GitHub・AWS などから公開されています。共通しているのは、**いきなり変換させず、まず既存の振る舞いを取り出して固定してから移す**という順番です。このページは、公開されている手順と製品を比べ、各段階でエージェントに任せること・人が決めることと、失敗しやすい点をまとめます。数値の主張（削減した時間・正確性）は、一次資料で確認できたものだけを書きます。

---

## 1. 移行の段階 — 任せることと決めること

| 段階 | エージェントに任せること | 人が決めること・確かめること |
|---|---|---|
| **1. 理解・文書化** | 呼び出し関係・依存関係の抽出、図の生成、業務ロジックの要約、母国語でないコメントの翻訳 | 抽出した業務ルールが正しいか（**業務の専門家が確認する**）。コードに書かれていない暗黙の仕様の補足 |
| **2. 振る舞いの固定** | 既存の振る舞いに対するテストの生成、テストデータの作成 | テストが本当に既存の振る舞いを表しているか。入出力の境界条件 |
| **3. 分割・計画** | 業務ドメインごとの分割案、移行の順番（wave）の案 | どこから移すか。最初は小さく、影響の少ないところから |
| **4. 変換** | ドメインごとのコードの変換、テストを通すまでの修正 | 変換後のコードを**社内のチームが保守できるか**。設計を引き継ぐか作り直すか |
| **5. 検証・切り替え** | 新旧の出力の比較、差分の報告 | 切り替えの判断、戻し方、並行稼働の期間 |

段階 1 と 2 の成果物（文書・テスト）は、以降のすべての段階の**正本**になります。Markdown などの読める形で残し、変換のたびに参照させます。[仕様駆動開発](spec-driven.md)の「仕様を実行可能な入力にする」考え方を、既存システムから仕様を取り出す方向に使う形です。

## 2. 公開されている手順と製品

| 取り組み | 形態 | 進め方の特徴 | `提供元` / `状態` |
|---|---|---|---|
| **Microsoft の COBOL 移行の取り組み**（[2025-07-09](https://devblogs.microsoft.com/all-things-azure/how-we-use-ai-agents-for-cobol-migration-and-mainframe-modernization/)） | OSS のフレームワーク [Azure-Samples/Legacy-Modernization-Agents](https://aka.ms/cobol)（Semantic Kernel） | デンマークの銀行向け IT 企業 Bankdata のコードで試した。COBOL の解析・Java（Quarkus）への変換・依存関係の地図を、役割ごとのエージェントに分けて調整役が回す | Official（Microsoft） / サンプル |
| **GitHub の解説**（[2025-10-14](https://github.blog/ai-and-ml/github-copilot/how-github-copilot-and-ai-agents-are-saving-legacy-systems/)） | Copilot での対話的な作業と、上記のフレームワークでの自動化 | 準備（リバースエンジニアリング）→ 補強（AI が理解しやすくする）→ 自動化（テスト駆動の移行）の 3 段階。**最初は 5,000 行未満の 1 つのシステムから**始めるよう勧める | Official（GitHub） |
| **AWS Transform for mainframe**（[User Guide](https://docs.aws.amazon.com/transform/latest/userguide/transform-app-mainframe.html)） | AWS のマネージドサービス | 目標を伝えると計画を立て、解析・文書化・業務ロジックの抽出・分割・計画・Java への変換を進める。分割や移行の順番などの**中間成果物は人の承認**を求める。z/OS の COBOL・PL/I・JCL・CICS・BMS・Db2・VSAM・IMS TM に加え、**富士通 GS21**（日本語の文字セット・PSAM・NDB）の変換にも対応 | Official（AWS） / GA |
| **AWS Transform とコーディングエージェントの組み合わせ**（[AWS ブログ](https://aws.amazon.com/blogs/migration-and-modernization/reimagining-mainframe-applications-with-aws-transform-and-claude-code/)） | AWS Transform で業務ルールを取り出し、Claude Code などで新しいサービスを作る | 既存の構造を保って変換する道（Refactor）と、取り出した業務ルールから作り直す道（Reimagine）を分ける。作り直す場合は、**生成した仕様を業務の専門家が確認してから**コードを作る | Official（AWS） |
| Anthropic の解説（[ウェビナー](https://www.anthropic.com/webinars/modernizing-legacy-code-with-claude-code)） | Claude Code での実演 | COBOL から Java への移行と、大きな Java のコードベースの版上げの実演（録画） | Official（Anthropic） |

> **データの扱いを最初に確認します。** 基幹システムのコードには機密の業務ロジックが含まれます。GitHub の解説は機密データを扱う場合にローカルのモデルを検討するよう述べ、AWS Transform のドキュメントは、データが利用しているのとは別のリージョンで処理されることがあると注記しています。コードを外部のモデルへ送ってよいかは、移行の計画より先に決めてください（[生成AIを業務で安全に使う](../business/safety.md)）。

## 3. 失敗しやすい点

| 失敗 | 何が起きるか | 公開資料の対処 |
|---|---|---|
| **文脈を詰め込みすぎる** | Microsoft の取り組みでは、文脈が多すぎるとエージェントの一貫性が崩れ、事実でない出力や作業の停止が起きた。呼び出しの階層は 3 段までしか扱えなかった | 文脈を短く保つ、前処理で要点だけを渡す、中間結果を Markdown に残して次の段階へ渡す |
| **暗黙の業務ルール** | 何十年分の業務ロジックや、文書になっていない仕様はコードだけから読み取れない | 業務の専門家が抽出結果を確認する。分からない箇所は分からないと書かせる |
| **検証の手段がない** | 変換が正しいかを判定できない | テストなどの**決定的な仕組み**で検証する（Microsoft の取り組みでも重要だったと述べている）。段階 2 を飛ばさない |
| **一度に全部を自動化しようとする** | 規模が大きいほど破綻しやすい | GitHub の解説は「ワンクリックで解決する」という主張を批判し、小さなシステムから始めるよう勧めている |
| **保守できないコードが大量にできる** | 自動変換したコードを社内のチームが理解できない | 変換後の可読性を受け入れの条件に入れる。AWS Transform は変換後のコードを Java らしく書き直す任意の段階（Reforge）を持つ |
| **知的財産を外に出しすぎる** | 移行の知識が外部に残り、社内に残らない | 文書とテストを自社の資産として管理する |

> **Hacker News での受け止め（コミュニティの見方）**: [Ask HN: COBOL devs, how are AI coding affecting your work?](https://news.ycombinator.com/item?id=46678550)（2026-01）では、COBOL の開発者から、ファイルレイアウトやテストデータの作成、長いマニュアルの検索、業務ルールの抽出には役立つという声と、固定桁の書式などの細部で誤りやすく、**レビューのほうが時間がかかって自分で書いたほうが早い**という声の両方が出ました。データベースの意味を知らないと正しく直せないこと、金融機関ではコードを外部のモデルへ送れないこと、制限された環境ではローカルで大きなモデルを動かすのも難しいこと、も繰り返し挙がっています。**段階 1・2 の人の確認と、データの扱いを先に決める必要がある**という点で、公開資料と同じ結論です。

## 4. 進め方の設計例

本ガイドの設計例です。対象のシステムと組織の制約に合わせて調整してください。

1. **データの扱いを決める** — どのモデルにコードを送ってよいか、ローカルで動かす必要があるか
2. **小さな対象を 1 つ選ぶ** — 影響が小さく、入出力がはっきりしたもの（バッチ処理の一部など）
3. **文書を作らせて、業務の専門家が読む** — 呼び出し関係の図、業務ルールの一覧。誤りを直し、正本として残す
4. **既存の振る舞いのテストを作る** — 旧システムで通ることを確かめる。通らないテストは、テストか理解のどちらかが誤っている
5. **変換させ、テストが通るまで直させる** — テストの書き換えで通していないかを確かめる（[AI 時代のコードレビュー](ai-code-review.md#1-実装と正しさの基準を分ける)）
6. **社内のチームが読めるかを確かめる** — 読めないなら、変換の方針（Refactor か Reimagine か）を見直す
7. **新旧を並べて動かす** — 同じ入力で出力を比べ、差分の理由を記録する
8. **次の対象へ広げる** — 1 つ目で作った文書・テスト・手順を [Skill](skill-publishing.md) にまとめ、次の対象に再利用する

長く続く移行は、途中で失敗する前提で設計します。段階ごとの成果物を checkpoint として残し、どこからでもやり直せるようにしてください（[長時間タスクの信頼性設計](agent-reliability.md#3-タスク分割と-checkpoint-境界)）。

## 人が確認すること

- コードを送ってよいモデルと送り先を、移行の前に決めたか
- 抽出した業務ルールを、業務の専門家が確認したか
- 変換の前に、既存の振る舞いを表すテストがあるか
- 変換後のコードを社内のチームが保守できるか
- 公開されている数値（削減時間・正確性）を、自分の対象にそのまま当てはめていないか

---

## 関連ドキュメント

- [仕様駆動開発（SDD）](spec-driven.md) — 仕様を実行可能な入力にする。既存システムから仕様を取り出す方向にも使える
- [マルチエージェントを使う境界線](multi-agent.md) — 解析・変換・依存関係の地図を役割ごとに分ける構成の判断
- [長時間タスクの信頼性設計](agent-reliability.md) — 段階ごとの checkpoint と再開
- [エージェントが働きやすいリポジトリ](agent-ready-repo.md) — テストがあることが、変えてよいかを判断する前提
- [AI 時代のコードレビュー](ai-code-review.md) — テストの書き換えで通していないかを見る
- [生成AIを業務で安全に使う](../business/safety.md) — コードを外部へ送る前の確認

## 参考リンク

- [How we use AI agents for COBOL migration and mainframe modernization](https://devblogs.microsoft.com/all-things-azure/how-we-use-ai-agents-for-cobol-migration-and-mainframe-modernization/) ／ [Azure-Samples/Legacy-Modernization-Agents](https://aka.ms/cobol) — Microsoft の取り組みとフレームワーク（2025-07-09）
- [How GitHub Copilot and AI agents are saving legacy systems](https://github.blog/ai-and-ml/github-copilot/how-github-copilot-and-ai-agents-are-saving-legacy-systems/) — GitHub の解説（2025-10-14）
- [Modernization of mainframe applications — AWS Transform](https://docs.aws.amazon.com/transform/latest/userguide/transform-app-mainframe.html) — 機能・対象のファイル・人の承認（AWS 公式、2026-10-24 確認）
- [Reimagining mainframe applications with AWS Transform and Claude Code](https://aws.amazon.com/blogs/migration-and-modernization/reimagining-mainframe-applications-with-aws-transform-and-claude-code/) — Refactor と Reimagine の 2 つの道（AWS 公式ブログ）
- [Modernizing legacy code with Claude Code](https://www.anthropic.com/webinars/modernizing-legacy-code-with-claude-code) — Anthropic のウェビナー（録画）
- [Ask HN: COBOL devs, how are AI coding affecting your work?](https://news.ycombinator.com/item?id=46678550) — コミュニティの議論（2026-01、`提供元`: Community）
