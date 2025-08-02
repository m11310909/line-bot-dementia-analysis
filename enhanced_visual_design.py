#!/usr/bin/env python3
"""
增強版視覺設計系統
參考智慧照護助手 UI 設計風格
"""

def create_enhanced_m1_flex_message(analysis: dict, original_text: str) -> dict:
    """創建增強版 M1 警訊分析 Flex Message"""
    
    # 根據檢測到的警訊數量決定顏色
    warning_count = len(analysis.get("detected_signs", []))
    if warning_count >= 3:
        header_color = "#E74C3C"  # 紅色 - 高風險
        severity_text = "高風險"
    elif warning_count >= 1:
        header_color = "#F39C12"  # 橙色 - 中風險
        severity_text = "中風險"
    else:
        header_color = "#27AE60"  # 綠色 - 低風險
        severity_text = "低風險"
    
    signs_text = "\n• ".join(analysis["detected_signs"]) if analysis["detected_signs"] else "未檢測到明顯警訊"
    
    return {
        "type": "flex",
        "altText": "M1 警訊分析結果",
        "contents": {
            "type": "bubble",
            "size": "kilo",
            "header": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "contents": [
                            {
                                "type": "text",
                                "text": "🚨",
                                "size": "lg",
                                "flex": 0
                            },
                            {
                                "type": "box",
                                "layout": "vertical",
                                "contents": [
                                    {
                                        "type": "text",
                                        "text": "M1 警訊分析",
                                        "weight": "bold",
                                        "color": "#ffffff",
                                        "size": "lg"
                                    },
                                    {
                                        "type": "text",
                                        "text": "AI 驅動的失智症警訊評估",
                                        "color": "#ffffff",
                                        "size": "xs",
                                        "opacity": 0.8
                                    }
                                ],
                                "flex": 1
                            }
                        ]
                    }
                ],
                "backgroundColor": header_color,
                "paddingAll": "20px"
            },
            "body": {
                "type": "box",
                "layout": "vertical",
                "spacing": "md",
                "contents": [
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "contents": [
                            {
                                "type": "text",
                                "text": "📊 風險評估",
                                "weight": "bold",
                                "size": "sm",
                                "flex": 0
                            },
                            {
                                "type": "text",
                                "text": severity_text,
                                "color": header_color,
                                "weight": "bold",
                                "size": "sm",
                                "align": "end"
                            }
                        ]
                    },
                    {
                        "type": "separator"
                    },
                    {
                        "type": "text",
                        "text": f"📝 您的描述：\n{original_text}",
                        "wrap": True,
                        "size": "sm",
                        "color": "#666666"
                    },
                    {
                        "type": "separator"
                    },
                    {
                        "type": "text",
                        "text": f"🔍 分析結果：\n{analysis['analysis']}",
                        "wrap": True,
                        "size": "sm"
                    },
                    {
                        "type": "separator"
                    },
                    {
                        "type": "text",
                        "text": f"⚠️ 檢測到的警訊：\n• {signs_text}",
                        "wrap": True,
                        "size": "sm",
                        "color": header_color if analysis["detected_signs"] else "#27AE60"
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
                        "text": "💡 建議：及早發現，及早介入",
                        "size": "xs",
                        "color": "#666666",
                        "align": "center"
                    }
                ],
                "paddingAll": "15px"
            }
        }
    }

