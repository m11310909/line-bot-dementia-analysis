#!/usr/bin/env python3
"""
測試真實 LINE 訊息處理
"""

import requests
import json
import time

def test_real_line_message():
    """測試真實的 LINE 訊息處理"""
    print("🔍 測試真實 LINE 訊息處理...")
    
    # 使用真實的 reply token 格式
    current_timestamp = int(time.time() * 1000)
    
    # 模擬真實的 LINE Webhook 事件
    webhook_event = {
        "events": [
            {
                "type": "message",
                "mode": "active",
                "timestamp": current_timestamp,
                "source": {
                    "type": "user",
                    "userId": "U1234567890abcdef"
                },
                "webhookEventId": f"test-{current_timestamp}",
                "deliveryContext": {
                    "isRedelivery": False
                },
                "message": {
                    "id": f"msg-{current_timestamp}",
                    "type": "text",
                    "quoteToken": "quote-token",
                    "text": "我最近常常忘記事情"
                },
                "replyToken": f"reply-token-{current_timestamp}"
            }
        ],
        "destination": "U1234567890abcdef"
    }
    
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
            result = response.json()
            if result.get("status") == "success":
                print("✅ 真實 LINE 訊息處理測試成功")
            else:
                print(f"⚠️ 測試部分成功: {result.get('message', '')}")
        else:
            print("❌ 真實 LINE 訊息處理測試失敗")
            
    except requests.exceptions.ConnectionError:
        print("❌ 無法連接到服務器")
    except Exception as e:
        print(f"❌ 測試失敗: {e}")

if __name__ == "__main__":
    test_real_line_message() 