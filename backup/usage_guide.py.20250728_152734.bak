from xai_flex_generator_fixed import XAIFlexGenerator
import json

def quick_test():
    """Quick test of the Flex Generator"""
    
    # Initialize generator
    flex_generator = XAIFlexGenerator()
    
    # Test data
    chunk = {
        "chunk_id": "test-01",
        "chunk_type": "warning_sign",
        "title": "記憶力測試",
        "content": "這是一個測試訊息，用來驗證 Flex Message 生成器是否正常運作。",
        "confidence_score": 0.85,
        "tags": ["測試", "範例"]
    }
    
    # Generate Flex Message
    flex_message = flex_generator.generate_enhanced_flex_message([chunk])
    
    print("✅ XAI Flex Message Generator Test Results:")
    print(f"📱 Alt Text: {flex_message['altText']}")
    print(f"🎨 Component Type: {flex_message['metadata']['component_type']}")
    print(f"🔧 Generated At: {flex_message['metadata']['generated_at']}")
    print(f"📦 Bubble Type: {flex_message['contents']['type']}")
    
    return flex_message

def test_all_types():
    """Test all 7 component types"""
    
    flex_generator = XAIFlexGenerator()
    
    test_cases = {
        "warning_sign": "⚠️ 警訊對比卡片",
        "bpsd_symptom": "📊 信心度量表", 
        "coping_strategy": "💡 XAI解釋盒",
        "legal_rights": "ℹ️ 資訊盒",
        "missing_prevention": "🎯 行動卡片",
        "stage_description": "📅 時間軸列表",
        "financial_safety": "🚨 警告盒"
    }
    
    print("\n=== Testing All 7 Component Types ===")
    
    for chunk_type, description in test_cases.items():
        try:
            chunk = {
                "chunk_id": f"test-{chunk_type}",
                "chunk_type": chunk_type,
                "title": f"測試{description}",
                "content": "這是測試內容" * 5,
                "confidence_score": 0.8
            }
            
            result = flex_generator.generate_enhanced_flex_message([chunk])
            component_type = result['metadata']['component_type']
            print(f"✅ {description} → {component_type}")
            
        except Exception as e:
            print(f"❌ {description} → Error: {e}")
    
    print("\n🎉 All tests completed!")

if __name__ == "__main__":
    print("🚀 Starting XAI Flex Message Generator Tests...\n")
    
    # Quick test
    quick_test()
    
    # Test all types
    test_all_types()
    
    print("\n✅ All examples completed successfully!")
