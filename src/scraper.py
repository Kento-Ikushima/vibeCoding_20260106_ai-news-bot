"""
ウェブサイトからAI技術ニュースをスクレイピングするモジュール
"""
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import time
import re


class ArticleScraper:
    """各サイトから記事をスクレイピングするクラス"""
    
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        self.session = requests.Session()
        self.session.headers.update(self.headers)
    
    def scrape_ai_scholar(self) -> List[Dict]:
        """AI-SCHOLARから記事を取得"""
        articles = []
        try:
            url = "https://ai-scholar.tech/"
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # AI-SCHOLARの記事リンクを取得（構造に応じて調整が必要）
            article_links = soup.find_all('a', href=True)
            
            for link in article_links[:20]:  # 最新20件を確認
                href = link.get('href', '')
                title = link.get_text(strip=True)
                
                if not href or not title or len(title) < 10:
                    continue
                
                # 相対URLを絶対URLに変換
                if href.startswith('/'):
                    href = f"https://ai-scholar.tech{href}"
                elif not href.startswith('http'):
                    continue
                
                # 公開日時を取得（可能な場合）
                published_date = self._extract_date(link)
                
                articles.append({
                    'url': href,
                    'title': title,
                    'published_date': published_date,
                    'site_name': 'AI-SCHOLAR'
                })
        except Exception as e:
            print(f"AI-SCHOLAR スクレイピングエラー: {e}")
        
        return articles
    
    def scrape_aizine(self) -> List[Dict]:
        """AIZINEから記事を取得"""
        articles = []
        try:
            url = "https://aizine.ai/"
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            article_links = soup.find_all('a', href=True)
            
            for link in article_links[:20]:
                href = link.get('href', '')
                title = link.get_text(strip=True)
                
                if not href or not title or len(title) < 10:
                    continue
                
                if href.startswith('/'):
                    href = f"https://aizine.ai{href}"
                elif not href.startswith('http'):
                    continue
                
                published_date = self._extract_date(link)
                
                articles.append({
                    'url': href,
                    'title': title,
                    'published_date': published_date,
                    'site_name': 'AIZINE'
                })
        except Exception as e:
            print(f"AIZINE スクレイピングエラー: {e}")
        
        return articles
    
    def scrape_itmedia_ai(self) -> List[Dict]:
        """ITmedia AIから記事を取得"""
        articles = []
        try:
            url = "https://www.itmedia.co.jp/news/subtop/ai/"
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            article_links = soup.find_all('a', href=True)
            
            for link in article_links[:20]:
                href = link.get('href', '')
                title = link.get_text(strip=True)
                
                if not href or not title or len(title) < 10:
                    continue
                
                if href.startswith('/'):
                    href = f"https://www.itmedia.co.jp{href}"
                elif href.startswith('//'):
                    href = f"https:{href}"
                elif not href.startswith('http'):
                    continue
                
                published_date = self._extract_date(link)
                
                articles.append({
                    'url': href,
                    'title': title,
                    'published_date': published_date,
                    'site_name': 'ITmedia AI'
                })
        except Exception as e:
            print(f"ITmedia AI スクレイピングエラー: {e}")
        
        return articles
    
    def scrape_nikkei_xtech(self) -> List[Dict]:
        """日経XTECH AIから記事を取得"""
        articles = []
        try:
            url = "https://xtech.nikkei.com/atcl/nxt/column/18/00001/"
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            article_links = soup.find_all('a', href=True)
            
            for link in article_links[:20]:
                href = link.get('href', '')
                title = link.get_text(strip=True)
                
                if not href or not title or len(title) < 10:
                    continue
                
                if href.startswith('/'):
                    href = f"https://xtech.nikkei.com{href}"
                elif not href.startswith('http'):
                    continue
                
                published_date = self._extract_date(link)
                
                articles.append({
                    'url': href,
                    'title': title,
                    'published_date': published_date,
                    'site_name': '日経XTECH AI'
                })
        except Exception as e:
            print(f"日経XTECH AI スクレイピングエラー: {e}")
        
        return articles
    
    def scrape_techcrunch_jp(self) -> List[Dict]:
        """TechCrunch Japan AIから記事を取得"""
        articles = []
        try:
            url = "https://jp.techcrunch.com/tag/ai/"
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            article_links = soup.find_all('a', href=True)
            
            for link in article_links[:20]:
                href = link.get('href', '')
                title = link.get_text(strip=True)
                
                if not href or not title or len(title) < 10:
                    continue
                
                if href.startswith('/'):
                    href = f"https://jp.techcrunch.com{href}"
                elif not href.startswith('http'):
                    continue
                
                published_date = self._extract_date(link)
                
                articles.append({
                    'url': href,
                    'title': title,
                    'published_date': published_date,
                    'site_name': 'TechCrunch Japan'
                })
        except Exception as e:
            print(f"TechCrunch Japan スクレイピングエラー: {e}")
        
        return articles
    
    def scrape_zdnet_jp(self) -> List[Dict]:
        """ZDNet Japan AIから記事を取得"""
        articles = []
        try:
            url = "https://japan.zdnet.com/tag/ai/"
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            article_links = soup.find_all('a', href=True)
            
            for link in article_links[:20]:
                href = link.get('href', '')
                title = link.get_text(strip=True)
                
                if not href or not title or len(title) < 10:
                    continue
                
                if href.startswith('/'):
                    href = f"https://japan.zdnet.com{href}"
                elif not href.startswith('http'):
                    continue
                
                published_date = self._extract_date(link)
                
                articles.append({
                    'url': href,
                    'title': title,
                    'published_date': published_date,
                    'site_name': 'ZDNet Japan'
                })
        except Exception as e:
            print(f"ZDNet Japan スクレイピングエラー: {e}")
        
        return articles
    
    def _extract_date(self, element) -> Optional[str]:
        """要素から公開日時を抽出"""
        try:
            # 親要素や近隣要素から日付を探す
            parent = element.parent
            if parent:
                date_text = parent.get_text()
                # 日付パターンを探す
                date_patterns = [
                    r'(\d{4})[/-](\d{1,2})[/-](\d{1,2})',
                    r'(\d{1,2})[/-](\d{1,2})[/-](\d{4})',
                ]
                for pattern in date_patterns:
                    match = re.search(pattern, date_text)
                    if match:
                        return match.group(0)
        except:
            pass
        return None
    
    def scrape_all(self) -> List[Dict]:
        """すべてのサイトから記事を収集"""
        all_articles = []
        
        scrapers = [
            self.scrape_ai_scholar,
            self.scrape_aizine,
            self.scrape_itmedia_ai,
            self.scrape_nikkei_xtech,
            self.scrape_techcrunch_jp,
            self.scrape_zdnet_jp,
        ]
        
        for scraper in scrapers:
            try:
                articles = scraper()
                all_articles.extend(articles)
                time.sleep(1)  # 各サイト間で1秒待機
            except Exception as e:
                print(f"スクレイピングエラー ({scraper.__name__}): {e}")
        
        # URLで重複を除去
        seen_urls = set()
        unique_articles = []
        for article in all_articles:
            if article['url'] not in seen_urls:
                seen_urls.add(article['url'])
                unique_articles.append(article)
        
        return unique_articles

