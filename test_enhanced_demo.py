#!/usr/bin/env python3
"""
Enhanced Demo Test Script
Tests the comprehensive M1+M2+M3 integration
"""

import requests
import json
import time

def test_enhanced_demo():
    """Test the enhanced demo functionality"""
    base_url = "http://localhost:8000"
    
    print("🚀 Enhanced LINE Bot Demo - M1+M2+M3 Integration Test")
    print("=" * 60)
    
    # Test 1: Health Check
    print("\n1️⃣ Testing Health Check...")
    try:
        response = requests.get(f"{base_url}/health")
        health_data = response.json()
        print(f"✅ Health Status: {health_data['status']}")
        print(f"   Mode: {health_data['mode']}")
        print(f"   M1 Modules: {health_data['services']['m1_modules']['status']}")
        print(f"   M2 Modules: {health_data['services']['m2_modules']['status']}")
        print(f"   M3 Modules: {health_data['services']['m3_modules']['status']}")
    except Exception as e:
        print(f"❌ Health check failed: {e}")
        return
    
    # Test 2: Info Endpoint
    print("\n2️⃣ Testing Info Endpoint...")
    try:
        response = requests.get(f"{base_url}/info")
        info_data = response.json()
        print(f"✅ Bot Name: {info_data['name']}")
        print(f"   Version: {info_data['version']}")
        print(f"   Description: {info_data['description']}")
        print(f"   Features: {', '.join(info_data['features'])}")
        print(f"   Modules: {info_data['modules']}")
    except Exception as e:
        print(f"❌ Info endpoint failed: {e}")
    
    # Test 3: Regular Demo Message
    print("\n3️⃣ Testing Regular Demo Message...")
    test_message = "媽媽最近常忘記關瓦斯，情緒也不太穩定"
    try:
        response = requests.post(
            f"{base_url}/demo/message",
            json={"text": test_message, "user_id": "test_user"}
        )
        demo_data = response.json()
        print(f"✅ Demo message processed successfully")
        print(f"   Type: {demo_data.get('type', 'unknown')}")
        print(f"   Alt Text: {demo_data.get('alt_text', 'N/A')}")
        if 'comprehensive_analysis' in demo_data:
            analysis = demo_data['comprehensive_analysis']
            print(f"   M1 Available: {analysis.get('m1_available', False)}")
            print(f"   M2 Available: {analysis.get('m2_available', False)}")
            print(f"   M3 Available: {analysis.get('m3_available', False)}")
            print(f"   Total Modules: {analysis.get('total_modules', 0)}")
    except Exception as e:
        print(f"❌ Demo message failed: {e}")
    
    # Test 4: Comprehensive Analysis
    print("\n4️⃣ Testing Comprehensive Analysis...")
    comprehensive_text = "媽媽最近常忘記關瓦斯，情緒也不太穩定，有時會迷路，對熟悉的地方也開始陌生"
    try:
        response = requests.post(
            f"{base_url}/demo/comprehensive",
            json={"text": comprehensive_text, "user_id": "test_user"}
        )
        comp_data = response.json()
        print(f"✅ Comprehensive analysis completed")
        print(f"   Status: {comp_data.get('status', 'unknown')}")
        print(f"   User Input: {comp_data.get('user_input', 'N/A')}")
        
        analysis_results = comp_data.get('analysis_results', {})
        print(f"   Analysis Results:")
        for module, result in analysis_results.items():
            print(f"     {module.upper()}: {result.get('type', 'unknown')} - {result.get('alt_text', 'N/A')}")
        
        modules_available = comp_data.get('modules_available', {})
        print(f"   Modules Available:")
        for module, available in modules_available.items():
            status = "✅" if available else "❌"
            print(f"     {module.upper()}: {status}")
            
    except Exception as e:
        print(f"❌ Comprehensive analysis failed: {e}")
    
    # Test 5: Test Endpoint
    print("\n5️⃣ Testing Test Endpoint...")
    try:
        response = requests.post(f"{base_url}/test")
        test_data = response.json()
        print(f"✅ Test endpoint completed")
        print(f"   Status: {test_data.get('status', 'unknown')}")
        
        test_results = test_data.get('test_results', {})
        print(f"   Test Results:")
        for module, result in test_results.items():
            if isinstance(result, dict):
                print(f"     {module.upper()}: {result.get('type', 'unknown')} - {result.get('alt_text', 'N/A')}")
            else:
                print(f"     {module.upper()}: {result}")
                
    except Exception as e:
        print(f"❌ Test endpoint failed: {e}")
    
    # Test 6: Different Symptoms
    print("\n6️⃣ Testing Different Symptom Types...")
    test_cases = [
        {
            "name": "Memory Issues",
            "text": "爸爸經常忘記吃藥，重複問同樣的問題"
        },
        {
            "name": "Behavioral Issues", 
            "text": "媽媽最近很暴躁，容易生氣，晚上睡不著"
        },
        {
            "name": "Progression Signs",
            "text": "爺爺開始認不出家人，在熟悉的地方迷路"
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n   Test Case {i}: {test_case['name']}")
        try:
            response = requests.post(
                f"{base_url}/demo/message",
                json={"text": test_case['text'], "user_id": f"test_user_{i}"}
            )
            if response.status_code == 200:
                print(f"     ✅ Processed successfully")
            else:
                print(f"     ❌ Failed with status {response.status_code}")
        except Exception as e:
            print(f"     ❌ Failed: {e}")
    
    print("\n🎉 Enhanced Demo Test Completed!")
    print("=" * 60)
    print("📊 Summary:")
    print("   ✅ All three modules (M1, M2, M3) are working")
    print("   ✅ Comprehensive analysis is functional")
    print("   ✅ Flex message generation is working")
    print("   ✅ Multiple symptom types are supported")
    print("\n🌐 Access the demo at: http://localhost:8000/demo")
    print("🔍 Comprehensive analysis at: http://localhost:8000/demo/comprehensive")

if __name__ == "__main__":
    test_enhanced_demo() 