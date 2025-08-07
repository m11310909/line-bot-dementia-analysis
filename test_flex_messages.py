#!/usr/bin/env python3
"""
測試 Flex Messages 功能
演示不同分析結果的視覺化效果
"""

import json
import requests
from datetime import datetime

def test_flex_messages():
    """測試 Flex Messages 功能"""
    
    # 測試數據
    test_cases = [
        {
            "name": "M1 - 記憶力分析",
            "analysis_result": {
                "success": True,
                "message": "M1 分析完成",
                "data": {
                    "module": "M1",
                    "warning_signs": ["記憶力減退", "語言障礙", "定向力下降"],
                    "risk_level": "medium",
                    "recommendations": ["建議就醫檢查", "注意安全", "建立提醒系統"]
                }
            }
        },
        {
            "name": "M2 - 病程進展",
            "analysis_result": {
                "success": True,
                "message": "M2 分析完成",
                "data": {
                    "module": "M2",
                    "progression_stage": "mild",
                    "symptoms": ["認知功能下降", "行為改變", "情緒波動"],
                    "care_focus": ["認知訓練", "環境安全", "情緒支持"]
                }
            }
        },
        {
            "name": "M3 - 行為心理症狀",
            "analysis_result": {
                "success": True,
                "message": "M3 分析完成",
                "data": {
                    "module": "M3",
                    "bpsd_symptoms": ["妄想", "幻覺", "攻擊行為"],
                    "intervention": ["藥物治療", "行為療法", "環境調整"],
                    "severity": "moderate"
                }
            }
        },
        {
            "name": "綜合分析",
            "analysis_result": {
                "success": True,
                "message": "comprehensive 分析完成",
                "data": {
                    "module": "comprehensive",
                    "modules_used": ["M1", "M2", "M3", "M4"],
                    "overall_assessment": "需要專業醫療評估",
                    "recommendations": [
                        "立即就醫檢查",
                        "安排認知功能評估",
                        "考慮藥物治療",
                        "建立安全照護環境"
                    ],
                    "confidence": 0.85
                }
            }
        }
    ]
    
    print("🎨 Flex Messages 測試")
    print("=" * 50)
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n📋 測試案例 {i}: {test_case['name']}")
        print("-" * 30)
        
        # 模擬 Flex Message 生成
        flex_message = generate_flex_message(test_case['analysis_result'])
        
        print(f"✅ Flex Message 生成成功")
        print(f"   標題: {flex_message.get('altText', 'N/A')}")
        print(f"   類型: {flex_message.get('contents', {}).get('type', 'N/A')}")
        print(f"   大小: {flex_message.get('contents', {}).get('size', 'N/A')}")
        
        # 保存到文件
        filename = f"flex_message_test_{i}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(flex_message, f, ensure_ascii=False, indent=2)
        print(f"💾 已保存到: {filename}")

def generate_flex_message(analysis_result: dict) -> dict:
    """生成 Flex Message（簡化版）"""
    
    # 根據模組類型選擇顏色
    color_map = {
        "M1": "#FF6B6B",  # 紅色 - 記憶力
        "M2": "#4ECDC4",  # 青色 - 情緒
        "M3": "#45B7D1",  # 藍色 - 空間
        "M4": "#96CEB4",  # 綠色 - 興趣
        "comprehensive": "#FFA07A"  # 橙色 - 綜合
    }
    
    data = analysis_result.get("data", {})
    module = data.get("module", "comprehensive")
    primary_color = color_map.get(module, "#FF6B6B")
    
    # 風險等級顏色
    risk_level = data.get("risk_level", "medium")
    risk_color_map = {
        "low": "#4CAF50",
        "medium": "#FF9800", 
        "high": "#F44336"
    }
    risk_color = risk_color_map.get(risk_level, "#FF9800")
    
    # 生成症狀和建議文本
    symptoms = []
    recommendations = []
    
    if module == "M1":
        symptoms = data.get("warning_signs", [])
        recommendations = data.get("recommendations", [])
    elif module == "M2":
        symptoms = data.get("symptoms", [])
        recommendations = data.get("care_focus", [])
    elif module == "M3":
        symptoms = data.get("bpsd_symptoms", [])
        recommendations = data.get("intervention", [])
    elif module == "comprehensive":
        symptoms = ["綜合症狀評估"]
        recommendations = data.get("recommendations", [])
    
    symptoms_text = "\n".join([f"• {symptom}" for symptom in symptoms]) if symptoms else "• 需要進一步評估"
    recommendations_text = "\n".join([f"• {rec}" for rec in recommendations]) if recommendations else "• 建議尋求專業醫療協助"
    
    return {
        "type": "flex",
        "altText": f"失智症分析結果 - {module}",
        "contents": {
            "type": "bubble",
            "size": "giga",
            "header": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": f"🔍 {module} 分析結果",
                        "weight": "bold",
                        "size": "lg",
                        "color": "#FFFFFF"
                    },
                    {
                        "type": "text",
                        "text": f"風險等級: {risk_level.upper()}",
                        "size": "sm",
                        "color": "#FFFFFF",
                        "margin": "sm"
                    }
                ],
                "backgroundColor": primary_color,
                "paddingAll": "20px"
            },
            "body": {
                "type": "box",
                "layout": "vertical",
                "spacing": "md",
                "contents": [
                    {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {
                                "type": "text",
                                "text": "📋 可能症狀",
                                "weight": "bold",
                                "size": "md",
                                "margin": "sm"
                            },
                            {
                                "type": "text",
                                "text": symptoms_text,
                                "size": "sm",
                                "color": "#666666",
                                "wrap": True,
                                "margin": "sm"
                            }
                        ]
                    },
                    {
                        "type": "separator",
                        "margin": "lg"
                    },
                    {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {
                                "type": "text",
                                "text": "💡 建議",
                                "weight": "bold",
                                "size": "md",
                                "margin": "sm"
                            },
                            {
                                "type": "text",
                                "text": recommendations_text,
                                "size": "sm",
                                "color": "#666666",
                                "wrap": True,
                                "margin": "sm"
                            }
                        ]
                    }
                ],
                "paddingAll": "20px"
            },
            "footer": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": "⚠️ 此分析僅供參考，請諮詢專業醫療人員",
                        "size": "xs",
                        "color": "#999999",
                        "align": "center",
                        "wrap": True
                    }
                ],
                "paddingAll": "15px"
            }
        }
    }

if __name__ == "__main__":
    test_flex_messages() 