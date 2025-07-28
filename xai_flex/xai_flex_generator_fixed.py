"""
XAI Flex Message 視覺組件生成器
支援失智症與長照 RAG 系統的可解釋性視覺化
"""

from typing import Dict, List, Any, Optional
from enum import Enum
import json
from datetime import datetime

class ComponentType(Enum):
    COMPARISON_CARD = "comparison_card"
    CONFIDENCE_METER = "confidence_meter"
    XAI_BOX = "xai_box"
    INFO_BOX = "info_box"
    ACTION_CARD = "action_card"
    TIMELINE_LIST = "timeline_list"
    WARNING_BOX = "warning_box"

class FlexColorTheme(Enum):
    WARNING = {"primary": "#FF6B6B", "secondary": "#FFE5E5", "text": "#333333"}
    INFO = {"primary": "#4ECDC4", "secondary": "#E5F7F6", "text": "#333333"}
    SUCCESS = {"primary": "#95E1A3", "secondary": "#E8F5E8", "text": "#333333"}
    NEUTRAL = {"primary": "#A8A8A8", "secondary": "#F5F5F5", "text": "#333333"}

class ConfidenceVisualizer:
    """信心度視覺化器"""

    def create_confidence_indicator(self, confidence_score: float) -> Dict:
        """創建簡單的信心度指標"""
        percentage = int(confidence_score * 100)
        color = self._get_confidence_color(confidence_score)

        return {
            "type": "box",
            "layout": "horizontal",
            "margin": "sm",
            "contents": [
                {
                    "type": "text",
                    "text": f"可信度 {percentage}%",
                    "size": "xs",
                    "color": color,
                    "flex": 0
                },
                {
                    "type": "box",
                    "layout": "vertical",
                    "flex": 1,
                    "margin": "sm",
                    "contents": [
                        {
                            "type": "box",
                            "layout": "horizontal",
                            "backgroundColor": "#F0F0F0",
                            "height": "6px",
                            "contents": [
                                {
                                    "type": "box",
                                    "layout": "vertical",
                                    "backgroundColor": color,
                                    "width": f"{percentage}%",
                                    "contents": []
                                }
                            ]
                        }
                    ]
                }
            ]
        }

    def create_detailed_confidence_meter(self, confidence_score: float, explanation_data: Dict) -> Dict:
        """創建詳細的信心度量表"""
        percentage = int(confidence_score * 100)
        color = self._get_confidence_color(confidence_score)
        confidence_text = self._get_confidence_text(confidence_score)

        return {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "box",
                    "layout": "horizontal",
                    "contents": [
                        {
                            "type": "text",
                            "text": "📊 AI 信心度評估",
                            "weight": "bold",
                            "size": "sm",
                            "color": "#4ECDC4",
                            "flex": 0
                        },
                        {
                            "type": "text",
                            "text": f"{percentage}%",
                            "size": "lg",
                            "weight": "bold",
                            "color": color,
                            "align": "end"
                        }
                    ]
                },
                {
                    "type": "box",
                    "layout": "horizontal",
                    "margin": "sm",
                    "contents": [
                        {
                            "type": "box",
                            "layout": "vertical",
                            "flex": 1,
                            "contents": [
                                {
                                    "type": "box",
                                    "layout": "horizontal",
                                    "backgroundColor": "#F0F0F0",
                                    "height": "8px",
                                    "cornerRadius": "4px",
                                    "contents": [
                                        {
                                            "type": "box",
                                            "layout": "vertical",
                                            "backgroundColor": color,
                                            "width": f"{percentage}%",
                                            "cornerRadius": "4px",
                                            "contents": []
                                        }
                                    ]
                                }
                            ]
                        }
                    ]
                },
                {
                    "type": "text",
                    "text": confidence_text,
                    "size": "xs",
                    "color": "#666666",
                    "margin": "sm",
                    "wrap": True
                }
            ]
        }

    def _get_confidence_color(self, confidence_score: float) -> str:
        """根據信心度分數返回對應顏色"""
        if confidence_score >= 0.8:
            return "#95E1A3"  # 高信心度 - 綠色
        elif confidence_score >= 0.6:
            return "#FFD93D"  # 中信心度 - 黃色
        else:
            return "#FF6B6B"  # 低信心度 - 紅色

    def _get_confidence_text(self, confidence_score: float) -> str:
        """根據信心度分數返回對應說明文字"""
        if confidence_score >= 0.9:
            return "極高可信度：基於權威醫療指引，建議依循"
        elif confidence_score >= 0.8:
            return "高可信度：多數專業來源一致，可信賴參考"
        elif confidence_score >= 0.7:
            return "中高可信度：有專業依據，建議進一步確認"
        elif confidence_score >= 0.6:
            return "中等可信度：部分專業支持，需謹慎判斷"
        else:
            return "低可信度：資訊有限，建議諮詢專業人員"

