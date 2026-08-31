# コーディングエージェントの選び方

> **対象ツール**: ツール横断（Claude Code・Codex・Qwen Code・OpenCode・Bionic） ｜ **対象読者**: エンジニア ｜ **最終更新**: 2026-08-31

> ターミナルやデスクトップで動く「コーディングエージェント」は、2026 年時点で選択肢が増えました。よく「Claude Code は Claude 中心、Codex は OpenAI 中心」のようにモデル系列で語られますが、**その分類は実態を半分しか説明していません**。本ページでは、何が本当に違うのかを整理します。

---

## 30 秒で選ぶ

| 事情・制約 | 向いているもの |
|-----------|--------------|
| Claude を主に使っていて、Skill やサブエージェントまで作り込みたい | [Claude Code](../claude-code/README.md) |
| ChatGPT / OpenAI のアカウントと環境に揃えたい | [Codex](../codex/README.md) |
| **エージェント自体を OSS で使いたい**（改造・自前ホストを含む） | Qwen Code ／ OpenCode |
| **モデルを頻繁に乗り換えたい**、プロバイダーを自分で選びたい | OpenCode |
| **コードを社外へ出せない**（ローカル推論が必須） | Bionic ／ OpenCode + ローカルモデル |
| ターミナルではなく GUI で使いたい | Bionic |

---

## 「モデル中心」という分類の落とし穴

5 つを「どのモデル系列のものか」で並べると次のようになります。

| ツール | 系列 |
|-------|------|
| Claude Code | Claude（Anthropic） |
| Codex | OpenAI |
| Qwen Code | Qwen（Alibaba） |
| OpenCode | マルチモデル |
| Bionic | オープンモデル＋ローカル実行 |

ただし**この「◯◯中心」は、既定値と開発元の立ち位置を指すものであって、使えるモデルの制約とは限りません**。実際、

- **Qwen Code** は名前に反して Qwen 専用ではありません。README は「OpenAI, Anthropic, Gemini, and Qwen APIs. Any third-party provider or local model (Ollama / vLLM)」に対応するマルチプロトコル構成だと述べています
- **OpenCode** は AI SDK と Models.dev を通じて **75 以上のプロバイダー**に対応し、Ollama・LM Studio・llama.cpp によるローカル実行も設定だけで使えます

つまり実務で効いてくる差は、モデル系列そのものより次の 3 点です。

| 判断軸 | 何が変わるか |
|-------|------------|
| **エージェント本体が OSS か** | 改造・監査・自前ホストの可否。組織で中身を検証したい場合に効く |
| **推論がどこで走るか** | コードが外部へ出るかどうか。規約・機密の制約に直結する |
| **モデルの選択肢** | 既定のモデルに縛られるか、乗り換えられるか |

---

## 比較

| ツール | 提供元 | ライセンス | 実行環境 | モデルの選択肢 | 状態 |
|-------|-------|----------|---------|--------------|------|
| **[Claude Code](../claude-code/README.md)** | Anthropic（Official） | プロプライエタリ | CLI / デスクトップ / Web / IDE | Claude 系 | GA |
| **[Codex](../codex/README.md)** | OpenAI（Official） | プロプライエタリ | CLI / IDE / クラウド | OpenAI 系 | GA |
| **Qwen Code** | Qwen（Alibaba）（Official） | Apache-2.0 | CLI / IDE / デスクトップ / SDK | OpenAI・Anthropic・Gemini・Qwen・ローカル | GA |
| **OpenCode** | Anomaly（Community） | MIT | CLI（TUI）/ デスクトップ（Beta）/ IDE | 75+ プロバイダー・ローカル | GA |
| **Bionic** | LM Studio（Official） | プロプライエタリ | **デスクトップアプリ** | オープンモデル（ローカル / クラウド） | GA |

