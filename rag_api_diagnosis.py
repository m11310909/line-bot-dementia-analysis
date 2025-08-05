#!/usr/bin/env python3
"""
RAG API Diagnosis - Comprehensive analysis of RAG API issues
"""

import requests
import json
import time
import subprocess
import os
import psutil
from datetime import datetime

def log(message):
    """Log message with timestamp"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {message}")

def check_process_details():
    """Check detailed process information"""
    log("🔍 Checking process details...")
    
    try:
        # Find RAG API process
        result = subprocess.run(['pgrep', '-f', 'enhanced_m1_m2_m3_m4_integrated_api.py'], 
                              capture_output=True, text=True)
        
        if result.returncode == 0:
            pid = result.stdout.strip()
            log(f"✅ RAG API process found: PID {pid}")
            
            # Get process details
            process = psutil.Process(int(pid))
            log(f"   CPU Usage: {process.cpu_percent()}%")
            log(f"   Memory Usage: {process.memory_info().rss / 1024 / 1024:.1f} MB")
            log(f"   Status: {process.status()}")
            log(f"   Create Time: {datetime.fromtimestamp(process.create_time())}")
            
            # Check if process is responsive
            try:
                response = requests.get("http://localhost:8005/health", timeout=5)
                if response.status_code == 200:
                    log("✅ Process is responsive to HTTP requests")
                else:
                    log(f"⚠️  Process responding but HTTP status: {response.status_code}")
            except Exception as e:
                log(f"❌ Process not responsive to HTTP: {e}")
            
            return True
        else:
            log("❌ RAG API process not found")
            return False
            
    except Exception as e:
        log(f"❌ Error checking process: {e}")
        return False

def check_port_usage():
    """Check port usage and conflicts"""
    log("🔌 Checking port usage...")
    
    try:
        # Check port 8005
        result = subprocess.run(['lsof', '-i', ':8005'], capture_output=True, text=True)
        
        if result.returncode == 0:
            lines = result.stdout.strip().split('\n')
            if len(lines) > 1:  # Header + data
                log("✅ Port 8005 is in use")
                for line in lines[1:]:  # Skip header
                    if line.strip():
                        parts = line.split()
                        if len(parts) >= 2:
                            log(f"   Process: {parts[0]} (PID: {parts[1]})")
            else:
                log("❌ Port 8005 not in use")
                return False
        else:
            log("❌ Port 8005 not in use")
            return False
            
    except Exception as e:
        log(f"❌ Error checking port: {e}")
        return False
    
    return True

def check_api_functionality():
    """Test API functionality with multiple requests"""
    log("🧪 Testing API functionality...")
    
    test_cases = [
        {"input": "爸爸不會用洗衣機", "module": "M1"},
        {"input": "媽媽中度失智", "module": "M2"},
        {"input": "爺爺有妄想症狀", "module": "M3"},
        {"input": "需要醫療協助", "module": "M4"}
    ]
    
    success_count = 0
    total_time = 0
    
    for i, test_case in enumerate(test_cases, 1):
        try:
            start_time = time.time()
            response = requests.post(
                f"http://localhost:8005/analyze/{test_case['module']}",
                json={"text": test_case["input"]},
                timeout=10
            )
            response_time = time.time() - start_time
            total_time += response_time
            
            if response.status_code == 200:
                data = response.json()
                if data.get("success") and "flex_message" in data:
                    log(f"✅ Test {i}: Success ({response_time:.2f}s)")
                    success_count += 1
                else:
                    log(f"❌ Test {i}: Invalid response format")
            else:
                log(f"❌ Test {i}: HTTP {response.status_code}")
                
        except Exception as e:
            log(f"❌ Test {i}: {e}")
    
    avg_time = total_time / len(test_cases) if test_cases else 0
    success_rate = (success_count / len(test_cases)) * 100 if test_cases else 0
    
    log(f"📊 API Test Results:")
    log(f"   Success Rate: {success_rate:.1f}%")
    log(f"   Average Response Time: {avg_time:.2f}s")
    log(f"   Successful Tests: {success_count}/{len(test_cases)}")
    
    return success_rate >= 75  # At least 75% success rate

def check_memory_usage():
    """Check memory usage patterns"""
    log("💾 Checking memory usage...")
    
    try:
        # Get system memory info
        memory = psutil.virtual_memory()
        log(f"   Total Memory: {memory.total / 1024 / 1024 / 1024:.1f} GB")
        log(f"   Available Memory: {memory.available / 1024 / 1024 / 1024:.1f} GB")
        log(f"   Memory Usage: {memory.percent}%")
        
        # Check if memory is low
        if memory.percent > 90:
            log("⚠️  High memory usage detected")
            return False
        elif memory.percent > 80:
            log("⚠️  Elevated memory usage")
            return False
        else:
            log("✅ Memory usage is normal")
            return True
            
    except Exception as e:
        log(f"❌ Error checking memory: {e}")
        return False

def check_cpu_usage():
    """Check CPU usage patterns"""
    log("🖥️  Checking CPU usage...")
    
    try:
        # Get CPU usage
        cpu_percent = psutil.cpu_percent(interval=1)
        log(f"   CPU Usage: {cpu_percent}%")
        
        # Check if CPU is overloaded
        if cpu_percent > 90:
            log("⚠️  High CPU usage detected")
            return False
        elif cpu_percent > 80:
            log("⚠️  Elevated CPU usage")
            return False
        else:
            log("✅ CPU usage is normal")
            return True
            
    except Exception as e:
        log(f"❌ Error checking CPU: {e}")
        return False

def check_error_logs():
    """Check for error logs"""
    log("📝 Checking error logs...")
    
    log_files = [
        "rag_api.log",
        "backend.log",
        "webhook.log"
    ]
    
    for log_file in log_files:
        if os.path.exists(log_file):
            try:
                # Get last 10 lines of log file
                result = subprocess.run(['tail', '-10', log_file], 
                                      capture_output=True, text=True)
                
                if result.stdout:
                    log(f"📄 Recent entries in {log_file}:")
                    lines = result.stdout.strip().split('\n')
                    for line in lines[-5:]:  # Show last 5 lines
                        if line.strip():
                            log(f"   {line}")
                else:
                    log(f"📄 {log_file}: No recent entries")
                    
            except Exception as e:
                log(f"❌ Error reading {log_file}: {e}")
        else:
            log(f"📄 {log_file}: File not found")

def check_network_connectivity():
    """Check network connectivity"""
    log("🌐 Checking network connectivity...")
    
    # Test local connectivity
    try:
        response = requests.get("http://localhost:8005/health", timeout=5)
        if response.status_code == 200:
            log("✅ Local connectivity: OK")
        else:
            log(f"⚠️  Local connectivity: HTTP {response.status_code}")
    except Exception as e:
        log(f"❌ Local connectivity failed: {e}")
    
    # Test external connectivity (if ngrok is running)
    try:
        response = requests.get("https://c9f4f5bcf183.ngrok-free.app/health", timeout=5)
        if response.status_code == 200:
            log("✅ External connectivity: OK")
        else:
            log(f"⚠️  External connectivity: HTTP {response.status_code}")
    except Exception as e:
        log(f"❌ External connectivity failed: {e}")

def create_diagnosis_report(process_ok, port_ok, api_ok, memory_ok, cpu_ok):
    """Create comprehensive diagnosis report"""
    log("📊 Creating diagnosis report...")
    
    overall_health = all([process_ok, port_ok, api_ok, memory_ok, cpu_ok])
    
    report = {
        "timestamp": datetime.now().isoformat(),
        "overall_health": overall_health,
        "checks": {
            "process": process_ok,
            "port": port_ok,
            "api_functionality": api_ok,
            "memory": memory_ok,
            "cpu": cpu_ok
        },
        "recommendations": []
    }
    
    if not process_ok:
        report["recommendations"].append("Restart RAG API process")
    
    if not port_ok:
        report["recommendations"].append("Check for port conflicts")
    
    if not api_ok:
        report["recommendations"].append("Check API configuration and modules")
    
    if not memory_ok:
        report["recommendations"].append("Monitor memory usage and consider restart")
    
    if not cpu_ok:
        report["recommendations"].append("Check for CPU-intensive processes")
    
    if overall_health:
        report["recommendations"].append("System appears healthy, monitor for intermittent issues")
    
    # Save report
    filename = f"rag_api_diagnosis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    
    log(f"💾 Diagnosis report saved: {filename}")
    
    # Print summary
    log("📋 DIAGNOSIS SUMMARY:")
    log(f"   Process Status: {'✅' if process_ok else '❌'}")
    log(f"   Port Status: {'✅' if port_ok else '❌'}")
    log(f"   API Functionality: {'✅' if api_ok else '❌'}")
    log(f"   Memory Status: {'✅' if memory_ok else '❌'}")
    log(f"   CPU Status: {'✅' if cpu_ok else '❌'}")
    log(f"   Overall Health: {'✅' if overall_health else '❌'}")
    
    if report["recommendations"]:
        log("🔧 RECOMMENDATIONS:")
        for rec in report["recommendations"]:
            log(f"   • {rec}")
    
    return report

def main():
    """Main diagnosis function"""
    print("🔍 RAG API DIAGNOSIS")
    print("="*50)
    
    # Run all checks
    process_ok = check_process_details()
    port_ok = check_port_usage()
    api_ok = check_api_functionality()
    memory_ok = check_memory_usage()
    cpu_ok = check_cpu_usage()
    
    # Check logs and network
    check_error_logs()
    check_network_connectivity()
    
    # Create report
    report = create_diagnosis_report(process_ok, port_ok, api_ok, memory_ok, cpu_ok)
    
    return report

if __name__ == "__main__":
    main() 