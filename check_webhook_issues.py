#!/usr/bin/env python3
"""
Check Webhook Issues
Comprehensive check for all potential webhook problems
"""

import requests
import subprocess
import os
import json
from dotenv import load_dotenv

load_dotenv()

def check_ngrok():
    """Check if ngrok is running and get tunnel URL"""
    print("🔍 Checking ngrok tunnel...")
    
    try:
        # Check if ngrok process is running
        result = subprocess.run(['ps', 'aux'], capture_output=True, text=True)
        ngrok_running = 'ngrok http 8081' in result.stdout
        
        if ngrok_running:
            print("✅ ngrok process is running")
        else:
            print("❌ ngrok process not found")
            return None
        
        # Get tunnel URL
        response = requests.get("http://localhost:4040/api/tunnels", timeout=5)
        if response.status_code == 200:
            data = response.json()
            if data.get('tunnels'):
                tunnel_url = data['tunnels'][0]['public_url']
                webhook_url = f"{tunnel_url}/webhook"
                print(f"✅ ngrok tunnel: {tunnel_url}")
                print(f"🔗 Webhook URL: {webhook_url}")
                return webhook_url
            else:
                print("❌ No ngrok tunnels found")
                return None
        else:
            print(f"❌ ngrok API error: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"❌ ngrok check failed: {e}")
        return None

def check_webhook_server():
    """Check if webhook server is responding"""
    print("\n🔍 Checking webhook server...")
    
    try:
        response = requests.post(
            "http://localhost:8081/test-webhook",
            json={"text": "測試"},
            timeout=5
        )
        
        if response.status_code == 200:
            data = response.json()
            rag_url = data.get('rag_api_url', '')
            print("✅ Webhook server is responding")
            print(f"📊 RAG API URL: {rag_url}")
            
            if "analyze/M1" in rag_url:
                print("✅ Webhook is configured to use RAG API")
                return True
            else:
                print("❌ Webhook is not using correct RAG API")
                return False
        else:
            print(f"❌ Webhook server error: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Webhook server check failed: {e}")
        return False

def check_external_connectivity(webhook_url):
    """Test if webhook is reachable from internet"""
    print(f"\n🔍 Testing external connectivity...")
    
    try:
        response = requests.post(
            webhook_url,
            json={"test": "connection"},
            timeout=10
        )
        
        if response.status_code in [200, 400, 401]:  # Any response means reachable
            print("✅ Webhook is reachable from internet")
            return True
        else:
            print(f"❌ Webhook not reachable: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ External connectivity failed: {e}")
        return False

def check_bot_credentials():
    """Check if bot credentials are valid"""
    print("\n🔍 Checking bot credentials...")
    
    token = os.getenv('LINE_CHANNEL_ACCESS_TOKEN')
    secret = os.getenv('LINE_CHANNEL_SECRET')
    
    if token and len(token) > 50:
        print("✅ LINE_CHANNEL_ACCESS_TOKEN is set and valid")
    else:
        print("❌ LINE_CHANNEL_ACCESS_TOKEN is missing or invalid")
        return False
    
    if secret and len(secret) > 20:
        print("✅ LINE_CHANNEL_SECRET is set and valid")
    else:
        print("❌ LINE_CHANNEL_SECRET is missing or invalid")
        return False
    
    return True

def check_rag_api():
    """Check if RAG API is working"""
    print("\n🔍 Checking RAG API...")
    
    try:
        response = requests.post(
            "http://localhost:8005/analyze/M1",
            json={"text": "測試", "user_context": {"user_level": "general"}},
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success') and 'flex_message' in data:
                print("✅ RAG API is working correctly")
                return True
            else:
                print("❌ RAG API response format unexpected")
                return False
        else:
            print(f"❌ RAG API error: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ RAG API check failed: {e}")
        return False

def main():
    print("=" * 60)
    print("🔧 WEBHOOK ISSUES CHECK")
    print("=" * 60)
    
    # Check all components
    webhook_url = check_ngrok()
    webhook_ok = check_webhook_server()
    credentials_ok = check_bot_credentials()
    rag_ok = check_rag_api()
    
    if webhook_url:
        external_ok = check_external_connectivity(webhook_url)
    else:
        external_ok = False
    
    print("\n" + "=" * 60)
    print("📊 CHECK RESULTS:")
    print(f"✅ ngrok tunnel: {'OK' if webhook_url else 'FAILED'}")
    print(f"✅ webhook server: {'OK' if webhook_ok else 'FAILED'}")
    print(f"✅ external connectivity: {'OK' if external_ok else 'FAILED'}")
    print(f"✅ bot credentials: {'OK' if credentials_ok else 'FAILED'}")
    print(f"✅ RAG API: {'OK' if rag_ok else 'FAILED'}")
    
    print("\n" + "=" * 60)
    if all([webhook_url, webhook_ok, external_ok, credentials_ok, rag_ok]):
        print("🎉 ALL CHECKS PASSED!")
        print("✅ Internal system is working correctly")
        print("\n📋 NEXT STEPS:")
        print("1. Go to LINE Developer Console")
        print("2. Set webhook URL to:", webhook_url)
        print("3. Enable webhook")
        print("4. Add bot as friend")
        print("5. Send test message: '測試'")
    else:
        print("❌ SOME CHECKS FAILED")
        print("\n🔧 TROUBLESHOOTING:")
        if not webhook_url:
            print("- Start ngrok: ngrok http 8081")
        if not webhook_ok:
            print("- Restart webhook server")
        if not external_ok:
            print("- Check firewall/network settings")
        if not credentials_ok:
            print("- Check .env file for LINE credentials")
        if not rag_ok:
            print("- Restart RAG API server")
    
    print("=" * 60)

if __name__ == "__main__":
    main() 