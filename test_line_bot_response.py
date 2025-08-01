#!/usr/bin/env python3
"""
Test LINE Bot Flex Message Response
"""

import requests
import json
import os
import time

def test_backend_flex_message():
    """Test if backend generates valid Flex Message"""
    print("🧪 Testing Backend Flex Message Generation...")
    
    try:
        response = requests.post(
            "http://localhost:8000/demo/message",
            json={"text": "媽媽最近常忘記關瓦斯", "user_id": "line_user"},
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            flex_message = response.json()
            print("✅ Backend API returned valid Flex Message")
            
            # Check critical properties
            required_fields = ["type", "altText", "contents"]
            for field in required_fields:
                if field not in flex_message:
                    print(f"❌ Missing required field: {field}")
                    return False
            
            print(f"✅ Flex Message type: {flex_message['type']}")
            print(f"✅ AltText: {flex_message['altText']}")
            print(f"✅ Contents type: {flex_message['contents']['type']}")
            
            return True
        else:
            print(f"❌ Backend API error: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Backend test error: {e}")
        return False

def test_webhook_health():
    """Test webhook health endpoint"""
    print("\n🏥 Testing Webhook Health...")
    
    try:
        response = requests.get("http://localhost:3000/health")
        
        if response.status_code == 200:
            health_data = response.json()
            print("✅ Webhook health check passed")
            print(f"   Status: {health_data.get('status', 'unknown')}")
            print(f"   LINE Bot: {health_data.get('services', {}).get('line_bot', 'unknown')}")
            print(f"   RAG API: {health_data.get('services', {}).get('rag_api', 'unknown')}")
            return True
        else:
            print(f"❌ Webhook health check failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Webhook health test error: {e}")
        return False

def test_ngrok_tunnel():
    """Test ngrok tunnel accessibility"""
    print("\n📡 Testing Ngrok Tunnel...")
    
    try:
        # Read ngrok URL from file
        if os.path.exists("ngrok_url.txt"):
            with open("ngrok_url.txt", "r") as f:
                ngrok_url = f.read().strip()
            
            if ngrok_url:
                print(f"✅ Ngrok URL: {ngrok_url}")
                
                # Test tunnel accessibility
                response = requests.get(f"{ngrok_url}/health", timeout=10)
                if response.status_code == 200:
                    print("✅ Ngrok tunnel is accessible")
                    return True
                else:
                    print(f"❌ Ngrok tunnel test failed: {response.status_code}")
                    return False
            else:
                print("❌ Ngrok URL is empty")
                return False
        else:
            print("❌ ngrok_url.txt not found")
            return False
            
    except Exception as e:
        print(f"❌ Ngrok tunnel test error: {e}")
        return False

def test_line_bot_credentials():
    """Test if LINE Bot credentials are properly loaded"""
    print("\n🔑 Testing LINE Bot Credentials...")
    
    try:
        # Check environment variables
        token = os.getenv('LINE_CHANNEL_ACCESS_TOKEN')
        secret = os.getenv('LINE_CHANNEL_SECRET')
        
        if token and token != "YOUR_CHANNEL_ACCESS_TOKEN":
            print("✅ LINE_CHANNEL_ACCESS_TOKEN is set")
        else:
            print("❌ LINE_CHANNEL_ACCESS_TOKEN not properly set")
            return False
            
        if secret and secret != "YOUR_CHANNEL_SECRET":
            print("✅ LINE_CHANNEL_SECRET is set")
        else:
            print("❌ LINE_CHANNEL_SECRET not properly set")
            return False
            
        return True
        
    except Exception as e:
        print(f"❌ Credentials test error: {e}")
        return False

def test_complete_flow():
    """Test the complete flow from backend to webhook"""
    print("\n🔄 Testing Complete Flow...")
    
    try:
        # Step 1: Get Flex Message from backend
        backend_response = requests.post(
            "http://localhost:8000/demo/message",
            json={"text": "測試記憶力問題", "user_id": "line_user"},
            headers={"Content-Type": "application/json"}
        )
        
        if backend_response.status_code != 200:
            print("❌ Backend API failed")
            return False
            
        flex_message = backend_response.json()
        print("✅ Backend generated Flex Message")
        
        # Step 2: Test webhook can process the message
        webhook_response = requests.get("http://localhost:3000/health")
        
        if webhook_response.status_code == 200:
            print("✅ Webhook is healthy and ready")
            
            # Step 3: Check if webhook has proper environment variables
            health_data = webhook_response.json()
            line_bot_status = health_data.get('services', {}).get('line_bot', {})
            if isinstance(line_bot_status, dict) and line_bot_status.get('status') == 'ok':
                print("✅ LINE Bot credentials are loaded in webhook")
                return True
            else:
                print("❌ LINE Bot credentials not properly loaded in webhook")
                return False
        else:
            print("❌ Webhook health check failed")
            return False
            
    except Exception as e:
        print(f"❌ Complete flow test error: {e}")
        return False

def main():
    """Run all tests"""
    print("🔍 LINE Bot Complete System Test")
    print("=" * 50)
    
    tests = [
        ("Backend Flex Message", test_backend_flex_message),
        ("Webhook Health", test_webhook_health),
        ("Ngrok Tunnel", test_ngrok_tunnel),
        ("LINE Bot Credentials", test_line_bot_credentials),
        ("Complete Flow", test_complete_flow)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n📋 Running: {test_name}")
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ Test failed with exception: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 Test Results Summary:")
    print("=" * 50)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"  {test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\n🎯 Overall: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 ALL TESTS PASSED!")
        print("✅ Your LINE Bot should now be able to send Flex Messages!")
        print("\n📱 To test:")
        print("   1. Open LINE and find your bot")
        print("   2. Send any message (e.g., '媽媽最近常忘記關瓦斯')")
        print("   3. Bot should reply with a beautiful Flex Message")
    else:
        print(f"\n⚠️  {total - passed} test(s) failed")
        print("Please check the issues above and fix them")
    
    return passed == total

if __name__ == "__main__":
    main() 