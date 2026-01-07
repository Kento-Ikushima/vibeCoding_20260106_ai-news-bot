# セットアップガイド - 動作確認までの手順

このガイドでは、AI技術ニュースBotを動作確認できるようになるまでの手順を説明します。

## 📋 事前準備チェックリスト

- [ ] GitHubリポジトリがプッシュ済み
- [ ] LINE Messaging APIのチャネルを作成済み
- [ ] Channel ID: `2008843686`
- [ ] Channel Secret: `5ba594d83126ce8c3b966f64b22eb477`
- [ ] Gemini Pro APIキーを取得済み（または取得方法を知っている）

---

## ステップ1: LINE Messaging APIの設定を完了

### 1-1. チャネルアクセストークンの取得

1. [LINE Developers Console](https://developers.line.biz/console/)にアクセスしてログイン
2. 作成済みのチャネルを選択（Channel ID: `2008843686`）
3. 左メニューから「Messaging API設定」タブをクリック
4. 「チャネルアクセストークン（長期）」セクションを開く
5. 「発行」ボタンをクリック
6. **表示されたトークンをコピー**（後で使用します）
   - ⚠️ **重要**: このトークンは一度しか表示されません。必ずコピーしてください

### 1-2. ユーザーIDの取得

ユーザーIDは、公式アカウントにメッセージを送信することで取得できます。

#### 方法A: Webhookイベントログから取得（推奨）

1. LINE Developers Consoleで、作成済みのチャネルを選択
2. 「Messaging API設定」タブを開く
3. 「Webhookの利用」セクションを開く
4. 「Webhook URL」に任意のURLを入力（例: `https://example.com/webhook`）
   - ⚠️ このURLは実際には動作しなくても問題ありません
5. 「更新」ボタンをクリック
6. 「応答確認」ボタンをクリックして成功することを確認
7. **LINEアプリで、作成した公式アカウントを友だち追加**
8. **公式アカウントにメッセージを送信**（「テスト」など）
9. LINE Developers Consoleに戻り、「Messaging API」→「Webhook」タブを開く
10. 「イベント」セクションで、送信したメッセージのイベントを確認
11. イベントのJSONを展開して、`source.userId`の値を探す
    - 例: `"userId": "U1234567890abcdef1234567890abcdef"`
12. **この`userId`の値をコピー**（後で使用します）
    - ⚠️ ユーザーIDは`U`で始まる長い文字列です

#### 方法B: 簡易的なWebhookサーバーで取得（上級者向け）

もし方法Aで取得できない場合は、ngrok等を使って簡易的なWebhookサーバーを立ち上げ、ユーザーIDをログ出力する方法もあります。

---

## ステップ2: Gemini Pro APIキーの取得（まだの場合）

1. [Google AI Studio](https://makersuite.google.com/app/apikey)にアクセス
2. Googleアカウントでログイン
3. 「Create API Key」をクリック
4. プロジェクトを選択（または新規作成）
5. **発行されたAPIキーをコピー**（後で使用します）

---

## ステップ3: GitHub Secretsの設定

GitHub Secretsに、取得した各種トークンやキーを設定します。

### 3-1. GitHub Secretsの設定画面を開く

1. リポジトリページ（https://github.com/Kento-Ikushima/vibeCoding_20260106_ai-news-bot）にアクセス
2. リポジトリの上部メニューから「**Settings**」をクリック
3. 左サイドバーから「**Secrets and variables**」を展開
4. 「**Actions**」をクリック
5. 「**New repository secret**」ボタンをクリック

### 3-2. 各シークレットを追加

以下のシークレットを**1つずつ**追加します。名前と値を間違えないように注意してください。

#### ① LINE_CHANNEL_ACCESS_TOKEN
- **Name**: `LINE_CHANNEL_ACCESS_TOKEN`
- **Secret**: ステップ1-1で取得したチャネルアクセストークン
- 「**Add secret**」をクリック

#### ② LINE_CHANNEL_ID
- **Name**: `LINE_CHANNEL_ID`
- **Secret**: `2008843686`
- 「**Add secret**」をクリック

#### ③ LINE_CHANNEL_SECRET
- **Name**: `LINE_CHANNEL_SECRET`
- **Secret**: `5ba594d83126ce8c3b966f64b22eb477`
- 「**Add secret**」をクリック

#### ④ LINE_USER_ID
- **Name**: `LINE_USER_ID`
- **Secret**: ステップ1-2で取得したユーザーID（`U`で始まる文字列）
- 「**Add secret**」をクリック

#### ⑤ GEMINI_API_KEY
- **Name**: `GEMINI_API_KEY`
- **Secret**: ステップ2で取得したGemini Pro APIキー
- 「**Add secret**」をクリック

#### ⑥ OPENAI_API_KEY（オプション）
- **Name**: `OPENAI_API_KEY`
- **Secret**: OpenAI APIキー（フォールバック用、持っている場合のみ）
- 「**Add secret**」をクリック

### 3-3. 設定確認

すべてのシークレットを追加したら、「Secrets」セクションに以下の6つ（または5つ、OPENAI_API_KEYなしの場合）が表示されていることを確認します：

- ✅ LINE_CHANNEL_ACCESS_TOKEN
- ✅ LINE_CHANNEL_ID
- ✅ LINE_CHANNEL_SECRET
- ✅ LINE_USER_ID
- ✅ GEMINI_API_KEY
- ✅ OPENAI_API_KEY（オプション）

---

## ステップ4: GitHub Actionsで手動実行（動作確認）

GitHub Secretsの設定が完了したら、実際にBotを実行して動作確認します。

### 4-1. GitHub Actionsの画面を開く

1. リポジトリページの上部メニューから「**Actions**」タブをクリック
2. 左サイドバーから「**AI技術ニュース通知**」ワークフローを選択

### 4-2. ワークフローを手動実行

1. 「**Run workflow**」ドロップダウンボタンをクリック
2. 「**Run workflow**」をクリック
3. 実行が開始されます（数秒かかります）

### 4-3. 実行結果を確認

1. 実行一覧から、今実行したワークフローをクリック
2. 「**記事収集・通知実行**」ステップをクリックしてログを確認
3. 以下のようなメッセージが表示されれば成功：
   ```
   記事を収集中...
   収集した記事数: XX
   記事を選択中...
   選択された記事: [記事タイトル]
   要約を生成中...
   LINE通知を送信中...
   LINE通知を送信しました
   処理が完了しました
   ```

### 4-4. LINEで通知を確認

1. LINEアプリを開く
2. 公式アカウントとのトーク画面を確認
3. **AI技術ニュースの通知が届いていることを確認**

---

## ✅ 動作確認チェックリスト

動作確認が完了したら、以下をチェックしてください：

- [ ] GitHub Actionsの実行が成功した
- [ ] ログにエラーが表示されていない
- [ ] LINEに通知が届いた
- [ ] 通知内容が正しい（タイトル、要約、リンクが含まれている）
- [ ] 履歴ファイルが更新された（`data/notified_articles.json`がコミットされた）

---

## 🐛 トラブルシューティング

### エラー: LINE_CHANNEL_ACCESS_TOKENが設定されていません

→ GitHub Secretsに`LINE_CHANNEL_ACCESS_TOKEN`が正しく設定されているか確認してください。名前のスペルミスがないか確認してください。

### エラー: LINE_USER_IDが設定されていません

→ GitHub Secretsに`LINE_USER_ID`が正しく設定されているか確認してください。ユーザーIDは`U`で始まる文字列です。

### エラー: LINE通知送信エラー: 401 Unauthorized

→ チャネルアクセストークンが間違っている可能性があります。LINE Developers Consoleで新しいトークンを発行してください。

### エラー: LINE通知送信エラー: 400 Bad Request

→ ユーザーIDが間違っている可能性があります。公式アカウントを友だち追加しているか、正しいユーザーIDを取得できているか確認してください。

### 記事が見つかりませんでした

→ スクレイピング対象のサイトが変更されている可能性があります。ログを確認して、どのサイトでエラーが発生しているか確認してください。

### 要約の生成に失敗しました

→ Gemini APIキーが正しく設定されているか確認してください。また、APIのレート制限に達していないか確認してください。

---

## 🔄 自動実行の確認

手動実行が成功したら、自動実行（毎朝8時JST）も確認してください。

1. GitHub Actionsの「AI技術ニュース通知」ワークフローを確認
2. 「Schedule」でスケジュール実行が設定されていることを確認
3. 次の実行時刻を確認（UTC 23:00 = JST 8:00）

---

## 📝 次のステップ

動作確認が完了したら：

1. ✅ 毎朝8時に自動実行されることを確認
2. ✅ 通知内容を確認して、必要に応じて調整
3. ✅ スクレイピング対象サイトが正しく動作しているか確認

問題があれば、GitHub Actionsのログを確認して、エラー内容を特定してください。

---

**作成日**: 2025年1月5日  
**最終更新**: 2025年1月5日

