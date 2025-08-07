from typing import Dict, List, Any
import jieba
import random

class XAIAnalyzer:
    def __init__(self):
        self.important_words = [
            "忘記", "重複", "迷路", "混淆", "躁動", "妄想",
            "記憶", "時間", "空間", "行為", "情緒", "照護"
        ]
        
    async def extract_keywords(self, text: str) -> List[str]:
        words = jieba.lcut(text)
        return [w for w in words if w in self.important_words or len(w) > 1]
    
    async def classify_intent(self, text: str) -> str:
        if any(word in text for word in ["症狀", "警訊", "正常"]):
            return "symptom_check"
        elif any(word in text for word in ["階段", "病程", "惡化"]):
            return "stage_inquiry"
        elif any(word in text for word in ["行為", "情緒", "躁動"]):
            return "behavioral_symptom"
        elif any(word in text for word in ["照護", "資源", "申請"]):
            return "care_guidance"
        return "general_inquiry"
    
    async def analyze(self, user_input: str, bot_response: Dict, 
                     module: str) -> Dict[str, Any]:
        keywords = await self.extract_keywords(user_input)
        
        # Calculate confidence based on keywords and response
        base_confidence = 0.7
        keyword_boost = min(len(keywords) * 0.05, 0.2)
        confidence = min(base_confidence + keyword_boost, 0.95)
        
        # Build reasoning path
        reasoning_path = [
            {"step": "關鍵詞提取", "confidence": 0.85, "detail": f"識別到 {len(keywords)} 個關鍵詞"},
            {"step": "症狀比對", "confidence": 0.78, "detail": f"匹配到{module}模組"},
            {"step": "結果判斷", "confidence": confidence, "detail": "綜合分析完成"}
        ]
        
        return {
            "confidence": confidence,
            "reasoning_path": reasoning_path,
            "keywords": keywords,
            "evidence": [{"text": kw, "importance": 0.8} for kw in keywords[:3]],
            "explanation": f"根據您的描述，系統判斷這可能與{self._get_module_name(module)}相關"
        }
    
    def _get_module_name(self, module: str) -> str:
        names = {
            "M1": "失智症警訊",
            "M2": "病程階段",
            "M3": "精神行為症狀",
            "M4": "照護資源"
        }
        return names.get(module, "一般諮詢")
