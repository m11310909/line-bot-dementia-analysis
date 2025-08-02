#!/usr/bin/env python3
"""
Debug script to identify and fix all issues with the LINE Bot system
"""

import os
import subprocess
import time
import requests
import json
import signal
from typing import Dict, Any, List

class SystemDebugger:
    def __init__(self):
        self.issues = []
        self.fixes = []
        
    def check_processes(self) -> Dict[str, bool]:
        """Check which processes are running"""
        print("🔍 Checking running processes...")
        
        processes = {
            'ngrok': False,
            'webhook_server': False,
            'rag_api': False
        }
        
        # Check ngrok
        try:
            result = subprocess.run(['pgrep', 'ngrok'], capture_output=True)
            if result.returncode == 0:
                processes['ngrok'] = True
                print("✅ ngrok is running")
            else:
                print("❌ ngrok is not running")
        except Exception as e:
            print(f"❌ Error checking ngrok: {e}")
        
        # Check webhook server
        try:
            result = subprocess.run(['lsof', '-i', ':8081'], capture_output=True)
            if result.returncode == 0:
                processes['webhook_server'] = True
                print("✅ Webhook server is running on port 8081")
            else:
                print("❌ Webhook server is not running on port 8081")
        except Exception as e:
            print(f"❌ Error checking webhook server: {e}")
        
        # Check RAG API
        try:
            result = subprocess.run(['lsof', '-i', ':8005'], capture_output=True)
            if result.returncode == 0:
                processes['rag_api'] = True
                print("✅ RAG API is running on port 8005")
            else:
                print("❌ RAG API is not running on port 8005")
        except Exception as e:
            print(f"❌ Error checking RAG API: {e}")
        
        return processes
    
    def check_ngrok_tunnel(self) -> str:
        """Check ngrok tunnel status"""
        print("🔍 Checking ngrok tunnel...")
        
        try:
            response = requests.get("http://localhost:4040/api/tunnels", timeout=5)
            if response.status_code == 200:
                tunnels = response.json()
                if tunnels.get("tunnels"):
                    url = tunnels["tunnels"][0]["public_url"]
                    print(f"✅ ngrok tunnel: {url}")
                    return url
                else:
                    print("❌ No ngrok tunnels found")
                    return None
            else:
                print(f"❌ ngrok API error: {response.status_code}")
                return None
        except Exception as e:
            print(f"❌ Error checking ngrok tunnel: {e}")
            return None
    
    def test_services(self) -> Dict[str, bool]:
        """Test service endpoints"""
        print("🧪 Testing service endpoints...")
        
        results = {
            'webhook_health': False,
            'rag_api_health': False,
            'ngrok_health': False
        }
        
        # Test webhook health
        try:
            response = requests.get("http://localhost:8081/health", timeout=5)
            if response.status_code == 200:
                results['webhook_health'] = True
                print("✅ Webhook health check passed")
            else:
                print(f"❌ Webhook health check failed: {response.status_code}")
        except Exception as e:
            print(f"❌ Webhook health check error: {e}")
        
        # Test RAG API health
        try:
            response = requests.get("http://localhost:8005/health", timeout=5)
            if response.status_code == 200:
                results['rag_api_health'] = True
                print("✅ RAG API health check passed")
            else:
                print(f"❌ RAG API health check failed: {response.status_code}")
        except Exception as e:
            print(f"❌ RAG API health check error: {e}")
        
        # Test ngrok health
        ngrok_url = self.check_ngrok_tunnel()
        if ngrok_url:
            try:
                response = requests.get(f"{ngrok_url}/health", timeout=10)
                if response.status_code == 200:
                    results['ngrok_health'] = True
                    print("✅ ngrok tunnel health check passed")
                else:
                    print(f"❌ ngrok tunnel health check failed: {response.status_code}")
            except Exception as e:
                print(f"❌ ngrok tunnel health check error: {e}")
        
        return results
    
    def kill_all_processes(self):
        """Kill all related processes"""
        print("🧹 Killing all related processes...")
        
        processes_to_kill = [
            'ngrok',
            'updated_line_bot_webhook.py',
            'enhanced_m1_m2_m3_m4_integrated_api.py'
        ]
        
        for process in processes_to_kill:
            try:
                subprocess.run(['pkill', '-f', process], capture_output=True)
                print(f"✅ Killed {process}")
            except Exception as e:
                print(f"⚠️  Error killing {process}: {e}")
        
        time.sleep(3)
    
    def start_services_manually(self):
        """Start services manually with proper error handling"""
        print("🚀 Starting services manually...")
        
        # Start RAG API
        print("📡 Starting RAG API...")
        try:
            rag_process = subprocess.Popen(
                ['python3', 'enhanced_m1_m2_m3_m4_integrated_api.py'],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            time.sleep(5)
            
            # Check if RAG API started
            try:
                response = requests.get("http://localhost:8005/health", timeout=5)
                if response.status_code == 200:
                    print("✅ RAG API started successfully")
                else:
                    print(f"❌ RAG API health check failed: {response.status_code}")
            except:
                print("❌ RAG API failed to start")
        except Exception as e:
            print(f"❌ Error starting RAG API: {e}")
        
        # Start webhook server
        print("📡 Starting webhook server...")
        try:
            webhook_process = subprocess.Popen(
                ['python3', 'updated_line_bot_webhook.py'],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            time.sleep(3)
            
            # Check if webhook server started
            try:
                response = requests.get("http://localhost:8081/health", timeout=5)
                if response.status_code == 200:
                    print("✅ Webhook server started successfully")
                else:
                    print(f"❌ Webhook server health check failed: {response.status_code}")
            except:
                print("❌ Webhook server failed to start")
        except Exception as e:
            print(f"❌ Error starting webhook server: {e}")
        
        # Start ngrok
        print("📡 Starting ngrok...")
        try:
            ngrok_process = subprocess.Popen(
                ['ngrok', 'http', '8081'],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            time.sleep(5)
            
            # Check ngrok tunnel
            ngrok_url = self.check_ngrok_tunnel()
            if ngrok_url:
                print(f"✅ ngrok started successfully: {ngrok_url}")
            else:
                print("❌ ngrok failed to start")
        except Exception as e:
            print(f"❌ Error starting ngrok: {e}")
    
    def create_debug_report(self):
        """Create a comprehensive debug report"""
        print("📋 Creating debug report...")
        
        report = f"""# 🐛 LINE Bot System Debug Report

## 🔍 Current Status

### Process Status
{self.check_processes()}

### Service Health
{self.test_services()}

### ngrok Tunnel
{self.check_ngrok_tunnel()}

## 🚀 Quick Fix Commands

### 1. Kill all processes and restart:
```bash
pkill -f "ngrok|updated_line_bot_webhook|enhanced_m1_m2_m3_m4"
python3 debug_system.py
```

### 2. Get current webhook URL:
```bash
python3 get_webhook_url.py
```

### 3. Test the system:
```bash
curl https://[ngrok-url]/health
```

## 🔧 Troubleshooting Steps

1. **If services won't start**: Check if ports are in use
2. **If ngrok URL changes**: Run `python3 get_webhook_url.py`
3. **If webhook doesn't respond**: Update LINE Developer Console
4. **If RAG API fails**: Check if all dependencies are installed

---
**Generated**: {time.strftime('%Y-%m-%d %H:%M:%S')}
**Status**: Debug complete
"""
        
        with open("DEBUG_REPORT.md", "w", encoding="utf-8") as f:
            f.write(report)
        
        print("✅ Debug report created: DEBUG_REPORT.md")
    
    def run_debug(self):
        """Run complete debug process"""
        print("🐛 LINE Bot System Debug")
        print("=" * 50)
        
        # Step 1: Check current status
        print("\n📊 Step 1: Checking current status...")
        processes = self.check_processes()
        services = self.test_services()
        ngrok_url = self.check_ngrok_tunnel()
        
        # Step 2: Identify issues
        print("\n🔍 Step 2: Identifying issues...")
        if not processes['rag_api']:
            self.issues.append("RAG API not running")
        if not processes['webhook_server']:
            self.issues.append("Webhook server not running")
        if not ngrok_url:
            self.issues.append("ngrok tunnel not available")
        if not services['webhook_health']:
            self.issues.append("Webhook health check failed")
        if not services['rag_api_health']:
            self.issues.append("RAG API health check failed")
        
        # Step 3: Apply fixes
        if self.issues:
            print(f"\n🔧 Step 3: Applying fixes for {len(self.issues)} issues...")
            self.kill_all_processes()
            self.start_services_manually()
            
            # Re-check after fixes
            print("\n📊 Step 4: Re-checking after fixes...")
            processes = self.check_processes()
            services = self.test_services()
            ngrok_url = self.check_ngrok_tunnel()
        
        # Step 5: Create report
        self.create_debug_report()
        
        # Step 6: Summary
        print("\n" + "=" * 50)
        print("🎉 DEBUG COMPLETE!")
        print("=" * 50)
        
        if ngrok_url:
            print(f"📍 Current webhook URL: {ngrok_url}/webhook")
            print("📋 Next steps:")
            print("1. Update LINE Developer Console with the webhook URL")
            print("2. Test with: 爸爸不會用洗衣機")
        else:
            print("❌ System still has issues - check DEBUG_REPORT.md")
        
        print("=" * 50)

def main():
    debugger = SystemDebugger()
    debugger.run_debug()

if __name__ == "__main__":
    main() 