"""
LINE Notify通知モジュール
"""
import os
import requests
from typing import Dict
from datetime import datetime


class LineNotifier:
    """LINE Notifyで通知を送信するクラス"""
    
    def __init__(self):
        self.token = os.getenv("LINE_NOTIFY_TOKEN")
        self.api_url = "https://notify-api.line.me/api/notify"
    
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
        """LINE通知を送信"""
        if not self.token:
            print("LINE_NOTIFY_TOKENが設定されていません")
            return False
        
        try:
            message = self.format_message(article, summary)
            
            headers = {
                "Authorization": f"Bearer {self.token}",
                "Content-Type": "application/x-www-form-urlencoded"
            }
            
            data = {
                "message": message
            }
            
            response = requests.post(
                self.api_url,
                headers=headers,
                data=data,
                timeout=10
            )
            
            response.raise_for_status()
            print("LINE通知を送信しました")
            return True
            
        except Exception as e:
            print(f"LINE通知送信エラー: {e}")
            return False

