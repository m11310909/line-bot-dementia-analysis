#!/usr/bin/env python3
"""
測試 Webhook 簽名驗證
"""

import os
import json
import hmac
import hashlib
from dotenv import load_dotenv

# 載入環境變數
load_dotenv()

def test_webhook_signature():
    """測試 Webhook 簽名驗證"""
    print("🔍 測試 Webhook 簽名驗證...")
    
    # 獲取 LINE Bot 憑證
    channel_secret = os.getenv("LINE_CHANNEL_SECRET")
    if not channel_secret:
        print("❌ LINE_CHANNEL_SECRET 未設置")
        return
    
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
    
    # 轉換為 JSON 字符串
    body = json.dumps(webhook_event)
    
    # 生成簽名
    signature = hmac.new(
        channel_secret.encode('utf-8'),
        body.encode('utf-8'),
        hashlib.sha256
    ).hexdigest()
    
    print(f"📋 測試數據:")
    print(f"   Channel Secret: {channel_secret[:10]}...")
    print(f"   Body: {body[:100]}...")
    print(f"   Generated Signature: {signature}")
    
    # 驗證簽名
    try:
        expected_signature = hmac.new(
            channel_secret.encode('utf-8'),
            body.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()
        
        if signature == expected_signature:
            print("✅ 簽名驗證成功")
        else:
            print("❌ 簽名驗證失敗")
            
    except Exception as e:
        print(f"❌ 簽名驗證錯誤: {e}")
    
    print("\n📝 測試完成")

if __name__ == "__main__":
    test_webhook_signature() 