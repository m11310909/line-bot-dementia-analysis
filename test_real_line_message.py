#!/usr/bin/env python3
"""
Test Real LINE Message
Simulates a real LINE message with proper signature
"""

import requests
import hmac
import hashlib
import json
import os
from dotenv import load_dotenv

load_dotenv()

def create_line_signature(body, secret):
    """Create LINE signature for webhook verification"""
    signature = hmac.new(
        secret.encode('utf-8'),
        body.encode('utf-8'),
        hashlib.sha256
    ).hexdigest()
    return signature

def test_real_line_message():
    """Test webhook with real LINE message format"""
    print("🔍 Testing Real LINE Message...")
    
    # Get LINE secret
    line_secret = os.getenv('LINE_CHANNEL_SECRET')
    if not line_secret:
        print("❌ LINE_CHANNEL_SECRET not found")
        return False
    
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
    signature = create_line_signature(body, line_secret)
    
    print(f"📊 Message: {message_body['events'][0]['message']['text']}")
    print(f"🔐 Signature: {signature[:20]}...")
    
    try:
        response = requests.post(
            "http://localhost:8081/webhook",
            headers={
                "Content-Type": "application/json",
                "X-Line-Signature": signature
            },
            data=body,
            timeout=10
        )
        
        print(f"📊 Response Status: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ Webhook processed LINE message successfully")
            return True
        else:
            print(f"❌ Webhook error: {response.status_code}")
            print(f"📄 Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

def main():
    print("=" * 50)
    print("🔧 Real LINE Message Test")
    print("=" * 50)
    
    success = test_real_line_message()
    
    print("\n" + "=" * 50)
    if success:
        print("🎉 Test Passed!")
        print("✅ Webhook can process real LINE messages")
        print("✅ Signature verification working")
        print("\n📋 Next Steps:")
        print("1. Update LINE Developer Console webhook URL")
        print("2. Add bot as friend")
        print("3. Send real message to bot")
    else:
        print("❌ Test Failed!")
        print("🔧 Check webhook configuration")
    
    print("=" * 50)

if __name__ == "__main__":
    main() 