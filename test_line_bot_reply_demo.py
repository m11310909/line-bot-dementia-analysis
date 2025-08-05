#!/usr/bin/env python3
"""
LINE Bot Reply Demo Test
Demonstrates the bot's reply functionality with different message types
"""

import requests
import json
import time
from datetime import datetime

def test_line_bot_replies():
    """Test different types of LINE bot replies"""
    
    print("🧪 LINE Bot Reply Demo Test")
    print("=" * 50)
    
    # Test 1: Simple text message
    print("\n📱 Test 1: Simple Text Message")
    print("-" * 30)
    
    test_data = {
        "text": "你好，小幫手"
    }
    
    response = requests.post(
        "http://localhost:8081/test-webhook",
        json=test_data,
        headers={"Content-Type": "application/json"}
    )
    
    print(f"✅ Status: {response.status_code}")
    print(f"📤 Sent: {test_data['text']}")
    print(f"📥 Response: {response.json()}")
    
    # Test 2: Dementia analysis query
    print("\n🧠 Test 2: Dementia Analysis Query")
    print("-" * 30)
    
    test_data = {
        "text": "爸爸不會用洗衣機"
    }
    
    response = requests.post(
        "http://localhost:8081/test-webhook",
        json=test_data,
        headers={"Content-Type": "application/json"}
    )
    
    print(f"✅ Status: {response.status_code}")
    print(f"📤 Sent: {test_data['text']}")
    print(f"📥 Response: {response.json()}")
    
    # Test 3: Memory concern query
    print("\n💭 Test 3: Memory Concern Query")
    print("-" * 30)
    
    test_data = {
        "text": "媽媽常常忘記關瓦斯"
    }
    
    response = requests.post(
        "http://localhost:8081/test-webhook",
        json=test_data,
        headers={"Content-Type": "application/json"}
    )
    
    print(f"✅ Status: {response.status_code}")
    print(f"📤 Sent: {test_data['text']}")
    print(f"📥 Response: {response.json()}")
    
    # Test 4: Normal aging query
    print("\n👴 Test 4: Normal Aging Query")
    print("-" * 30)
    
    test_data = {
        "text": "爺爺偶爾忘記鑰匙放在哪裡"
    }
    
    response = requests.post(
        "http://localhost:8081/test-webhook",
        json=test_data,
        headers={"Content-Type": "application/json"}
    )
    
    print(f"✅ Status: {response.status_code}")
    print(f"📤 Sent: {test_data['text']}")
    print(f"📥 Response: {response.json()}")
    
    # Test 5: Complex symptom query
    print("\n🏥 Test 5: Complex Symptom Query")
    print("-" * 30)
    
    test_data = {
        "text": "奶奶最近常常重複問同樣的問題，而且情緒變化很大"
    }
    
    response = requests.post(
        "http://localhost:8081/test-webhook",
        json=test_data,
        headers={"Content-Type": "application/json"}
    )
    
    print(f"✅ Status: {response.status_code}")
    print(f"📤 Sent: {test_data['text']}")
    print(f"📥 Response: {response.json()}")
    
    print("\n🎯 Expected LINE Bot Replies:")
    print("=" * 50)
    print("📱 Text Message Reply:")
    print("   🧠 AI 分析結果:")
    print("   [Analysis text from RAG API]")
    print("   信心度: [Confidence level]")
    print()
    print("🎨 Flex Message Reply (if successful):")
    print("   📊 Detailed Analysis Report")
    print("   🎯 Confidence Level Bar")
    print("   ✅ Normal Aging Indicators")
    print("   ⚠️ Dementia Warning Signs")
    print("   🔗 Interactive Buttons")
    
    print("\n✅ Demo completed! Check your LINE app for the actual replies.")

def test_rag_api_direct():
    """Test RAG API directly to see the analysis results"""
    
    print("\n🔬 Direct RAG API Test")
    print("=" * 30)
    
    test_queries = [
        "爸爸不會用洗衣機",
        "媽媽常常忘記關瓦斯",
        "爺爺偶爾忘記鑰匙放在哪裡",
        "奶奶最近常常重複問同樣的問題"
    ]
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n📝 Test Query {i}: {query}")
        
        response = requests.post(
            "http://localhost:8005/analyze/M1",
            json={"text": query},
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Analysis: {data.get('result', {}).get('analysis', 'N/A')}")
            print(f"🎯 Signs: {data.get('result', {}).get('matched_signs', 'N/A')}")
            print(f"📊 Module: {data.get('module', 'N/A')}")
        else:
            print(f"❌ Error: {response.status_code}")

if __name__ == "__main__":
    print("🚀 Starting LINE Bot Reply Demo...")
    print(f"⏰ Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    try:
        # Test webhook functionality
        test_line_bot_replies()
        
        # Test RAG API directly
        test_rag_api_direct()
        
        print("\n🎉 All tests completed successfully!")
        print("📱 Check your LINE app for the actual bot replies!")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        print("🔧 Make sure the webhook server and RAG API are running") 