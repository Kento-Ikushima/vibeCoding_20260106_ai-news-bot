"""
記事選択ロジックモジュール
"""
from typing import List, Dict, Optional
from datetime import datetime

try:
    from .history_manager import HistoryManager
except ImportError:
    from history_manager import HistoryManager


class ArticleSelector:
    """条件に合致する記事を選択するクラス"""
    
    def __init__(self, history_manager: HistoryManager):
        self.history_manager = history_manager
        self.priority_keywords = ["Vive Coding", "生成AI", "Generative AI", "vive coding", "generative ai"]
        self.related_keywords = [
            "言語モデル", "language model", "LLM",
            "レコーディングツール", "recording tool",
            "技術革新", "innovation",
            "AI技術", "AI technology",
            "マルチモーダル", "multimodal",
            "音声AI", "voice AI", "speech AI",
            "コード生成", "code generation"
        ]
    
    def _contains_keywords(self, text: str, keywords: List[str]) -> bool:
        """テキストにキーワードが含まれているかチェック"""
        text_lower = text.lower()
        for keyword in keywords:
            if keyword.lower() in text_lower:
                return True
        return False
    
    def _score_article(self, article: Dict) -> int:
        """記事のスコアを計算（高いほど優先）"""
        score = 0
        title = article.get("title", "")
        
        # 優先キーワードにマッチ
        if self._contains_keywords(title, self.priority_keywords):
            score += 100
        
        # 関連キーワードにマッチ
        if self._contains_keywords(title, self.related_keywords):
            score += 10
        
        # 公開日が新しいほど高スコア（7日以内は追加点）
        published_date = article.get("published_date")
        if published_date:
            try:
                # 日付文字列をパース（簡易版）
                if isinstance(published_date, str):
                    # ISO形式やその他の形式に対応
                    pub_date = datetime.fromisoformat(published_date.replace('Z', '+00:00'))
                    days_ago = (datetime.now(pub_date.tzinfo).replace(tzinfo=None) - pub_date.replace(tzinfo=None)).days
                    if days_ago <= 7:
                        score += 20 - days_ago * 2
            except:
                pass
        
        return score
    
    def select_article(self, articles: List[Dict]) -> Optional[Dict]:
        """記事リストから最適な記事を1件選択"""
        if not articles:
            return None
        
        # 重複チェック：通知済み記事を除外
        candidate_articles = []
        for article in articles:
            url = article.get("url", "")
            title = article.get("title", "")
            
            if not self.history_manager.is_notified(url, title):
                candidate_articles.append(article)
        
        if not candidate_articles:
            return None
        
        # 優先キーワードを含む記事を優先
        priority_articles = [
            a for a in candidate_articles
            if self._contains_keywords(a.get("title", ""), self.priority_keywords)
        ]
        
        if priority_articles:
            candidate_articles = priority_articles
        
        # スコアでソート
        scored_articles = [
            (article, self._score_article(article))
            for article in candidate_articles
        ]
        scored_articles.sort(key=lambda x: x[1], reverse=True)
        
        # 最もスコアが高い記事を返す
        if scored_articles:
            return scored_articles[0][0]
        
        return None

