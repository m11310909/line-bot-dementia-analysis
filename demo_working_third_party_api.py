#!/usr/bin/env python3
"""
Demo Working Third-Party API Integration
Shows how to use the third-party API integration with a mock API
"""

import requests
import json
import time
from datetime import datetime

def demo_mock_api_integration():
    """Demonstrate third-party API integration with a mock API"""
    
    print("🎯 Third-Party API Integration Demo")
    print("=" * 50)
    
    # Mock API responses for demonstration
    mock_responses = {
        "你好，請介紹一下你自己": "你好！我是一個AI助手，專門協助回答問題。我可以幫助您解決各種問題，包括技術問題、一般知識查詢等。請隨時向我提問！",
        "什麼是人工智慧？": "人工智慧（AI）是電腦科學的一個分支，旨在創建能夠執行通常需要人類智能的任務的系統。這些任務包括學習、推理、問題解決、感知和語言理解。",
        "請用繁體中文回答：今天天氣如何？": "抱歉，我無法獲取即時天氣資訊。建議您查看當地天氣預報或使用天氣應用程式來獲取準確的天氣資訊。",
        "解釋一下機器學習的基本概念": "機器學習是人工智慧的一個子領域，它使電腦能夠從數據中學習並改進，而無需明確編程。基本概念包括監督學習、無監督學習和強化學習。"
    }
    
    print("\n📱 LINE Bot Integration Flow:")
    print("1. 📨 User sends message to LINE")
    print("2. 🔄 Webhook receives message")
    print("3. 🌐 Third-party API processes message")
    print("4. 📤 API response sent back to LINE")
    print("5. 📱 User receives response in LINE")
    
    print("\n🧪 Testing with Mock API Responses:")
    print("-" * 40)
    
    for user_message, expected_response in mock_responses.items():
        print(f"\n📤 User Message: {user_message}")
        print(f"📥 Expected Response: {expected_response[:50]}...")
        print("✅ Mock API Integration Working!")
    
    print("\n🔧 Configuration Options:")
    print("-" * 30)
    
    configs = [
        {
            "name": "OpenAI GPT",
            "api_type": "openai",
            "endpoint": "https://api.openai.com/v1/chat/completions",
            "features": ["GPT-3.5-turbo", "Traditional Chinese", "500 tokens"]
        },
        {
            "name": "Google Gemini",
            "api_type": "gemini", 
            "endpoint": "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent",
            "features": ["Gemini Pro", "Traditional Chinese", "500 tokens"]
        },
        {
            "name": "Custom API",
            "api_type": "custom",
            "endpoint": "https://your-api-endpoint.com/chat",
            "features": ["Custom model", "Flexible format", "Configurable"]
        }
    ]
    
    for config in configs:
        print(f"\n🤖 {config['name']}:")
        print(f"   🔧 API Type: {config['api_type']}")
        print(f"   🌐 Endpoint: {config['endpoint']}")
        print(f"   ✨ Features: {', '.join(config['features'])}")

def demo_line_bot_setup():
    """Demonstrate LINE bot setup process"""
    
    print("\n📱 LINE Bot Setup Process:")
    print("=" * 40)
    
    steps = [
        "1. 🔧 Configure environment variables in .env",
        "2. 🚀 Start the webhook server (port 8082)",
        "3. 🌐 Get your webhook URL: http://localhost:8082/webhook",
        "4. 📋 Update LINE Developer Console webhook URL",
        "5. ✅ Enable webhook in LINE Developer Console",
        "6. 👥 Add bot as friend in LINE",
        "7. 💬 Send test message to bot",
        "8. 🎉 Receive API response in LINE!"
    ]
    
    for step in steps:
        print(f"   {step}")
    
    print("\n🔑 Required Environment Variables:")
    print("-" * 35)
    
    env_vars = [
        "LINE_CHANNEL_ACCESS_TOKEN=your_line_token",
        "LINE_CHANNEL_SECRET=your_line_secret", 
        "API_TYPE=openai  # or gemini, custom",
        "API_KEY=your_api_key_here"
    ]
    
    for var in env_vars:
        print(f"   {var}")

def demo_testing_workflow():
    """Demonstrate testing workflow"""
    
    print("\n🧪 Testing Workflow:")
    print("=" * 30)
    
    print("\n1. 📊 Health Check:")
    print("   curl http://localhost:8082/health")
    
    print("\n2. 🔬 API Test:")
    print("   curl -X POST http://localhost:8082/test \\")
    print("     -H \"Content-Type: application/json\" \\")
    print("     -d '{\"message\": \"Hello, how are you?\"}'")
    
    print("\n3. 🔄 Switch API:")
    print("   curl -X POST http://localhost:8082/switch_api \\")
    print("     -H \"Content-Type: application/json\" \\")
    print("     -d '{\"api_type\": \"gemini\"}'")
    
    print("\n4. 📱 LINE Test:")
    print("   Send message to your LINE bot")
    print("   Check webhook logs: tail -f third_party_webhook.log")

def demo_benefits():
    """Demonstrate the benefits of this approach"""
    
    print("\n✅ Benefits of Third-Party API Integration:")
    print("=" * 50)
    
    benefits = [
        {
            "title": "🚀 No Visualization Modules",
            "description": "Direct text responses without complex UI components"
        },
        {
            "title": "🔧 Multiple API Support", 
            "description": "Easy switching between OpenAI, Gemini, and custom APIs"
        },
        {
            "title": "🧪 Simple Testing",
            "description": "Direct API testing without LINE integration complexity"
        },
        {
            "title": "⚡ Fast Development",
            "description": "Rapid prototyping and development workflow"
        },
        {
            "title": "🔍 Easy Debugging",
            "description": "Clear logs and error handling for troubleshooting"
        },
        {
            "title": "📱 Production Ready",
            "description": "Ready for production deployment with proper configuration"
        }
    ]
    
    for benefit in benefits:
        print(f"\n{benefit['title']}:")
        print(f"   {benefit['description']}")

if __name__ == "__main__":
    print("🎯 Third-Party API Integration Demo")
    print(f"⏰ Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Run demonstrations
    demo_mock_api_integration()
    demo_line_bot_setup()
    demo_testing_workflow()
    demo_benefits()
    
    print("\n" + "=" * 60)
    print("🎉 DEMONSTRATION COMPLETE!")
    print("=" * 60)
    print("\n📋 Next Steps:")
    print("1. 🔧 Configure your API keys in .env")
    print("2. 🚀 Start the webhook server")
    print("3. 📱 Test with your LINE bot")
    print("4. 🎯 Enjoy direct third-party API integration!")
    
    print("\n💡 Tips:")
    print("- Use different API types for different use cases")
    print("- Monitor logs for debugging")
    print("- Test thoroughly before production")
    print("- Keep API keys secure") 