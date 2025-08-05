"""
🎨 增強版 M1 API 整合
整合新的 Flex Message 設計與現有的 LINE Bot 系統
"""

import json
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime
from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
import uvicorn

from enhanced_m1_flex_generator import EnhancedM1FlexGenerator

# 配置日誌
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 初始化 FastAPI 應用
app = FastAPI(
    title="Enhanced M1 API",
    description="增強版 M1 警訊分析 API",
    version="1.0.0"
)

# 初始化 Flex Message 生成器
flex_generator = EnhancedM1FlexGenerator()

class UserInput(BaseModel):
    """用戶輸入模型"""
    user_input: str
    user_id: Optional[str] = None
    context: Optional[Dict[str, Any]] = None

class AnalysisResponse(BaseModel):
    """分析回應模型"""
    success: bool
    flex_message: Dict[str, Any]
    analysis_data: Dict[str, Any]
    original_text: str
    timestamp: str

@app.get("/")
async def root():
    """根端點"""
    return {
        "message": "Enhanced M1 API",
        "version": "1.0.0",
        "status": "running"
    }

@app.get("/health")
async def health_check():
    """健康檢查端點"""
    stats = flex_generator.get_stats()
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "stats": stats
    }

@app.post("/analyze", response_model=AnalysisResponse)
async def analyze_m1_warning_signs(user_input: UserInput):
    """
    分析 M1 警訊並生成增強版 Flex Message
    """
    try:
        logger.info(f"收到分析請求：{user_input.user_input[:50]}...")
        
        # 模擬 M1 分析結果（實際應用中會調用真實的分析服務）
        analysis_result = await _simulate_m1_analysis(user_input.user_input)
        
        # 生成增強版 Flex Message
        flex_message = flex_generator.create_enhanced_m1_flex_message(
            analysis_result, 
            user_input.user_input
        )
        
        # 構建回應
        response = AnalysisResponse(
            success=True,
            flex_message=flex_message,
            analysis_data=analysis_result,
            original_text=user_input.user_input,
            timestamp=datetime.now().isoformat()
        )
        
        logger.info(f"分析完成，生成 Flex Message 成功")
        return response
        
    except Exception as e:
        logger.error(f"分析失敗：{e}")
        raise HTTPException(status_code=500, detail=f"分析失敗：{str(e)}")

async def _simulate_m1_analysis(user_input: str) -> Dict[str, Any]:
    """
    模擬 M1 分析結果
    實際應用中會調用真實的 M1 分析服務
    """
    
    # 根據輸入內容模擬檢測結果
    detected_signs = []
    confidence_score = 0.85
    
    # 簡單的關鍵字檢測邏輯
    if any(keyword in user_input for keyword in ["重複", "同樣", "忘記"]):
        detected_signs.append("重複發問行為")
        confidence_score = 0.90
    
    if any(keyword in user_input for keyword in ["瓦斯", "爐", "火", "安全"]):
        detected_signs.append("安全意識下降")
        confidence_score = 0.95
    
    if any(keyword in user_input for keyword in ["記憶", "忘記", "記不住"]):
        detected_signs.append("記憶力減退")
        confidence_score = 0.88
    
    if any(keyword in user_input for keyword in ["語言", "表達", "說話"]):
        detected_signs.append("語言表達困難")
        confidence_score = 0.82
    
    # 生成回應文字
    if detected_signs:
        if len(detected_signs) >= 3:
            reply = "檢測到多個失智症警訊，建議及早就醫評估。"
        elif len(detected_signs) >= 2:
            reply = "檢測到多個警訊，建議密切觀察並考慮專業評估。"
        else:
            reply = "檢測到個別警訊，建議進一步觀察。"
    else:
        reply = "根據您的描述，目前未檢測到明顯的失智症警訊。"
    
    return {
        "detected_signs": detected_signs,
        "xai_data": {
            "confidence_score": confidence_score,
            "analysis_method": "keyword_based",
            "features_used": ["repetition", "safety", "memory", "language"]
        },
        "chatbot_reply": reply,
        "risk_assessment": {
            "level": "high" if len(detected_signs) >= 3 else "medium" if detected_signs else "low",
            "factors": detected_signs
        }
    }

@app.post("/webhook")
async def line_webhook(request: Request):
    """
    LINE Bot Webhook 端點
    處理 LINE Bot 的訊息並回傳增強版 Flex Message
    """
    try:
        body = await request.body()
        events = json.loads(body.decode('utf-8')).get('events', [])
        
        responses = []
        
        for event in events:
            if event['type'] == 'message' and event['message']['type'] == 'text':
                user_message = event['message']['text']
                user_id = event['source']['userId']
                
                logger.info(f"收到 LINE 訊息：{user_message}")
                
                # 分析訊息
                analysis_result = await _simulate_m1_analysis(user_message)
                
                # 生成 Flex Message
                flex_message = flex_generator.create_enhanced_m1_flex_message(
                    analysis_result,
                    user_message
                )
                
                responses.append({
                    "reply_token": event['replyToken'],
                    "flex_message": flex_message
                })
        
        return {
            "status": "success",
            "responses": responses,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Webhook 處理失敗：{e}")
        raise HTTPException(status_code=500, detail=f"Webhook 處理失敗：{str(e)}")

@app.get("/stats")
async def get_stats():
    """取得生成統計"""
    return {
        "generator_stats": flex_generator.get_stats(),
        "api_stats": {
            "total_requests": 0,  # 可以加入請求計數
            "uptime": datetime.now().isoformat()
        }
    }

# ===== 測試端點 =====

@app.post("/test")
async def test_flex_message():
    """測試 Flex Message 生成"""
    
    test_cases = [
        {
            "input": "媽媽最近常重複問同樣的問題",
            "expected_signs": ["重複發問行為", "記憶力減退"]
        },
        {
            "input": "爸爸忘記關瓦斯爐",
            "expected_signs": ["安全意識下降", "記憶力減退"]
        },
        {
            "input": "爺爺偶爾忘記鑰匙放哪裡",
            "expected_signs": []
        }
    ]
    
    results = []
    
    for test_case in test_cases:
        try:
            analysis_result = await _simulate_m1_analysis(test_case["input"])
            flex_message = flex_generator.create_enhanced_m1_flex_message(
                analysis_result,
                test_case["input"]
            )
            
            results.append({
                "input": test_case["input"],
                "success": True,
                "detected_signs": analysis_result["detected_signs"],
                "flex_message_size": len(json.dumps(flex_message, ensure_ascii=False))
            })
            
        except Exception as e:
            results.append({
                "input": test_case["input"],
                "success": False,
                "error": str(e)
            })
    
    return {
        "test_results": results,
        "generator_stats": flex_generator.get_stats()
    }

if __name__ == "__main__":
    print("🚀 啟動增強版 M1 API 服務...")
    print("📍 服務地址：http://localhost:8002")
    print("📋 API 文檔：http://localhost:8002/docs")
    print("🔍 健康檢查：http://localhost:8002/health")
    print("🧪 測試端點：http://localhost:8002/test")
    
    uvicorn.run(
        "enhanced_m1_api:app",
        host="0.0.0.0",
        port=8002,
        reload=True,
        log_level="info"
    ) 