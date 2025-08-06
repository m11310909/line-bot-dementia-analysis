#!/usr/bin/env python3
"""
Test LINE Bot Signature Verification
Verifies that the webhook properly handles signature verification
"""

import os
import hmac
import hashlib
import base64
import json
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_signature_verification():
    """Test signature verification with proper LINE Bot credentials"""
    
    print("🔐 Testing LINE Bot Signature Verification")
    print("=" * 50)
    
    # Get credentials from .env
    channel_secret = os.getenv('LINE_CHANNEL_SECRET')
    channel_access_token = os.getenv('LINE_CHANNEL_ACCESS_TOKEN')
    
    if not channel_secret or not channel_access_token:
        print("❌ Missing LINE Bot credentials in .env file")
        print("Please add your credentials to .env:")
        print("LINE_CHANNEL_SECRET=your_secret_here")
        print("LINE_CHANNEL_ACCESS_TOKEN=your_token_here")
        return False
    
    print("✅ LINE Bot credentials found")
    print(f"Channel Secret: {channel_secret[:10]}...")
    print(f"Access Token: {channel_access_token[:10]}...")
    
    # Test webhook endpoint
    webhook_url = "http://localhost:3000/webhook"
    
    # Create test message
    test_message = {
        "events": [
            {
                "type": "message",
                "message": {
                    "type": "text",
                    "text": "測試訊息"
                },
                "source": {
                    "userId": "test_user_id",
                    "type": "user"
                },
                "timestamp": 1234567890
            }
        ]
    }
    
    body = json.dumps(test_message)
    
    # Generate signature (same as LINE does)
    signature = base64.b64encode(
        hmac.new(
            channel_secret.encode('utf-8'),
            body.encode('utf-8'),
            hashlib.sha256
        ).digest()
    ).decode('utf-8')
    
    print(f"\n📝 Test Message: {test_message['events'][0]['message']['text']}")
    print(f"🔑 Generated Signature: {signature}")
    
    # Test webhook with signature
    try:
        headers = {
            'Content-Type': 'application/json',
            'X-Line-Signature': signature
        }
        
        response = requests.post(
            webhook_url,
            data=body,
            headers=headers,
            timeout=10
        )
        
        print(f"\n📡 Webhook Response:")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            print("✅ Signature verification successful!")
            return True
        else:
            print("❌ Signature verification failed")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to webhook service")
        print("Make sure the webhook service is running on port 3000")
        return False
    except Exception as e:
        print(f"❌ Error testing webhook: {e}")
        return False

def test_invalid_signature():
    """Test with invalid signature to ensure security"""
    
    print("\n🔒 Testing Invalid Signature (Security Check)")
    print("=" * 50)
    
    channel_secret = os.getenv('LINE_CHANNEL_SECRET')
    if not channel_secret:
        print("❌ Missing channel secret")
        return False
    
    test_message = {
        "events": [
            {
                "type": "message",
                "message": {
                    "type": "text",
                    "text": "惡意測試"
                }
            }
        ]
    }
    
    body = json.dumps(test_message)
    
    # Use wrong signature
    wrong_signature = "wrong_signature_here"
    
    try:
        headers = {
            'Content-Type': 'application/json',
            'X-Line-Signature': wrong_signature
        }
        
        response = requests.post(
            "http://localhost:3000/webhook",
            data=body,
            headers=headers,
            timeout=10
        )
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 400:
            print("✅ Invalid signature correctly rejected!")
            return True
        else:
            print("❌ Invalid signature not rejected - security issue!")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Webhook service not running")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    """Run all signature verification tests"""
    
    print("🧪 LINE Bot Signature Verification Test Suite")
    print("=" * 60)
    
    # Test 1: Valid signature
    test1_result = test_signature_verification()
    
    # Test 2: Invalid signature
    test2_result = test_invalid_signature()
    
    print("\n📊 Test Results:")
    print("=" * 30)
    print(f"Valid Signature Test: {'✅ PASS' if test1_result else '❌ FAIL'}")
    print(f"Invalid Signature Test: {'✅ PASS' if test2_result else '❌ FAIL'}")
    
    if test1_result and test2_result:
        print("\n🎉 All signature verification tests passed!")
        print("Your LINE Bot webhook is properly secured.")
    else:
        print("\n⚠️ Some tests failed. Check your configuration.")
        
    return test1_result and test2_result

if __name__ == "__main__":
    main() 