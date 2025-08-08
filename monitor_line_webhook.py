#!/usr/bin/env python3
"""
LINE Webhook Activity Monitor
Real-time monitoring of webhook activity to verify LINE Developer Console configuration
"""

import subprocess
import time
import signal
import sys


def monitor_webhook_activity():
    """Monitor LINE Bot logs for webhook activity"""
    print("🔍 Monitoring LINE Bot Webhook Activity...")
    print("📋 What to look for:")
    print("   ✅ 'Webhook processed successfully' - Configuration working")
    print("   ❌ 'Invalid signature' - Check credentials")
    print("   📨 POST /webhook requests - LINE is sending events")
    print("\n" + "=" * 60)
    print("🚀 REAL-TIME LOG MONITORING (Press Ctrl+C to stop)")
    print("=" * 60)

    try:
        # Run docker-compose logs in real-time
        process = subprocess.Popen(
            ["docker-compose", "logs", "-f", "line-bot"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True,
            bufsize=1,
        )

        for line in iter(process.stdout.readline, ""):
            if line:
                # Highlight important log entries
                if "POST /webhook" in line:
                    print(f"📨 {line.strip()}")
                elif "Webhook processed successfully" in line:
                    print(f"✅ {line.strip()}")
                elif "Invalid signature" in line:
                    print(f"❌ {line.strip()}")
                elif "ERROR" in line:
                    print(f"🚨 {line.strip()}")
                elif "INFO" in line and ("health" not in line.lower()):
                    print(f"ℹ️  {line.strip()}")
                else:
                    print(line.strip())

    except KeyboardInterrupt:
        print("\n\n🛑 Monitoring stopped by user")
        process.terminate()
    except Exception as e:
        print(f"\n❌ Monitoring error: {e}")


def print_configuration_status():
    """Print current configuration status"""
    print("🔧 LINE DEVELOPER CONSOLE CONFIGURATION")
    print("=" * 60)

    print("\n📋 Required Configuration:")
    print("1. Webhook URL: https://6f59006e1132.ngrok-free.app/webhook")
    print("2. Enable webhook: ON ✅")
    print("3. Webhook events:")
    print("   • Message events ✅")
    print("   • Follow events ✅")
    print("   • Unfollow events ✅")
    print("   • Postback events ✅")

    print("\n🧪 Testing Steps:")
    print("1. Add your bot as friend in LINE")
    print("2. Send test message: '我最近常常忘記事情'")
    print("3. Watch logs below for successful processing")

    print("\n📊 Success Indicators:")
    print("✅ 'POST /webhook' requests appear")
    print("✅ 'Webhook processed successfully' messages")
    print("✅ No 'Invalid signature' errors")
    print("✅ Bot replies with analysis in LINE")


def signal_handler(sig, frame):
    """Handle Ctrl+C gracefully"""
    print("\n\n🛑 Monitoring stopped")
    sys.exit(0)


def main():
    """Main function"""
    signal.signal(signal.SIGINT, signal_handler)

    print("📱 LINE Webhook Configuration Monitor")
    print("=" * 60)

    print_configuration_status()

    print("\n" + "=" * 60)
    input(
        "Press Enter when you've configured LINE Developer Console to start monitoring..."
    )

    monitor_webhook_activity()


if __name__ == "__main__":
    main()
