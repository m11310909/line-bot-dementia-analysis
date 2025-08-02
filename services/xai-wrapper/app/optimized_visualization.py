"""
🎯 Optimized M1-M4 Visualization Module
Implements performance-optimized XAI visualizations with progressive loading
"""

import time
import json
from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from enum import Enum

class ConfidenceLevel(Enum):
    HIGH = "high"      # >80%
    MEDIUM = "medium"  # 60-80%
    LOW = "low"        # <60%

class VisualizationStage(Enum):
    IMMEDIATE = "immediate"  # <1秒
    QUICK = "quick"         # <3秒
    DETAILED = "detailed"   # LIFF載入

@dataclass
class VisualizationConfig:
    """視覺化配置"""
    max_bubble_size: int = 5000  # 5KB limit
    max_nesting_levels: int = 3
    use_unicode_symbols: bool = True
    progressive_loading: bool = True
    show_original_response: bool = True  # 顯示原始回應

class OptimizedVisualizationGenerator:
    """優化的視覺化生成器"""
    
    def __init__(self):
        self.config = VisualizationConfig()
        self.cache = {}
        self.confidence_colors = {
            ConfidenceLevel.HIGH: "#4CAF50",
            ConfidenceLevel.MEDIUM: "#2196F3", 
            ConfidenceLevel.LOW: "#FF9800"
        }
        
        # 預存常見症狀組合
        self.preset_symptom_patterns = {
            "memory_repetition": {
                "keywords": ["重複", "忘記", "重複問"],
                "confidence": 0.85,
                "treatment": "環境調整 + 記憶輔助"
            },
            "behavioral_agitation": {
                "keywords": ["躁動", "攻擊", "不安"],
                "confidence": 0.78,
                "treatment": "藥物介入 + 行為療法"
            },
            "care_navigation": {
                "keywords": ["醫療", "協助", "照顧"],
                "confidence": 0.82,
                "treatment": "專業照護資源"
            }
        }
    
    def get_confidence_level(self, score: float) -> ConfidenceLevel:
        """獲取信心度等級"""
        if score > 0.8:
            return ConfidenceLevel.HIGH
        elif score > 0.6:
            return ConfidenceLevel.MEDIUM
        else:
            return ConfidenceLevel.LOW
    
    def create_collapsible_section(self, title: str, content: List[Dict], is_expanded: bool = False) -> Dict[str, Any]:
        """創建可收合的區塊"""
        return {
            "type": "box",
            "layout": "vertical",
            "spacing": "sm",
            "contents": [
                {
                    "type": "box",
                    "layout": "horizontal",
                    "contents": [
                        {
                            "type": "text",
                            "text": title,
                            "weight": "bold",
                            "size": "sm",
                            "color": "#333333",
                            "flex": 1
                        },
                        {
                            "type": "text",
                            "text": "▼" if is_expanded else "▶",
                            "size": "sm",
                            "color": "#666666"
                        }
                    ],
                    "action": {
                        "type": "postback",
                        "label": "toggle",
                        "data": f"toggle_{title.lower().replace(' ', '_')}"
                    }
                },
                {
                    "type": "box",
                    "layout": "vertical",
                    "spacing": "sm",
                    "contents": content,
                    "margin": "sm" if is_expanded else "none",
                    "display": "flex" if is_expanded else "none"
                }
            ]
        }
    
    def create_original_response_section(self, original_response: Dict[str, Any]) -> Dict[str, Any]:
        """創建原始回應區塊"""
        # 提取原始回應的內容
        original_content = ""
        if "contents" in original_response:
            contents = original_response["contents"]
            if "body" in contents:
                body = contents["body"]
                if "contents" in body:
                    for item in body["contents"]:
                        if "text" in item:
                            original_content += item["text"] + "\n"
        
        return {
            "type": "box",
            "layout": "vertical",
            "spacing": "sm",
            "contents": [
                {
                    "type": "text",
                    "text": "🤖 失智小幫手原始回應",
                    "weight": "bold",
                    "size": "sm",
                    "color": "#666666"
                },
                {
                    "type": "text",
                    "text": original_content.strip() if original_content else "無原始回應",
                    "size": "xs",
                    "color": "#999999",
                    "wrap": True
                }
            ],
            "backgroundColor": "#F8F9FA",
            "paddingAll": "8px",
            "cornerRadius": "8px"
        }
    
    def create_xai_analysis_section(self, xai_data: Dict[str, Any]) -> Dict[str, Any]:
        """創建 XAI 分析區塊"""
        confidence = xai_data.get("confidence", 0.0)
        module = xai_data.get("module", "unknown")
        keywords = xai_data.get("keywords", {})
        
        confidence_level = self.get_confidence_level(confidence)
        confidence_color = self.confidence_colors[confidence_level]
        
        analysis_contents = [
            {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                    {
                        "type": "text",
                        "text": "🎯 檢測模組",
                        "size": "xs",
                        "color": "#666666",
                        "flex": 1
                    },
                    {
                        "type": "text",
                        "text": module,
                        "size": "xs",
                        "color": confidence_color,
                        "weight": "bold"
                    }
                ]
            },
            {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                    {
                        "type": "text",
                        "text": "📊 信心度",
                        "size": "xs",
                        "color": "#666666",
                        "flex": 1
                    },
                    {
                        "type": "text",
                        "text": f"{confidence:.1%}",
                        "size": "xs",
                        "color": confidence_color,
                        "weight": "bold"
                    }
                ]
            }
        ]
        
        # 添加關鍵詞
        if keywords:
            keyword_text = "、".join(list(keywords.keys())[:3])
            analysis_contents.append({
                "type": "box",
                "layout": "horizontal",
                "contents": [
                    {
                        "type": "text",
                        "text": "🔍 關鍵詞",
                        "size": "xs",
                        "color": "#666666",
                        "flex": 1
                    },
                    {
                        "type": "text",
                        "text": keyword_text,
                        "size": "xs",
                        "color": "#666666"
                    }
                ]
            })
        
        return {
            "type": "box",
            "layout": "vertical",
            "spacing": "sm",
            "contents": [
                {
                    "type": "text",
                    "text": "🧠 XAI 分析結果",
                    "weight": "bold",
                    "size": "sm",
                    "color": "#333333"
                }
            ] + analysis_contents,
            "backgroundColor": "#E3F2FD",
            "paddingAll": "8px",
            "cornerRadius": "8px"
        }
    
    def generate_m1_warning_signs(self, xai_data: Dict[str, Any], original_response: Dict[str, Any] = None, stage: VisualizationStage = VisualizationStage.IMMEDIATE) -> Dict[str, Any]:
        """生成 M1 十大警訊比對卡"""
        confidence = xai_data.get("confidence", 0.0)
        keywords = xai_data.get("keywords", {})
        
        # 基礎推理路徑
        reasoning_steps = [
            {"step": "關鍵詞標記", "confidence": 0.9, "description": f"識別關鍵詞: {list(keywords.keys())}"},
            {"step": "症狀分類", "confidence": 0.85, "description": "分類為記憶相關症狀"},
            {"step": "警訊判斷", "confidence": confidence, "description": "判定為M1警訊"}
        ]
        
        # 證據高亮
        evidence_highlights = []
        for keyword, score in keywords.items():
            evidence_highlights.append({
                "text": keyword,
                "importance": score,
                "highlighted": True
            })
        
        # 根據階段生成不同複雜度的視覺化
        if stage == VisualizationStage.IMMEDIATE:
            return self._generate_m1_immediate(confidence, evidence_highlights, original_response)
        elif stage == VisualizationStage.QUICK:
            return self._generate_m1_quick(confidence, reasoning_steps, evidence_highlights, original_response)
        else:
            return self._generate_m1_detailed(confidence, reasoning_steps, evidence_highlights, original_response)
    
    def _generate_m1_immediate(self, confidence: float, evidence_highlights: List[Dict], original_response: Dict[str, Any] = None) -> Dict[str, Any]:
        """生成 M1 即時視覺化 (<1秒)"""
        confidence_level = self.get_confidence_level(confidence)
        confidence_color = self.confidence_colors[confidence_level]
        
        # 簡化的證據顯示
        evidence_text = "、".join([item["text"] for item in evidence_highlights[:3]])
        
        # 主要內容
        main_contents = [
            {
                "type": "text",
                "text": f"檢測到關鍵詞：{evidence_text}",
                "size": "sm",
                "color": "#666666",
                "wrap": True
            },
            {
                "type": "separator"
            },
            {
                "type": "text",
                "text": "整體信心度",
                "size": "sm",
                "color": "#333333"
            },
            {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                    {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {
                                "type": "text",
                                "text": "█" * int(confidence * 10) + "░" * (10 - int(confidence * 10)),
                                "size": "sm",
                                "color": confidence_color
                            }
                        ]
                    },
                    {
                        "type": "text",
                        "text": f"{confidence:.0%}",
                        "size": "sm",
                        "color": confidence_color,
                        "weight": "bold"
                    }
                ]
            }
        ]
        
        # 添加可收合的詳細資訊
        if self.config.show_original_response and original_response:
            main_contents.append({
                "type": "separator"
            })
            main_contents.append(
                self.create_collapsible_section("📋 詳細分析", [
                    self.create_xai_analysis_section({"confidence": confidence, "module": "M1", "keywords": evidence_highlights}),
                    self.create_original_response_section(original_response)
                ])
            )
        
        return {
            "type": "flex",
            "altText": "M1 警訊分析 - 即時結果",
            "contents": {
                "type": "bubble",
                "size": "kilo",
                "header": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "text",
                            "text": "🧠 AI 分析：記憶力評估",
                            "weight": "bold",
                            "color": "#ffffff",
                            "size": "lg"
                        },
                        {
                            "type": "text",
                            "text": f"信心度: {confidence:.0%}",
                            "color": "#ffffff",
                            "size": "sm"
                        }
                    ],
                    "backgroundColor": confidence_color
                },
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "spacing": "md",
                    "contents": main_contents
                }
            }
        }
    
    def _generate_m1_quick(self, confidence: float, reasoning_steps: List[Dict], evidence_highlights: List[Dict], original_response: Dict[str, Any] = None) -> Dict[str, Any]:
        """生成 M1 快速視覺化 (<3秒)"""
        confidence_level = self.get_confidence_level(confidence)
        confidence_color = self.confidence_colors[confidence_level]
        
        # 推理路徑視覺化
        reasoning_contents = []
        for i, step in enumerate(reasoning_steps):
            step_color = "#FFF3E0" if step["confidence"] > 0.8 else "#F5F5F5"
            reasoning_contents.append({
                "type": "box",
                "layout": "horizontal",
                "contents": [
                    {
                        "type": "text",
                        "text": f"• {step['step']}",
                        "size": "sm",
                        "color": "#333333",
                        "flex": 1
                    },
                    {
                        "type": "text",
                        "text": f"{step['confidence']:.0%}",
                        "size": "xs",
                        "color": confidence_color
                    }
                ],
                "backgroundColor": step_color,
                "paddingAll": "8px",
                "cornerRadius": "20px",
                "margin": "4px"
            })
        
        # 主要內容
        main_contents = [
            {
                "type": "text",
                "text": "推理路徑：",
                "weight": "bold",
                "size": "sm",
                "color": "#333333"
            }
        ] + reasoning_contents + [
            {
                "type": "separator"
            },
            {
                "type": "text",
                "text": "💡 建議：及早發現，及早介入",
                "size": "sm",
                "color": "#666666",
                "wrap": True
            }
        ]
        
        # 添加可收合的詳細資訊
        if self.config.show_original_response and original_response:
            main_contents.append({
                "type": "separator"
            })
            main_contents.append(
                self.create_collapsible_section("📋 詳細分析", [
                    self.create_xai_analysis_section({"confidence": confidence, "module": "M1", "keywords": evidence_highlights}),
                    self.create_original_response_section(original_response)
                ])
            )
        
        return {
            "type": "flex",
            "altText": "M1 警訊分析 - 詳細結果",
            "contents": {
                "type": "bubble",
                "size": "kilo",
                "header": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "text",
                            "text": "🧠 AI 分析：記憶力評估",
                            "weight": "bold",
                            "color": "#ffffff",
                            "size": "lg"
                        },
                        {
                            "type": "text",
                            "text": f"信心度: {confidence:.0%}",
                            "color": "#ffffff",
                            "size": "sm"
                        }
                    ],
                    "backgroundColor": confidence_color
                },
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "spacing": "md",
                    "contents": main_contents
                }
            }
        }
    
    def _generate_m1_detailed(self, confidence: float, reasoning_steps: List[Dict], evidence_highlights: List[Dict], original_response: Dict[str, Any] = None) -> Dict[str, Any]:
        """生成 M1 詳細視覺化 (LIFF載入)"""
        # 這裡可以包含更複雜的視覺化，如圖表、互動元素等
        # 目前返回快速版本，實際應用中可以擴展
        return self._generate_m1_quick(confidence, reasoning_steps, evidence_highlights, original_response)
    
    def generate_m2_progression(self, xai_data: Dict[str, Any], original_response: Dict[str, Any] = None, stage: VisualizationStage = VisualizationStage.IMMEDIATE) -> Dict[str, Any]:
        """生成 M2 病程階段對照"""
        confidence = xai_data.get("confidence", 0.0)
        keywords = xai_data.get("keywords", {})
        
        # 簡化版 Aspect 評估
        aspect_scores = {
            "症狀吻合": min(confidence + 0.05, 1.0),
            "特徵符合": max(confidence - 0.1, 0.0),
            "進展合理": confidence
        }
        
        # 階段判斷
        if confidence > 0.8:
            stage_name = "晚期階段"
        elif confidence > 0.6:
            stage_name = "中期階段"
        else:
            stage_name = "早期階段"
        
        confidence_level = self.get_confidence_level(confidence)
        confidence_color = self.confidence_colors[confidence_level]
        
        # 雷達圖視覺化（簡化版）
        radar_contents = []
        for aspect, score in aspect_scores.items():
            radar_contents.append({
                "type": "box",
                "layout": "horizontal",
                "contents": [
                    {
                        "type": "text",
                        "text": aspect,
                        "size": "sm",
                        "color": "#333333",
                        "flex": 1
                    },
                    {
                        "type": "text",
                        "text": "█" * int(score * 10) + "░" * (10 - int(score * 10)),
                        "size": "sm",
                        "color": confidence_color
                    },
                    {
                        "type": "text",
                        "text": f"{score:.0%}",
                        "size": "xs",
                        "color": confidence_color
                    }
                ]
            })
        
        # 主要內容
        main_contents = radar_contents + [
            {
                "type": "separator"
            },
            {
                "type": "text",
                "text": f"整體信心度：{confidence:.0%}",
                "size": "sm",
                "color": "#333333",
                "weight": "bold"
            },
            {
                "type": "text",
                "text": "💡 建議：定期追蹤病程變化",
                "size": "sm",
                "color": "#666666",
                "wrap": True
            }
        ]
        
        # 添加可收合的詳細資訊
        if self.config.show_original_response and original_response:
            main_contents.append({
                "type": "separator"
            })
            main_contents.append(
                self.create_collapsible_section("📋 詳細分析", [
                    self.create_xai_analysis_section({"confidence": confidence, "module": "M2", "keywords": keywords}),
                    self.create_original_response_section(original_response)
                ])
            )
        
        return {
            "type": "flex",
            "altText": "M2 病程階段分析",
            "contents": {
                "type": "bubble",
                "size": "kilo",
                "header": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "text",
                            "text": "📈 階段評估雷達圖",
                            "weight": "bold",
                            "color": "#ffffff",
                            "size": "lg"
                        },
                        {
                            "type": "text",
                            "text": f"判斷：{stage_name}",
                            "color": "#ffffff",
                            "size": "sm"
                        }
                    ],
                    "backgroundColor": confidence_color
                },
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "spacing": "md",
                    "contents": main_contents
                }
            }
        }
    
    def generate_m3_bpsd_symptoms(self, xai_data: Dict[str, Any], original_response: Dict[str, Any] = None, stage: VisualizationStage = VisualizationStage.IMMEDIATE) -> Dict[str, Any]:
        """生成 M3 BPSD 症狀分類"""
        confidence = xai_data.get("confidence", 0.0)
        keywords = xai_data.get("keywords", {})
        
        # 預存處理方案
        treatment_options = [
            {
                "name": "環境調整",
                "rating": 5,
                "confidence": 0.85,
                "description": "最少副作用"
            },
            {
                "name": "藥物介入",
                "rating": 3,
                "confidence": 0.65,
                "description": "需要醫師評估"
            },
            {
                "name": "行為療法",
                "rating": 4,
                "confidence": 0.75,
                "description": "長期效果佳"
            }
        ]
        
        # 選擇最佳方案
        best_option = max(treatment_options, key=lambda x: x["confidence"])
        
        confidence_level = self.get_confidence_level(confidence)
        confidence_color = self.confidence_colors[confidence_level]
        
        # 方案比較視覺化
        options_contents = []
        for option in treatment_options:
            stars = "⭐" * option["rating"] + "☆" * (5 - option["rating"])
            options_contents.append({
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": f"方案：{option['name']} {stars}",
                        "size": "sm",
                        "color": "#333333"
                    },
                    {
                        "type": "text",
                        "text": f"信心度：{option['confidence']:.0%}",
                        "size": "xs",
                        "color": confidence_color
                    }
                ],
                "margin": "4px"
            })
        
        # 主要內容
        main_contents = options_contents + [
            {
                "type": "separator"
            },
            {
                "type": "text",
                "text": f"推薦理由：{best_option['description']}",
                "size": "sm",
                "color": "#666666",
                "wrap": True
            },
            {
                "type": "text",
                "text": "💡 建議：尋求精神科醫師協助",
                "size": "sm",
                "color": "#666666",
                "wrap": True
            }
        ]
        
        # 添加可收合的詳細資訊
        if self.config.show_original_response and original_response:
            main_contents.append({
                "type": "separator"
            })
            main_contents.append(
                self.create_collapsible_section("📋 詳細分析", [
                    self.create_xai_analysis_section({"confidence": confidence, "module": "M3", "keywords": keywords}),
                    self.create_original_response_section(original_response)
                ])
            )
        
        return {
            "type": "flex",
            "altText": "M3 BPSD 症狀分析",
            "contents": {
                "type": "bubble",
                "size": "kilo",
                "header": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "text",
                            "text": "🎯 處理方案建議",
                            "weight": "bold",
                            "color": "#ffffff",
                            "size": "lg"
                        },
                        {
                            "type": "text",
                            "text": f"AI 推薦：{best_option['name']}",
                            "color": "#ffffff",
                            "size": "sm"
                        }
                    ],
                    "backgroundColor": confidence_color
                },
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "spacing": "md",
                    "contents": main_contents
                }
            }
        }
    
    def generate_m4_care_navigation(self, xai_data: Dict[str, Any], original_response: Dict[str, Any] = None, stage: VisualizationStage = VisualizationStage.IMMEDIATE) -> Dict[str, Any]:
        """生成 M4 任務導航"""
        confidence = xai_data.get("confidence", 0.0)
        keywords = xai_data.get("keywords", {})
        
        # 任務狀態
        tasks = [
            {"name": "醫療任務", "status": "active", "description": "預約神經科評估"},
            {"name": "日常照護", "status": "pending", "description": "建立照護計劃"},
            {"name": "社交支持", "status": "future", "description": "加入支持團體"}
        ]
        
        confidence_level = self.get_confidence_level(confidence)
        confidence_color = self.confidence_colors[confidence_level]
        
        # 任務導航視覺化
        task_contents = []
        for task in tasks:
            status_icon = "●" if task["status"] == "active" else "○"
            status_color = "#4CAF50" if task["status"] == "active" else "#999999"
            
            task_contents.append({
                "type": "box",
                "layout": "horizontal",
                "contents": [
                    {
                        "type": "text",
                        "text": status_icon,
                        "size": "sm",
                        "color": status_color
                    },
                    {
                        "type": "text",
                        "text": task["name"],
                        "size": "sm",
                        "color": "#333333",
                        "flex": 1
                    },
                    {
                        "type": "text",
                        "text": f"({task['status']})",
                        "size": "xs",
                        "color": status_color
                    }
                ]
            })
        
        # 主要內容
        main_contents = task_contents + [
            {
                "type": "separator"
            },
            {
                "type": "text",
                "text": "下一步：預約神經科評估",
                "size": "sm",
                "color": "#333333",
                "weight": "bold"
            },
            {
                "type": "text",
                "text": "預計時間：本週內完成",
                "size": "xs",
                "color": "#666666"
            },
            {
                "type": "text",
                "text": "💡 建議：尋求專業照護資源",
                "size": "sm",
                "color": "#666666",
                "wrap": True
            }
        ]
        
        # 添加可收合的詳細資訊
        if self.config.show_original_response and original_response:
            main_contents.append({
                "type": "separator"
            })
            main_contents.append(
                self.create_collapsible_section("📋 詳細分析", [
                    self.create_xai_analysis_section({"confidence": confidence, "module": "M4", "keywords": keywords}),
                    self.create_original_response_section(original_response)
                ])
            )
        
        return {
            "type": "flex",
            "altText": "M4 照護需求分析",
            "contents": {
                "type": "bubble",
                "size": "kilo",
                "header": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "text",
                            "text": "📍 當前任務導航",
                            "weight": "bold",
                            "color": "#ffffff",
                            "size": "lg"
                        },
                        {
                            "type": "text",
                            "text": f"優先級：{confidence:.0%}",
                            "color": "#ffffff",
                            "size": "sm"
                        }
                    ],
                    "backgroundColor": confidence_color
                },
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "spacing": "md",
                    "contents": main_contents
                }
            }
        }
    
    def generate_visualization(self, module: str, xai_data: Dict[str, Any], original_response: Dict[str, Any] = None, stage: VisualizationStage = VisualizationStage.IMMEDIATE) -> Dict[str, Any]:
        """生成優化的視覺化"""
        start_time = time.time()
        
        try:
            if module == "M1":
                result = self.generate_m1_warning_signs(xai_data, original_response, stage)
            elif module == "M2":
                result = self.generate_m2_progression(xai_data, original_response, stage)
            elif module == "M3":
                result = self.generate_m3_bpsd_symptoms(xai_data, original_response, stage)
            elif module == "M4":
                result = self.generate_m4_care_navigation(xai_data, original_response, stage)
            else:
                result = self.generate_m1_warning_signs(xai_data, original_response, stage)  # 預設
            
            # 效能監控
            generation_time = time.time() - start_time
            if generation_time > 1.0:  # 超過1秒警告
                print(f"⚠️ 視覺化生成時間過長: {generation_time:.2f}秒")
            
            return result
            
        except Exception as e:
            print(f"❌ 視覺化生成錯誤: {e}")
            # 返回簡化的錯誤視覺化
            return {
                "type": "flex",
                "altText": "分析結果",
                "contents": {
                    "type": "bubble",
                    "size": "kilo",
                    "body": {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {
                                "type": "text",
                                "text": "抱歉，視覺化生成失敗",
                                "size": "md",
                                "color": "#FF0000"
                            }
                        ]
                    }
                }
            }

