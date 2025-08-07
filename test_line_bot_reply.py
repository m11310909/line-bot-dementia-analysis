#!/usr/bin/env python3
"""
測試 LINE Bot 回應功能
"""

import requests
import json
import time

def test_line_bot_reply():
    """測試 LINE Bot 回應功能"""
    print("🔍 測試 LINE Bot 回應功能...")
    
    # 測試不同的訊息類型
    test_messages = [
        "我最近常常忘記事情",
        "我爸爸最近變得比較容易生氣",
        "我爺爺最近在熟悉的地方也會迷路",
        "我奶奶最近不太愛說話",
        "爸爸不會用洗衣機"
    ]
    
    for i, message in enumerate(test_messages, 1):
        print(f"\n📝 測試 {i}: {message}")
        
        current_timestamp = int(time.time() * 1000)
        
        # 模擬 LINE Webhook 事件
        webhook_event = {
            "events": [
                {
                    "type": "message",
                    "mode": "active",
                    "timestamp": current_timestamp,
                    "source": {
                        "type": "user",
                        "userId": f"Utestuser{i}"
                    },
                    "webhookEventId": f"test-{current_timestamp}-{i}",
                    "deliveryContext": {
                        "isRedelivery": False
                    },
                    "message": {
                        "id": f"msg-{current_timestamp}-{i}",
                        "type": "text",
                        "quoteToken": "quote-token",
                        "text": message
                    },
                    "replyToken": f"reply-token-{current_timestamp}-{i}"
                }
            ],
            "destination": "Utestuser"
        }
        
        try:
            response = requests.post(
                "http://localhost:8005/test-webhook",
                json=webhook_event,
                headers={"Content-Type": "application/json"},
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                if result.get("status") == "success":
                    print(f"✅ 測試 {i} 成功")
                else:
                    print(f"⚠️ 測試 {i} 部分成功: {result.get('message', '')}")
            else:
                print(f"❌ 測試 {i} 失敗: {response.status_code}")
                
        except Exception as e:
            print(f"❌ 測試 {i} 錯誤: {e}")
        
        time.sleep(1)  # 避免請求過於頻繁
    
    print("\n📋 測試完成")

if __name__ == "__main__":
    test_line_bot_reply() 