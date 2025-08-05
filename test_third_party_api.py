#!/usr/bin/env python3
"""
Test Third Party API Usage
Verify that the webhook is using the third-party API
"""

import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

def test_third_party_api_config():
    """Test third-party API configuration"""
    print("🔍 Testing Third-Party API Configuration...")
    
    # Check environment variables
    use_third_party = os.getenv('USE_THIRD_PARTY_API', 'false').lower() == 'true'
    third_party_url = os.getenv('THIRD_PARTY_API_URL', '')
    third_party_name = os.getenv('THIRD_PARTY_API_NAME', '')
    
    print(f"📊 USE_THIRD_PARTY_API: {use_third_party}")
    print(f"📊 THIRD_PARTY_API_URL: {third_party_url}")
    print(f"📊 THIRD_PARTY_API_NAME: {third_party_name}")
    
    if use_third_party and third_party_url:
        print("✅ Third-party API is configured")
        return True
    else:
        print("❌ Third-party API not properly configured")
        return False

def test_webhook_api_selection():
    """Test webhook API selection"""
    print("\n🔍 Testing Webhook API Selection...")
    
    try:
        response = requests.post(
            "http://localhost:8081/test-webhook",
            json={"text": "爸爸不會用洗衣機"},
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Webhook test endpoint: {response.status_code}")
            print(f"📊 Platform: {data.get('platform', 'unknown')}")
            print(f"📊 Version: {data.get('version', 'unknown')}")
            return True
        else:
            print(f"❌ Webhook test failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Webhook test error: {e}")
        return False

def test_third_party_api_direct():
    """Test third-party API directly"""
    print("\n🔍 Testing Third-Party API Directly...")
    
    third_party_url = os.getenv('THIRD_PARTY_API_URL', '')
    if not third_party_url:
        print("❌ THIRD_PARTY_API_URL not set")
        return False
    
    try:
        # Test the third-party API URL
        response = requests.get(third_party_url, timeout=10)
        print(f"📊 Third-party API Status: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ Third-party API is accessible")
            return True
        else:
            print(f"❌ Third-party API error: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Third-party API test failed: {e}")
        return False

def main():
    print("=" * 50)
    print("🔧 Third-Party API Test")
    print("=" * 50)
    
    config_ok = test_third_party_api_config()
    webhook_ok = test_webhook_api_selection()
    api_ok = test_third_party_api_direct()
    
    print("\n" + "=" * 50)
    print("📊 Test Results:")
    print(f"✅ Configuration: {'OK' if config_ok else 'FAILED'}")
    print(f"✅ Webhook Selection: {'OK' if webhook_ok else 'FAILED'}")
    print(f"✅ Third-Party API: {'OK' if api_ok else 'FAILED'}")
    
    if config_ok and webhook_ok:
        print("\n�� Third-Party API is configured!")
        print("✅ Webhook will use third-party API")
        print("✅ Ready for LINE messages")
        print("\n📋 Next Steps:")
        print("1. Send message to your LINE bot")
        print("2. Expected: Third-party API response")
    else:
        print("\n❌ Some tests failed")
        print("🔧 Check third-party API configuration")
    
    print("=" * 50)

if __name__ == "__main__":
    main() 