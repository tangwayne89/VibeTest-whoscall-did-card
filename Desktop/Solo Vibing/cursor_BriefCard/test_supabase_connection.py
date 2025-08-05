#!/usr/bin/env python3
"""
BriefCard - Supabase 連線測試
快速驗證 Supabase 設定是否正確
"""

import os
from supabase import create_client, Client
import json
from datetime import datetime

# 你的 Supabase 配置
SUPABASE_URL = "https://iimqqijtbylbfkyjodct.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImlpbXFxaWp0YnlsYmZreWpvZGN0Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTQzMTk1NDAsImV4cCI6MjA2OTg5NTU0MH0.ooTwZFFVse8dbsO47DQnQ90hqW0ZydfUzohkhbOYwsE"

def test_supabase_connection():
    """測試 Supabase 基本連線和表格操作"""
    
    print("🚀 開始測試 Supabase 連線...")
    
    try:
        # 建立 Supabase 客戶端
        supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
        print("✅ Supabase 客戶端建立成功")
        
        # 測試 1: 檢查表格是否存在
        print("\n📋 測試 1: 檢查資料庫表格...")
        
        # 嘗試查詢 bookmarks 表格 (應該是空的)
        result = supabase.table("bookmarks").select("*").limit(1).execute()
        print(f"✅ bookmarks 表格存在，目前有 {len(result.data)} 筆資料")
        
        # 檢查其他表格
        shares_result = supabase.table("shares").select("*").limit(1).execute()
        print(f"✅ shares 表格存在，目前有 {len(shares_result.data)} 筆資料")
        
        reminders_result = supabase.table("reminders").select("*").limit(1).execute()
        print(f"✅ reminders 表格存在，目前有 {len(reminders_result.data)} 筆資料")
        
        # 測試 2: 測試 Storage (檔案儲存)
        print("\n📁 測試 2: 檢查 Storage 設定...")
        try:
            buckets = supabase.storage.list_buckets()
            print(f"✅ Storage 連線成功，目前有 {len(buckets)} 個 bucket")
        except Exception as e:
            print(f"⚠️ Storage 測試失敗 (這是正常的，我們還沒設定): {e}")
        
        # 測試 3: 測試插入資料 (模擬書籤)
        print("\n💾 測試 3: 測試資料插入...")
        
        test_bookmark = {
            "url": "https://example.com",
            "title": "測試書籤",
            "description": "這是一個測試用的書籤",
            "user_id": "00000000-0000-0000-0000-000000000000"  # 測試用假 UUID
        }
        
        try:
            # 注意：這個可能會因為 RLS 政策而失敗，這是正常的
            insert_result = supabase.table("bookmarks").insert(test_bookmark).execute()
            print("✅ 資料插入成功 (或 RLS 政策運作正常)")
            
            # 如果插入成功，清理測試資料
            if insert_result.data:
                cleanup = supabase.table("bookmarks").delete().eq("url", "https://example.com").execute()
                print("🧹 清理測試資料完成")
                
        except Exception as e:
            print(f"⚠️ 資料插入失敗 (可能是 RLS 政策保護，這是正常的): {e}")
        
        print("\n🎉 Supabase 連線測試完成！")
        print("📝 下一步：設定 Crawl4AI 環境")
        
        return True
        
    except Exception as e:
        print(f"❌ Supabase 連線測試失敗: {e}")
        return False

if __name__ == "__main__":
    # 安裝必要套件提示
    print("💡 請先安裝 Supabase Python 客戶端:")
    print("   pip install supabase")
    print()
    
    test_supabase_connection()