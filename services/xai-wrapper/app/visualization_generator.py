from typing import Dict, Any

class VisualizationGenerator:
    def __init__(self):
        self.module_templates = self._load_templates()
        
    async def generate(self, module: str, xai_data: Dict[str, Any]) -> Dict[str, Any]:
        if module == "M1":
            return await self._generate_m1(xai_data)
        elif module == "M2":
            return await self._generate_m2(xai_data)
        elif module == "M3":
            return await self._generate_m3(xai_data)
        elif module == "M4":
            return await self._generate_m4(xai_data)
        else:
            return await self._generate_default(xai_data)
    
    async def _generate_m1(self, xai_data: Dict) -> Dict:
        confidence = xai_data["confidence"]
        return {
            "type": "comparison_card",
            "flex_message": {
                "confidence_bar": {
                    "value": confidence,
                    "color": self._get_confidence_color(confidence),
                    "label": f"{int(confidence * 100)}%"
                },
                "reasoning_steps": [
                    {
                        "label": step["step"],
                        "confidence": step["confidence"]
                    }
                    for step in xai_data["reasoning_path"]
                ],
                "comparison": {
                    "normal": {
                        "title": "正常老化",
                        "items": ["偶爾忘記", "提醒後想起", "日常生活正常"],
                        "color": "#4CAF50"
                    },
                    "warning": {
                        "title": "失智警訊",
                        "items": ["影響生活", "重複發問", "忘記重要事件"],
                        "color": "#FF9800"
                    }
                }
            },
            "liff_url": "https://liff.line.me/YOUR_LIFF_ID/m1"
        }
    
    async def _generate_m2(self, xai_data: Dict) -> Dict:
        return {
            "type": "stage_timeline",
            "flex_message": {
                "current_stage": "middle",
                "stages": ["早期", "中期", "晚期"],
                "features": ["日常需協助", "行為症狀", "認知退化"]
            }
        }
    
    async def _generate_m3(self, xai_data: Dict) -> Dict:
        return {
            "type": "symptom_cards",
            "flex_message": {
                "symptoms": [
                    {"name": "躁動不安", "severity": 75, "color": "#F44336"},
                    {"name": "憂鬱情緒", "severity": 60, "color": "#2196F3"}
                ]
            }
        }
    
    async def _generate_m4(self, xai_data: Dict) -> Dict:
        return {
            "type": "task_navigation",
            "flex_message": {
                "tasks": [
                    {"category": "醫療", "priority": "緊急", "action": "預約評估"},
                    {"category": "日常", "priority": "建議", "action": "環境調整"}
                ]
            }
        }
    
    async def _generate_default(self, xai_data: Dict) -> Dict:
        return {
            "type": "simple_text",
            "text": xai_data.get("explanation", "請提供更多資訊")
        }
    
    def _get_confidence_color(self, confidence: float) -> str:
        if confidence > 0.8:
            return "#4CAF50"
        elif confidence > 0.6:
            return "#2196F3"
        else:
            return "#FF9800"
    
    def _load_templates(self) -> Dict:
        return {}
