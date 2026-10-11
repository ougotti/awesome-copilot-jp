# Skill の公開・共有 — 配布方法を選び、Codex の Plugin として届ける

> **対象ツール**: ツール横断（具体的な Plugin 配布例は Codex） ｜ **実行環境**: CLI（PowerShell） / Chat UI（デスクトップアプリ） ｜ **対象読者**: 自作 Skill を共有したい開発者・チームの運用担当 ｜ **最終更新**: 2026-10-11

自作 Skill は、フォルダを渡すだけでも共有できます。継続して配るなら GitHub で変更を管理し、まとめてインストールしてほしい Skill を Plugin に束ねると扱いやすくなります。このページでは共有方法を選んだ後、**配布側のファイル作成 → 利用者の登録・インストール → 更新確認**までを説明します。

ここでいう「GitHub でのマーケットプレイス配布」は、**GitHub リポジトリに Codex 用のカタログを置く方法**です。GitHub Marketplace への出品や、OpenAI の公式公開ディレクトリへの掲載とは別の経路です。

## 1. 誰に、どの単位で渡すかを決める

| 方法 | 向いている状況 | 配るもの・導入単位 | 更新方法・条件 |
|---|---|---|---|
| フォルダ / ZIP | 少人数に一度試してもらう。 | `SKILL.md` と参照ファイルを含む Skill フォルダ。 | 受け手が置き換える。対象ホストの読み込み先へ配置する。 |
| プロジェクトの Git に含める | 同じリポジトリの作業手順を共有する。 | Codex なら `.agents/skills/<skill-name>/`。 | リポジトリの取得・更新と一緒に配る。非公開ならアクセス権が必要。 |
| GitHub の Skill 集 | 複数プロジェクトで個別の Skill を選んで使う。 | Skill フォルダ。Codex の `$skill-installer` にリポジトリ内の URL を指定して導入を依頼できる。 | インストーラーの更新方法を確認する。配布元の push だけで導入済みコピーが更新されるとは限らない。 |
| Git ベースの Plugin marketplace | 関連 Skill を一括導入してもらう。 | Plugin 定義、Skills、カタログ。インストール単位は Plugin。 | 利用者がカタログを登録・更新し、Plugin を導入・再読み込みする。 |
| ワークスペースへの公開 | 組織内の役割に応じて配る。 | ワークスペースの Plugin。 | 管理者権限と組織の許可が必要。詳細は後述。 |
| 公式公開ディレクトリ | 対象ユーザーが検索して見つけられる形で配る。 | 掲載情報を含む Plugin パッケージ。 | 開発者確認、検証・審査、承認後の公開が必要。 |

