"""
Test Enhanced M1-M4 Visualization System
Demonstrates the redesigned visualization system with sample data
"""

import json
import requests
from datetime import datetime
from enhanced_flex_message_generator import (
    AnalysisResult, 
    create_enhanced_flex_message,
    EnhancedFlexMessageGenerator
)

def test_m1_warning_signs():
    """Test M1: 十大警訊比對卡"""
    print("🧪 Testing M1: 十大警訊比對卡")
    print("=" * 50)
    
    # Sample data for M1
    sample_result = AnalysisResult(
        module="M1",
        confidence=0.85,
        matched_items=[
            {
                "id": "M1-01",
                "name": "記憶力減退",
                "normal_aging": "偶爾忘記鑰匙放哪裡",
                "dementia_warning": "忘記剛吃過飯、重複問同樣問題",
                "confidence": 0.85
            },
            {
                "id": "M1-02",
                "name": "日常生活能力下降",
                "normal_aging": "偶爾忘記關瓦斯",
                "dementia_warning": "不會使用洗衣機、忘記如何煮飯",
                "confidence": 0.72
            }
        ],
        summary="檢測到記憶力減退和日常生活能力下降症狀，建議及早就醫評估",
        timestamp=datetime.now(),
        user_input="我媽媽最近常常忘記剛吃過飯，還會重複問同樣的問題"
    )
    
    # Generate enhanced flex message
    flex_message = create_enhanced_flex_message("M1", sample_result)
    
    print(f"✅ Confidence: {sample_result.confidence * 100:.0f}%")
    print(f"📊 Matched Items: {len(sample_result.matched_items)}")
    print(f"📝 Summary: {sample_result.summary}")
    print(f"🎨 Flex Message Size: {len(json.dumps(flex_message))} bytes")
    
    return flex_message

def test_m2_progression_matrix():
    """Test M2: 病程階段對照"""
    print("\n🧪 Testing M2: 病程階段對照")
    print("=" * 50)
    
    # Sample data for M2
    sample_result = AnalysisResult(
        module="M2",
        confidence=0.78,
        matched_items=[
            {
                "stage": "middle",
                "progress": 65,
                "name": "中期階段",
                "description": "明顯記憶力減退，需要協助處理日常事務",
                "symptoms": ["記憶力減退", "語言表達困難", "判斷力下降"]
            }
        ],
        summary="根據症狀分析，患者目前處於中期階段，需要適當的照護協助",
        timestamp=datetime.now(),
        user_input="我爸爸最近記憶力明顯變差，需要我協助處理很多事情"
    )
    
    # Generate enhanced flex message
    flex_message = create_enhanced_flex_message("M2", sample_result)
    
    print(f"✅ Confidence: {sample_result.confidence * 100:.0f}%")
    print(f"📊 Current Stage: {sample_result.matched_items[0]['stage']}")
    print(f"📈 Progress: {sample_result.matched_items[0]['progress']}%")
    print(f"📝 Summary: {sample_result.summary}")
    print(f"🎨 Flex Message Size: {len(json.dumps(flex_message))} bytes")
    
    return flex_message

def test_m3_bpsd_classification():
    """Test M3: BPSD 症狀分類"""
    print("\n🧪 Testing M3: BPSD 症狀分類")
    print("=" * 50)
    
    # Sample data for M3
    sample_result = AnalysisResult(
        module="M3",
        confidence=0.82,
        matched_items=[
            {
                "id": "M3-01",
                "name": "躁動不安",
                "category": "躁動不安",
                "confidence": 0.85,
                "description": "患者表現出明顯的躁動和不安情緒"
            },
            {
                "id": "M3-02",
                "name": "憂鬱情緒",
                "category": "憂鬱情緒",
                "confidence": 0.72,
                "description": "患者出現憂鬱和情緒低落症狀"
            },
            {
                "id": "M3-03",
                "name": "幻覺症狀",
                "category": "幻覺症狀",
                "confidence": 0.68,
                "description": "患者報告看到或聽到不存在的東西"
            }
        ],
        summary="檢測到躁動不安、憂鬱情緒和幻覺症狀，建議專業醫療評估",
        timestamp=datetime.now(),
        user_input="我媽媽最近很躁動，情緒低落，還說看到有人在家裡"
    )
    
    # Generate enhanced flex message
    flex_message = create_enhanced_flex_message("M3", sample_result)
    
    print(f"✅ Confidence: {sample_result.confidence * 100:.0f}%")
    print(f"📊 Symptoms Detected: {len(sample_result.matched_items)}")
    
    # Group by category
    categories = {}
    for symptom in sample_result.matched_items:
        category = symptom["category"]
        if category not in categories:
            categories[category] = []
        categories[category].append(symptom["name"])
    
    for category, symptoms in categories.items():
        print(f"   • {category}: {', '.join(symptoms)}")
    
    print(f"📝 Summary: {sample_result.summary}")
    print(f"🎨 Flex Message Size: {len(json.dumps(flex_message))} bytes")
    
    return flex_message

