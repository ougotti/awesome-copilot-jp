# anthropics/skills - Claude 公式スキルリポジトリ

> **対象ツール**: Claude.ai・Claude Code ｜ **対象読者**: エンジニア・非エンジニア ｜ **最終更新**: 2026-07-29

> [anthropics/skills](https://github.com/anthropics/skills) は Anthropic が公開している Claude 用の公式スキルリポジトリです。ドキュメント処理、クリエイティブデザイン、開発支援、エンタープライズ向けなど 17 種類のスキルが収録されています。

## スキルとは

スキルは `SKILL.md`（指示書）とスクリプトをフォルダにまとめた**自己完結型のツールキット**です。Claude がセッション開始時や必要なタイミングで動的に読み込み、特定のタスクに最適化された動作を実現します。

```
my-skill/
├── SKILL.md        # スキルの指示書（必須）
├── scripts/        # ヘルパースクリプト（任意）
└── examples/       # 使用例（任意）
```

### GitHub Copilot の Skills との違い

| | **anthropics/skills** | **GitHub Copilot Skills** |
|--|----------------------|--------------------------|
| 対象ツール | Claude Code / Claude.ai | GitHub Copilot |
| 形式 | `SKILL.md` + スクリプト | `SKILL.md` + 関連ファイル |
| 用途 | ファイル操作・API連携・生成 | Copilot チャットのテンプレート |
| インストール | `/plugin install` | `.github/skills/` に配置 |

---

## インストール方法

### Claude Code（CLI）

```bash
# マーケットプレイスを登録
/plugin marketplace add anthropics/skills

# ドキュメント処理スキルをインストール
/plugin install document-skills@anthropic-agent-skills

# サンプルスキルをインストール
/plugin install example-skills@anthropic-agent-skills
```

または UI から：`Browse and install plugins` → `anthropic-agent-skills` → スキルセットを選択 → `Install now`

### Claude.ai

有料プランユーザーは、ドキュメント処理スキル（docx / pdf / pptx / xlsx）が最初から利用可能です。カスタムスキルのアップロードも可能です。

### Claude API

[Skills API Quickstart](https://docs.claude.com/en/api/skills-guide#creating-a-skill) を参照してください。

---

## スキル一覧

### ドキュメント処理（Document Skills）

本番環境で利用されている主要スキルです。Claude.ai の有料プランに標準搭載されています。

#### docx — Word ドキュメント

| 項目 | 内容 |
|-----|------|
| **機能** | Word 文書の作成・編集・変換 |
| **使用場面** | 報告書、契約書、技術仕様書の自動生成・編集 |
| **主要技術** | docx-js（JavaScript）、Pandoc（テキスト抽出）、XML 直接編集 |

**できること：**
- docx-js ライブラリを使って新規 Word 文書を作成
- 既存ファイルを XML として展開・編集・再パック
- PDF や画像への変換
- トラックされた変更（Track Changes）の追加・管理
- 表、画像、ヘッダー・フッターの操作

**使用例：**
```
「docx スキルを使って、プロジェクト進捗報告書を Word 形式で作成してください」
「このレポートに変更履歴付きで修正を加えてください」
```

---

#### pdf — PDF 処理

| 項目 | 内容 |
|-----|------|
| **機能** | PDF の結合・分割・テキスト抽出・フォーム処理・新規作成 |
| **使用場面** | PDF からのデータ収集、文書処理自動化 |
| **主要技術** | pypdf、pdfplumber、reportlab（Python） |

**できること：**
- 複数 PDF の結合・ページの分割
- レイアウトを維持したテキスト・表の抽出
- ReportLab で新規 PDF を生成
- OCR によるスキャン文書のテキスト化
- 透かし追加・パスワード保護
- フォームフィールドの抽出・入力

**使用例：**
```
「pdf スキルを使って、path/to/some-file.pdf からフォームフィールドを抽出してください」
「この 3 つの PDF を結合して 1 ファイルにしてください」
```

---

#### pptx — PowerPoint プレゼンテーション

| 項目 | 内容 |
|-----|------|
| **機能** | PowerPoint プレゼンテーションの作成・編集・変換 |
| **使用場面** | 提案資料、報告書、デッキの自動生成 |
| **主要技術** | PptxgenJS、markitdown（テキスト抽出）、LibreOffice |

**できること：**
- 既存テンプレートへのコンテンツ流し込み
- PptxgenJS を使ったスクラッチからの作成
- スライドサムネイル生成による QA
- 10 種類のプロデザインカラーパレット適用
- サブエージェントによるビジュアル QA（誤字・プレースホルダー検出）

**デザイン原則：**
- 各スライドに必ず画像・図・アイコンを配置（テキストのみ禁止）
- タイトル 36-44pt、本文 14-16pt の一貫したタイポグラフィ
- 13 のよくある落とし穴（青単色、センタリング乱用など）を自動回避

**使用例：**
```
「pptx スキルを使って、Q3 売上報告書のプレゼンを作成してください」
「この資料を Midnight Executive テーマで再デザインしてください」
```

---

#### xlsx — Excel スプレッドシート

| 項目 | 内容 |
|-----|------|
| **機能** | Excel ファイルの作成・編集・数式計算・データ分析 |
| **使用場面** | 財務モデル、データ集計、レポート自動生成 |
| **主要技術** | pandas（データ処理）、openpyxl（書式・数式） |

**できること：**
- 数式を埋め込んだ動的スプレッドシートの作成
- 財務モデルのカラーコーディング規則を自動適用
- `recalc.py` スクリプトで数式エラーを検出・報告
- CSV / TSV / .xlsm の変換・処理

**財務モデル規則：**

| 色 | 意味 |
|---|-----|
| 青（入力値） | ユーザーが変更する入力セル |
| 黒（数式） | 計算式で導かれる値 |
| 緑（内部リンク） | 同ファイル内の参照 |
| 赤（外部リンク） | 別ファイルからの参照 |

**使用例：**
```
「xlsx スキルを使って、5 年間の収益予測モデルを作成してください」
「この CSV データを分析して、月別売上のグラフ付き Excel レポートを作ってください」
```

---

### クリエイティブ・デザイン（Creative & Design）

#### algorithmic-art — アルゴリズム生成アート

| 項目 | 内容 |
|-----|------|
| **機能** | p5.js を使ったインタラクティブな生成アートの作成 |
| **使用場面** | ビジュアルアート、プロシージャル生成、クリエイティブコーディング |
| **主要技術** | p5.js（CDN 経由）、HTML アーティファクト |

**できること：**
- 独自の「アルゴリズム哲学」（コンピュテーショナル美学マニフェスト）を定義
- シード値ベースの再現可能な生成アートを実装
- リアルタイムパラメータ調整スライダー付き UI
- シード移動・ランダム・ダウンロードボタン付きサイドバー

**ワークフロー：**
1. アルゴリズム哲学を策定（例: "Organic Turbulence"）
2. 哲学を体現する p5.js コードを実装
3. 各シード値で異なる表現を生成

**使用例：**
```
「algorithmic-art スキルを使って、水の流れをテーマにした生成アートを作ってください」
```

---

#### canvas-design — キャンバスデザイン

| 項目 | 内容 |
|-----|------|
| **機能** | PNG・PDF 形式のビジュアルアートを生成 |
| **使用場面** | アートポスター、ビジュアルアイデンティティ、展示用デザイン |
| **出力形式** | .png / .pdf |

**できること：**
- 独自の美学的ムーブメント（1-2語のネーミング）を定義
- スパース・タイポグラフィを視覚デザインとして統合
- 美術館品質のビジュアルアート作品を生成

**デザイン哲学：** 「ドキュメントのデコレーションではなくアートオブジェクトを作る」

**使用例：**
```
「canvas-design スキルで、未来都市をテーマにしたポスターを作ってください」
```

---

#### frontend-design — フロントエンドデザイン

| 項目 | 内容 |
|-----|------|
| **機能** | 本番品質のフロントエンド UI の設計・実装 |
| **使用場面** | ランディングページ、ダッシュボード、Web アプリ UI |
| **主要技術** | HTML/CSS/JavaScript |

**できること：**
- 「AI らしいありきたりなデザイン」を避けた意図的なデザイン
- CSS 変数で管理された統一カラーシステム
- アニメーション・非対称レイアウト・負の空間の活用
- 特徴的なフォント選択（Arial などの汎用フォントを避ける）

**使用例：**
```
「frontend-design スキルで、SaaS ダッシュボードのトップページを作ってください」
```

---

#### theme-factory — テーマファクトリー

| 項目 | 内容 |
|-----|------|
| **機能** | プレゼンテーション・Web ページへのプロフェッショナルテーマ適用 |
| **使用場面** | スライド、ドキュメント、レポート、ランディングページ |

**組み込みテーマ 10 種：**

| テーマ名 | 雰囲気 |
|---------|-------|
| Ocean Depths | 深海ブルー |
| Sunset Boulevard | 夕暮れオレンジ |
| Forest Canopy | 森林グリーン |
| Modern Minimalist | モノクロミニマル |
| Golden Hour | ゴールデン |
| Arctic Frost | 北極ホワイト |
| Desert Rose | 砂漠ローズ |
| Tech Innovation | テックブルー |
| Botanical Garden | ボタニカル |
| Midnight Galaxy | 深夜ギャラクシー |

**使用例：**
```
「theme-factory スキルで Ocean Depths テーマをこのプレゼンに適用してください」
「カスタムテーマを作成して、会社のカラーを使ったスライドにしてください」
```

---

### 開発・技術（Development & Technical）

#### claude-api — Claude API 開発

| 項目 | 内容 |
|-----|------|
| **機能** | Claude API / Anthropic SDK を使ったアプリケーション開発 |
| **使用場面** | Claude を組み込んだアプリ開発、SDK の活用 |
| **対応言語** | Python、TypeScript、Java、Go、Ruby、C#、PHP |

**できること：**
- 単一 API コール（分類・要約）
- ツールユース（関数呼び出し付きワークフロー）
- Managed Agents（Anthropic ホストのステートフルエージェント）
- Adaptive Thinking（Opus 4.7 / Sonnet 4.6 対応）

**デフォルトモデル：** `claude-opus-4-7`

| モデル | ID |
|-------|---|
| Claude Opus 4.7 | `claude-opus-4-7` |
| Claude Opus 4.6 | `claude-opus-4-6` |
| Claude Sonnet 4.6 | `claude-sonnet-4-6` |
| Claude Haiku 4.5 | `claude-haiku-4-5-20251001` |

**使用例：**
```
「claude-api スキルを使って、テキスト分類器を Python で実装してください」
「ストリーミング対応の TypeScript SDK の使い方を教えてください」
```

---

#### mcp-builder — MCP サーバービルダー

| 項目 | 内容 |
|-----|------|
| **機能** | Model Context Protocol（MCP）サーバーの設計・実装・テスト |
| **使用場面** | 外部 API と Claude を統合するツールの開発 |
| **推奨言語** | TypeScript（SDK サポートが充実）、Python（FastMCP） |

**4 フェーズ開発プロセス：**

| フェーズ | 内容 |
|---------|------|
| Research & Planning | MCP 仕様の理解、API カバレッジの計画 |
| Implementation | プロジェクト構成、ツール定義、エラーハンドリング |
| Testing | MCP Inspector でツール動作を検証 |
| Evaluation | 10 問の現実的なタスクで LLM の使いやすさを評価 |

**使用例：**
```
「mcp-builder スキルを使って、Jira API の MCP サーバーを TypeScript で作ってください」
```

---

#### webapp-testing — Web アプリテスト

| 項目 | 内容 |
|-----|------|
| **機能** | Playwright を使ったローカル Web アプリの自動テスト |
| **使用場面** | フロントエンドの動作検証、UI バグの発見 |
| **主要技術** | Python + Playwright |

**できること：**
- ブラウザ操作の自動化（クリック・フォーム入力・ナビゲーション）
- スクリーンショット取得によるビジュアル確認
- コンソールログの収集・分析
- `with_server.py` でサーバーライフサイクルを管理

**重要ポイント：** 動的 Web アプリは `page.wait_for_load_state('networkidle')` で JavaScript 完了を待ってから操作する

**使用例：**
```
「webapp-testing スキルを使って、localhost:3000 のログインフォームをテストしてください」
```

---

#### web-artifacts-builder — Web アーティファクトビルダー

| 項目 | 内容 |
|-----|------|
| **機能** | React + TypeScript + shadcn/ui で Claude.ai アーティファクトを生成 |
| **使用場面** | インタラクティブなデモ・ツール・ダッシュボードの作成 |
| **技術スタック** | React 18、TypeScript、Vite、Tailwind CSS、shadcn/ui、Parcel |

**ワークフロー：**
1. フロントエンドリポジトリを初期化（40+ の shadcn/ui コンポーネント込み）
2. コンポーネントを実装
3. 単一 HTML ファイルにバンドル（JS・CSS・依存関係をすべてインライン化）
4. Claude.ai のアーティファクトとして表示

**使用例：**
```
「web-artifacts-builder スキルで、リアルタイムのデータビジュアライザーを作ってください」
```

---

### エンタープライズ・コミュニケーション（Enterprise & Communication）

#### brand-guidelines — ブランドガイドライン適用

| 項目 | 内容 |
|-----|------|
| **機能** | Anthropic のブランドガイドラインをアーティファクトに適用 |
| **使用場面** | 会社ブランドに合った資料作成 |
| **対象** | プレゼンテーション、ドキュメント |

**Anthropic ブランド仕様：**

| 要素 | 仕様 |
|-----|------|
| ダーク | `#141413` |
| ライト | `#faf9f5` |
| オレンジ | `#d97757` |
| ブルー | `#6a9bcc` |
| グリーン | `#788c5d` |
| 見出しフォント | Poppins（Arial フォールバック） |
| 本文フォント | Lora（Georgia フォールバック） |

**使用例：**
```
「brand-guidelines スキルで、このプレゼンに Anthropic のブランドスタイルを適用してください」
```

---

#### doc-coauthoring — ドキュメント共同作成

| 項目 | 内容 |
|-----|------|
| **機能** | 対話型の 3 ステージワークフローで高品質ドキュメントを共同作成 |
| **使用場面** | 提案書、仕様書、設計ドキュメントの作成 |

**3 ステージワークフロー：**

| ステージ | 内容 |
|---------|------|
| Context Gathering | 文書の目的・読者・制約を整理し、情報を包括的に収集 |
| Refinement & Structure | セクション単位で質問・ブレスト・精錬を繰り返す |
| Reader Testing | 文脈なしで読み込んだ別の Claude インスタンスが盲点を検出 |

**使用例：**
```
「doc-coauthoring スキルを使って、新機能のテクニカル仕様書を一緒に書いてください」
```

---

#### internal-comms — 社内コミュニケーション

| 項目 | 内容 |
|-----|------|
| **機能** | 6 種類の社内コミュニケーション文書を作成 |
| **使用場面** | 定例報告、ニュースレター、インシデントレポートなど |

**対応文書タイプ：**

| タイプ | 内容 |
|-------|------|
| 3P Updates | Progress / Plans / Problems の進捗報告 |
| Company Newsletter | 全社向けニュースレター |
| FAQ Responses | よくある質問への回答 |
| Status Reports | ステータスレポート |
| Leadership Updates | リーダーシップからのアップデート |
| Incident Reports | インシデントレポート |

**使用例：**
```
「internal-comms スキルを使って、今週の 3P アップデートを作成してください」
```

---

#### slack-gif-creator — Slack GIF 作成

| 項目 | 内容 |
|-----|------|
| **機能** | Slack 向けに最適化されたアニメーション GIF を生成 |
| **使用場面** | カスタム絵文字、リアクション GIF の作成 |
| **主要技術** | Pillow、imageio、NumPy（Python） |

**仕様：**

| 用途 | サイズ | フレームレート |
|-----|-------|--------------|
| 絵文字 GIF | 128×128 px | 10-30 FPS |
| メッセージ GIF | 480×480 px | 10-30 FPS |
| カラーパレット | 48-128 色 | — |

**アニメーション効果：** シェイク、パルス、バウンス、ローテーション、フェード、スライド、ズーム、パーティクル爆発など

**使用例：**
```
「slack-gif-creator スキルで、ガッツポーズの絵文字 GIF を作ってください」
```

---

#### skill-creator — スキル作成支援

| 項目 | 内容 |
|-----|------|
| **機能** | 新しいスキルの設計・テスト・最適化を体系的に支援 |
| **使用場面** | カスタムスキルの開発 |

**ワークフロー：**

```
意図の把握 → スキル下書き → テストケース作成 → 評価 → 反復改善 → 最適化
```

**特徴：**
- ベースラインと比較した定量的評価
- 20 クエリによるトリガー評価（いつスキルが発動すべきか最適化）
- スキルの説明フィールドを自動チューニング

**使用例：**
```
「skill-creator スキルを使って、コードレビュー専用のスキルを作ってください」
```

---

## カスタムスキルの作成方法

### 基本構成

```
my-skill/
└── SKILL.md
```

### SKILL.md テンプレート

```markdown
---
name: my-skill-name
description: このスキルが何をするか、いつ使用するかの説明（Claude がいつ呼び出すかを決定します）
---

# スキル名

[Claude が実行する指示をここに記述]

## 使用例
- 使用例 1
- 使用例 2

## ガイドライン
- ガイドライン 1
- ガイドライン 2
```

### フロントマターの必須フィールド

| フィールド | 説明 |
|----------|------|
| `name` | スキル識別子（小文字、スペースはハイフンに置換） |
| `description` | スキルの機能と使用タイミングの説明（Claude がこれをもとにスキルを選択） |

### スクリプトの追加

複雑な処理が必要な場合は `scripts/` ディレクトリにヘルパースクリプトを追加できます。

```
my-skill/
├── SKILL.md
├── scripts/
│   ├── process.py    # データ処理スクリプト
│   └── helper.sh     # シェルユーティリティ
└── examples/
    └── sample.md
```

### 良い `description` の書き方

`description` は Claude がスキルを自動選択する際の判断基準になります。

```yaml
# 良い例：いつ使うかが明確
description: |
  Word 文書（.docx）の作成・編集・変換が必要なときに使用する。
  新規文書の作成、既存文書の修正、PDF 変換などに対応。

# 悪い例：曖昧すぎる
description: ドキュメント処理スキル
```

---

## スキルのカテゴリまとめ

| カテゴリ | スキル | 主な用途 |
|---------|-------|---------|
| **ドキュメント処理** | docx, pdf, pptx, xlsx | ビジネス文書の自動生成・処理 |
| **クリエイティブ** | algorithmic-art, canvas-design, frontend-design, theme-factory | アート・デザイン・UI 生成 |
| **開発・技術** | claude-api, mcp-builder, webapp-testing, web-artifacts-builder | 開発支援・テスト自動化 |
| **エンタープライズ** | brand-guidelines, doc-coauthoring, internal-comms, slack-gif-creator, skill-creator | 組織コミュニケーション |

---

## 参考リンク

- [anthropics/skills リポジトリ](https://github.com/anthropics/skills) — 公式スキルリポジトリ
- [スキルとは？（公式サポート）](https://support.claude.com/en/articles/12512176-what-are-skills)
- [Claude でのスキル使用方法](https://support.claude.com/en/articles/12512180-using-skills-in-claude)
- [カスタムスキルの作成方法](https://support.claude.com/en/articles/12512198-creating-custom-skills)
- [Skills API クイックスタート](https://docs.claude.com/en/api/skills-guide#creating-a-skill)
- [agentskills.io](https://agentskills.io) — Agent Skills 標準仕様
- [Notion Skills for Claude](https://www.notion.so/notiondevs/Notion-Skills-for-Claude-28da4445d27180c7af1df7d8615723d0) — パートナースキル例

---

> **注意**: ドキュメント処理スキル（docx / pdf / pptx / xlsx）はソース公開ライセンスのため、Apache 2.0 とは異なります。その他のスキルはデモ・教育目的であり、本番環境での使用前に十分なテストが必要です。
