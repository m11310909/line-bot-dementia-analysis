#!/usr/bin/env python3
"""
系統測試腳本
"""

import os
import sys
import subprocess
import requests
import json
import time

def test_python_environment():
    """測試 Python 環境"""
    print("🐍 測試 Python 環境...")
    
    # 檢查 Python 版本
    print(f"Python 版本: {sys.version}")
    
    # 檢查必要套件
    packages = ['fastapi', 'redis', 'google.generativeai', 'linebot']
    missing_packages = []
    
    for package in packages:
        try:
            __import__(package)
            print(f"✅ {package} 已安裝")
        except ImportError:
            print(f"❌ {package} 未安裝")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n需要安裝的套件: {', '.join(missing_packages)}")
        return False
    return True

def test_env_file():
    """測試 .env 檔案"""
    print("\n📝 測試 .env 檔案...")
    
    if not os.path.exists('.env'):
        print("❌ .env 檔案不存在")
        return False
    
    with open('.env', 'r') as f:
        content = f.read()
    
    # 檢查憑證
    if 'your_actual_channel_access_token_here' in content:
        print("❌ LINE Bot 憑證未設置")
        return False
    else:
        print("✅ LINE Bot 憑證已設置")
    
    if 'your_actual_gemini_api_key_here' in content:
        print("❌ Gemini API 憑證未設置")
        return False
    else:
        print("✅ Gemini API 憑證已設置")
    
    return True

def test_redis():
    """測試 Redis 連接"""
    print("\n🔴 測試 Redis...")
    
    try:
        import redis
        r = redis.Redis()
        r.ping()
        print("✅ Redis 連接成功")
        return True
    except Exception as e:
        print(f"❌ Redis 連接失敗: {e}")
        return False

def test_api_endpoints():
    """測試 API 端點"""
    print("\n🌐 測試 API 端點...")
    
    base_url = "http://localhost:8005"
    endpoints = [
        "/health",
        "/",
        "/cache/stats"
    ]
    
    for endpoint in endpoints:
        try:
            response = requests.get(f"{base_url}{endpoint}", timeout=5)
            if response.status_code == 200:
                print(f"✅ {endpoint} - 正常")
            else:
                print(f"⚠️  {endpoint} - 狀態碼: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"❌ {endpoint} - 無法連接: {e}")
    
    return True

def test_analysis_endpoint():
    """測試分析端點"""
    print("\n🧠 測試分析端點...")
    
    url = "http://localhost:8005/comprehensive-analysis"
    test_data = {
        "user_input": "我媽媽最近常常忘記事情"
    }
    
    try:
        response = requests.post(url, json=test_data, timeout=10)
        if response.status_code == 200:
            result = response.json()
            print("✅ 分析端點正常")
            print(f"回應時間: {response.elapsed.total_seconds():.2f}秒")
            return True
        else:
            print(f"❌ 分析端點錯誤: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ 分析端點測試失敗: {e}")
        return False

def test_line_bot_connection():
    """測試 LINE Bot 連接"""
    print("\n🤖 測試 LINE Bot 連接...")
    
    try:
        from linebot import LineBotApi
        import os
        
        # 載入環境變數
        from dotenv import load_dotenv
        load_dotenv()
        
        channel_access_token = os.getenv('LINE_CHANNEL_ACCESS_TOKEN')
        if not channel_access_token or channel_access_token == 'your_actual_channel_access_token_here':
            print("❌ LINE Bot 憑證未設置")
            return False
        
        line_bot_api = LineBotApi(channel_access_token)
        profile = line_bot_api.get_profile('test')
        print("✅ LINE Bot 連接成功")
        return True
    except Exception as e:
        print(f"❌ LINE Bot 連接失敗: {e}")
        return False

def main():
    """主測試函數"""
    print("🧪 系統測試開始")
    print("=" * 50)
    
    tests = [
        ("Python 環境", test_python_environment),
        ("環境變數", test_env_file),
        ("Redis 連接", test_redis),
        ("API 端點", test_api_endpoints),
        ("分析功能", test_analysis_endpoint),
        ("LINE Bot 連接", test_line_bot_connection)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} 測試異常: {e}")
            results.append((test_name, False))
    
    # 顯示測試結果
    print("\n" + "=" * 50)
    print("📊 測試結果總結:")
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ 通過" if result else "❌ 失敗"
        print(f"   {test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\n🎯 總計: {passed}/{total} 項測試通過")
    
    if passed == total:
        print("🎉 所有測試通過！系統運行正常")
    else:
        print("⚠️  部分測試失敗，請檢查配置")

if __name__ == "__main__":
    main() 