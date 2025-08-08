#!/usr/bin/env python3
"""
LINE Webhook Verification Test
Tests if LINE Developer Console can successfully connect to your webhook
"""

import requests
import time


def test_webhook_connection():
    """Test if webhook is accessible from LINE"""
    print("🔍 Testing Webhook Connection for LINE Developer Console...")

    webhook_url = "https://6f59006e1132.ngrok-free.app/webhook"

    try:
        # Test basic connectivity
        response = requests.get(
            "https://6f59006e1132.ngrok-free.app/health", timeout=10
        )
        if response.status_code == 200:
            print("✅ Base URL accessible")
        else:
            print(f"❌ Base URL issue: {response.status_code}")
            return False

        # Test webhook endpoint responds to POST
        test_payload = {"events": [], "destination": "test"}

        response = requests.post(
            webhook_url,
            json=test_payload,
            headers={
                "Content-Type": "application/json",
                "X-Line-Signature": "test_signature",
            },
            timeout=10,
        )

        if response.status_code == 200:
            print("✅ Webhook endpoint responding correctly")
            print(f"   Response: {response.text}")
            return True
        else:
            print(f"❌ Webhook endpoint issue: {response.status_code}")
            return False

    except Exception as e:
        print(f"❌ Connection error: {e}")
        return False


def print_configuration_guide():
    """Print detailed configuration guide"""
    print("\n" + "=" * 60)
    print("🔧 LINE DEVELOPER CONSOLE CONFIGURATION GUIDE")
    print("=" * 60)

    print("\n📋 Step-by-Step Instructions:")

    print("\n1️⃣ ACCESS LINE DEVELOPER CONSOLE")
    print("   • Go to: https://developers.line.biz/")
    print("   • Sign in with your LINE account")
    print("   • Select your Messaging API channel")

    print("\n2️⃣ CONFIGURE WEBHOOK URL")
    print("   • Go to 'Messaging API' tab")
    print("   • Find 'Webhook settings' section")
    print("   • Set Webhook URL to:")
    print("     https://6f59006e1132.ngrok-free.app/webhook")
    print("   • Click 'Update'")
    print("   • Toggle 'Use webhook' to ON ✅")

    print("\n3️⃣ ENABLE WEBHOOK EVENTS")
    print("   • In 'Messaging API' tab")
    print("   • Find 'Webhook events' section")
    print("   • Enable these events:")
    print("     ✅ Message events")
    print("     ✅ Follow events")
    print("     ✅ Unfollow events")
    print("     ✅ Postback events")

    print("\n4️⃣ VERIFY CONFIGURATION")
    print("   • Click 'Verify' button next to webhook URL")
    print("   • Should show 'Success' message")
    print("   • If error, check URL and try again")

    print("\n5️⃣ TEST YOUR BOT")
    print("   • Add your bot as friend in LINE")
    print("   • Send test message: '我最近常常忘記事情'")
    print("   • Bot should reply with analysis")

    print("\n" + "=" * 60)
    print("🌐 YOUR WEBHOOK INFORMATION")
    print("=" * 60)
    print(f"Webhook URL: https://6f59006e1132.ngrok-free.app/webhook")
    print(f"Health Check: https://6f59006e1132.ngrok-free.app/health")
    print(f"Status: Ready for configuration ✅")


def main():
    """Main function"""
    print("🧪 LINE WEBHOOK CONFIGURATION VERIFICATION")
    print("=" * 50)

    # Test webhook connectivity
    webhook_ok = test_webhook_connection()

    if webhook_ok:
        print("\n✅ WEBHOOK READY FOR LINE DEVELOPER CONSOLE")
        print("Your webhook is accessible and ready to be configured.")
    else:
        print("\n❌ WEBHOOK CONNECTIVITY ISSUE")
        print("Please check your services before configuring LINE Developer Console.")

    # Print configuration guide
    print_configuration_guide()

    if webhook_ok:
        print("\n🎉 NEXT STEPS:")
        print("1. Follow the configuration guide above")
        print("2. Configure webhook in LINE Developer Console")
        print("3. Test your bot by sending messages")
        print("4. Monitor logs: docker-compose logs -f line-bot")


if __name__ == "__main__":
    main()
