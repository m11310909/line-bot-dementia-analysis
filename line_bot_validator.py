#!/usr/bin/env python3
"""
LINE Bot Configuration Validator
Validates that all components are properly configured
"""

import requests
import json
import os
import sys
from datetime import datetime

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    END = '\033[0m'

def check_service(name, url, expected_status=200):
    """Check if a service is running"""
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == expected_status:
            print(f"{Colors.GREEN}✓ {name}: Running{Colors.END}")
            return True
        else:
            print(f"{Colors.RED}✗ {name}: Unexpected status {response.status_code}{Colors.END}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"{Colors.RED}✗ {name}: Not reachable - {str(e)}{Colors.END}")
        return False

def check_ngrok():
    """Check ngrok tunnel status"""
    try:
        response = requests.get("http://localhost:4040/api/tunnels", timeout=5)
        tunnels = response.json()
        if tunnels.get("tunnels"):
            url = tunnels["tunnels"][0]["public_url"]
            print(f"{Colors.GREEN}✓ ngrok: Running at {url}{Colors.END}")
            return url
        else:
            print(f"{Colors.YELLOW}⚠ ngrok: No tunnels found{Colors.END}")
            return None
    except:
        print(f"{Colors.RED}✗ ngrok: Not running{Colors.END}")
        return None

def test_rag_api():
    """Test RAG API endpoint"""
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
                print(f"{Colors.GREEN}✓ RAG API M1: Working correctly{Colors.END}")
                return True
            else:
                print(f"{Colors.YELLOW}⚠ RAG API M1: Unexpected response format{Colors.END}")
                return False
        else:
            print(f"{Colors.RED}✗ RAG API M1: Error {response.status_code}{Colors.END}")
            return False
    except Exception as e:
        print(f"{Colors.RED}✗ RAG API M1: Failed - {str(e)}{Colors.END}")
        return False

def check_env_vars():
    """Check required environment variables"""
    # Load .env file
    from dotenv import load_dotenv
    load_dotenv()
    
    required_vars = [
        "LINE_CHANNEL_ACCESS_TOKEN",
        "LINE_CHANNEL_SECRET",
        "GOOGLE_GEMINI_API_KEY"
    ]
    
    all_good = True
    for var in required_vars:
        if os.getenv(var):
            print(f"{Colors.GREEN}✓ {var}: Set{Colors.END}")
        else:
            print(f"{Colors.RED}✗ {var}: Not set{Colors.END}")
            all_good = False
    
    return all_good

def main():
    print(f"\n{Colors.BLUE}🔍 LINE Bot Configuration Validator{Colors.END}")
    print(f"{Colors.BLUE}{'='*40}{Colors.END}\n")
    
    print(f"{Colors.YELLOW}Checking Services:{Colors.END}")
    webhook_ok = check_service("Webhook Server", "http://localhost:8081/health")
    rag_ok = check_service("RAG API", "http://localhost:8005/health")
    ngrok_url = check_ngrok()
    
    print(f"\n{Colors.YELLOW}Testing API Endpoints:{Colors.END}")
    api_ok = test_rag_api()
    
    print(f"\n{Colors.YELLOW}Checking Environment:{Colors.END}")
    env_ok = check_env_vars()
    
    # Summary
    print(f"\n{Colors.BLUE}{'='*40}{Colors.END}")
    print(f"{Colors.BLUE}Summary:{Colors.END}")
    
    all_ok = webhook_ok and rag_ok and ngrok_url and api_ok and env_ok
    
    if all_ok:
        print(f"{Colors.GREEN}✅ All systems operational!{Colors.END}")
        if ngrok_url:
            webhook_url = f"{ngrok_url}/webhook"
            print(f"\n{Colors.YELLOW}📋 Next Steps:{Colors.END}")
            print(f"1. Update LINE webhook URL to: {Colors.BLUE}{webhook_url}{Colors.END}")
            print(f"2. Enable webhook in LINE Developer Console")
            print(f"3. Click 'Verify' to test connection")
            print(f"4. Send a test message to your bot")
            
            # Save webhook URL to file
            with open("CURRENT_WEBHOOK_URL.md", "w") as f:
                f.write(f"# Current Webhook URL\n\n**URL:** {webhook_url}\n\n**Last Updated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n## Instructions\n\n1. Go to LINE Developer Console\n2. Select your bot\n3. Go to Messaging API settings\n4. Set Webhook URL to: `{webhook_url}`\n5. Enable 'Use webhook'\n6. Click 'Verify' to test\n7. Save changes\n\n## Test Message\n\nSend this message to your bot:\n- '爸爸不會用洗衣機'\n- '媽媽中度失智'\n- '爺爺有妄想症狀'\n\nExpected response: Rich Flex Message with analysis")
    else:
        print(f"{Colors.RED}❌ Some issues need attention{Colors.END}")
        print(f"\n{Colors.YELLOW}📋 Fix Required:{Colors.END}")
        if not webhook_ok:
            print("- Start webhook server: python3 updated_line_bot_webhook.py")
        if not rag_ok:
            print("- Start RAG API: python3 enhanced_m1_m2_m3_m4_integrated_api.py")
        if not ngrok_url:
            print("- Start ngrok: ngrok http 8081")
        if not env_ok:
            print("- Check .env file for missing variables")
    
    print(f"\n{Colors.BLUE}Validation completed at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{Colors.END}\n")

if __name__ == "__main__":
    main() 