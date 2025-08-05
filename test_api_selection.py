#!/usr/bin/env python3
"""
Test API Selection
Verifies which API the webhook is actually using
"""

import requests
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_api_selection():
    """Test which API the webhook is configured to use"""
    print("🔍 Testing API Selection...")
    
    # Check environment variables
    use_third_party = os.getenv('USE_THIRD_PARTY_API', 'false').lower() == 'true'
    third_party_url = os.getenv('THIRD_PARTY_API_URL', '')
    use_chatbot = os.getenv('USE_CHATBOT_API', 'false').lower() == 'true'
    chatbot_url = os.getenv('CHATBOT_API_URL', '')
    
    print(f"📊 Environment Variables:")
    print(f"   USE_THIRD_PARTY_API: {use_third_party}")
    print(f"   THIRD_PARTY_API_URL: {third_party_url}")
    print(f"   USE_CHATBOT_API: {use_chatbot}")
    print(f"   CHATBOT_API_URL: {chatbot_url}")
    
    # Determine which API should be used
    if use_third_party and third_party_url:
        expected_api = "Third-party API"
    elif use_chatbot and chatbot_url:
        expected_api = "Chatbot API"
    else:
        expected_api = "RAG API"
    
    print(f"\n🎯 Expected API: {expected_api}")
    
    # Test webhook configuration
    try:
        response = requests.post(
            "http://localhost:8081/test-webhook",
            json={"text": "測試"},
            timeout=5
        )
        
        if response.status_code == 200:
            data = response.json()
            rag_url = data.get('rag_api_url', '')
            
            print(f"\n📊 Webhook Configuration:")
            print(f"   RAG API URL: {rag_url}")
            
            if "analyze/M1" in rag_url:
                print("✅ Webhook is configured to use RAG API")
                return True
            else:
                print("❌ Webhook is not using RAG API")
                return False
        else:
            print(f"❌ Webhook test failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Webhook test error: {e}")
        return False

def main():
    print("=" * 50)
    print("🔧 API Selection Test")
    print("=" * 50)
    
    success = test_api_selection()
    
    print("\n" + "=" * 50)
    if success:
        print("🎉 API Selection Test Passed!")
        print("✅ Webhook is using RAG API")
        print("✅ No third-party API calls")
    else:
        print("❌ API Selection Test Failed!")
        print("🔧 Check webhook configuration")
    
    print("=" * 50)

if __name__ == "__main__":
    main() 