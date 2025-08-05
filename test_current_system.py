#!/usr/bin/env python3
"""
Current System Test - Tests the running API on port 8005
"""

import requests
import json
import time

def test_current_api():
    """Test the currently running API on port 8005"""
    print("🧪 Testing Current System (Port 8005)")
    print("="*50)
    
    # Test health endpoint
    print("1. Testing Health Endpoint...")
    try:
        response = requests.get("http://localhost:8005/health", timeout=5)
        if response.status_code == 200:
            health_data = response.json()
            print(f"✅ Health Check: {health_data.get('status', 'unknown')}")
            print(f"   Mode: {health_data.get('mode', 'unknown')}")
            print(f"   Modules: {len(health_data.get('modules', {}))} active")
        else:
            print(f"❌ Health Check: HTTP {response.status_code}")
    except Exception as e:
        print(f"❌ Health Check: {e}")
        return
    
    # Test each module
    test_cases = [
        {
            "module": "M1",
            "input": "爸爸忘記關瓦斯爐",
            "description": "M1 警訊測試"
        },
        {
            "module": "M2", 
            "input": "媽媽中度失智",
            "description": "M2 病程測試"
        },
        {
            "module": "M3",
            "input": "爺爺有妄想症狀", 
            "description": "M3 BPSD 測試"
        },
        {
            "module": "M4",
            "input": "需要醫療協助",
            "description": "M4 照護測試"
        }
    ]
    
    print("\n2. Testing Module Analysis...")
    results = []
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n📋 Test {i}: {test_case['description']}")
        print(f"   Input: {test_case['input']}")
        print(f"   Module: {test_case['module']}")
        
        try:
            start_time = time.time()
            response = requests.post(
                f"http://localhost:8005/analyze/{test_case['module']}",
                json={"text": test_case["input"]},
                timeout=10
            )
            response_time = time.time() - start_time
            
            if response.status_code == 200:
                data = response.json()
                success = data.get("success", False)
                module = data.get("module", "unknown")
                
                status = "✅" if success else "❌"
                print(f"   {status} Response ({response_time:.2f}s)")
                print(f"   Success: {success}")
                print(f"   Module: {module}")
                
                # Check if flex message was generated
                flex_msg = data.get("flex_message", {})
                if flex_msg:
                    print(f"   Flex Message: {len(json.dumps(flex_msg))} bytes")
                
                results.append({
                    "test": test_case["description"],
                    "success": success,
                    "module": module,
                    "response_time": response_time,
                    "has_flex": bool(flex_msg)
                })
            else:
                print(f"   ❌ HTTP {response.status_code}")
                results.append({
                    "test": test_case["description"],
                    "success": False,
                    "error": f"HTTP {response.status_code}"
                })
                
        except Exception as e:
            print(f"   ❌ Error: {e}")
            results.append({
                "test": test_case["description"],
                "success": False,
                "error": str(e)
            })
    
    # Summary
    print("\n" + "="*50)
    print("📊 Test Summary")
    print("="*50)
    
    successful_tests = sum(1 for r in results if r.get("success", False))
    total_tests = len(results)
    
    print(f"✅ Successful: {successful_tests}/{total_tests}")
    
    for result in results:
        status = "✅" if result.get("success", False) else "❌"
        print(f"   {status} {result['test']}")
        if result.get("has_flex"):
            print(f"      📱 Flex message generated")
    
    # Save results
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    filename = f"current_system_test_{timestamp}.json"
    
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 Results saved to: {filename}")
    print("\n🎉 Test Complete!")

if __name__ == "__main__":
    test_current_api() 