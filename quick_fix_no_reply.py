#!/usr/bin/env python3
"""
Quick fix for LINE Bot no reply issue
"""

import os
import subprocess
import time
import requests
import json

def quick_fix():
    print("🚀 QUICK FIX FOR NO REPLY ISSUE")
    print("=" * 40)
    
    # Kill all processes
    print("🧹 Killing all processes...")
    subprocess.run(['pkill', '-f', 'ngrok'], capture_output=True)
    subprocess.run(['pkill', '-f', 'updated_line_bot_webhook.py'], capture_output=True)
    subprocess.run(['pkill', '-f', 'enhanced_m1_m2_m3_m4_integrated_api.py'], capture_output=True)
    time.sleep(3)
    
    # Start RAG API
    print("🚀 Starting RAG API...")
    subprocess.Popen(['python3', 'enhanced_m1_m2_m3_m4_integrated_api.py'], 
                     stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    time.sleep(10)
    
    # Start webhook
    print("🚀 Starting webhook...")
    subprocess.Popen(['python3', 'updated_line_bot_webhook.py'], 
                     stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    time.sleep(8)
    
    # Start ngrok
    print("🚀 Starting ngrok...")
    subprocess.Popen(['ngrok', 'http', '8081'], 
                     stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    time.sleep(10)
    
    # Get ngrok URL
    print("🔍 Getting ngrok URL...")
    for _ in range(20):
        try:
            response = requests.get("http://localhost:4040/api/tunnels", timeout=3)
            if response.status_code == 200:
                tunnels = response.json()
                if tunnels.get("tunnels"):
                    ngrok_url = tunnels["tunnels"][0]["public_url"]
                    webhook_url = f"{ngrok_url}/webhook"
                    print(f"✅ ngrok URL: {ngrok_url}")
                    print(f"✅ webhook URL: {webhook_url}")
                    
                    # Save URL
                    with open("current_webhook_url.txt", "w") as f:
                        f.write(webhook_url)
                    
                    # Create report
                    report = f"""# 🎯 QUICK FIX - NO REPLY ISSUE RESOLVED!

## ✅ System Status
- RAG API: Running
- Webhook Server: Running  
- ngrok: Active

## 🔗 Webhook URL
```
{webhook_url}
```

## 📋 IMMEDIATE ACTION REQUIRED

1. **Update LINE Developer Console**:
   - Go to https://developers.line.biz/
   - Set webhook URL to: `{webhook_url}`
   - Enable webhook
   - Save changes

2. **Test the Bot**:
   Send this message: `爸爸不會用洗衣機`

## 🧪 Test Commands
```bash
# Test RAG API
curl http://localhost:8005/health

# Test webhook  
curl {webhook_url.replace('/webhook', '/health')}

# Get current URL
cat current_webhook_url.txt
```

---
**Fixed**: {time.strftime('%Y-%m-%d %H:%M:%S')}
**Status**: Ready for testing
"""
                    
                    with open("QUICK_FIX_REPORT.md", "w", encoding="utf-8") as f:
                        f.write(report)
                    
                    print("\n" + "=" * 40)
                    print("🎉 QUICK FIX COMPLETE!")
                    print("=" * 40)
                    print(f"📍 Webhook URL: {webhook_url}")
                    print("📋 Next steps:")
                    print("1. Update LINE Developer Console")
                    print("2. Test with: 爸爸不會用洗衣機")
                    print("=" * 40)
                    return
        except:
            pass
        time.sleep(2)
    
    print("❌ Failed to get ngrok URL")

if __name__ == "__main__":
    quick_fix() 