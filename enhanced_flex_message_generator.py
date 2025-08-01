"""
Enhanced Flex Message Generator for M1-M4 Visualization Modules
Implements the redesigned visualization system with LINE Flex Message and LIFF requirements
"""

import json
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from datetime import datetime
import math

# Design System Constants
class DesignSystem:
    # Color System
    PRIMARY_BLUE = "#2196F3"
    PRIMARY_GREEN = "#4CAF50"
    PRIMARY_ORANGE = "#FF9800"
    PRIMARY_RED = "#F44336"
    
    # Confidence Colors
    CONFIDENCE_HIGH = "#4CAF50"
    CONFIDENCE_MEDIUM = "#2196F3"
    CONFIDENCE_LOW = "#FF9800"
    
    # Background Colors
    BG_CARD = "#FFFFFF"
    BG_SUBTLE = "#F8F9FA"
    BG_SECTION = "#F5F5F5"
    
    # Typography Sizes (optimized for seniors)
    TEXT_XS = "13px"
    TEXT_SM = "15px"
    TEXT_BASE = "17px"
    TEXT_LG = "19px"
    TEXT_XL = "21px"

@dataclass
class AnalysisResult:
    module: str
    confidence: float
    matched_items: List[Dict]
    summary: str
    timestamp: datetime
    user_input: str

