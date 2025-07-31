"""
M2 模組：病程階段評估矩陣
提供視覺化的失智症病程階段評估，包含症狀特徵和照護重點
"""

from typing import Dict, List, Any
from dataclasses import dataclass
from enum import Enum

class Stage(Enum):
    MILD = "輕度"
    MODERATE = "中度" 
    SEVERE = "重度"

@dataclass
class ProgressionStage:
    stage: Stage
    symptoms: List[str]
    care_focus: List[str]
    color: str
    icon: str
    description: str

class M2ProgressionMatrixModule:
    def __init__(self):
        self.stages = self._load_progression_stages()
    
    def _load_progression_stages(self) -> Dict[Stage, ProgressionStage]:
        """載入病程階段資料"""
        return {
            Stage.MILD: ProgressionStage(
                stage=Stage.MILD,
                symptoms=[
                    "記憶力減退，忘記最近發生的事",
                    "語言表達困難，找不到適當詞彙",
                    "時間空間概念開始混亂",
                    "判斷力下降，容易被詐騙",
                    "情緒變化，容易焦慮憂鬱"
                ],
                care_focus=[
                    "建立規律作息，保持認知刺激",
                    "協助記憶，使用提醒工具",
                    "保持社交活動，避免孤立",
                    "定期醫療追蹤，及早介入"
                ],
                color="#ffc107",
                icon="🟡",
                description="認知功能開始下降，但日常生活能力大致正常"
            ),
            Stage.MODERATE: ProgressionStage(
                stage=Stage.MODERATE,
                symptoms=[
                    "記憶力明顯減退，忘記親人姓名",
                    "語言表達嚴重困難，無法完整表達",
                    "在熟悉環境中迷路",
                    "日常生活能力明顯下降",
                    "行為心理症狀加劇"
                ],
                care_focus=[
                    "提供24小時照護，防止走失",
                    "簡化環境，減少刺激",
                    "建立安全防護措施",
                    "尋求專業照護資源"
                ],
                color="#fd7e14",
                icon="🟠",
                description="認知功能明顯受損，需要他人協助"
            ),
            Stage.SEVERE: ProgressionStage(
                stage=Stage.SEVERE,
                symptoms=[
                    "完全失去語言能力",
                    "無法辨識親人",
                    "完全依賴他人照護",
                    "身體功能逐漸退化",
                    "可能出現吞嚥困難"
                ],
                care_focus=[
                    "提供完全照護，注意身體健康",
                    "預防感染和併發症",
                    "維持舒適和尊嚴",
                    "家屬心理支持"
                ],
                color="#dc3545",
                icon="🔴",
                description="認知功能嚴重受損，完全依賴照護"
            )
        }
    
    def analyze_progression_stage(self, user_input: str) -> Dict:
        """分析用戶輸入，評估可能的病程階段"""
        user_input_lower = user_input.lower()
        
        # 關鍵字對應不同階段
        stage_keywords = {
            Stage.MILD: ["輕度", "初期", "剛開始", "記憶力", "忘記", "語言"],
            Stage.MODERATE: ["中度", "中期", "明顯", "迷路", "不會用", "暴躁"],
            Stage.SEVERE: ["重度", "晚期", "嚴重", "完全", "不認識", "臥床"]
        }
        
        # 症狀關鍵字分析
        symptom_scores = {stage: 0 for stage in Stage}
        
        for stage, keywords in stage_keywords.items():
            for keyword in keywords:
                if keyword in user_input_lower:
                    symptom_scores[stage] += 1
        
        # 選擇得分最高的階段
        detected_stage = max(symptom_scores.items(), key=lambda x: x[1])[0]
        
        return {
            "detected_stage": detected_stage,
            "stage_info": self.stages[detected_stage],
            "confidence": "high" if symptom_scores[detected_stage] > 0 else "low",
            "analysis": f"根據描述，可能處於{detected_stage.value}階段"
        }
    
    def create_progression_card(self, user_input: str, stage_analysis: Dict) -> Dict:
        """創建病程階段評估卡片"""
        stage_info = stage_analysis["stage_info"]
        
        return {
            "type": "flex",
            "altText": f"病程階段評估：{stage_info.stage.value}",
            "contents": {
                "type": "bubble",
                "size": "kilo",
                "header": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "text",
                            "text": f"{stage_info.icon} {stage_info.stage.value}階段評估",
                            "weight": "bold",
                            "size": "lg",
                            "color": "#ffffff"
                        }
                    ],
                    "backgroundColor": stage_info.color,
                    "paddingAll": "15dp"
                },
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "text",
                            "text": stage_info.description,
                            "weight": "bold",
                            "size": "md",
                            "color": stage_info.color,
                            "wrap": True,
                            "margin": "md"
                        },
                        {
                            "type": "separator",
                            "margin": "md"
                        },
                        {
                            "type": "text",
                            "text": "🔍 主要症狀特徵",
                            "weight": "bold",
                            "size": "sm",
                            "color": "#666666",
                            "margin": "md"
                        },
                        *self._create_symptom_list(stage_info.symptoms),
                        {
                            "type": "separator",
                            "margin": "md"
                        },
                        {
                            "type": "text",
                            "text": "💡 照護重點",
                            "weight": "bold",
                            "size": "sm",
                            "color": "#666666",
                            "margin": "md"
                        },
                        *self._create_care_list(stage_info.care_focus),
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
                                "text": "請提供更多症狀描述"
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
        for i, symptom in enumerate(symptoms[:3]):  # 只顯示前3個
            contents.append({
                "type": "text",
                "text": f"• {symptom}",
                "size": "sm",
                "wrap": True,
                "margin": "xs"
            })
        return contents
    
    def _create_care_list(self, care_focus: List[str]) -> List[Dict]:
        """創建照護重點列表"""
        contents = []
        for i, care in enumerate(care_focus[:3]):  # 只顯示前3個
            contents.append({
                "type": "text",
                "text": f"• {care}",
                "size": "sm",
                "wrap": True,
                "margin": "xs"
            })
        return contents 