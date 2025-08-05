#!/usr/bin/env python3
"""
Global System Diagnosis - Comprehensive check for "系統暫時無法使用" issue
"""

import requests
import json
import time
import subprocess
import os
import sys
from dotenv import load_dotenv

def check_environment():
    """Check environment variables and configuration"""
    print("🔧 Environment Check")
    print("="*40)
    
    # Load environment variables
    load_dotenv()
    
    # Check LINE Bot credentials
    line_token = os.getenv('LINE_CHANNEL_ACCESS_TOKEN')
    line_secret = os.getenv('LINE_CHANNEL_SECRET')
    
    print(f"✅ LINE_CHANNEL_ACCESS_TOKEN: {'SET' if line_token else 'NOT SET'}")
    print(f"✅ LINE_CHANNEL_SECRET: {'SET' if line_secret else 'NOT SET'}")
    
    # Check other important variables
    third_party_api = os.getenv('THIRD_PARTY_API_URL')
    chatbot_api = os.getenv('CHATBOT_API_URL')
    
    print(f"✅ THIRD_PARTY_API_URL: {'SET' if third_party_api else 'NOT SET'}")
    print(f"✅ CHATBOT_API_URL: {'SET' if chatbot_api else 'NOT SET'}")
    
    return bool(line_token and line_secret)

def check_services():
    """Check all services health"""
    print("\n🏥 Services Health Check")
    print("="*40)
    
    services = [
        {
            "name": "RAG API",
            "url": "http://localhost:8005/health",
            "expected": "healthy"
        },
        {
            "name": "Webhook Server",
            "url": "http://localhost:8081/health",
            "expected": "healthy"
        }
    ]
    
    all_healthy = True
    
    for service in services:
        try:
            response = requests.get(service["url"], timeout=5)
            if response.status_code == 200:
                data = response.json()
                status = data.get("status", "unknown")
                if status == service["expected"]:
                    print(f"✅ {service['name']}: {status}")
                else:
                    print(f"⚠️  {service['name']}: {status} (expected {service['expected']})")
                    all_healthy = False
            else:
                print(f"❌ {service['name']}: HTTP {response.status_code}")
                all_healthy = False
        except Exception as e:
            print(f"❌ {service['name']}: {e}")
            all_healthy = False
    
    return all_healthy

def check_processes():
    """Check if required processes are running"""
    print("\n🔄 Process Check")
    print("="*40)
    
    processes = [
        "enhanced_m1_m2_m3_m4_integrated_api.py",
        "updated_line_bot_webhook.py",
        "ngrok"
    ]
    
    all_running = True
    
    for process in processes:
        try:
            result = subprocess.run(['pgrep', '-f', process], capture_output=True, text=True)
            if result.returncode == 0:
                print(f"✅ {process}: Running")
            else:
                print(f"❌ {process}: Not running")
                all_running = False
        except Exception as e:
            print(f"❌ {process}: Error checking - {e}")
            all_running = False
    
    return all_running

def check_ports():
    """Check if ports are in use"""
    print("\n🔌 Port Check")
    print("="*40)
    
    ports = [8005, 8081]
    all_ports_ok = True
    
    for port in ports:
        try:
            result = subprocess.run(['lsof', '-i', f':{port}'], capture_output=True, text=True)
            if result.returncode == 0:
                print(f"✅ Port {port}: In use")
            else:
                print(f"❌ Port {port}: Not in use")
                all_ports_ok = False
        except Exception as e:
            print(f"❌ Port {port}: Error checking - {e}")
            all_ports_ok = False
    
    return all_ports_ok

def test_api_functionality():
    """Test API functionality with real requests"""
    print("\n🧪 API Functionality Test")
    print("="*40)
    
    test_cases = [
        {
            "input": "爸爸不會用洗衣機",
            "module": "M1",
            "description": "M1 警訊測試"
        },
        {
            "input": "媽媽中度失智",
            "module": "M2",
            "description": "M2 病程測試"
        }
    ]
    
    all_success = True
    
    for test_case in test_cases:
        try:
            start_time = time.time()
            response = requests.post(
                f"http://localhost:8005/analyze/{test_case['module']}",
                json={"text": test_case["input"]},
                timeout=10
            )
            response_time = time.time() - start_time
            
            if response.status_code == 200:
                data = response.json()
                success = data.get("success", False)
                has_flex = "flex_message" in data
                
                if success and has_flex:
                    print(f"✅ {test_case['description']}: Success ({response_time:.2f}s)")
                else:
                    print(f"❌ {test_case['description']}: Failed")
                    all_success = False
            else:
                print(f"❌ {test_case['description']}: HTTP {response.status_code}")
                all_success = False
                
        except Exception as e:
            print(f"❌ {test_case['description']}: {e}")
            all_success = False
    
    return all_success