Codex のローカル Skill は、現行の[公式説明](https://developers.openai.com/codex/skills/)ではプロジェクトの `.agents/skills/` とユーザーの `~/.agents/skills/` などから読み込まれます。既存のインストーラーが使う保存先とは区別してください。他ホストの配置先やコマンドへ一般化せず、[各ツールの入口](../../README.md#ドキュメント一覧)を確認します。

## 2. リポジトリ・Plugin・Skill の関係

**1 リポジトリ＝1 Skill という制約はありません。** 1 リポジトリに複数 Plugin を置けて、1 Plugin に複数 Skill を同梱できます。

```text
my-codex-plugins/                  # GitHub で共有するリポジトリ
├── .agents/plugins/
│   └── marketplace.json           # Plugin のカタログ
├── plugins/
│   ├── writing-tools/             # Plugin A（インストール単位）
│   │   ├── plugin.json
│   │   └── skills/
│   │       ├── daily-report/SKILL.md
│   │       └── proofreading/SKILL.md
│   └── research-tools/            # Plugin B
│       ├── plugin.json
│       └── skills/
│           └── source-check/SKILL.md
└── README.md
```

| 単位 | 役割 | 分ける目安 |
|---|---|---|
| Repository | ソースと変更履歴を管理する。 | 管理者・公開範囲・保守責任が異なる。 |
| Marketplace | 利用者が選べる Plugin の一覧を示す。 | 配布先やカタログの管理方針が異なる。 |
| Plugin | 関連する機能をまとめてインストールする。 | 利用者が個別に導入・有効化したい。 |
| Skill | 特定の仕事の指示と補助ファイルをまとめる。 | 起動する条件や作業の目的が異なる。 |

たとえば日報作成と文章校正を一緒に使うなら `writing-tools` にまとめます。別の外部認証が必要な調査機能は独立した Plugin にすると、利用者が必要なものを選べます。カタログには同じリポジトリ内の Plugin のほか、別の Git リポジトリにある Plugin も登録できます。

形式の可搬性は[プラグインの可搬性](plugin-portability.md)を参照してください。可搬なパッケージでも、Marketplace の登録コマンドや実行環境まで共通になるわけではありません。

## 3. Codex 向けの最小パッケージを作る

以下は **Skill のみを含む Portable Agent Plugins 形式**です。外部 MCP サーバーや認証設定は不要です。OpenAI の[手動作成・配布ガイド](https://developers.openai.com/plugins/build/plugins)に沿って、まず `writing-tools` と `daily-report` だけを作ります。前節の残りの Plugin / Skill は追加時の構成例です。

前提は Git、Codex CLI、対応するデスクトップアプリ、配布先 GitHub リポジトリへの書き込み権限です。利用者には Git の取得権限と Codex を使える環境が必要です。IDE 拡張は Plugin 非対応で、ローカル / Git カタログを Web・モバイルでもそのまま使えるとは限りません。対応面は[公式 Plugins ガイド](https://learn.chatgpt.com/docs/plugins)で確認します。

### フォルダを用意する

**PowerShell**で、配布用の親フォルダから実行します。既存リポジトリを使う場合は、そのルートへ移動して `New-Item` の行から始めます。

```powershell
git init -b main my-codex-plugins
Set-Location my-codex-plugins
New-Item -ItemType Directory -Force .agents/plugins, plugins/writing-tools/skills/daily-report
```

以下の 3 ファイルを UTF-8 で保存します。JSON 中の `$schema` や、後述の `$daily-report` は文字列そのものです。PowerShell の変数として展開しないでください。

### Plugin の定義

`plugins/writing-tools/plugin.json`:

```json
{
  "$schema": "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json",
  "name": "writing-tools",
  "version": "1.0.0",
  "description": "日々の文章作成を支援する。",
  "author": {
    "name": "Example Author"
  }
}
```

`author.name` を自分の公開名に置き換えます。この形式は Plugin ルートの `skills/` を探索するため、`skills` フィールドを追加しません。Codex 互換形式の `.codex-plugin/plugin.json` とフィールドを混ぜないでください。アイコン等の OpenAI 固有設定を加える場合は、公式ガイドの `extensions.com.openai` を参照します。

### Skill 本体

`plugins/writing-tools/skills/daily-report/SKILL.md`:

```markdown
---
name: daily-report
description: 作業日報の作成を依頼されたときに使う。
---

入力から「作業」「結果」「次の予定」の順で日本語の日報を作る。
不明な項目は「未記入」とし、実施していない作業や理由を補わない。
```

既存 Skill を移す場合は `SKILL.md` だけでなく、参照している `scripts/`・`references/`・`assets/` も同梱します。複数 Skill に増やすときは `skills/` 直下にフォルダを追加します。

### カタログ

`.agents/plugins/marketplace.json`:

```json
{
  "name": "example-skills",
  "interface": {
    "displayName": "Example Skills"
  },
  "plugins": [
    {
      "name": "writing-tools",
      "source": {
        "source": "local",
        "path": "./plugins/writing-tools"
      },
      "policy": {
        "installation": "AVAILABLE",
        "authentication": "ON_INSTALL"
      },
      "category": "Productivity"
    }
  ]
}
```

`source.path` は **Marketplace のルート（この例ではリポジトリルート）基準**です。`.agents/plugins/` 基準ではありません。`source: "local"` は取得したカタログ内の Plugin フォルダを指すため、この構成のまま GitHub に置けます。複数 Plugin を載せる場合は `plugins` 配列へ別のエントリを追加します。

`authentication` は認証を行うタイミングの指定です。認証機能を追加したり、利用者の GitHub 権限を与えたりする設定ではありません。この Skill のみの例では外部サービスへのログインは発生しません。

## 4. ローカルで導入して確かめる

カタログの登録と Plugin のインストールを順に行います。**PowerShell**で、作ったリポジトリルートから実行します。

```powershell
codex --version
codex plugin marketplace add .
codex plugin marketplace list
```

一覧に `example-skills` と意図したフォルダが出ることを確認します。公式のローカル Plugin ガイドでは、デスクトップアプリを再起動し、**Plugins → 自分の Marketplace → writing-tools → インストール**の順で試す手順が案内されています。

CLI からの導入に対応する版では、同じ登録先から次のようにインストールできます。以下は Codex CLI 0.153.4 で確認した構文です。異なる版では `codex plugin --help` と各サブコマンドの `--help` を確認してください。

```powershell
codex plugin add writing-tools@example-skills --json
codex plugin list --marketplace example-skills --json
```

結果の `pluginId`・`version`・`installed`・`enabled` を確認します。Plugin がインストールされていても、Skill が正しく選ばれ、指示どおりに働くかは別に確認します。

**新しい Codex チャット**で、Skill 選択欄から `daily-report` を選び、次の依頼を送ります。CLI のチャットでは `$` から Skill を選択できます。同名がある場合は `writing-tools` に属するものを選んでください。

```text
daily-report スキルを使って日報を作ってください。
今日の作業は「公開記事の構成を作成」、結果は「構成案を保存」です。
```

| 確認 | 期待する結果 |
|---|---|
| 起動元 | インストールした Plugin の `daily-report` が選ばれる。 |
| 手順 | 「作業」「結果」「次の予定」の順に出力される。 |
| 不明情報 | 入力していない次の予定は「未記入」になる。 |

## 5. GitHub に置き、利用者へ案内する

先に、下表の項目を含む `README.md` を配布リポジトリのルートへ保存します。次に GitHub で公開または非公開の空のリポジトリを用意します。**PowerShell**で配布リポジトリのルートから、ファイルと公開範囲を確認して push します。`OWNER/REPO` は実際の所有者・リポジトリ名へ置き換えます。すでに `origin` がある場合は追加せず、宛先を確認します。

```powershell
git status --short
git add .agents/plugins/marketplace.json plugins/writing-tools README.md
git commit -m "Add writing-tools plugin"
git remote add origin https://github.com/OWNER/REPO.git
git push -u origin main
```

README の本文には実際の `OWNER/REPO` を記載し、必要ならライセンスファイルも同梱します。

| README に書く項目 | この例の記載内容 |
|---|---|
| 目的・収録 Skill | `writing-tools` に `daily-report` を含む。入力から日報を作る。 |
| 前提 | Git、対応版 Codex CLI / デスクトップアプリ、必要なら GitHub の取得権限。 |
| 登録・導入 | 下記の登録コマンド、Marketplace 名、Plugin 名、インストール操作。 |
| 使用例 | 前節の日報依頼と期待する出力。 |
| 更新 | 次節のカタログ更新・Plugin 再導入・新規チャットでの確認。 |
| 依存・利用条件 | この例は追加 MCP・スクリプトなし。作者が選んだライセンスと問い合わせ先。 |

**利用者の PowerShell**で登録します。GitHub への push だけで、相手の Codex へ自動導入されるわけではありません。

```powershell
codex plugin marketplace add OWNER/REPO --ref main
codex plugin marketplace list
```

登録後は前節と同様に Plugins 画面、または対応 CLI の `codex plugin add writing-tools@example-skills` でインストールし、新しいチャットで試します。非公開リポジトリでは、取得する環境の Git 認証・アクセス権を先に用意します。GitHub の取得権限と、Plugin が使う外部サービスの認証は別です。

すでに同名のローカル `example-skills` を登録している作者が Git 版を試す場合は、`marketplace list` で登録先を確認し、ローカル登録を `codex plugin marketplace remove example-skills` で外してから Git 版を登録します。この操作はカタログ登録の削除で、ソースリポジトリの削除ではありません。

### バージョンを固定して配る

動く内容を揃えたい場合は、公開済み tag や commit SHA を `--ref` に指定します。`main` は更新される参照なので、固定バージョンではありません。

```powershell
codex plugin marketplace add OWNER/REPO --ref v1.0.0
```

この tag は配布側で作成・push しておく必要があります。固定した参照を更新するときは、新しい参照を明示して登録先を切り替えます。カタログが別リポジトリの Plugin を参照する場合は、そのエントリ側の `ref` / `sha` も固定します。カタログだけの固定で全配布物が固定されるとは限りません。[公式の Git ソース指定](https://developers.openai.com/plugins/build/plugins#marketplace-metadata)を参照してください。

## 6. 更新して利用者側の反映を確認する

配布側は Skill と `plugin.json` の `version` を更新し、変更内容を README 等に記録して commit・push します。この例なら `1.0.0` から `1.0.1` へ上げ、Skill に「末尾に『確認待ち』と書く」を追加すると、更新前後を見分けられます。

**Git 経由で登録した利用者の PowerShell**:

```powershell
codex plugin marketplace upgrade example-skills
codex plugin add writing-tools@example-skills --json
codex plugin list --marketplace example-skills --json
```

最初のコマンドは Git カタログのスナップショットを更新します。カタログ更新だけでインストール済み Plugin の反映まで済んだと判断せず、対応 CLI で再導入するか、利用中の Plugin 画面で更新を確認してください。固定 tag / SHA を指定している場合、カタログ更新だけで別の版には移りません。

**ローカルパスで登録した開発中のカタログ**には `marketplace upgrade` を使いません。元ファイルを修正してデスクトップアプリを再起動する公式手順、または対応 CLI での `plugin add` による再導入を使います。0.153.4 では、ローカル登録への `marketplace upgrade` は Git 登録ではない旨のエラーになりました。

最後に表示バージョン・有効状態を確認し、新しいチャットで同じ入力を試します。「確認待ち」が出るか、不明な予定を作っていないかまで確かめます。導入先のコピーと元ファイルが異なる場合があるため、元の `SKILL.md` の変更だけをもって完了としません。

## 7. 配布先ごとの公開条件

2026-10-11 時点の公式情報に基づく比較です。プラン・アカウント・組織ポリシーによる条件は、公開時にリンク先で再確認してください。

| 配布先 | 主な条件 | Skill のみ / MCP 同梱の違い |
|---|---|---|
| Git / ローカルの Marketplace | パッケージとカタログ、取得権限、対応クライアント。公式公開ディレクトリの掲載申請とは別経路。 | Skill のみなら外部サーバー不要。MCP を含む場合は接続先・依存関係・認証も準備する。 |
| ChatGPT ワークスペース | 公開操作はワークスペース管理者が行い、利用できる役割を指定する。組織設定で公開が無効化されている場合がある。公開先の組織外からは利用できない。 | 外部サービスの権限・認証はワークスペースへの公開とは別に適用される。 |
| 公式公開ディレクトリ | 個人または企業の開発者確認、Platform の組織オーナーまたは Apps Management Write 権限。ZIP・説明・アイコン等を用意し、必要な検証と審査を経て、承認後に公開する。 | Skill のみでもパッケージ・Skill の検証が必要。MCP 用のテストケース・動画は不要。MCP 同梱ではドメイン・接続・認証確認、正常系5件／非実行系3件のテスト、デモ動画、必要なら審査用アカウント等が追加される。 |

ローカルで動く最小パッケージが、そのまま公式掲載に必要な情報を満たすとは限りません。MCP の公開審査では製品・サポート・プライバシーポリシー・利用規約の HTTPS URL 等が必要です。Skill のみへの MCP 追加や Hooks 等の同梱にも公開フロー固有の制限があるため、申請前に[公式申請ガイド](https://developers.openai.com/plugins/deploy/submission)を確認します。ワークスペース内公開の操作は[公式パッケージガイド](https://developers.openai.com/plugins/build/plugins#share-a-local-plugin-with-your-workspace)を参照してください。

## 8. 配布前の確認と検証範囲

| 確認するもの | 合格の目安 |
|---|---|
| 同梱ファイル | 参照資料・スクリプト・画像が揃い、作者の PC 固有パスを前提にしない。 |
| 公開内容 | 秘密情報・個人情報を含めず、依存関係とライセンスを明記する。 |
| 初回導入 | 別の導入先でカタログ登録、Plugin インストール、有効状態を確認する。 |
| Skill の実行 | 選ばれた Skill、入力、期待結果、実際の結果を記録する。 |
| 更新 | 導入されたバージョンと変更後の挙動を確認する。 |

詳細な出自・権限の確認は [Skill / Plugin のセキュリティ](skill-security.md)、選択と手順遵守の評価は [Skill / エージェントの評価](evals.md)を参照してください。

**このページの検証記録（2026-10-11）**:

| 環境・対象 | 確認結果 |
|---|---|
| Windows / PowerShell / Codex CLI 0.153.4 | 一時的な専用設定領域で、ローカルカタログの登録・一覧表示、Portable Plugin の導入を確認。`installed: true` / `enabled: true` / `version: 1.0.0` を確認した。 |
| 更新 | 元ファイルとバージョンを変更し、`plugin add` の再実行で `1.0.1` と更新済み `SKILL.md` が導入先へ反映されることを確認した。 |
| ローカルと Git の違い | ローカルカタログへの `marketplace upgrade` が拒否されることを確認。Git 経由の登録・更新は公式資料と CLI ヘルプの確認で、GitHub からの取得実行は未検証。 |
| アプリ操作・モデルによる実行 | デスクトップ画面での導入と、チャットからの日報生成は未検証。上記はインストール・ファイル更新の確認であり、Skill 選択・出力品質の保証ではない。 |
| 公開申請 | ワークスペースへの公開、公式ディレクトリの申請は公式資料を確認。実申請はしていない。 |

## 公式資料と関連ページ

状態の「—」はガイド・仕様資料であり、各機能の一律の GA 宣言を意味しません。

| 資料 | 提供元 | 状態 | 用途 |
|---|---|---|---|
| [Build skills](https://developers.openai.com/codex/skills/) | Official（OpenAI） | — | Skill の構成、ローカル配置、呼び出し。 |
| [Package your plugin](https://developers.openai.com/plugins/build/plugins) | Official（OpenAI） | — | Plugin とカタログの形式、Git 登録、組織内配布。 |
| [Plugins](https://learn.chatgpt.com/docs/plugins) | Official（OpenAI） | — | 対応する利用面とインストール操作。 |
| [Upload and submit your plugin](https://developers.openai.com/plugins/deploy/submission) | Official（OpenAI） | — | 公式公開ディレクトリの申請要件。 |

- [Codex ガイド](../codex/README.md) — 導入・利用の入口。
- [プラグインの可搬性](plugin-portability.md) — 標準形式とクライアント固有機能。
- [GitHub Copilot Plugins](../copilot/plugins.md) — Copilot 固有の構成・コマンド。
