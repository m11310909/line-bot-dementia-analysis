"""
XAI Flex Message API 端點實作
整合 RAG 檢索結果與 Flex Message 視覺化
"""

from fastapi import FastAPI, HTTPException, Depends, BackgroundTasks
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional, Union
from enum import Enum
import asyncio
import logging
from datetime import datetime
import json

# 匯入我們的 XAI 組件
from xai_flex_generator import XAIFlexGenerator, ComponentType
from retrieval_engine import MultiLevelRetrieval  # 假設你已有的檢索引擎
from explanation_engine import ExplanationEngine

# 設定日誌
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="失智照護 XAI Flex Message API",
    description="提供可解釋性視覺化的失智症與長照資訊檢索服務",
    version="1.0.0"
)

# === Request/Response Models ===

class AnalyzeRequest(BaseModel):
    """分析請求模型"""
    query: str = Field(..., description="使用者查詢", min_length=1, max_length=500)
    module: Optional[str] = Field("hybrid", description="指定模組：dementia, ltc, hybrid")
    language: str = Field("zh-TW", description="語言：zh-TW, zh-CN, en")
    max_chunks: int = Field(5, description="最大返回 chunk 數量", ge=1, le=10)
    include_explanation: bool = Field(True, description="是否包含 XAI 解釋")
    user_context: Optional[Dict[str, Any]] = Field(None, description="使用者上下文")

class FlexMessageRequest(BaseModel):
    """Flex Message 生成請求"""
    chunk_ids: List[str] = Field(..., description="Chunk ID 列表", min_items=1, max_items=10)
    component_preference: Optional[str] = Field(None, description="偏好的組件類型")
    interaction_mode: str = Field("basic", description="互動模式：basic, advanced")
    accessibility_mode: bool = Field(False, description="無障礙模式")
    user_context: Optional[Dict[str, Any]] = Field(None, description="使用者上下文")

class ChunkData(BaseModel):
    """Chunk 資料模型"""
    chunk_id: str
    module_id: str
    chunk_type: str
    title: str
    content: str
    summary: Optional[str] = None
    keywords: List[str] = []
    tags: List[str] = []
    confidence_score: float = Field(ge=0.0, le=1.0)
    difficulty_level: str = "basic"
    explanation_data: Dict[str, Any] = {}
    source_trace: Dict[str, Any] = {}
    visual_config: Dict[str, Any] = {}

class AnalyzeResponse(BaseModel):
    """分析響應模型"""
    chunks: List[ChunkData]
    total_found: int
    query_analysis: Dict[str, Any]
    processing_time: float
    explanation_summary: Optional[Dict[str, Any]] = None
    suggestions: List[str] = []

class FlexMessageResponse(BaseModel):
    """Flex Message 響應模型"""
    flex_message: Dict[str, Any]
    fallback_text: str
    interaction_handlers: List[Dict[str, Any]] = []
    metadata: Dict[str, Any] = {}
    accessibility_enhanced: bool = False

class ExplanationResponse(BaseModel):
    """解釋詳情響應模型"""
    chunk_id: str
    reasoning_chain: List[Dict[str, Any]]
    confidence_breakdown: Dict[str, Any]
    evidence_sources: List[Dict[str, Any]]
    related_concepts: List[str]
    interpretation_notes: List[str]
    generated_at: datetime

class HealthCheckResponse(BaseModel):
    """健康檢查響應"""
    status: str
    timestamp: datetime
    version: str
    services: Dict[str, str]

# === Dependencies ===

async def get_retrieval_engine():
    """取得檢索引擎實例"""
    if not hasattr(app.state, 'retrieval_engine'):
        app.state.retrieval_engine = MultiLevelRetrieval()
    return app.state.retrieval_engine

async def get_flex_generator():
    """取得 Flex Message 生成器實例"""
    if not hasattr(app.state, 'flex_generator'):
        app.state.flex_generator = XAIFlexGenerator()
    return app.state.flex_generator

async def get_explanation_engine():
    """取得解釋引擎實例"""
    if not hasattr(app.state, 'explanation_engine'):
        app.state.explanation_engine = ExplanationEngine()
    return app.state.explanation_engine

# === Core API Endpoints ===