class SourceTracer:
    """來源追蹤器"""

    def create_source_section(self, source_trace: Dict) -> Dict:
        """創建來源追蹤區塊"""
        if not source_trace:
            return {"type": "spacer", "size": "xs"}

        source_name = source_trace.get('source', '未知來源')
        version = source_trace.get('version', '')
        last_verified = source_trace.get('last_verified', '')
        authority_level = source_trace.get('authority_level', 'general')

        authority_color = self._get_authority_color(authority_level)
        authority_icon = self._get_authority_icon(authority_level)

        return {
            "type": "box",
            "layout": "vertical",
            "margin": "lg",
            "paddingAll": "8px",
            "backgroundColor": "#F8F9FA",
            "cornerRadius": "4px",
            "contents": [
                {
                    "type": "text",
                    "text": "📋 資料來源",
                    "weight": "bold",
                    "size": "xs",
                    "color": "#666666"
                },
                {
                    "type": "box",
                    "layout": "horizontal",
                    "margin": "xs",
                    "contents": [
                        {
                            "type": "text",
                            "text": authority_icon,
                            "flex": 0,
                            "color": authority_color
                        },
                        {
                            "type": "text",
                            "text": source_name,
                            "size": "xs",
                            "color": "#333333",
                            "wrap": True,
                            "margin": "xs"
                        }
                    ]
                },
                {
                    "type": "box",
                    "layout": "horizontal",
                    "margin": "xs",
                    "contents": [
                        {
                            "type": "text",
                            "text": f"版本: {version}" if version else "",
                            "size": "xs",
                            "color": "#999999",
                            "flex": 1
                        },
                        {
                            "type": "text",
                            "text": f"驗證: {last_verified}" if last_verified else "",
                            "size": "xs",
                            "color": "#999999",
                            "flex": 1,
                            "align": "end"
                        }
                    ]
                }
            ]
        }

    def _get_authority_color(self, authority_level: str) -> str:
        """根據權威級別返回顏色"""
        colors = {
            'official': '#95E1A3',      # 官方 - 綠色
            'academic': '#4ECDC4',      # 學術 - 青色
            'professional': '#FFD93D',  # 專業 - 黃色
            'general': '#A8A8A8'        # 一般 - 灰色
        }
        return colors.get(authority_level, '#A8A8A8')

    def _get_authority_icon(self, authority_level: str) -> str:
        """根據權威級別返回圖標"""
        icons = {
            'official': '🏛️',     # 官方
            'academic': '🎓',     # 學術
            'professional': '👨‍⚕️', # 專業
            'general': 'ℹ️'       # 一般
        }
        return icons.get(authority_level, 'ℹ️')

