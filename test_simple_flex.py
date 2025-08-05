#!/usr/bin/env python3
"""
Test Simple Flex Message
Send a simple Flex Message to test LINE API
"""

import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

def test_simple_flex():
    """Test sending a simple Flex Message"""
    print("🔍 Testing Simple Flex Message...")
    
    # Simple Flex Message
    simple_flex = {
        "type": "bubble",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "text",
                    "text": "測試訊息",
                    "weight": "bold",
                    "size": "lg"
                },
                {
                    "type": "text",
                    "text": "這是一個簡單的測試",
                    "size": "sm",
                    "color": "#666666",
                    "wrap": True
                }
            ]
        }
    }
    
    print("📊 Simple Flex Message structure:")
    print(json.dumps(simple_flex, indent=2, ensure_ascii=False))
    
    return simple_flex

def test_webhook_with_simple_flex():
    """Test webhook with simple Flex Message"""
    print("\n🔍 Testing Webhook with Simple Flex...")
    
    simple_flex = test_simple_flex()
    
    # Test data
    test_data = {
        "text": "測試",
        "user_id": "test_user",
        "flex_message": simple_flex
    }
    
    try:
        response = requests.post(
            "http://localhost:8081/test-webhook",
            json=test_data,
            timeout=10
        )
        
        print(f"📊 Response Status: {response.status_code}")
        print(f"📄 Response: {response.text}")
        
        return response.status_code == 200
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

def main():
    print("=" * 50)
    print("🔧 Simple Flex Message Test")
    print("=" * 50)
    
    success = test_webhook_with_simple_flex()
    
    print("\n" + "=" * 50)
    if success:
        print("✅ Simple Flex Message test passed")
        print("📋 Next: Test with real LINE message")
    else:
        print("❌ Simple Flex Message test failed")
    
    print("=" * 50)

if __name__ == "__main__":
    main() 