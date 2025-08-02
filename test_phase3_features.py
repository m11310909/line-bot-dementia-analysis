#!/usr/bin/env python3
"""
Phase 3 Feature Testing Script
Tests Aspect Verifiers, BoN-MAV, LIFF integration, and monitoring
"""

import requests
import json
import time
from datetime import datetime

# Configuration
BASE_URL = "http://localhost"
LINE_BOT_URL = f"{BASE_URL}:8081"
XAI_URL = f"{BASE_URL}:8005"
RAG_URL = f"{BASE_URL}:8006"
ASPECT_VERIFIERS_URL = f"{BASE_URL}:8007"
BON_MAV_URL = f"{BASE_URL}:8008"
MONITORING_URL = f"{BASE_URL}:8009"

def test_aspect_verifiers():
    """Test Aspect Verifiers service"""
    print("🔍 Testing Aspect Verifiers...")
    
    try:
        # Test aspects endpoint
        response = requests.get(f"{ASPECT_VERIFIERS_URL}/aspects", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Aspect Verifiers: {len(data.get('aspects', []))} aspects available")
            for aspect, desc in data.get('descriptions', {}).items():
                print(f"   📋 {aspect}: {desc}")
        else:
            print(f"❌ Aspect Verifiers: HTTP {response.status_code}")
    except Exception as e:
        print(f"❌ Aspect Verifiers: {str(e)}")
    
    # Test verification
    try:
        verification_data = {
            "text": "爸爸經常忘記事情，有時候會迷路，情緒也不太穩定",
            "user_id": "test_user_001",
            "aspects": ["symptom", "severity", "urgency", "context"]
        }
        
        response = requests.post(f"{ASPECT_VERIFIERS_URL}/verify", json=verification_data, timeout=30)
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Verification: {result.get('verified_count', 0)}/{result.get('total_aspects', 0)} aspects verified")
            print(f"   Overall Confidence: {result.get('overall_confidence', 0):.2f}")
            print(f"   Verification Score: {result.get('verification_score', 0):.2f}")
            
            for aspect, data in result.get('verified_aspects', {}).items():
                status = "✅" if data.get('verified') else "❌"
                confidence = data.get('confidence', 0)
                print(f"   {status} {aspect}: {confidence:.2f}")
        else:
            print(f"❌ Verification: HTTP {response.status_code}")
    except Exception as e:
        print(f"❌ Verification: {str(e)}")

def test_bon_mav():
    """Test BoN-MAV service"""
    print("\n🌐 Testing BoN-MAV...")
    
    try:
        # Test networks endpoint
        response = requests.get(f"{BON_MAV_URL}/networks", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ BoN-MAV: {len(data.get('networks', []))} networks available")
            for network, desc in data.get('descriptions', {}).items():
                print(f"   🌐 {network}: {desc}")
        else:
            print(f"❌ BoN-MAV: HTTP {response.status_code}")
    except Exception as e:
        print(f"❌ BoN-MAV: {str(e)}")
    
    # Test validation
    try:
        mav_data = {
            "text": "媽媽最近經常忘記關瓦斯，語言表達也有困難",
            "user_id": "test_user_001",
            "networks": ["symptom", "severity", "context", "temporal"],
            "validation_mode": "ensemble"
        }
        
        response = requests.post(f"{BON_MAV_URL}/validate", json=mav_data, timeout=30)
        if response.status_code == 200:
            result = response.json()
            print(f"✅ MAV Validation: {result.get('validated_count', 0)}/{result.get('total_networks', 0)} networks validated")
            print(f"   Validation Score: {result.get('validation_score', 0):.2f}")
            print(f"   Mode: {result.get('mode', 'unknown')}")
            
            ensemble_result = result.get('ensemble_result', {})
            print(f"   Ensemble Confidence: {ensemble_result.get('ensemble_confidence', 0):.2f}")
            print(f"   Ensemble Validated: {ensemble_result.get('ensemble_validated', False)}")
        else:
            print(f"❌ MAV Validation: HTTP {response.status_code}")
    except Exception as e:
        print(f"❌ MAV Validation: {str(e)}")

def test_monitoring():
    """Test monitoring service"""
    print("\n📊 Testing Monitoring...")
    
    try:
        # Test services health
        response = requests.get(f"{MONITORING_URL}/services/health", timeout=10)
        if response.status_code == 200:
            data = response.json()
            services = data.get('services', {})
            print(f"✅ Monitoring: {len(services)} services monitored")
            
            for service_name, health in services.items():
                status = "✅" if health.get('status') == 'healthy' else "❌"
                response_time = health.get('response_time', 0)
                print(f"   {status} {service_name}: {response_time:.3f}s")
        else:
            print(f"❌ Services Health: HTTP {response.status_code}")
    except Exception as e:
        print(f"❌ Services Health: {str(e)}")
    
    # Test system metrics
    try:
        response = requests.get(f"{MONITORING_URL}/system/metrics", timeout=10)
        if response.status_code == 200:
            data = response.json()
            metrics = data.get('metrics', {})
            print(f"✅ System Metrics:")
            print(f"   CPU Usage: {metrics.get('cpu_usage', 0):.1f}%")
            print(f"   Memory Usage: {metrics.get('memory_usage', 0):.1f}%")
            print(f"   Disk Usage: {metrics.get('disk_usage', 0):.1f}%")
            print(f"   Active Connections: {metrics.get('active_connections', 0)}")
        else:
            print(f"❌ System Metrics: HTTP {response.status_code}")
    except Exception as e:
        print(f"❌ System Metrics: {str(e)}")
    
    # Test performance summary
    try:
        response = requests.get(f"{MONITORING_URL}/performance/summary", timeout=10)
        if response.status_code == 200:
            data = response.json()
            summary = data.get('summary', {})
            print(f"✅ Performance Summary:")
            print(f"   Service Health: {summary.get('service_health_percentage', 0):.1f}%")
            print(f"   Active Alerts: {summary.get('active_alerts', 0)}")
            print(f"   Total Alerts: {summary.get('total_alerts', 0)}")
        else:
            print(f"❌ Performance Summary: HTTP {response.status_code}")
    except Exception as e:
        print(f"❌ Performance Summary: {str(e)}")

def test_integrated_analysis():
    """Test integrated analysis with all Phase 3 services"""
    print("\n🔗 Testing Integrated Analysis...")
    
    test_text = "爸爸最近經常忘記關瓦斯，語言表達也有困難，情緒不太穩定"
    
    try:
        # Step 1: Aspect Verification
        print("📋 Step 1: Aspect Verification")
        verification_data = {
            "text": test_text,
            "user_id": "test_user_integrated",
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
            "user_id": "test_user_integrated",
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
            "user_id": "test_user_integrated",
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
        
        # Summary
        print("\n🎯 Integrated Analysis Summary:")
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
        
    except Exception as e:
        print(f"❌ Integrated Analysis: {str(e)}")

def test_service_health():
    """Test health of all Phase 3 services"""
    print("🏥 Testing Phase 3 Service Health...")
    
    services = {
        "Aspect Verifiers": f"{ASPECT_VERIFIERS_URL}/health",
        "BoN-MAV": f"{BON_MAV_URL}/health",
        "Monitoring": f"{MONITORING_URL}/health"
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

def main():
    """Main testing function"""
    print("🧪 Phase 3 Feature Testing")
    print("=" * 50)
    print(f"⏰ Start Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Run all tests
    test_service_health()
    test_aspect_verifiers()
    test_bon_mav()
    test_monitoring()
    test_integrated_analysis()
    
    print("\n" + "=" * 50)
    print(f"⏰ End Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("🎉 Phase 3 Testing Complete!")

if __name__ == "__main__":
    main() 