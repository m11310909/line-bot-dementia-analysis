#!/usr/bin/env python3
"""
🧪 XAI System Test Script
Tests the complete XAI-enhanced LINE Bot system
"""

import requests
import json
import time
import sys
from typing import Dict, Any

# Configuration
XAI_WRAPPER_URL = "http://localhost:8009/analyze"
CHATBOT_API_URL = "http://localhost:8008/analyze"
LINE_BOT_URL = "http://localhost:8081/health"

# Test cases
TEST_CASES = [
    {
        "input": "爸爸不會用洗衣機",
        "expected_module": "M1",
        "description": "M1 Warning Signs Test"
    },
    {
        "input": "媽媽中度失智",
        "expected_module": "M2", 
        "description": "M2 Progression Test"
    },
    {
        "input": "爺爺有妄想症狀",
        "expected_module": "M3",
        "description": "M3 BPSD Symptoms Test"
    },
    {
        "input": "需要醫療協助",
        "expected_module": "M4",
        "description": "M4 Care Navigation Test"
    },
    {
        "input": "一般健康問題",
        "expected_module": "M1",  # Default fallback
        "description": "General Inquiry Test"
    }
]

def test_service_health(url: str, service_name: str) -> bool:
    """Test if a service is healthy"""
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            print(f"✅ {service_name} is healthy")
            return True
        else:
            print(f"❌ {service_name} returned status {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ {service_name} is not responding: {e}")
        return False

def test_xai_wrapper(test_case: Dict[str, Any]) -> bool:
    """Test XAI wrapper with a specific test case"""
    try:
        payload = {
            "user_input": test_case["input"],
            "user_id": "test_user"
        }
        
        response = requests.post(XAI_WRAPPER_URL, json=payload, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        
        # Check if response has expected structure
        if "xai_enhanced" not in data:
            print(f"❌ {test_case['description']}: Missing xai_enhanced data")
            return False
        
        xai_data = data["xai_enhanced"]
        detected_module = xai_data.get("module", "unknown")
        confidence = xai_data.get("confidence", 0.0)
        
        # Check module detection
        if detected_module == test_case["expected_module"]:
            print(f"✅ {test_case['description']}: Correctly detected {detected_module} (confidence: {confidence:.2f})")
            return True
        else:
            print(f"⚠️  {test_case['description']}: Expected {test_case['expected_module']}, got {detected_module} (confidence: {confidence:.2f})")
            return False
            
    except Exception as e:
        print(f"❌ {test_case['description']}: Error - {e}")
        return False

def test_visualization_data(test_case: Dict[str, Any]) -> bool:
    """Test if visualization data is properly generated"""
    try:
        payload = {
            "user_input": test_case["input"],
            "user_id": "test_user"
        }
        
        response = requests.post(XAI_WRAPPER_URL, json=payload, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        xai_data = data["xai_enhanced"]
        visualization = xai_data.get("visualization", {})
        
        # Check if visualization has required fields
        required_fields = ["type", "module", "title", "confidence_score"]
        missing_fields = [field for field in required_fields if field not in visualization]
        
        if missing_fields:
            print(f"❌ {test_case['description']}: Missing visualization fields: {missing_fields}")
            return False
        
        # Check module-specific fields
        module = xai_data.get("module", "unknown")
        if module == "M1":
            if "evidence_highlights" not in visualization:
                print(f"❌ {test_case['description']}: M1 missing evidence_highlights")
                return False
        elif module == "M2":
            if "stage_indicators" not in visualization:
                print(f"❌ {test_case['description']}: M2 missing stage_indicators")
                return False
        elif module == "M3":
            if "symptoms" not in visualization:
                print(f"❌ {test_case['description']}: M3 missing symptoms")
                return False
        elif module == "M4":
            if "care_needs" not in visualization:
                print(f"❌ {test_case['description']}: M4 missing care_needs")
                return False
        
        print(f"✅ {test_case['description']}: Visualization data is complete")
        return True
        
    except Exception as e:
        print(f"❌ {test_case['description']}: Visualization test error - {e}")
        return False

def test_chatbot_api() -> bool:
    """Test the chatbot API directly"""
    try:
        payload = {
            "message": "爸爸不會用洗衣機",
            "user_id": "test_user"
        }
        
        response = requests.post(CHATBOT_API_URL, json=payload, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        
        if "type" in data and data["type"] == "flex":
            print("✅ Chatbot API: Returns proper Flex Message")
            return True
        else:
            print("❌ Chatbot API: Does not return Flex Message")
            return False
            
    except Exception as e:
        print(f"❌ Chatbot API test error: {e}")
        return False

def main():
    """Run all tests"""
    print("🧪 XAI System Test Suite")
    print("=" * 50)
    
    # Test service health
    print("\n📊 Testing Service Health...")
    services_healthy = True
    services_healthy &= test_service_health(CHATBOT_API_URL, "Chatbot API")
    services_healthy &= test_service_health(XAI_WRAPPER_URL, "XAI Wrapper")
    services_healthy &= test_service_health(LINE_BOT_URL, "LINE Bot")
    
    if not services_healthy:
        print("\n❌ Some services are not healthy. Please start the system first.")
        print("   Run: ./start_xai_system.sh")
        sys.exit(1)
    
    # Test chatbot API
    print("\n🤖 Testing Chatbot API...")
    chatbot_ok = test_chatbot_api()
    
    # Test XAI wrapper
    print("\n🧠 Testing XAI Wrapper...")
    xai_tests_passed = 0
    visualization_tests_passed = 0
    
    for test_case in TEST_CASES:
        if test_xai_wrapper(test_case):
            xai_tests_passed += 1
        
        if test_visualization_data(test_case):
            visualization_tests_passed += 1
    
    # Summary
    print("\n" + "=" * 50)
    print("📋 Test Summary")
    print("=" * 50)
    print(f"✅ Services Health: {'All Healthy' if services_healthy else 'Some Issues'}")
    print(f"✅ Chatbot API: {'Working' if chatbot_ok else 'Issues'}")
    print(f"✅ XAI Module Detection: {xai_tests_passed}/{len(TEST_CASES)} tests passed")
    print(f"✅ Visualization Data: {visualization_tests_passed}/{len(TEST_CASES)} tests passed")
    
    total_tests = 3 + len(TEST_CASES) * 2  # health + chatbot + xai_tests + visualization_tests
    passed_tests = (3 if services_healthy else 0) + (1 if chatbot_ok else 0) + xai_tests_passed + visualization_tests_passed
    
    print(f"\n🎯 Overall: {passed_tests}/{total_tests} tests passed")
    
    if passed_tests == total_tests:
        print("\n🎉 All tests passed! XAI system is working correctly.")
        return True
    else:
        print("\n⚠️  Some tests failed. Please check the system configuration.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 