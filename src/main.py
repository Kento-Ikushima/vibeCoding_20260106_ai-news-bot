"""
メイン処理スクリプト
"""
import sys
import os

# プロジェクトルートをパスに追加
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.scraper import ArticleScraper
from src.selector import ArticleSelector
from src.history_manager import HistoryManager
from src.summarizer import Summarizer
from src.line_notifier import LineNotifier


def main():
    """メイン処理"""
    print("=== AI技術ニュースBot 実行開始 ===")
    
    try:
        # 初期化
        scraper = ArticleScraper()
        history_manager = HistoryManager()
        selector = ArticleSelector(history_manager)
        summarizer = Summarizer()
        notifier = LineNotifier()
        
        # 1. 記事を収集
        print("記事を収集中...")
        articles = scraper.scrape_all()
        print(f"収集した記事数: {len(articles)}")
        
        if not articles:
            print("記事が見つかりませんでした")
            return
        
        # 2. 記事を選択
        print("記事を選択中...")
        selected_article = selector.select_article(articles)
        
        if not selected_article:
            print("通知可能な記事が見つかりませんでした（すべて通知済みの可能性があります）")
            return
        
        print(f"選択された記事: {selected_article['title']}")
        print(f"URL: {selected_article['url']}")
        
        # 3. 要約を生成
        print("要約を生成中...")
        summary = summarizer.summarize(selected_article)
        
        if not summary:
            print("要約の生成に失敗しました（タイトルとリンクのみで通知します）")
        
        # 4. LINE通知を送信
        print("LINE通知を送信中...")
        success = notifier.send_notification(selected_article, summary)
        
        if success:
            # 5. 履歴に追加
            history_manager.add_notified_article(selected_article)
            print("処理が完了しました")
        else:
            print("LINE通知の送信に失敗しました")
            sys.exit(1)
            
    except Exception as e:
        print(f"エラーが発生しました: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()

