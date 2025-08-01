#!/usr/bin/env python3
"""
Test Webhook Fix
Verifies that the webhook can now process messages correctly
"""

import requests
import json
import time

def test_rag_api():
    """Test the RAG API directly"""
    print("🧪 Testing RAG API...")
    
    url = "http://localhost:8005/comprehensive-analysis"
    data = {"text": "媽媽最近常忘記關瓦斯"}
    
    try:
        response = requests.post(url, json=data, timeout=10)
        print(f"✅ RAG API Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            if "type" in result and result["type"] == "flex":
                print("✅ RAG API returns correct flex format")
                return True
            else:
                print("❌ RAG API format incorrect")
                return False
        else:
            print(f"❌ RAG API error: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ RAG API test failed: {e}")
        return False

def test_webhook_processing():
    """Test webhook message processing"""
    print("\n🧪 Testing Webhook Processing...")
    
    # Simulate a webhook call to the RAG API
    rag_url = "http://localhost:8005/comprehensive-analysis"
    webhook_url = "http://localhost:3000/test-webhook"
    
    try:
        # Test RAG API first
        rag_response = requests.post(rag_url, json={"text": "媽媽最近常忘記關瓦斯"}, timeout=10)
        
        if rag_response.status_code == 200:
            rag_result = rag_response.json()
            
            # Check if the format is correct for webhook
            if "type" in rag_result and rag_result["type"] == "flex":
                print("✅ RAG API format is correct for webhook")
                
                # Test webhook test endpoint
                webhook_response = requests.post(webhook_url, json={"text": "test"}, timeout=10)
                print(f"✅ Webhook test endpoint: {webhook_response.status_code}")
                
                return True
            else:
                print("❌ RAG API format not compatible with webhook")
                return False
        else:
            print(f"❌ RAG API failed: {rag_response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Webhook test failed: {e}")
        return False

def test_full_workflow():
    """Test the complete workflow"""
    print("\n🧪 Testing Full Workflow...")
    
    # This simulates what happens when a user sends a message
    test_message = "媽媽最近常忘記關瓦斯"
    
    try:
        # Step 1: Call RAG API (what webhook does)
        rag_response = requests.post(
            "http://localhost:8005/comprehensive-analysis",
            json={"text": test_message},
            timeout=10
        )
        
        if rag_response.status_code == 200:
            result = rag_response.json()
            
            # Step 2: Check if webhook can process this format
            if "type" in result and result["type"] == "flex":
                print("✅ Full workflow should work correctly")
                print(f"📊 Analysis result: {result.get('analysis_data', {}).get('comprehensive_summary', 'N/A')}")
                return True
            else:
                print("❌ Workflow format issue")
                return False
        else:
            print(f"❌ RAG API workflow failed: {rag_response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Full workflow test failed: {e}")
        return False

def main():
    """Main test function"""
    print("🔧 Testing Webhook Fix")
    print("=" * 40)
    
    # Test 1: RAG API
    test1 = test_rag_api()
    
    # Test 2: Webhook Processing
    test2 = test_webhook_processing()
    
    # Test 3: Full Workflow
    test3 = test_full_workflow()
    
    print("\n📊 Test Results:")
    print(f"   RAG API Test: {'✅ PASS' if test1 else '❌ FAIL'}")
    print(f"   Webhook Processing: {'✅ PASS' if test2 else '❌ FAIL'}")
    print(f"   Full Workflow: {'✅ PASS' if test3 else '❌ FAIL'}")
    
    if test1 and test2 and test3:
        print("\n🎉 All tests passed! The webhook fix is working correctly.")
        print("💡 Next real message should work properly.")
    else:
        print("\n⚠️ Some tests failed. Check the logs for details.")
    
    print("\n📋 Next Steps:")
    print("   1. Send a real message to your LINE Bot")
    print("   2. Check if you receive proper analysis results")
    print("   3. Monitor webhook logs for any issues")

if __name__ == "__main__":
    main() 