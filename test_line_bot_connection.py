#!/usr/bin/env python3
"""
LINE Bot 連接測試腳本
測試 LINE Bot 的配置和 API 連接
"""

import os
import requests
import json
from linebot import LineBotApi, WebhookHandler

def test_line_bot_config():
    """測試 LINE Bot 配置"""
    print("🔍 測試 LINE Bot 配置...")
    
    # 檢查環境變數
    channel_access_token = os.getenv('LINE_CHANNEL_ACCESS_TOKEN')
    channel_secret = os.getenv('LINE_CHANNEL_SECRET')
    
    print(f"📋 Channel Access Token: {'✅ 已設置' if channel_access_token else '❌ 未設置'}")
    print(f"📋 Channel Secret: {'✅ 已設置' if channel_secret else '❌ 未設置'}")
    
    if not channel_access_token or not channel_secret:
        print("❌ LINE Bot 憑證未設置")
        return False
    
    # 測試 LINE Bot API
    try:
        line_bot_api = LineBotApi(channel_access_token)
        bot_info = line_bot_api.get_bot_info()
        print(f"✅ LINE Bot API 連接成功")
        print(f"🤖 Bot 名稱: {bot_info.display_name}")
        print(f"📝 Bot 描述: {bot_info.description}")
        return True
    except Exception as e:
        print(f"❌ LINE Bot API 連接失敗: {e}")
        return False

def test_rag_api():
    """測試 RAG API"""
    print("\n🔍 測試 RAG API...")
    
    # 測試健康檢查
    try:
        response = requests.get('http://localhost:8005/health', timeout=5)
        if response.status_code == 200:
            data = response.json()
            print("✅ RAG API 健康檢查通過")
            print(f"📊 狀態: {data.get('status')}")
            print(f"📊 M1 chunks: {data.get('engine_info', {}).get('m1_chunks')}")
            print(f"📊 M2 chunks: {data.get('engine_info', {}).get('m2_chunks')}")
            print(f"📊 M3 chunks: {data.get('engine_info', {}).get('m3_chunks')}")
            return True
        else:
            print(f"❌ RAG API 健康檢查失敗: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ 無法連接到 RAG API (端口 8005)")
        return False
    except Exception as e:
        print(f"❌ RAG API 測試失敗: {e}")
        return False

def test_analysis_endpoint():
    """測試分析端點"""
    print("\n🔍 測試分析端點...")
    
    test_input = "奶奶經常迷路"
    
    try:
        response = requests.post(
            'http://localhost:8005/comprehensive-analysis',
            json={"user_input": test_input},
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            print("✅ 分析端點測試成功")
            print(f"📊 輸入: {test_input}")
            print(f"📊 檢測到的模組: {data.get('detected_modules', [])}")
            print(f"📊 分析結果: {data.get('analysis_summary', 'N/A')}")
            return True
        else:
            print(f"❌ 分析端點測試失敗: {response.status_code}")
            print(f"📄 回應: {response.text}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ 無法連接到分析端點")
        return False
    except Exception as e:
        print(f"❌ 分析端點測試失敗: {e}")
        return False

def test_webhook_config():
    """測試 webhook 配置"""
    print("\n🔍 測試 webhook 配置...")
    
    # 檢查 webhook 檔案
    webhook_files = [
        'updated_line_bot_webhook.py',
        'enhanced_line_bot.py',
        'line_bot_app.py'
    ]
    
    for file in webhook_files:
        if os.path.exists(file):
            print(f"✅ 找到 webhook 檔案: {file}")
        else:
            print(f"❌ 未找到 webhook 檔案: {file}")
    
    # 檢查端口配置
    try:
        with open('updated_line_bot_webhook.py', 'r', encoding='utf-8') as f:
            content = f.read()
            if 'localhost:8005' in content:
                print("✅ webhook 配置指向正確的 API 端口 (8005)")
            else:
                print("❌ webhook 配置可能指向錯誤的端口")
    except Exception as e:
        print(f"❌ 無法讀取 webhook 配置: {e}")

def main():
    """主測試函數"""
    print("🚀 LINE Bot 連接測試")
    print("=" * 50)
    
    # 測試 LINE Bot 配置
    line_bot_ok = test_line_bot_config()
    
    # 測試 RAG API
    rag_api_ok = test_rag_api()
    
    # 測試分析端點
    analysis_ok = test_analysis_endpoint()
    
    # 測試 webhook 配置
    test_webhook_config()
    
    print("\n" + "=" * 50)
    print("📊 測試結果總結:")
    print(f"   LINE Bot 配置: {'✅ 通過' if line_bot_ok else '❌ 失敗'}")
    print(f"   RAG API: {'✅ 通過' if rag_api_ok else '❌ 失敗'}")
    print(f"   分析端點: {'✅ 通過' if analysis_ok else '❌ 失敗'}")
    
    if line_bot_ok and rag_api_ok and analysis_ok:
        print("\n🎉 所有測試通過！LINE Bot 應該可以正常回應")
    else:
        print("\n⚠️  部分測試失敗，請檢查配置")

if __name__ == "__main__":
    main() 