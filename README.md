# AI技術ニュース通知Bot

毎朝8時（JST）に最新のAI技術情報を収集し、LINE Notifyで個人のLINEアカウントに通知するGitHub ActionsベースのBotです。

## 機能

- **自動記事収集**: 複数の日本語AI技術ニュースサイトから最新記事を収集
- **スマート選択**: 「Vive Coding」「生成AI」などのキーワードを優先して記事を選択
- **重複防止**: 過去に通知した記事は再度通知されません
- **AI要約**: Google Gemini Pro APIを使用して記事を要約（フォールバック: OpenAI API）
- **LINE通知**: わかりやすい形式でLINE Notify経由で通知

## 対象サイト

- AI-SCHOLAR
- AIZINE
- ITmedia AI
- 日経XTECH AI
- TechCrunch Japan AI
- ZDNet Japan AI

## セットアップ

> 📖 **詳細なセットアップ手順**: [SETUP_GUIDE.md](./SETUP_GUIDE.md) を参照してください。動作確認までの具体的な手順を説明しています。

### 1. リポジトリの準備

```bash
git clone <このリポジトリのURL>
cd ai-news-bot
```

### 2. 必要なAPIキー・トークンの取得

#### LINE Messaging API の設定
1. [LINE Developers](https://developers.line.biz/ja/)にアクセスしてログイン
2. 「プロバイダー」を作成（まだ作成していない場合）
3. 「チャネルを作成」→「Messaging API」を選択
4. チャネル情報を入力して作成
5. **チャネル情報を確認**：
   - チャネル設定ページの「基本設定」タブで確認：
     - **チャネルID**: `LINE_CHANNEL_ID`として使用（数値）
     - **チャネルシークレット**: `LINE_CHANNEL_SECRET`として使用（英数字の文字列）
6. **チャネルアクセストークン**を発行：
   - チャネル設定ページの「Messaging API設定」タブを開く
   - 「チャネルアクセストークン（長期）」セクションで「発行」をクリック
   - 発行されたトークンをコピー（**`LINE_CHANNEL_ACCESS_TOKEN`**として使用）
7. **ユーザーIDを取得**：
   
   以下の方法でユーザーIDを取得できます：
   
   **方法1: Webhookイベントログから取得（推奨）**
   - お使いのLINEアカウントで、作成した公式アカウントを友だち追加
   - [LINE Developers Console](https://developers.line.biz/console/)で、チャネルの「Messaging API設定」→「Webhookの利用」で「Webhook URL」を一時的に設定（例: `https://example.com/webhook`）
   - Webhook URLの「応答確認」をクリックして成功することを確認（この時点では実際のイベントは保存されません）
   - 公式アカウントに任意のメッセージを送信（「こんにちは」など）
   - [LINE Developers Console](https://developers.line.biz/console/)の「Messaging API」→「Webhook」タブで「イベント」を確認
   - イベントのJSONの中から`source.userId`の値をコピー（**`LINE_USER_ID`**として使用）
   
   **方法2: プロフィール取得APIを使用（一時的なWebhookサーバーが必要）**
   - 簡易的なWebhookサーバーをローカルで起動（ngrok等を使用して公開）
   - 公式アカウントにメッセージを送信してユーザーIDをログ出力
   
   **方法3: 公式アカウントからメッセージを送信**
   - LINE Developers Consoleの「Messaging API」→「Webhook」→「Webhook URL」を設定
   - 公式アカウントからあなた自身にメッセージを送信
   - Webhookイベントから`source.userId`を取得

**注意**: 
- ユーザーIDは、公式アカウントにメッセージを送信するか、公式アカウントからメッセージを受信する必要があります
- ユーザーIDは`U`で始まる文字列です（例: `U1234567890abcdef1234567890abcdef`）

#### Gemini Pro APIキーの取得
1. [Google AI Studio](https://makersuite.google.com/app/apikey)にアクセス
2. Googleアカウントでログイン
3. 「Create API Key」をクリック
4. 発行されたAPIキーをコピー

#### OpenAI APIキー（オプション・フォールバック用）
1. [OpenAI Platform](https://platform.openai.com/api-keys)にアクセス
2. アカウントでログイン
3. 「Create new secret key」をクリック
4. 発行されたAPIキーをコピー

### 3. GitHub Secretsの設定

1. GitHubリポジトリの「Settings」→「Secrets and variables」→「Actions」に移動
2. 「New repository secret」をクリック
3. 以下のシークレットを追加：

   - `LINE_CHANNEL_ACCESS_TOKEN`: LINE Messaging APIのチャネルアクセストークン（必須・Messaging API設定で発行）
   - `LINE_CHANNEL_ID`: LINE Messaging APIのチャネルID（必須・基本設定タブで確認）
   - `LINE_CHANNEL_SECRET`: LINE Messaging APIのチャネルシークレット（必須・基本設定タブで確認）
   - `LINE_USER_ID`: 通知を送信するユーザーID（必須・Webhookイベントから取得、`U`で始まる文字列）
   - `GEMINI_API_KEY`: Gemini Pro APIキー（必須・Google AI Studioで発行、`AIza...`で始まる文字列）
   - `OPENAI_API_KEY`: OpenAI APIキー（オプション、フォールバック用）

### 4. 初回設定の確認

履歴ファイルが正しく作成されているか確認：

```bash
# ローカルでテスト実行する場合
python -m src.main
```

## 使用方法

### 自動実行

GitHub Actionsが毎朝8時（JST）に自動的に実行されます。

### 手動実行

1. GitHubリポジトリの「Actions」タブを開く
2. 「AI技術ニュース通知」ワークフローを選択
3. 「Run workflow」をクリック

### ローカルでのテスト実行

```bash
# 環境変数を設定（Windows PowerShell）
# ⚠️ 実際の値を設定してください（例示の値ではありません）
$env:LINE_CHANNEL_ACCESS_TOKEN="your_channel_access_token_here"
$env:LINE_CHANNEL_ID="your_channel_id_here"
$env:LINE_CHANNEL_SECRET="your_channel_secret_here"
$env:LINE_USER_ID="your_user_id_here"
$env:GEMINI_API_KEY="your_gemini_api_key_here"
$env:OPENAI_API_KEY="your_openai_key_here"  # オプション

# Pythonスクリプトを実行
python -m src.main
```

## ディレクトリ構成

```
.
├── .github/
│   └── workflows/
│       └── daily-news.yml      # GitHub Actionsワークフロー
├── src/
│   ├── __init__.py
│   ├── main.py                 # メイン処理
│   ├── scraper.py              # スクレイピング機能
│   ├── selector.py             # 記事選択ロジック
│   ├── history_manager.py      # 履歴管理
│   ├── summarizer.py           # 要約生成
│   └── line_notifier.py        # LINE通知
├── data/
│   └── notified_articles.json  # 通知履歴
├── requirements.txt            # 依存パッケージ
├── requirements.md             # 要件定義書
└── README.md                   # このファイル
```

## 通知形式

```
📰 AI技術ニュース 【YYYY/MM/DD】

【タイトル】
記事のタイトル

【要約】
記事の要約内容（300-500文字）
- 主要ポイント1
- 主要ポイント2
- 主要ポイント3

【タグ】
#生成AI #ViveCoding #言語モデル

【詳細リンク】
https://example.com/article

---
情報元: AI-SCHOLAR
公開日: YYYY年MM月DD日
```

## 技術スタック

- **Python 3.11+**
- **BeautifulSoup4**: ウェブスクレイピング
- **requests**: HTTPリクエスト
- **LINE Messaging API**: 通知送信
- **Google Gemini Pro API**: 記事要約
- **OpenAI API**: 要約のフォールバック
- **GitHub Actions**: スケジュール実行

## 注意事項

- 各サイトの利用規約とrobots.txtを遵守してください
- APIキーはGitHub Secretsで管理し、リポジトリに直接コミットしないでください
- スクレイピングは適度な間隔を空けて実行されます
- 通知履歴は30日間保持され、その後自動的に削除されます

## トラブルシューティング

### 記事が見つからない
- 各サイトのHTML構造が変更されている可能性があります
- スクレイピングロジックの調整が必要かもしれません

### 要約が生成されない
- APIキーが正しく設定されているか確認してください
- APIのレート制限に達していないか確認してください

### LINE通知が送信されない
- LINEチャネルアクセストークンとユーザーIDが正しく設定されているか確認してください
- 公式アカウントが友だち追加されているか確認してください
- ユーザーIDが正しいか確認してください（Webhookイベントから取得）
- GitHub Actionsのログでエラー内容を確認してください

## ライセンス

MIT License

## 作成日

2025年1月5日