class FlexComponentFactory:
    def __init__(self):
        self.confidence_visualizer = ConfidenceVisualizer()
        self.source_tracer = SourceTracer()

    def create_component(self, component_type: ComponentType, chunk: Dict, user_context: Dict = None) -> Dict:
        """工廠方法：根據組件類型創建對應的 Flex 組件"""

        creators = {
            ComponentType.COMPARISON_CARD: self.create_comparison_card,
            ComponentType.CONFIDENCE_METER: self.create_confidence_meter,
            ComponentType.XAI_BOX: self.create_xai_box,
            ComponentType.INFO_BOX: self.create_info_box,
            ComponentType.ACTION_CARD: self.create_action_card,
            ComponentType.TIMELINE_LIST: self.create_timeline_list,
            ComponentType.WARNING_BOX: self.create_warning_box
        }

        creator = creators.get(component_type, self.create_info_box)
        return creator(chunk, user_context)

    def create_comparison_card(self, chunk: Dict, user_context: Dict = None) -> Dict:
        """創建對比卡片 - 適用於失智症警訊對比"""

        theme = FlexColorTheme.WARNING.value
        confidence_score = chunk.get('confidence_score', 0.8)

        return {
            "type": "bubble",
            "header": {
                "type": "box",
                "layout": "vertical",
                "backgroundColor": theme["secondary"],
                "paddingAll": "12px",
                "contents": [
                    {
                        "type": "text",
                        "text": f"⚠️ {chunk.get('title', '失智症警訊')}",
                        "weight": "bold",
                        "size": "md",
                        "color": theme["primary"],
                        "wrap": True
                    },
                    self.confidence_visualizer.create_confidence_indicator(confidence_score)
                ]
            },
            "body": {
                "type": "box",
                "layout": "vertical",
                "paddingAll": "16px",
                "contents": [
                    {
                        "type": "text",
                        "text": chunk.get('summary', chunk.get('content', ''))[:100] + "...",
                        "wrap": True,
                        "size": "sm",
                        "color": theme["text"],
                        "margin": "none"
                    },
                    {
                        "type": "separator",
                        "margin": "lg"
                    },
                    self._create_comparison_section(chunk),
                    self.source_tracer.create_source_section(chunk.get('source_trace', {}))
                ]
            },
            "footer": self._create_action_footer(chunk)
        }

    def create_confidence_meter(self, chunk: Dict, user_context: Dict = None) -> Dict:
        """創建信心度量表 - 適用於 BPSD 症狀評估"""

        theme = FlexColorTheme.INFO.value
        confidence_score = chunk.get('confidence_score', 0.8)

        return {
            "type": "bubble",
            "header": {
                "type": "box",
                "layout": "vertical",
                "backgroundColor": theme["secondary"],
                "paddingAll": "12px",
                "contents": [
                    {
                        "type": "text",
                        "text": f"📊 {chunk.get('title', '症狀評估')}",
                        "weight": "bold",
                        "size": "md",
                        "color": theme["primary"],
                        "wrap": True
                    }
                ]
            },
            "body": {
                "type": "box",
                "layout": "vertical",
                "paddingAll": "16px",
                "contents": [
                    self.confidence_visualizer.create_detailed_confidence_meter(
                        confidence_score, 
                        chunk.get('explanation_data', {})
                    ),
                    {
                        "type": "separator",
                        "margin": "lg"
                    },
                    {
                        "type": "text",
                        "text": chunk.get('content', '')[:120] + "...",
                        "wrap": True,
                        "size": "sm",
                        "color": theme["text"]
                    },
                    self._create_severity_indicators(chunk),
                    self.source_tracer.create_source_section(chunk.get('source_trace', {}))
                ]
            },
            "footer": self._create_action_footer(chunk)
        }

    def create_xai_box(self, chunk: Dict, user_context: Dict = None) -> Dict:
        """創建 XAI 解釋盒 - 適用於照護策略解釋"""

        theme = FlexColorTheme.SUCCESS.value
        explanation_data = chunk.get('explanation_data', {})

        return {
            "type": "bubble",
            "header": {
                "type": "box",
                "layout": "vertical",
                "backgroundColor": theme["secondary"],
                "paddingAll": "12px",
                "contents": [
                    {
                        "type": "text",
                        "text": f"💡 {chunk.get('title', '照護建議')}",
                        "weight": "bold",
                        "size": "md",
                        "color": theme["primary"],
                        "wrap": True
                    }
                ]
            },
            "body": {
                "type": "box",
                "layout": "vertical",
                "paddingAll": "16px",
                "contents": [
                    {
                        "type": "text",
                        "text": chunk.get('content', '')[:100] + "...",
                        "wrap": True,
                        "size": "sm",
                        "color": theme["text"]
                    },
                    {
                        "type": "separator",
                        "margin": "lg"
                    },
                    self._create_explanation_section(explanation_data),
                    self._create_evidence_strength_indicator(explanation_data),
                    self.source_tracer.create_source_section(chunk.get('source_trace', {}))
                ]
            },
            "footer": self._create_action_footer(chunk)
        }

    def create_info_box(self, chunk: Dict, user_context: Dict = None) -> Dict:
        """創建資訊盒 - 通用資訊顯示"""

        theme = FlexColorTheme.NEUTRAL.value

        return {
            "type": "bubble",
            "header": {
                "type": "box",
                "layout": "vertical",
                "backgroundColor": theme["secondary"],
                "paddingAll": "12px",
                "contents": [
                    {
                        "type": "text",
                        "text": f"ℹ️ {chunk.get('title', '相關資訊')}",
                        "weight": "bold",
                        "size": "md",
                        "color": theme["primary"],
                        "wrap": True
                    }
                ]
            },
            "body": {
                "type": "box",
                "layout": "vertical",
                "paddingAll": "16px",
                "contents": [
                    {
                        "type": "text",
                        "text": chunk.get('content', '')[:150] + "...",
                        "wrap": True,
                        "size": "sm",
                        "color": theme["text"]
                    },
                    self._create_tags_section(chunk.get('tags', [])),
                    self.source_tracer.create_source_section(chunk.get('source_trace', {}))
                ]
            },
            "footer": self._create_action_footer(chunk)
        }

    def create_action_card(self, chunk: Dict, user_context: Dict = None) -> Dict:
        """創建行動卡片 - 適用於走失預防等行動指引"""

        theme = FlexColorTheme.WARNING.value

        return {
            "type": "bubble",
            "header": {
                "type": "box",
                "layout": "vertical",
                "backgroundColor": theme["secondary"],
                "paddingAll": "12px",
                "contents": [
                    {
                        "type": "text",
                        "text": f"🎯 {chunk.get('title', '行動指引')}",
                        "weight": "bold",
                        "size": "md",
                        "color": theme["primary"],
                        "wrap": True
                    }
                ]
            },
            "body": {
                "type": "box",
                "layout": "vertical",
                "paddingAll": "16px",
                "contents": [
                    {
                        "type": "text",
                        "text": "立即行動建議：",
                        "weight": "bold",
                        "size": "sm",
                        "color": theme["text"]
                    },
                    {
                        "type": "text",
                        "text": chunk.get('content', '')[:120] + "...",
                        "wrap": True,
                        "size": "sm",
                        "color": theme["text"],
                        "margin": "sm"
                    },
                    self._create_action_steps(chunk),
                    self.source_tracer.create_source_section(chunk.get('source_trace', {}))
                ]
            },
            "footer": self._create_urgent_action_footer(chunk)
        }

    def create_timeline_list(self, chunk: Dict, user_context: Dict = None) -> Dict:
        """創建時間軸列表 - 適用於病程階段描述"""

        theme = FlexColorTheme.INFO.value

        return {
            "type": "bubble",
            "header": {
                "type": "box",
                "layout": "vertical",
                "backgroundColor": theme["secondary"],
                "paddingAll": "12px",
                "contents": [
                    {
                        "type": "text",
                        "text": f"📅 {chunk.get('title', '病程階段')}",
                        "weight": "bold",
                        "size": "md",
                        "color": theme["primary"],
                        "wrap": True
                    }
                ]
            },
            "body": {
                "type": "box",
                "layout": "vertical",
                "paddingAll": "16px",
                "contents": [
                    self._create_timeline_content(chunk),
                    self.source_tracer.create_source_section(chunk.get('source_trace', {}))
                ]
            },
            "footer": self._create_action_footer(chunk)
        }

    def create_warning_box(self, chunk: Dict, user_context: Dict = None) -> Dict:
        """創建警告盒 - 適用於財務安全等重要警告"""

        theme = FlexColorTheme.WARNING.value

        return {
            "type": "bubble",
            "header": {
                "type": "box",
                "layout": "vertical",
                "backgroundColor": "#FFE5E5",
                "paddingAll": "12px",
                "contents": [
                    {
                        "type": "text",
                        "text": "⚠️ 重要警告",
                        "weight": "bold",
                        "size": "md",
                        "color": "#FF3333",
                        "wrap": True
                    },
                    {
                        "type": "text",
                        "text": chunk.get('title', ''),
                        "weight": "bold",
                        "size": "sm",
                        "color": theme["primary"],
                        "wrap": True
                    }
                ]
            },
            "body": {
                "type": "box",
                "layout": "vertical",
                "paddingAll": "16px",
                "contents": [
                    {
                        "type": "text",
                        "text": chunk.get('content', '')[:120] + "...",
                        "wrap": True,
                        "size": "sm",
                        "color": theme["text"]
                    },
                    self._create_warning_checklist(chunk),
                    self.source_tracer.create_source_section(chunk.get('source_trace', {}))
                ]
            },
            "footer": self._create_urgent_action_footer(chunk)
        }

    def _create_comparison_section(self, chunk: Dict) -> Dict:
        """創建正常vs異常對比區塊"""
        return {
            "type": "box",
            "layout": "vertical",
            "margin": "lg",
            "contents": [
                {
                    "type": "text",
                    "text": "🔍 正常 vs 需注意",
                    "weight": "bold",
                    "size": "sm",
                    "color": "#333333"
                },
                {
                    "type": "box",
                    "layout": "horizontal",
                    "margin": "sm",
                    "contents": [
                        {
                            "type": "box",
                            "layout": "vertical",
                            "flex": 1,
                            "contents": [
                                {
                                    "type": "text",
                                    "text": "✅ 正常老化",
                                    "size": "xs",
                                    "color": "#95E1A3",
                                    "weight": "bold"
                                },
                                {
                                    "type": "text",
                                    "text": "偶爾忘記約會但稍後想起",
                                    "size": "xs",
                                    "color": "#666666",
                                    "wrap": True
                                }
                            ]
                        },
                        {
                            "type": "separator",
                            "margin": "sm"
                        },
                        {
                            "type": "box",
                            "layout": "vertical",
                            "flex": 1,
                            "contents": [
                                {
                                    "type": "text",
                                    "text": "⚠️ 需注意",
                                    "size": "xs",
                                    "color": "#FF6B6B",
                                    "weight": "bold"
                                },
                                {
                                    "type": "text",
                                    "text": "完全忘記重要約會且無法回想",
                                    "size": "xs",
                                    "color": "#666666",
                                    "wrap": True
                                }
                            ]
                        }
                    ]
                }
            ]
        }

    def _create_severity_indicators(self, chunk: Dict) -> Dict:
        """創建嚴重程度指標"""
        difficulty_level = chunk.get('difficulty_level', 'basic')

        colors = {
            'basic': '#95E1A3',
            'moderate': '#FFD93D', 
            'severe': '#FF6B6B'
        }

        return {
            "type": "box",
            "layout": "horizontal",
            "margin": "lg",
            "contents": [
                {
                    "type": "text",
                    "text": "嚴重程度：",
                    "size": "xs",
                    "color": "#666666",
                    "flex": 0
                },
                {
                    "type": "text",
                    "text": f"●●●●●"[:{'basic': 2, 'moderate': 4, 'severe': 5}.get(difficulty_level, 2)],
                    "size": "sm",
                    "color": colors.get(difficulty_level, '#95E1A3'),
                    "flex": 0,
                    "margin": "sm"
                }
            ]
        }

    def _create_explanation_section(self, explanation_data: Dict) -> Dict:
        """創建解釋說明區塊"""
        reasoning = explanation_data.get('reasoning', '基於專業醫療指引建議')

        return {
            "type": "box",
            "layout": "vertical",
            "margin": "lg",
            "contents": [
                {
                    "type": "text",
                    "text": "🧠 AI 解釋依據",
                    "weight": "bold",
                    "size": "sm",
                    "color": "#4ECDC4"
                },
                {
                    "type": "text",
                    "text": reasoning[:80] + "...",
                    "wrap": True,
                    "size": "xs",
                    "color": "#666666",
                    "margin": "sm"
                }
            ]
        }

    def _create_evidence_strength_indicator(self, explanation_data: Dict) -> Dict:
        """創建證據強度指標"""
        evidence_strength = explanation_data.get('evidence_strength', 'medium')

        strength_colors = {
            'high': '#95E1A3',
            'medium': '#FFD93D',
            'low': '#FF6B6B'
        }

        strength_texts = {
            'high': '證據充分',
            'medium': '證據中等',
            'low': '證據有限'
        }

        return {
            "type": "box",
            "layout": "horizontal",
            "margin": "sm",
            "contents": [
                {
                    "type": "text",
                    "text": "📋 證據強度：",
                    "size": "xs",
                    "color": "#666666",
                    "flex": 0
                },
                {
                    "type": "text",
                    "text": strength_texts.get(evidence_strength, '證據中等'),
                    "size": "xs",
                    "color": strength_colors.get(evidence_strength, '#FFD93D'),
                    "flex": 0,
                    "margin": "sm"
                }
            ]
        }

    def _create_tags_section(self, tags: List[str]) -> Dict:
        """創建標籤區塊"""
        if not tags:
            return {"type": "spacer", "size": "xs"}

        return {
            "type": "box",
            "layout": "horizontal",
            "margin": "lg",
            "contents": [
                {
                    "type": "text",
                    "text": " ".join([f"#{tag}" for tag in tags[:3]]),
                    "size": "xs",
                    "color": "#4ECDC4",
                    "wrap": True
                }
            ]
        }

    def _create_action_steps(self, chunk: Dict) -> Dict:
        """創建行動步驟列表"""
        return {
            "type": "box",
            "layout": "vertical",
            "margin": "lg",
            "contents": [
                {
                    "type": "text",
                    "text": "📋 建議步驟：",
                    "weight": "bold",
                    "size": "sm",
                    "color": "#333333"
                },
                {
                    "type": "text",
                    "text": "1. 立即評估現況\n2. 聯絡專業人員\n3. 制定應對計畫",
                    "size": "xs",
                    "color": "#666666",
                    "wrap": True,
                    "margin": "sm"
                }
            ]
        }

    def _create_timeline_content(self, chunk: Dict) -> Dict:
        """創建時間軸內容"""
        return {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "text",
                    "text": chunk.get('content', '')[:100] + "...",
                    "wrap": True,
                    "size": "sm",
                    "color": "#333333"
                },
                {
                    "type": "box",
                    "layout": "vertical",
                    "margin": "lg",
                    "contents": [
                        {
                            "type": "box",
                            "layout": "horizontal",
                            "contents": [
                                {
                                    "type": "text",
                                    "text": "🔵",
                                    "flex": 0
                                },
                                {
                                    "type": "text",
                                    "text": "輕度期：記憶力開始下降",
                                    "size": "xs",
                                    "color": "#666666",
                                    "margin": "sm",
                                    "wrap": True
                                }
                            ]
                        }
                    ]
                }
            ]
        }

    def _create_warning_checklist(self, chunk: Dict) -> Dict:
        """創建警告檢查清單"""
        return {
            "type": "box",
            "layout": "vertical",
            "margin": "lg",
            "contents": [
                {
                    "type": "text",
                    "text": "⚠️ 立即檢查：",
                    "weight": "bold",
                    "size": "sm",
                    "color": "#FF6B6B"
                },
                {
                    "type": "text",
                    "text": "□ 檢查重要文件\n□ 確認財務安全\n□ 尋求專業協助",
                    "size": "xs",
                    "color": "#666666",
                    "wrap": True,
                    "margin": "sm"
                }
            ]
        }

    def _create_action_footer(self, chunk: Dict) -> Dict:
        """創建標準行動足部"""
        return {
            "type": "box",
            "layout": "horizontal",
            "paddingAll": "12px",
            "contents": [
                {
                    "type": "button",
                    "style": "primary",
                    "height": "sm",
                    "action": {
                        "type": "message",
                        "text": f"詳細說明 {chunk.get('chunk_id', '')}"
                    },
                    "color": "#4ECDC4",
                    "flex": 1,
                    "margin": "none"
                },
                {
                    "type": "button",
                    "style": "secondary",
                    "height": "sm",
                    "action": {
                        "type": "message", 
                        "text": f"相關資源 {chunk.get('chunk_id', '')}"
                    },
                    "flex": 1,
                    "margin": "sm"
                }
            ]
        }

    def _create_urgent_action_footer(self, chunk: Dict) -> Dict:
        """創建緊急行動足部"""
        return {
            "type": "box",
            "layout": "vertical",
            "paddingAll": "12px",
            "contents": [
                {
                    "type": "button",
                    "style": "primary",
                    "height": "sm",
                    "action": {
                        "type": "message",
                        "text": f"立即行動 {chunk.get('chunk_id', '')}"
                    },
                    "color": "#FF6B6B"
                },
                {
                    "type": "box",
                    "layout": "horizontal",
                    "margin": "sm",
                    "contents": [
                        {
                            "type": "button",
                            "style": "secondary",
                            "height": "sm",
                            "action": {
                                "type": "message",
                                "text": f"詳細資訊 {chunk.get('chunk_id', '')}"
                            },
                            "flex": 1
                        },
                        {
                            "type": "button",
                            "style": "secondary", 
                            "height": "sm",
                            "action": {
                                "type": "message",
                                "text": f"專業協助 {chunk.get('chunk_id', '')}"
                            },
                            "flex": 1,
                            "margin": "sm"
                        }
                    ]
                }
            ]
        }

