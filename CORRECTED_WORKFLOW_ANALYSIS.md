# 🔄 **修正工作流程分析：失智小幫手核心處理流程**

## 📋 **正確的工作流程圖**

```
📱 用戶發送訊息到 LINE Bot
    ↓
🔗 Webhook 接收並驗證訊息
    ↓
🤖 失智小幫手 (Dementia Assistant) 核心分析
    ↓
🧠 基於失智小幫手回答的後續處理
    ↓
📊 XAI 引擎分析失智小幫手的回答
    ↓
📋 生成結構化的分析結果
    ↓
🎨 創建豐富的 Flex Message
    ↓
📤 發送回應給用戶
```

---

## 🔍 **詳細流程分析**

### **📱 步驟 1: 用戶發送訊息到 LINE Bot**
```python
# 用戶在 LINE 中發送訊息
user_message = "我媽媽最近常常忘記剛吃過飯，還會重複問同樣的問題"
```

**處理機制**:
- LINE Bot 接收用戶訊息
- 提取用戶 ID、訊息內容、時間戳
- 進行初步的訊息格式驗證

### **🔗 步驟 2: Webhook 接收並驗證訊息**
```python
@app.post("/webhook")
async def webhook(request: Request):
    # 獲取 LINE 簽名
    signature = request.headers.get('X-Line-Signature', '')
    
    # 驗證簽名
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        raise HTTPException(status_code=400, detail="Invalid signature")
```

**安全機制**:
- **簽名驗證**: 確保訊息來自 LINE 官方
- **時間戳檢查**: 防止重放攻擊
- **用戶身份驗證**: 驗證用戶權限

### **🤖 步驟 3: 失智小幫手核心分析**
```python
async def call_dementia_assistant(user_message: str) -> Dict[str, Any]:
    """調用失智小幫手進行核心分析"""
    
    dementia_prompt = f"""
你是一個專業的失智症照護助手「失智小幫手」。
請分析以下用戶描述，並提供：

1. 失智症警訊分析
2. 專業建議
3. 關懷提醒
4. 後續行動建議
5. 嚴重程度評估
6. 建議就醫時機

用戶描述：{user_message}

請用繁體中文回答，並提供結構化的分析結果。
"""
    
    # 調用失智小幫手 API
    response = requests.post(
        "https://api.dementia-assistant.com/analyze",
        json={
            "prompt": dementia_prompt,
            "user_id": user_id,
            "timestamp": datetime.now().isoformat()
        },
        timeout=30
    )
    
    return response.json()
```

**失智小幫手分析內容**:
- **警訊識別**: 分析記憶力減退、語言困難等症狀
- **嚴重程度評估**: 判斷症狀的嚴重程度
- **專業建議生成**: 提供具體的照護建議
- **關懷提醒**: 提供心理支持建議
- **就醫建議**: 明確的就醫時機和建議

### **🧠 步驟 4: 基於失智小幫手回答的後續處理**
```python
async def process_dementia_assistant_response(assistant_response: Dict) -> Dict[str, Any]:
    """基於失智小幫手回答進行後續處理"""
    
    # 提取失智小幫手的回答
    dementia_analysis = assistant_response.get("analysis", "")
    recommendations = assistant_response.get("recommendations", [])
    warnings = assistant_response.get("warnings", [])
    severity = assistant_response.get("severity", "unknown")
    
    # 步驟 4.1: 模組選擇 (基於失智小幫手的分析)
    selected_module = select_module_based_on_assistant_response(dementia_analysis)
    
    # 步驟 4.2: BoN-MAV 驗證 (驗證失智小幫手的回答)
    bon_mav_result = await validate_assistant_response_with_bon_mav(dementia_analysis)
    
    # 步驟 4.3: SHAP 特徵分析 (分析失智小幫手回答的特徵)
    shap_result = analyze_assistant_response_features(dementia_analysis)
    
    # 步驟 4.4: LIME 局部解釋 (解釋失智小幫手的推理過程)
    lime_result = explain_assistant_reasoning(dementia_analysis)
    
    return {
        "original_assistant_response": assistant_response,
        "selected_module": selected_module,
        "bon_mav_validation": bon_mav_result,
        "shap_analysis": shap_result,
        "lime_explanation": lime_result
    }

def select_module_based_on_assistant_response(analysis: str) -> str:
    """基於失智小幫手的分析選擇最適合的模組"""
    
    # 根據失智小幫手的分析內容選擇模組
    if any(keyword in analysis for keyword in ["警訊", "徵兆", "初期", "記憶"]):
        return "M1"  # 警訊徵兆分析
    elif any(keyword in analysis for keyword in ["進展", "階段", "中期", "晚期"]):
        return "M2"  # 病程進展評估
    elif any(keyword in analysis for keyword in ["行為", "心理", "激動", "憂鬱"]):
        return "M3"  # 行為心理症狀分析
    elif any(keyword in analysis for keyword in ["照護", "資源", "醫生", "醫院"]):
        return "M4"  # 照護資源導航
    else:
        return "M1"  # 預設使用 M1 模組
```

