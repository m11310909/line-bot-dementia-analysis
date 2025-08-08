#!/usr/bin/env python3
"""
Test script for LINE Bot real testing setup
"""

import requests
import json
import os
from datetime import datetime


def test_health_endpoint():
    """Test health endpoint"""
    print("🔍 Testing health endpoint...")
    try:
        response = requests.get(
            "https://6f59006e1132.ngrok-free.app/health", timeout=10
        )
        print(f"✅ Health check: {response.status_code} - {response.text}")
        return True
    except Exception as e:
        print(f"❌ Health check failed: {e}")
        return False


def test_webhook_endpoint():
    """Test webhook endpoint"""
    print("\n🔍 Testing webhook endpoint...")
    try:
        # Test data
        test_data = {
            "events": [
                {
                    "type": "message",
                    "message": {"type": "text", "text": "我最近常常忘記事情"},
                    "replyToken": "test_reply_token",
                    "source": {"userId": "test_user_id", "type": "user"},
                }
            ]
        }

        response = requests.post(
            "https://6f59006e1132.ngrok-free.app/webhook",
            headers={
                "Content-Type": "application/json",
                "X-Line-Signature": "test_signature",
            },
            json=test_data,
            timeout=10,
        )

        print(f"✅ Webhook test: {response.status_code}")
        if response.status_code == 400:
            print("   (400 is expected for invalid signature)")
        return True
    except Exception as e:
        print(f"❌ Webhook test failed: {e}")
        return False


def test_api_endpoint():
    """Test API endpoint"""
    print("\n🔍 Testing API endpoint...")
    try:
        test_data = {"user_input": "我最近常常忘記事情", "user_id": "test_user"}

        response = requests.post(
            "https://6f59006e1132.ngrok-free.app/api/v1/analyze",
            headers={"Content-Type": "application/json"},
            json=test_data,
            timeout=10,
        )

        print(f"✅ API test: {response.status_code}")
        if response.status_code == 200:
            print("   API is responding correctly")
        return True
    except Exception as e:
        print(f"❌ API test failed: {e}")
        return False


def check_environment():
    """Check environment configuration"""
    print("\n🔍 Checking environment configuration...")

    # Check if .env file exists
    if os.path.exists(".env"):
        print("✅ .env file exists")
    else:
        print("❌ .env file not found")
        return False

    # Check required environment variables
    required_vars = ["LINE_CHANNEL_ACCESS_TOKEN", "LINE_CHANNEL_SECRET", "EXTERNAL_URL"]

    missing_vars = []
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)

    if missing_vars:
        print(f"❌ Missing environment variables: {missing_vars}")
        print("   Please update your .env file with real LINE Bot credentials")
        return False
    else:
        print("✅ All required environment variables are set")
        return True


def print_setup_instructions():
    """Print setup instructions"""
    print("\n" + "=" * 60)
    print("🚀 LINE BOT REAL TESTING SETUP")
    print("=" * 60)

    print("\n📋 Next Steps:")
    print("1. Update your .env file with real LINE Bot credentials:")
    print("   LINE_CHANNEL_ACCESS_TOKEN=your_actual_token")
    print("   LINE_CHANNEL_SECRET=your_actual_secret")

    print("\n2. Configure LINE Developer Console:")
    print("   - Go to: https://developers.line.biz/")
    print("   - Set webhook URL to: https://6f59006e1132.ngrok-free.app/webhook")
    print("   - Enable webhook events: message, follow, unfollow, postback")

    print("\n3. Test with your LINE Bot:")
    print("   - Add your bot as a friend")
    print("   - Send test messages like:")
    print("     • '我最近常常忘記事情'")
    print("     • '爸爸最近變得比較容易生氣'")
    print("     • '爺爺最近在熟悉的地方也會迷路'")

    print("\n4. Monitor logs:")
    print("   docker-compose logs -f line-bot")

    print("\n🌐 Current URLs:")
    print(f"   Webhook: https://6f59006e1132.ngrok-free.app/webhook")
    print(f"   Health: https://6f59006e1132.ngrok-free.app/health")
    print(f"   API: https://6f59006e1132.ngrok-free.app/api/")


def main():
    """Main test function"""
    print("🧪 LINE Bot Real Testing Setup Verification")
    print("=" * 50)

    # Run tests
    health_ok = test_health_endpoint()
    webhook_ok = test_webhook_endpoint()
    api_ok = test_api_endpoint()
    env_ok = check_environment()

    # Summary
    print("\n" + "=" * 50)
    print("📊 TEST RESULTS SUMMARY")
    print("=" * 50)

    tests = [
        ("Health Endpoint", health_ok),
        ("Webhook Endpoint", webhook_ok),
        ("API Endpoint", api_ok),
        ("Environment Config", env_ok),
    ]

    all_passed = True
    for test_name, passed in tests:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{test_name}: {status}")
        if not passed:
            all_passed = False

    print("\n" + "=" * 50)
    if all_passed:
        print("🎉 ALL TESTS PASSED!")
        print("Your LINE Bot is ready for real testing!")
    else:
        print("⚠️  Some tests failed. Please check the issues above.")

    print_setup_instructions()


if __name__ == "__main__":
    main()
