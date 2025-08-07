#!/usr/bin/env python3
"""
調試 Flex Messages 生成
檢查 Flex Messages 是否正確生成
"""

import json
import sys
import importlib.util

def debug_flex_message_generation():
    """調試 Flex Message 生成"""
    
    print("🔍 調試 Flex Message 生成")
    print("=" * 40)
    
    # 測試數據
    test_cases = [
        {
            "name": "M1 測試",
            "analysis_result": {
                "success": True,
                "message": "M1 分析完成",
                "data": {
                    "module": "M1",
                    "warning_signs": ["記憶力減退", "語言障礙", "定向力下降"],
                    "risk_level": "medium",
                    "recommendations": ["建議就醫檢查", "注意安全", "建立提醒系統"]
                }
            },
            "expected_module": "M1"
        },
        {
            "name": "M3 測試",
            "analysis_result": {
                "success": True,
                "message": "M3 分析完成",
                "data": {
                    "module": "M3",
                    "bpsd_symptoms": ["妄想", "幻覺", "攻擊行為"],
                    "intervention": ["藥物治療", "行為療法", "環境調整"],
                    "severity": "moderate"
                }
            },
            "expected_module": "M3"
        }
    ]
    
    try:
        # 動態導入模組
        spec = importlib.util.spec_from_file_location("enhanced_api", "enhanced_m1_m2_m3_integrated_api_fixed.py")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        
        print("✅ 成功導入模組")
        
        for i, test_case in enumerate(test_cases, 1):
            print(f"\n📋 測試案例 {i}: {test_case['name']}")
            print("-" * 30)
            
            # 生成 Flex Message
            flex_message = module.create_flex_message(
                test_case['analysis_result'], 
                test_case['expected_module']
            )
            
            print(f"✅ Flex Message 生成成功")
            print(f"   標題: {flex_message.get('altText', 'N/A')}")
            print(f"   類型: {flex_message.get('contents', {}).get('type', 'N/A')}")
            print(f"   大小: {flex_message.get('contents', {}).get('size', 'N/A')}")
            
            # 檢查內容結構
            contents = flex_message.get('contents', {})
            header = contents.get('header', {})
            body = contents.get('body', {})
            
            print(f"   標題顏色: {header.get('backgroundColor', 'N/A')}")
            print(f"   內容區塊數量: {len(body.get('contents', []))}")
            
            # 檢查症狀和建議
            body_contents = body.get('contents', [])
            if len(body_contents) >= 3:
                symptoms_box = body_contents[0]
                recommendations_box = body_contents[2]
                
                symptoms_text = ""
                recommendations_text = ""
                
                if 'contents' in symptoms_box:
                    for content in symptoms_box['contents']:
                        if content.get('type') == 'text':
                            symptoms_text = content.get('text', '')
                            break
                
                if 'contents' in recommendations_box:
                    for content in recommendations_box['contents']:
                        if content.get('type') == 'text':
                            recommendations_text = content.get('text', '')
                            break
                
                print(f"   症狀: {symptoms_text[:50]}...")
                print(f"   建議: {recommendations_text[:50]}...")
            
            # 保存到文件
            filename = f"debug_flex_message_{i}_{test_case['expected_module']}.json"
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(flex_message, f, ensure_ascii=False, indent=2)
            print(f"💾 已保存到: {filename}")
        
        print(f"\n🎉 調試完成！")
        print("=" * 40)
        print("📝 檢查生成的文件以確認 Flex Message 結構")
        
    except Exception as e:
        print(f"❌ 調試失敗: {e}")
        import traceback
        traceback.print_exc()

def test_flex_message_sending():
    """測試 Flex Message 發送"""
    
    print("\n📤 測試 Flex Message 發送")
    print("=" * 30)
    
    try:
        # 動態導入模組
        spec = importlib.util.spec_from_file_location("enhanced_api", "enhanced_m1_m2_m3_integrated_api_fixed.py")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        
        # 模擬分析結果
        test_analysis = {
            "success": True,
            "message": "M1 分析完成",
            "data": {
                "module": "M1",
                "warning_signs": ["記憶力減退", "語言障礙"],
                "risk_level": "medium",
                "recommendations": ["建議就醫檢查", "注意安全"]
            }
        }
        
        # 生成 Flex Message
        flex_message = module.generate_flex_reply(test_analysis)
        
        print("✅ Flex Message 生成成功")
        print(f"   標題: {flex_message.get('altText', 'N/A')}")
        
        # 模擬發送（測試模式）
        module.send_line_reply("test-reply-token", "", flex_message)
        
        print("✅ Flex Message 發送測試完成")
        
    except Exception as e:
        print(f"❌ 發送測試失敗: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("🚀 啟動 Flex Messages 調試")
    print("=" * 50)
    
    # 調試 Flex Message 生成
    debug_flex_message_generation()
    
    # 測試 Flex Message 發送
    test_flex_message_sending() 