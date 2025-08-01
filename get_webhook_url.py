#!/usr/bin/env python3
"""
Quick script to get current webhook URL
"""

import requests
import json
import os

def get_current_webhook_url():
    """Get the current webhook URL"""
    print("🔍 Getting current webhook URL...")
    
    # Try to get from config file first
    if os.path.exists("webhook_config.json"):
        with open("webhook_config.json", "r") as f:
            config = json.load(f)
            url = config.get("webhook_url")
            if url:
                print(f"✅ Found saved webhook URL: {url}")
                return url
    
    # Try to get from ngrok API
    try:
        response = requests.get("http://localhost:4040/api/tunnels", timeout=5)
        if response.status_code == 200:
            tunnels = response.json()
            if tunnels.get("tunnels"):
                ngrok_url = tunnels["tunnels"][0]["public_url"]
                webhook_url = f"{ngrok_url}/webhook"
                print(f"✅ Current webhook URL: {webhook_url}")
                return webhook_url
    except:
        pass
    
    print("❌ No webhook URL found")
    print("💡 Run: python3 stable_webhook_solution.py")
    return None

def main():
    url = get_current_webhook_url()
    if url:
        print("\n" + "=" * 50)
        print("📋 COPY THIS URL TO LINE DEVELOPER CONSOLE:")
        print("=" * 50)
        print(url)
        print("=" * 50)
        print("1. Go to LINE Developer Console")
        print("2. Set webhook URL to the URL above")
        print("3. Enable webhook")
        print("4. Test with: 爸爸不會用洗衣機")

if __name__ == "__main__":
    main() 