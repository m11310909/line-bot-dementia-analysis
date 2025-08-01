"""
M3 模組：行為心理症狀分類 (BPSD)
提供視覺化的行為心理症狀分析，包含症狀分類和處理建議
"""

from typing import Dict, List, Any
from dataclasses import dataclass
from enum import Enum
from safe_enum_handler import safe_enum_value

class BPSDCategory(Enum):
    AGITATION = "激動/攻擊"
    DEPRESSION = "憂鬱/焦慮"
    PSYCHOSIS = "精神病症狀"
    APATHY = "冷漠/退縮"
    SLEEP = "睡眠障礙"

@dataclass
class BPSDSymptom:
    category: BPSDCategory
    symptoms: List[str]
    triggers: List[str]
    interventions: List[str]
    severity_levels: Dict[str, str]
    color: str
    icon: str

class M3BPSDClassificationModule:
    def __init__(self):
        self.bpsd_symptoms = self._load_bpsd_symptoms()
    
    def _load_bpsd_symptoms(self) -> Dict[BPSDCategory, BPSDSymptom]:
        """載入 BPSD 症狀資料"""
        return {
            BPSDCategory.AGITATION: BPSDSymptom(
                category=BPSDCategory.AGITATION,
                symptoms=[
                    "暴躁易怒，情緒不穩",
                    "攻擊性行為，推打他人",
                    "大聲叫罵，言語攻擊",
                    "坐立不安，來回走動",
                    "拒絕照護，反抗行為"
                ],
                triggers=[
                    "環境改變或刺激過多",
                    "身體不適或疼痛",
                    "溝通困難或挫折",
                    "無聊或缺乏活動"
                ],
                interventions=[
                    "保持環境安靜，減少刺激",
                    "建立規律作息，提供安全感",
                    "使用非藥物療法，如音樂療法",
                    "必要時尋求醫療協助"
                ],
                severity_levels={
                    "mild": "偶爾情緒不穩，可安撫",
                    "moderate": "經常暴躁，需要干預",
                    "severe": "持續攻擊行為，需要醫療"
                },
                color="#dc3545",
                icon="😠"
            ),
            BPSDCategory.DEPRESSION: BPSDSymptom(
                category=BPSDCategory.DEPRESSION,
                symptoms=[
                    "情緒低落，缺乏興趣",
                    "食慾改變，體重減輕",
                    "睡眠障礙，早醒或失眠",
                    "自責自貶，負面想法",
                    "社交退縮，不願與人互動"
                ],
                triggers=[
                    "認知功能下降的挫折感",
                    "失去獨立能力的失落感",
                    "社交活動減少",
                    "身體健康狀況惡化"
                ],
                interventions=[
                    "增加社交活動和陪伴",
                    "提供認知刺激和成就感",
                    "建立規律作息和運動",
                    "必要時尋求心理治療"
                ],
                severity_levels={
                    "mild": "偶爾情緒低落，可改善",
                    "moderate": "持續憂鬱，影響生活",
                    "severe": "嚴重憂鬱，需要醫療"
                },
                color="#6f42c1",
                icon="😢"
            ),
            BPSDCategory.PSYCHOSIS: BPSDSymptom(
                category=BPSDCategory.PSYCHOSIS,
                symptoms=[
                    "幻覺，看到或聽到不存在的事物",
                    "妄想，堅信錯誤的想法",
                    "錯認，認錯人或地方",
                    "妄想性懷疑，懷疑被偷或被騙",
                    "視覺幻覺，看到動物或人物"
                ],
                triggers=[
                    "認知功能嚴重受損",
                    "環境改變或刺激",
                    "身體不適或感染",
                    "藥物副作用"
                ],
                interventions=[
                    "保持環境穩定，避免突然改變",
                    "使用現實導向，溫和糾正",
                    "避免爭辯，順應其需求",
                    "必要時尋求精神科協助"
                ],
                severity_levels={
                    "mild": "偶爾錯認，可糾正",
                    "moderate": "經常幻覺，影響生活",
                    "severe": "持續妄想，需要醫療"
                },
                color="#fd7e14",
                icon="👻"
            ),
            BPSDCategory.APATHY: BPSDSymptom(
                category=BPSDCategory.APATHY,
                symptoms=[
                    "缺乏動機，不願活動",
                    "情感淡漠，缺乏表情",
                    "社交退縮，不願與人互動",
                    "興趣減退，不參與活動",
                    "被動依賴，需要他人推動"
                ],
                triggers=[
                    "認知功能下降",
                    "缺乏刺激和活動",
                    "身體健康狀況不佳",
                    "環境單調無趣"
                ],
                interventions=[
                    "提供適當的刺激和活動",
                    "鼓勵參與社交活動",
                    "建立成就感和小目標",
                    "保持身體健康"
                ],
                severity_levels={
                    "mild": "偶爾缺乏興趣，可鼓勵",
                    "moderate": "經常被動，需要推動",
                    "severe": "完全退縮，需要照護"
                },
                color="#6c757d",
                icon="😐"
            ),
            BPSDCategory.SLEEP: BPSDSymptom(
                category=BPSDCategory.SLEEP,
                symptoms=[
                    "日夜顛倒，白天睡覺晚上清醒",
                    "睡眠時間不規律",
                    "夜間遊走，四處走動",
                    "睡眠品質差，容易醒來",
                    "白天嗜睡，精神不佳"
                ],
                triggers=[
                    "生理時鐘混亂",
                    "白天活動不足",
                    "環境不適或噪音",
                    "身體不適或疼痛"
                ],
                interventions=[
                    "建立規律作息，固定睡眠時間",
                    "增加白天活動和運動",
                    "改善睡眠環境，減少干擾",
                    "避免午睡過長"
                ],
                severity_levels={
                    "mild": "偶爾睡眠不規律",
                    "moderate": "經常日夜顛倒",
                    "severe": "嚴重影響生活作息"
                },
                color="#17a2b8",
                icon="😴"
            )
        }
    
    def analyze_bpsd_symptoms(self, user_input: str) -> Dict:
        """分析用戶輸入中的 BPSD 症狀"""
        user_input_lower = user_input.lower()
        
        # 關鍵字對應不同症狀類別
        category_keywords = {
            BPSDCategory.AGITATION: ["暴躁", "易怒", "攻擊", "打人", "罵人", "反抗"],
            BPSDCategory.DEPRESSION: ["憂鬱", "低落", "不開心", "想哭", "沒興趣", "退縮"],
            BPSDCategory.PSYCHOSIS: ["幻覺", "妄想", "看到", "聽到", "錯認", "懷疑"],
            BPSDCategory.APATHY: ["冷漠", "沒興趣", "被動", "退縮", "不說話"],
            BPSDCategory.SLEEP: ["睡不著", "日夜顛倒", "遊走", "睡眠", "晚上"]
        }
        
        # 分析症狀
        detected_categories = []
        for category, keywords in category_keywords.items():
            for keyword in keywords:
                if keyword in user_input_lower:
                    detected_categories.append(category)
                    break
        
        return {
            "detected_categories": list(set(detected_categories)),
            "primary_category": detected_categories[0] if detected_categories else None,
            "analysis": f"發現 {len(detected_categories)} 種行為心理症狀"
        }
    
    def create_bpsd_card(self, user_input: str, bpsd_analysis: Dict) -> Dict:
        """創建 BPSD 症狀分析卡片"""
        if not bpsd_analysis["detected_categories"]:
            return self._create_general_bpsd_card(user_input)
        
        primary_category = bpsd_analysis["primary_category"]
        symptom_info = self.bpsd_symptoms[primary_category]
        
        return {
            "type": "flex",
            "altText": f"行為心理症狀分析：{safe_enum_value(symptom_info.category, 'unknown')}",
            "contents": {
                "type": "bubble",
                "size": "kilo",
                "header": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "text",
                            "text": f"{symptom_info.icon} {safe_enum_value(symptom_info.category, 'unknown')}",
                            "weight": "bold",
                            "size": "lg",
                            "color": "#ffffff"
                        }
                    ],
                    "backgroundColor": symptom_info.color,
                    "paddingAll": "15dp"
                },
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "text",
                            "text": "🔍 症狀特徵",
                            "weight": "bold",
                            "size": "sm",
                            "color": "#666666",
                            "margin": "md"
                        },
                        *self._create_symptom_list(symptom_info.symptoms),
                        {
                            "type": "separator",
                            "margin": "md"
                        },
                        {
                            "type": "text",
                            "text": "💡 處理建議",
                            "weight": "bold",
                            "size": "sm",
                            "color": "#666666",
                            "margin": "md"
                        },
                        *self._create_intervention_list(symptom_info.interventions),
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
                                "text": "請描述更多行為症狀"
                            },
                            "flex": 1
                        }
                    ]
                }
            }
        }
    
    def _create_general_bpsd_card(self, user_input: str) -> Dict:
        """創建一般性 BPSD 卡片"""
        return {
            "type": "flex",
            "altText": "行為心理症狀分析",
            "contents": {
                "type": "bubble",
                "size": "kilo",
                "header": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "text",
                            "text": "🧠 行為心理症狀分析",
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
                            "text": "🔍 根據您的描述進行行為心理症狀分析，建議提供更具體的症狀表現。",
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
                                "text": "請描述具體的行為症狀"
                            },
                            "flex": 1
                        }
                    ]
                }
            }
        }
    
    def _create_symptom_list(self, symptoms: List[str]) -> List[Dict]:
        """創建症狀列表"""
        contents = []
        for symptom in symptoms[:3]:  # 只顯示前3個
            contents.append({
                "type": "text",
                "text": f"• {symptom}",
                "size": "sm",
                "wrap": True,
                "margin": "xs"
            })
        return contents
    
    def _create_intervention_list(self, interventions: List[str]) -> List[Dict]:
        """創建處理建議列表"""
        contents = []
        for intervention in interventions[:3]:  # 只顯示前3個
            contents.append({
                "type": "text",
                "text": f"• {intervention}",
                "size": "sm",
                "wrap": True,
                "margin": "xs"
            })
        return contents 