def create_enhanced_m2_flex_message(analysis: dict, original_text: str) -> dict:
    """創建增強版 M2 病程階段 Flex Message"""
    
    stage = analysis.get("detected_stage", "輕度")
    stage_colors = {
        "輕度": {"header": "#27AE60", "progress": "#27AE60", "text": "早期階段"},
        "中度": {"header": "#F39C12", "progress": "#F39C12", "text": "中期階段"},
        "重度": {"header": "#E74C3C", "progress": "#E74C3C", "text": "晚期階段"}
    }
    
    color_info = stage_colors.get(stage, stage_colors["輕度"])
    
    return {
        "type": "flex",
        "altText": "M2 病程階段分析結果",
        "contents": {
            "type": "bubble",
            "size": "kilo",
            "header": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "contents": [
                            {
                                "type": "text",
                                "text": "📊",
                                "size": "lg",
                                "flex": 0
                            },
                            {
                                "type": "box",
                                "layout": "vertical",
                                "contents": [
                                    {
                                        "type": "text",
                                        "text": "M2 病程階段",
                                        "weight": "bold",
                                        "color": "#ffffff",
                                        "size": "lg"
                                    },
                                    {
                                        "type": "text",
                                        "text": "AI 驅動的病程評估",
                                        "color": "#ffffff",
                                        "size": "xs",
                                        "opacity": 0.8
                                    }
                                ],
                                "flex": 1
                            }
                        ]
                    }
                ],
                "backgroundColor": color_info["header"],
                "paddingAll": "20px"
            },
            "body": {
                "type": "box",
                "layout": "vertical",
                "spacing": "md",
                "contents": [
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "contents": [
                            {
                                "type": "text",
                                "text": "🎯 當前階段",
                                "weight": "bold",
                                "size": "sm",
                                "flex": 0
                            },
                            {
                                "type": "text",
                                "text": color_info["text"],
                                "color": color_info["header"],
                                "weight": "bold",
                                "size": "sm",
                                "align": "end"
                            }
                        ]
                    },
                    {
                        "type": "separator"
                    },
                    {
                        "type": "text",
                        "text": f"📝 您的描述：\n{original_text}",
                        "wrap": True,
                        "size": "sm",
                        "color": "#666666"
                    },
                    {
                        "type": "separator"
                    },
                    {
                        "type": "text",
                        "text": f"🔍 分析結果：\n{analysis['analysis']}",
                        "wrap": True,
                        "size": "sm"
                    },
                    {
                        "type": "separator"
                    },
                    {
                        "type": "text",
                        "text": f"📈 進展程度：{stage}",
                        "size": "sm",
                        "color": color_info["header"]
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
                        "text": "💡 建議：根據階段調整照護策略",
                        "size": "xs",
                        "color": "#666666",
                        "align": "center"
                    }
                ],
                "paddingAll": "15px"
            }
        }
    }

def create_enhanced_m3_flex_message(analysis: dict, original_text: str) -> dict:
    """創建增強版 M3 BPSD 症狀 Flex Message"""
    
    symptoms_count = len(analysis.get("detected_symptoms", []))
    if symptoms_count >= 3:
        header_color = "#9B59B6"  # 紫色 - 嚴重
        severity_text = "嚴重"
    elif symptoms_count >= 1:
        header_color = "#8E44AD"  # 深紫色 - 中度
        severity_text = "中度"
    else:
        header_color = "#BB8FCE"  # 淺紫色 - 輕度
        severity_text = "輕度"
    
    symptoms_text = "\n• ".join(analysis["detected_symptoms"]) if analysis["detected_symptoms"] else "未檢測到明顯 BPSD 症狀"
    
    return {
        "type": "flex",
        "altText": "M3 BPSD 症狀分析結果",
        "contents": {
            "type": "bubble",
            "size": "kilo",
            "header": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "contents": [
                            {
                                "type": "text",
                                "text": "🧠",
                                "size": "lg",
                                "flex": 0
                            },
                            {
                                "type": "box",
                                "layout": "vertical",
                                "contents": [
                                    {
                                        "type": "text",
                                        "text": "M3 BPSD 症狀",
                                        "weight": "bold",
                                        "color": "#ffffff",
                                        "size": "lg"
                                    },
                                    {
                                        "type": "text",
                                        "text": "AI 驅動的行為症狀分析",
                                        "color": "#ffffff",
                                        "size": "xs",
                                        "opacity": 0.8
                                    }
                                ],
                                "flex": 1
                            }
                        ]
                    }
                ],
                "backgroundColor": header_color,
                "paddingAll": "20px"
            },
            "body": {
                "type": "box",
                "layout": "vertical",
                "spacing": "md",
                "contents": [
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "contents": [
                            {
                                "type": "text",
                                "text": "📊 症狀嚴重度",
                                "weight": "bold",
                                "size": "sm",
                                "flex": 0
                            },
                            {
                                "type": "text",
                                "text": severity_text,
                                "color": header_color,
                                "weight": "bold",
                                "size": "sm",
                                "align": "end"
                            }
                        ]
                    },
                    {
                        "type": "separator"
                    },
                    {
                        "type": "text",
                        "text": f"📝 您的描述：\n{original_text}",
                        "wrap": True,
                        "size": "sm",
                        "color": "#666666"
                    },
                    {
                        "type": "separator"
                    },
                    {
                        "type": "text",
                        "text": f"🔍 分析結果：\n{analysis['analysis']}",
                        "wrap": True,
                        "size": "sm"
                    },
                    {
                        "type": "separator"
                    },
                    {
                        "type": "text",
                        "text": f"⚠️ 檢測到的症狀：\n• {symptoms_text}",
                        "wrap": True,
                        "size": "sm",
                        "color": header_color if analysis["detected_symptoms"] else "#27AE60"
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
                        "text": "💡 建議：尋求專業醫療協助",
                        "size": "xs",
                        "color": "#666666",
                        "align": "center"
                    }
                ],
                "paddingAll": "15px"
            }
        }
    }

