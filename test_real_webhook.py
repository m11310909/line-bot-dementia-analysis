#!/usr/bin/env python3
"""
Test script to simulate real LINE Bot webhook calls
"""

import requests
import json
import time
import hmac
import hashlib
import base64

# Configuration
WEBHOOK_URL = "https://9d189967bd36.ngrok-free.app/webhook"
LINE_CHANNEL_SECRET = "091dfc73fed73a681e4e7ea5d9eb461b"  # From your .env file

def create_line_signature(body: str, secret: str) -> str:
    """Create a proper LINE signature"""
    hash = hmac.new(
        secret.encode('utf-8'),
        body.encode('utf-8'),
        hashlib.sha256
    ).digest()
    return base64.b64encode(hash).decode('utf-8')

def test_real_webhook():
    """Test the webhook with proper LINE signature"""
    print("🧪 Testing Real LINE Bot Webhook")
    print("=" * 50)
    
    # Test message
    test_message = "我媽媽最近經常忘記事情，會重複問同樣的問題"
    
    # Create LINE event
    event_data = {
        "events": [
            {
                "type": "message",
                "mode": "active",
                "timestamp": int(time.time() * 1000),
                "source": {
                    "type": "user",
                    "userId": "U123456789"
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
                    "text": test_message
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
    
    print(f"📝 Test Message: {test_message}")
    print(f"🔐 Signature: {signature[:20]}...")
    
    try:
        # Send POST request to webhook
        response = requests.post(
            WEBHOOK_URL,
            data=body,
            headers=headers,
            timeout=30
        )
        
        print(f"✅ Status Code: {response.status_code}")
        print(f"📤 Response: {response.text[:200]}...")
        
        if response.status_code == 200:
            print("🎉 SUCCESS: Webhook responded correctly!")
        else:
            print("❌ FAILED: Webhook returned error")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Error: {e}")

def test_health_endpoints():
    """Test health endpoints"""
    print("\n🏥 Testing Health Endpoints")
    print("=" * 30)
    
    base_url = WEBHOOK_URL.replace('/webhook', '')
    
    # Test health endpoint
    try:
        response = requests.get(f"{base_url}/health")
        print(f"✅ Health Status: {response.status_code}")
        health_data = response.json()
        print(f"📊 Services: {list(health_data.get('services', {}).keys())}")
    except Exception as e:
        print(f"❌ Health Error: {e}")
    
    # Test RAG status endpoint
    try:
        response = requests.get(f"{base_url}/rag-status")
        print(f"✅ RAG Status: {response.status_code}")
        rag_data = response.json()
        print(f"🧠 RAG API Status: {rag_data.get('rag_api_status', 'unknown')}")
    except Exception as e:
        print(f"❌ RAG Status Error: {e}")

def main():
    """Main test function"""
    print("🚀 Real LINE Bot Webhook Test")
    print("=" * 50)
    print(f"📍 Webhook URL: {WEBHOOK_URL}")
    print(f"⏰ Test Time: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 50)
    
    # Test health endpoints first
    test_health_endpoints()
    
    # Test real webhook
    test_real_webhook()
    
    print("\n" + "=" * 50)
    print("✅ Test completed!")
    print("📋 Next Steps:")
    print("   1. Update LINE Developer Console webhook URL")
    print("   2. Add bot as friend in LINE")
    print("   3. Send real messages to test")
    print("=" * 50)

if __name__ == "__main__":
    main() 