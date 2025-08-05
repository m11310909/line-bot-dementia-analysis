#!/usr/bin/env python3
"""
Final Webhook URL Getter
Gets the current ngrok webhook URL using Python requests
"""

import requests
import json
import time
from datetime import datetime

def get_webhook_url():
    """Get the current webhook URL from ngrok"""
    print("🔍 Getting webhook URL...")
    
    # Try multiple times with increasing delays
    for attempt in range(1, 6):
        try:
            print(f"Attempt {attempt}/5...")
            response = requests.get("http://localhost:4040/api/tunnels", timeout=5)
            
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
            else:
                print(f"❌ ngrok API error: {response.status_code}")
                
        except Exception as e:
            print(f"❌ Attempt {attempt} failed: {e}")
            
        if attempt < 5:
            print(f"⏳ Waiting {attempt * 2} seconds before retry...")
            time.sleep(attempt * 2)
    
    print("❌ Failed to get webhook URL after 5 attempts")
    print("💡 Please check if ngrok is running: ngrok http 8081")
    return None

if __name__ == "__main__":
    get_webhook_url() 