#!/usr/bin/env python3
"""
Test script to simulate real LINE Bot messages with proper handling
"""

import requests
import json
import time
import hmac
import hashlib
import base64
import uuid

# Configuration
WEBHOOK_URL = "https://1bd6facd30d6.ngrok-free.app/webhook"
LINE_CHANNEL_SECRET = "091dfc73fed73a681e4e7ea5d9eb461b"

def create_line_signature(body: str, secret: str) -> str:
    """Create a proper LINE signature"""
    hash = hmac.new(
        secret.encode('utf-8'),
        body.encode('utf-8'),
        hashlib.sha256
    ).digest()
    return base64.b64encode(hash).decode('utf-8')

def test_real_line_message():
    """Test with a real LINE message simulation"""
    print("🧪 Testing Real LINE Message")
    print("=" * 50)
    
    # Test messages that should trigger responses
    test_messages = [
        "我媽媽最近經常忘記事情，會重複問同樣的問題",
        "我爸爸最近變得比較容易生氣，而且睡眠時間變得不規律",
        "我爺爺最近在熟悉的地方也會迷路，這正常嗎？",
        "我奶奶最近不太愛說話，而且對以前喜歡的活動失去興趣",
        "爸爸不會用洗衣機"  # This is the message from your screenshot
    ]
    
    for i, message in enumerate(test_messages, 1):
        print(f"\n📝 Test {i}: {message}")
        
        # Create a realistic LINE event
        event_data = {
            "events": [
                {
                    "type": "message",
                    "mode": "active",
                    "timestamp": int(time.time() * 1000),
                    "source": {
                        "type": "user",
                        "userId": f"U{str(uuid.uuid4()).replace('-', '')[:8]}"
                    },
                    "webhookEventId": f"test_event_{i}_{int(time.time())}",
                    "deliveryContext": {
                        "isRedelivery": False
                    },
                    "replyToken": f"test_reply_token_{i}_{int(time.time())}",
                    "message": {
                        "id": f"test_message_{i}_{int(time.time())}",
                        "type": "text",
                        "quoteToken": None,
                        "text": message
                    }
                }
            ],
            "destination": "test_destination"
        }
        
        # Convert to JSON string
        body = json.dumps(event_data)
        
        # Create proper LINE signature
        signature = create_line_signature(body, LINE_CHANNEL_SECRET)
        
        # Headers with proper signature
        headers = {
            "Content-Type": "application/json",
            "X-Line-Signature": signature
        }
        
        try:
            # Send POST request to webhook
            response = requests.post(
                WEBHOOK_URL,
                data=body,
                headers=headers,
                timeout=30
            )
            
            print(f"✅ Status Code: {response.status_code}")
            
            if response.status_code == 200:
                print("🎉 SUCCESS: Webhook processed message correctly!")
            else:
                print(f"❌ FAILED: {response.text[:100]}...")
                
        except requests.exceptions.RequestException as e:
            print(f"❌ Error: {e}")
        
        time.sleep(2)  # Wait between tests

def test_health_endpoints():
    """Test all health endpoints"""
    print("\n🏥 Testing Health Endpoints")
    print("=" * 30)
    
    base_url = WEBHOOK_URL.replace('/webhook', '')
    
    endpoints = [
        ("/health", "Health Check"),
        ("/rag-status", "RAG Status"),
        ("/", "Root Endpoint")
    ]
    
    for endpoint, name in endpoints:
        try:
            response = requests.get(f"{base_url}{endpoint}")
            print(f"✅ {name}: {response.status_code}")
            if response.status_code == 200:
                data = response.json()
                if "status" in data:
                    print(f"   Status: {data['status']}")
        except Exception as e:
            print(f"❌ {name}: {e}")

def test_rag_api_directly():
    """Test RAG API directly"""
    print("\n🧠 Testing RAG API Directly")
    print("=" * 30)
    
    test_message = "爸爸不會用洗衣機"
    
    try:
        response = requests.post(
            "http://localhost:8005/comprehensive-analysis",
            json={"text": test_message},
            timeout=10
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ RAG API working correctly")
            print(f"📊 Response type: {result.get('type', 'unknown')}")
            if 'contents' in result:
                print("📋 Flex message generated successfully")
        else:
            print(f"❌ RAG API error: {response.status_code}")
            print(f"📄 Response: {response.text[:200]}...")
            
    except Exception as e:
        print(f"❌ RAG API test failed: {e}")

def main():
    """Main test function"""
    print("🚀 Real LINE Message Test Suite")
    print("=" * 50)
    print(f"📍 Webhook URL: {WEBHOOK_URL}")
    print(f"⏰ Test Time: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 50)
    
    # Test health endpoints first
    test_health_endpoints()
    
    # Test RAG API directly
    test_rag_api_directly()
    
    # Test real LINE messages
    test_real_line_message()
    
    print("\n" + "=" * 50)
    print("✅ Test completed!")
    print("📋 Next Steps:")
    print("   1. Update LINE Developer Console webhook URL")
    print("   2. Add bot as friend in LINE")
    print("   3. Send real messages to test")
    print("=" * 50)

if __name__ == "__main__":
    main() 