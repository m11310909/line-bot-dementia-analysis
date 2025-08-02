#!/usr/bin/env python3
"""
Complete System Testing Script
Tests all phases (1, 2, 3) in one comprehensive test
"""

import requests
import json
import time
import os
from datetime import datetime

# Configuration
BASE_URL = "http://localhost"
LINE_BOT_URL = f"{BASE_URL}:8081"
XAI_URL = f"{BASE_URL}:8005"
RAG_URL = f"{BASE_URL}:8006"
ASPECT_VERIFIERS_URL = f"{BASE_URL}:8007"
BON_MAV_URL = f"{BASE_URL}:8008"
MONITORING_URL = f"{BASE_URL}:8009"

def test_phase1_features():
    """Test Phase 1: Basic Infrastructure"""
    print("🏗️  Testing Phase 1: Basic Infrastructure...")
    
    # Test basic services
    services = {
        "LINE Bot": f"{LINE_BOT_URL}/health",
        "XAI Analysis": f"{XAI_URL}/health",
        "RAG Service": f"{RAG_URL}/health"
    }
    
    for service_name, url in services.items():
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                data = response.json()
                print(f"✅ {service_name}: {data.get('status', 'unknown')}")
            else:
                print(f"❌ {service_name}: HTTP {response.status_code}")
        except Exception as e:
            print(f"❌ {service_name}: {str(e)}")

def test_phase2_features():
    """Test Phase 2: GPU Acceleration & Enhanced Features"""
    print("\n🚀 Testing Phase 2: GPU Acceleration & Enhanced Features...")
    
    # Test GPU acceleration
    try:
        response = requests.get(f"{RAG_URL}/gpu-status", timeout=10)
        if response.status_code == 200:
            gpu_data = response.json()
            print(f"✅ GPU Status: {gpu_data.get('device_name', 'unknown')}")
            print(f"   CUDA Available: {gpu_data.get('cuda_available', False)}")
        else:
            print(f"❌ GPU Status: HTTP {response.status_code}")
    except Exception as e:
        print(f"❌ GPU Status: {str(e)}")
    
    # Test XAI features
    try:
        response = requests.get(f"{XAI_URL}/xai-features", timeout=10)
        if response.status_code == 200:
            features = response.json()
            print(f"✅ XAI Features: {len(features.get('features', []))} features available")
        else:
            print(f"❌ XAI Features: HTTP {response.status_code}")
    except Exception as e:
        print(f"❌ XAI Features: {str(e)}")