def create_enhanced_m4_flex_message(analysis: dict, original_text: str) -> dict:
    """創建增強版 M4 照護需求 Flex Message"""
    
    needs_count = len(analysis.get("detected_needs", []))
    if needs_count >= 3:
        header_color = "#3498DB"  # 藍色 - 高需求
        priority_text = "高優先"
    elif needs_count >= 1:
        header_color = "#5DADE2"  # 中藍色 - 中需求
        priority_text = "中優先"
    else:
        header_color = "#85C1E9"  # 淺藍色 - 低需求
        priority_text = "低優先"
    
    needs_text = "\n• ".join(analysis["detected_needs"]) if analysis["detected_needs"] else "未識別特定照護需求"
    
    return {
        "type": "flex",
        "altText": "M4 照護需求分析結果",
        "contents": {
            "type": "bubble",
            "size": "kilo",
            "header": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "contents": [
                            {
                                "type": "text",
                                "text": "🏥",
                                "size": "lg",
                                "flex": 0
                            },
                            {
                                "type": "box",
                                "layout": "vertical",
                                "contents": [
                                    {
                                        "type": "text",
                                        "text": "M4 照護需求",
                                        "weight": "bold",
                                        "color": "#ffffff",
                                        "size": "lg"
                                    },
                                    {
                                        "type": "text",
                                        "text": "AI 驅動的照護需求分析",
                                        "color": "#ffffff",
                                        "size": "xs",
                                        "opacity": 0.8
                                    }
                                ],
                                "flex": 1
                            }
                        ]
                    }
                ],
                "backgroundColor": header_color,
                "paddingAll": "20px"
            },
            "body": {
                "type": "box",
                "layout": "vertical",
                "spacing": "md",
                "contents": [
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "contents": [
                            {
                                "type": "text",
                                "text": "🎯 需求優先級",
                                "weight": "bold",
                                "size": "sm",
                                "flex": 0
                            },
                            {
                                "type": "text",
                                "text": priority_text,
                                "color": header_color,
                                "weight": "bold",
                                "size": "sm",
                                "align": "end"
                            }
                        ]
                    },
                    {
                        "type": "separator"
                    },
                    {
                        "type": "text",
                        "text": f"📝 您的描述：\n{original_text}",
                        "wrap": True,
                        "size": "sm",
                        "color": "#666666"
                    },
                    {
                        "type": "separator"
                    },
                    {
                        "type": "text",
                        "text": f"🔍 分析結果：\n{analysis['analysis']}",
                        "wrap": True,
                        "size": "sm"
                    },
                    {
                        "type": "separator"
                    },
                    {
                        "type": "text",
                        "text": f"🎯 識別的需求：\n• {needs_text}",
                        "wrap": True,
                        "size": "sm",
                        "color": header_color if analysis["detected_needs"] else "#27AE60"
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
                        "text": "💡 建議：尋求相關資源協助",
                        "size": "xs",
                        "color": "#666666",
                        "align": "center"
                    }
                ],
                "paddingAll": "15px"
            }
        }
    }

# 視覺設計系統配置
VISUAL_DESIGN_CONFIG = {
    "colors": {
        "m1": {
            "high_risk": "#E74C3C",
            "medium_risk": "#F39C12", 
            "low_risk": "#27AE60"
        },
        "m2": {
            "early": "#27AE60",
            "middle": "#F39C12",
            "late": "#E74C3C"
        },
        "m3": {
            "severe": "#9B59B6",
            "moderate": "#8E44AD",
            "mild": "#BB8FCE"
        },
        "m4": {
            "high": "#3498DB",
            "medium": "#5DADE2",
            "low": "#85C1E9"
        }
    },
    "icons": {
        "m1": "🚨",
        "m2": "📊", 
        "m3": "🧠",
        "m4": "🏥"
    },
    "titles": {
        "m1": "M1 警訊分析",
        "m2": "M2 病程階段",
        "m3": "M3 BPSD 症狀", 
        "m4": "M4 照護需求"
    },
    "subtitles": {
        "m1": "AI 驅動的失智症警訊評估",
        "m2": "AI 驅動的病程評估",
        "m3": "AI 驅動的行為症狀分析",
        "m4": "AI 驅動的照護需求分析"
    }
} 