### **📊 步驟 5: XAI 引擎分析失智小幫手的回答**
```python
async def validate_assistant_response_with_bon_mav(assistant_response: str) -> Dict[str, Any]:
    """使用 BoN-MAV 驗證失智小幫手的回答"""
    
    # 生成多個候選答案進行比較
    candidates = [
        assistant_response,  # 失智小幫手的原始回答
        await generate_alternative_response(assistant_response, "gemini"),
        await generate_alternative_response(assistant_response, "openai"),
        await generate_alternative_response(assistant_response, "third_party")
    ]
    
    # 對每個候選答案進行多面向驗證
    verified_candidates = []
    for candidate in candidates:
        verification = await verify_aspects(candidate)
        verified_candidates.append({
            "answer": candidate,
            "verification": verification,
            "overall_score": calculate_comprehensive_score(candidate, verification)
        })
    
    # 選擇最佳答案
    best_candidate = max(verified_candidates, key=lambda x: x["overall_score"])
    
    return {
        "best_answer": best_candidate["answer"],
        "verification_results": best_candidate["verification"],
        "overall_score": best_candidate["overall_score"],
        "is_original_best": best_candidate["answer"] == assistant_response
    }

def analyze_assistant_response_features(assistant_response: str) -> Dict[str, Any]:
    """使用 SHAP 分析失智小幫手回答的特徵重要度"""
    
    # 特徵提取
    features = extract_features_from_response(assistant_response)
    
    # SHAP 分析
    shap_values = shap_analyzer.analyze_feature_importance(assistant_response)
    
    return {
        "feature_importance": shap_values["feature_importance"],
        "key_phrases": extract_key_phrases(assistant_response),
        "medical_terms": extract_medical_terms(assistant_response),
        "safety_indicators": extract_safety_indicators(assistant_response)
    }

def explain_assistant_reasoning(assistant_response: str) -> Dict[str, Any]:
    """使用 LIME 解釋失智小幫手的推理過程"""
    
    # LIME 局部解釋
    lime_result = lime_analyzer.analyze_local_importance(assistant_response, model)
    
    return {
        "reasoning_path": extract_reasoning_path(assistant_response),
        "confidence_factors": extract_confidence_factors(assistant_response),
        "evidence_highlight": highlight_evidence(assistant_response),
        "lime_explanation": lime_result
    }
```

### **📋 步驟 6: 生成結構化的分析結果**
```python
def generate_structured_analysis(assistant_response: Dict, xai_results: Dict) -> Dict[str, Any]:
    """整合失智小幫手回答和 XAI 分析結果"""
    
    return {
        # 失智小幫手的原始分析
        "dementia_assistant_analysis": {
            "summary": assistant_response.get("summary", ""),
            "warnings": assistant_response.get("warnings", []),
            "recommendations": assistant_response.get("recommendations", []),
            "severity": assistant_response.get("severity", "unknown"),
            "next_actions": assistant_response.get("next_actions", [])
        },
        
        # XAI 驗證和分析
        "xai_validation": {
            "bon_mav_result": xai_results.get("bon_mav_validation", {}),
            "shap_analysis": xai_results.get("shap_analysis", {}),
            "lime_explanation": xai_results.get("lime_explanation", {}),
            "selected_module": xai_results.get("selected_module", "M1")
        },
        
        # 綜合評估
        "comprehensive_assessment": {
            "confidence_score": calculate_confidence_score(assistant_response, xai_results),
            "reliability_indicator": assess_reliability(assistant_response, xai_results),
            "medical_accuracy": assess_medical_accuracy(assistant_response),
            "safety_level": assess_safety_level(assistant_response)
        },
        
        # 元數據
        "metadata": {
            "timestamp": datetime.now().isoformat(),
            "processing_time": calculate_processing_time(),
            "ai_engines_used": ["dementia_assistant", "bon_mav", "shap", "lime"]
        }
    }
```