def check_webhook_url():
    """Check webhook URL accessibility"""
    print("\n🌐 Webhook URL Check")
    print("="*40)
    
    try:
        # Get current ngrok URL
        response = requests.get("http://localhost:4040/api/tunnels", timeout=5)
        if response.status_code == 200:
            tunnels = response.json()["tunnels"]
            if tunnels:
                ngrok_url = tunnels[0]["public_url"]
                print(f"✅ ngrok URL: {ngrok_url}")
                
                # Test webhook health
                webhook_health_url = f"{ngrok_url}/health"
                try:
                    health_response = requests.get(webhook_health_url, timeout=5)
                    if health_response.status_code == 200:
                        print(f"✅ Webhook health: Accessible")
                        return ngrok_url
                    else:
                        print(f"❌ Webhook health: HTTP {health_response.status_code}")
                        return None
                except Exception as e:
                    print(f"❌ Webhook health: {e}")
                    return None
            else:
                print("❌ No ngrok tunnels found")
                return None
        else:
            print("❌ Cannot access ngrok API")
            return None
    except Exception as e:
        print(f"❌ ngrok check: {e}")
        return None

def check_error_handling():
    """Check error handling in webhook"""
    print("\n🚨 Error Handling Check")
    print("="*40)
    
    # Test webhook with invalid signature
    try:
        response = requests.post(
            "https://4c6f9c800a6c.ngrok-free.app/webhook",
            json={"events": [{"type": "message", "message": {"type": "text", "text": "test"}}]},
            timeout=5
        )
        
        if response.status_code == 400:
            data = response.json()
            if "Missing X-Line-Signature header" in data.get("error", ""):
                print("✅ Webhook error handling: Working correctly")
                return True
            else:
                print(f"⚠️  Webhook error handling: Unexpected response - {data}")
                return False
        else:
            print(f"❌ Webhook error handling: Unexpected status {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Webhook error handling: {e}")
        return False

def create_diagnosis_report(env_ok, services_ok, processes_ok, ports_ok, api_ok, webhook_url, error_handling_ok):
    """Create comprehensive diagnosis report"""
    print("\n📊 Diagnosis Report")
    print("="*40)
    
    overall_success = all([env_ok, services_ok, processes_ok, ports_ok, api_ok, error_handling_ok])
    
    print(f"✅ Environment: {'OK' if env_ok else 'FAILED'}")
    print(f"✅ Services: {'OK' if services_ok else 'FAILED'}")
    print(f"✅ Processes: {'OK' if processes_ok else 'FAILED'}")
    print(f"✅ Ports: {'OK' if ports_ok else 'FAILED'}")
    print(f"✅ API Functionality: {'OK' if api_ok else 'FAILED'}")
    print(f"✅ Error Handling: {'OK' if error_handling_ok else 'FAILED'}")
    
    if webhook_url:
        print(f"✅ Webhook URL: {webhook_url}/webhook")
    else:
        print("❌ Webhook URL: Not accessible")
    
    print(f"\n🎯 Overall Status: {'✅ HEALTHY' if overall_success else '❌ ISSUES DETECTED'}")
    
    if overall_success:
        print("\n🎉 System appears to be working correctly!")
        print("📋 If you're still seeing '系統暫時無法使用':")
        print("1. Check LINE Developer Console webhook URL")
        print("2. Verify LINE Bot credentials")
        print("3. Test with real user messages")
    else:
        print("\n⚠️  Issues detected. Recommended actions:")
        if not env_ok:
            print("- Check .env file configuration")
        if not services_ok:
            print("- Restart services: python3 comprehensive_system_fix.py")
        if not processes_ok:
            print("- Restart processes: python3 comprehensive_system_fix.py")
        if not api_ok:
            print("- Check API configuration and restart")
    
    return overall_success

def main():
    """Main diagnosis function"""
    print("🔍 GLOBAL SYSTEM DIAGNOSIS")
    print("="*50)
    
    # Run all checks
    env_ok = check_environment()
    services_ok = check_services()
    processes_ok = check_processes()
    ports_ok = check_ports()
    api_ok = test_api_functionality()
    webhook_url = check_webhook_url()
    error_handling_ok = check_error_handling()
    
    # Create report
    success = create_diagnosis_report(env_ok, services_ok, processes_ok, ports_ok, api_ok, webhook_url, error_handling_ok)
    
    # Save results
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    results = {
        "timestamp": timestamp,
        "environment": env_ok,
        "services": services_ok,
        "processes": processes_ok,
        "ports": ports_ok,
        "api_functionality": api_ok,
        "webhook_url": webhook_url,
        "error_handling": error_handling_ok,
        "overall_success": success
    }
    
    filename = f"global_diagnosis_{timestamp}.json"
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 Diagnosis results saved to: {filename}")
    
    return success

if __name__ == "__main__":
    main() 