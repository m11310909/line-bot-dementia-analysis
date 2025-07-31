"""
M1 模組：失智症十大警訊比對
提供視覺化的警訊比對卡片，幫助用戶理解正常老化 vs 失智症警訊
"""

import json
from typing import Dict, List, Any
from dataclasses import dataclass

@dataclass
class WarningSign:
    id: str
    title: str
    description: str
    normal_aging: str
    dementia_warning: str
    severity: str
    action: str

class M1WarningSignsModule:
    def __init__(self):
        self.warning_signs = self._load_warning_signs()
    
    def _load_warning_signs(self) -> List[WarningSign]:
        """載入十大警訊資料"""
        return [
            WarningSign(
                id="M1-01",
                title="記憶力減退",
                description="忘記最近發生的事情",
                normal_aging="偶爾忘記鑰匙放哪裡",
                dementia_warning="忘記剛吃過飯、重複問同樣問題",
                severity="high",
                action="建議及早就醫評估"
            ),
            WarningSign(
                id="M1-02", 
                title="日常生活能力下降",
                description="無法完成熟悉的家務",
                normal_aging="偶爾忘記關瓦斯",
                dementia_warning="不會使用洗衣機、忘記如何煮飯",
                severity="high",
                action="需要家屬協助，建議就醫"
            ),
            WarningSign(
                id="M1-03",
                title="語言表達困難",
                description="找不到適當的詞彙",
                normal_aging="偶爾想不起來某個詞",
                dementia_warning="無法表達簡單需求、詞彙量明顯減少",
                severity="medium",
                action="建議語言治療評估"
            ),
            WarningSign(
                id="M1-04",
                title="時間空間概念混亂",
                description="搞不清楚時間地點",
                normal_aging="偶爾忘記今天是星期幾",
                dementia_warning="在熟悉的地方迷路、搞不清楚季節",
                severity="high",
                action="建議神經科就醫"
            ),
            WarningSign(
                id="M1-05",
                title="判斷力減退",
                description="無法做出合理判斷",
                normal_aging="偶爾做錯決定",
                dementia_warning="容易被詐騙、無法處理金錢",
                severity="high",
                action="需要監護人協助"
            )
        ]
    
    def create_visual_comparison_card(self, user_input: str, matched_signs: List[str]) -> Dict:
        """創建視覺化比對卡片"""
        if not matched_signs:
            return self._create_general_card(user_input)
        
        # 選擇最相關的警訊
        primary_sign = matched_signs[0] if matched_signs else "M1-01"
        warning_sign = next((sign for sign in self.warning_signs if sign.id == primary_sign), self.warning_signs[0])
        
        return {
            "type": "flex",
            "altText": f"失智症警訊分析：{warning_sign.title}",
            "contents": {
                "type": "bubble",
                "size": "kilo",
                "header": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "text",
                            "text": f"⚠️ {warning_sign.title}",
                            "weight": "bold",
                            "size": "lg",
                            "color": "#ffffff"
                        }
                    ],
                    "backgroundColor": "#d9534f",
                    "paddingAll": "15dp"
                },
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "text",
                            "text": "🔍 警訊比對分析",
                            "weight": "bold",
                            "size": "md",
                            "color": "#d9534f",
                            "margin": "md"
                        },
                        {
                            "type": "separator",
                            "margin": "md"
                        },
                        {
                            "type": "box",
                            "layout": "vertical",
                            "margin": "md",
                            "contents": [
                                {
                                    "type": "text",
                                    "text": "✅ 正常老化",
                                    "size": "sm",
                                    "weight": "bold",
                                    "color": "#5cb85c"
                                },
                                {
                                    "type": "text",
                                    "text": warning_sign.normal_aging,
                                    "size": "sm",
                                    "wrap": True,
                                    "margin": "xs"
                                }
                            ]
                        },
                        {
                            "type": "box",
                            "layout": "vertical",
                            "margin": "md",
                            "contents": [
                                {
                                    "type": "text",
                                    "text": "🚨 失智症警訊",
                                    "size": "sm",
                                    "weight": "bold",
                                    "color": "#d9534f"
                                },
                                {
                                    "type": "text",
                                    "text": warning_sign.dementia_warning,
                                    "size": "sm",
                                    "wrap": True,
                                    "margin": "xs"
                                }
                            ]
                        },
                        {
                            "type": "separator",
                            "margin": "md"
                        },
                        {
                            "type": "text",
                            "text": f"📝 用戶描述：{user_input}",
                            "size": "sm",
                            "color": "#666666",
                            "wrap": True,
                            "margin": "md"
                        },
                        {
                            "type": "text",
                            "text": f"💡 建議：{warning_sign.action}",
                            "size": "sm",
                            "weight": "bold",
                            "color": "#0275d8",
                            "wrap": True,
                            "margin": "md"
                        }
                    ]
                },
                "footer": {
                    "type": "box",
                    "layout": "horizontal",
                    "contents": [
                        {
                            "type": "button",
                            "style": "primary",
                            "height": "sm",
                            "action": {
                                "type": "message",
                                "label": "更多警訊",
                                "text": "請提供更多詳細症狀"
                            },
                            "flex": 1
                        }
                    ]
                }
            }
        }
    
    def _create_general_card(self, user_input: str) -> Dict:
        """創建一般性警訊卡片"""
        return {
            "type": "flex",
            "altText": "失智症警訊分析",
            "contents": {
                "type": "bubble",
                "size": "kilo",
                "header": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "text",
                            "text": "🧠 失智症警訊分析",
                            "weight": "bold",
                            "size": "lg",
                            "color": "#ffffff"
                        }
                    ],
                    "backgroundColor": "#005073",
                    "paddingAll": "15dp"
                },
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "text",
                            "text": "🔍 根據您的描述進行初步分析，建議提供更具體的症狀資訊以獲得精確評估。",
                            "weight": "bold",
                            "size": "md",
                            "color": "#005073",
                            "wrap": True
                        },
                        {
                            "type": "separator",
                            "margin": "md"
                        },
                        {
                            "type": "text",
                            "text": f"📝 用戶描述：{user_input}",
                            "size": "sm",
                            "color": "#666666",
                            "wrap": True,
                            "margin": "md"
                        }
                    ]
                },
                "footer": {
                    "type": "box",
                    "layout": "horizontal",
                    "contents": [
                        {
                            "type": "button",
                            "style": "primary",
                            "height": "sm",
                            "action": {
                                "type": "message",
                                "label": "詳細症狀",
                                "text": "請描述具體的症狀表現"
                            },
                            "flex": 1
                        }
                    ]
                }
            }
        }
    
    def analyze_warning_signs(self, user_input: str) -> Dict:
        """分析用戶輸入中的警訊關鍵字"""
        user_input_lower = user_input.lower()
        matched_signs = []
        
        # 關鍵字對應
        keyword_mapping = {
            "記憶": ["M1-01"],
            "忘記": ["M1-01"],
            "重複": ["M1-01"],
            "洗衣機": ["M1-02"],
            "不會用": ["M1-02"],
            "家務": ["M1-02"],
            "語言": ["M1-03"],
            "詞彙": ["M1-03"],
            "表達": ["M1-03"],
            "迷路": ["M1-04"],
            "時間": ["M1-04"],
            "空間": ["M1-04"],
            "判斷": ["M1-05"],
            "詐騙": ["M1-05"],
            "金錢": ["M1-05"]
        }
        
        for keyword, sign_ids in keyword_mapping.items():
            if keyword in user_input_lower:
                matched_signs.extend(sign_ids)
        
        return {
            "matched_signs": list(set(matched_signs)),
            "analysis": f"在您的描述中發現 {len(matched_signs)} 個可能的警訊"
        } 