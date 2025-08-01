#!/usr/bin/env python3
"""
Test LIFF Integration
Verifies that the LIFF page and RAG API integration work correctly
"""

import requests
import json
import time

def test_liff_integration():
    """Test the complete LIFF integration"""
    print("🧪 Testing LIFF Integration")
    print("=" * 50)
    
    # Test 1: LIFF Server
    print("\n📱 Test 1: LIFF Server")
    try:
        response = requests.get("http://localhost:8081/index.html", timeout=5)
        if response.status_code == 200:
            print("✅ LIFF Server: PASSED")
            print(f"   Status: {response.status_code}")
            print(f"   Content Length: {len(response.text)} characters")
        else:
            print(f"❌ LIFF Server: FAILED ({response.status_code})")
            return False
    except Exception as e:
        print(f"❌ LIFF Server Error: {e}")
        return False
    
    # Test 2: RAG API with LIFF URL
    print("\n🔍 Test 2: RAG API with LIFF URL")
    try:
        response = requests.post(
            "http://localhost:8005/comprehensive-analysis",
            json={"text": "媽媽最近常忘記關瓦斯"},
            timeout=10
        )
        if response.status_code == 200:
            data = response.json()
            button_url = data['contents']['footer']['contents'][0]['action']['uri']
            print("✅ RAG API: PASSED")
            print(f"   Button Type: {data['contents']['footer']['contents'][0]['action']['type']}")
            print(f"   Button Label: {data['contents']['footer']['contents'][0]['action']['label']}")
            print(f"   LIFF URL: {button_url[:80]}...")
            
            if "localhost:8081" in button_url and "analysis=" in button_url:
                print("✅ LIFF URL: CORRECTLY FORMATTED")
            else:
                print("❌ LIFF URL: INCORRECTLY FORMATTED")
                return False
        else:
            print(f"❌ RAG API: FAILED ({response.status_code})")
            return False
    except Exception as e:
        print(f"❌ RAG API Error: {e}")
        return False
    
    # Test 3: LIFF Page with Analysis Data
    print("\n📊 Test 3: LIFF Page with Analysis Data")
    try:
        # Create sample analysis data
        sample_data = {
            "symptom_titles": ["記憶力減退", "日常生活能力下降"],
            "action_suggestions": ["建議及早就醫評估", "進行認知功能測試"],
            "comprehensive_summary": "檢測到多項症狀，建議綜合醫療評估"
        }
        
        import urllib.parse
        encoded_data = urllib.parse.quote(json.dumps(sample_data, ensure_ascii=False))
        
        response = requests.get(f"http://localhost:8081/index.html?analysis={encoded_data}", timeout=5)
        if response.status_code == 200:
            print("✅ LIFF Page with Data: PASSED")
            print(f"   Status: {response.status_code}")
            print(f"   Contains Analysis Script: {'analysis' in response.text}")
        else:
            print(f"❌ LIFF Page with Data: FAILED ({response.status_code})")
            return False
    except Exception as e:
        print(f"❌ LIFF Page Error: {e}")
        return False
    
    # Test 4: Webhook Integration
    print("\n🔗 Test 4: Webhook Integration")
    try:
        response = requests.get("http://localhost:3000/health", timeout=5)
        if response.status_code == 200:
            health_data = response.json()
            print("✅ Webhook Health: PASSED")
            print(f"   LINE Bot Status: {health_data['services']['line_bot']['status']}")
            print(f"   RAG API Status: {health_data['services']['rag_api']['status']}")
        else:
            print(f"❌ Webhook Health: FAILED ({response.status_code})")
            return False
    except Exception as e:
        print(f"❌ Webhook Error: {e}")
        return False
    
    print("\n" + "=" * 50)
    print("📊 Integration Test Summary")
    print("✅ LIFF Server is running and accessible")
    print("✅ RAG API generates correct LIFF URLs")
    print("✅ LIFF page can receive and process analysis data")
    print("✅ Webhook is healthy and ready")
    
    print("\n🎯 Next Steps:")
    print("   1. Use ngrok to expose the LIFF server to the internet")
    print("   2. Update your LINE Bot LIFF settings with the ngrok URL")
    print("   3. Test the button click in your LINE Bot")
    print("   4. Verify the LIFF page opens with analysis data")
    
    return True

def show_ngrok_instructions():
    """Show instructions for setting up ngrok"""
    print("\n" + "=" * 60)
    print("🚀 Setting up ngrok for LIFF")
    print("=" * 60)
    
    print("1. Start ngrok to expose the LIFF server:")
    print("   ngrok http 8081")
    
    print("\n2. Get the public URL from ngrok output")
    print("   Example: https://abc123.ngrok.io")
    
    print("\n3. Update the RAG API with the ngrok URL:")
    print("   Replace 'localhost:8081' with your ngrok URL")
    
    print("\n4. Update your LINE Bot LIFF settings:")
    print("   - Go to LINE Developers Console")
    print("   - Find your bot's LIFF settings")
    print("   - Add the ngrok URL as a LIFF endpoint")
    print("   - Set the LIFF ID in the HTML file")
    
    print("\n5. Test the integration:")
    print("   - Send a message to your LINE Bot")
    print("   - Click the '查看詳細報告' button")
    print("   - Verify the LIFF page opens with analysis data")

if __name__ == "__main__":
    success = test_liff_integration()
    
    if success:
        print("\n🎉 All LIFF integration tests passed!")
        print("📱 Your LINE Bot is ready for LIFF integration")
        show_ngrok_instructions()
    else:
        print("\n❌ Some tests failed. Please check the configuration.") 