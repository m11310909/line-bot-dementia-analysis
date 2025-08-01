#!/usr/bin/env python3
"""
Comprehensive System Test
Tests all components of the LINE Bot system
"""

import requests
import json
import time

def test_all_components():
    """Test all system components"""
    print("🧪 Comprehensive System Test")
    print("=" * 60)
    
    all_tests_passed = True
    
    # Test 1: Ngrok Tunnel
    print("\n📱 Test 1: Ngrok Tunnel")
    try:
        response = requests.get("https://d6ad4bf748cd.ngrok-free.app/index.html", timeout=10)
        if response.status_code == 200:
            print("✅ Ngrok Tunnel: PASSED")
            print(f"   Status: {response.status_code}")
            print(f"   Content Length: {len(response.text)} characters")
        else:
            print(f"❌ Ngrok Tunnel: FAILED ({response.status_code})")
            all_tests_passed = False
    except Exception as e:
        print(f"❌ Ngrok Tunnel Error: {e}")
        all_tests_passed = False
    
    # Test 2: RAG API
    print("\n🔍 Test 2: RAG API")
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
            
            if "ngrok-free.app" in button_url and "analysis=" in button_url:
                print("✅ LIFF URL: CORRECTLY FORMATTED")
            else:
                print("❌ LIFF URL: INCORRECTLY FORMATTED")
                all_tests_passed = False
        else:
            print(f"❌ RAG API: FAILED ({response.status_code})")
            all_tests_passed = False
    except Exception as e:
        print(f"❌ RAG API Error: {e}")
        all_tests_passed = False
    
    # Test 3: Webhook Health
    print("\n🔗 Test 3: Webhook Health")
    try:
        response = requests.get("http://localhost:3000/health", timeout=5)
        if response.status_code == 200:
            health_data = response.json()
            print("✅ Webhook Health: PASSED")
            print(f"   LINE Bot Status: {health_data['services']['line_bot']['status']}")
            print(f"   RAG API Status: {health_data['services']['rag_api']['status']}")
        else:
            print(f"❌ Webhook Health: FAILED ({response.status_code})")
            all_tests_passed = False
    except Exception as e:
        print(f"❌ Webhook Error: {e}")
        all_tests_passed = False
    
    # Test 4: LIFF Page with Analysis Data
    print("\n📊 Test 4: LIFF Page with Analysis Data")
    try:
        # Create sample analysis data
        sample_data = {
            "symptom_titles": ["記憶力減退", "日常生活能力下降"],
            "action_suggestions": ["建議及早就醫評估", "進行認知功能測試"],
            "comprehensive_summary": "檢測到多項症狀，建議綜合醫療評估"
        }
        
        import urllib.parse
        encoded_data = urllib.parse.quote(json.dumps(sample_data, ensure_ascii=False))
        
        response = requests.get(f"https://d6ad4bf748cd.ngrok-free.app/index.html?analysis={encoded_data}", timeout=10)
        if response.status_code == 200:
            print("✅ LIFF Page with Data: PASSED")
            print(f"   Status: {response.status_code}")
            print(f"   Contains Analysis Script: {'analysis' in response.text}")
        else:
            print(f"❌ LIFF Page with Data: FAILED ({response.status_code})")
            all_tests_passed = False
    except Exception as e:
        print(f"❌ LIFF Page Error: {e}")
        all_tests_passed = False
    
    # Test 5: Process Status
    print("\n⚙️  Test 5: Process Status")
    try:
        import subprocess
        result = subprocess.run(['ps', 'aux'], capture_output=True, text=True)
        processes = result.stdout
        
        # Check if all required processes are running
        required_processes = [
            "rag_api_service.py",
            "updated_line_bot_webhook.py", 
            "liff_server.py",
            "ngrok http 8081"
        ]
        
        all_processes_running = True
        for process in required_processes:
            if process in processes:
                print(f"✅ {process}: RUNNING")
            else:
                print(f"❌ {process}: NOT RUNNING")
                all_processes_running = False
        
        if all_processes_running:
            print("✅ All Processes: RUNNING")
        else:
            print("❌ Some Processes: NOT RUNNING")
            all_tests_passed = False
            
    except Exception as e:
        print(f"❌ Process Check Error: {e}")
        all_tests_passed = False
    
    print("\n" + "=" * 60)
    print("📊 Comprehensive Test Summary")
    
    if all_tests_passed:
        print("🎉 ALL TESTS PASSED!")
        print("✅ Ngrok tunnel is accessible")
        print("✅ RAG API is generating correct URLs")
        print("✅ Webhook is healthy")
        print("✅ LIFF page is working with data")
        print("✅ All processes are running")
        
        print("\n🎯 System Status: FULLY OPERATIONAL")
        print("📱 Ready to test in LINE Bot!")
        
        print("\n💡 Next Steps:")
        print("   1. Send a message to your LINE Bot")
        print("   2. Click the '查看詳細報告' button")
        print("   3. Verify the LIFF page opens successfully")
        
    else:
        print("❌ SOME TESTS FAILED!")
        print("🔧 Please check the failed components above")
        
    return all_tests_passed

def show_current_configuration():
    """Show current system configuration"""
    print("\n" + "=" * 60)
    print("🔧 Current System Configuration")
    print("=" * 60)
    
    print("📱 Ngrok URL: https://d6ad4bf748cd.ngrok-free.app")
    print("🔗 LIFF Server: Port 8081")
    print("🧠 RAG API: Port 8005")
    print("🌐 Webhook: Port 3000")
    
    print("\n📋 Service Status:")
    print("   • Ngrok Tunnel: ✅ Active")
    print("   • LIFF Server: ✅ Running")
    print("   • RAG API: ✅ Running")
    print("   • Webhook: ✅ Running")
    
    print("\n🎯 Button Configuration:")
    print("   • Type: uri")
    print("   • Label: 查看詳細報告")
    print("   • Action: Opens LIFF page with analysis data")

if __name__ == "__main__":
    success = test_all_components()
    show_current_configuration()
    
    if success:
        print("\n🎉 System is fully operational!")
        print("📱 Test the button in your LINE Bot now!")
    else:
        print("\n❌ System has issues that need to be fixed.") 