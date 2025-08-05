#!/usr/bin/env python3
"""
Test LINE Bot Response
Checks if the LINE Bot is responding to messages properly
"""

import requests
import json
import time
from datetime import datetime

def test_rag_api():
    """Test RAG API functionality"""
    print("🔍 Testing RAG API...")
    
    try:
        # Test health endpoint
        response = requests.get("http://localhost:8005/health", timeout=5)
        if response.status_code == 200:
            print("✅ RAG API Health: OK")
        else:
            print(f"❌ RAG API Health: Failed ({response.status_code})")
            return False
        
        # Test analysis endpoint
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
            result = response.json()
            print("✅ RAG API Analysis: OK")
            print(f"   Response: {result.get('status', 'unknown')}")
            return True
        else:
            print(f"❌ RAG API Analysis: Failed ({response.status_code})")
            return False
            
    except Exception as e:
        print(f"❌ RAG API Test Failed: {e}")
        return False

def test_webhook_server():
    """Test webhook server functionality"""
    print("🔍 Testing Webhook Server...")
    
    try:
        # Test health endpoint
        response = requests.get("http://localhost:8081/health", timeout=5)
        if response.status_code == 200:
            print("✅ Webhook Server Health: OK")
        else:
            print(f"❌ Webhook Server Health: Failed ({response.status_code})")
            return False
        
        # Test webhook endpoint with mock LINE message
        mock_line_message = {
            "events": [{
                "type": "message",
                "message": {
                    "type": "text",
                    "text": "爸爸不會用洗衣機"
                },
                "replyToken": "test_reply_token",
                "source": {
                    "userId": "test_user_id",
                    "type": "user"
                }
            }]
        }
        
        response = requests.post(
            "http://localhost:8081/webhook",
            json=mock_line_message,
            headers={
                "Content-Type": "application/json",
                "X-Line-Signature": "test_signature"
            },
            timeout=10
        )
        
        if response.status_code == 200:
            print("✅ Webhook Server: OK")
            return True
        else:
            print(f"❌ Webhook Server: Failed ({response.status_code})")
            return False
            
    except Exception as e:
        print(f"❌ Webhook Server Test Failed: {e}")
        return False

def test_ngrok_tunnel():
    """Test ngrok tunnel"""
    print("🔍 Testing ngrok tunnel...")
    
    try:
        response = requests.get("http://localhost:4040/api/tunnels", timeout=5)
        if response.status_code == 200:
            tunnels = response.json().get("tunnels", [])
            if tunnels:
                tunnel_url = tunnels[0].get("public_url")
                print(f"✅ ngrok tunnel: {tunnel_url}")
                return tunnel_url
            else:
                print("❌ No ngrok tunnels found")
                return None
        else:
            print(f"❌ ngrok API: Failed ({response.status_code})")
            return None
            
    except Exception as e:
        print(f"❌ ngrok Test Failed: {e}")
        return None

def test_complete_flow():
    """Test complete message flow"""
    print("🔍 Testing Complete Message Flow...")
    
    try:
        # Test with a real message
        test_message = "媽媽中度失智"
        
        # Step 1: Test RAG API
        rag_data = {
            "text": test_message,
            "user_context": {"user_level": "general"}
        }
        
        response = requests.post(
            "http://localhost:8005/analyze/M1",
            json=rag_data,
            timeout=10
        )
        
        if response.status_code != 200:
            print("❌ RAG API analysis failed")
            return False
        
        rag_result = response.json()
        print(f"✅ RAG Analysis: {rag_result.get('status', 'unknown')}")
        
        # Step 2: Test webhook processing
        mock_event = {
            "events": [{
                "type": "message",
                "message": {
                    "type": "text",
                    "text": test_message
                },
                "replyToken": "test_reply_token",
                "source": {
                    "userId": "test_user_id",
                    "type": "user"
                }
            }]
        }
        
        response = requests.post(
            "http://localhost:8081/webhook",
            json=mock_event,
            headers={
                "Content-Type": "application/json",
                "X-Line-Signature": "test_signature"
            },
            timeout=10
        )
        
        if response.status_code == 200:
            print("✅ Complete Flow: OK")
            return True
        else:
            print(f"❌ Complete Flow: Failed ({response.status_code})")
            return False
            
    except Exception as e:
        print(f"❌ Complete Flow Test Failed: {e}")
        return False

def main():
    """Main test function"""
    print("🧪 LINE BOT RESPONSE TEST")
    print("=" * 50)
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 50)
    
    # Run all tests
    tests = [
        ("RAG API", test_rag_api),
        ("Webhook Server", test_webhook_server),
        ("ngrok Tunnel", test_ngrok_tunnel),
        ("Complete Flow", test_complete_flow)
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        print(f"\n📋 {test_name} Test:")
        print("-" * 30)
        
        try:
            result = test_func()
            results[test_name] = result
            status = "✅ PASS" if result else "❌ FAIL"
            print(f"{status}")
        except Exception as e:
            results[test_name] = False
            print(f"❌ FAIL: {e}")
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 TEST SUMMARY")
    print("=" * 50)
    
    passed = sum(1 for result in results.values() if result)
    total = len(results)
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name}: {status}")
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! LINE Bot should be working.")
    else:
        print("⚠️  Some tests failed. Check the issues above.")
    
    return passed == total

if __name__ == "__main__":
    main() 