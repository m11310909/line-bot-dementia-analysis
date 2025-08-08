"""
📊 圖表組件庫
支援 M1 模組的視覺化需求
"""

from typing import Dict, List, Any, Optional
import json
from linebot.models import (
    FlexSendMessage,
    BoxComponent,
    TextComponent,
    SeparatorComponent,
    SpacerComponent,
)


class ChartComponents:
    """圖表組件庫"""

    @staticmethod
    def create_severity_chart(
        symptoms: Dict[str, int], title: str = "症狀嚴重程度"
    ) -> Dict[str, Any]:
        """
        創建症狀嚴重程度圖表

        Args:
            symptoms: 症狀字典，格式為 {"症狀名": 嚴重程度(1-5)}
            title: 圖表標題

        Returns:
            Flex Message 組件
        """
        # 顏色映射：綠色(輕微) -> 黃色(中等) -> 紅色(嚴重)
        colors = {
            1: "#4CAF50",  # 綠色 - 輕微
            2: "#8BC34A",  # 淺綠
            3: "#FFC107",  # 黃色 - 中等
            4: "#FF9800",  # 橙色 - 較重
            5: "#F44336",  # 紅色 - 嚴重
        }

        # 創建進度條組件
        progress_bars = []
        for symptom, severity in symptoms.items():
            percentage = (severity / 5) * 100
            color = colors.get(severity, "#9E9E9E")

            progress_bar = {
                "type": "box",
                "layout": "vertical",
                "spacing": "sm",
                "contents": [
                    {
                        "type": "text",
                        "text": symptom,
                        "size": "sm",
                        "color": "#666666",
                        "wrap": True,
                    },
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "spacing": "sm",
                        "contents": [
                            {
                                "type": "box",
                                "layout": "vertical",
                                "width": f"{percentage}%",
                                "backgroundColor": color,
                                "height": "8px",
                                "cornerRadius": "4px",
                            },
                            {
                                "type": "text",
                                "text": f"{severity}/5",
                                "size": "xs",
                                "color": "#666666",
                                "align": "end",
                            },
                        ],
                    },
                ],
            }
            progress_bars.append(progress_bar)

        return {
            "type": "box",
            "layout": "vertical",
            "spacing": "md",
            "contents": [
                {
                    "type": "text",
                    "text": title,
                    "weight": "bold",
                    "size": "lg",
                    "color": "#333333",
                },
                *progress_bars,
            ],
        }

    @staticmethod
    def create_risk_radar_chart(
        risk_factors: Dict[str, float], title: str = "風險評估"
    ) -> Dict[str, Any]:
        """
        創建風險評估雷達圖（簡化版）

        Args:
            risk_factors: 風險因素字典，格式為 {"風險因素": 風險值(0-1)}
            title: 圖表標題

        Returns:
            Flex Message 組件
        """

        # 風險等級顏色
        def get_risk_color(risk: float) -> str:
            if risk < 0.3:
                return "#4CAF50"  # 低風險 - 綠色
            elif risk < 0.6:
                return "#FFC107"  # 中風險 - 黃色
            else:
                return "#F44336"  # 高風險 - 紅色

        # 創建風險指標
        risk_indicators = []
        for factor, risk in risk_factors.items():
            risk_level = "高" if risk > 0.6 else "中" if risk > 0.3 else "低"
            color = get_risk_color(risk)

            indicator = {
                "type": "box",
                "layout": "horizontal",
                "spacing": "sm",
                "contents": [
                    {
                        "type": "box",
                        "width": "8px",
                        "height": "8px",
                        "backgroundColor": color,
                        "cornerRadius": "4px",
                    },
                    {
                        "type": "text",
                        "text": factor,
                        "size": "sm",
                        "color": "#333333",
                        "flex": 1,
                    },
                    {
                        "type": "text",
                        "text": risk_level,
                        "size": "sm",
                        "color": color,
                        "weight": "bold",
                    },
                ],
            }
            risk_indicators.append(indicator)

        return {
            "type": "box",
            "layout": "vertical",
            "spacing": "md",
            "contents": [
                {
                    "type": "text",
                    "text": title,
                    "weight": "bold",
                    "size": "lg",
                    "color": "#333333",
                },
                *risk_indicators,
            ],
        }

    @staticmethod
    def create_warning_indicator(level: int, message: str) -> Dict[str, Any]:
        """
        創建警訊等級指示器

        Args:
            level: 警訊等級 (1-5)
            message: 警訊訊息

        Returns:
            Flex Message 組件
        """
        # 警訊等級配置
        warning_configs = {
            1: {"color": "#4CAF50", "icon": "🟢", "text": "正常"},
            2: {"color": "#8BC34A", "icon": "🟡", "text": "注意"},
            3: {"color": "#FFC107", "icon": "🟠", "text": "警告"},
            4: {"color": "#FF9800", "icon": "🟠", "text": "危險"},
            5: {"color": "#F44336", "icon": "🔴", "text": "緊急"},
        }

        config = warning_configs.get(level, warning_configs[1])

        return {
            "type": "box",
            "layout": "horizontal",
            "spacing": "md",
            "backgroundColor": config["color"],
            "cornerRadius": "8px",
            "paddingAll": "12px",
            "contents": [
                {"type": "text", "text": config["icon"], "size": "lg"},
                {
                    "type": "box",
                    "layout": "vertical",
                    "flex": 1,
                    "contents": [
                        {
                            "type": "text",
                            "text": f"警訊等級 {level}: {config['text']}",
                            "weight": "bold",
                            "color": "#FFFFFF",
                            "size": "sm",
                        },
                        {
                            "type": "text",
                            "text": message,
                            "color": "#FFFFFF",
                            "size": "xs",
                            "wrap": True,
                        },
                    ],
                },
            ],
        }

    @staticmethod
    def create_timeline_chart(
        events: List[Dict[str, Any]], title: str = "症狀時間軸"
    ) -> Dict[str, Any]:
        """
        創建時間軸症狀變化圖表

        Args:
            events: 事件列表，格式為 [{"date": "2024-01", "symptom": "症狀", "severity": 3}]
            title: 圖表標題

        Returns:
            Flex Message 組件
        """
        timeline_items = []

        for i, event in enumerate(events):
            # 嚴重程度顏色
            severity_colors = {
                1: "#4CAF50",
                2: "#8BC34A",
                3: "#FFC107",
                4: "#FF9800",
                5: "#F44336",
            }
            color = severity_colors.get(event.get("severity", 1), "#9E9E9E")

            item = {
                "type": "box",
                "layout": "horizontal",
                "spacing": "sm",
                "contents": [
                    {
                        "type": "box",
                        "width": "8px",
                        "height": "8px",
                        "backgroundColor": color,
                        "cornerRadius": "4px",
                    },
                    {
                        "type": "box",
                        "layout": "vertical",
                        "flex": 1,
                        "contents": [
                            {
                                "type": "text",
                                "text": event.get("date", ""),
                                "size": "xs",
                                "color": "#666666",
                            },
                            {
                                "type": "text",
                                "text": event.get("symptom", ""),
                                "size": "sm",
                                "color": "#333333",
                                "weight": "bold",
                            },
                        ],
                    },
                ],
            }
            timeline_items.append(item)

            # 添加分隔線（除了最後一個項目）
            if i < len(events) - 1:
                timeline_items.append({"type": "separator", "margin": "sm"})

        return {
            "type": "box",
            "layout": "vertical",
            "spacing": "md",
            "contents": [
                {
                    "type": "text",
                    "text": title,
                    "weight": "bold",
                    "size": "lg",
                    "color": "#333333",
                },
                *timeline_items,
            ],
        }


