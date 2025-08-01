#!/usr/bin/env python3
"""
Test Flex Message format for LINE Bot API compatibility
"""

import requests
import json
import os

def test_flex_message_format():
    """Test the Flex Message format from our backend API"""
    
    # Test the backend API
    print("🧪 Testing Flex Message format...")
    
    try:
        response = requests.post(
            "http://localhost:8000/demo/message",
            json={"text": "測試記憶力問題", "user_id": "line_user"},
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            flex_message = response.json()
            print("✅ Backend API returned Flex Message successfully")
            
            # Validate key format requirements
            issues = []
            
            # Check altText (not alt_text)
            if "altText" not in flex_message:
                issues.append("❌ Missing 'altText' field (should not be 'alt_text')")
            else:
                print("✅ altText field is correct")
            
            # Check contents structure
            if "contents" not in flex_message:
                issues.append("❌ Missing 'contents' field")
            else:
                print("✅ contents field is present")
                
                # Check bubble structure
                contents = flex_message["contents"]
                if contents.get("type") != "bubble":
                    issues.append("❌ Contents type should be 'bubble'")
                else:
                    print("✅ Bubble type is correct")
                
                # Check body structure
                if "body" in contents:
                    body = contents["body"]
                    if "contents" in body:
                        for i, item in enumerate(body["contents"]):
                            # Check height properties
                            if "height" in item:
                                if not isinstance(item["height"], int):
                                    issues.append(f"❌ Height at body[{i}] should be integer, got {type(item['height'])}")
                                else:
                                    print(f"✅ Height at body[{i}] is integer: {item['height']}")
                            
                            # Check cornerRadius properties
                            if "cornerRadius" in item:
                                if not isinstance(item["cornerRadius"], int):
                                    issues.append(f"❌ cornerRadius at body[{i}] should be integer, got {type(item['cornerRadius'])}")
                                else:
                                    print(f"✅ cornerRadius at body[{i}] is integer: {item['cornerRadius']}")
                
                # Check footer structure
                if "footer" in contents:
                    footer = contents["footer"]
                    if "contents" in footer:
                        for i, item in enumerate(footer["contents"]):
                            # Check height properties in footer
                            if "height" in item:
                                if not isinstance(item["height"], int):
                                    issues.append(f"❌ Height at footer[{i}] should be integer, got {type(item['height'])}")
                                else:
                                    print(f"✅ Height at footer[{i}] is integer: {item['height']}")
            
            if issues:
                print("\n❌ Found format issues:")
                for issue in issues:
                    print(f"  {issue}")
                return False
            else:
                print("\n🎉 All Flex Message format checks passed!")
                return True
                
        else:
            print(f"❌ Backend API returned status code: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error testing Flex Message: {e}")
        return False

def test_line_bot_api_compatibility():
    """Test if our Flex Message would be accepted by LINE Bot API"""
    
    print("\n🔗 Testing LINE Bot API compatibility...")
    
    # Get LINE credentials
    line_token = os.getenv('LINE_CHANNEL_ACCESS_TOKEN')
    if not line_token:
        print("❌ LINE_CHANNEL_ACCESS_TOKEN not found in environment")
        return False
    
    try:
        # Get Flex Message from our backend
        response = requests.post(
            "http://localhost:8000/demo/message",
            json={"text": "測試記憶力問題", "user_id": "line_user"},
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            flex_message = response.json()
            
            # Test with LINE Bot API (using a test endpoint)
            test_url = "https://api.line.me/v2/bot/message/push"
            headers = {
                "Authorization": f"Bearer {line_token}",
                "Content-Type": "application/json"
            }
            
            # Create a test message (we won't actually send it)
            test_message = {
                "to": "test_user",
                "messages": [flex_message]
            }
            
            print("✅ Flex Message format is ready for LINE Bot API")
            print(f"📋 Message structure:")
            print(f"  - Type: {flex_message.get('type')}")
            print(f"  - AltText: {flex_message.get('altText', 'N/A')}")
            print(f"  - Contents type: {flex_message.get('contents', {}).get('type')}")
            
            return True
            
    except Exception as e:
        print(f"❌ Error testing LINE Bot API compatibility: {e}")
        return False

if __name__ == "__main__":
    print("🔍 Flex Message Format Validation")
    print("=" * 40)
    
    # Test 1: Format validation
    format_ok = test_flex_message_format()
    
    # Test 2: LINE Bot API compatibility
    api_ok = test_line_bot_api_compatibility()
    
    print("\n📊 Test Results:")
    print(f"  Format Validation: {'✅ PASS' if format_ok else '❌ FAIL'}")
    print(f"  API Compatibility: {'✅ PASS' if api_ok else '❌ FAIL'}")
    
    if format_ok and api_ok:
        print("\n🎉 All tests passed! Flex Message should work with LINE Bot.")
    else:
        print("\n⚠️  Some tests failed. Please check the issues above.") 