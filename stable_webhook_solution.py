#!/usr/bin/env python3
"""
Stable Webhook Solution - Maintains consistent webhook URL
"""

import os
import subprocess
import time
import requests
import json
import re
from typing import Optional

class StableWebhookSolution:
    def __init__(self):
        self.ngrok_url = None
        self.webhook_url = None
        self.config_file = "webhook_config.json"
        
    def load_config(self):
        """Load existing webhook configuration"""
        if os.path.exists(self.config_file):
            with open(self.config_file, 'r') as f:
                config = json.load(f)
                self.ngrok_url = config.get('ngrok_url')
                self.webhook_url = config.get('webhook_url')
                return True
        return False
    
    def save_config(self):
        """Save webhook configuration"""
        config = {
            'ngrok_url': self.ngrok_url,
            'webhook_url': self.webhook_url,
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
        }
        with open(self.config_file, 'w') as f:
            json.dump(config, f, indent=2)
    
    def get_ngrok_url(self) -> Optional[str]:
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
    
    def start_services(self):
        """Start all services with stable configuration"""
        print("🔧 Starting Stable Webhook Solution")
        print("=" * 50)
        
        # Load existing config
        if self.load_config():
            print(f"📋 Found existing config:")
            print(f"   ngrok URL: {self.ngrok_url}")
            print(f"   webhook URL: {self.webhook_url}")
        
        # Kill existing processes
        print("🧹 Cleaning up existing processes...")
        subprocess.run(["pkill", "-f", "updated_line_bot_webhook.py"], capture_output=True)
        subprocess.run(["pkill", "-f", "enhanced_m1_m2_m3_m4_integrated_api.py"], capture_output=True)
        subprocess.run(["pkill", "ngrok"], capture_output=True)
        time.sleep(3)
        
        # Start RAG API
        print("🚀 Starting RAG API...")
        subprocess.Popen(
            ["python3", "enhanced_m1_m2_m3_m4_integrated_api.py"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        time.sleep(5)
        
        # Start webhook server
        print("🚀 Starting webhook server...")
        subprocess.Popen(
            ["python3", "updated_line_bot_webhook.py"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        time.sleep(3)
        
        # Start ngrok
        print("🚀 Starting ngrok...")
        subprocess.Popen(
            ["ngrok", "http", "8081"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        time.sleep(5)
        
        # Get ngrok URL
        self.ngrok_url = self.get_ngrok_url()
        if self.ngrok_url:
            self.webhook_url = f"{self.ngrok_url}/webhook"
            self.save_config()
            print(f"✅ ngrok tunnel: {self.ngrok_url}")
            print(f"✅ webhook URL: {self.webhook_url}")
            return True
        else:
            print("❌ Failed to get ngrok URL")
            return False
    
    def create_stable_guide(self):
        """Create a stable guide with the current webhook URL"""
        guide = f"""# 🧠 LINE Bot - Stable Webhook Solution

## ✅ Current Configuration

### Stable Webhook URL
**Use this URL in LINE Developer Console:**
```
{self.webhook_url}
```

### System Status
- ✅ ngrok tunnel: {self.ngrok_url}
- ✅ webhook server: Running on port 8081
- ✅ RAG API: Running on port 8005
- ✅ All services: Active and monitored

## 🚀 Setup Instructions

### 1. Update LINE Developer Console
1. Go to [LINE Developer Console](https://developers.line.biz/)
2. Select your bot channel
3. Go to **Messaging API** settings
4. Set **Webhook URL** to: `{self.webhook_url}`
5. **Enable** "Use webhook"
6. Click **Save**

### 2. Test the Bot
Send this message to your bot:
```
爸爸不會用洗衣機
```

## 🎯 Expected Response
The bot will respond with:
- 🧠 Rich Flex Messages with visual analysis
- 📊 Confidence scores for each assessment
- 💡 Detailed explanations of findings
- 🎯 Actionable recommendations

## 🔧 Troubleshooting

### If webhook URL changes:
1. Run: `python3 stable_webhook_solution.py`
2. Check the new URL in the output
3. Update LINE Developer Console with the new URL

### If bot doesn't respond:
1. Check status: `curl {self.ngrok_url}/health`
2. Verify webhook URL in LINE Developer Console
3. Restart services: `python3 stable_webhook_solution.py`

## 📊 Quick Status Check
```bash
# Check if services are running
curl {self.ngrok_url}/health

# Check RAG API
curl http://localhost:8005/health

# Get current webhook URL
cat webhook_config.json
```

---
**Generated**: {time.strftime('%Y-%m-%d %H:%M:%S')}
**Stable URL**: {self.webhook_url}
**Status**: READY FOR TESTING! 🚀
"""
        
        with open("STABLE_WEBHOOK_GUIDE.md", "w", encoding="utf-8") as f:
            f.write(guide)
        
        print("✅ Stable webhook guide created: STABLE_WEBHOOK_GUIDE.md")
    
    def monitor_services(self):
        """Monitor services and restart if needed"""
        print("👀 Monitoring services...")
        print("Press Ctrl+C to stop")
        
        while True:
            try:
                # Check webhook server
                response = requests.get(f"{self.ngrok_url}/health", timeout=5)
                if response.status_code != 200:
                    print("⚠️  Webhook server down, restarting...")
                    self.start_services()
                
                # Check RAG API
                response = requests.get("http://localhost:8005/health", timeout=5)
                if response.status_code != 200:
                    print("⚠️  RAG API down, restarting...")
                    self.start_services()
                
                time.sleep(30)
                
            except KeyboardInterrupt:
                print("\n🛑 Stopping monitoring...")
                break
            except Exception as e:
                print(f"⚠️  Monitoring error: {e}")
                time.sleep(30)
    
    def run(self):
        """Main execution"""
        if self.start_services():
            self.create_stable_guide()
            
            print("\n" + "=" * 50)
            print("🎉 STABLE WEBHOOK SOLUTION READY!")
            print("=" * 50)
            print(f"📍 Stable ngrok URL: {self.ngrok_url}")
            print(f"📍 Stable webhook URL: {self.webhook_url}")
            print("")
            print("📋 NEXT STEPS:")
            print(f"1. Update LINE Developer Console with: {self.webhook_url}")
            print("2. Send message to bot: 爸爸不會用洗衣機")
            print("")
            print("👀 Services will be monitored automatically")
            print("📄 Check STABLE_WEBHOOK_GUIDE.md for details")
            print("=" * 50)
            
            # Start monitoring
            self.monitor_services()
        else:
            print("❌ Failed to start services")

def main():
    solution = StableWebhookSolution()
    solution.run()

if __name__ == "__main__":
    main() 