#!/usr/bin/env python3
"""
測試 Webhook 事件處理（跳過簽名驗證）
"""

import requests
import json

def test_webhook_no_signature():
    """測試 webhook 事件處理，跳過簽名驗證"""
    print("🔍 測試 Webhook 事件處理...")
    
    # 模擬 LINE Webhook 事件
    webhook_event = {
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
    
    # 發送請求到測試端點（跳過簽名驗證）
    try:
        response = requests.post(
            "http://localhost:8005/test-webhook",
            json=webhook_event,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        print(f"📋 測試結果:")
        print(f"   狀態碼: {response.status_code}")
        print(f"   回應: {response.text}")
        
        if response.status_code == 200:
            print("✅ Webhook 事件處理測試成功")
        else:
            print("❌ Webhook 事件處理測試失敗")
            
    except requests.exceptions.ConnectionError:
        print("❌ 無法連接到 webhook 端點")
    except Exception as e:
        print(f"❌ 測試失敗: {e}")
    
    print("\n📝 測試完成")

if __name__ == "__main__":
    test_webhook_no_signature() 