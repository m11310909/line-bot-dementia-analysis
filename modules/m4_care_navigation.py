"""
M4 模組：照護導航系統
提供視覺化的照護資源導航，包含醫療資源、社會支持、照護技巧等
"""

from typing import Dict, List, Any
from dataclasses import dataclass
from enum import Enum

class CareCategory(Enum):
    MEDICAL = "醫療資源"
    SOCIAL = "社會支持"
    SKILLS = "照護技巧"
    EMERGENCY = "緊急處理"
    LEGAL = "法律權益"

@dataclass
class CareResource:
    category: CareCategory
    title: str
    description: str
    resources: List[str]
    contact_info: List[str]
    tips: List[str]
    color: str
    icon: str

class M4CareNavigationModule:
    def __init__(self):
        self.care_resources = self._load_care_resources()
    
    def _load_care_resources(self) -> Dict[CareCategory, CareResource]:
        """載入照護資源資料"""
        return {
            CareCategory.MEDICAL: CareResource(
                category=CareCategory.MEDICAL,
                title="醫療資源導航",
                description="專業醫療評估和治療資源",
                resources=[
                    "神經科醫師評估",
                    "精神科醫師諮詢",
                    "認知功能評估",
                    "藥物治療追蹤",
                    "復健治療服務"
                ],
                contact_info=[
                    "各大醫院神經科門診",
                    "失智症專科診所",
                    "認知障礙評估中心",
                    "社區心理衛生中心"
                ],
                tips=[
                    "建議先至神經科進行完整評估",
                    "定期追蹤認知功能變化",
                    "記錄症狀變化供醫師參考",
                    "詢問藥物副作用和注意事項"
                ],
                color="#007bff",
                icon="🏥"
            ),
            CareCategory.SOCIAL: CareResource(
                category=CareCategory.SOCIAL,
                title="社會支持資源",
                description="社會福利和照護支持服務",
                resources=[
                    "失智症照護者支持團體",
                    "日間照護中心",
                    "居家照護服務",
                    "喘息服務",
                    "經濟補助申請"
                ],
                contact_info=[
                    "各縣市社會局",
                    "失智症協會",
                    "長照管理中心",
                    "家庭照顧者關懷總會"
                ],
                tips=[
                    "主動尋求社會資源協助",
                    "參加照護者支持團體",
                    "申請相關補助減輕負擔",
                    "建立照護者互助網絡"
                ],
                color="#28a745",
                icon="🤝"
            ),
            CareCategory.SKILLS: CareResource(
                category=CareCategory.SKILLS,
                title="照護技巧指導",
                description="實用的照護技巧和知識",
                resources=[
                    "溝通技巧訓練",
                    "行為問題處理",
                    "環境安全設計",
                    "營養照護指導",
                    "活動設計技巧"
                ],
                contact_info=[
                    "失智症照護教育課程",
                    "護理師居家指導",
                    "職能治療師諮詢",
                    "營養師評估服務"
                ],
                tips=[
                    "學習有效的溝通方式",
                    "建立安全的居家環境",
                    "設計適合的活動",
                    "注意營養均衡"
                ],
                color="#ffc107",
                icon="📚"
            ),
            CareCategory.EMERGENCY: CareResource(
                category=CareCategory.EMERGENCY,
                title="緊急處理指南",
                description="緊急情況的處理方法和資源",
                resources=[
                    "走失處理流程",
                    "急性症狀處理",
                    "意外事件應對",
                    "緊急聯絡資訊",
                    "救護車叫車"
                ],
                contact_info=[
                    "警察局失蹤人口協尋",
                    "119緊急救護",
                    "醫院急診室",
                    "24小時照護專線"
                ],
                tips=[
                    "準備緊急聯絡卡",
                    "安裝GPS定位裝置",
                    "記錄重要醫療資訊",
                    "建立緊急應變計畫"
                ],
                color="#dc3545",
                icon="🚨"
            ),
            CareCategory.LEGAL: CareResource(
                category=CareCategory.LEGAL,
                title="法律權益保障",
                description="法律權益和財產保護",
                resources=[
                    "監護宣告申請",
                    "財產信託規劃",
                    "遺產規劃諮詢",
                    "保險理賠協助",
                    "法律諮詢服務"
                ],
                contact_info=[
                    "法院家事法庭",
                    "法律扶助基金會",
                    "律師公會",
                    "社會局法律諮詢"
                ],
                tips=[
                    "及早規劃財產管理",
                    "了解監護宣告程序",
                    "準備相關法律文件",
                    "尋求專業法律諮詢"
                ],
                color="#6f42c1",
                icon="⚖️"
            )
        }
    
    def analyze_care_needs(self, user_input: str) -> Dict:
        """分析用戶的照護需求"""
        user_input_lower = user_input.lower()
        
        # 關鍵字對應不同照護需求
        care_keywords = {
            CareCategory.MEDICAL: ["醫生", "醫院", "治療", "藥物", "評估", "診斷"],
            CareCategory.SOCIAL: ["補助", "資源", "支持", "團體", "服務", "幫助"],
            CareCategory.SKILLS: ["技巧", "方法", "怎麼做", "照顧", "溝通", "活動"],
            CareCategory.EMERGENCY: ["緊急", "走失", "意外", "危險", "救護", "警察"],
            CareCategory.LEGAL: ["法律", "財產", "監護", "權益", "保險", "遺產"]
        }
        
        # 分析需求
        detected_needs = []
        for category, keywords in care_keywords.items():
            for keyword in keywords:
                if keyword in user_input_lower:
                    detected_needs.append(category)
                    break
        
        return {
            "detected_needs": list(set(detected_needs)),
            "primary_need": detected_needs[0] if detected_needs else None,
            "analysis": f"識別出 {len(detected_needs)} 種照護需求"
        }
    
    def create_care_navigation_card(self, user_input: str, care_analysis: Dict) -> Dict:
        """創建照護導航卡片"""
        if not care_analysis["detected_needs"]:
            return self._create_general_care_card(user_input)
        
        primary_need = care_analysis["primary_need"]
        care_resource = self.care_resources[primary_need]
        
        return {
            "type": "flex",
            "altText": f"照護導航：{care_resource.title}",
            "contents": {
                "type": "bubble",
                "size": "kilo",
                "header": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "text",
                            "text": f"{care_resource.icon} {care_resource.title}",
                            "weight": "bold",
                            "size": "lg",
                            "color": "#ffffff"
                        }
                    ],
                    "backgroundColor": care_resource.color,
                    "paddingAll": "15dp"
                },
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "text",
                            "text": care_resource.description,
                            "weight": "bold",
                            "size": "md",
                            "color": care_resource.color,
                            "wrap": True,
                            "margin": "md"
                        },
                        {
                            "type": "separator",
                            "margin": "md"
                        },
                        {
                            "type": "text",
                            "text": "📋 可用資源",
                            "weight": "bold",
                            "size": "sm",
                            "color": "#666666",
                            "margin": "md"
                        },
                        *self._create_resource_list(care_resource.resources),
                        {
                            "type": "separator",
                            "margin": "md"
                        },
                        {
                            "type": "text",
                            "text": "💡 實用建議",
                            "weight": "bold",
                            "size": "sm",
                            "color": "#666666",
                            "margin": "md"
                        },
                        *self._create_tips_list(care_resource.tips),
                        {
                            "type": "separator",
                            "margin": "md"
                        },
                        {
                            "type": "text",
                            "text": f"📝 用戶需求：{user_input}",
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
                                "label": "更多資源",
                                "text": "請提供更多照護需求"
                            },
                            "flex": 1
                        }
                    ]
                }
            }
        }
    
    def _create_general_care_card(self, user_input: str) -> Dict:
        """創建一般性照護導航卡片"""
        return {
            "type": "flex",
            "altText": "照護導航系統",
            "contents": {
                "type": "bubble",
                "size": "kilo",
                "header": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "text",
                            "text": "🧭 照護導航系統",
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
                            "text": "🔍 根據您的需求提供照護資源導航，包含醫療、社會支持、照護技巧等全方位協助。",
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
                            "text": f"📝 用戶需求：{user_input}",
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
                                "label": "詳細需求",
                                "text": "請描述具體的照護需求"
                            },
                            "flex": 1
                        }
                    ]
                }
            }
        }
    
    def _create_resource_list(self, resources: List[str]) -> List[Dict]:
        """創建資源列表"""
        contents = []
        for resource in resources[:3]:  # 只顯示前3個
            contents.append({
                "type": "text",
                "text": f"• {resource}",
                "size": "sm",
                "wrap": True,
                "margin": "xs"
            })
        return contents
    
    def _create_tips_list(self, tips: List[str]) -> List[Dict]:
        """創建建議列表"""
        contents = []
        for tip in tips[:3]:  # 只顯示前3個
            contents.append({
                "type": "text",
                "text": f"• {tip}",
                "size": "sm",
                "wrap": True,
                "margin": "xs"
            })
        return contents 