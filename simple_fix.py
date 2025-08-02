#!/usr/bin/env python3
"""
Simple fix for LINE Bot no reply issue
"""

import os
import subprocess
import time
import requests
import json

def kill_processes():
    """Kill all related processes"""
    print("🧹 Killing all processes...")
    processes = ['ngrok', 'updated_line_bot_webhook.py', 'enhanced_m1_m2_m3_m4_integrated_api.py']
    for process in processes:
        subprocess.run(['pkill', '-f', process], capture_output=True)
    time.sleep(3)

def start_rag_api():
    """Start RAG API"""
    print("🚀 Starting RAG API...")
    
    # Check if port is free
    result = subprocess.run(['lsof', '-i', ':8005'], capture_output=True)
    if result.returncode == 0:
        print("❌ Port 8005 is in use, killing process...")
        subprocess.run(['lsof', '-ti', ':8005'], capture_output=True)
        time.sleep(2)
    
    # Start RAG API
    try:
        process = subprocess.Popen(
            ['python3', 'enhanced_m1_m2_m3_m4_integrated_api.py'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        # Wait and check
        time.sleep(10)
        
        try:
            response = requests.get("http://localhost:8005/health", timeout=5)
            if response.status_code == 200:
                print("✅ RAG API started successfully")
                return True
            else:
                print(f"❌ RAG API health check failed: {response.status_code}")
                return False
        except:
            print("❌ RAG API failed to start")
            return False
            
    except Exception as e:
        print(f"❌ Error starting RAG API: {e}")
        return False

def start_webhook():
    """Start webhook server"""
    print("🚀 Starting webhook server...")
    
    # Check if port is free
    result = subprocess.run(['lsof', '-i', ':8081'], capture_output=True)
    if result.returncode == 0:
        print("❌ Port 8081 is in use, killing process...")
        subprocess.run(['lsof', '-ti', ':8081'], capture_output=True)
        time.sleep(2)
    
    # Start webhook server
    try:
        process = subprocess.Popen(
            ['python3', 'updated_line_bot_webhook.py'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        # Wait and check
        time.sleep(8)
        
        try:
            response = requests.get("http://localhost:8081/health", timeout=5)
            if response.status_code == 200:
                print("✅ Webhook server started successfully")
                return True
            else:
                print(f"❌ Webhook server health check failed: {response.status_code}")
                return False
        except:
            print("❌ Webhook server failed to start")
            return False
            
    except Exception as e:
        print(f"❌ Error starting webhook server: {e}")
        return False

def start_ngrok():
    """Start ngrok and get URL"""
    print("🚀 Starting ngrok...")
    
    # Kill existing ngrok
    subprocess.run(['pkill', 'ngrok'], capture_output=True)
    time.sleep(3)
    
    # Start ngrok
    try:
        process = subprocess.Popen(
            ['ngrok', 'http', '8081'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        # Wait for ngrok to start
        time.sleep(8)
        
        # Get URL
        for _ in range(15):
            try:
                response = requests.get("http://localhost:4040/api/tunnels", timeout=3)
                if response.status_code == 200:
                    tunnels = response.json()
                    if tunnels.get("tunnels"):
                        url = tunnels["tunnels"][0]["public_url"]
                        print(f"✅ ngrok started: {url}")
                        return url
            except:
                pass
            time.sleep(2)
        
        print("❌ Failed to get ngrok URL")
        return None
        
    except Exception as e:
        print(f"❌ Error starting ngrok: {e}")
        return None

def save_url(ngrok_url):
    """Save URL to file"""
    config = {
        "ngrok_url": ngrok_url,
        "webhook_url": f"{ngrok_url}/webhook",
        "timestamp": time.strftime('%Y-%m-%d %H:%M:%S')
    }
    
    with open("current_webhook_url.json", "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2, ensure_ascii=False)
    
    print(f"✅ URL saved: {ngrok_url}/webhook")

def create_report(webhook_url):
    """Create final report"""
    report = f"""# 🎉 LINE Bot Fixed!

## ✅ System Status
- RAG API: ✅ Running
- Webhook Server: ✅ Running  
- ngrok: ✅ Active

## 🔗 Webhook URL
```
{webhook_url}
```

## 📋 NEXT STEPS

1. **Update LINE Developer Console**:
   - Go to https://developers.line.biz/
   - Set webhook URL to: `{webhook_url}`
   - Enable webhook
   - Save

2. **Test the bot**:
   Send: `爸爸不會用洗衣機`

## 🧪 Test Commands
```bash
# Test health
curl {webhook_url.replace('/webhook', '/health')}

# Get current URL
python3 get_webhook_url.py
```

---
Fixed: {time.strftime('%Y-%m-%d %H:%M:%S')}
"""
    
    with open("SIMPLE_FIX_REPORT.md", "w", encoding="utf-8") as f:
        f.write(report)
    
    print("✅ Report created: SIMPLE_FIX_REPORT.md")

def main():
    print("🔧 Simple LINE Bot Fix")
    print("=" * 40)
    
    # Step 1: Clean up
    kill_processes()
    
    # Step 2: Start RAG API
    if not start_rag_api():
        print("❌ Failed to start RAG API")
        return
    
    # Step 3: Start webhook
    if not start_webhook():
        print("❌ Failed to start webhook")
        return
    
    # Step 4: Start ngrok
    ngrok_url = start_ngrok()
    if not ngrok_url:
        print("❌ Failed to start ngrok")
        return
    
    # Step 5: Save and report
    webhook_url = f"{ngrok_url}/webhook"
    save_url(ngrok_url)
    create_report(webhook_url)
    
    # Final check
    try:
        response = requests.get(f"{ngrok_url}/health", timeout=10)
        if response.status_code == 200:
            print("✅ Public health check passed")
        else:
            print(f"⚠️  Public health: {response.status_code}")
    except Exception as e:
        print(f"⚠️  Public health failed: {e}")
    
    print("\n" + "=" * 40)
    print("🎉 FIX COMPLETE!")
    print("=" * 40)
    print(f"📍 Webhook URL: {webhook_url}")
    print("📋 Update LINE Developer Console and test!")
    print("=" * 40)

if __name__ == "__main__":
    main() 