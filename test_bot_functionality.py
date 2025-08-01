#!/usr/bin/env python3
"""
Test script to simulate LINE Bot messages and test dementia analysis functionality
"""

import requests
import json
import time
from datetime import datetime

# Configuration
WEBHOOK_URL = "https://9d189967bd36.ngrok-free.app/webhook"
TEST_MESSAGES = [
    "我最近發現我媽媽經常忘記事情，她會重複問同樣的問題",
    "我爸爸最近變得比較容易生氣，而且睡眠時間變得不規律",
    "我爺爺最近在熟悉的地方也會迷路，這正常嗎？",
    "我奶奶最近不太愛說話，而且對以前喜歡的活動失去興趣",
    "我媽媽最近在處理金錢方面有困難，她以前很會理財的"
]

def create_line_event(user_id="U123456789", message_text="測試訊息"):
    """Create a simulated LINE Bot event"""
    return {
        "events": [
            {
                "type": "message",
                "mode": "active",
                "timestamp": int(time.time() * 1000),
                "source": {
                    "type": "user",
                    "userId": user_id
                },
                "webhookEventId": "test_event_id",
                "deliveryContext": {
                    "isRedelivery": False
                },
                "replyToken": "test_reply_token",
                "message": {
                    "id": "test_message_id",
                    "type": "text",
                    "quoteToken": None,
                    "text": message_text
                }
            }
        ],
        "destination": "test_destination"
    }

def test_webhook_endpoint():
    """Test the webhook endpoint with simulated LINE Bot events"""
    print("🧪 Testing LINE Bot Webhook Functionality")
    print("=" * 50)
    
    for i, message in enumerate(TEST_MESSAGES, 1):
        print(f"\n📝 Test {i}: {message}")
        
        # Create LINE event
        event_data = create_line_event(message_text=message)
        
        # Add LINE signature (simulated)
        headers = {
            "Content-Type": "application/json",
            "X-Line-Signature": "test_signature"
        }
        
        try:
            # Send POST request to webhook
            response = requests.post(
                WEBHOOK_URL,
                json=event_data,
                headers=headers,
                timeout=10
            )
            
            print(f"✅ Status Code: {response.status_code}")
            print(f"📤 Response: {response.text[:200]}...")
            
        except requests.exceptions.RequestException as e:
            print(f"❌ Error: {e}")
        
        time.sleep(1)  # Small delay between tests

def test_health_endpoint():
    """Test the health endpoint"""
    print("\n🏥 Testing Health Endpoint")
    print("=" * 30)
    
    try:
        response = requests.get(f"{WEBHOOK_URL.replace('/webhook', '')}/health")
        print(f"✅ Status Code: {response.status_code}")
        print(f"📊 Health Data: {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"❌ Error: {e}")

def test_rag_status():
    """Test the RAG status endpoint"""
    print("\n🧠 Testing RAG Status Endpoint")
    print("=" * 30)
    
    try:
        response = requests.get(f"{WEBHOOK_URL.replace('/webhook', '')}/rag-status")
        print(f"✅ Status Code: {response.status_code}")
        print(f"📊 RAG Status: {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"❌ Error: {e}")

def main():
    """Main test function"""
    print("🚀 LINE Bot Dementia Analysis Test Suite")
    print("=" * 50)
    print(f"📍 Webhook URL: {WEBHOOK_URL}")
    print(f"⏰ Test Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 50)
    
    # Test health endpoint first
    test_health_endpoint()
    
    # Test RAG status
    test_rag_status()
    
    # Test webhook functionality
    test_webhook_endpoint()
    
    print("\n" + "=" * 50)
    print("✅ Test suite completed!")
    print("📋 Next Steps:")
    print("   1. Update LINE Developer Console webhook URL")
    print("   2. Add bot as friend in LINE")
    print("   3. Send real messages to test")
    print("=" * 50)

if __name__ == "__main__":
    main() 