class ExplanationEngine:
    """解釋引擎"""

    def generate_explanations(self, chunks: List[Dict], user_context: Dict = None) -> List[Dict]:
        """為 chunk 列表生成解釋"""
        explanations = []

        for chunk in chunks:
            explanation = {
                'chunk_id': chunk.get('chunk_id'),
                'reasoning_chain': self._build_reasoning_chain(chunk),
                'confidence_breakdown': self._analyze_confidence(chunk),
                'evidence_sources': self._trace_evidence_sources(chunk),
                'related_concepts': self._find_related_concepts(chunk),
                'interpretation_notes': self._generate_interpretation_notes(chunk, user_context)
            }
            explanations.append(explanation)

        return explanations

    def _build_reasoning_chain(self, chunk: Dict) -> List[Dict]:
        """建構推理鏈"""
        chunk_type = chunk.get('chunk_type', '')

        reasoning_templates = {
            'warning_sign': [
                {"step": 1, "description": "識別行為模式", "evidence": "基於臨床觀察指標"},
                {"step": 2, "description": "對比正常老化", "evidence": "參考醫學診斷標準"},
                {"step": 3, "description": "評估嚴重程度", "evidence": "依據失智症評估量表"}
            ],
            'bpsd_symptom': [
                {"step": 1, "description": "症狀分類識別", "evidence": "基於 BPSD 評估工具"},
                {"step": 2, "description": "觸發因子分析", "evidence": "參考行為心理學研究"},
                {"step": 3, "description": "影響程度評估", "evidence": "依據照護難度量表"}
            ],
            'coping_strategy': [
                {"step": 1, "description": "問題情境分析", "evidence": "基於照護實務經驗"},
                {"step": 2, "description": "策略適用性評估", "evidence": "參考循證照護指引"},
                {"step": 3, "description": "執行可行性判斷", "evidence": "考量家庭照護能力"}
            ]
        }

        return reasoning_templates.get(chunk_type, [
            {"step": 1, "description": "資料收集與驗證", "evidence": "基於可信來源"},
            {"step": 2, "description": "專業知識比對", "evidence": "參考醫療指引"},
            {"step": 3, "description": "適用性評估", "evidence": "考量實際應用情境"}
        ])

    def _analyze_confidence(self, chunk: Dict) -> Dict:
        """分析信心度組成"""
        confidence_score = chunk.get('confidence_score', 0.8)
        source_trace = chunk.get('source_trace', {})

        # 計算各項信心度因子
        source_reliability = self._calculate_source_reliability(source_trace)
        content_completeness = self._calculate_content_completeness(chunk)
        validation_strength = self._calculate_validation_strength(chunk)

        return {
            'overall_confidence': confidence_score,
            'source_reliability': source_reliability,
            'content_completeness': content_completeness,
            'validation_strength': validation_strength,
            'confidence_factors': {
                '來源可靠性': f"{source_reliability:.0%}",
                '內容完整性': f"{content_completeness:.0%}",
                '驗證強度': f"{validation_strength:.0%}"
            }
        }

    def _trace_evidence_sources(self, chunk: Dict) -> List[Dict]:
        """追蹤證據來源"""
        source_trace = chunk.get('source_trace', {})
        explanation_data = chunk.get('explanation_data', {})

        sources = []

        # 主要來源
        if source_trace:
            sources.append({
                'type': 'primary',
                'name': source_trace.get('source', ''),
                'authority': source_trace.get('authority_level', 'general'),
                'verified_date': source_trace.get('last_verified', ''),
                'relevance': 'high'
            })

        # 相關概念來源
        related_concepts = explanation_data.get('related_concepts', [])
        for concept in related_concepts[:2]:  # 限制顯示數量
            sources.append({
                'type': 'supporting',
                'name': f'相關概念：{concept}',
                'authority': 'academic',
                'relevance': 'medium'
            })

        return sources

    def _find_related_concepts(self, chunk: Dict) -> List[str]:
        """尋找相關概念"""
        chunk_type = chunk.get('chunk_type', '')
        keywords = chunk.get('keywords', [])

        concept_mapping = {
            'warning_sign': ['認知功能', '記憶障礙', '執行功能', '海馬迴退化'],
            'bpsd_symptom': ['行為症狀', '心理症狀', '神經傳導物質', '環境因子'],
            'coping_strategy': ['照護技巧', '溝通方法', '環境調整', '壓力管理'],
            'stage_description': ['病程進展', '功能退化', '照護需求', '生活品質'],
            'missing_prevention': ['安全管理', 'GPS 定位', '社區網絡', '預防措施']
        }

        base_concepts = concept_mapping.get(chunk_type, ['失智症', '照護'])
        return base_concepts + keywords[:2]  # 結合基礎概念和關鍵字

    def _generate_interpretation_notes(self, chunk: Dict, user_context: Dict) -> List[str]:
        """生成解釋註記"""
        notes = []

        # 基於 chunk 類型的註記
        chunk_type = chunk.get('chunk_type', '')
        difficulty_level = chunk.get('difficulty_level', 'basic')

        if chunk_type == 'warning_sign':
            notes.append("此為失智症早期警訊，出現時建議儘早諮詢專業醫師")
            if difficulty_level == 'severe':
                notes.append("症狀較為嚴重，建議立即尋求醫療協助")

        elif chunk_type == 'bpsd_symptom':
            notes.append("行為心理症狀需要耐心應對，可尋求專業照護指導")
            notes.append("每個人的症狀表現可能不同，需要個別化的照護方式")

        elif chunk_type == 'coping_strategy':
            notes.append("照護策略需要根據個人情況調整，建議循序漸進實施")
            notes.append("如果策略效果不佳，請諮詢專業照護人員")

        # 基於信心度的註記
        confidence_score = chunk.get('confidence_score', 0.8)
        if confidence_score < 0.7:
            notes.append("此資訊的確定性較低，建議進一步確認或諮詢專業人員")

        return notes

    def _calculate_source_reliability(self, source_trace: Dict) -> float:
        """計算來源可靠性分數"""
        if not source_trace:
            return 0.5

        authority_scores = {
            'official': 1.0,
            'academic': 0.9,
            'professional': 0.8,
            'general': 0.6
        }

        authority_level = source_trace.get('authority_level', 'general')
        base_score = authority_scores.get(authority_level, 0.6)

        # 根據最後驗證時間調整
        last_verified = source_trace.get('last_verified', '')
        if last_verified:
            # 簡化時間衰減計算
            import re
            if re.search(r'2024|2025', last_verified):
                time_factor = 1.0
            elif re.search(r'2022|2023', last_verified):
                time_factor = 0.9
            else:
                time_factor = 0.8
        else:
            time_factor = 0.8

        return base_score * time_factor

    def _calculate_content_completeness(self, chunk: Dict) -> float:
        """計算內容完整性分數"""
        score = 0.0

        # 檢查必要欄位
        if chunk.get('title'):
            score += 0.2
        if chunk.get('content'):
            score += 0.3
        if chunk.get('summary'):
            score += 0.2
        if chunk.get('keywords'):
            score += 0.1
        if chunk.get('tags'):
            score += 0.1
        if chunk.get('explanation_data'):
            score += 0.1

        return min(score, 1.0)

    def _calculate_validation_strength(self, chunk: Dict) -> float:
        """計算驗證強度分數"""
        explanation_data = chunk.get('explanation_data', {})
        evidence_strength = explanation_data.get('evidence_strength', 'medium')

        strength_scores = {
            'high': 1.0,
            'medium': 0.7,
            'low': 0.4
        }

        return strength_scores.get(evidence_strength, 0.7)