> ラベルの意味は [情報ラベルの読み方](../../README.md#情報ラベルの読み方) を参照してください。

> **Bionic だけ種類が違います。** 他の 4 つがターミナル中心のコーディングエージェントであるのに対し、Bionic は**デスクトップアプリ**です。同じ「AI エージェント」でも、CLI で開発フローに差し込むものと、GUI で使うものは前提が異なります。

---

## それぞれの位置づけ

### Claude Code — 作り込みの深さ

Anthropic 公式。CLAUDE.md・Agent Skills・サブエージェント・フック・プラグインと、**エージェントの振る舞いを組み立てる仕組みが最も揃っています**。チームの手順を仕組みとして固めたい場合の第一候補です。

**→ 詳細は [Claude Code ガイド](../claude-code/README.md) ／ [カスタマイズ機能](../claude-code/basics.md)**

### Codex — OpenAI 環境との一体感

OpenAI 公式。ChatGPT のアカウントと地続きで、Agent Skills のカタログ（`openai/skills`）が 3 層（System / Curated / Experimental）で整理されています。2026-08 からは業界標準の Agent Plugins 形式にも対応しました。

**→ 詳細は [Codex ガイド](../codex/README.md)**

### Qwen Code — OSS のエージェント本体

Alibaba の Qwen チームが Apache-2.0 で公開。Google の **Gemini CLI v0.8.2 を出発点**に、独自のマルチプロトコル構成へ分岐しました。ターミナル UI に加え、IDE プラグイン・デスクトップアプリ・デーモン・SDK と入口が複数あります。Agent Skills・MCP・LSP・Plan Mode・Hooks に対応します。

```bash
npm install -g @qwen-code/qwen-code@latest
```

> Node.js 22 以降が必要です。「エージェント本体もモデルも OSS で揃えたい」という要求に対して、現状もっとも直球な選択肢です。

### OpenCode — プロバイダーを選ぶ前提の設計

Anomaly が MIT で公開（リポジトリは [anomalyco/opencode](https://github.com/anomalyco/opencode)）。**特定のモデル提供元に紐づかない**ことが設計の中心にあります。

導入はパッケージマネージャー経由が確実です（npm・Homebrew・Scoop などに対応）。

```bash
npm install -g opencode-ai
```

公式サイトのインストールスクリプトを使う場合は、**取得して中身を確認してから実行**してください。

```bash
curl -fsSL https://opencode.ai/install -o opencode-install.sh
less opencode-install.sh          # 何をするスクリプトか確認する
bash opencode-install.sh
```

> `curl ... | bash` の一行で済ませると、**実行するまで中身を確認できません**。配布元が正当でも、経路の差し替えに気づけない形になります。本ガイドが [Skill / Plugin のセキュリティ](skill-security.md) で述べている「導入前に中身を読む」は、インストールスクリプトにも同じく当てはまります。

| 特徴 | 内容 |
|------|------|
| モデル | AI SDK / Models.dev 経由で 75+ プロバイダー。Ollama・LM Studio・llama.cpp でローカル実行も可 |
| エージェント | `Build`（フルアクセス）／ `Plan`（読み取り専用）を Tab で切り替え。汎用サブエージェントも持つ |
| 拡張 | AGENTS.md・Agent Skills・MCP・LSP |
| 迷ったとき | 検証済みモデルを集めた **OpenCode Zen** が用意されている |

> 読み取り専用の `Plan` エージェントが標準で用意されている点は、**調査と変更を明確に分ける**運用と相性が良い設計です。

### Bionic — ローカル実行を出発点にする

LM Studio が 2026-07-16 に公開した、**オープンモデル向けのデスクトップエージェント**です（LM Studio 本体とは別アプリ）。コード検索とインライン差分によるコード編集に加え、文書の読み取りや音声入力も扱います。

実行先を 3 段階から選べます。

| 実行先 | 位置づけ |
|-------|---------|
| ローカル | 自分のハードウェアで完結。外部送信なし |
| LM Link | 手元の環境へ接続して動かす |
| LM Studio Secure Cloud | 手元では重いモデル（GLM 5.2 / Kimi K2.7 Code 等）をクラウドで |

クラウド利用時も **Zero Data Retention（データを保持せず、学習にも使わない）**を明示しています。ローカルとクラウドの切り替えはプロジェクト単位でユーザーが指定する設計です。

> **確認したいこと**: クラウドのモデル利用には LM Studio アカウントと課金設定が必要です。また、この 2 つの点は公式発表では確認できませんでした — **MCP や Skill への対応可否**、および **macOS 以外のプラットフォーム対応**（配布物は darwin/arm64 が案内されています）。導入前に公式サイトで最新の対応状況を確認してください。

---

## 共通化している部分

ツールが増える一方で、**設定ファイルの形式は収束しつつあります**。乗り換えのコストは以前より下がっています。

| 仕組み | 状況 |
|-------|------|
| `SKILL.md`（Agent Skills） | Claude Code・Codex・Qwen Code・OpenCode が対応。同じ Skill を複数ツールで使い回せる |
| `AGENTS.md` | プロジェクトの前提を書く共通ファイルとして普及 |
| MCP | 外部サービス接続の共通規格。上記 4 ツールが対応 |
| [Agent Plugins 1.0.0](../trends.md#8-agent-plugins-100--マルチベンダー共通のエージェント設定標準) | Skill と MCP 設定をまとめる可搬形式。Codex・GitHub Copilot・Cursor が対応（Claude Code は独自形式のまま） |

**→ Skill の探し方・導入は [skills.sh ガイド](skills-sh.md)、導入前の安全確認は [Skill / Plugin のセキュリティ](skill-security.md) を参照**

> **注意**: 同じ `SKILL.md` が動くということは、**同じ危険も持ち込める**ということです。エージェントを乗り換えても、導入前に中身を読む必要は変わりません。

---

## 乗り換えるときに見る軸

2026 年後半に入り、**設定と作業そのものを別のエージェントへ持ち出せる**製品機能が出てきました。Codex は Claude Code・Cursor から Instructions・Skills / Plugins・プロジェクト・直近の chat を取り込めます（[Codex ガイド 7 節](../codex/README.md#7-他のエージェントから設定と作業を引き継ぐ)）。

これにより、選定で見るべき点が「モデルの性能」だけではなくなりました。

| 軸 | 確認すること |
|----|-------------|
| 定義の可搬性 | Instructions / Skills / Plugins を持ち出せるか |
| 作業の継続性 | プロジェクト・chat・セッションを再開できるか |
| 同期方式 | 一度だけコピーするのか、自動同期を続けられるのか |
| 再認証の要否 | 取り込んだ Plugin / コネクタで認証をやり直す必要があるか |
| 対応する面 | デスクトップ / CLI / IDE / クラウドのどこで使えるか |

**乗り換えコストが下がるほど、乗り換え先で何が自動実行されるかの確認が重要になります。** 取り込みは Hooks や MCP 設定まで運ぶため、有効化の前に中身を読む必要は変わりません（[Skill / Plugin のセキュリティ](skill-security.md)）。

---

## エージェントとハーネスの関係

ここで挙げたツールは「エージェントループを回す部分」です。その外側で、権限・セッション・ツール接続を管理する層を**ハーネス**と呼びます。組織で複数のエージェントを運用する場合は、この層の設計が効いてきます。

**エージェント本体とハーネスは層が違うため、同じ表では比べられません。** たとえば AWS の [Kiro Crew](harness.md#kiro-crew--常駐して動き続けるハーネス) は「6 つ目のコーディングエージェント」ではなく、`kiro-cli` を下敷きにして**対話の外で作業を続ける常駐レイヤー**です。比較で選ぶのは本ページの 5 つのようなループを回す本体、その上に載せるかどうかを決めるのがハーネス、という順で考えてください。

**→ [AI エージェントの実行基盤（ハーネス）](harness.md)**

---

## 関連ドキュメント

- [Claude Code ガイド](../claude-code/README.md) ／ [Codex ガイド](../codex/README.md) — 本ページで扱った 2 つの詳細
- [AI エージェントの実行基盤（ハーネス）](harness.md) — エージェントの外側の層
- [Skill / Plugin のセキュリティ](skill-security.md) — どのエージェントでも共通の導入前チェック
- [skills.sh ガイド](skills-sh.md) — Skill の検索・導入
- [Skills 最新動向](../trends.md) — エコシステム全体の動き

## 参考リンク

- [QwenLM/qwen-code](https://github.com/QwenLM/qwen-code) — Qwen Code のリポジトリ（公式）
- [anomalyco/opencode](https://github.com/anomalyco/opencode) — OpenCode のリポジトリ（公式）
- [OpenCode ドキュメント](https://opencode.ai/docs/) — 設定・プロバイダー一覧（公式）
- [Introducing LM Studio Bionic](https://lmstudio.ai/blog/introducing-lm-studio-bionic) — Bionic の発表記事（公式・2026-07-16）
- [Claude Code 公式ドキュメント](https://code.claude.com/docs/) ／ [Codex 公式ドキュメント](https://developers.openai.com/codex/cli)

---

> **注意**: 各ツールの対応モデル・機能は短期間で変わります。本ページは冒頭の「最終更新」日時点で各公式リポジトリ・公式ドキュメントを確認した内容です。導入時は必ず一次情報で最新の状態を確認してください。
