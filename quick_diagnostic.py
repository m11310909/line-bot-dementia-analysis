#!/usr/bin/env python3
"""
Quick Diagnostic Script for LINE Bot Troubleshooting
Runs all essential checks in one command
"""

import requests
import json
import os
import sys
from datetime import datetime
from dotenv import load_dotenv

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    END = '\033[0m'

def print_header():
    print(f"\n{Colors.BLUE}🔧 LINE Bot Quick Diagnostic{Colors.END}")
    print(f"{Colors.BLUE}{'='*50}{Colors.END}")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

def check_service(name, url, timeout=5):
    """Check if a service is responding"""
    try:
        response = requests.get(url, timeout=timeout)
        if response.status_code == 200:
            print(f"{Colors.GREEN}✅ {name}: Healthy{Colors.END}")
            return True
        else:
            print(f"{Colors.RED}❌ {name}: Status {response.status_code}{Colors.END}")
            return False
    except Exception as e:
        print(f"{Colors.RED}❌ {name}: Not reachable - {str(e)}{Colors.END}")
        return False

def check_ngrok():
    """Check ngrok tunnel status"""
    try:
        response = requests.get("http://localhost:4040/api/tunnels", timeout=5)
        tunnels = response.json()
        if tunnels.get("tunnels"):
            url = tunnels["tunnels"][0]["public_url"]
            webhook_url = f"{url}/webhook"
            print(f"{Colors.GREEN}✅ ngrok: Active at {url}{Colors.END}")
            print(f"{Colors.BLUE}🔗 Webhook URL: {webhook_url}{Colors.END}")
            return webhook_url
        else:
            print(f"{Colors.YELLOW}⚠️  ngrok: No tunnels found{Colors.END}")
            return None
    except Exception as e:
        print(f"{Colors.RED}❌ ngrok: Not running - {str(e)}{Colors.END}")
        return None

def check_env_vars():
    """Check environment variables"""
    load_dotenv()
    required_vars = [
        "LINE_CHANNEL_ACCESS_TOKEN",
        "LINE_CHANNEL_SECRET", 
        "GOOGLE_GEMINI_API_KEY"
    ]
    
    all_good = True
    for var in required_vars:
        if os.getenv(var):
            print(f"{Colors.GREEN}✅ {var}: Set{Colors.END}")
        else:
            print(f"{Colors.RED}❌ {var}: Not set{Colors.END}")
            all_good = False
    
    return all_good

def test_rag_api():
    """Test RAG API with sample request"""
    try:
        test_data = {
            "text": "測試訊息",
            "user_context": {"user_level": "general"}
        }
        response = requests.post(
            "http://localhost:8005/analyze/M1",
            json=test_data,
            timeout=10
        )
        if response.status_code == 200:
            data = response.json()
            if "flex_message" in data:
                print(f"{Colors.GREEN}✅ RAG API: Working correctly{Colors.END}")
                return True
            else:
                print(f"{Colors.YELLOW}⚠️  RAG API: Unexpected response format{Colors.END}")
                return False
        else:
            print(f"{Colors.RED}❌ RAG API: Error {response.status_code}{Colors.END}")
            return False
    except Exception as e:
        print(f"{Colors.RED}❌ RAG API: Failed - {str(e)}{Colors.END}")
        return False

def check_ports():
    """Check if required ports are in use"""
    import subprocess
    
    ports = [8005, 8081, 4040]
    for port in ports:
        try:
            result = subprocess.run(['lsof', '-i', f':{port}'], 
                                  capture_output=True, text=True)
            if result.stdout.strip():
                print(f"{Colors.GREEN}✅ Port {port}: In use{Colors.END}")
            else:
                print(f"{Colors.RED}❌ Port {port}: Not in use{Colors.END}")
        except Exception:
            print(f"{Colors.YELLOW}⚠️  Port {port}: Cannot check{Colors.END}")

def main():
    print_header()
    
    print(f"{Colors.YELLOW}🔍 Checking Services:{Colors.END}")
    rag_ok = check_service("RAG API", "http://localhost:8005/health")
    webhook_ok = check_service("Webhook Server", "http://localhost:8081/health")
    ngrok_url = check_ngrok()
    
    print(f"\n{Colors.YELLOW}🔍 Testing API:{Colors.END}")
    api_ok = test_rag_api()
    
    print(f"\n{Colors.YELLOW}🔍 Checking Environment:{Colors.END}")
    env_ok = check_env_vars()
    
    print(f"\n{Colors.YELLOW}🔍 Checking Ports:{Colors.END}")
    check_ports()
    
    # Summary
    print(f"\n{Colors.BLUE}{'='*50}{Colors.END}")
    print(f"{Colors.BLUE}📊 Summary:{Colors.END}")
    
    all_ok = rag_ok and webhook_ok and ngrok_url and api_ok and env_ok
    
    if all_ok:
        print(f"{Colors.GREEN}🎉 All systems operational!{Colors.END}")
        if ngrok_url:
            print(f"\n{Colors.YELLOW}📋 Next Steps:{Colors.END}")
            print(f"1. Update LINE webhook URL to: {Colors.BLUE}{ngrok_url}{Colors.END}")
            print(f"2. Enable webhook in LINE Developer Console")
            print(f"3. Test with message: '爸爸不會用洗衣機'")
            
            # Save webhook URL
            with open("CURRENT_WEBHOOK_URL.md", "w") as f:
                f.write(f"# Current Webhook URL\n\n**URL:** {ngrok_url}\n\n**Last Updated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n## Instructions\n\n1. Go to LINE Developer Console\n2. Set webhook URL to: `{ngrok_url}`\n3. Enable webhook\n4. Test with: '爸爸不會用洗衣機'")
    else:
        print(f"{Colors.RED}⚠️  Some issues detected{Colors.END}")
        print(f"\n{Colors.YELLOW}🔧 Quick Fixes:{Colors.END}")
        if not rag_ok:
            print("- Start RAG API: python3 enhanced_m1_m2_m3_m4_integrated_api.py")
        if not webhook_ok:
            print("- Start webhook: python3 updated_line_bot_webhook.py")
        if not ngrok_url:
            print("- Start ngrok: ngrok http 8081")
        if not env_ok:
            print("- Check .env file")
    
    print(f"\n{Colors.BLUE}Diagnostic completed at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{Colors.END}\n")

if __name__ == "__main__":
    main() 