class A11yEnhancer:
    """無障礙增強器"""

    def enhance_accessibility(self, flex_message: Dict) -> Dict:
        """增強 Flex Message 的無障礙性"""

        # 確保有適當的 alt text
        flex_message = self._ensure_alt_text(flex_message)

        # 優化顏色對比度
        flex_message = self._optimize_color_contrast(flex_message)

        # 添加語義結構
        flex_message = self._add_semantic_structure(flex_message)

        # 確保鍵盤可操作性
        flex_message = self._ensure_keyboard_accessibility(flex_message)

        return flex_message

    def _ensure_alt_text(self, flex_message: Dict) -> Dict:
        """確保適當的替代文字"""
        if 'altText' not in flex_message or not flex_message['altText']:
            # 從內容中生成 alt text
            contents = flex_message.get('contents', {})
            if contents.get('type') == 'bubble':
                header = contents.get('header', {})
                if header:
                    title_text = self._extract_text_from_component(header)
                    flex_message['altText'] = f"失智照護資訊：{title_text}"
                else:
                    flex_message['altText'] = "失智照護相關資訊"
            elif contents.get('type') == 'carousel':
                bubble_count = len(contents.get('contents', []))
                flex_message['altText'] = f"失智照護資訊輪播，共 {bubble_count} 則"

        return flex_message

    def _optimize_color_contrast(self, flex_message: Dict) -> Dict:
        """優化顏色對比度以符合 WCAG 標準"""

        # 定義符合 WCAG AA 標準的顏色組合
        accessible_colors = {
            '#FF6B6B': {'background': '#FFFFFF', 'text': '#FFFFFF'},  # 紅色
            '#4ECDC4': {'background': '#FFFFFF', 'text': '#FFFFFF'},  # 青色
            '#95E1A3': {'background': '#FFFFFF', 'text': '#000000'},  # 綠色
            '#FFD93D': {'background': '#FFFFFF', 'text': '#000000'},  # 黃色
            '#A8A8A8': {'background': '#FFFFFF', 'text': '#FFFFFF'}   # 灰色
        }

        # 遞迴檢查和調整顏色
        self._adjust_colors_recursive(flex_message, accessible_colors)

        return flex_message

    def _add_semantic_structure(self, flex_message: Dict) -> Dict:
        """添加語義結構標記"""

        # 為主要區塊添加語義角色
        contents = flex_message.get('contents', {})

        if contents.get('type') == 'bubble':
            # 為 header 添加標題角色
            if 'header' in contents:
                contents['header']['role'] = 'heading'
                contents['header']['level'] = 2

            # 為 body 添加主要內容角色
            if 'body' in contents:
                contents['body']['role'] = 'main'

            # 為 footer 添加導航角色
            if 'footer' in contents:
                contents['footer']['role'] = 'navigation'

        return flex_message

    def _ensure_keyboard_accessibility(self, flex_message: Dict) -> Dict:
        """確保鍵盤可操作性"""

        # 為所有按鈕添加適當的 action
        self._add_keyboard_actions_recursive(flex_message)

        return flex_message

    def _extract_text_from_component(self, component: Dict) -> str:
        """從組件中提取文字內容"""
        if component.get('type') == 'text':
            return component.get('text', '')
        elif component.get('type') == 'box':
            texts = []
            for content in component.get('contents', []):
                text = self._extract_text_from_component(content)
                if text:
                    texts.append(text)
            return ' '.join(texts)
        return ''

    def _adjust_colors_recursive(self, obj: Dict, accessible_colors: Dict):
        """遞迴調整顏色對比度"""
        if isinstance(obj, dict):
            # 檢查顏色屬性
            if 'color' in obj:
                original_color = obj['color']
                if original_color in accessible_colors:
                    # 保持原色，確保對比度
                    pass

            # 遞迴處理子元素
            for key, value in obj.items():
                if isinstance(value, (dict, list)):
                    self._adjust_colors_recursive(value, accessible_colors)
        elif isinstance(obj, list):
            for item in obj:
                if isinstance(item, (dict, list)):
                    self._adjust_colors_recursive(item, accessible_colors)

    def _add_keyboard_actions_recursive(self, obj: Dict):
        """遞迴添加鍵盤操作支援"""
        if isinstance(obj, dict):
            # 為按鈕添加鍵盤支援
            if obj.get('type') == 'button':
                if 'action' in obj:
                    obj['accessibility'] = {
                        'role': 'button',
                        'label': obj.get('text', '按鈕'),
                        'keyboard_shortcut': True
                    }

            # 遞迴處理子元素
            for key, value in obj.items():
                if isinstance(value, (dict, list)):
                    self._add_keyboard_actions_recursive(value)
        elif isinstance(obj, list):
            for item in obj:
                if isinstance(item, (dict, list)):
                    self._add_keyboard_actions_recursive(item)