@app.post("/api/v1/analyze/{module}", response_model=AnalyzeResponse)
async def analyze_query(
    module: str,
    request: AnalyzeRequest,
    retrieval_engine = Depends(get_retrieval_engine),
    explanation_engine = Depends(get_explanation_engine)
):
    """
    分析使用者查詢並返回相關的失智照護資訊

    Args:
        module: 模組名稱 (dementia, ltc, hybrid)
        request: 分析請求參數

    Returns:
        包含 chunks 和解釋的分析結果
    """
    start_time = datetime.now()

    try:
        # 驗證模組參數
        valid_modules = ["dementia", "ltc", "hybrid"]
        if module not in valid_modules:
            raise HTTPException(
                status_code=400, 
                detail=f"無效的模組名稱。支援的模組：{', '.join(valid_modules)}"
            )

        logger.info(f"開始分析查詢：{request.query} (模組：{module})")

        # 執行多層級檢索
        retrieval_results = await retrieval_engine.retrieve(
            query=request.query,
            module_filter=module if module != "hybrid" else None,
            max_results=request.max_chunks,
            language=request.language
        )

        # 轉換為 ChunkData 格式
        chunks = []
        for result in retrieval_results['chunks']:
            chunk_data = ChunkData(
                chunk_id=result.get('chunk_id', ''),
                module_id=result.get('module_id', ''),
                chunk_type=result.get('chunk_type', ''),
                title=result.get('title', ''),
                content=result.get('content', ''),
                summary=result.get('summary'),
                keywords=result.get('keywords', []),
                tags=result.get('tags', []),
                confidence_score=result.get('confidence_score', 0.8),
                difficulty_level=result.get('difficulty_level', 'basic'),
                explanation_data=result.get('explanation_data', {}),
                source_trace=result.get('source_trace', {}),
                visual_config=result.get('visual_config', {})
            )
            chunks.append(chunk_data)

        # 生成解釋摘要
        explanation_summary = None
        if request.include_explanation and chunks:
            explanations = explanation_engine.generate_explanations(
                [chunk.dict() for chunk in chunks], 
                request.user_context
            )
            explanation_summary = {
                'total_explanations': len(explanations),
                'average_confidence': sum(chunk.confidence_score for chunk in chunks) / len(chunks),
                'primary_concepts': _extract_primary_concepts(explanations),
                'reasoning_complexity': _assess_reasoning_complexity(explanations)
            }

        # 生成查詢建議
        suggestions = _generate_query_suggestions(request.query, chunks)

        # 計算處理時間
        processing_time = (datetime.now() - start_time).total_seconds()

        return AnalyzeResponse(
            chunks=chunks,
            total_found=len(chunks),
            query_analysis={
                'original_query': request.query,
                'detected_intent': retrieval_results.get('intent', 'information_seeking'),
                'extracted_entities': retrieval_results.get('entities', []),
                'suggested_modules': retrieval_results.get('suggested_modules', []),
                'complexity_score': _calculate_query_complexity(request.query)
            },
            processing_time=processing_time,
            explanation_summary=explanation_summary,
            suggestions=suggestions
        )

    except Exception as e:
        logger.error(f"分析查詢時發生錯誤：{str(e)}")
        raise HTTPException(status_code=500, detail=f"分析失敗：{str(e)}")

@app.post("/api/v1/flex-message", response_model=FlexMessageResponse)
async def generate_flex_message(
    request: FlexMessageRequest,
    flex_generator = Depends(get_flex_generator),
    retrieval_engine = Depends(get_retrieval_engine)
):
    """
    根據 chunk IDs 生成 Flex Message 視覺化內容

    Args:
        request: Flex Message 生成請求

    Returns:
        包含 Flex Message JSON 和相關資料的響應
    """
    try:
        logger.info(f"生成 Flex Message，chunk_ids：{request.chunk_ids}")

        # 根據 chunk_ids 取得完整的 chunk 資料
        chunks_data = []
        for chunk_id in request.chunk_ids:
            chunk = await _get_chunk_by_id(chunk_id, retrieval_engine)
            if chunk:
                chunks_data.append(chunk)
            else:
                logger.warning(f"找不到 chunk_id：{chunk_id}")

        if not chunks_data:
            raise HTTPException(
                status_code=404, 
                detail="找不到指定的 chunk 資料"
            )

        # 生成 Flex Message
        flex_result = flex_generator.generate_enhanced_flex_message(
            chunks_data, 
            request.user_context
        )

        # 無障礙增強
        if request.accessibility_mode:
            flex_result = flex_generator.accessibility_enhancer.enhance_accessibility(
                flex_result
            )

        # 生成 fallback 文字
        fallback_text = _generate_fallback_text(chunks_data)

        # 生成互動處理器
        interaction_handlers = _create_interaction_handlers(
            chunks_data, 
            request.interaction_mode
        )

        return FlexMessageResponse(
            flex_message=flex_result,
            fallback_text=fallback_text,
            interaction_handlers=interaction_handlers,
            metadata={
                'chunk_count': len(chunks_data),
                'component_types': _identify_component_types(chunks_data),
                'generated_at': datetime.now().isoformat(),
                'accessibility_enhanced': request.accessibility_mode
            },
            accessibility_enhanced=request.accessibility_mode
        )

    except Exception as e:
        logger.error(f"生成 Flex Message 時發生錯誤：{str(e)}")
        raise HTTPException(status_code=500, detail=f"生成失敗：{str(e)}")

