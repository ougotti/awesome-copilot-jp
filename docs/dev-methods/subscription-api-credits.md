# AIの月額プランで使えるAPIクレジットを比較する

> **対象ツール**: ChatGPT / Claude / Gemini ｜ **実行環境**: Chat UI / Cloud ｜ **対象読者**: 自作アプリやスクリプトでAPIを使う開発者 ｜ **最終更新**: 2026-11-18

ChatGPT、Claude、Googleの一部の月額契約には、自作アプリや定期ジョブのAPI料金に充てられるクレジットが付いてきます。契約済みのプランで試すなら、まずクレジットの受取先と、呼び出しに使うAPIキーの所属先が一致しているかを確認します。

## 3社の個人プランを比較する

金額は公式資料にある米ドル建ての付与額です。対象国、契約状態、受け取り条件は各社の請求画面で確認してください。

| 提供元・状態 | 対象プランと月次付与額 | 受取先と主な用途 | 有効期限・更新 |
|---|---|---|---|
| OpenAI（Official / 対象契約に提供中） | ChatGPT Pro 100 / 200 / 500にそれぞれ $100 / $200 / $500。 | 紐づけたOpenAI API組織でResponses API、Agents API、Realtime API、Images APIなどに充当。 | 初回は残りの請求期間に応じて日割り。未使用分は請求期間末に失効。対象契約の更新時に次回分が付与される。[OpenAI公式ガイド](https://developers.openai.com/api/docs/guides/chatgpt-api-credits) |
| Anthropic（Official / 対象契約に提供中） | Claude Maxは $100、Ultraは $200。Claude Proは対象外。 | 紐づけたClaude Console組織でClaude API、Managed Agents、Agent SDKなどに充当。 | 請求期間ごとに付与され、未使用分は期間末に失効。[Claude公式ガイド](https://platform.claude.com/docs/en/about-claude/api-credits-for-subscribers) |
| Google（Official / 対象契約に提供中） | Google AI Pro / Ultra 5x / Ultra 20xにそれぞれ $10 / $40 / $100。 | Google Developer Program経由でCloud Billingアカウントに適用。Gemini API、AI Studio、Firebaseなど対象サービスに充当。 | 初回の特典有効化日を基準に毎月発行。各クレジットは付与から1年で失効。将来分を自動適用する設定がある。[Google公式FAQ](https://developers.google.com/profile/help/benefits?hl=en) |

組織向けでは、対象のChatGPT BusinessとClaude Teamにも特典があります。有償Standard席は1席あたり $20、Premium席は $100 を組織で合算し、月ごとの上限は $500 です。年払い時は付与のタイミングが異なります。詳細は各社の公式資料で確認してください。[OpenAI](https://developers.openai.com/api/docs/guides/chatgpt-api-credits)・[Anthropic](https://platform.claude.com/docs/en/about-claude/api-credits-for-subscribers)

## ChatGPT Proで特典を有効化する

有料Pro契約が有効になってから7日以上経ち、ChatGPTとAPI Platformで同じメールアドレスを使っていることを確認します。操作する人は契約と受取先API組織の両方の所有者である必要があります。APIを初めて使う場合はPersonal API Organizationを選べます。

1. ブラウザーで対象のPro契約を持つアカウントにサインインし、ChatGPTの「設定 → 請求」を開きます。[ChatGPTの請求設定](https://chatgpt.com/settings/billing)
2. APIクレジット特典を選び、受取先のAPI組織と表示された付与額を確認して有効化します。特典が見当たらない場合は契約の経過日数、アカウント、国や対象グループの提供条件を確認します。[対象条件とトラブルシューティング](https://help.openai.com/en/articles/20001626-api-credits-benefit-for-eligible-chatgpt-subscriptions)
3. API Platformで受取先組織に切り替え、請求画面で付与額と失効日を確認します。有効な特典残高があればAPI用の支払い方法を追加せずに利用できます。[API Platformの請求画面](https://platform.openai.com/settings/organization/billing/overview)
4. 受取先組織のプロジェクトでAPIキーを用意し、機密情報を含まない短い入力でResponses APIを試します。利用状況と請求画面で、意図した組織に計上されたかを確認します。[APIクイックスタート](https://developers.openai.com/api/docs/quickstart)・[API利用状況](https://platform.openai.com/usage)

## コーディングツールの利用枠とAPI残高

- **Codex**。ChatGPTでログインしたセッションは契約側の利用枠を使います。APIキー経由でCodexを動かす場合にも、このAPI特典は適用されません。自作アプリからAgents APIを呼び出す場合は特典の対象です。[OpenAI公式ガイド](https://developers.openai.com/api/docs/guides/chatgpt-api-credits)
- **Claude Code**。対話型セッションは月次API特典の対象外です。自分で起動する `claude -p` とClaude Agent SDKは、紐づけたConsole組織のAPIキーを使うと対象になります。Claude契約でログインして起動すると契約の利用枠を使います。GitHub Actions、IDE拡張、デスクトップアプリが起動するClaude Codeは対話型と同様に対象外です。[Claude公式FAQ](https://support.claude.com/en/articles/17154008-monthly-api-credits-for-max-ultra-and-team-plans)
- **Google AI Studio**。Web画面で使えるプラン枠と、プロジェクトのAPIキーを使うGemini APIの請求を確認します。2026年11月13日からAI Studio内でも開発者特典を受け取れます。請求方式によっては特典を利用する前に初回の前払いが必要です。[Google公式発表](https://blog.google/innovation-and-ai/technology/developers-tools/google-cloud-credits-gdp-ai-studio/)・[請求FAQ](https://developers.google.com/profile/help/faq?hl=en)

## 残高切れで定期ジョブをどう扱うか

OpenAIとClaudeは特典分を先に消費し、購入済み残高があればそちらに移ります。OpenAIは両方の残高がなくなると `429 credit_balance_exhausted` を返します。Claudeも請求契約による例外を除き、利用可能な残高が尽きるとリクエストが止まります。Gemini APIはCloud Billingの前払い・後払いによって挙動が変わり、前払い残高が尽きたプロジェクトは自動でFree Tierに戻りません。[OpenAI](https://developers.openai.com/api/docs/guides/chatgpt-api-credits)・[Anthropic](https://platform.claude.com/docs/en/about-claude/api-credits-for-subscribers)・[Google](https://aistudio.google.com/docs/billing)

定期実行で残高不足が起きたら、ジョブを止めて通知するか、購入済み残高や自動補充で継続するかを先に決めます。API残高とリクエスト頻度の上限は別々に確認します。残高不足で停止したジョブは、同じリクエストを繰り返す前に、対象組織と次回の付与日を確認してください。

この記事は2026年11月18日時点の公式資料に基づきます。実際のアカウントでの有効化、請求画面への反映、API呼び出しは未検証です。