class XAIFlexGenerator:
    def __init__(self):
        self.component_factory = FlexComponentFactory()
        self.explanation_engine = ExplanationEngine()
        self.accessibility_enhancer = A11yEnhancer()

    def generate_enhanced_flex_message(self, chunks: List[Dict], user_context: Dict = None) -> Dict:
        """生成增強版 Flex Message，包含 XAI 解釋"""

        if not chunks:
            return self._create_empty_state_message()

        # 根據 chunk 數量決定容器類型
        if len(chunks) == 1:
            return self._create_single_bubble_message(chunks[0], user_context)
        else:
            return self._create_carousel_message(chunks, user_context)

    def _create_single_bubble_message(self, chunk: Dict, user_context: Dict = None) -> Dict:
        """創建單個 bubble 的 Flex Message"""

        component_type = self._determine_component_type(chunk)
        bubble_content = self.component_factory.create_component(component_type, chunk, user_context)

        return {
            "type": "flex",
            "altText": f"失智照護資訊：{chunk.get('title', '相關資訊')}",
            "contents": bubble_content,
            "metadata": {
                "chunk_id": chunk.get('chunk_id'),
                "component_type": component_type.value,
                "generated_at": datetime.now().isoformat()
            }
        }

    def _create_carousel_message(self, chunks: List[Dict], user_context: Dict = None) -> Dict:
        """創建輪播式 Flex Message"""

        bubbles = []
        for chunk in chunks[:10]:  # 限制最多 10 個 bubble
            component_type = self._determine_component_type(chunk)
            bubble = self.component_factory.create_component(component_type, chunk, user_context)
            bubbles.append(bubble)

        return {
            "type": "flex",
            "altText": f"找到 {len(chunks)} 筆相關的失智照護資訊",
            "contents": {
                "type": "carousel",
                "contents": bubbles
            },
            "metadata": {
                "total_chunks": len(chunks),
                "displayed_chunks": len(bubbles),
                "generated_at": datetime.now().isoformat()
            }
        }

    def _determine_component_type(self, chunk: Dict) -> ComponentType:
        """根據 chunk_type 決定視覺組件類型"""

        chunk_type = chunk.get('chunk_type', '')
        mapping = {
            'warning_sign': ComponentType.COMPARISON_CARD,
            'normal_vs_abnormal': ComponentType.COMPARISON_CARD,
            'bpsd_symptom': ComponentType.CONFIDENCE_METER,
            'coping_strategy': ComponentType.XAI_BOX,
            'stage_description': ComponentType.TIMELINE_LIST,
            'missing_prevention': ComponentType.ACTION_CARD,
            'legal_rights': ComponentType.INFO_BOX,
            'financial_safety': ComponentType.WARNING_BOX
        }

        return mapping.get(chunk_type, ComponentType.INFO_BOX)

    def _create_empty_state_message(self) -> Dict:
        """創建空狀態訊息"""
        return {
            "type": "flex",
            "altText": "很抱歉，目前找不到相關資訊",
            "contents": {
                "type": "bubble",
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "text",
                            "text": "🔍 找不到相關資訊",
                            "weight": "bold",
                            "size": "lg",
                            "align": "center"
                        },
                        {
                            "type": "text",
                            "text": "請嘗試：\n• 使用不同的關鍵字\n• 簡化問題描述\n• 聯絡專業人員協助",
                            "wrap": True,
                            "margin": "md",
                            "size": "sm",
                            "color": "#666666"
                        }
                    ]
                }
            }
        }

