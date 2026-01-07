# 設定状況まとめ

このファイルには、現在の設定状況をまとめています。

⚠️ **重要**: 機密情報（APIキー、トークン、シークレット）はGitHub Secretsにのみ設定してください。このファイルやコードに直接書き込まないでください。

## ✅ 設定が必要な情報

### LINE Messaging API
以下の情報をLINE Developers Consoleで取得してください：
- **Channel ID**: チャネルの基本設定タブで確認
- **Channel Secret**: チャネルの基本設定タブで確認
- **User ID**: Webhookイベントから取得（`U`で始まる文字列）
- **Channel Access Token**: Messaging API設定で発行

### Gemini Pro API
- **API Key**: Google AI Studioで発行（`AIza...`で始まる文字列）

## 📝 GitHub Secretsで設定が必要な項目

以下のシークレットをGitHubリポジトリに設定してください：

| シークレット名 | 説明 | 状態 |
|---|---|---|
| `LINE_CHANNEL_ACCESS_TOKEN` | Messaging API設定で発行したトークン | ⚠️ GitHub Secretsに設定 |
| `LINE_CHANNEL_ID` | 基本設定タブで確認したChannel ID | ⚠️ GitHub Secretsに設定 |
| `LINE_CHANNEL_SECRET` | 基本設定タブで確認したChannel Secret | ⚠️ GitHub Secretsに設定 |
| `LINE_USER_ID` | Webhookイベントから取得したユーザーID | ⚠️ GitHub Secretsに設定 |
| `GEMINI_API_KEY` | Google AI Studioで発行したAPIキー | ⚠️ GitHub Secretsに設定 |
| `OPENAI_API_KEY` | （オプション）フォールバック用 | ⚪ 任意 |

## 🚀 次のステップ

1. **LINE Developers Consoleで各種情報を取得**
   - [LINE Developers Console](https://developers.line.biz/console/)にアクセス
   - チャネルを選択
   - 基本設定タブでChannel IDとChannel Secretを確認
   - Messaging API設定でチャネルアクセストークンを発行
   - WebhookイベントからユーザーIDを取得

2. **Gemini APIキーを取得**
   - [Google AI Studio](https://makersuite.google.com/app/apikey)で発行

3. **GitHub Secretsに設定**
   - リポジトリの「Settings」→「Secrets and variables」→「Actions」
   - 上記の6つのシークレットをすべて追加

4. **動作確認**
   - GitHub Actionsで手動実行
   - LINEで通知が届くことを確認

詳細は [SETUP_GUIDE.md](./SETUP_GUIDE.md) を参照してください。

---

**⚠️ セキュリティ注意事項**:
- 機密情報はGitHub Secretsにのみ保存してください
- コードやドキュメントに機密情報を直接書き込まないでください
- もし機密情報を誤ってコミットした場合は、すぐに再発行してください

**最終更新**: 2025年1月5日