@app.get("/api/v1/explanation/{chunk_id}", response_model=ExplanationResponse)
async def get_explanation_details(
    chunk_id: str,
    explanation_engine = Depends(get_explanation_engine),
    retrieval_engine = Depends(get_retrieval_engine)
):
    """
    取得特定 chunk 的詳細解釋資訊

    Args:
        chunk_id: Chunk 識別碼

    Returns:
        詳細的解釋資訊
    """
    try:
        logger.info(f"取得解釋詳情，chunk_id：{chunk_id}")

        # 取得 chunk 資料
        chunk = await _get_chunk_by_id(chunk_id, retrieval_engine)
        if not chunk:
            raise HTTPException(
                status_code=404, 
                detail=f"找不到 chunk_id：{chunk_id}"
            )

        # 生成詳細解釋
        explanations = explanation_engine.generate_explanations([chunk])
        if not explanations:
            raise HTTPException(
                status_code=500, 
                detail="無法生成解釋資訊"
            )

        explanation = explanations[0]

        return ExplanationResponse(
            chunk_id=chunk_id,
            reasoning_chain=explanation['reasoning_chain'],
            confidence_breakdown=explanation['confidence_breakdown'],
            evidence_sources=explanation['evidence_sources'],
            related_concepts=explanation['related_concepts'],
            interpretation_notes=explanation['interpretation_notes'],
            generated_at=datetime.now()
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"取得解釋詳情時發生錯誤：{str(e)}")
        raise HTTPException(status_code=500, detail=f"取得解釋失敗：{str(e)}")

# === Management Endpoints ===

@app.get("/api/v1/health", response_model=HealthCheckResponse)
async def health_check():
    """系統健康檢查"""
    try:
        # 檢查各個服務的狀態
        services_status = {
            'retrieval_engine': 'healthy',
            'flex_generator': 'healthy', 
            'explanation_engine': 'healthy',
            'vector_index': 'healthy'
        }

        # 可以添加實際的健康檢查邏輯
        # 例如：檢查向量索引是否可用、資料庫連線等

        return HealthCheckResponse(
            status='healthy',
            timestamp=datetime.now(),
            version='1.0.0',
            services=services_status
        )

    except Exception as e:
        logger.error(f"健康檢查失敗：{str(e)}")
        return HealthCheckResponse(
            status='unhealthy',
            timestamp=datetime.now(),
            version='1.0.0',
            services={'error': str(e)}
        )

@app.post("/api/v1/admin/data-refresh")
async def refresh_data(background_tasks: BackgroundTasks):
    """重新整理資料索引"""
    try:
        logger.info("開始重新整理資料索引")

        # 在背景執行資料重新整理
        background_tasks.add_task(_refresh_data_indexes)

        return {
            'status': 'started',
            'message': '資料重新整理已在背景啟動',
            'timestamp': datetime.now()
        }

    except Exception as e:
        logger.error(f"啟動資料重新整理失敗：{str(e)}")
        raise HTTPException(status_code=500, detail=f"重新整理失敗：{str(e)}")

