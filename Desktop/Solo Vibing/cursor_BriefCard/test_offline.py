#!/usr/bin/env python3
"""
BriefCard - 離線測試模式
在沒有外部 API 的情況下測試核心功能
"""

import asyncio
import json
from datetime import datetime
from typing import Dict, Any

# 本地匯入（不依賴外部 API）
from crawler_service import WebCrawlerService

class OfflineTest:
    """離線測試類"""
    
    def __init__(self):
        self.crawler = WebCrawlerService()
    
    async def test_crawler_only(self, url: str) -> Dict[str, Any]:
        """僅測試爬蟲功能，不依賴其他服務"""
        print(f"🕷️ 測試爬取: {url}")
        print("-" * 50)
        
        try:
            start_time = datetime.now()
            result = await self.crawler.extract_content(url)
            end_time = datetime.now()
            
            duration = (end_time - start_time).total_seconds()
            
            if result and result.get("success"):
                print("✅ 爬取成功！")
                print(f"📄 標題: {result.get('title', '無標題')}")
                print(f"📝 描述: {result.get('description', '無描述')[:100]}...")
                print(f"🖼️ 圖片: {result.get('image_url', '無圖片')}")
                print(f"📊 字數: {result.get('word_count', 0)} 字")
                print(f"⏱️ 耗時: {duration:.2f} 秒")
                print(f"🔗 最終 URL: {result.get('url')}")
                
                # 顯示內容預覽
                content = result.get('content_markdown', '')
                if content:
                    print(f"\n📃 內容預覽:")
                    print("-" * 30)
                    print(content[:300] + "..." if len(content) > 300 else content)
                
                return {"status": "success", "result": result, "duration": duration}
            else:
                print("❌ 爬取失敗")
                print(f"錯誤: {result.get('error', '未知錯誤')}")
                return {"status": "failed", "error": result.get('error'), "duration": duration}
                
        except Exception as e:
            print(f"❌ 測試異常: {e}")
            return {"status": "error", "error": str(e)}
    
    async def test_multiple_sites(self):
        """測試多個網站"""
        test_urls = [
            "https://httpbin.org/html",  # 簡單的測試頁面
            "https://example.com",       # 基本範例頁面  
            "https://github.com",        # 較複雜的現代網站
            "https://news.ycombinator.com",  # 簡單但有內容的網站
        ]
        
        print("🧪 多網站爬取測試")
        print("=" * 60)
        
        results = {}
        
        for i, url in enumerate(test_urls, 1):
            print(f"\n[{i}/{len(test_urls)}] 測試網站")
            result = await self.test_crawler_only(url)
            results[url] = result
            
            # 在測試間稍作暫停
            await asyncio.sleep(2)
        
        # 統計結果
        print("\n📊 測試總結")
        print("=" * 60)
        
        successful = len([r for r in results.values() if r["status"] == "success"])
        total = len(results)
        
        print(f"總測試: {total}")
        print(f"成功: {successful}")
        print(f"失敗: {total - successful}")
        print(f"成功率: {(successful/total*100):.1f}%")
        
        # 顯示失敗的網站
        failed_sites = [(url, result) for url, result in results.items() 
                       if result["status"] != "success"]
        
        if failed_sites:
            print(f"\n❌ 失敗的網站:")
            for url, result in failed_sites:
                print(f"   {url}: {result.get('error', '未知錯誤')}")
        
        return results
    
    def mock_ai_analysis(self, title: str, content: str) -> Dict[str, Any]:
        """模擬 AI 分析（離線版本）"""
        # 簡單的關鍵詞提取
        words = content.lower().split()
        common_words = ['the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should', 'may', 'might', 'can', 'must']
        
        # 統計詞頻並過濾常見詞
        word_freq = {}
        for word in words:
            clean_word = ''.join(c for c in word if c.isalnum())
            if len(clean_word) > 3 and clean_word not in common_words:
                word_freq[clean_word] = word_freq.get(clean_word, 0) + 1
        
        # 取前5個最常見的詞作為關鍵詞
        keywords = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:5]
        keywords = [word for word, _ in keywords]
        
        # 生成簡單摘要（取前兩句）
        sentences = content.split('.')
        summary = '. '.join(sentences[:2]).strip()
        if summary and not summary.endswith('.'):
            summary += '.'
        
        # 簡單分類
        tech_keywords = ['python', 'javascript', 'code', 'development', 'api', 'software', 'github']
        news_keywords = ['news', 'report', 'today', 'breaking', 'update']
        
        if any(kw in content.lower() for kw in tech_keywords):
            category = "技術/科技"
        elif any(kw in content.lower() for kw in news_keywords):
            category = "新聞時事"
        else:
            category = "其他"
        
        return {
            "summary": summary[:200] + "..." if len(summary) > 200 else summary,
            "keywords": keywords,
            "category": category
        }
    
    async def test_full_pipeline_offline(self, url: str):
        """測試完整的離線處理流程"""
        print(f"🔄 完整離線測試: {url}")
        print("=" * 60)
        
        # 1. 爬取內容
        crawl_result = await self.test_crawler_only(url)
        
        if crawl_result["status"] != "success":
            return crawl_result
        
        content_data = crawl_result["result"]
        
        # 2. 模擬 AI 分析
        print(f"\n🤖 模擬 AI 分析...")
        ai_analysis = self.mock_ai_analysis(
            content_data.get("title", ""),
            content_data.get("content_markdown", "")
        )
        
        print(f"📝 摘要: {ai_analysis['summary']}")
        print(f"🏷️ 關鍵詞: {', '.join(ai_analysis['keywords'])}")
        print(f"📂 分類: {ai_analysis['category']}")
        
        # 3. 模擬最終書籤資料
        bookmark_data = {
            "id": "test-bookmark-123",
            "url": content_data.get("url"),
            "title": content_data.get("title"),
            "description": content_data.get("description"),
            "image_url": content_data.get("image_url"),
            "summary": ai_analysis["summary"],
            "keywords": ai_analysis["keywords"],
            "category": ai_analysis["category"],
            "created_at": datetime.now().isoformat(),
            "status": "completed"
        }
        
        print(f"\n💾 模擬書籤資料:")
        print(json.dumps(bookmark_data, indent=2, ensure_ascii=False))
        
        return {"status": "success", "bookmark": bookmark_data}

async def main():
    """主測試程式"""
    tester = OfflineTest()
    
    print("🧪 BriefCard 離線功能測試")
    print("=" * 60)
    print("這個測試不需要 Supabase 或 DeepSeek API")
    print("僅測試核心的爬蟲和處理邏輯")
    print("=" * 60)
    
    # 選擇測試模式
    print("\n選擇測試模式:")
    print("1. 單一網站完整測試")
    print("2. 多網站爬取測試") 
    print("3. 自訂網址測試")
    
    choice = input("\n請選擇 (1-3): ")
    
    if choice == "1":
        await tester.test_full_pipeline_offline("https://httpbin.org/html")
    elif choice == "2":
        await tester.test_multiple_sites()
    elif choice == "3":
        url = input("請輸入要測試的網址: ")
        await tester.test_full_pipeline_offline(url)
    else:
        print("無效選擇，執行預設測試...")
        await tester.test_full_pipeline_offline("https://httpbin.org/html")

if __name__ == "__main__":
    asyncio.run(main())