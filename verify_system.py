#!/usr/bin/env python3
"""
Verify that the LINE Bot system is working correctly
"""

import requests
import json

def verify_system():
    """Verify all components are working"""
    print("🔍 Verifying LINE Bot System")
    print("=" * 40)
    
    # Check ngrok tunnel
    try:
        response = requests.get("http://localhost:4040/api/tunnels")
        if response.status_code == 200:
            tunnels = response.json()
            if tunnels.get("tunnels"):
                url = tunnels["tunnels"][0]["public_url"]
                print(f"✅ ngrok tunnel: {url}")
                
                # Test webhook endpoint
                webhook_response = requests.get(f"{url}/health")
                if webhook_response.status_code == 200:
                    print("✅ Webhook server responding")
                else:
                    print(f"❌ Webhook server error: {webhook_response.status_code}")
            else:
                print("❌ No ngrok tunnels found")
        else:
            print("❌ ngrok API not responding")
    except Exception as e:
        print(f"❌ ngrok check failed: {e}")
    
    # Check RAG API
    try:
        response = requests.get("http://localhost:8005/health")
        if response.status_code == 200:
            print("✅ RAG API healthy")
        else:
            print(f"❌ RAG API error: {response.status_code}")
    except Exception as e:
        print(f"❌ RAG API check failed: {e}")
    
    # Test RAG API with sample message
    try:
        response = requests.post(
            "http://localhost:8005/comprehensive-analysis",
            json={"text": "爸爸不會用洗衣機"},
            timeout=10
        )
        if response.status_code == 200:
            result = response.json()
            print("✅ RAG API processing messages correctly")
            print(f"📊 Response type: {result.get('type', 'unknown')}")
        else:
            print(f"❌ RAG API processing error: {response.status_code}")
    except Exception as e:
        print(f"❌ RAG API processing test failed: {e}")
    
    print("\n" + "=" * 40)
    print("📋 NEXT STEPS:")
    print("1. Go to LINE Developer Console")
    print("2. Set webhook URL to: https://1bd6facd30d6.ngrok-free.app/webhook")
    print("3. Enable webhook")
    print("4. Send message to bot: 爸爸不會用洗衣機")
    print("=" * 40)

if __name__ == "__main__":
    verify_system() 