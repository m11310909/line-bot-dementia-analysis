#!/usr/bin/env python3
"""
M1 警訊分析視覺化模組
Generates Flex Messages for M1 Dementia Warning Analysis
"""

import json
from datetime import datetime
from typing import Dict, Any, Optional
from enum import Enum


class WarningLevel(Enum):
    """警訊等級"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class M1VisualizationGenerator:
    """M1 警訊分析視覺化生成器"""
    
    def __init__(self):
        self.colors = {
            'header_bg': '#E74C3C',      # 紅色背景
            'text_white': '#ffffff',      # 白色文字
            'text_primary': '#333333',    # 主要文字
            'text_secondary': '#666666',  # 次要文字
            'warning': '#E74C3C',         # 警告色
            'success': '#27AE60',         # 成功色
            'info': '#3498DB'             # 資訊色
        }
    
    def generate_m1_flex_message(
        self, 
        user_input: str,
        analysis_result: str,
        warning_level: WarningLevel = WarningLevel.HIGH,
        confidence_score: float = 0.85,
        recommendations: Optional[list] = None
    ) -> Dict[str, Any]:
        """
        生成 M1 警訊分析 Flex Message
        
        Args:
            user_input: 使用者輸入的描述
            analysis_result: 分析結果
            warning_level: 警訊等級
            confidence_score: 信心度分數 (0-1)
            recommendations: 建議清單
        
        Returns:
            Dict: Flex Message JSON (simulator format)
        """
        
        # 預設建議
        if recommendations is None:
            recommendations = [
                "立即尋求專業醫療評估",
                "考慮安裝安全裝置",
                "定期進行認知功能檢查"
            ]
        
        # 警訊等級文字
        warning_text = {
            WarningLevel.LOW: "低",
            WarningLevel.MEDIUM: "中",
            WarningLevel.HIGH: "高",
            WarningLevel.CRITICAL: "極高"
        }
        
        # 生成 Flex Message
        flex_message = {
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
                        "color": self.colors['text_white'],
                        "size": "lg"
                    }
                ],
                "backgroundColor": self.colors['header_bg']
            },
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    # 使用者描述
                    {
                        "type": "text",
                        "text": f"📝 您的描述：\n{user_input}",
                        "wrap": True,
                        "size": "sm",
                        "color": self.colors['text_secondary']
                    },
                    {
                        "type": "separator"
                    },
                    # 分析結果
                    {
                        "type": "text",
                        "text": "🔍 分析結果：",
                        "weight": "bold",
                        "size": "sm",
                        "color": self.colors['text_primary']
                    },
                    {
                        "type": "text",
                        "text": f"⚠️ 警訊等級：{warning_text[warning_level]}\n\n{analysis_result}",
                        "wrap": True,
                        "size": "sm",
                        "color": self.colors['warning']
                    },
                    # 建議
                    {
                        "type": "text",
                        "text": f"💡 建議：\n• " + "\n• ".join(recommendations),
                        "wrap": True,
                        "size": "sm",
                        "color": self.colors['success']
                    }
                ]
            },
            "footer": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "button",
                        "style": "primary",
                        "action": {
                            "type": "postback",
                            "label": "查看詳細說明",
                            "data": "action=m1_details"
                        }
                    },
                    {
                        "type": "button",
                        "style": "secondary",
                        "action": {
                            "type": "uri",
                            "label": "專業諮詢",
                            "uri": "https://www.tada2002.org.tw/"
                        }
                    }
                ]
            }
        }
        
        return flex_message
    
    def generate_full_flex_message(
        self,
        user_input: str,
        analysis_result: str,
        warning_level: WarningLevel = WarningLevel.HIGH,
        confidence_score: float = 0.85,
        recommendations: Optional[list] = None
    ) -> Dict[str, Any]:
        """
        生成完整的 Flex Message (用於 LINE Bot API)
        
        Returns:
            Dict: 完整的 Flex Message JSON (API format)
        """
        contents = self.generate_m1_flex_message(
            user_input, analysis_result, warning_level, confidence_score, recommendations
        )
        
        return {
            "type": "flex",
            "altText": "M1 警訊分析結果",
            "contents": contents
        }
    
    def generate_simulator_json(
        self,
        user_input: str,
        analysis_result: str,
        warning_level: WarningLevel = WarningLevel.HIGH,
        confidence_score: float = 0.85,
        recommendations: Optional[list] = None
    ) -> str:
        """
        生成用於 LINE Flex Message Simulator 的 JSON 字串
        
        Returns:
            str: JSON 字串 (simulator format)
        """
        flex_message = self.generate_m1_flex_message(
            user_input, analysis_result, warning_level, confidence_score, recommendations
        )
        
        return json.dumps(flex_message, ensure_ascii=False, indent=2)
    
    def generate_api_json(
        self,
        user_input: str,
        analysis_result: str,
        warning_level: WarningLevel = WarningLevel.HIGH,
        confidence_score: float = 0.85,
        recommendations: Optional[list] = None
    ) -> str:
        """
        生成用於 LINE Bot API 的 JSON 字串
        
        Returns:
            str: JSON 字串 (API format)
        """
        flex_message = self.generate_full_flex_message(
            user_input, analysis_result, warning_level, confidence_score, recommendations
        )
        
        return json.dumps(flex_message, ensure_ascii=False, indent=2)


def demo_m1_visualization():
    """示範 M1 視覺化功能"""
    
    generator = M1VisualizationGenerator()
    
    # 測試案例
    test_cases = [
        {
            "user_input": "媽媽忘記關瓦斯",
            "analysis_result": "根據您的描述，這可能是失智症的早期警訊。忘記關瓦斯屬於安全相關的記憶問題，需要特別關注。",
            "warning_level": WarningLevel.HIGH,
            "recommendations": [
                "立即尋求專業醫療評估",
                "考慮安裝安全裝置",
                "定期進行認知功能檢查"
            ]
        },
        {
            "user_input": "爸爸不會用洗衣機",
            "analysis_result": "這可能是認知功能下降的徵兆。無法操作熟悉的家電設備是失智症的常見症狀之一。",
            "warning_level": WarningLevel.MEDIUM,
            "recommendations": [
                "安排認知功能評估",
                "考慮簡化操作流程",
                "增加安全監控"
            ]
        },
        {
            "user_input": "爺爺重複問同樣的問題",
            "analysis_result": "重複性行為是失智症的典型症狀。短期記憶受損導致無法記住已問過的問題。",
            "warning_level": WarningLevel.HIGH,
            "recommendations": [
                "尋求神經科醫師評估",
                "建立記憶輔助工具",
                "考慮藥物治療"
            ]
        }
    ]
    
    print("🎨 M1 警訊分析視覺化模組示範")
    print("=" * 50)
    
    for i, case in enumerate(test_cases, 1):
        print(f"\n📋 測試案例 {i}: {case['user_input']}")
        print("-" * 30)
        
        # 生成 Simulator JSON
        simulator_json = generator.generate_simulator_json(
            case['user_input'],
            case['analysis_result'],
            case['warning_level'],
            recommendations=case['recommendations']
        )
        
        print("📱 Simulator JSON (複製到 LINE Flex Message Simulator):")
        print(simulator_json)
        
        # 生成 API JSON
        api_json = generator.generate_api_json(
            case['user_input'],
            case['analysis_result'],
            case['warning_level'],
            recommendations=case['recommendations']
        )
        
        print(f"\n🤖 API JSON (用於 LINE Bot):")
        print(api_json)
        
        print("\n" + "="*50)


if __name__ == "__main__":
    demo_m1_visualization() 