# 快取管理器
class VisualizationCache:
    """視覺化快取管理器"""
    
    def __init__(self):
        self.cache = {}
        self.cache_ttl = {
            "症狀組合": 3600,  # 1小時
            "處理方案": 86400,  # 24小時
        }
    
    def get_cache_key(self, module: str, keywords: Dict[str, float], confidence: float) -> str:
        """生成快取鍵"""
        keyword_str = "_".join(sorted(keywords.keys()))
        confidence_bucket = int(confidence * 10)  # 分組信心度
        return f"{module}_{keyword_str}_{confidence_bucket}"
    
    def get(self, cache_key: str) -> Optional[Dict[str, Any]]:
        """獲取快取"""
        if cache_key in self.cache:
            cached_data = self.cache[cache_key]
            if time.time() - cached_data["timestamp"] < self.cache_ttl.get("症狀組合", 3600):
                return cached_data["data"]
        return None
    
    def set(self, cache_key: str, data: Dict[str, Any]) -> None:
        """設置快取"""
        self.cache[cache_key] = {
            "data": data,
            "timestamp": time.time()
        }
    
    def clear_expired(self) -> None:
        """清理過期快取"""
        current_time = time.time()
        expired_keys = []
        
        for key, value in self.cache.items():
            if current_time - value["timestamp"] > self.cache_ttl.get("症狀組合", 3600):
                expired_keys.append(key)
        
        for key in expired_keys:
            del self.cache[key] 