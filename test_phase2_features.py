#!/usr/bin/env python3
"""
Phase 2 Feature Testing Script
Tests GPU acceleration, XAI visualization, and non-linear navigation
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

def test_service_health():
    """Test all service health endpoints"""
    print("🏥 Testing Service Health...")
    
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
                if service_name == "RAG Service":
                    print(f"   🚀 GPU Available: {data.get('gpu_available', 'unknown')}")
                    print(f"   💻 Device: {data.get('device', 'unknown')}")
            else:
                print(f"❌ {service_name}: HTTP {response.status_code}")
        except Exception as e:
            print(f"❌ {service_name}: {str(e)}")

def test_gpu_acceleration():
    """Test GPU acceleration features"""
    print("\n🚀 Testing GPU Acceleration...")
    
    try:
        # Test GPU status
        response = requests.get(f"{RAG_URL}/gpu-status", timeout=10)
        if response.status_code == 200:
            gpu_data = response.json()
            print(f"✅ GPU Status: {gpu_data.get('device_name', 'unknown')}")
            print(f"   CUDA Available: {gpu_data.get('cuda_available', False)}")
            print(f"   GPU Count: {gpu_data.get('gpu_count', 0)}")
        else:
            print(f"❌ GPU Status: HTTP {response.status_code}")
    except Exception as e:
        print(f"❌ GPU Status: {str(e)}")
    
    # Test GPU-accelerated search
    try:
        search_data = {
            "query": "失智症早期症狀",
            "top_k": 3,
            "threshold": 0.5,
            "use_gpu": True
        }
        
        response = requests.post(f"{RAG_URL}/search", json=search_data, timeout=30)
        if response.status_code == 200:
            result = response.json()
            print(f"✅ GPU Search: {result.get('total_found', 0)} results")
            print(f"   Processing Time: {result.get('processing_time', 0):.3f}s")
            print(f"   GPU Used: {result.get('gpu_used', False)}")
            print(f"   Confidence: {result.get('confidence', 0):.2f}")
        else:
            print(f"❌ GPU Search: HTTP {response.status_code}")
    except Exception as e:
        print(f"❌ GPU Search: {str(e)}")

def test_xai_visualization():
    """Test XAI visualization features"""
    print("\n📊 Testing XAI Visualization...")
    
    try:
        # Test XAI features endpoint
        response = requests.get(f"{XAI_URL}/xai-features", timeout=10)
        if response.status_code == 200:
            features = response.json()
            print(f"✅ XAI Features: {len(features.get('features', []))} features available")
            print(f"   Modules: {', '.join(features.get('modules', []))}")
        else:
            print(f"❌ XAI Features: HTTP {response.status_code}")
    except Exception as e:
        print(f"❌ XAI Features: {str(e)}")
    
    # Test comprehensive analysis with visualization
    try:
        analysis_data = {
            "text": "爸爸經常忘記事情，有時候會迷路，情緒也不太穩定",
            "user_id": "test_user_001",
            "include_visualization": True
        }
        
        response = requests.post(f"{XAI_URL}/comprehensive-analysis", json=analysis_data, timeout=30)
        if response.status_code == 200:
            result = response.json()
            print(f"✅ XAI Analysis: {len(result.get('modules_used', []))} modules used")
            print(f"   Confidence: {result.get('confidence', 0):.2f}")
            print(f"   Visualization: {'Available' if result.get('visualization_data') else 'Not available'}")
            print(f"   Explanation Path: {len(result.get('explanation_path', []))} explanations")
            
            # Show explanation path
            for explanation in result.get('explanation_path', [])[:3]:
                print(f"   📝 {explanation}")
        else:
            print(f"❌ XAI Analysis: HTTP {response.status_code}")
    except Exception as e:
        print(f"❌ XAI Analysis: {str(e)}")

def test_non_linear_navigation():
    """Test non-linear navigation features"""
    print("\n🧭 Testing Non-linear Navigation...")
    
    try:
        # Test LINE Bot root endpoint
        response = requests.get(f"{LINE_BOT_URL}/", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ LINE Bot: {data.get('message', 'unknown')}")
            print(f"   Architecture: {data.get('architecture', 'unknown')}")
            print(f"   External URL: {data.get('external_url', 'unknown')}")
        else:
            print(f"❌ LINE Bot: HTTP {response.status_code}")
    except Exception as e:
        print(f"❌ LINE Bot: {str(e)}")
    
    # Test webhook URL endpoint
    try:
        response = requests.get(f"{LINE_BOT_URL}/webhook-url", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Webhook URL: {data.get('webhook_url', 'unknown')}")
        else:
            print(f"❌ Webhook URL: HTTP {response.status_code}")
    except Exception as e:
        print(f"❌ Webhook URL: {str(e)}")

def test_individual_modules():
    """Test individual module analysis"""
    print("\n🔍 Testing Individual Modules...")
    
    modules = ["M1", "M2", "M3", "M4"]
    test_texts = {
        "M1": "記憶力減退，經常忘記事情",
        "M2": "症狀已經進入中期階段",
        "M3": "出現妄想和幻覺症狀",
        "M4": "需要醫療資源和照護服務"
    }
    
    for module in modules:
        try:
            analysis_data = {
                "text": test_texts.get(module, f"測試{module}模組"),
                "user_id": f"test_user_{module}",
                "include_visualization": True
            }
            
            response = requests.post(f"{XAI_URL}/analyze/{module}", json=analysis_data, timeout=30)
            if response.status_code == 200:
                result = response.json()
                module_result = result.get('result', {})
                print(f"✅ {module}: {module_result.get('summary', 'No summary')}")
                print(f"   Confidence: {module_result.get('confidence', 0):.2f}")
                print(f"   XAI Enhanced: {result.get('xai_enhanced', False)}")
            else:
                print(f"❌ {module}: HTTP {response.status_code}")
        except Exception as e:
            print(f"❌ {module}: {str(e)}")

def test_knowledge_domains():
    """Test knowledge domain features"""
    print("\n📚 Testing Knowledge Domains...")
    
    try:
        # Test domains endpoint
        response = requests.get(f"{RAG_URL}/domains", timeout=10)
        if response.status_code == 200:
            data = response.json()
            domains = data.get('domains', [])
            descriptions = data.get('descriptions', {})
            print(f"✅ Knowledge Domains: {len(domains)} domains available")
            for domain in domains:
                desc = descriptions.get(domain, "No description")
                print(f"   📖 {domain}: {desc}")
        else:
            print(f"❌ Knowledge Domains: HTTP {response.status_code}")
    except Exception as e:
        print(f"❌ Knowledge Domains: {str(e)}")
    
    # Test specific domain
    try:
        response = requests.get(f"{RAG_URL}/knowledge/warning_signs", timeout=10)
        if response.status_code == 200:
            data = response.json()
            knowledge = data.get('knowledge', {})
            print(f"✅ Warning Signs: {len(knowledge)} items available")
        else:
            print(f"❌ Warning Signs: HTTP {response.status_code}")
    except Exception as e:
        print(f"❌ Warning Signs: {str(e)}")

def main():
    """Main testing function"""
    print("🧪 Phase 2 Feature Testing")
    print("=" * 50)
    print(f"⏰ Start Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Run all tests
    test_service_health()
    test_gpu_acceleration()
    test_xai_visualization()
    test_non_linear_navigation()
    test_individual_modules()
    test_knowledge_domains()
    
    print("\n" + "=" * 50)
    print(f"⏰ End Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("🎉 Phase 2 Testing Complete!")

if __name__ == "__main__":
    main() 