def test_phase3_features():
    """Test Phase 3: Advanced Features"""
    print("\n🔍 Testing Phase 3: Advanced Features...")
    
    # Test Aspect Verifiers
    try:
        response = requests.get(f"{ASPECT_VERIFIERS_URL}/aspects", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Aspect Verifiers: {len(data.get('aspects', []))} aspects available")
        else:
            print(f"❌ Aspect Verifiers: HTTP {response.status_code}")
    except Exception as e:
        print(f"❌ Aspect Verifiers: {str(e)}")
    
    # Test BoN-MAV
    try:
        response = requests.get(f"{BON_MAV_URL}/networks", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ BoN-MAV: {len(data.get('networks', []))} networks available")
        else:
            print(f"❌ BoN-MAV: HTTP {response.status_code}")
    except Exception as e:
        print(f"❌ BoN-MAV: {str(e)}")
    
    # Test Monitoring
    try:
        response = requests.get(f"{MONITORING_URL}/services/health", timeout=10)
        if response.status_code == 200:
            data = response.json()
            services = data.get('services', {})
            print(f"✅ Monitoring: {len(services)} services monitored")
        else:
            print(f"❌ Monitoring: HTTP {response.status_code}")
    except Exception as e:
        print(f"❌ Monitoring: {str(e)}")

def test_integrated_workflow():
    """Test complete integrated workflow"""
    print("\n🔗 Testing Complete Integrated Workflow...")
    
    test_text = "爸爸最近經常忘記關瓦斯，語言表達也有困難，情緒不太穩定"
    
    try:
        # Step 1: Aspect Verification
        print("📋 Step 1: Aspect Verification")
        verification_data = {
            "text": test_text,
            "user_id": "test_user_complete",
            "aspects": ["symptom", "severity", "urgency", "context"]
        }
        
        response = requests.post(f"{ASPECT_VERIFIERS_URL}/verify", json=verification_data, timeout=30)
        if response.status_code == 200:
            verification_result = response.json()
            print(f"   ✅ Verification Score: {verification_result.get('verification_score', 0):.2f}")
        else:
            print(f"   ❌ Verification failed: HTTP {response.status_code}")
            return
        
        # Step 2: BoN-MAV Validation
        print("🌐 Step 2: BoN-MAV Validation")
        mav_data = {
            "text": test_text,
            "user_id": "test_user_complete",
            "networks": ["symptom", "severity", "context", "temporal"],
            "validation_mode": "ensemble"
        }
        
        response = requests.post(f"{BON_MAV_URL}/validate", json=mav_data, timeout=30)
        if response.status_code == 200:
            mav_result = response.json()
            print(f"   ✅ Validation Score: {mav_result.get('validation_score', 0):.2f}")
        else:
            print(f"   ❌ MAV validation failed: HTTP {response.status_code}")
            return
        
        # Step 3: XAI Analysis
        print("🧠 Step 3: XAI Analysis")
        analysis_data = {
            "text": test_text,
            "user_id": "test_user_complete",
            "include_visualization": True
        }
        
        response = requests.post(f"{XAI_URL}/comprehensive-analysis", json=analysis_data, timeout=30)
        if response.status_code == 200:
            analysis_result = response.json()
            print(f"   ✅ Analysis Confidence: {analysis_result.get('confidence', 0):.2f}")
        else:
            print(f"   ❌ Analysis failed: HTTP {response.status_code}")
            return
        
        # Step 4: RAG Knowledge Search
        print("📚 Step 4: RAG Knowledge Search")
        rag_data = {
            "query": "失智症早期症狀照護",
            "top_k": 3,
            "threshold": 0.5,
            "use_gpu": True
        }
        
        response = requests.post(f"{RAG_URL}/search", json=rag_data, timeout=30)
        if response.status_code == 200:
            rag_result = response.json()
            print(f"   ✅ RAG Results: {rag_result.get('total_found', 0)} found")
        else:
            print(f"   ❌ RAG search failed: HTTP {response.status_code}")
            return
        
        # Final Summary
        print("\n🎯 Complete System Test Summary:")
        print(f"   Aspect Verification: {verification_result.get('verification_score', 0):.2f}")
        print(f"   BoN-MAV Validation: {mav_result.get('validation_score', 0):.2f}")
        print(f"   XAI Analysis: {analysis_result.get('confidence', 0):.2f}")
        print(f"   RAG Knowledge: {rag_result.get('total_found', 0)} results")
        
        # Calculate overall score
        overall_score = (
            verification_result.get('verification_score', 0) * 0.25 +
            mav_result.get('validation_score', 0) * 0.25 +
            analysis_result.get('confidence', 0) * 0.3 +
            min(rag_result.get('total_found', 0) / 3.0, 1.0) * 0.2
        )
        print(f"   Overall Score: {overall_score:.2f}")
        
        if overall_score >= 0.7:
            print("🎉 System Test: PASSED")
        else:
            print("⚠️  System Test: NEEDS ATTENTION")
        
    except Exception as e:
        print(f"❌ Integrated Workflow: {str(e)}")

def test_environment_check():
    """Check environment and credentials"""
    print("🔧 Environment & Credentials Check...")
    
    # Check .env file
    env_file = ".env"
    if os.path.exists(env_file):
        print(f"✅ .env file exists")
        
        # Check required environment variables
        required_vars = [
            "LINE_CHANNEL_ACCESS_TOKEN",
            "LINE_CHANNEL_SECRET",
            "EXTERNAL_URL"
        ]
        
        with open(env_file, 'r') as f:
            env_content = f.read()
            
        for var in required_vars:
            if var in env_content:
                print(f"✅ {var}: Configured")
            else:
                print(f"❌ {var}: Missing")
    else:
        print(f"❌ .env file not found")
    
    # Check Docker
    try:
        import subprocess
        result = subprocess.run(['docker', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Docker: {result.stdout.strip()}")
        else:
            print("❌ Docker: Not available")
    except Exception as e:
        print(f"❌ Docker: {str(e)}")
    
    # Check Docker Compose
    try:
        result = subprocess.run(['docker-compose', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Docker Compose: {result.stdout.strip()}")
        else:
            print("❌ Docker Compose: Not available")
    except Exception as e:
        print(f"❌ Docker Compose: {str(e)}")

def main():
    """Main testing function"""
    print("🧪 Complete System Testing")
    print("=" * 60)
    print(f"⏰ Start Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Environment check
    test_environment_check()
    
    # Test all phases
    test_phase1_features()
    test_phase2_features()
    test_phase3_features()
    test_integrated_workflow()
    
    print("\n" + "=" * 60)
    print(f"⏰ End Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("🎉 Complete System Testing Finished!")

if __name__ == "__main__":
    main() 