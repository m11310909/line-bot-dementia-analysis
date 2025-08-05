#!/usr/bin/env python3
"""
Test Webhook RAG API Usage
Verifies that the webhook is using the RAG API correctly
"""

import requests
import json
import time

def test_webhook_rag():
    """Test if webhook is using RAG API"""
    print("🔍 Testing Webhook RAG API Usage...")
    
    # Test data
    test_data = {
        "text": "爸爸不會用洗衣機",
        "user_id": "test_user"
    }
    
    try:
        # Test webhook endpoint
        response = requests.post(
            "http://localhost:8081/test-webhook",
            json=test_data,
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Webhook test endpoint: {response.status_code}")
            print(f"📊 RAG API URL: {data.get('rag_api_url', 'N/A')}")
            
            # Check if it's using the correct RAG API endpoint
            if "analyze/M1" in data.get('rag_api_url', ''):
                print("✅ Webhook is configured to use RAG API")
                return True
            else:
                print("❌ Webhook is not using correct RAG API endpoint")
                return False
        else:
            print(f"❌ Webhook test failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Webhook test error: {e}")
        return False

def test_rag_api_direct():
    """Test RAG API directly"""
    print("\n🔍 Testing RAG API Directly...")
    
    try:
        response = requests.post(
            "http://localhost:8005/analyze/M1",
            json={"text": "爸爸不會用洗衣機", "user_context": {"user_level": "general"}},
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success') and 'flex_message' in data:
                print("✅ RAG API is working correctly")
                print(f"📊 Module: {data.get('module', 'N/A')}")
                print(f"📊 Flex Message: Generated")
                return True
            else:
                print("❌ RAG API response format unexpected")
                return False
        else:
            print(f"❌ RAG API error: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ RAG API test error: {e}")
        return False

def main():
    print("=" * 50)
    print("🔧 Webhook RAG API Test")
    print("=" * 50)
    
    webhook_ok = test_webhook_rag()
    rag_ok = test_rag_api_direct()
    
    print("\n" + "=" * 50)
    print("📊 Test Results:")
    print(f"✅ Webhook Configuration: {'OK' if webhook_ok else 'FAILED'}")
    print(f"✅ RAG API Direct: {'OK' if rag_ok else 'FAILED'}")
    
    if webhook_ok and rag_ok:
        print("\n🎉 All tests passed!")
        print("✅ Webhook is configured to use RAG API")
        print("✅ RAG API is working correctly")
        print("\n📋 Next Steps:")
        print("1. Update LINE Developer Console webhook URL")
        print("2. Test with message: '爸爸不會用洗衣機'")
        print("3. Expected: Rich Flex Message response")
    else:
        print("\n❌ Some tests failed")
        print("🔧 Check webhook configuration and RAG API")
    
    print("=" * 50)

if __name__ == "__main__":
    main() 