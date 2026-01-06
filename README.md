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

### 1. リポジトリの準備

```bash
git clone <このリポジトリのURL>
cd ai-news-bot
```

### 2. 必要なAPIキー・トークンの取得

#### LINE Notify トークンの取得
1. [LINE Notify](https://notify-bot.line.me/)にアクセス
2. ログイン後、「マイページ」→「トークンを発行する」
3. トークン名を入力（例: "AI技術ニュースBot"）
4. 通知を送信するトークルームを選択（1-on-1でLINE Notifyから通知を受け取る）
5. 発行されたトークンをコピー

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

   - `LINE_NOTIFY_TOKEN`: LINE Notifyトークン（必須）
   - `GEMINI_API_KEY`: Gemini Pro APIキー（必須）
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
$env:LINE_NOTIFY_TOKEN="your_token"
$env:GEMINI_API_KEY="your_api_key"
$env:OPENAI_API_KEY="your_openai_key"  # オプション

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
- LINE Notifyトークンが正しく設定されているか確認してください
- GitHub Actionsのログでエラー内容を確認してください

## ライセンス

MIT License

## 作成日

2025年1月5日

