#!/usr/bin/env python3
"""
調試腳本 - 檢查系統問題
"""

import os
import sys
import traceback

def debug_imports():
    """調試導入問題"""
    print("🔍 調試導入問題...")
    
    # 檢查基本套件
    basic_packages = ['fastapi', 'uvicorn', 'pydantic']
    for pkg in basic_packages:
        try:
            __import__(pkg)
            print(f"✅ {pkg} 導入成功")
        except ImportError as e:
            print(f"❌ {pkg} 導入失敗: {e}")
    
    # 檢查優化套件
    optimization_packages = ['redis', 'google.generativeai']
    for pkg in optimization_packages:
        try:
            __import__(pkg)
            print(f"✅ {pkg} 導入成功")
        except ImportError as e:
            print(f"❌ {pkg} 導入失敗: {e}")
    
    # 檢查 LINE Bot
    try:
        from linebot import LineBotApi
        print("✅ linebot 導入成功")
    except ImportError as e:
        print(f"❌ linebot 導入失敗: {e}")

def debug_env():
    """調試環境變數"""
    print("\n🔍 調試環境變數...")
    
    # 檢查 .env 檔案
    if os.path.exists('.env'):
        print("✅ .env 檔案存在")
        with open('.env', 'r') as f:
            content = f.read()
            lines = content.split('\n')
            for line in lines:
                if line.strip() and not line.startswith('#'):
                    key = line.split('=')[0] if '=' in line else line
                    print(f"   {key}")
    else:
        print("❌ .env 檔案不存在")
    
    # 檢查環境變數
    env_vars = ['LINE_CHANNEL_ACCESS_TOKEN', 'LINE_CHANNEL_SECRET', 'AISTUDIO_API_KEY']
    for var in env_vars:
        value = os.getenv(var)
        if value:
            print(f"✅ {var} = {value[:10]}...")
        else:
            print(f"❌ {var} 未設置")

def debug_files():
    """調試檔案問題"""
    print("\n🔍 調試檔案問題...")
    
    # 檢查重要檔案
    important_files = [
        'enhanced_m1_m2_m3_integrated_api.py',
        'm1_m2_m3_integrated_rag.py',
        'redis_cache_manager.py',
        'optimized_gemini_client.py'
    ]
    
    for file in important_files:
        if os.path.exists(file):
            print(f"✅ {file} 存在")
            # 檢查檔案大小
            size = os.path.getsize(file)
            print(f"   大小: {size} bytes")
        else:
            print(f"❌ {file} 不存在")

def debug_syntax():
    """調試語法問題"""
    print("\n🔍 調試語法問題...")
    
    # 檢查主要 API 檔案的語法
    api_file = 'enhanced_m1_m2_m3_integrated_api.py'
    if os.path.exists(api_file):
        try:
            with open(api_file, 'r') as f:
                content = f.read()
            
            # 嘗試編譯
            compile(content, api_file, 'exec')
            print("✅ API 檔案語法正確")
        except SyntaxError as e:
            print(f"❌ API 檔案語法錯誤: {e}")
            print(f"   行號: {e.lineno}")
            print(f"   錯誤: {e.text}")
        except Exception as e:
            print(f"❌ API 檔案其他錯誤: {e}")

def debug_modules():
    """調試模組問題"""
    print("\n🔍 調試模組問題...")
    
    # 嘗試導入自定義模組
    custom_modules = [
        'm1_m2_m3_integrated_rag',
        'redis_cache_manager',
        'optimized_gemini_client'
    ]
    
    for module in custom_modules:
        try:
            __import__(module)
            print(f"✅ {module} 導入成功")
        except ImportError as e:
            print(f"❌ {module} 導入失敗: {e}")
        except Exception as e:
            print(f"❌ {module} 其他錯誤: {e}")

def main():
    """主調試函數"""
    print("🐛 系統調試開始")
    print("=" * 50)
    
    try:
        debug_imports()
        debug_env()
        debug_files()
        debug_syntax()
        debug_modules()
        
        print("\n" + "=" * 50)
        print("🎯 調試完成！")
        
    except Exception as e:
        print(f"\n❌ 調試過程中發生錯誤: {e}")
        print("詳細錯誤信息:")
        traceback.print_exc()

if __name__ == "__main__":
    main() 