#!/usr/bin/env python3
"""
Persistent System Monitor - Continuously monitors and auto-restarts services
"""

import requests
import json
import time
import subprocess
import os
import signal
import sys
from datetime import datetime
from dotenv import load_dotenv

class SystemMonitor:
    def __init__(self):
        self.check_interval = 30  # Check every 30 seconds
        self.max_restart_attempts = 3
        self.restart_cooldown = 60  # Wait 60 seconds between restart attempts
        self.last_restart_time = 0
        self.restart_count = 0
        self.running = True
        
        # Load environment variables
        load_dotenv()
        
        # Setup signal handlers for graceful shutdown
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)
    
    def signal_handler(self, signum, frame):
        """Handle shutdown signals"""
        print(f"\n🛑 Received signal {signum}, shutting down gracefully...")
        self.running = False
    
    def log(self, message):
        """Log message with timestamp"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] {message}")
    
    def check_service_health(self, name, url, expected_status="healthy"):
        """Check if a service is healthy"""
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                data = response.json()
                status = data.get("status", "unknown")
                if status == expected_status:
                    return True, status
                else:
                    return False, f"Expected {expected_status}, got {status}"
            else:
                return False, f"HTTP {response.status_code}"
        except Exception as e:
            return False, str(e)
    
    def check_process_running(self, process_name):
        """Check if a process is running"""
        try:
            result = subprocess.run(['pgrep', '-f', process_name], capture_output=True, text=True)
            return result.returncode == 0
        except Exception:
            return False
    
    def kill_process(self, process_name):
        """Kill a process"""
        try:
            subprocess.run(['pkill', '-f', process_name], capture_output=True)
            time.sleep(2)
            return True
        except Exception:
            return False
    
    def start_rag_api(self):
        """Start RAG API"""
        self.log("🚀 Starting RAG API...")
        
        # Kill any existing process
        self.kill_process("enhanced_m1_m2_m3_m4_integrated_api.py")
        time.sleep(2)
        
        # Start RAG API
        process = subprocess.Popen(
            ['python3', 'enhanced_m1_m2_m3_m4_integrated_api.py'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        # Wait for startup
        time.sleep(12)
        
        # Check if it's working
        for _ in range(5):
            healthy, status = self.check_service_health("RAG API", "http://localhost:8005/health")
            if healthy:
                self.log("✅ RAG API started successfully")
                return True
            time.sleep(2)
        
        self.log("❌ RAG API failed to start")
        return False
    
    def start_webhook_server(self):
        """Start webhook server"""
        self.log("🚀 Starting webhook server...")
        
        # Kill any existing process
        self.kill_process("updated_line_bot_webhook.py")
        time.sleep(2)
        
        # Start webhook server
        process = subprocess.Popen(
            ['python3', 'updated_line_bot_webhook.py'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        # Wait for startup
        time.sleep(8)
        
        # Check if it's working
        for _ in range(5):
            healthy, status = self.check_service_health("Webhook Server", "http://localhost:8081/health")
            if healthy:
                self.log("✅ Webhook server started successfully")
                return True
            time.sleep(2)
        
        self.log("❌ Webhook server failed to start")
        return False
    
    def start_ngrok(self):
        """Start ngrok"""
        self.log("🚀 Starting ngrok...")
        
        # Kill existing ngrok
        self.kill_process("ngrok")
        time.sleep(2)
        
        # Start ngrok
        subprocess.Popen(['ngrok', 'http', '8081'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        time.sleep(5)
        
        # Get ngrok URL
        try:
            response = requests.get("http://localhost:4040/api/tunnels", timeout=5)
            if response.status_code == 200:
                tunnels = response.json()["tunnels"]
                if tunnels:
                    ngrok_url = tunnels[0]["public_url"]
                    self.log(f"✅ ngrok started: {ngrok_url}")
                    return ngrok_url
        except:
            pass
        
        self.log("❌ ngrok failed to start")
        return None
    
    def restart_all_services(self):
        """Restart all services"""
        current_time = time.time()
        
        # Check if we should restart (cooldown period)
        if current_time - self.last_restart_time < self.restart_cooldown:
            self.log(f"⏳ Restart cooldown active, waiting...")
            return False
        
        if self.restart_count >= self.max_restart_attempts:
            self.log(f"⚠️  Maximum restart attempts reached ({self.max_restart_attempts})")
            return False
        
        self.log("🔄 Restarting all services...")
        
        # Restart services
        rag_success = self.start_rag_api()
        webhook_success = self.start_webhook_server()
        ngrok_url = self.start_ngrok()
        
        if rag_success and webhook_success and ngrok_url:
            self.log("✅ All services restarted successfully")
            self.last_restart_time = current_time
            self.restart_count += 1
            return True
        else:
            self.log("❌ Service restart failed")
            return False
    
    def monitor_services(self):
        """Monitor all services continuously"""
        self.log("🔍 Starting persistent system monitor...")
        
        while self.running:
            try:
                # Check RAG API
                rag_healthy, rag_status = self.check_service_health("RAG API", "http://localhost:8005/health")
                
                # Check Webhook Server
                webhook_healthy, webhook_status = self.check_service_health("Webhook Server", "http://localhost:8081/health")
                
                # Check processes
                rag_process = self.check_process_running("enhanced_m1_m2_m3_m4_integrated_api.py")
                webhook_process = self.check_process_running("updated_line_bot_webhook.py")
                ngrok_process = self.check_process_running("ngrok")
                
                # Log status
                status_msg = f"RAG API: {'✅' if rag_healthy else '❌'} | Webhook: {'✅' if webhook_healthy else '❌'} | Processes: {'✅' if all([rag_process, webhook_process, ngrok_process]) else '❌'}"
                self.log(status_msg)
                
                # Check if any service is down
                if not (rag_healthy and webhook_healthy and rag_process and webhook_process and ngrok_process):
                    self.log("⚠️  Service failure detected, attempting restart...")
                    if self.restart_all_services():
                        self.log("✅ Services restored")
                    else:
                        self.log("❌ Service restart failed")
                
                # Wait before next check
                time.sleep(self.check_interval)
                
            except KeyboardInterrupt:
                self.log("🛑 Monitor stopped by user")
                break
            except Exception as e:
                self.log(f"❌ Monitor error: {e}")
                time.sleep(self.check_interval)
    
    def save_status_report(self):
        """Save current status report"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Get current status
        rag_healthy, rag_status = self.check_service_health("RAG API", "http://localhost:8005/health")
        webhook_healthy, webhook_status = self.check_service_health("Webhook Server", "http://localhost:8081/health")
        
        # Get ngrok URL
        ngrok_url = None
        try:
            response = requests.get("http://localhost:4040/api/tunnels", timeout=5)
            if response.status_code == 200:
                tunnels = response.json()["tunnels"]
                if tunnels:
                    ngrok_url = tunnels[0]["public_url"]
        except:
            pass
        
        report = {
            "timestamp": timestamp,
            "rag_api": {
                "healthy": rag_healthy,
                "status": rag_status
            },
            "webhook_server": {
                "healthy": webhook_healthy,
                "status": webhook_status
            },
            "ngrok_url": ngrok_url,
            "restart_count": self.restart_count,
            "monitor_running": self.running
        }
        
        filename = f"persistent_monitor_status_{timestamp}.json"
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        self.log(f"💾 Status report saved: {filename}")
        return report

def main():
    """Main function"""
    print("🔄 PERSISTENT SYSTEM MONITOR")
    print("="*50)
    print("This monitor will continuously check services and auto-restart if needed")
    print("Press Ctrl+C to stop the monitor")
    print("="*50)
    
    monitor = SystemMonitor()
    
    try:
        # Start monitoring
        monitor.monitor_services()
    except KeyboardInterrupt:
        print("\n🛑 Stopping monitor...")
    finally:
        # Save final status report
        monitor.save_status_report()
        print("✅ Monitor stopped")

if __name__ == "__main__":
    main() 