#!/usr/bin/env python3
"""
BriefCard - 網路診斷工具
檢查所有外部服務的連線狀態
"""

import asyncio
import httpx
import socket
import time
from typing import Dict, Any
import logging

# 設定日誌
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class NetworkDiagnostic:
    """網路診斷工具"""
    
    def __init__(self):
        self.results = {}
    
    def test_dns_resolution(self, hostname: str) -> Dict[str, Any]:
        """測試 DNS 解析"""
        try:
            start_time = time.time()
            ip = socket.gethostbyname(hostname)
            duration = time.time() - start_time
            
            return {
                "status": "success",
                "ip": ip,
                "duration": round(duration * 1000, 2),
                "error": None
            }
        except Exception as e:
            return {
                "status": "failed",
                "ip": None,
                "duration": None,
                "error": str(e)
            }
    
    async def test_http_connection(self, url: str, timeout: int = 10) -> Dict[str, Any]:
        """測試 HTTP 連線"""
        try:
            start_time = time.time()
            
            async with httpx.AsyncClient(timeout=timeout) as client:
                response = await client.get(url)
                duration = time.time() - start_time
                
                return {
                    "status": "success",
                    "status_code": response.status_code,
                    "duration": round(duration * 1000, 2),
                    "headers": dict(response.headers),
                    "error": None
                }
        except Exception as e:
            duration = time.time() - start_time
            return {
                "status": "failed",
                "status_code": None,
                "duration": round(duration * 1000, 2),
                "headers": None,
                "error": str(e)
            }
    
    async def test_supabase_connection(self, url: str, api_key: str) -> Dict[str, Any]:
        """測試 Supabase 連線"""
        try:
            headers = {
                "apikey": api_key,
                "Authorization": f"Bearer {api_key}"
            }
            
            start_time = time.time()
            
            async with httpx.AsyncClient(timeout=10) as client:
                # 測試基本連線
                response = await client.get(
                    f"{url}/rest/v1/",
                    headers=headers
                )
                duration = time.time() - start_time
                
                return {
                    "status": "success" if response.status_code in [200, 404] else "failed",
                    "status_code": response.status_code,
                    "duration": round(duration * 1000, 2),
                    "error": None
                }
        except Exception as e:
            duration = time.time() - start_time
            return {
                "status": "failed",
                "status_code": None,
                "duration": round(duration * 1000, 2),
                "error": str(e)
            }
    
    async def test_deepseek_api(self, api_key: str, base_url: str) -> Dict[str, Any]:
        """測試 DeepSeek API"""
        try:
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "model": "deepseek-chat",
                "messages": [{"role": "user", "content": "Hello"}],
                "max_tokens": 10
            }
            
            start_time = time.time()
            
            async with httpx.AsyncClient(timeout=10) as client:
                response = await client.post(
                    f"{base_url}/chat/completions",
                    headers=headers,
                    json=payload
                )
                duration = time.time() - start_time
                
                return {
                    "status": "success" if response.status_code == 200 else "failed",
                    "status_code": response.status_code,
                    "duration": round(duration * 1000, 2),
                    "error": None if response.status_code == 200 else response.text
                }
        except Exception as e:
            duration = time.time() - start_time
            return {
                "status": "failed",
                "status_code": None,
                "duration": round(duration * 1000, 2),
                "error": str(e)
            }
    
    async def run_full_diagnostic(self, 
                                supabase_url: str = "", 
                                supabase_key: str = "",
                                deepseek_key: str = "",
                                deepseek_url: str = "https://api.deepseek.com/v1") -> Dict[str, Any]:
        """執행完整的網路診斷"""
        
        print("🔍 開始網路診斷...")
        print("=" * 60)
        
        results = {}
        
        # 1. 基礎網路測試
        print("\n📡 基礎網路測試")
        print("-" * 30)
        
        basic_hosts = [
            "google.com",
            "github.com", 
            "supabase.co"
        ]
        
        for host in basic_hosts:
            dns_result = self.test_dns_resolution(host)
            print(f"DNS {host}: {'✅' if dns_result['status'] == 'success' else '❌'} "
                  f"({dns_result.get('ip', 'N/A')}) - {dns_result.get('duration', 'N/A')}ms")
            results[f"dns_{host}"] = dns_result
        
        # 2. Supabase 測試
        print("\n🗄️ Supabase 連線測試")
        print("-" * 30)
        
        if supabase_url and supabase_key:
            # 先測試域名解析
            from urllib.parse import urlparse
            hostname = urlparse(supabase_url).netloc
            dns_result = self.test_dns_resolution(hostname)
            print(f"Supabase DNS: {'✅' if dns_result['status'] == 'success' else '❌'} {hostname}")
            results["supabase_dns"] = dns_result
            
            if dns_result['status'] == 'success':
                # 測試 API 連線
                api_result = await self.test_supabase_connection(supabase_url, supabase_key)
                print(f"Supabase API: {'✅' if api_result['status'] == 'success' else '❌'} "
                      f"({api_result.get('status_code', 'N/A')}) - {api_result.get('duration', 'N/A')}ms")
                results["supabase_api"] = api_result
        else:
            print("❌ Supabase 設定缺失")
            results["supabase_api"] = {"status": "skipped", "error": "Missing configuration"}
        
        # 3. DeepSeek API 測試
        print("\n🤖 DeepSeek API 測試")
        print("-" * 30)
        
        if deepseek_key:
            # 先測試域名
            hostname = urlparse(deepseek_url).netloc
            dns_result = self.test_dns_resolution(hostname)
            print(f"DeepSeek DNS: {'✅' if dns_result['status'] == 'success' else '❌'} {hostname}")
            results["deepseek_dns"] = dns_result
            
            if dns_result['status'] == 'success':
                # 測試 API
                api_result = await self.test_deepseek_api(deepseek_key, deepseek_url)
                print(f"DeepSeek API: {'✅' if api_result['status'] == 'success' else '❌'} "
                      f"({api_result.get('status_code', 'N/A')}) - {api_result.get('duration', 'N/A')}ms")
                results["deepseek_api"] = api_result
        else:
            print("❌ DeepSeek API Key 缺失")
            results["deepseek_api"] = {"status": "skipped", "error": "Missing API key"}
        
        # 4. 總結
        print("\n📊 診斷總結")
        print("=" * 60)
        
        total_tests = len([r for r in results.values() if r["status"] != "skipped"])
        successful_tests = len([r for r in results.values() if r["status"] == "success"])
        
        print(f"總測試: {total_tests}")
        print(f"成功: {successful_tests}")
        print(f"失敗: {total_tests - successful_tests}")
        print(f"成功率: {(successful_tests/total_tests*100):.1f}%" if total_tests > 0 else "N/A")
        
        return results