class EnhancedFlexMessageGenerator:
    def __init__(self):
        self.design = DesignSystem()
    
    def create_m1_warning_signs_card(self, result: AnalysisResult) -> Dict:
        """M1: 十大警訊比對卡 (重新設計)"""
        
        # Calculate confidence percentage
        confidence_percentage = int(result.confidence * 100)
        confidence_level = self._get_confidence_level(confidence_percentage)
        
        # Get primary matched item
        primary_item = result.matched_items[0] if result.matched_items else None
        
        return {
            "type": "bubble",
            "size": "mega",
            "header": {
                "type": "box",
                "layout": "vertical",
                "backgroundColor": self.design.BG_SUBTLE,
                "paddingAll": "16px",
                "contents": [
                    {
                        "type": "text",
                        "text": "AI 智慧分析",
                        "size": "sm",
                        "color": "#666666"
                    },
                    {
                        "type": "text",
                        "text": "記憶力評估分析",
                        "size": "xl",
                        "weight": "bold",
                        "color": "#212121",
                        "margin": "sm"
                    },
                    {
                        "type": "text",
                        "text": result.timestamp.strftime("%Y/%m/%d %p%I:%M"),
                        "size": "xs",
                        "color": "#999999"
                    }
                ]
            },
            "body": {
                "type": "box",
                "layout": "vertical",
                "spacing": "md",
                "paddingAll": "16px",
                "contents": [
                    # AI Confidence Block
                    {
                        "type": "box",
                        "layout": "vertical",
                        "spacing": "sm",
                        "contents": [
                            {
                                "type": "text",
                                "text": "AI 信心度",
                                "size": "sm",
                                "weight": "bold",
                                "color": "#666666"
                            },
                            {
                                "type": "box",
                                "layout": "horizontal",
                                "contents": [
                                    {
                                        "type": "box",
                                        "width": f"{confidence_percentage}%",
                                        "height": "8px",
                                        "backgroundColor": confidence_level["color"],
                                        "cornerRadius": "4px"
                                    },
                                    {
                                        "type": "box",
                                        "width": f"{100 - confidence_percentage}%",
                                        "height": "8px",
                                        "backgroundColor": "#E0E0E0",
                                        "cornerRadius": "4px"
                                    }
                                ]
                            },
                            {
                                "type": "text",
                                "text": f"{confidence_percentage}% {confidence_level['label']}",
                                "size": "xs",
                                "color": confidence_level["color"],
                                "align": "end"
                            }
                        ]
                    },
                    # Comparison Cards
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "spacing": "md",
                        "margin": "lg",
                        "contents": [
                            # Normal Aging Card
                            {
                                "type": "box",
                                "layout": "vertical",
                                "flex": 1,
                                "backgroundColor": self.design.BG_SECTION,
                                "cornerRadius": "12px",
                                "paddingAll": "16px",
                                "contents": [
                                    {
                                        "type": "box",
                                        "layout": "horizontal",
                                        "contents": [
                                            {
                                                "type": "text",
                                                "text": "✓",
                                                "color": self.design.PRIMARY_GREEN,
                                                "size": "lg",
                                                "flex": 0
                                            },
                                            {
                                                "type": "text",
                                                "text": "正常老化",
                                                "weight": "bold",
                                                "size": "sm",
                                                "color": self.design.PRIMARY_GREEN,
                                                "margin": "sm"
                                            }
                                        ]
                                    },
                                    {
                                        "type": "text",
                                        "text": primary_item.get("normal_aging", "偶爾忘記事情，提醒後能想起") if primary_item else "偶爾忘記事情，提醒後能想起",
                                        "size": "xs",
                                        "color": "#666666",
                                        "wrap": True,
                                        "margin": "md"
                                    }
                                ]
                            },
                            # Dementia Warning Card
                            {
                                "type": "box",
                                "layout": "vertical",
                                "flex": 1,
                                "backgroundColor": "#FFF3E0",
                                "borderColor": self.design.PRIMARY_ORANGE,
                                "borderWidth": "2px",
                                "cornerRadius": "12px",
                                "paddingAll": "16px",
                                "contents": [
                                    {
                                        "type": "box",
                                        "layout": "horizontal",
                                        "contents": [
                                            {
                                                "type": "text",
                                                "text": "⚠",
                                                "color": self.design.PRIMARY_ORANGE,
                                                "size": "lg",
                                                "flex": 0
                                            },
                                            {
                                                "type": "text",
                                                "text": "失智警訊",
                                                "weight": "bold",
                                                "size": "sm",
                                                "color": self.design.PRIMARY_ORANGE,
                                                "margin": "sm"
                                            }
                                        ]
                                    },
                                    {
                                        "type": "text",
                                        "text": primary_item.get("dementia_warning", "記憶力減退影響生活，常重複發問") if primary_item else "記憶力減退影響生活，常重複發問",
                                        "size": "xs",
                                        "color": "#666666",
                                        "wrap": True,
                                        "margin": "md"
                                    }
                                ]
                            }
                        ]
                    }
                ]
            },
            "footer": {
                "type": "box",
                "layout": "vertical",
                "backgroundColor": self.design.BG_SUBTLE,
                "paddingAll": "12px",
                "contents": [
                    {
                        "type": "button",
                        "action": {
                            "type": "uri",
                            "label": "查看完整分析報告",
                            "uri": "https://line.me/R/ti/p/@your-bot-id"
                        },
                        "style": "primary",
                        "color": self.design.PRIMARY_BLUE
                    }
                ]
            }
        }
    
    def create_m2_progression_matrix(self, result: AnalysisResult) -> Dict:
        """M2: 病程階段對照 (Based on 照護任務導航 reference)"""
        
        # Get stage information
        current_stage = result.matched_items[0] if result.matched_items else {"stage": "early", "progress": 30}
        stage_info = self._get_stage_info(current_stage.get("stage", "early"))
        
        return {
            "type": "bubble",
            "size": "mega",
            "header": {
                "type": "box",
                "layout": "vertical",
                "backgroundColor": self.design.PRIMARY_BLUE,
                "paddingAll": "16px",
                "contents": [
                    {
                        "type": "text",
                        "text": "🏥 病程階段分析",
                        "weight": "bold",
                        "size": "lg",
                        "color": "#ffffff"
                    },
                    {
                        "type": "text",
                        "text": f"當前階段：{stage_info['name']}",
                        "size": "sm",
                        "color": "#ffffff",
                        "margin": "sm"
                    }
                ]
            },
            "body": {
                "type": "box",
                "layout": "vertical",
                "spacing": "md",
                "paddingAll": "16px",
                "contents": [
                    # Progress Indicator
                    {
                        "type": "box",
                        "layout": "vertical",
                        "spacing": "sm",
                        "contents": [
                            {
                                "type": "text",
                                "text": "病程進展",
                                "size": "sm",
                                "weight": "bold",
                                "color": "#666666"
                            },
                            {
                                "type": "box",
                                "layout": "horizontal",
                                "spacing": "sm",
                                "contents": self._create_stage_progress(current_stage.get("stage", "early"))
                            }
                        ]
                    },
                    # Stage Details
                    {
                        "type": "box",
                        "layout": "vertical",
                        "backgroundColor": stage_info["bg_color"],
                        "cornerRadius": "12px",
                        "paddingAll": "16px",
                        "contents": [
                            {
                                "type": "text",
                                "text": stage_info["name"],
                                "weight": "bold",
                                "size": "lg",
                                "color": stage_info["text_color"]
                            },
                            {
                                "type": "text",
                                "text": stage_info["description"],
                                "size": "sm",
                                "wrap": True,
                                "margin": "sm",
                                "color": stage_info["text_color"]
                            }
                        ]
                    }
                ]
            },
            "footer": {
                "type": "box",
                "layout": "vertical",
                "backgroundColor": self.design.BG_SUBTLE,
                "paddingAll": "12px",
                "contents": [
                    {
                        "type": "button",
                        "action": {
                            "type": "uri",
                            "label": "查看照護建議",
                            "uri": "https://line.me/R/ti/p/@your-bot-id"
                        },
                        "style": "primary",
                        "color": stage_info["button_color"]
                    }
                ]
            }
        }
    
    def create_m3_bpsd_classification(self, result: AnalysisResult) -> Dict:
        """M3: BPSD 症狀分類 (Based on 精神行為症狀 reference)"""
        
        # Group symptoms by category
        symptom_categories = self._group_symptoms_by_category(result.matched_items)
        
        return {
            "type": "bubble",
            "size": "mega",
            "header": {
                "type": "box",
                "layout": "vertical",
                "backgroundColor": "#9C27B0",
                "paddingAll": "16px",
                "contents": [
                    {
                        "type": "text",
                        "text": "🧠 BPSD 症狀分析",
                        "weight": "bold",
                        "size": "lg",
                        "color": "#ffffff"
                    },
                    {
                        "type": "text",
                        "text": f"檢測到 {len(result.matched_items)} 項症狀",
                        "size": "sm",
                        "color": "#ffffff",
                        "margin": "sm"
                    }
                ]
            },
            "body": {
                "type": "box",
                "layout": "vertical",
                "spacing": "md",
                "paddingAll": "16px",
                "contents": [
                    # Symptom Grid
                    {
                        "type": "box",
                        "layout": "vertical",
                        "spacing": "sm",
                        "contents": self._create_symptom_grid(symptom_categories)
                    }
                ]
            },
            "footer": {
                "type": "box",
                "layout": "vertical",
                "backgroundColor": self.design.BG_SUBTLE,
                "paddingAll": "12px",
                "contents": [
                    {
                        "type": "button",
                        "action": {
                            "type": "uri",
                            "label": "查看症狀詳情",
                            "uri": "https://line.me/R/ti/p/@your-bot-id"
                        },
                        "style": "primary",
                        "color": "#9C27B0"
                    }
                ]
            }
        }
    
    def create_m4_care_navigation(self, result: AnalysisResult) -> Dict:
        """M4: 任務導航儀表板 (Based on 病程階段對照 reference)"""
        
        # Get care tasks
        care_tasks = result.matched_items if result.matched_items else []
        
        return {
            "type": "bubble",
            "size": "mega",
            "header": {
                "type": "box",
                "layout": "vertical",
                "backgroundColor": self.design.PRIMARY_GREEN,
                "paddingAll": "16px",
                "contents": [
                    {
                        "type": "text",
                        "text": "📊 照護任務導航",
                        "weight": "bold",
                        "size": "lg",
                        "color": "#ffffff"
                    },
                    {
                        "type": "text",
                        "text": f"共 {len(care_tasks)} 項任務",
                        "size": "sm",
                        "color": "#ffffff",
                        "margin": "sm"
                    }
                ]
            },
            "body": {
                "type": "box",
                "layout": "vertical",
                "spacing": "md",
                "paddingAll": "16px",
                "contents": [
                    # Task List
                    {
                        "type": "box",
                        "layout": "vertical",
                        "spacing": "sm",
                        "contents": self._create_care_task_list(care_tasks)
                    }
                ]
            },
            "footer": {
                "type": "box",
                "layout": "vertical",
                "backgroundColor": self.design.BG_SUBTLE,
                "paddingAll": "12px",
                "contents": [
                    {
                        "type": "button",
                        "action": {
                            "type": "uri",
                            "label": "查看完整任務清單",
                            "uri": "https://line.me/R/ti/p/@your-bot-id"
                        },
                        "style": "primary",
                        "color": self.design.PRIMARY_GREEN
                    }
                ]
            }
        }
    
    def _get_confidence_level(self, percentage: int) -> Dict:
        """Get confidence level information"""
        if percentage >= 75:
            return {
                "color": self.design.CONFIDENCE_HIGH,
                "label": "高信心度"
            }
        elif percentage >= 50:
            return {
                "color": self.design.CONFIDENCE_MEDIUM,
                "label": "中信心度"
            }
        else:
            return {
                "color": self.design.CONFIDENCE_LOW,
                "label": "需人工確認"
            }
    
    def _get_stage_info(self, stage: str) -> Dict:
        """Get stage information for M2"""
        stage_map = {
            "early": {
                "name": "早期階段",
                "description": "輕微記憶力減退，日常生活能力正常",
                "bg_color": "#E8F5E9",
                "text_color": self.design.PRIMARY_GREEN,
                "button_color": self.design.PRIMARY_GREEN
            },
            "middle": {
                "name": "中期階段",
                "description": "明顯記憶力減退，需要協助處理日常事務",
                "bg_color": "#FFF3E0",
                "text_color": self.design.PRIMARY_ORANGE,
                "button_color": self.design.PRIMARY_ORANGE
            },
            "late": {
                "name": "晚期階段",
                "description": "嚴重認知功能障礙，需要全天候照護",
                "bg_color": "#FFEBEE",
                "text_color": self.design.PRIMARY_RED,
                "button_color": self.design.PRIMARY_RED
            }
        }
        return stage_map.get(stage, stage_map["early"])
    
    def _create_stage_progress(self, current_stage: str) -> List[Dict]:
        """Create stage progress indicator"""
        stages = ["early", "middle", "late"]
        current_index = stages.index(current_stage) if current_stage in stages else 0
        
        progress_items = []
        for i, stage in enumerate(stages):
            stage_info = self._get_stage_info(stage)
            
            if i <= current_index:
                # Completed or current stage
                dot_color = stage_info["text_color"]
                line_color = stage_info["text_color"] if i < current_index else "#E0E0E0"
            else:
                # Upcoming stage
                dot_color = "#E0E0E0"
                line_color = "#E0E0E0"
            
            progress_items.append({
                "type": "box",
                "layout": "vertical",
                "flex": 1,
                "contents": [
                    {
                        "type": "box",
                        "width": "32px",
                        "height": "32px",
                        "backgroundColor": dot_color,
                        "cornerRadius": "16px",
                        "alignSelf": "center"
                    },
                    {
                        "type": "text",
                        "text": stage_info["name"],
                        "size": "xs",
                        "color": dot_color,
                        "align": "center",
                        "margin": "sm"
                    }
                ]
            })
            
            # Add connecting line (except for last item)
            if i < len(stages) - 1:
                progress_items.append({
                    "type": "box",
                    "flex": 1,
                    "height": "2px",
                    "backgroundColor": line_color,
                    "alignSelf": "center"
                })
        
        return progress_items
    
    def _group_symptoms_by_category(self, symptoms: List[Dict]) -> Dict:
        """Group symptoms by category for M3"""
        categories = {
            "躁動不安": {"color": "#FF5252", "symptoms": []},
            "憂鬱情緒": {"color": "#2196F3", "symptoms": []},
            "幻覺症狀": {"color": "#9C27B0", "symptoms": []},
            "妄想症狀": {"color": "#FF9800", "symptoms": []}
        }
        
        for symptom in symptoms:
            category = symptom.get("category", "其他")
            if category in categories:
                categories[category]["symptoms"].append(symptom)
        
        return categories
    
    def _create_symptom_grid(self, categories: Dict) -> List[Dict]:
        """Create symptom grid for M3"""
        grid_contents = []
        
        for category_name, category_info in categories.items():
            if not category_info["symptoms"]:
                continue
                
            # Create category card
            card_contents = []
            for symptom in category_info["symptoms"][:2]:  # Limit to 2 symptoms per card
                confidence = int(symptom.get("confidence", 0.5) * 100)
                
                card_contents.append({
                    "type": "box",
                    "layout": "horizontal",
                    "contents": [
                        {
                            "type": "text",
                            "text": symptom.get("name", "症狀"),
                            "size": "sm",
                            "flex": 1,
                            "wrap": True
                        },
                        {
                            "type": "box",
                            "backgroundColor": "#F5F5F5",
                            "cornerRadius": "12px",
                            "paddingAll": "4px",
                            "contents": [
                                {
                                    "type": "text",
                                    "text": f"{confidence}%",
                                    "size": "xs",
                                    "color": category_info["color"],
                                    "weight": "bold"
                                }
                            ]
                        }
                    ],
                    "margin": "sm"
                })
            
            if card_contents:
                grid_contents.append({
                    "type": "box",
                    "layout": "vertical",
                    "flex": 1,
                    "backgroundColor": self.design.BG_CARD,
                    "cornerRadius": "12px",
                    "paddingAll": "16px",
                    "borderWidth": "1px",
                    "borderColor": "#E0E0E0",
                    "borderLeftWidth": "4px",
                    "borderLeftColor": category_info["color"],
                    "contents": [
                        {
                            "type": "text",
                            "text": category_name,
                            "weight": "bold",
                            "size": "sm",
                            "color": category_info["color"],
                            "margin": "sm"
                        }
                    ] + card_contents
                })
        
        return grid_contents
    
    def _create_care_task_list(self, tasks: List[Dict]) -> List[Dict]:
        """Create care task list for M4"""
        task_contents = []
        
        for task in tasks[:5]:  # Limit to 5 tasks
            priority_color = {
                "high": self.design.PRIMARY_RED,
                "medium": self.design.PRIMARY_ORANGE,
                "low": self.design.PRIMARY_GREEN
            }.get(task.get("priority", "medium"), self.design.PRIMARY_ORANGE)
            
            task_contents.append({
                "type": "box",
                "layout": "horizontal",
                "backgroundColor": self.design.BG_CARD,
                "cornerRadius": "8px",
                "paddingAll": "16px",
                "margin": "sm",
                "contents": [
                    {
                        "type": "box",
                        "width": "40px",
                        "height": "40px",
                        "backgroundColor": priority_color,
                        "cornerRadius": "8px",
                        "alignSelf": "center",
                        "contents": [
                            {
                                "type": "text",
                                "text": task.get("icon", "📋"),
                                "align": "center",
                                "color": "#ffffff"
                            }
                        ]
                    },
                    {
                        "type": "box",
                        "layout": "vertical",
                        "flex": 1,
                        "margin": "sm",
                        "contents": [
                            {
                                "type": "text",
                                "text": task.get("title", "照護任務"),
                                "weight": "bold",
                                "size": "sm"
                            },
                            {
                                "type": "text",
                                "text": task.get("description", "任務描述"),
                                "size": "xs",
                                "color": "#666666",
                                "wrap": True
                            }
                        ]
                    },
                    {
                        "type": "button",
                        "action": {
                            "type": "uri",
                            "label": "查看",
                            "uri": "https://line.me/R/ti/p/@your-bot-id"
                        },
                        "style": "link",
                        "color": priority_color,
                        "height": "sm"
                    }
                ]
            })
        
        return task_contents

# Factory function for creating flex messages
def create_enhanced_flex_message(module: str, result: AnalysisResult) -> Dict:
    """Create enhanced flex message based on module type"""
    generator = EnhancedFlexMessageGenerator()
    
    if module == "M1":
        return generator.create_m1_warning_signs_card(result)
    elif module == "M2":
        return generator.create_m2_progression_matrix(result)
    elif module == "M3":
        return generator.create_m3_bpsd_classification(result)
    elif module == "M4":
        return generator.create_m4_care_navigation(result)
    else:
        # Default fallback
        return generator.create_m1_warning_signs_card(result) 