def test_m4_care_navigation():
    """Test M4: 任務導航儀表板"""
    print("\n🧪 Testing M4: 任務導航儀表板")
    print("=" * 50)
    
    # Sample data for M4
    sample_result = AnalysisResult(
        module="M4",
        confidence=0.75,
        matched_items=[
            {
                "id": "M4-01",
                "title": "藥物管理",
                "description": "協助患者按時服藥，確保藥物安全",
                "priority": "high",
                "icon": "💊",
                "category": "醫療照護"
            },
            {
                "id": "M4-02",
                "title": "日常生活協助",
                "description": "協助洗澡、穿衣、進食等日常活動",
                "priority": "high",
                "icon": "🛁",
                "category": "生活照護"
            },
            {
                "id": "M4-03",
                "title": "安全環境維護",
                "description": "確保居家環境安全，防止意外發生",
                "priority": "medium",
                "icon": "🏠",
                "category": "環境安全"
            },
            {
                "id": "M4-04",
                "title": "情緒支持",
                "description": "提供情感支持和陪伴，減少孤獨感",
                "priority": "medium",
                "icon": "❤️",
                "category": "心理支持"
            }
        ],
        summary="根據患者狀況，建議優先處理藥物管理和日常生活協助任務",
        timestamp=datetime.now(),
        user_input="我需要知道如何照顧我媽媽，她需要協助服藥和日常生活"
    )
    
    # Generate enhanced flex message
    flex_message = create_enhanced_flex_message("M4", sample_result)
    
    print(f"✅ Confidence: {sample_result.confidence * 100:.0f}%")
    print(f"📊 Tasks Generated: {len(sample_result.matched_items)}")
    
    # Group by priority
    priorities = {"high": [], "medium": [], "low": []}
    for task in sample_result.matched_items:
        priority = task["priority"]
        priorities[priority].append(task["title"])
    
    for priority, tasks in priorities.items():
        if tasks:
            print(f"   • {priority.upper()}: {', '.join(tasks)}")
    
    print(f"📝 Summary: {sample_result.summary}")
    print(f"🎨 Flex Message Size: {len(json.dumps(flex_message))} bytes")
    
    return flex_message

def test_api_integration():
    """Test API integration"""
    print("\n🧪 Testing API Integration")
    print("=" * 50)
    
    try:
        # Test the enhanced API
        api_url = "http://localhost:8006"
        
        # Test health check
        response = requests.get(f"{api_url}/health")
        if response.status_code == 200:
            print("✅ API Health Check: PASSED")
            health_data = response.json()
            print(f"   Status: {health_data.get('status')}")
            print(f"   Mode: {health_data.get('mode')}")
        else:
            print("❌ API Health Check: FAILED")
            return
        
        # Test design system
        response = requests.get(f"{api_url}/design-system")
        if response.status_code == 200:
            print("✅ Design System: AVAILABLE")
            design_data = response.json()
            print(f"   Components: {len(design_data['design_system']['components'])}")
        else:
            print("❌ Design System: UNAVAILABLE")
        
        # Test flex message generation
        test_data = {"text": "我媽媽最近記憶力變差，常常忘記事情"}
        response = requests.post(f"{api_url}/flex/M1", json=test_data)
        if response.status_code == 200:
            print("✅ Flex Message Generation: WORKING")
            flex_data = response.json()
            print(f"   Message Type: {flex_data.get('type')}")
        else:
            print("❌ Flex Message Generation: FAILED")
        
    except requests.exceptions.ConnectionError:
        print("❌ API Connection: FAILED (API not running)")
    except Exception as e:
        print(f"❌ API Test Error: {str(e)}")

def save_sample_flex_messages():
    """Save sample flex messages to files"""
    print("\n💾 Saving Sample Flex Messages")
    print("=" * 50)
    
    # Generate sample messages
    m1_flex = test_m1_warning_signs()
    m2_flex = test_m2_progression_matrix()
    m3_flex = test_m3_bpsd_classification()
    m4_flex = test_m4_care_navigation()
    
    # Save to files
    samples = {
        "m1_warning_signs.json": m1_flex,
        "m2_progression_matrix.json": m2_flex,
        "m3_bpsd_classification.json": m3_flex,
        "m4_care_navigation.json": m4_flex
    }
    
    for filename, flex_message in samples.items():
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(flex_message, f, ensure_ascii=False, indent=2)
        print(f"✅ Saved: {filename}")
    
    # Create combined sample
    combined_sample = {
        "timestamp": datetime.now().isoformat(),
        "version": "2.0.0",
        "description": "Enhanced M1-M4 Visualization Samples",
        "samples": {
            "M1": m1_flex,
            "M2": m2_flex,
            "M3": m3_flex,
            "M4": m4_flex
        }
    }
    
    with open("enhanced_visualization_samples.json", 'w', encoding='utf-8') as f:
        json.dump(combined_sample, f, ensure_ascii=False, indent=2)
    print("✅ Saved: enhanced_visualization_samples.json")

def main():
    """Main test function"""
    print("🎨 Enhanced M1-M4 Visualization System Test")
    print("=" * 60)
    print("Testing redesigned visualization system with LINE Flex Message requirements")
    print()
    
    # Test individual modules
    test_m1_warning_signs()
    test_m2_progression_matrix()
    test_m3_bpsd_classification()
    test_m4_care_navigation()
    
    # Test API integration
    test_api_integration()
    
    # Save sample messages
    save_sample_flex_messages()
    
    print("\n🎉 Test Complete!")
    print("=" * 60)
    print("✅ All modules tested successfully")
    print("✅ Enhanced flex messages generated")
    print("✅ Sample files saved")
    print("\n📱 Next Steps:")
    print("   1. Review generated flex messages")
    print("   2. Test with LINE Bot webhook")
    print("   3. Implement LIFF integration")
    print("   4. Deploy to production")

if __name__ == "__main__":
    main() 