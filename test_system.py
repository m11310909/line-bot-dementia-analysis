#!/usr/bin/env python3
import httpx
import json
import asyncio

async def test_xai_analysis():
    """Test XAI analysis endpoint"""
    test_cases = [
        {"user_input": "媽媽最近常常忘記吃藥", "expected_module": "M1"},
        {"user_input": "失智症中期會有什麼症狀", "expected_module": "M2"},
        {"user_input": "爸爸晚上很躁動怎麼辦", "expected_module": "M3"},
        {"user_input": "需要申請什麼補助嗎", "expected_module": "M4"}
    ]
    
    async with httpx.AsyncClient() as client:
        for test in test_cases:
            try:
                response = await client.post(
                    "http://localhost:8005/api/v1/analyze",
                    json={"user_input": test["user_input"], "user_id": "test_user"}
                )
                result = response.json()
                
                print(f"✅ Input: {test['user_input']}")
                print(f"   Module: {result['module']} (Expected: {test['expected_module']})")
                print(f"   Confidence: {result['xai_analysis']['confidence']:.2%}")
                print()
                
            except Exception as e:
                print(f"❌ Test failed: {e}")

if __name__ == "__main__":
    print("🧪 Testing XAI Analysis System...")
    asyncio.run(test_xai_analysis())