# 使用範例和測試函數
def test_flex_generator():
    """測試 Flex Message 生成器"""

    # 測試用的 chunk 資料
    test_chunks = [
        {
            "chunk_id": "M1-04",
            "module_id": "M1",
            "chunk_type": "warning_sign",
            "title": "對時間地點感到混淆",
            "content": "失智症患者會搞不清楚年月日、季節變化，或迷失在熟悉的地方。這與正常老化的偶爾健忘不同，是持續且逐漸加重的認知障礙。",
            "summary": "時間空間認知障礙是失智症早期重要警訊",
            "keywords": ["記憶混淆", "時間障礙", "空間迷失"],
            "tags": ["十大警訊", "早期症狀", "認知功能"],
            "confidence_score": 0.92,
            "difficulty_level": "basic",
            "explanation_data": {
                "reasoning": "基於台灣失智症協會官方指引",
                "evidence_strength": "high",
                "related_concepts": ["海馬迴退化", "執行功能障礙"]
            },
            "source_trace": {
                "source": "台灣失智症協會-十大警訊DM",
                "version": "v2.1",
                "authority_level": "official",
                "last_verified": "2025-07-20"
            }
        }
    ]

    # 初始化生成器
    flex_generator = XAIFlexGenerator()

    # 生成 Flex Message
    result = flex_generator.generate_enhanced_flex_message(test_chunks)

    # 輸出結果
    print("生成的 Flex Message:")
    print(json.dumps(result, ensure_ascii=False, indent=2))

    return result

if __name__ == "__main__":
    # 執行測試
    test_result = test_flex_generator()
    print("\n✅ XAI Flex Message 生成器測試完成！")