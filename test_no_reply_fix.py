#!/usr/bin/env python3
"""
Test No Reply Fix - Comprehensive verification
"""

import requests
import json
import time
import subprocess
import os

def test_services():
    """Test all services are running"""
    print("🧪 Testing Services")
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
        },
        {
            "name": "ngrok Tunnel",
            "url": "https://85ddf115fba0.ngrok-free.app/health",
            "expected": "healthy"
        }
    ]
    
    all_healthy = True
    
    for service in services:
        try:
            response = requests.get(service["url"], timeout=10)
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

def test_analysis_api():
    """Test the analysis API directly"""
    print("\n🧪 Testing Analysis API")
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
            response = requests.post(
                f"http://localhost:8005/analyze/{test_case['module']}",
                json={"text": test_case["input"]},
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                success = data.get("success", False)
                has_flex = "flex_message" in data
                
                if success and has_flex:
                    print(f"✅ {test_case['description']}: Success")
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

def test_webhook_endpoint():
    """Test webhook endpoint"""
    print("\n🧪 Testing Webhook Endpoint")
    print("="*40)
    
    try:
        response = requests.get("https://85ddf115fba0.ngrok-free.app/health", timeout=10)
        if response.status_code == 200:
            print("✅ Webhook endpoint accessible")
            return True
        else:
            print(f"❌ Webhook endpoint: HTTP {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Webhook endpoint: {e}")
        return False

def check_processes():
    """Check if required processes are running"""
    print("\n🧪 Checking Processes")
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

def create_test_report(services_ok, analysis_ok, webhook_ok, processes_ok):
    """Create test report"""
    print("\n📊 Test Report")
    print("="*40)
    
    overall_success = all([services_ok, analysis_ok, webhook_ok, processes_ok])
    
    print(f"✅ Services: {'OK' if services_ok else 'FAILED'}")
    print(f"✅ Analysis API: {'OK' if analysis_ok else 'FAILED'}")
    print(f"✅ Webhook Endpoint: {'OK' if webhook_ok else 'FAILED'}")
    print(f"✅ Processes: {'OK' if processes_ok else 'FAILED'}")
    
    print(f"\n🎯 Overall Status: {'✅ PASSED' if overall_success else '❌ FAILED'}")
    
    if overall_success:
        print("\n🎉 NO REPLY ISSUE RESOLVED!")
        print("📱 Your LINE Bot should now respond to messages.")
        print("\n📋 Next Steps:")
        print("1. Update LINE Developer Console webhook URL")
        print("2. Test with message: '爸爸不會用洗衣機'")
        print("3. Check bot responses")
    else:
        print("\n⚠️  Issues detected. Run: python3 no_reply_final_fix.py")
    
    return overall_success

def main():
    """Main test function"""
    print("🎯 NO REPLY FIX VERIFICATION")
    print("="*50)
    
    # Run all tests
    services_ok = test_services()
    analysis_ok = test_analysis_api()
    webhook_ok = test_webhook_endpoint()
    processes_ok = check_processes()
    
    # Create report
    success = create_test_report(services_ok, analysis_ok, webhook_ok, processes_ok)
    
    # Save results
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    results = {
        "timestamp": timestamp,
        "services": services_ok,
        "analysis": analysis_ok,
        "webhook": webhook_ok,
        "processes": processes_ok,
        "overall_success": success
    }
    
    filename = f"no_reply_test_results_{timestamp}.json"
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 Results saved to: {filename}")
    
    return success

if __name__ == "__main__":
    main() 