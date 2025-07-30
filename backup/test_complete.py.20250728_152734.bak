import requests
import json
import time

# Replace with your actual Replit URL
BASE_URL = "https://workspace.replit.dev"

def test_health():
    print("🏥 Testing Health Check...")
    try:
        response = requests.get(f"{BASE_URL}/api/v1/health")
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_analyze():
    print("\n🔍 Testing Analysis Endpoint...")
    data = {
        "query": "記憶力減退",
        "module": "dementia",
        "max_chunks": 5
    }
    try:
        response = requests.post(f"{BASE_URL}/api/v1/analyze/dementia", json=data)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"Found {result['total_found']} chunks:")
            for chunk in result['chunks']:
                print(f"  - {chunk['title']} (confidence: {chunk['confidence_score']:.2f})")
        else:
            print(f"Error: {response.text}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_flex_message():
    print("\n🎨 Testing Flex Message Generation...")
    chunk_ids = ["D001"]
    try:
        response = requests.post(f"{BASE_URL}/api/v1/flex-message", json=chunk_ids)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print("Flex Message generated successfully!")
            print(f"Type: {result['flex_message']['type']}")
            print(f"Fallback: {result['fallback_text']}")
        else:
            print(f"Error: {response.text}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_different_queries():
    print("\n🧪 Testing Different Queries...")
    test_queries = [
        ("記憶力問題", "dementia"),
        ("長照服務", "ltc"),
        ("失智症症狀", "hybrid")
    ]
    
    for query, module in test_queries:
        print(f"\nTesting: '{query}' in {module} module")
        data = {"query": query, "module": module, "max_chunks": 3}
        try:
            response = requests.post(f"{BASE_URL}/api/v1/analyze/{module}", json=data)
            if response.status_code == 200:
                result = response.json()
                print(f"✅ Found {result['total_found']} results")
            else:
                print(f"❌ Failed: {response.status_code}")
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    print("🚀 Starting Complete API Test...")
    print(f"Testing URL: {BASE_URL}")
    
    # Run all tests
    health_ok = test_health()
    analyze_ok = test_analyze()
    flex_ok = test_flex_message()
    
    test_different_queries()
    
    print(f"\n📊 Test Results:")
    print(f"Health Check: {'✅' if health_ok else '❌'}")
    print(f"Analysis: {'✅' if analyze_ok else '❌'}")  
    print(f"Flex Message: {'✅' if flex_ok else '❌'}")
    
    if all([health_ok, analyze_ok, flex_ok]):
        print("\n🎉 All tests passed! API is working correctly.")
    else:
        print("\n⚠️  Some tests failed. Check the logs above.")
