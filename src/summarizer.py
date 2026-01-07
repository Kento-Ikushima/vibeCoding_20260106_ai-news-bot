"""
記事要約生成モジュール（Gemini Pro API優先、OpenAI API フォールバック）
"""
import os
from typing import Dict, Optional
import requests
import google.generativeai as genai
from openai import OpenAI


class Summarizer:
    """記事の要約を生成するクラス"""
    
    def __init__(self):
        self.gemini_api_key = os.getenv("GEMINI_API_KEY")
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        
        # Gemini APIの初期化
        if self.gemini_api_key:
            genai.configure(api_key=self.gemini_api_key)
    
    def fetch_article_content(self, url: str) -> Optional[str]:
        """記事の本文を取得"""
        try:
            print(f"記事本文を取得中: {url}")
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            }
            response = requests.get(url, headers=headers, timeout=15)
            response.raise_for_status()
            response.encoding = response.apparent_encoding  # エンコーディングを自動判定
            
            from bs4 import BeautifulSoup
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # 不要な要素を削除
            for script in soup(["script", "style", "nav", "header", "footer", "aside", "advertisement"]):
                script.decompose()
            
            # 本文を取得（一般的なタグを試す）
            content_tags = ['article', 'main', '.article-body', '.content', '.post-content', '.entry-content', 'p']
            content = ""
            
            for tag in content_tags:
                if tag.startswith('.'):
                    elements = soup.select(tag)
                else:
                    elements = soup.find_all(tag)
                
                if elements:
                    for elem in elements:
                        text = elem.get_text(strip=True)
                        if len(text) > 100:  # 十分な長さのテキストのみ
                            content += text + "\n"
                    if len(content) > 500:  # 十分なコンテンツが取得できたら終了
                        break
            
            if not content or len(content) < 200:
                # フォールバック：すべてのpタグから取得
                paragraphs = soup.find_all('p')
                content = "\n".join([p.get_text(strip=True) for p in paragraphs if len(p.get_text(strip=True)) > 50])
            
            # 文字数制限（4000文字まで）
            if len(content) > 4000:
                content = content[:4000]
            
            if not content or len(content) < 100:
                print(f"WARNING: 記事本文が短すぎます (長さ: {len(content)}文字)")
                return None
            
            print(f"記事本文を取得成功 (長さ: {len(content)}文字)")
            return content
            
        except Exception as e:
            print(f"ERROR: 記事本文の取得エラー: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def summarize_with_gemini(self, title: str, content: str) -> Optional[str]:
        """Gemini Pro APIで要約を生成"""
        if not self.gemini_api_key:
            return None
        
        try:
            model = genai.GenerativeModel('gemini-pro')
            
            # 長い場合は切り詰め
            content_trimmed = content[:3000] if len(content) > 3000 else content
            
            prompt = f"""以下のAI技術に関する記事のタイトルと本文を読み、わかりやすい日本語で要約してください。

【タイトル】
{title}

【本文】
{content_trimmed}

【要件】
- 300-500文字程度の要約を作成
- 3-5個の箇条書きポイントを含める
- 技術的な専門用語は簡潔に説明する
- 重要な技術名や製品名は必ず含める
- 日本語で記述

【要約】"""
            
            response = model.generate_content(prompt)
            summary = response.text.strip()
            
            return summary
        except Exception as e:
            print(f"Gemini API 要約エラー: {e}")
            return None
    
    def summarize_with_openai(self, title: str, content: str) -> Optional[str]:
        """OpenAI APIで要約を生成（フォールバック）"""
        if not self.openai_api_key:
            return None
        
        try:
            client = OpenAI(api_key=self.openai_api_key)
            
            prompt = f"""以下のAI技術に関する記事のタイトルと本文を読み、わかりやすい日本語で要約してください。

【タイトル】
{title}

【本文】
{content[:3000]}

【要件】
- 300-500文字程度の要約を作成
- 3-5個の箇条書きポイントを含める
- 技術的な専門用語は簡潔に説明する
- 重要な技術名や製品名は必ず含める
- 日本語で記述

【要約】"""
            
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "あなたはAI技術ニュースをわかりやすく要約する専門家です。"},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=500,
                temperature=0.7
            )
            
            summary = response.choices[0].message.content.strip()
            return summary
        except Exception as e:
            print(f"OpenAI API 要約エラー: {e}")
            return None
    
    def summarize(self, article: Dict) -> Optional[str]:
        """記事を要約（Gemini優先、OpenAI フォールバック）"""
        title = article.get("title", "")
        url = article.get("url", "")
        
        print(f"要約生成を開始: {title}")
        
        # 記事本文を取得
        content = self.fetch_article_content(url)
        if not content:
            print("ERROR: 記事本文の取得に失敗したため、要約を生成できません")
            return None
        
        # Gemini Pro APIで要約を試行
        if self.gemini_api_key:
            print("Gemini Pro APIで要約を試行...")
            summary = self.summarize_with_gemini(title, content)
            if summary:
                return summary
            print("Gemini APIでの要約に失敗。OpenAI APIを試行...")
        else:
            print("WARNING: GEMINI_API_KEYが設定されていません。OpenAI APIを試行...")
        
        # Geminiが失敗した場合、OpenAI APIで要約
        if self.openai_api_key:
            summary = self.summarize_with_openai(title, content)
            if summary:
                return summary
        
        print("ERROR: すべての要約APIで失敗しました")
        return None