# 主執行程式
async def main():
    """主程式"""
    # 從環境變數或直接輸入獲取設定
    from dotenv import load_dotenv
    import os
    
    load_dotenv()
    
    diagnostic = NetworkDiagnostic()
    
    results = await diagnostic.run_full_diagnostic(
        supabase_url=os.getenv("SUPABASE_URL", ""),
        supabase_key=os.getenv("SUPABASE_ANON_KEY", ""),
        deepseek_key=os.getenv("DEEPSEEK_API_KEY", ""),
        deepseek_url=os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com/v1")
    )
    
    # 提供修復建議
    print("\n🔧 修復建議")
    print("=" * 60)
    
    if results.get("supabase_dns", {}).get("status") == "failed":
        print("❌ Supabase URL 無效，請檢查 .env 檔案中的 SUPABASE_URL")
        print("   前往 https://supabase.com/dashboard 獲取正確的 Project URL")
    
    if results.get("supabase_api", {}).get("status") == "failed":
        print("❌ Supabase API Key 可能無效，請檢查 SUPABASE_ANON_KEY")
    
    if results.get("deepseek_api", {}).get("status") == "failed":
        print("❌ DeepSeek API Key 可能無效，請檢查 DEEPSEEK_API_KEY")
        print("   前往 https://platform.deepseek.com 驗證你的 API Key")

if __name__ == "__main__":
    asyncio.run(main())