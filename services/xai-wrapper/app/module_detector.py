from typing import List, Dict

class ModuleDetector:
    def __init__(self):
        self.module_patterns = {
            "M1": {
                "keywords": ["記憶", "忘記", "重複", "迷路", "時間混淆", 
                            "忘記吃藥", "記不住", "想不起來"],
                "intents": ["symptom_check", "memory_concern"],
                "weight": 1.0
            },
            "M2": {
                "keywords": ["階段", "病程", "早期", "中期", "晚期", 
                            "惡化", "進展", "變嚴重"],
                "intents": ["stage_inquiry", "progression_check"],
                "weight": 0.9
            },
            "M3": {
                "keywords": ["躁動", "妄想", "憂鬱", "幻覺", "攻擊",
                            "遊走", "不安", "情緒", "行為"],
                "intents": ["behavioral_symptom", "psychological_symptom"],
                "weight": 1.1
            },
            "M4": {
                "keywords": ["照護", "資源", "申請", "補助", "日常",
                            "醫療", "任務", "協助"],
                "intents": ["care_guidance", "resource_inquiry"],
                "weight": 0.8
            }
        }
        
    def detect(self, user_input: str, keywords: List[str], 
               intent: str, bot_response: Dict) -> str:
        scores = {}
        
        for module, pattern in self.module_patterns.items():
            keyword_score = self._calculate_keyword_score(keywords, pattern["keywords"])
            intent_score = 1.0 if intent in pattern["intents"] else 0.3
            scores[module] = (keyword_score * 0.6 + intent_score * 0.4) * pattern["weight"]
        
        selected = max(scores, key=scores.get)
        return selected if scores[selected] > 0.3 else "M1"
    
    def _calculate_keyword_score(self, found_keywords: List[str], 
                                 pattern_keywords: List[str]) -> float:
        if not found_keywords:
            return 0.0
        matches = sum(1 for kw in found_keywords if any(
            pk in kw or kw in pk for pk in pattern_keywords
        ))
        return min(matches / len(pattern_keywords), 1.0)
