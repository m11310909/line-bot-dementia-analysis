"""
🎨 增強版 M1 Flex Message 生成器
基於新的設計指南，提供更簡潔、更直觀的佈局
"""

import json
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime
from dataclasses import dataclass

@dataclass
class M1AnalysisResult:
    """M1 分析結果資料結構"""
    detected_signs: List[str]
    confidence_score: float
    risk_level: str
    risk_color: str
    chatbot_reply: str
    original_text: str
    xai_data: Dict[str, Any]

class EnhancedM1FlexGenerator:
    """增強版 M1 Flex Message 生成器"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.generation_stats = {
            'total_generated': 0,
            'error_count': 0,
            'risk_levels': {'high': 0, 'medium': 0, 'low': 0}
        }
        
        # 顏色配置
        self.colors = {
            "header_bg": "#27AE60",      # 綠色標題背景
            "risk_high": "#E74C3C",      # 高風險紅色
            "risk_medium": "#F39C12",    # 中風險橙色
            "risk_low": "#27AE60",       # 低風險綠色
            "progress_bg": "#F5F5F5",    # 進度條背景
            "progress_fill": "#E0E0E0",  # 進度條填充
            "text_primary": "#000000",    # 主要文字
            "text_secondary": "#666666"   # 次要文字
        }
    
    def create_enhanced_m1_flex_message(self, analysis: Dict[str, Any], original_text: str) -> Dict[str, Any]:
        """創建增強版 M1 警訊 Flex Message - 基於附圖設計"""
        
        try:
            self.generation_stats['total_generated'] += 1
            
            # 解析分析結果
            m1_result = self._parse_analysis_result(analysis, original_text)
            
            # 生成 Flex Message
            flex_message = self._build_flex_message(m1_result)
            
            # 更新統計
            risk_key = m1_result.risk_level.replace('風險', '').lower()
            if risk_key in self.generation_stats['risk_levels']:
                self.generation_stats['risk_levels'][risk_key] += 1
            
            return flex_message
            
        except Exception as e:
            self.generation_stats['error_count'] += 1
            self.logger.error(f"Flex Message 生成失敗: {e}")
            return self._create_error_message(str(e))
    
    def _parse_analysis_result(self, analysis: Dict[str, Any], original_text: str) -> M1AnalysisResult:
        """解析分析結果"""
        
        # 根據檢測到的警訊數量決定風險等級
        warnings = analysis.get("detected_signs", [])
        warning_count = len(warnings)
        
        if warning_count >= 3:
            risk_level = "高風險"
            risk_color = self.colors["risk_high"]
        elif warning_count >= 1:
            risk_level = "中風險"
            risk_color = self.colors["risk_medium"]
        else:
            risk_level = "低風險"
            risk_color = self.colors["risk_low"]
        
        # XAI 數據
        xai_data = analysis.get("xai_data", {})
        confidence_score = xai_data.get("confidence_score", 0.85)
        
        return M1AnalysisResult(
            detected_signs=warnings,
            confidence_score=confidence_score,
            risk_level=risk_level,
            risk_color=risk_color,
            chatbot_reply=analysis.get("chatbot_reply", "根據您的描述進行了初步分析，建議進一步觀察。"),
            original_text=original_text,
            xai_data=xai_data
        )
    
    def _build_flex_message(self, result: M1AnalysisResult) -> Dict[str, Any]:
        """構建 Flex Message"""
        
        return {
            "type": "flex",
            "altText": "M1 警訊分析結果",
            "contents": {
                "type": "bubble",
                "size": "kilo",
                "header": self._build_header(result),
                "body": self._build_body(result),
                "footer": self._build_footer(result)
            }
        }
    
    def _build_header(self, result: M1AnalysisResult) -> Dict[str, Any]:
        """構建標題區"""
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
                            "text": "警訊分析",
                            "color": "#ffffff",
                            "weight": "bold",
                            "size": "lg"
                        },
                        {
                            "type": "box",
                            "layout": "horizontal",
                            "contents": [
                                {
                                    "type": "text",
                                    "text": "🚨",
                                    "size": "sm"
                                },
                                {
                                    "type": "text",
                                    "text": result.risk_level,
                                    "color": "#ffffff",
                                    "size": "sm"
                                }
                            ]
                        }
                    ]
                }
            ],
            "backgroundColor": self.colors["header_bg"],
            "paddingAll": "20px"
        }
    
    def _build_body(self, result: M1AnalysisResult) -> Dict[str, Any]:
        """構建內容區"""
        
        # AI 信心度區塊
        confidence_percentage = int(result.confidence_score * 100)
        confidence_blocks = [
            {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                    {
                        "type": "text",
                        "text": "AI信心度",
                        "size": "sm",
                        "color": self.colors["text_secondary"]
                    },
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "contents": [
                            {
                                "type": "box",
                                "layout": "horizontal",
                                "contents": [
                                    {
                                        "type": "box",
                                        "layout": "horizontal",
                                        "contents": [],
                                        "backgroundColor": self.colors["progress_fill"],
                                        "width": f"{confidence_percentage}%",
                                        "height": "8px"
                                    }
                                ],
                                "backgroundColor": self.colors["progress_bg"],
                                "width": "60px",
                                "height": "8px"
                            },
                            {
                                "type": "text",
                                "text": f"{confidence_percentage}%",
                                "size": "lg",
                                "weight": "bold",
                                "color": self.colors["text_primary"]
                            }
                        ]
                    }
                ]
            },
            {
                "type": "separator",
                "margin": "md"
            }
        ]
        
        # 分析摘要區塊
        analysis_blocks = [
            {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                    {
                        "type": "text",
                        "text": "👨‍⚕️",
                        "size": "sm"
                    },
                    {
                        "type": "text",
                        "text": "分析",
                        "size": "sm",
                        "color": self.colors["text_secondary"]
                    }
                ]
            },
            {
                "type": "text",
                "text": result.chatbot_reply,
                "size": "sm",
                "color": self.colors["text_secondary"],
                "wrap": True
            },
            {
                "type": "separator",
                "margin": "md"
            }
        ]
        
        # 警訊區塊
        warning_blocks = [
            {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                    {
                        "type": "text",
                        "text": "!!",
                        "color": "#FF6B6B",
                        "size": "sm"
                    },
                    {
                        "type": "text",
                        "text": "警訊",
                        "color": "#FF6B6B",
                        "size": "sm"
                    }
                ]
            },
            {
                "type": "box",
                "layout": "vertical",
                "spacing": "sm",
                "contents": self._build_warning_buttons(result.detected_signs)
            }
        ]
        
        return {
            "type": "box",
            "layout": "vertical",
            "spacing": "md",
            "contents": confidence_blocks + analysis_blocks + warning_blocks,
            "paddingAll": "20px"
        }
    
    def _build_warning_buttons(self, warnings: List[str]) -> List[Dict[str, Any]]:
        """構建警訊按鈕"""
        warning_buttons = []
        
        for i, warning in enumerate(warnings[:3]):  # 最多顯示3個警訊
            warning_buttons.append({
                "type": "button",
                "action": {
                    "type": "postback",
                    "label": warning,
                    "data": f"warning_detail_{i+1}"
                },
                "style": "link",
                "color": self.colors["text_secondary"],
                "height": "sm"
            })
        
        # 如果沒有警訊，顯示預設訊息
        if not warnings:
            warning_buttons.append({
                "type": "text",
                "text": "未檢測到明顯警訊",
                "size": "sm",
                "color": self.colors["header_bg"]
            })
        
        return warning_buttons
    
    def _build_footer(self, result: M1AnalysisResult) -> Dict[str, Any]:
        """構建底部按鈕區"""
        return {
            "type": "box",
            "layout": "vertical",
            "spacing": "sm",
            "contents": [
                {
                    "type": "button",
                    "action": {
                        "type": "uri",
                        "label": "🛒 AI小幫手原文",
                        "uri": f"https://your-liff-url.com/original-text?text={result.original_text}"
                    },
                    "style": "link",
                    "color": self.colors["header_bg"]
                },
                {
                    "type": "button",
                    "action": {
                        "type": "uri",
                        "label": "📊 查看完整分析",
                        "uri": "https://your-liff-url.com/full-analysis"
                    },
                    "style": "primary",
                    "color": self.colors["header_bg"]
                },
                {
                    "type": "button",
                    "action": {
                        "type": "postback",
                        "label": "💡 建議下一步",
                        "data": "next_steps"
                    },
                    "style": "secondary",
                    "color": "#3498DB"
                }
            ]
        }
    
    def _create_error_message(self, error_msg: str) -> Dict[str, Any]:
        """創建錯誤訊息"""
        return {
            "type": "flex",
            "altText": "分析發生錯誤",
            "contents": {
                "type": "bubble",
                "size": "kilo",
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "text",
                            "text": "❌ 分析發生錯誤",
                            "weight": "bold",
                            "size": "lg",
                            "color": "#E74C3C"
                        },
                        {
                            "type": "text",
                            "text": error_msg,
                            "size": "sm",
                            "color": self.colors["text_secondary"],
                            "wrap": True
                        }
                    ],
                    "paddingAll": "20px"
                }
            }
        }
    
    def get_stats(self) -> Dict[str, Any]:
        """取得生成統計"""
        return {
            "total_generated": self.generation_stats["total_generated"],
            "error_count": self.generation_stats["error_count"],
            "risk_levels": self.generation_stats["risk_levels"],
            "success_rate": (
                (self.generation_stats["total_generated"] - self.generation_stats["error_count"]) 
                / max(self.generation_stats["total_generated"], 1) * 100
            )
        }

# ===== 測試函數 =====

def test_enhanced_m1_flex_generator():
    """測試增強版 M1 Flex Message 生成器"""
    
    generator = EnhancedM1FlexGenerator()
    
    # 測試案例 1：重複行為警訊
    test_case_1 = {
        "detected_signs": ["重複發問行為", "記憶力減退", "語言表達困難"],
        "xai_data": {
            "confidence_score": 0.85
        },
        "chatbot_reply": "根據您的描述，檢測到多個失智症警訊，建議及早就醫評估。"
    }
    
    # 測試案例 2：安全警訊
    test_case_2 = {
        "detected_signs": ["記憶力減退", "安全意識下降"],
        "xai_data": {
            "confidence_score": 0.90
        },
        "chatbot_reply": "檢測到安全相關警訊，建議立即安裝安全裝置並諮詢醫師。"
    }
    
    # 測試案例 3：無警訊
    test_case_3 = {
        "detected_signs": [],
        "xai_data": {
            "confidence_score": 0.75
        },
        "chatbot_reply": "根據您的描述，目前未檢測到明顯的失智症警訊。"
    }
    
    test_cases = [
        ("重複行為警訊", test_case_1, "媽媽最近常重複問同樣的問題"),
        ("安全警訊", test_case_2, "爸爸忘記關瓦斯爐"),
        ("無警訊", test_case_3, "爺爺偶爾忘記鑰匙放哪裡")
    ]
    
    print("🧪 測試增強版 M1 Flex Message 生成器")
    print("=" * 50)
    
    for name, analysis, original_text in test_cases:
        print(f"\n📋 測試案例：{name}")
        print(f"輸入：{original_text}")
        
        try:
            flex_message = generator.create_enhanced_m1_flex_message(analysis, original_text)
            
            # 檢查結構
            if flex_message.get("type") == "flex" and "contents" in flex_message:
                print("✅ Flex Message 結構正確")
                
                # 檢查標題
                header = flex_message["contents"].get("header", {})
                if header.get("backgroundColor") == "#27AE60":
                    print("✅ 綠色標題設計正確")
                
                # 檢查底部按鈕
                footer = flex_message["contents"].get("footer", {})
                if "contents" in footer and len(footer["contents"]) >= 3:
                    print("✅ 底部按鈕設計正確")
                
                # 計算回應大小
                response_size = len(json.dumps(flex_message, ensure_ascii=False))
                print(f"📏 回應大小：{response_size} 字符")
                
            else:
                print("❌ Flex Message 結構錯誤")
                
        except Exception as e:
            print(f"❌ 測試失敗：{e}")
    
    # 顯示統計
    stats = generator.get_stats()
    print(f"\n📊 生成統計：")
    print(f"總生成次數：{stats['total_generated']}")
    print(f"錯誤次數：{stats['error_count']}")
    print(f"成功率：{stats['success_rate']:.1f}%")
    print(f"風險等級分布：{stats['risk_levels']}")

if __name__ == "__main__":
    test_enhanced_m1_flex_generator() 