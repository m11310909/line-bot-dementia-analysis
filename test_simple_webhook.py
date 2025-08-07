#!/usr/bin/env python3
"""
簡單的 Webhook 測試（不發送 LINE 訊息）
"""

import requests
import json

def test_simple_webhook():
    """簡單的 webhook 測試，不發送 LINE 訊息"""
    print("🔍 簡單 Webhook 測試...")
    
    # 簡單的測試數據
    test_data = {
        "events": [
            {
                "type": "message",
                "mode": "active",
                "timestamp": 1234567890,
                "source": {
                    "type": "user",
                    "userId": "U1234567890abcdef"
                },
                "webhookEventId": "01234567-89ab-cdef-0123-456789abcdef",
                "deliveryContext": {
                    "isRedelivery": False
                },
                "message": {
                    "id": "14353798921116",
                    "type": "text",
                    "quoteToken": "quote-token",
                    "text": "測試訊息"
                },
                "replyToken": "reply-token"
            }
        ],
        "destination": "U1234567890abcdef"
    }
    
    try:
        response = requests.post(
            "http://localhost:8005/test-webhook",
            json=test_data,
            headers={"Content-Type": "application/json"},
            timeout=5
        )
        
        print(f"📋 測試結果:")
        print(f"   狀態碼: {response.status_code}")
        print(f"   回應: {response.text}")
        
        if response.status_code == 200:
            result = response.json()
            if result.get("status") == "success":
                print("✅ Webhook 測試成功")
            else:
                print(f"⚠️ Webhook 測試部分成功: {result.get('message', '')}")
        else:
            print("❌ Webhook 測試失敗")
            
    except requests.exceptions.ConnectionError:
        print("❌ 無法連接到服務器")
    except Exception as e:
        print(f"❌ 測試失敗: {e}")

if __name__ == "__main__":
    test_simple_webhook() 