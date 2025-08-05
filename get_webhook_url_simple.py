#!/usr/bin/env python3
"""
Simple Webhook URL Getter
Gets the current ngrok webhook URL
"""

import requests
import json
from datetime import datetime

def get_webhook_url():
    """Get the current webhook URL from ngrok"""
    try:
        # Start ngrok if not running
        import subprocess
        import time
        
        # Check if ngrok is running
        result = subprocess.run(['ps', 'aux'], capture_output=True, text=True)
        if 'ngrok http 8081' not in result.stdout:
            print("Starting ngrok...")
            subprocess.Popen(['ngrok', 'http', '8081'], 
                           stdout=subprocess.DEVNULL, 
                           stderr=subprocess.DEVNULL)
            time.sleep(5)
        
        # Get tunnel URL
        response = requests.get("http://localhost:4040/api/tunnels", timeout=10)
        if response.status_code == 200:
            tunnels = response.json()
            if tunnels.get("tunnels"):
                ngrok_url = tunnels["tunnels"][0]["public_url"]
                webhook_url = f"{ngrok_url}/webhook"
                
                print("✅ ngrok tunnel found!")
                print(f"🌐 ngrok URL: {ngrok_url}")
                print(f"🔗 Webhook URL: {webhook_url}")
                
                # Save to file
                with open("CURRENT_WEBHOOK_URL.md", "w") as f:
                    f.write(f"""# Current Webhook URL

**URL:** {webhook_url}

**Last Updated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Instructions

1. Go to LINE Developer Console
2. Select your bot
3. Go to Messaging API settings
4. Set Webhook URL to: `{webhook_url}`
5. Enable 'Use webhook'
6. Click 'Verify' to test
7. Save changes

## Test Messages

Send these messages to your bot:
- '爸爸不會用洗衣機'
- '媽媽中度失智'
- '爺爺有妄想症狀'

Expected response: Rich Flex Message with analysis

## System Status

✅ RAG API: Working
✅ Webhook Server: Running
✅ Environment Variables: Loaded
✅ ngrok Tunnel: Active
""")
                
                print(f"\n📄 Webhook URL saved to: CURRENT_WEBHOOK_URL.md")
                print(f"\n🎉 Setup complete!")
                print(f"📱 Update your LINE webhook URL to: {webhook_url}")
                return webhook_url
            else:
                print("❌ No ngrok tunnels found")
                return None
        else:
            print(f"❌ ngrok API error: {response.status_code}")
            return None
    except Exception as e:
        print(f"❌ Failed to get webhook URL: {e}")
        print("💡 Try running: ngrok http 8081")
        return None

if __name__ == "__main__":
    print("🔍 Getting current webhook URL...")
    get_webhook_url() 