class FlexMessageBuilder:
    """Flex Message 構建器"""

    @staticmethod
    def create_m1_analysis_message(
        symptoms: Dict[str, int],
        risk_factors: Dict[str, float],
        warning_level: int,
        warning_message: str,
        timeline_events: Optional[List[Dict[str, Any]]] = None,
    ) -> FlexSendMessage:
        """
        創建 M1 模組分析結果的 Flex Message

        Args:
            symptoms: 症狀嚴重程度
            risk_factors: 風險因素
            warning_level: 警訊等級
            warning_message: 警訊訊息
            timeline_events: 時間軸事件（可選）

        Returns:
            FlexSendMessage
        """
        contents = []

        # 1. 警訊指示器
        contents.append(
            ChartComponents.create_warning_indicator(warning_level, warning_message)
        )
        contents.append({"type": "separator", "margin": "lg"})

        # 2. 症狀嚴重程度圖表
        contents.append(ChartComponents.create_severity_chart(symptoms))
        contents.append({"type": "separator", "margin": "lg"})

        # 3. 風險評估圖表
        contents.append(ChartComponents.create_risk_radar_chart(risk_factors))

        # 4. 時間軸（如果有數據）
        if timeline_events:
            contents.append({"type": "separator", "margin": "lg"})
            contents.append(ChartComponents.create_timeline_chart(timeline_events))

        # 5. 建議按鈕
        contents.append(
            {
                "type": "box",
                "layout": "vertical",
                "spacing": "sm",
                "margin": "lg",
                "contents": [
                    {
                        "type": "button",
                        "action": {
                            "type": "postback",
                            "label": "📋 詳細建議",
                            "data": "m1_detailed_advice",
                        },
                        "style": "primary",
                        "color": "#4CAF50",
                    },
                    {
                        "type": "button",
                        "action": {
                            "type": "postback",
                            "label": "🏥 醫療資源",
                            "data": "m1_medical_resources",
                        },
                        "style": "secondary",
                        "color": "#2196F3",
                    },
                ],
            }
        )

        return FlexSendMessage(
            alt_text="失智症警訊徵兆檢測結果",
            contents={
                "type": "bubble",
                "size": "giga",
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "spacing": "md",
                    "contents": contents,
                },
            },
        )
