"""
通知済み記事の履歴管理モジュール
"""
import json
import os
from datetime import datetime, timedelta
from typing import List, Dict, Optional


class HistoryManager:
    """通知済み記事の履歴を管理するクラス"""
    
    def __init__(self, history_file: str = "data/notified_articles.json"):
        self.history_file = history_file
        self.history = self._load_history()
    
    def _load_history(self) -> Dict:
        """履歴ファイルを読み込む"""
        if not os.path.exists(self.history_file):
            return {
                "notified_articles": [],
                "last_updated": None
            }
        
        try:
            with open(self.history_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"履歴ファイルの読み込みエラー: {e}")
            return {
                "notified_articles": [],
                "last_updated": None
            }
    
    def _save_history(self):
        """履歴ファイルに保存"""
        os.makedirs(os.path.dirname(self.history_file), exist_ok=True)
        
        try:
            with open(self.history_file, 'w', encoding='utf-8') as f:
                json.dump(self.history, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"履歴ファイルの保存エラー: {e}")
            raise
    
    def is_notified(self, url: str, title: Optional[str] = None) -> bool:
        """記事が既に通知済みかチェック"""
        notified_articles = self.history.get("notified_articles", [])
        
        # URLでチェック
        for article in notified_articles:
            if article.get("url") == url:
                return True
        
        # タイトルでチェック（30日以内）
        if title:
            cutoff_date = datetime.now() - timedelta(days=30)
            for article in notified_articles:
                if article.get("title") == title:
                    notified_at_str = article.get("notified_at")
                    if notified_at_str:
                        try:
                            notified_at = datetime.fromisoformat(notified_at_str.replace('Z', '+00:00'))
                            if notified_at.replace(tzinfo=None) > cutoff_date:
                                return True
                        except:
                            pass
        
        return False
    
    def add_notified_article(self, article: Dict):
        """通知済み記事を履歴に追加"""
        notified_article = {
            "url": article.get("url"),
            "title": article.get("title"),
            "notified_at": datetime.now().isoformat(),
            "article_published_at": article.get("published_date"),
            "site_name": article.get("site_name")
        }
        
        if "notified_articles" not in self.history:
            self.history["notified_articles"] = []
        
        self.history["notified_articles"].append(notified_article)
        self.history["last_updated"] = datetime.now().isoformat()
        
        # 30日以上前の履歴を削除
        self._cleanup_old_history()
        
        self._save_history()
    
    def _cleanup_old_history(self):
        """30日以上前の履歴を削除"""
        cutoff_date = datetime.now() - timedelta(days=30)
        notified_articles = self.history.get("notified_articles", [])
        
        filtered_articles = []
        for article in notified_articles:
            notified_at_str = article.get("notified_at")
            if notified_at_str:
                try:
                    notified_at = datetime.fromisoformat(notified_at_str.replace('Z', '+00:00'))
                    if notified_at.replace(tzinfo=None) > cutoff_date:
                        filtered_articles.append(article)
                except:
                    # 日付パースエラーは保持
                    filtered_articles.append(article)
            else:
                filtered_articles.append(article)
        
        self.history["notified_articles"] = filtered_articles

