#!/usr/bin/env python3
"""
Test Gemini Flex LIFF Flow
Demonstrates the complete flow: LINE → Webhook → Third Party API (小幫手) → Gemini → Visualization (Flex Message + LIFF) → LINE
"""
import requests
import json
import time
from datetime import datetime

def test_gemini_flex_liff_webhook():
    """Test the complete Gemini Flex LIFF webhook flow"""
    print("🧪 Testing Gemini Flex LIFF Webhook Flow")
    print("=" * 60)
    
    # Test 1: Health Check
    print("\n📋 Test 1: Health Check")
    try:
        response = requests.get("http://localhost:8083/health")
        if response.status_code == 200:
            health_data = response.json()
            print(f"✅ Status: {health_data['status']}")
            print(f"🔧 Service: {health_data['service']}")
            print(f"🔑 Gemini API: {'✅ Configured' if health_data['gemini_configured'] else '❌ Not configured'}")
            print(f"📱 LINE Bot: {'✅ Configured' if health_data['line_bot_configured'] else '❌ Not configured'}")
            print(f"🌐 LIFF URL: {health_data['liff_url']}")
        else:
            print(f"❌ Health check failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Health check error: {str(e)}")
    
    # Test 2: Service Information
    print("\n📋 Test 2: Service Information")
    try:
        response = requests.get("http://localhost:8083/")
        if response.status_code == 200:
            info_data = response.json()
            print(f"✅ Service: {info_data['service']}")
            print(f"📦 Version: {info_data['version']}")
            print(f"📝 Description: {info_data['description']}")
            print("🎯 Features:")
            for feature in info_data['features']:
                print(f"   {feature}")
        else:
            print(f"❌ Service info failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Service info error: {str(e)}")
    
    # Test 3: API Functionality Test
    print("\n📋 Test 3: API Functionality Test")
    test_messages = [
        "爸爸最近忘記怎麼使用洗衣機",
        "媽媽常常找不到鑰匙",
        "爺爺開始忘記親人的名字"
    ]
    
    for i, message in enumerate(test_messages, 1):
        print(f"\n🔍 Test {i}: {message}")
        try:
            response = requests.post(
                "http://localhost:8083/test",
                json={"message": message},
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                result = response.json()
                if result['success']:
                    print(f"✅ API Test successful")
                    print(f"📤 Test Message: {result['test_message']}")
                    print(f"🤖 Gemini Response: {result['gemini_response']['success']}")
                    print(f"🌐 LIFF URL: {result['liff_url']}")
                    
                    # Show parsed analysis if available
                    if result['gemini_response']['success']:
                        analysis = result['gemini_response']['analysis']
                        print(f"📊 Analysis: {analysis.get('analysis', 'N/A')[:100]}...")
                else:
                    print(f"❌ API Test failed: {result.get('error', 'Unknown error')}")
            else:
                print(f"❌ API Test failed: {response.status_code}")
        except Exception as e:
            print(f"❌ API Test error: {str(e)}")
    
    # Test 4: Simulate LINE Webhook
    print("\n📋 Test 4: Simulate LINE Webhook")
    try:
        # Simulate a LINE webhook event
        webhook_data = {
            "events": [{
                "type": "message",
                "message": {
                    "type": "text",
                    "text": "爸爸不會用洗衣機"
                },
                "source": {
                    "userId": "test_user_123"
                },
                "replyToken": "test_reply_token"
            }]
        }
        
        response = requests.post(
            "http://localhost:8083/webhook",
            json=webhook_data,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"📤 Webhook Response: {response.status_code}")
        if response.status_code == 200:
            print("✅ Webhook simulation successful")
        else:
            print(f"❌ Webhook simulation failed: {response.text}")
            
    except Exception as e:
        print(f"❌ Webhook simulation error: {str(e)}")

def demonstrate_complete_flow():
    """Demonstrate the complete flow step by step"""
    print("\n🎯 Complete Flow Demonstration")
    print("=" * 60)
    
    flow_steps = [
        "1. 📱 LINE User sends message",
        "2. 🔗 Webhook receives message",
        "3. 🤖 Third Party API (小幫手) processes",
        "4. 🧠 Gemini AI analyzes",
        "5. 🎨 Flex Message created",
        "6. 📱 LIFF integration added",
        "7. 📤 Response sent to LINE"
    ]
    
    print("🔄 Flow Steps:")
    for step in flow_steps:
        print(f"   {step}")
    
    print("\n💡 Key Features:")
    features = [
        "🧠 Enhanced Gemini AI with 小幫手 prompt",
        "🎨 Rich Flex Message visualization",
        "📱 LIFF integration for detailed reports",
        "🔗 Complete LINE ecosystem integration",
        "⚡ Real-time processing and response"
    ]
    
    for feature in features:
        print(f"   {feature}")

def show_setup_instructions():
    """Show setup instructions"""
    print("\n🔧 Setup Instructions")
    print("=" * 60)
    
    print("1. 📋 Environment Variables (.env):")
    env_vars = [
        "LINE_CHANNEL_ACCESS_TOKEN=your_line_channel_access_token",
        "LINE_CHANNEL_SECRET=your_line_channel_secret", 
        "GOOGLE_GEMINI_API_KEY=your_google_gemini_api_key",
        "LIFF_URL=https://your-liff-app.com"
    ]
    
    for var in env_vars:
        print(f"   {var}")
    
    print("\n2. 🚀 Start the Webhook:")
    print("   python3 gemini_flex_liff_webhook.py")
    
    print("\n3. 🌐 Expose with ngrok:")
    print("   ngrok http 8083")
    
    print("\n4. 📱 Configure LINE Developer Console:")
    print("   Webhook URL: https://your-ngrok-url.ngrok.io/webhook")
    
    print("\n5. 🧪 Test the Integration:")
    print("   python3 test_gemini_flex_liff_flow.py")

if __name__ == "__main__":
    print("🚀 Gemini Flex LIFF Flow Test")
    print("=" * 60)
    print(f"⏰ Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    test_gemini_flex_liff_webhook()
    demonstrate_complete_flow()
    show_setup_instructions()
    
    print(f"\n✅ Test completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}") 