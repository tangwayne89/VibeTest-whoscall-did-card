#!/usr/bin/env python3
"""
BriefCard - Crawl4AI 基本功能測試
驗證 Crawl4AI 安裝和基本爬取功能
"""

import asyncio
import time
from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig

async def test_basic_crawling():
    """測試基本網頁爬取功能"""
    
    print("🕷️ 開始測試 Crawl4AI 基本功能...")
    
    # 測試網址列表
    test_urls = [
        "https://example.com",
        "https://httpbin.org/html",  # 簡單的 HTML 測試頁面
        "https://quotes.toscrape.com"  # 專門用於測試爬蟲的網站
    ]
    
    browser_cfg = BrowserConfig(
        headless=True,
        viewport_width=1920,
        viewport_height=1080
    )
    
    try:
        async with AsyncWebCrawler(config=browser_cfg) as crawler:
            
            for i, url in enumerate(test_urls, 1):
                print(f"\n📄 測試 {i}: 爬取 {url}")
                
                start_time = time.time()
                
                try:
                    result = await crawler.arun(url=url)
                    end_time = time.time()
                    
                    if result.success:
                        print(f"✅ 爬取成功！")
                        print(f"⏱️  耗時: {end_time - start_time:.2f} 秒")
                        print(f"📏 內容長度: {len(result.markdown)} 字元")
                        print(f"🖼️  圖片數量: {len(result.media.get('images', []))}")
                        print(f"🔗 連結數量: {len(result.links.get('internal', []) + result.links.get('external', []))}")
                        
                        # 顯示前 200 字元的內容預覽
                        preview = result.markdown[:200].replace('\n', ' ')
                        print(f"📝 內容預覽: {preview}...")
                        
                    else:
                        print(f"❌ 爬取失敗: {result.error_message}")
                        
                except Exception as e:
                    print(f"❌ 爬取出錯: {e}")
                
                # 避免請求過於頻繁
                await asyncio.sleep(1)
        
        print("\n🎉 Crawl4AI 基本功能測試完成！")
        print("📝 下一步：測試 AI 驅動的內容提取")
        
    except Exception as e:
        print(f"❌ Crawl4AI 測試失敗: {e}")
        print("💡 請確認已正確安裝 Crawl4AI 並執行 crawl4ai-setup")

async def test_ai_extraction():
    """測試 AI 驅動的內容提取 (需要 API Key)"""
    
    print("\n🤖 測試 AI 內容提取功能...")
    print("💡 這個測試需要 DeepSeek API Key")
    print("   如果還沒申請，可以先跳過這個測試")
    
    # 這裡我們只做基本的 markdown 提取，不使用 LLM
    # 等獲得 DeepSeek API Key 後再進行完整測試
    
    test_url = "https://quotes.toscrape.com"
    
    try:
        async with AsyncWebCrawler() as crawler:
            result = await crawler.arun(url=test_url)
            
            if result.success:
                print("✅ 基本內容提取成功")
                print("📋 可以進行下一步：整合 DeepSeek API")
            else:
                print(f"❌ 內容提取失敗: {result.error_message}")
                
    except Exception as e:
        print(f"❌ AI 提取測試失敗: {e}")

if __name__ == "__main__":
    print("💡 請先確認已安裝 Crawl4AI:")
    print("   pip install crawl4ai")
    print("   crawl4ai-setup")
    print("   crawl4ai-doctor")
    print()
    
    # 運行基本測試
    asyncio.run(test_basic_crawling())
    
    # 運行 AI 提取測試
    asyncio.run(test_ai_extraction())