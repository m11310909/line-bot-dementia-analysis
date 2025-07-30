def handle_message(event):
    logger.info(f"handle_message 被呼叫，event: {event}")#!/usr/bin/env python3
"""
測試 Webhook 功能
"""

import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

def test_webhook_endpoint():
    """測試 webhook 端點"""
    print("🧪 測試 Webhook 端點...")
    
    url = "http://localhost:8005/webhook"
    
    # 模擬 LINE Bot 的 webhook 請求
    test_data = {
        "events": [
            {
                "type": "message",
                "message": {
                    "type": "text",
                    "text": "我媽媽最近常常忘記事情"
                },
                "source": {
                    "userId": "test_user_id"
                },
                "replyToken": "test_reply_token"
            }
        ]
    }
    
    headers = {
        "Content-Type": "application/json",
        "X-Line-Signature": "test_signature"
    }
    
    try:
        response = requests.post(url, json=test_data, headers=headers, timeout=10)
        print(f"狀態碼: {response.status_code}")
        print(f"回應: {response.text}")
        
        if response.status_code == 200:
            print("✅ Webhook 端點正常")
            return True
        else:
            print("❌ Webhook 端點異常")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Webhook 測試失敗: {e}")
        return False

def test_api_endpoints():
    """測試 API 端點"""
    print("\n🌐 測試 API 端點...")
    
    base_url = "http://localhost:8005"
    endpoints = [
        "/",
        "/health",
        "/webhook"
    ]
    
    for endpoint in endpoints:
        try:
            response = requests.get(f"{base_url}{endpoint}", timeout=5)
            print(f"✅ {endpoint} - {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"❌ {endpoint} - 無法連接: {e}")

def test_line_bot_config():
    """測試 LINE Bot 配置"""
    print("\n🤖 測試 LINE Bot 配置...")
    
    # 檢查環境變數
    channel_access_token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")
    channel_secret = os.getenv("LINE_CHANNEL_SECRET")
    
    if channel_access_token and channel_access_token != "your_actual_channel_access_token_here":
        print("✅ LINE Channel Access Token 已設置")
    else:
        print("❌ LINE Channel Access Token 未設置")
    
    if channel_secret and channel_secret != "your_actual_channel_secret_here":
        print("✅ LINE Channel Secret 已設置")
    else:
        print("❌ LINE Channel Secret 未設置")

def main():
    """主測試函數"""
    print("🧪 Webhook 測試開始")
    print("=" * 50)
    
    # 測試 LINE Bot 配置
    test_line_bot_config()
    
    # 測試 API 端點
    test_api_endpoints()
    
    # 測試 webhook 端點
    test_webhook_endpoint()
    
    print("\n" + "=" * 50)
    print("🎯 Webhook 測試完成！")
    print("\n📋 注意事項：")
    print("1. 確保 API 正在運行 (python3 enhanced_m1_m2_m3_integrated_api.py)")
    print("2. 設置正確的 LINE Bot 憑證")
    print("3. 配置 LINE Bot Webhook URL: http://your-domain/webhook")

if __name__ == "__main__":
    main() 