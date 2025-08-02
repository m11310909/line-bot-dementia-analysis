from typing import Dict, Any, List
import json

class XAIFlexMessageBuilder:
    """Enhanced Flex Message builder for XAI visualization"""
    
    def __init__(self):
        self.module_colors = {
            "M1": "#E74C3C",  # Red for warning signs
            "M2": "#E67E22",  # Orange for progression
            "M3": "#9B59B6",  # Purple for BPSD
            "M4": "#3498DB",  # Blue for care
            "general": "#27AE60"  # Green for general
        }
    
    def build_xai_message(self, 
                         module: str, 
                         visualization_data: Dict[str, Any], 
                         original_text: str = "") -> Dict[str, Any]:
        """Build enhanced Flex Message with XAI visualization"""
        
        if module == "M1":
            return self.build_m1_message(visualization_data, original_text)
        elif module == "M2":
            return self.build_m2_message(visualization_data, original_text)
        elif module == "M3":
            return self.build_m3_message(visualization_data, original_text)
        elif module == "M4":
            return self.build_m4_message(visualization_data, original_text)
        else:
            return self.build_general_message(visualization_data, original_text)
    
    def build_m1_message(self, visualization_data: Dict[str, Any], original_text: str) -> Dict[str, Any]:
        """Build M1 warning signs comparison message"""
        confidence = visualization_data.get("confidence_score", 0.0)
        evidence_highlights = visualization_data.get("evidence_highlights", [])
        
        # Create evidence items
        evidence_items = []
        for highlight in evidence_highlights[:3]:  # Limit to 3 items
            evidence_items.append({
                "type": "text",
                "text": f"• {highlight['text']}",
                "size": "sm",
                "color": "#E74C3C",
                "weight": "bold"
            })
        
        # Create comparison section
        comparison = visualization_data.get("comparison", {})
        normal_aging = comparison.get("normal_aging", [])
        warning_signs = comparison.get("warning_signs", [])
        
        comparison_items = []
        if normal_aging:
            comparison_items.append({
                "type": "text",
                "text": "正常老化 vs 失智警訊",
                "size": "sm",
                "weight": "bold",
                "color": "#666666"
            })
        
        return {
            "type": "flex",
            "altText": "M1 失智症警訊分析結果",
            "contents": {
                "type": "bubble",
                "size": "kilo",
                "header": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "text",
                            "text": "🚨 M1 警訊分析",
                            "weight": "bold",
                            "color": "#ffffff",
                            "size": "lg"
                        },
                        {
                            "type": "text",
                            "text": f"信心度: {confidence:.1%}",
                            "color": "#ffffff",
                            "size": "sm"
                        }
                    ],
                    "backgroundColor": self.module_colors["M1"]
                },
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "spacing": "md",
                    "contents": [
                        {
                            "type": "text",
                            "text": "📝 分析結果",
                            "weight": "bold",
                            "size": "md",
                            "color": "#333333"
                        },
                        {
                            "type": "separator"
                        }
                    ] + evidence_items + [
                        {
                            "type": "separator"
                        },
                        {
                            "type": "text",
                            "text": "💡 建議",
                            "weight": "bold",
                            "size": "sm",
                            "color": "#333333"
                        },
                        {
                            "type": "text",
                            "text": "如發現多項警訊，建議及早諮詢專業醫療人員",
                            "size": "sm",
                            "color": "#666666",
                            "wrap": True
                        }
                    ]
                }
            }
        }
    
    def build_m2_message(self, visualization_data: Dict[str, Any], original_text: str) -> Dict[str, Any]:
        """Build M2 progression stage message"""
        confidence = visualization_data.get("confidence_score", 0.0)
        stage_indicators = visualization_data.get("stage_indicators", [])
        
        # Create stage indicator items
        indicator_items = []
        for indicator in stage_indicators[:3]:  # Limit to 3 items
            indicator_items.append({
                "type": "text",
                "text": f"• {indicator}",
                "size": "sm",
                "color": "#E67E22"
            })
        
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
                            "type": "text",
                            "text": "📊 M2 病程階段",
                            "weight": "bold",
                            "color": "#ffffff",
                            "size": "lg"
                        },
                        {
                            "type": "text",
                            "text": f"信心度: {confidence:.1%}",
                            "color": "#ffffff",
                            "size": "sm"
                        }
                    ],
                    "backgroundColor": self.module_colors["M2"]
                },
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "spacing": "md",
                    "contents": [
                        {
                            "type": "text",
                            "text": "📈 階段指標",
                            "weight": "bold",
                            "size": "md",
                            "color": "#333333"
                        },
                        {
                            "type": "separator"
                        }
                    ] + indicator_items + [
                        {
                            "type": "separator"
                        },
                        {
                            "type": "text",
                            "text": "💡 建議",
                            "weight": "bold",
                            "size": "sm",
                            "color": "#333333"
                        },
                        {
                            "type": "text",
                            "text": "定期追蹤病程變化，適時調整照護策略",
                            "size": "sm",
                            "color": "#666666",
                            "wrap": True
                        }
                    ]
                }
            }
        }
    
    def build_m3_message(self, visualization_data: Dict[str, Any], original_text: str) -> Dict[str, Any]:
        """Build M3 BPSD symptoms message"""
        confidence = visualization_data.get("confidence_score", 0.0)
        symptoms = visualization_data.get("symptoms", [])
        severity = visualization_data.get("severity_indicators", "low")
        
        # Create symptom items
        symptom_items = []
        for symptom in symptoms[:3]:  # Limit to 3 items
            symptom_items.append({
                "type": "text",
                "text": f"• {symptom}",
                "size": "sm",
                "color": "#9B59B6"
            })
        
        severity_text = {
            "high": "高",
            "medium": "中",
            "low": "低"
        }.get(severity, "低")
        
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
                            "type": "text",
                            "text": "🧠 M3 BPSD 症狀",
                            "weight": "bold",
                            "color": "#ffffff",
                            "size": "lg"
                        },
                        {
                            "type": "text",
                            "text": f"嚴重程度: {severity_text}",
                            "color": "#ffffff",
                            "size": "sm"
                        }
                    ],
                    "backgroundColor": self.module_colors["M3"]
                },
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "spacing": "md",
                    "contents": [
                        {
                            "type": "text",
                            "text": "🔍 症狀分析",
                            "weight": "bold",
                            "size": "md",
                            "color": "#333333"
                        },
                        {
                            "type": "separator"
                        }
                    ] + symptom_items + [
                        {
                            "type": "separator"
                        },
                        {
                            "type": "text",
                            "text": "💡 建議",
                            "weight": "bold",
                            "size": "sm",
                            "color": "#333333"
                        },
                        {
                            "type": "text",
                            "text": "尋求精神科醫師協助，考慮藥物治療",
                            "size": "sm",
                            "color": "#666666",
                            "wrap": True
                        }
                    ]
                }
            }
        }
    
    def build_m4_message(self, visualization_data: Dict[str, Any], original_text: str) -> Dict[str, Any]:
        """Build M4 care navigation message"""
        confidence = visualization_data.get("confidence_score", 0.0)
        care_needs = visualization_data.get("care_needs", [])
        priority = visualization_data.get("priority_level", "low")
        
        # Create care need items
        care_items = []
        for need in care_needs[:3]:  # Limit to 3 items
            care_items.append({
                "type": "text",
                "text": f"• {need}",
                "size": "sm",
                "color": "#3498DB"
            })
        
        priority_text = {
            "high": "高",
            "medium": "中",
            "low": "低"
        }.get(priority, "低")
        
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
                            "type": "text",
                            "text": "🏥 M4 照護需求",
                            "weight": "bold",
                            "color": "#ffffff",
                            "size": "lg"
                        },
                        {
                            "type": "text",
                            "text": f"優先級: {priority_text}",
                            "color": "#ffffff",
                            "size": "sm"
                        }
                    ],
                    "backgroundColor": self.module_colors["M4"]
                },
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "spacing": "md",
                    "contents": [
                        {
                            "type": "text",
                            "text": "🎯 照護重點",
                            "weight": "bold",
                            "size": "md",
                            "color": "#333333"
                        },
                        {
                            "type": "separator"
                        }
                    ] + care_items + [
                        {
                            "type": "separator"
                        },
                        {
                            "type": "text",
                            "text": "💡 建議",
                            "weight": "bold",
                            "size": "sm",
                            "color": "#333333"
                        },
                        {
                            "type": "text",
                            "text": "尋求專業照護資源，建立支持網絡",
                            "size": "sm",
                            "color": "#666666",
                            "wrap": True
                        }
                    ]
                }
            }
        }
    
    def build_general_message(self, visualization_data: Dict[str, Any], original_text: str) -> Dict[str, Any]:
        """Build general analysis message"""
        confidence = visualization_data.get("confidence_score", 0.0)
        key_points = visualization_data.get("key_points", [])
        
        # Create key point items
        point_items = []
        for point in key_points[:3]:  # Limit to 3 items
            point_items.append({
                "type": "text",
                "text": f"• {point}",
                "size": "sm",
                "color": "#27AE60"
            })
        
        return {
            "type": "flex",
            "altText": "一般分析結果",
            "contents": {
                "type": "bubble",
                "size": "kilo",
                "header": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "text",
                            "text": "📝 一般分析",
                            "weight": "bold",
                            "color": "#ffffff",
                            "size": "lg"
                        },
                        {
                            "type": "text",
                            "text": f"信心度: {confidence:.1%}",
                            "color": "#ffffff",
                            "size": "sm"
                        }
                    ],
                    "backgroundColor": self.module_colors["general"]
                },
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "spacing": "md",
                    "contents": [
                        {
                            "type": "text",
                            "text": "🔍 分析重點",
                            "weight": "bold",
                            "size": "md",
                            "color": "#333333"
                        },
                        {
                            "type": "separator"
                        }
                    ] + point_items + [
                        {
                            "type": "separator"
                        },
                        {
                            "type": "text",
                            "text": "💡 建議",
                            "weight": "bold",
                            "size": "sm",
                            "color": "#333333"
                        },
                        {
                            "type": "text",
                            "text": "持續觀察症狀變化，適時尋求專業協助",
                            "size": "sm",
                            "color": "#666666",
                            "wrap": True
                        }
                    ]
                }
            }
        } 