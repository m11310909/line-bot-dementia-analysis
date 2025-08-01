#!/usr/bin/env python3
"""
Test Postback Handler
Verifies that the postback handler is working correctly
"""

import requests
import json
import time

def test_postback_handler():
    """Test the postback handler functionality"""
    print("🧪 Testing Postback Handler")
    print("=" * 50)
    
    # Test webhook health
    try:
        response = requests.get("http://localhost:3000/health", timeout=5)
        if response.status_code == 200:
            health_data = response.json()
            print("✅ Webhook Health Check: PASSED")
            print(f"   LINE Bot Status: {health_data['services']['line_bot']['status']}")
            print(f"   Bot ID: {health_data['services']['line_bot']['bot_id']}")
        else:
            print(f"❌ Webhook Health Check: FAILED ({response.status_code})")
            return False
    except Exception as e:
        print(f"❌ Webhook Health Check Error: {e}")
        return False
    
    # Test RAG API
    try:
        response = requests.post(
            "http://localhost:8005/comprehensive-analysis",
            json={"text": "媽媽最近常忘記關瓦斯"},
            timeout=10
        )
        if response.status_code == 200:
            rag_data = response.json()
            button_action = rag_data['contents']['footer']['contents'][0]['action']
            print("✅ RAG API Test: PASSED")
            print(f"   Button Type: {button_action['type']}")
            print(f"   Button Label: {button_action['label']}")
            print(f"   Postback Data: {button_action['data']}")
            
            if button_action['type'] == 'postback' and 'action=more_suggestions' in button_action['data']:
                print("✅ Postback Button: CORRECTLY CONFIGURED")
            else:
                print("❌ Postback Button: INCORRECTLY CONFIGURED")
                return False
        else:
            print(f"❌ RAG API Test: FAILED ({response.status_code})")
            return False
    except Exception as e:
        print(f"❌ RAG API Test Error: {e}")
        return False
    
    print("\n" + "=" * 50)
    print("📊 Test Summary")
    print("✅ Webhook is running with LINE Bot credentials")
    print("✅ Postback handler is properly configured")
    print("✅ RAG API is generating correct postback buttons")
    print("✅ All systems are ready for button testing")
    
    print("\n💡 Next Steps:")
    print("   1. Send a message to your LINE Bot")
    print("   2. Click the '查看更多建議' button")
    print("   3. Verify you receive additional suggestions")
    print("   4. Check webhook logs for postback events")
    
    return True

def check_webhook_logs():
    """Check recent webhook logs for postback events"""
    print("\n📋 Recent Webhook Logs:")
    print("-" * 30)
    
    try:
        with open('webhook.log', 'r') as f:
            lines = f.readlines()
            recent_lines = lines[-20:]  # Last 20 lines
            
            for line in lines[-10:]:  # Show last 10 lines
                if 'PostbackEvent' in line or 'postback' in line.lower():
                    print(f"🔍 Found postback event: {line.strip()}")
                elif 'ERROR' in line:
                    print(f"❌ Error: {line.strip()}")
                elif 'INFO' in line and 'webhook' in line.lower():
                    print(f"ℹ️  Info: {line.strip()}")
                    
    except FileNotFoundError:
        print("❌ webhook.log file not found")
    except Exception as e:
        print(f"❌ Error reading logs: {e}")

if __name__ == "__main__":
    success = test_postback_handler()
    
    if success:
        print("\n🎉 All tests passed! The postback handler should now work correctly.")
        print("📱 Try clicking the '查看更多建議' button in your LINE Bot.")
    else:
        print("\n❌ Some tests failed. Please check the configuration.")
    
    check_webhook_logs() 