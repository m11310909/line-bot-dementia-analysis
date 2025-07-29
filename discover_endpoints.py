#!/usr/bin/env python3
import requests
import json

base_url = "http://localhost:8001"
test_data = {"user_input": "媽媽最近常重複問同樣的問題"}

# Common endpoint patterns for FastAPI apps
endpoints = [
    "/analyze",
    "/flex", 
    "/m1-flex",
    "/api/analyze",
    "/api/flex",
    "/api/m1-flex",
    "/api/v1/analyze",
    "/api/v1/flex", 
    "/api/v1/m1-flex",
    "/api/v1/dementia",
    "/api/v1/xai",
    "/v1/analyze",
    "/v1/flex",
    "/dementia/analyze",
    "/xai/analyze"
]

print("🔍 Discovering API Endpoints")
print("=" * 50)

working_endpoint = None

for endpoint in endpoints:
    url = base_url + endpoint
    try:
        print(f"\n🧪 Testing: {endpoint}")
        response = requests.post(url, json=test_data, timeout=5)
        
        if response.status_code == 200:
            print(f"✅ SUCCESS! {endpoint}")
            result = response.json()
            
            # Check response structure
            if isinstance(result, dict):
                if 'type' in result and result['type'] == 'flex':
                    print("🎯 FLEX MESSAGE FOUND!")
                    working_endpoint = endpoint
                    
                    # Save the response
                    with open('discovered_flex_response.json', 'w', encoding='utf-8') as f:
                        json.dump(result, f, indent=2, ensure_ascii=False)
                    print("💾 Saved to: discovered_flex_response.json")
                    break
                else:
                    print(f"📄 Response type: {type(result)}")
                    print(f"📝 Keys: {list(result.keys()) if isinstance(result, dict) else 'Not a dict'}")
            
        elif response.status_code == 404:
            print("❌ Not Found")
        elif response.status_code == 405:
            print("⚠️ Method Not Allowed (endpoint exists but wrong method)")
        else:
            print(f"❌ Status: {response.status_code}")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Connection error: {e}")

if working_endpoint:
    print(f"\n🎉 WORKING ENDPOINT FOUND: {working_endpoint}")
    print(f"🔧 Update your tester to use: {base_url}{working_endpoint}")
else:
    print("\n❌ No working flex endpoint found")
    print("💡 Try checking the Swagger UI in browser: http://localhost:8001/docs")
