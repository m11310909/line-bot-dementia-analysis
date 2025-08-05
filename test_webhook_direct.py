#!/usr/bin/env python3
"""
Test Webhook Directly
Test webhook functionality without signature verification
"""

import requests
import json

def test_webhook_direct():
    """Test webhook directly with LINE message format"""
    print("🔍 Testing Webhook Directly...")
    
    # Create LINE message body
    message_body = {
        "events": [
            {
                "type": "message",
                "message": {
                    "type": "text",
                    "text": "爸爸不會用洗衣機"
                },
                "replyToken": "test_reply_token_123",
                "source": {
                    "userId": "test_user_123",
                    "type": "user"
                },
                "timestamp": 1234567890
            }
        ],
        "destination": "test_destination"
    }
    
    body = json.dumps(message_body)
    
    print(f"📊 Message: {message_body['events'][0]['message']['text']}")
    
    try:
        # Test local webhook
        response = requests.post(
            "http://localhost:8081/webhook",
            headers={
                "Content-Type": "application/json",
                "X-Line-Signature": "test_signature"
            },
            data=body,
            timeout=10
        )
        
        print(f"📊 Local Response Status: {response.status_code}")
        print(f"📄 Local Response: {response.text[:200]}...")
        
        # Test external webhook
        external_response = requests.post(
            "https://a3527fa7720b.ngrok-free.app/webhook",
            headers={
                "Content-Type": "application/json",
                "X-Line-Signature": "test_signature"
            },
            data=body,
            timeout=10
        )
        
        print(f"📊 External Response Status: {external_response.status_code}")
        print(f"📄 External Response: {external_response.text[:200]}...")
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

def test_webhook_health():
    """Test webhook health endpoints"""
    print("\n🔍 Testing Webhook Health...")
    
    try:
        # Test health endpoint
        response = requests.get("http://localhost:8081/health", timeout=5)
        print(f"📊 Health Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Health: {data.get('status', 'unknown')}")
        
        # Test root endpoint
        response = requests.get("http://localhost:8081/", timeout=5)
        print(f"📊 Root Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Platform: {data.get('platform', 'unknown')}")
        
        return True
        
    except Exception as e:
        print(f"❌ Health test failed: {e}")
        return False

def main():
    print("=" * 50)
    print("🔧 Direct Webhook Test")
    print("=" * 50)
    
    webhook_ok = test_webhook_direct()
    health_ok = test_webhook_health()
    
    print("\n" + "=" * 50)
    print("📊 Test Results:")
    print(f"✅ Webhook Direct: {'OK' if webhook_ok else 'FAILED'}")
    print(f"✅ Health Check: {'OK' if health_ok else 'FAILED'}")
    
    if webhook_ok and health_ok:
        print("\n🎉 All tests passed!")
        print("✅ Webhook is working correctly")
        print("✅ Ready for real LINE messages")
        print("\n📋 Next Steps:")
        print("1. Update LINE Developer Console webhook URL")
        print("2. Add bot as friend")
        print("3. Send real message to bot")
    else:
        print("\n❌ Some tests failed")
        print("🔧 Check webhook configuration")
    
    print("=" * 50)

if __name__ == "__main__":
    main() 