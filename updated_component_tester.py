#!/usr/bin/env python3
import requests
import json
import time

# Correct API endpoint
FLEX_API_URL = "http://localhost:8001/api/v1/flex-message"

def test_component(user_input, component_name):
    """Test a specific component"""
    print(f"\n🧪 Testing {component_name}")
    print(f"📝 Input: {user_input}")
    
    payload = {"user_input": user_input}
    
    try:
        response = requests.post(FLEX_API_URL, json=payload, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            
            # Check if specific components are present in response
            flex_content = json.dumps(result, indent=2, ensure_ascii=False)
            
            components_found = []
            if "comparison_card" in flex_content or "正常老化" in flex_content:
                components_found.append("⚠️ comparison_card")
            if "confidence_meter" in flex_content or "信心度" in flex_content:
                components_found.append("📊 confidence_meter")
            if "xai_box" in flex_content or "分析說明" in flex_content:
                components_found.append("💡 xai_box")
            if "info_box" in flex_content or "資訊" in flex_content:
                components_found.append("ℹ️ info_box")
            if "action_card" in flex_content or "建議" in flex_content:
                components_found.append("🎯 action_card")
            if "timeline_list" in flex_content or "時間" in flex_content:
                components_found.append("📅 timeline_list")
            if "warning_box" in flex_content or "警告" in flex_content:
                components_found.append("🚨 warning_box")
            
            print(f"✅ Components detected: {', '.join(components_found) if components_found else 'Basic response'}")
            print(f"📄 Response length: {len(flex_content)} characters")
            
            # Save response for inspection
            filename = f"component_{component_name.replace(' ', '_')}.json"
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(result, f, indent=2, ensure_ascii=False)
            print(f"💾 Saved to: {filename}")
            
        else:
            print(f"❌ Error: {response.status_code} - {response.text}")
    
    except Exception as e:
        print(f"❌ Exception: {e}")

def main():
    """Test all components"""
    print("🚀 Updated LINE Bot Component Tester")
    print("=" * 50)
    
    # Test cases for different components
    test_cases = [
        ("媽媽最近常重複問同樣的問題", "Memory_Issues"),
        ("爸爸無法安排日常活動", "Planning_Problems"), 
        ("外婆不會使用以前熟悉的電器", "Familiar_Tasks"),
        ("help", "Help_Command")
    ]
    
    for user_input, component_name in test_cases:
        test_component(user_input, component_name)
        time.sleep(1)  # Avoid overwhelming the API
    
    print("\n📊 Testing Summary")
    print("=" * 50)
    print("✅ Check the generated component_*.json files")
    print("📱 Send the same messages to your LINE Bot to see visual results")
    
    # Check what files were created
    import glob
    json_files = glob.glob("component_*.json")
    if json_files:
        print(f"📁 Generated files: {', '.join(json_files)}")
    else:
        print("❌ No files generated - check API connection")

if __name__ == "__main__":
    main()