@app.get("/api/v1/metrics/usage")
async def get_usage_metrics():
    """取得使用統計資料"""
    try:
        # 這裡應該從實際的監控系統取得資料
        # 暫時返回模擬資料

        return {
            'total_queries': 1250,
            'avg_response_time': 0.85,
            'popular_modules': {
                'dementia': 580,
                'ltc': 420,
                'hybrid': 250
            },
            'top_query_types': [
                {'type': 'warning_signs', 'count': 320},
                {'type': 'coping_strategies', 'count': 280},
                {'type': 'ltc_services', 'count': 190}
            ],
            'flex_message_usage': {
                'total_generated': 890,
                'component_distribution': {
                    'comparison_card': 340,
                    'confidence_meter': 220,
                    'xai_box': 180,
                    'info_box': 150
                }
            },
            'timestamp': datetime.now()
        }

    except Exception as e:
        logger.error(f"取得使用統計失敗：{str(e)}")
        raise HTTPException(status_code=500, detail=f"取得統計失敗：{str(e)}")

@app.post("/api/v1/feedback")
async def submit_feedback(
    chunk_id: str,
    rating: int = Field(..., ge=1, le=5),
    feedback_type: str = Field(...),
    comment: Optional[str] = None
):
    """提交使用者回饋"""
    try:
        logger.info(f"收到回饋：chunk_id={chunk_id}, rating={rating}")

        # 儲存回饋資料
        feedback_data = {
            'chunk_id': chunk_id,
            'rating': rating,
            'feedback_type': feedback_type,
            'comment': comment,
            'timestamp': datetime.now(),
            'processed': False
        }

        # 這裡應該儲存到實際的資料庫
        # await save_feedback(feedback_data)

        return {
            'status': 'success',
            'message': '感謝您的回饋',
            'feedback_id': f"fb_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        }

    except Exception as e:
        logger.error(f"處理回饋失敗：{str(e)}")
        raise HTTPException(status_code=500, detail=f"回饋處理失敗：{str(e)}")

# === Helper Functions ===

async def _get_chunk_by_id(chunk_id: str, retrieval_engine) -> Optional[Dict[str, Any]]:
    """根據 chunk_id 取得完整的 chunk 資料"""
    try:
        # 這裡應該實作實際的資料查詢邏輯
        # 暫時返回模擬資料

        # 模擬資料庫查詢
        mock_chunk = {
            "chunk_id": chunk_id,
            "module_id": "M1",
            "chunk_type": "warning_sign",
            "title": "對時間地點感到混淆",
            "content": "失智症患者會搞不清楚年月日、季節變化，或迷失在熟悉的地方。",
            "summary": "時間空間認知障礙是失智症早期重要警訊",
            "keywords": ["記憶混淆", "時間障礙", "空間迷失"],
            "tags": ["十大警訊", "早期症狀"],
            "confidence_score": 0.92,
            "difficulty_level": "basic",
            "explanation_data": {
                "reasoning": "基於台灣失智症協會官方指引",
                "evidence_strength": "high"
            },
            "source_trace": {
                "source": "台灣失智症協會",
                "authority_level": "official"
            }
        }

        return mock_chunk if chunk_id == "M1-04" else None

    except Exception as e:
        logger.error(f"取得 chunk 資料失敗：{str(e)}")
        return None

def _generate_fallback_text(chunks_data: List[Dict[str, Any]]) -> str:
    """生成 fallback 文字"""
    if not chunks_data:
        return "很抱歉，找不到相關資訊。"

    if len(chunks_data) == 1:
        chunk = chunks_data[0]
        return f"【{chunk.get('title', '相關資訊')}】{chunk.get('summary', chunk.get('content', ''))[:100]}..."
    else:
        titles = [chunk.get('title', '相關資訊') for chunk in chunks_data[:3]]
        return f"找到 {len(chunks_data)} 筆相關資訊：{', '.join(titles)}等。"

def _create_interaction_handlers(chunks_data: List[Dict[str, Any]], interaction_mode: str) -> List[Dict[str, Any]]:
    """創建互動處理器"""
    handlers = []

    for chunk in chunks_data:
        chunk_id = chunk.get('chunk_id', '')

        # 基本互動
        handlers.append({
            'action_type': 'detail_explanation',
            'trigger': f"詳細說明 {chunk_id}",
            'target_chunk_id': chunk_id,
            'response_type': 'explanation'
        })

        handlers.append({
            'action_type': 'related_resources',
            'trigger': f"相關資源 {chunk_id}",
            'target_chunk_id': chunk_id,
            'response_type': 'resource_list'
        })

        # 進階互動
        if interaction_mode == 'advanced':
            handlers.append({
                'action_type': 'self_assessment',
                'trigger': f"自我檢測 {chunk_id}",
                'target_chunk_id': chunk_id,
                'response_type': 'assessment_form'
            })

    return handlers

def _identify_component_types(chunks_data: List[Dict[str, Any]]) -> List[str]:
    """識別使用的組件類型"""
    component_types = []

    for chunk in chunks_data:
        chunk_type = chunk.get('chunk_type', '')

        if chunk_type == 'warning_sign':
            component_types.append('comparison_card')
        elif chunk_type == 'bpsd_symptom':
            component_types.append('confidence_meter')
        elif chunk_type == 'coping_strategy':
            component_types.append('xai_box')
        else:
            component_types.append('info_box')

    return list(set(component_types))  # 去重

def _extract_primary_concepts(explanations: List[Dict[str, Any]]) -> List[str]:
    """提取主要概念"""
    all_concepts = []

    for explanation in explanations:
        concepts = explanation.get('related_concepts', [])
        all_concepts.extend(concepts)

    # 統計概念出現頻率並返回前5個
    from collections import Counter
    concept_counts = Counter(all_concepts)
    return [concept for concept, _ in concept_counts.most_common(5)]

def _assess_reasoning_complexity(explanations: List[Dict[str, Any]]) -> str:
    """評估推理複雜度"""
    total_steps = 0

    for explanation in explanations:
        reasoning_chain = explanation.get('reasoning_chain', [])
        total_steps += len(reasoning_chain)

    avg_steps = total_steps / len(explanations) if explanations else 0

    if avg_steps >= 4:
        return 'complex'
    elif avg_steps >= 2:
        return 'moderate'
    else:
        return 'simple'

def _generate_query_suggestions(original_query: str, chunks: List[ChunkData]) -> List[str]:
    """生成查詢建議"""
    suggestions = []

    # 基於找到的 chunks 生成相關建議
    if chunks:
        # 基於標籤生成建議
        all_tags = []
        for chunk in chunks:
            all_tags.extend(chunk.tags)

        unique_tags = list(set(all_tags))[:3]
        for tag in unique_tags:
            suggestions.append(f"了解更多關於「{tag}」的資訊")

        # 基於 chunk 類型生成建議
        chunk_types = [chunk.chunk_type for chunk in chunks]
        if 'warning_sign' in chunk_types:
            suggestions.append("想知道如何預防失智症嗎？")
        if 'coping_strategy' in chunk_types:
            suggestions.append("尋找更多照護技巧")

    # 通用建議
    if not suggestions:
        suggestions = [
            "了解失智症十大警訊",
            "查詢長照服務申請流程",
            "尋找專業照護資源"
        ]

    return suggestions[:3]  # 限制建議數量

def _calculate_query_complexity(query: str) -> float:
    """計算查詢複雜度"""
    # 簡單的複雜度評估
    word_count = len(query.split())
    char_count = len(query)

    # 基於長度的基礎分數
    complexity = min(word_count * 0.1 + char_count * 0.01, 1.0)

    # 基於特殊詞彙調整
    complex_keywords = ['如何', '為什麼', '什麼時候', '比較', '差異', '原因', '影響']
    for keyword in complex_keywords:
        if keyword in query:
            complexity += 0.1

    return min(complexity, 1.0)

async def _refresh_data_indexes():
    """重新整理資料索引（背景任務）"""
    try:
        logger.info("開始執行資料索引重新整理")

        # 模擬重新整理過程
        await asyncio.sleep(2)  # 模擬處理時間

        # 這裡應該實作實際的索引重建邏輯
        # 1. 重新讀取資料檔案
        # 2. 重新計算向量嵌入
        # 3. 更新 FAISS 索引
        # 4. 更新元資料

        logger.info("資料索引重新整理完成")

    except Exception as e:
        logger.error(f"資料索引重新整理失敗：{str(e)}")

# === Application Startup ===

@app.on_event("startup")
async def startup_event():
    """應用程式啟動時的初始化作業"""
    logger.info("啟動 XAI Flex Message API 服務")

    # 初始化各個引擎
    app.state.retrieval_engine = MultiLevelRetrieval()
    app.state.flex_generator = XAIFlexGenerator()
    app.state.explanation_engine = ExplanationEngine()

    logger.info("所有服務組件初始化完成")

@app.on_event("shutdown")
async def shutdown_event():
    """應用程式關閉時的清理作業"""
    logger.info("關閉 XAI Flex Message API 服務")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)