### **🎨 步驟 7: 創建豐富的 Flex Message**
```python
def create_comprehensive_flex_message(structured_result: Dict) -> Dict:
    """基於失智小幫手回答創建 Flex Message"""
    
    dementia_analysis = structured_result["dementia_assistant_analysis"]
    xai_validation = structured_result["xai_validation"]
    
    return {
        "type": "carousel",
        "contents": [
            # 頁面 1: 失智小幫手核心分析
            create_dementia_assistant_card(dementia_analysis),
            
            # 頁面 2: XAI 驗證結果
            create_xai_validation_card(xai_validation),
            
            # 頁面 3: 綜合評估
            create_comprehensive_assessment_card(structured_result["comprehensive_assessment"])
        ]
    }

def create_dementia_assistant_card(dementia_analysis: Dict) -> Dict:
    """創建失智小幫手分析卡片"""
    return {
        "type": "bubble",
        "header": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "text",
                    "text": "🧠 失智小幫手專業分析",
                    "weight": "bold",
                    "color": "#ffffff"
                }
            ],
            "backgroundColor": "#FF6B6B"
        },
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                # 分析摘要
                {
                    "type": "text",
                    "text": "📋 分析摘要",
                    "weight": "bold",
                    "size": "md"
                },
                {
                    "type": "text",
                    "text": dementia_analysis["summary"],
                    "wrap": True,
                    "margin": "sm"
                },
                
                # 警訊列表
                create_warning_section(dementia_analysis["warnings"]),
                
                # 建議列表
                create_recommendation_section(dementia_analysis["recommendations"]),
                
                # 嚴重程度
                {
                    "type": "text",
                    "text": f"⚠️ 嚴重程度: {dementia_analysis['severity']}",
                    "size": "sm",
                    "margin": "sm"
                }
            ]
        }
    }

def create_xai_validation_card(xai_validation: Dict) -> Dict:
    """創建 XAI 驗證卡片"""
    return {
        "type": "bubble",
        "header": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "text",
                    "text": "🔍 AI 驗證結果",
                    "weight": "bold",
                    "color": "#ffffff"
                }
            ],
            "backgroundColor": "#4ECDC4"
        },
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                # BoN-MAV 驗證
                {
                    "type": "text",
                    "text": "🏆 多引擎驗證",
                    "weight": "bold",
                    "size": "sm"
                },
                {
                    "type": "text",
                    "text": f"可信度: {xai_validation['bon_mav_result'].get('overall_score', 0):.1%}",
                    "size": "sm"
                },
                
                # SHAP 特徵分析
                {
                    "type": "text",
                    "text": "📊 特徵重要度",
                    "weight": "bold",
                    "size": "sm",
                    "margin": "sm"
                },
                create_feature_importance_chart(xai_validation["shap_analysis"]),
                
                # LIME 解釋
                {
                    "type": "text",
                    "text": "🎯 推理解釋",
                    "weight": "bold",
                    "size": "sm",
                    "margin": "sm"
                },
                create_reasoning_explanation(xai_validation["lime_explanation"])
            ]
        }
    }
```

### **📤 步驟 8: 發送回應給用戶**
```python
async def send_line_message_with_retry(reply_token: str, flex_message: Dict) -> bool:
    """發送 LINE 訊息並處理重試"""
    
    max_retries = 3
    for attempt in range(max_retries):
        try:
            # 發送 Flex Message
            line_bot_api.reply_message(
                reply_token,
                FlexSendMessage(
                    alt_text="失智小幫手專業分析結果",
                    contents=flex_message["contents"]
                )
            )
            return True
            
        except Exception as e:
            logger.error(f"發送訊息失敗 (嘗試 {attempt + 1}/{max_retries}): {e}")
            if attempt < max_retries - 1:
                await asyncio.sleep(1)  # 等待 1 秒後重試
    
    return False
```

---

## 🔧 **完整整合工作流程**

### **📱 主工作流程**
```python
async def main_workflow(user_input: str, user_id: str) -> Dict[str, Any]:
    """完整的工作流程"""
    
    # 步驟 1-2: Webhook 處理 (已在上層完成)
    
    # 步驟 3: 失智小幫手核心分析
    assistant_response = await call_dementia_assistant(user_input)
    
    # 步驟 4: 基於失智小幫手回答的後續處理
    xai_results = await process_dementia_assistant_response(assistant_response)
    
    # 步驟 5: XAI 引擎分析 (已在步驟 4 中完成)
    
    # 步驟 6: 生成結構化的分析結果
    structured_result = generate_structured_analysis(assistant_response, xai_results)
    
    # 步驟 7: 創建豐富的 Flex Message
    flex_message = create_comprehensive_flex_message(structured_result)
    
    # 步驟 8: 發送回應 (由上層處理)
    
    return {
        "assistant_response": assistant_response,
        "xai_results": xai_results,
        "structured_result": structured_result,
        "flex_message": flex_message
    }
```

---

## 📊 **失智小幫手的核心地位**

### **🤖 失智小幫手的作用**
1. **核心分析引擎**: 提供專業的失智症分析
2. **統一回答標準**: 確保回答的一致性和專業性
3. **多面向評估**: 涵蓋警訊、建議、關懷、行動等各個方面
4. **可信度基礎**: 為後續的 XAI 驗證提供基準

### **🔄 後續處理的依賴關係**
- **BoN-MAV**: 驗證失智小幫手回答的可信度
- **SHAP**: 分析失智小幫手回答的特徵重要度
- **LIME**: 解釋失智小幫手的推理過程
- **模組選擇**: 基於失智小幫手的分析選擇視覺化模組

### **📈 效能優勢**
- **專業性**: 失智小幫手提供醫學專業的分析
- **一致性**: 統一的回答標準和格式
- **可驗證性**: 後續的 XAI 分析可以驗證和解釋
- **用戶信任**: 明確的專業身份和可信度

---

*這個修正的工作流程明確了失智小幫手在整個系統中的核心地位，所有後續的處理都基於失智小幫手的專業分析，確保了系統的專業性、一致性和可信度。* 