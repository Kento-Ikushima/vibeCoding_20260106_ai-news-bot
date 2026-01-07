"""
LINE Messaging API通知モジュール
"""
import os
import requests
from typing import Dict
from datetime import datetime


class LineNotifier:
    """LINE Messaging APIで通知を送信するクラス"""
    
    def __init__(self):
        self.channel_access_token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")
        self.channel_id = os.getenv("LINE_CHANNEL_ID", "2008843686")  # デフォルト値
        self.channel_secret = os.getenv("LINE_CHANNEL_SECRET", "5ba594d83126ce8c3b966f64b22eb477")  # デフォルト値
        self.user_id = os.getenv("LINE_USER_ID")
        self.api_url = "https://api.line.me/v2/bot/message/push"
    
    def format_message(self, article: Dict, summary: str = None) -> str:
        """通知メッセージをフォーマット"""
        title = article.get("title", "")
        url = article.get("url", "")
        site_name = article.get("site_name", "")
        published_date = article.get("published_date", "")
        
        # 日付フォーマット
        today = datetime.now().strftime("%Y/%m/%d")
        date_str = ""
        if published_date:
            try:
                pub_date = datetime.fromisoformat(published_date.replace('Z', '+00:00'))
                date_str = pub_date.strftime("%Y年%m月%d日")
            except:
                date_str = published_date
        
        # メッセージ組み立て
        message = f"""📰 AI技術ニュース 【{today}】

【タイトル】
{title}

"""
        
        if summary:
            message += f"""【要約】
{summary}

"""
        else:
            message += """【要約】
要約の取得に失敗しました。詳細はリンクからご確認ください。

"""
        
        # キーワードからタグを生成
        tags = []
        title_lower = title.lower()
        if "vive coding" in title_lower or "vivecoding" in title_lower:
            tags.append("#ViveCoding")
        if "生成ai" in title_lower or "generative ai" in title_lower:
            tags.append("#生成AI")
        if "言語モデル" in title_lower or "language model" in title_lower or "llm" in title_lower:
            tags.append("#言語モデル")
        
        if tags:
            message += f"""【タグ】
{' '.join(tags)}

"""
        
        message += f"""【詳細リンク】
{url}

---
情報元: {site_name}
"""
        
        if date_str:
            message += f"公開日: {date_str}"
        
        return message
    
    def send_notification(self, article: Dict, summary: str = None) -> bool:
        """LINE Messaging APIで通知を送信"""
        if not self.channel_access_token:
            print("LINE_CHANNEL_ACCESS_TOKENが設定されていません")
            return False
        
        if not self.user_id:
            print("LINE_USER_IDが設定されていません")
            return False
        
        try:
            message_text = self.format_message(article, summary)
            
            # LINE Messaging APIのメッセージ形式
            # 長いメッセージは分割する（最大5000文字）
            messages = []
            if len(message_text) <= 5000:
                messages.append({
                    "type": "text",
                    "text": message_text
                })
            else:
                # 5000文字を超える場合は分割
                chunks = [message_text[i:i+5000] for i in range(0, len(message_text), 5000)]
                for chunk in chunks:
                    messages.append({
                        "type": "text",
                        "text": chunk
                    })
            
            headers = {
                "Authorization": f"Bearer {self.channel_access_token}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "to": self.user_id,
                "messages": messages
            }
            
            response = requests.post(
                self.api_url,
                headers=headers,
                json=payload,
                timeout=10
            )
            
            response.raise_for_status()
            print("LINE通知を送信しました")
            return True
            
        except Exception as e:
            print(f"LINE通知送信エラー: {e}")
            if hasattr(e, 'response') and e.response is not None:
                print(f"エラー詳細: {e.response.text}")
            return False

