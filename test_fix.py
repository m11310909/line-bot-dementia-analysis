#!/usr/bin/env python3
"""
測試修復結果
"""

import os
import sys

def test_basic_imports():
    """測試基本導入"""
    print("🔍 測試基本導入...")
    
    try:
        import fastapi
        print("✅ FastAPI 導入成功")
    except ImportError as e:
        print(f"❌ FastAPI 導入失敗: {e}")
        return False
    
    try:
        import redis
        print("✅ Redis 導入成功")
    except ImportError as e:
        print(f"❌ Redis 導入失敗: {e}")
        return False
    
    try:
        import google.generativeai
        print("✅ Google Generative AI 導入成功")
    except ImportError as e:
        print(f"❌ Google Generative AI 導入失敗: {e}")
        return False
    
    return True

def test_custom_modules():
    """測試自定義模組"""
    print("\n🔍 測試自定義模組...")
    
    try:
        from redis_cache_manager import RedisCacheManager
        print("✅ Redis 快取管理器導入成功")
        
        # 測試初始化
        cache_manager = RedisCacheManager()
        if cache_manager.is_available():
            print("✅ Redis 快取管理器初始化成功")
        else:
            print("⚠️  Redis 快取不可用")
    except Exception as e:
        print(f"❌ Redis 快取管理器測試失敗: {e}")
    
    try:
        from optimized_gemini_client import OptimizedGeminiClient
        print("✅ 優化 Gemini 客戶端導入成功")
        
        # 測試初始化
        gemini_client = OptimizedGeminiClient()
        print("✅ 優化 Gemini 客戶端初始化成功")
    except Exception as e:
        print(f"❌ 優化 Gemini 客戶端測試失敗: {e}")

def test_api_file():
    """測試 API 檔案"""
    print("\n🔍 測試 API 檔案...")
    
    try:
        # 嘗試導入 API 檔案
        import enhanced_m1_m2_m3_integrated_api
        print("✅ API 檔案導入成功")
    except Exception as e:
        print(f"❌ API 檔案導入失敗: {e}")
        return False
    
    return True

def test_env_file():
    """測試環境檔案"""
    print("\n🔍 測試環境檔案...")
    
    if os.path.exists('.env'):
        print("✅ .env 檔案存在")
        
        with open('.env', 'r') as f:
            content = f.read()
            
        if 'your_actual_channel_access_token_here' in content:
            print("⚠️  LINE Bot 憑證未設置")
        else:
            print("✅ LINE Bot 憑證已設置")
            
        if 'your_actual_gemini_api_key_here' in content:
            print("⚠️  Gemini API 憑證未設置")
        else:
            print("✅ Gemini API 憑證已設置")
    else:
        print("❌ .env 檔案不存在")

def main():
    """主測試函數"""
    print("🧪 測試修復結果")
    print("=" * 50)
    
    # 測試基本導入
    if not test_basic_imports():
        print("❌ 基本導入測試失敗")
        return
    
    # 測試自定義模組
    test_custom_modules()
    
    # 測試 API 檔案
    if not test_api_file():
        print("❌ API 檔案測試失敗")
        return
    
    # 測試環境檔案
    test_env_file()
    
    print("\n" + "=" * 50)
    print("🎯 修復測試完成！")
    print("\n📋 下一步：")
    print("1. 設置實際的 LINE Bot 和 Gemini API 憑證")
    print("2. 執行: python3 enhanced_m1_m2_m3_integrated_api.py")

if __name__ == "__main__":
    main() 