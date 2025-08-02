#!/usr/bin/env python3
"""
Webhook URL Manager
Helps track and manage the current working webhook URL
"""

import requests
import json
import time
import subprocess

def get_current_ngrok_url():
    """Get current ngrok URL"""
    try:
        response = requests.get("http://localhost:4040/api/tunnels", timeout=5)
        if response.status_code == 200:
            tunnels = response.json()
            if tunnels.get("tunnels"):
                return tunnels["tunnels"][0]["public_url"]
    except:
        pass
    return None

def test_webhook_url(url):
    """Test if webhook URL is working"""
    try:
        health_url = url.replace('/webhook', '/health')
        response = requests.get(health_url, timeout=10)
        if response.status_code == 200:
            return True
    except:
        pass
    return False

def save_working_url(url):
    """Save working URL to file"""
    config = {
        "webhook_url": url,
        "timestamp": time.strftime('%Y-%m-%d %H:%M:%S'),
        "status": "working"
    }
    
    with open("working_webhook_url.json", "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Working URL saved: {url}")

def create_url_report(url):
    """Create URL report"""
    report = f"""# 🔗 Current Working Webhook URL

## ✅ Status: WORKING
**URL**: `{url}`

## 📋 IMMEDIATE ACTION REQUIRED

### Update LINE Developer Console:
1. Go to https://developers.line.biz/
2. Set webhook URL to: `{url}`
3. Enable webhook
4. Save changes

### Test the Bot:
Send: `爸爸不會用洗衣機`

## 🧪 Verification:
```bash
curl {url.replace('/webhook', '/health')}
```

## 🔧 If URL Changes:
Run: `python3 final_solution.py`

---
**Last Updated**: {time.strftime('%Y-%m-%d %H:%M:%S')}
"""
    
    with open("CURRENT_WEBHOOK_URL.md", "w", encoding="utf-8") as f:
        f.write(report)
    
    print("✅ URL report created: CURRENT_WEBHOOK_URL.md")

def main():
    print("🔗 Webhook URL Manager")
    print("=" * 40)
    
    # Get current ngrok URL
    ngrok_url = get_current_ngrok_url()
    if not ngrok_url:
        print("❌ No ngrok tunnel found")
        print("💡 Run: python3 final_solution.py")
        return
    
    webhook_url = f"{ngrok_url}/webhook"
    print(f"📍 Current ngrok URL: {ngrok_url}")
    print(f"📍 Webhook URL: {webhook_url}")
    
    # Test the URL
    print("🧪 Testing webhook URL...")
    if test_webhook_url(webhook_url):
        print("✅ Webhook URL is working!")
        save_working_url(webhook_url)
        create_url_report(webhook_url)
        
        print("\n" + "=" * 40)
        print("🎉 WEBHOOK URL READY!")
        print("=" * 40)
        print(f"📍 URL: {webhook_url}")
        print("📋 Update LINE Developer Console now!")
        print("=" * 40)
    else:
        print("❌ Webhook URL is not working")
        print("💡 Run: python3 final_solution.py")

if __name__ == "__main__":
    main() 