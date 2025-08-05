#!/usr/bin/env python3
"""
Test LINE Bot Connection
Simple test to verify the LINE Bot is working
"""

import requests
import json
from datetime import datetime

def test_line_bot_connection():
    """Test if the LINE Bot is responding"""
    print("🔍 Testing LINE Bot Connection...")
    
    # Test webhook endpoint
    webhook_url = "https://a3527fa7720b.ngrok-free.app/webhook"
    
    try:
        # Test if webhook is reachable
        response = requests.get(webhook_url.replace('/webhook', '/health'), timeout=5)
        if response.status_code == 200:
            print("✅ Webhook server is reachable")
        else:
            print(f"⚠️  Webhook server status: {response.status_code}")
    except Exception as e:
        print(f"❌ Webhook server not reachable: {e}")
    
    # Test RAG API
    try:
        test_data = {
            "text": "爸爸不會用洗衣機",
            "user_context": {"user_level": "general"}
        }
        response = requests.post(
            "http://localhost:8005/analyze/M1",
            json=test_data,
            timeout=10
        )
        if response.status_code == 200:
            data = response.json()
            if "flex_message" in data:
                print("✅ RAG API is generating Flex Messages")
                print("✅ LINE Bot should be working correctly")
                return True
            else:
                print("⚠️  RAG API response format unexpected")
                return False
        else:
            print(f"❌ RAG API error: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ RAG API test failed: {e}")
        return False

def main():
    print("=" * 50)
    print("🔧 LINE Bot Connection Test")
    print("=" * 50)
    
    success = test_line_bot_connection()
    
    print("\n" + "=" * 50)
    if success:
        print("🎉 LINE Bot is working correctly!")
        print("\n📋 Next Steps:")
        print("1. Go to LINE Developer Console")
        print("2. Set webhook URL to: https://a3527fa7720b.ngrok-free.app/webhook")
        print("3. Enable webhook")
        print("4. Test with message: '爸爸不會用洗衣機'")
        print("\n✅ Expected: Rich Flex Message with dementia analysis")
    else:
        print("❌ LINE Bot has issues")
        print("\n🔧 Troubleshooting:")
        print("1. Check if services are running")
        print("2. Run: python3 quick_diagnostic.py")
        print("3. Check logs for errors")
    
    print("=" * 50)

if __name__ == "__main__":
    main() 