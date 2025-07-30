"""
智能模組路由系統
階段四任務 7.1：整合 M2-M4 模組路由架構
"""

from typing import Dict, List, Any, Optional
from enum import Enum
import re

class ModuleType(str, Enum):
    M1 = "M1"  # 失智症十大警訊
    M2 = "M2"  # 病程階段分析
    M3 = "M3"  # BPSD 行為心理症狀
    M4 = "M4"  # 照護任務導航

class ModuleRouter:
    """根據 AI 判斷結果路由到對應模組"""
    
    ROUTING_RULES = {
        # M1 → M2 條件
        "M1_to_M2": {
            "triggers": [
                "中期症狀", "行為改變", "認知退化明顯", "記憶力明顯減退",
                "定向感障礙", "語言能力下降", "執行功能受損", "需要協助"
            ],
            "confidence_threshold": 0.7,
            "keywords": ["忘記", "迷路", "需要幫助", "無法", "困難"]
        },
        # M1 → M3 條件
        "M1_to_M3": {
            "triggers": [
                "妄想", "幻覺", "攻擊行為", "憂鬱", "焦慮", "激動",
                "懷疑", "看到", "聽到", "罵人", "推人", "打人"
            ],
            "confidence_threshold": 0.75,
            "keywords": ["懷疑", "看到", "聽到", "罵", "推", "打", "生氣"]
        },
        # M2 → M4 條件
        "M2_to_M4": {
            "triggers": [
                "需要照護指引", "詢問資源", "照護困難", "不知道怎麼辦",
                "尋求協助", "資源連結", "專業諮詢"
            ],
            "confidence_threshold": 0.65,
            "keywords": ["怎麼辦", "協助", "資源", "諮詢", "幫助"]
        },
        # M3 → M4 條件
        "M3_to_M4": {
            "triggers": [
                "照護策略", "處理方法", "專業協助", "資源需求",
                "照護技巧", "環境調整"
            ],
            "confidence_threshold": 0.6,
            "keywords": ["處理", "方法", "技巧", "策略", "環境"]
        }
    }
    
    def __init__(self):
        self.conversation_history = []
        self.current_module = ModuleType.M1
        self.user_context = {}
    
    def route_to_module(self, current_module: str, 
                       ai_analysis: dict,
                       user_input: str = "") -> Dict[str, Any]:
        """決定下一個模組"""
        
        # 更新對話歷史
        self.conversation_history.append({
            "module": current_module,
            "input": user_input,
            "analysis": ai_analysis,
            "timestamp": self._get_timestamp()
        })
        
        # 分析用戶意圖
        intent = self._analyze_user_intent(user_input, ai_analysis)
        
        # 決定下一個模組
        next_module = self._determine_next_module(current_module, intent, ai_analysis)
        
        # 生成路由建議
        routing_suggestion = {
            "current_module": current_module,
            "next_module": next_module,
            "confidence": intent.get("confidence", 0.0),
            "reasoning": intent.get("reasoning", ""),
            "suggested_actions": self._get_suggested_actions(next_module),
            "conversation_context": self._get_conversation_context()
        }
        
        return routing_suggestion
    
    def _analyze_user_intent(self, user_input: str, ai_analysis: dict) -> Dict[str, Any]:
        """分析用戶意圖"""
        intent = {
            "primary_intent": "information_seeking",
            "confidence": 0.5,
            "reasoning": "",
            "keywords": []
        }
        
        # 提取關鍵詞
        keywords = self._extract_keywords(user_input)
        intent["keywords"] = keywords
        
        # 分析意圖類型
        if any(word in user_input for word in ["怎麼辦", "如何", "怎麼處理"]):
            intent["primary_intent"] = "action_seeking"
            intent["confidence"] = 0.8
            intent["reasoning"] = "用戶尋求具體行動建議"
        elif any(word in user_input for word in ["資源", "協助", "諮詢"]):
            intent["primary_intent"] = "resource_seeking"
            intent["confidence"] = 0.7
            intent["reasoning"] = "用戶需要資源連結"
        elif any(word in user_input for word in ["階段", "程度", "嚴重"]):
            intent["primary_intent"] = "stage_assessment"
            intent["confidence"] = 0.6
            intent["reasoning"] = "用戶想了解病程階段"
        
        return intent
    
    def _determine_next_module(self, current_module: str, 
                             intent: dict, 
                             ai_analysis: dict) -> str:
        """決定下一個模組"""
        
        # 根據當前模組和意圖決定路由
        if current_module == ModuleType.M1:
            return self._route_from_m1(intent, ai_analysis)
        elif current_module == ModuleType.M2:
            return self._route_from_m2(intent, ai_analysis)
        elif current_module == ModuleType.M3:
            return self._route_from_m3(intent, ai_analysis)
        elif current_module == ModuleType.M4:
            return self._route_from_m4(intent, ai_analysis)
        else:
            return ModuleType.M1  # 預設回到 M1
    
    def _route_from_m1(self, intent: dict, ai_analysis: dict) -> str:
        """從 M1 路由到其他模組"""
        user_input = intent.get("keywords", [])
        
        # 檢查 M1 → M2 條件
        if self._check_routing_condition("M1_to_M2", user_input, ai_analysis):
            return ModuleType.M2
        
        # 檢查 M1 → M3 條件
        if self._check_routing_condition("M1_to_M3", user_input, ai_analysis):
            return ModuleType.M3
        
        # 預設繼續在 M1
        return ModuleType.M1
    
    def _route_from_m2(self, intent: dict, ai_analysis: dict) -> str:
        """從 M2 路由到其他模組"""
        user_input = intent.get("keywords", [])
        
        # 檢查 M2 → M4 條件
        if self._check_routing_condition("M2_to_M4", user_input, ai_analysis):
            return ModuleType.M4
        
        # 預設繼續在 M2
        return ModuleType.M2
    
    def _route_from_m3(self, intent: dict, ai_analysis: dict) -> str:
        """從 M3 路由到其他模組"""
        user_input = intent.get("keywords", [])
        
        # 檢查 M3 → M4 條件
        if self._check_routing_condition("M3_to_M4", user_input, ai_analysis):
            return ModuleType.M4
        
        # 預設繼續在 M3
        return ModuleType.M3
    
    def _route_from_m4(self, intent: dict, ai_analysis: dict) -> str:
        """從 M4 路由到其他模組"""
        # M4 通常是最終模組，但可以根據需要路由回其他模組
        if intent.get("primary_intent") == "stage_assessment":
            return ModuleType.M2
        elif intent.get("primary_intent") == "symptom_assessment":
            return ModuleType.M1
        
        return ModuleType.M4
    
    def _check_routing_condition(self, rule_name: str, 
                               user_input: List[str], 
                               ai_analysis: dict) -> bool:
        """檢查路由條件"""
        rule = self.ROUTING_RULES.get(rule_name, {})
        
        # 檢查關鍵詞匹配
        keywords = rule.get("keywords", [])
        if any(keyword in " ".join(user_input) for keyword in keywords):
            return True
        
        # 檢查 AI 分析結果
        confidence = ai_analysis.get("confidence", 0.0)
        threshold = rule.get("confidence_threshold", 0.5)
        
        if confidence >= threshold:
            return True
        
        return False
    
    def _extract_keywords(self, text: str) -> List[str]:
        """提取關鍵詞"""
        # 簡單的關鍵詞提取
        keywords = []
        common_words = [
            "忘記", "迷路", "懷疑", "看到", "聽到", "罵", "推", "打",
            "怎麼辦", "如何", "怎麼處理", "資源", "協助", "諮詢",
            "階段", "程度", "嚴重", "需要", "幫助", "困難"
        ]
        
        for word in common_words:
            if word in text:
                keywords.append(word)
        
        return keywords
    
    def _get_suggested_actions(self, module: str) -> List[str]:
        """獲取建議行動"""
        actions = {
            ModuleType.M1: [
                "查看十大警訊詳情",
                "進行認知功能評估",
                "諮詢專業醫師"
            ],
            ModuleType.M2: [
                "了解病程階段特徵",
                "查看階段性照護重點",
                "評估照護需求"
            ],
            ModuleType.M3: [
                "學習行為管理技巧",
                "了解症狀處理方法",
                "尋求專業協助"
            ],
            ModuleType.M4: [
                "查看照護資源",
                "聯繫專業服務",
                "學習照護技巧"
            ]
        }
        
        return actions.get(module, [])
    
    def _get_conversation_context(self) -> Dict[str, Any]:
        """獲取對話上下文"""
        if not self.conversation_history:
            return {}
        
        recent_history = self.conversation_history[-3:]  # 最近 3 輪對話
        
        return {
            "recent_modules": [h["module"] for h in recent_history],
            "conversation_length": len(self.conversation_history),
            "last_module": recent_history[-1]["module"] if recent_history else None
        }
    
    def _get_timestamp(self) -> str:
        """獲取時間戳"""
        from datetime import datetime
        return datetime.now().isoformat()
    
    def reset_conversation(self):
        """重置對話歷史"""
        self.conversation_history = []
        self.current_module = ModuleType.M1
        self.user_context = {}

# 使用範例
def example_usage():
    """路由系統使用範例"""
    router = ModuleRouter()
    
    # 模擬 AI 分析結果
    ai_analysis = {
        "confidence": 0.8,
        "matched_codes": ["M1-01"],
        "symptom_titles": ["記憶力減退影響日常生活"]
    }
    
    # 測試路由
    result = router.route_to_module(
        current_module="M1",
        ai_analysis=ai_analysis,
        user_input="媽媽常忘記關瓦斯，而且最近會懷疑有人偷東西"
    )
    
    print("路由結果:", result)
    return result

if __name__ == "__main__":
    example_usage() 