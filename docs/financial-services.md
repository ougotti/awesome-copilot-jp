# anthropics/financial-services - 金融・経理業務向け Claude スキル

> [anthropics/financial-services](https://github.com/anthropics/financial-services) は Anthropic が公開している**金融サービス業界向けのエージェント・スキル・データコネクタ**の参照実装リポジトリです。投資銀行・リサーチ・PE・ファンド管理・ウェルスマネジメント・コンプライアンスといった業務を、すぐに導入できる形でカバーしています。

## このリポジトリの特徴

- **業務ワークフロー単位**でパッケージ化されたエージェント（10 種）と垂直スキルプラグイン（7 種 + パートナー提供 2 種）を収録
- **Claude Cowork プラグイン**として直接インストール、または **Managed Agents API**（`/v1/agents`）でバックエンド展開、のいずれも可能（同じシステムプロンプト・スキルを使い、実行環境だけ選べる）
- 11 種の金融データプロバイダーと **MCP** 経由で連携可能
- **Microsoft 365（Excel / PowerPoint / Word / Outlook）連携**のプロビジョニングを同梱

> [!IMPORTANT]
> このリポジトリは**法的・投資助言ではありません**。エージェントはあくまで**ドラフト作成支援**であり、投資推奨・取引執行・リスク承認・台帳記帳・オンボーディング承認などは行いません。すべての出力は**有資格者による確認（ヒューマン・イン・ザ・ループ）が前提**です。

---

## インストール方法

### Claude Cowork（最も簡単）

1. Settings → Plugins → Add plugin
2. リポジトリ URL を貼り付け：`https://github.com/anthropics/financial-services`
3. 必要なエージェント・垂直プラグインを選択

### Claude CLI

```bash
claude plugin marketplace add anthropics/financial-services
claude plugin install financial-analysis@claude-for-financial-services
claude plugin install pitch-agent@claude-for-financial-services
```

### Managed Agents API（バックエンド展開）

```bash
export ANTHROPIC_API_KEY=sk-ant-...
scripts/deploy-managed-agent.sh gl-reconciler
```

---

## カバーする業務ワークフロー

| 業務領域 | 主なユースケース |
|---------|----------------|
| **投資銀行（Investment Banking）** | ピッチデック作成（Comps・先例案件・LBO）、CIM/ティーザー、M&A 会計モデル（Accretion/Dilution）、バイヤーリスト |
| **エクイティリサーチ（Equity Research）** | 決算レビュー、モデル更新、調査ノート、セクター分析、銘柄スクリーニング |
| **プライベートエクイティ（PE）** | ディール発掘・スクリーニング、DD チェックリスト、IC メモ、ポートフォリオ監視、IRR/MOIC 分析 |
| **ファンド管理・経理（Fund Admin & Finance Ops）** | **GL（総勘定元帳）照合**、**月次決算**（見越計上・ロールフォワード・差異説明）、LP 報告書監査、NAV 照合 |
| **ウェルスマネジメント** | クライアント面談準備、ファイナンシャルプラン、ポートフォリオリバランス、租税損失収穫（TLH） |
| **オペレーション・コンプライアンス** | KYC スクリーニング、オンボーディング書類のパース → ルールエンジン実行 |

---

## エージェント一覧（主なもの）

業務ワークフローをまるごと自動化する単位です。

| エージェント | 用途 |
|------------|------|
| **Pitch Agent** | ピッチデック（Comps・先例案件・LBO）の作成 |
| **Meeting Prep Agent** | クライアント会議用ブリーフパックの準備 |
| **Market Researcher** | セクター／テーマ分析 → 業界概況・競争環境マッピング |
| **Earnings Reviewer** | 決算分析 → モデル更新 → 調査ノート生成 |
| **Model Builder** | DCF / LBO / 3 計算書モデルを Excel で即座に構築 |
| **Valuation Reviewer** | GP 資料取り込み → バリュエーション → LP 報告 |
| **GL Reconciler** | 照合ミス（ブレーク）の検出・原因追跡・承認ルーティング |
| **Month-End Closer** | 見越計上・ロールフォワード・差異説明 |
| **Statement Auditor** | LP 決算書の配信前監査 |
| **KYC Screener** | オンボーディング規則エンジンの実行 |

---

## 垂直スキルプラグイン

業務領域ごとにスキルをまとめたパッケージです。

### コアプラグイン

| プラグイン | 主なスキル |
|-----------|-----------|
| **financial-analysis** | Comps（`/comps`）、DCF（`/dcf`）、LBO（`/lbo`）、3 計算書、Excel 監査、デック QC、全データコネクタ |
| **investment-banking** | CIM、ティーザー、バイヤーリスト、M&A モデル、ディール追跡 |
| **equity-research** | 決算分析、カバレッジ開始（`/initiate`）、モデル更新、朝礼ノート、セクター分析 |
| **private-equity** | 発掘、スクリーニング、DD チェックリスト、IC メモ、ポートフォリオ監視 |
| **wealth-management** | クライアントレビュー、ファイナンシャルプラン、リバランス、租税損失収穫 |
| **fund-admin** | GL 照合、見越計上、差異説明、NAV 照合 |
| **operations** | KYC パース・ルール実行 |

### パートナー提供プラグイン

- **LSEG** — 債券評価、スワップカーブ、FX キャリーコスト、オプション変動率
- **S&P Global** — ティアシート、決算プレビュー、ファンディングダイジェスト

---

## 主なスラッシュコマンド

```
/comps          → Comps 分析（取引倍数）
/dcf            → DCF 評価（WACC・感度分析）
/lbo            → LBO モデル
/earnings       → 決算分析ノート
/initiate       → カバレッジ開始レポート
/ic-memo        → IC メモのドラフト
/client-review  → クライアント面談準備
/tlh            → 租税損失収穫の機会抽出
/dd-checklist   → DD チェックリスト
/buyer-list     → 戦略・ファイナンシャルバイヤーのユニバース
```

---

## データコネクタ（MCP 連携）

11 種のデータプロバイダーを `.mcp.json` で差し替え可能です。

| プロバイダー | 機能 |
|------------|------|
| **Daloopa** | 企業財務データ |
| **Morningstar** | ファンド・投資データ |
| **S&P Global** | Capital IQ |
| **FactSet** | マルチアセットデータ |
| **Moody's** | クレジット・ESG データ |
| **MT Newswires** | ニュースフィード |
| **Aiera** | アーニングコール文字起こし |
| **LSEG** | リアルタイム市場データ |
| **PitchBook** | M&A・VC 取引データ |
| **Chronograph** | PE ポートフォリオプラットフォーム |
| **Egnyte / Box** | 文書ストレージ |

---

## 日本の事務・経理現場での活用イメージ

金融専業でなくても、**経理・財務・バックオフィス**の定型業務にそのまま応用できる考え方が多く含まれています。

- **月次決算の効率化** — `Month-End Closer` の考え方を参考に、見越計上・差異コメントのドラフトを自動生成
- **勘定照合（突合）** — `GL Reconciler` のように、台帳と明細のブレークを検出し原因候補を提示
- **取引先審査（KYC 的チェック）** — オンボーディング書類のパース → 社内ルールに沿った確認
- **Excel モデルの自動構築・監査** — `financial-analysis` の Excel 監査スキルで計算ミスや循環参照を検出

> 日本の会計基準・税制・社内規程に合わせるには、スキルファイルへの**社内用語・プロセスの追記**と、有資格者によるレビューが必須です。

---

## カスタマイズのポイント

- **コネクタ交換** — `.mcp.json` を編集して自社データプロバイダーに変更
- **社内プロセス追加** — スキルファイルに社内用語・承認フローを追記
- **ブランドテンプレート** — `/ppt-template` で自社の PowerPoint テンプレートを指定
- **新規ワークフロー** — フォークして独自エージェントを追加

---

## 参考リンク

- [anthropics/financial-services](https://github.com/anthropics/financial-services) — 公式リポジトリ
- [Claude Cowork](https://www.anthropic.com/) — プラグインの実行環境
- [Managed Agents API](https://docs.claude.com/) — バックエンド展開向け API
- [anthropics/skills](https://github.com/anthropics/skills) — 汎用ドキュメント処理スキル（[日本語解説](anthropics-skills.md)）

---

> **注意**: 本ドキュメントは [anthropics/financial-services](https://github.com/anthropics/financial-services) の公開情報を元にした日本語解説です。最新の収録内容・インストール手順は公式リポジトリを確認してください。金融・会計・税務に関する判断は必ず有資格の専門家のレビューを受けてください。
