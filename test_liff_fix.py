#!/usr/bin/env python3
"""
Test LIFF Fix
Verifies that the LIFF integration is now working with ngrok
"""

import requests
import json

def test_liff_fix():
    """Test the LIFF fix with ngrok URL"""
    print("🧪 Testing LIFF Fix with Ngrok")
    print("=" * 50)
    
    # Test 1: Ngrok URL accessibility
    print("\n📱 Test 1: Ngrok URL Accessibility")
    try:
        response = requests.get("https://56e350ec809b.ngrok-free.app/index.html", timeout=10)
        if response.status_code == 200:
            print("✅ Ngrok URL: PASSED")
            print(f"   Status: {response.status_code}")
            print(f"   Content Length: {len(response.text)} characters")
            print(f"   Contains LIFF Content: {'失智症警訊分析' in response.text}")
        else:
            print(f"❌ Ngrok URL: FAILED ({response.status_code})")
            return False
    except Exception as e:
        print(f"❌ Ngrok URL Error: {e}")
        return False
    
    # Test 2: RAG API with ngrok URL
    print("\n🔍 Test 2: RAG API with Ngrok URL")
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
            print(f"   Ngrok URL: {button_url[:80]}...")
            
            if "ngrok-free.app" in button_url and "analysis=" in button_url:
                print("✅ Ngrok URL: CORRECTLY FORMATTED")
            else:
                print("❌ Ngrok URL: INCORRECTLY FORMATTED")
                return False
        else:
            print(f"❌ RAG API: FAILED ({response.status_code})")
            return False
    except Exception as e:
        print(f"❌ RAG API Error: {e}")
        return False
    
    # Test 3: LIFF Page with Analysis Data via Ngrok
    print("\n📊 Test 3: LIFF Page with Analysis Data via Ngrok")
    try:
        # Create sample analysis data
        sample_data = {
            "symptom_titles": ["記憶力減退", "日常生活能力下降"],
            "action_suggestions": ["建議及早就醫評估", "進行認知功能測試"],
            "comprehensive_summary": "檢測到多項症狀，建議綜合醫療評估"
        }
        
        import urllib.parse
        encoded_data = urllib.parse.quote(json.dumps(sample_data, ensure_ascii=False))
        
        response = requests.get(f"https://56e350ec809b.ngrok-free.app/index.html?analysis={encoded_data}", timeout=10)
        if response.status_code == 200:
            print("✅ LIFF Page via Ngrok: PASSED")
            print(f"   Status: {response.status_code}")
            print(f"   Contains Analysis Script: {'analysis' in response.text}")
            print(f"   Contains LIFF Content: {'失智症警訊分析' in response.text}")
        else:
            print(f"❌ LIFF Page via Ngrok: FAILED ({response.status_code})")
            return False
    except Exception as e:
        print(f"❌ LIFF Page Error: {e}")
        return False
    
    # Test 4: Webhook Health
    print("\n🔗 Test 4: Webhook Health")
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
    print("📊 LIFF Fix Test Summary")
    print("✅ Ngrok URL is accessible from internet")
    print("✅ RAG API generates correct ngrok URLs")
    print("✅ LIFF page works with analysis data via ngrok")
    print("✅ Webhook is healthy and ready")
    
    print("\n🎯 The 'no response' issue should now be fixed!")
    print("📱 Try clicking the '查看詳細報告' button in your LINE Bot")
    print("🌐 The button should now open the LIFF page successfully")
    
    return True

if __name__ == "__main__":
    success = test_liff_fix()
    
    if success:
        print("\n🎉 All LIFF fix tests passed!")
        print("📱 Your LINE Bot button should now work correctly!")
        print("\n💡 Next Steps:")
        print("   1. Send a message to your LINE Bot")
        print("   2. Click the '查看詳細報告' button")
        print("   3. Verify the LIFF page opens successfully")
    else:
        print("\n❌ Some tests failed. Please check the configuration.") 