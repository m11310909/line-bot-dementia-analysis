import json
from typing import Dict, Any
from api.core.genai_client import genai_client

M1_PROMPT_TEMPLATE = """
你是專業的失智症評估助手。請分析以下症狀描述，對照台灣失智症協會十大警訊：

用戶描述："{user_input}"

請以JSON格式回應，包含：
1. 分析過程說明
2. 符合的警訊項目
3. 信心指數 (0-10)
4. 建議行動

十大警訊：
1. 記憶力減退影響日常生活
2. 計劃事情或解決問題有困難
3. 無法勝任原本熟悉的事務
4. 對時間地點感到混淆
5. 理解視覺影像和空間關係有困難
6. 言語表達或書寫出現困難
7. 東西擺放錯亂且失去回溯能力
8. 判斷力變差或減退
9. 從工作或社交活動中退出
10. 情緒和個性的改變
"""

M1_SCHEMA = {
    "type": "object",
    "properties": {
        "analysis_process": {
            "type": "string",
            "description": "分析思路說明"
        },
        "matched_warnings": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "warning_id": {"type": "integer"},
                    "warning_name": {"type": "string"},
                    "match_confidence": {"type": "number"}
                }
            }
        },
        "overall_confidence": {
            "type": "number",
            "minimum": 0,
            "maximum": 10
        },
        "risk_level": {
            "type": "string",
            "enum": ["low", "moderate", "high", "urgent"]
        },
        "recommendations": {
            "type": "array",
            "items": {"type": "string"}
        }
    },
    "required": ["analysis_process", "matched_warnings", "overall_confidence", "risk_level"]
}

async def analyze_symptoms(user_input: str) -> Dict[str, Any]:
    """Analyze user-described symptoms against dementia warning signs"""
    
    prompt = M1_PROMPT_TEMPLATE.format(user_input=user_input)
    
    try:
        result = await genai_client.generate_response(prompt, M1_SCHEMA)
        response_data = json.loads(result["content"])
        
        # Add metadata
        response_data["metadata"] = {
            "module_id": "M1",
            "provider": result["provider"],
            "tokens_used": result["tokens_used"]
        }
        
        return response_data
        
    except Exception as e:
        # Fallback response
        return {
            "analysis_process": "分析過程中發生錯誤，請稍後再試",
            "matched_warnings": [],
            "overall_confidence": 0,
            "risk_level": "low",
            "recommendations": ["建議諮詢專業醫療人員"],
            "error": str(e)
        }
