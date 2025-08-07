#!/usr/bin/env python3
import requests
import json
import time

def test_production_webhook():
    print("🧪 測試生產模式 Webhook...")
    
    # Test with a real LINE-like webhook event
    current_timestamp = int(time.time() * 1000)
    webhook_event = {
        "events": [{
            "type": "message",
            "mode": "active",
            "timestamp": current_timestamp,
            "source": {
                "type": "user",
                "userId": "Uproductiontest123"
            },
            "webhookEventId": f"prod-test-{current_timestamp}",
            "deliveryContext": {
                "isRedelivery": False
            },
            "message": {
                "id": f"msg-prod-{current_timestamp}",
                "type": "text",
                "quoteToken": "quote-token-prod",
                "text": "我最近常常忘記事情"
            },
            "replyToken": f"reply-token-prod-{current_timestamp}"
        }],
        "destination": "Uproductiontest123"
    }
    
    try:
        print("📤 發送測試訊息到生產模式...")
        response = requests.post(
            "http://localhost:8005/webhook",
            json=webhook_event,
            headers={"Content-Type": "application/json"},
            timeout=15
        )
        
        print(f"📊 回應狀態: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ 生產模式 Webhook 測試成功!")
            print("💡 現在可以接收真實的 LINE 訊息了")
        else:
            print(f"⚠️ 回應狀態: {response.status_code}")
            print(f"回應內容: {response.text}")
            
    except Exception as e:
        print(f"❌ 測試失敗: {e}")

if __name__ == "__main__":
    test_production_webhook() 