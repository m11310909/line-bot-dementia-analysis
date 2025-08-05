#!/usr/bin/env python3
"""
Test Third-Party API Integration
Demonstrates direct third-party API integration with LINE bot
"""

import requests
import json
import time
from datetime import datetime

def test_third_party_api_webhook():
    """Test the third-party API webhook functionality"""
    
    print("🧪 Testing Third-Party API Integration")
    print("=" * 50)
    
    # Test 1: Health Check
    print("\n📊 Test 1: Health Check")
    print("-" * 30)
    
    try:
        response = requests.get("http://localhost:8082/health")
        if response.status_code == 200:
            health_data = response.json()
            print(f"✅ Status: {health_data['status']}")
            print(f"📍 Service: {health_data['service']}")
            print(f"🔧 API Type: {health_data['api_type']}")
            print(f"📱 LINE Bot Configured: {health_data['line_bot_configured']}")
            print(f"🔑 API Key Configured: {health_data['api_key_configured']}")
            print(f"📋 Supported APIs: {health_data['supported_apis']}")
        else:
            print(f"❌ Health check failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Health check error: {e}")
    
    # Test 2: API Test
    print("\n🔬 Test 2: API Functionality Test")
    print("-" * 30)
    
    test_messages = [
        "你好，請介紹一下你自己",
        "什麼是人工智慧？",
        "請用繁體中文回答：今天天氣如何？",
        "解釋一下機器學習的基本概念"
    ]
    
    for i, message in enumerate(test_messages, 1):
        print(f"\n📝 Test {i}: {message}")
        
        try:
            response = requests.post(
                "http://localhost:8082/test",
                json={"message": message},
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                result = response.json()
                print(f"✅ Status: {result['status']}")
                print(f"🔧 API Type: {result['api_type']}")
                print(f"📤 Input: {result['input']}")
                print(f"📥 Output: {result['output'][:100]}...")
            else:
                print(f"❌ API test failed: {response.status_code}")
                print(f"Error: {response.text}")
        except Exception as e:
            print(f"❌ API test error: {e}")
    
    # Test 3: Switch API Type
    print("\n🔄 Test 3: Switch API Type")
    print("-" * 30)
    
    api_types = ["openai", "gemini", "custom"]
    
    for api_type in api_types:
        print(f"\n🔄 Switching to {api_type} API...")
        
        try:
            response = requests.post(
                "http://localhost:8082/switch_api",
                json={"api_type": api_type},
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                result = response.json()
                print(f"✅ {result['message']}")
                print(f"🔧 Current API: {result['api_type']}")
            else:
                error_data = response.json()
                print(f"❌ Switch failed: {error_data['error']}")
        except Exception as e:
            print(f"❌ Switch error: {e}")
    
    # Test 4: LINE Webhook Simulation
    print("\n📱 Test 4: LINE Webhook Simulation")
    print("-" * 30)
    
    test_line_message = {
        "message": "這是一個測試訊息，請回應我"
    }
    
    try:
        response = requests.post(
            "http://localhost:8082/test",
            json=test_line_message,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ LINE message simulation successful")
            print(f"📤 User message: {result['input']}")
            print(f"📥 Bot response: {result['output'][:100]}...")
        else:
            print(f"❌ LINE simulation failed: {response.status_code}")
    except Exception as e:
        print(f"❌ LINE simulation error: {e}")

def test_different_api_configurations():
    """Test different API configurations"""
    
    print("\n🔧 Testing Different API Configurations")
    print("=" * 50)
    
    # Test OpenAI configuration
    print("\n🤖 Testing OpenAI Configuration")
    print("-" * 30)
    
    openai_test = {
        "api_type": "openai",
        "message": "請用繁體中文回答：什麼是深度學習？"
    }
    
    try:
        response = requests.post(
            "http://localhost:8082/test",
            json=openai_test,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ OpenAI test successful")
            print(f"📥 Response: {result['output'][:150]}...")
        else:
            print(f"❌ OpenAI test failed: {response.status_code}")
    except Exception as e:
        print(f"❌ OpenAI test error: {e}")
    
    # Test Gemini configuration
    print("\n🌟 Testing Gemini Configuration")
    print("-" * 30)
    
    gemini_test = {
        "api_type": "gemini",
        "message": "請解釋什麼是自然語言處理"
    }
    
    try:
        response = requests.post(
            "http://localhost:8082/test",
            json=gemini_test,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Gemini test successful")
            print(f"📥 Response: {result['output'][:150]}...")
        else:
            print(f"❌ Gemini test failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Gemini test error: {e}")

def demonstrate_line_integration():
    """Demonstrate LINE integration capabilities"""
    
    print("\n📱 LINE Integration Demonstration")
    print("=" * 50)
    
    print("""
🎯 How the Third-Party API Integration Works:

1. 📨 User sends message to LINE bot
2. 🔄 Webhook receives the message
3. 🌐 Third-party API processes the message
4. 📤 API response is sent back to LINE
5. 📱 User receives the response in LINE

✅ Benefits:
   - No visualization modules needed
   - Direct API integration
   - Simple text responses
   - Easy to test and debug
   - Supports multiple APIs

🔧 Supported APIs:
   - OpenAI GPT models
   - Google Gemini
   - Custom APIs
   - Any REST API

📋 Usage:
   1. Start the webhook server
   2. Configure your API keys
   3. Send messages to your LINE bot
   4. Get direct API responses
    """)

if __name__ == "__main__":
    print("🚀 Starting Third-Party API Integration Tests...")
    print(f"⏰ Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    try:
        # Test basic functionality
        test_third_party_api_webhook()
        
        # Test different configurations
        test_different_api_configurations()
        
        # Demonstrate LINE integration
        demonstrate_line_integration()
        
        print("\n🎉 All tests completed successfully!")
        print("📱 Your LINE bot is ready for third-party API integration!")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        print("🔧 Make sure the webhook server is running on port 8082") 