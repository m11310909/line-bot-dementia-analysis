# enhanced_api.py - 基於你現有代碼的增強版本
# 整合PRD實用概念：統一資料格式、配置管理、錯誤處理、測試框架

from fastapi import FastAPI, HTTPException, Depends, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field, field_validator
from typing import List, Dict, Any, Optional, Union
from dataclasses import dataclass, asdict
from enum import Enum
import logging
import yaml
import json
from datetime import datetime
from pathlib import Path
import uuid
import time

# ===== 1. 統一資料格式 (基於你的需求增強) =====

@dataclass
class SourceTrace:
    """來源追蹤"""
    source: str
    version: str = "1.0"
    authority_level: str = "general"
    last_verified: str = ""

@dataclass
class ExplanationData:
    """解釋資料"""
    reasoning: str = ""
    evidence_strength: str = "medium"
    similarity_score: float = 0.0
    authority_level: float = 0.0

class ChunkData(BaseModel):
    """統一的 Chunk 資料格式 - 兼容你現有的結構"""
    chunk_id: str
    module_id: str = "general"
    chunk_type: str = "info"
    title: str
    content: str
    confidence_score: float = Field(ge=0, le=1)
    keywords: List[str] = Field(default_factory=list)
    tags: List[str] = Field(default_factory=list)

    # 擴展資料
    explanation_data: Optional[Dict[str, Any]] = None
    source_trace: Optional[Dict[str, Any]] = None

    # 元數據
    created_at: str = ""

    def __post_init__(self):
        if not self.created_at:
            self.created_at = datetime.now().isoformat()

# ===== 2. 簡單配置管理 =====

class SimpleConfig:
    """簡化配置管理 - 適合你的項目規模"""

    def __init__(self, config_file: str = "config.yaml"):
        self.config_file = config_file
        self.config = self._load_config()
        self._setup_logging()

    def _load_config(self) -> Dict[str, Any]:
        default_config = {
            'api': {
                'title': 'Enhanced XAI Flex API',
                'version': '2.0.0',
                'debug': True
            },
            'knowledge_base': {
                'cache_enabled': True,
                'max_results': 10,
                'confidence_threshold': 0.5
            },
            'flex_message': {
                'default_template': 'bubble',
                'enable_xai': True,
                'max_components': 5
            },
            'logging': {
                'level': 'INFO',
                'file': 'api.log'
            }
        }

        try:
            config_path = Path(self.config_file)
            if config_path.exists():
                with open(config_path, 'r', encoding='utf-8') as f:
                    user_config = yaml.safe_load(f) or {}
                return self._merge_config(default_config, user_config)
            else:
                # 創建預設配置
                with open(config_path, 'w', encoding='utf-8') as f:
                    yaml.dump(default_config, f, default_flow_style=False, allow_unicode=True)
                return default_config
        except Exception as e:
            print(f"配置載入失敗，使用預設配置: {e}")
            return default_config

    def _merge_config(self, default: Dict, user: Dict) -> Dict:
        result = default.copy()
        for key, value in user.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = self._merge_config(result[key], value)
            else:
                result[key] = value
        return result

    def _setup_logging(self):
        log_level = getattr(logging, self.config['logging']['level'])
        logging.basicConfig(
            level=log_level,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.StreamHandler(),
                logging.FileHandler(self.config['logging']['file'], encoding='utf-8')
            ]
        )

    def get(self, key_path: str, default=None):
        """取得配置值，支援點記法"""
        keys = key_path.split('.')
        value = self.config
        try:
            for key in keys:
                value = value[key]
            return value
        except (KeyError, TypeError):
            return default

# ===== 3. 錯誤處理 =====

class APIError(Exception):
    """API 基礎錯誤"""
    pass

class KnowledgeBaseError(APIError):
    """知識庫錯誤"""
    pass

class FlexMessageError(APIError):
    """Flex Message 生成錯誤"""
    pass

class ErrorHandler:
    """統一錯誤處理"""

    def __init__(self, config: SimpleConfig):
        self.config = config
        self.logger = logging.getLogger(__name__)

    def handle_error(self, error: Exception, context: Dict = None) -> Dict[str, Any]:
        error_info = {
            'error_type': type(error).__name__,
            'error_message': str(error),
            'timestamp': datetime.now().isoformat(),
            'context': context or {}
        }

        # 記錄錯誤
        self.logger.error(f"API Error: {error_info}")

        # 用戶友好訊息
        user_message = self._get_user_message(error)

        return {
            'success': False,
            'error': user_message,
            'details': error_info if self.config.get('api.debug') else None
        }

    def _get_user_message(self, error: Exception) -> str:
        messages = {
            KnowledgeBaseError: "知識庫查詢失敗，請稍後再試",
            FlexMessageError: "視覺化組件生成失敗，請稍後再試",
            ConnectionError: "網路連線失敗，請檢查網路狀態",
            TimeoutError: "處理時間過長，請稍後再試"
        }

        for error_type, message in messages.items():
            if isinstance(error, error_type):
                return message

        return "系統發生錯誤，請稍後再試"

# ===== 4. 增強版知識庫 =====

class EnhancedKnowledgeBase:
    """增強版知識庫 - 基於你現有的結構"""

    def __init__(self, config: SimpleConfig):
        self.config = config
        self.logger = logging.getLogger(__name__)

        # 使用你的現有資料結構，但增強格式
        self.knowledge_base = {
            "dementia": [
                {
                    "chunk_id": "D001",
                    "module_id": "M1",
                    "chunk_type": "warning_sign",
                    "title": "記憶力減退影響日常生活",
                    "content": "忘記剛發生的事情、重複詢問同樣問題、需要依賴記憶輔助工具。",
                    "confidence_score": 0.95,
                    "keywords": ["記憶力", "健忘", "重複詢問"],
                    "tags": ["十大警訊", "早期症狀"],
                    "explanation_data": {
                        "reasoning": "基於台灣失智症協會十大警訊標準",
                        "evidence_strength": "high",
                        "similarity_score": 0.95,
                        "authority_level": 0.98
                    },
                    "source_trace": {
                        "source": "台灣失智症協會",
                        "version": "2024版",
                        "authority_level": "official",
                        "last_verified": "2024-12-01"
                    }
                },
                {
                    "chunk_id": "D002",
                    "module_id": "M1", 
                    "chunk_type": "warning_sign",
                    "title": "計劃事情或解決問題有困難",
                    "content": "無法專心、處理數字有困難、處理熟悉的事務需要更多時間。",
                    "confidence_score": 0.92,
                    "keywords": ["計劃困難", "數字處理", "專注力"],
                    "tags": ["十大警訊", "執行功能"],
                    "explanation_data": {
                        "reasoning": "執行功能障礙是失智症重要指標",
                        "evidence_strength": "high",
                        "similarity_score": 0.88,
                        "authority_level": 0.96
                    }
                }
            ],
            "ltc": [
                {
                    "chunk_id": "L001",
                    "module_id": "L1",
                    "chunk_type": "service_info",
                    "title": "長照2.0服務申請流程",
                    "content": "撥打1966長照專線或至長照管理中心申請評估。評估後依失能等級提供相應服務。",
                    "confidence_score": 0.97,
                    "keywords": ["長照2.0", "1966專線", "失能評估"],
                    "tags": ["長照服務", "申請指南"],
                    "explanation_data": {
                        "reasoning": "官方長照服務標準流程",
                        "evidence_strength": "high",
                        "similarity_score": 0.94,
                        "authority_level": 0.99
                    },
                    "source_trace": {
                        "source": "衛生福利部長照司",
                        "version": "2024版",
                        "authority_level": "official",
                        "last_verified": "2024-11-15"
                    }
                }
            ]
        }

        self.search_stats = {
            'total_queries': 0,
            'successful_queries': 0,
            'average_results': 0.0
        }

    def search(self, query: str, module: str = "hybrid", max_results: int = None) -> List[Dict[str, Any]]:
        """增強版搜尋 - 保持你的介面但增加功能"""

        self.search_stats['total_queries'] += 1
        max_results = max_results or self.config.get('knowledge_base.max_results', 5)

        try:
            results = []
            search_modules = [module] if module != "hybrid" else ["dementia", "ltc"]

            for search_module in search_modules:
                if search_module in self.knowledge_base:
                    for item in self.knowledge_base[search_module]:
                        # 增強的匹配邏輯
                        score = self._calculate_relevance_score(query, item)
                        if score > self.config.get('knowledge_base.confidence_threshold', 0.5):
                            # 轉換為統一格式但保持你的API相容性
                            result = {
                                "chunk_id": item["chunk_id"],
                                "module_id": item["module_id"],
                                "chunk_type": item["chunk_type"],
                                "title": item["title"],
                                "content": item["content"],
                                "confidence_score": item["confidence_score"],
                                "keywords": item["keywords"],
                                "tags": item["tags"],
                                "explanation_data": item.get("explanation_data", {}),
                                "source_trace": item.get("source_trace", {}),
                                "relevance_score": score  # 新增相關性分數
                            }
                            results.append(result)

            # 按相關性排序
            results.sort(key=lambda x: x['relevance_score'], reverse=True)

            if results:
                self.search_stats['successful_queries'] += 1

            return results[:max_results]

        except Exception as e:
            self.logger.error(f"搜尋失敗: {e}")
            raise KnowledgeBaseError(f"搜尋失敗: {str(e)}")

    def _calculate_relevance_score(self, query: str, item: Dict) -> float:
        """計算相關性分數"""
        query_lower = query.lower()
        score = 0.0

        # 關鍵字匹配
        keyword_matches = sum(1 for keyword in item["keywords"] if keyword in query_lower)
        score += keyword_matches * 0.3

        # 標題匹配
        if any(word in item["title"].lower() for word in query_lower.split()):
            score += 0.4

        # 內容匹配
        if any(word in item["content"].lower() for word in query_lower.split()):
            score += 0.2

        # 標籤匹配
        tag_matches = sum(1 for tag in item["tags"] if tag in query_lower)
        score += tag_matches * 0.1

        return min(score, 1.0)

    def get_stats(self) -> Dict[str, Any]:
        """取得搜尋統計"""
        if self.search_stats['total_queries'] > 0:
            self.search_stats['success_rate'] = self.search_stats['successful_queries'] / self.search_stats['total_queries']
        return self.search_stats.copy()

# ===== 5. 增強版 Flex Message 生成器 =====

class EnhancedFlexGenerator:
    """增強版 Flex Message 生成器 - 基於你的需求"""

    def __init__(self, config: SimpleConfig):
        self.config = config
        self.logger = logging.getLogger(__name__)
        self.generation_stats = {
            'total_generated': 0,
            'template_usage': {},
            'error_count': 0
        }

    def generate_flex_message(self, chunks: List[Dict[str, Any]], options: Dict = None) -> Dict[str, Any]:
        """生成 Flex Message - 保持你的 API 但增強功能"""

        try:
            self.generation_stats['total_generated'] += 1

            if not chunks:
                return self._create_empty_message()

            # 根據 chunk 數量選擇模板
            if len(chunks) == 1:
                return self._create_single_bubble(chunks[0])
            else:
                return self._create_carousel(chunks)

        except Exception as e:
            self.generation_stats['error_count'] += 1
            self.logger.error(f"Flex Message 生成失敗: {e}")
            raise FlexMessageError(f"生成失敗: {str(e)}")

    def _create_single_bubble(self, chunk: Dict[str, Any]) -> Dict[str, Any]:
        """創建單一泡泡訊息 - 增強版"""

        # 根據 chunk_type 決定樣式
        colors = self._get_colors_by_type(chunk.get('chunk_type', 'info'))

        bubble = {
            "type": "bubble",
            "size": "giga",
            "header": {
                "type": "box",
                "layout": "vertical",
                "backgroundColor": colors['header_bg'],
                "paddingAll": "12px",
                "contents": [
                    {
                        "type": "text",
                        "text": f"🔍 {chunk['title']}",
                        "weight": "bold",
                        "size": "lg",
                        "color": colors['header_text'],
                        "wrap": True
                    },
                    self._create_confidence_indicator(chunk.get('confidence_score', 0.8))
                ]
            },
            "body": {
                "type": "box",
                "layout": "vertical",
                "paddingAll": "16px",
                "contents": [
                    {
                        "type": "text",
                        "text": chunk['content'][:200] + ("..." if len(chunk['content']) > 200 else ""),
                        "wrap": True,
                        "size": "sm",
                        "color": "#333333"
                    }
                ]
            },
            "footer": self._create_enhanced_footer(chunk)
        }

        # 如果有 XAI 資料，添加解釋區塊
        if chunk.get('explanation_data'):
            bubble["body"]["contents"].extend([
                {"type": "separator", "margin": "lg"},
                self._create_xai_section(chunk['explanation_data'])
            ])

        return {
            "type": "flex",
            "altText": f"失智照護資訊：{chunk['title']}",
            "contents": bubble
        }

    def _create_carousel(self, chunks: List[Dict[str, Any]]) -> Dict[str, Any]:
        """創建輪播訊息"""

        max_bubbles = self.config.get('flex_message.max_components', 5)
        bubbles = []

        for chunk in chunks[:max_bubbles]:
            single_result = self._create_single_bubble(chunk)
            bubbles.append(single_result["contents"])

        return {
            "type": "flex",
            "altText": f"找到 {len(chunks)} 筆相關的失智照護資訊",
            "contents": {
                "type": "carousel",
                "contents": bubbles
            }
        }

    def _create_confidence_indicator(self, confidence: float) -> Dict[str, Any]:
        """創建信心度指標"""
        percentage = int(confidence * 100)
        color = "#95E1A3" if confidence >= 0.8 else "#FFD93D" if confidence >= 0.6 else "#FF6B6B"

        return {
            "type": "box",
            "layout": "horizontal",
            "margin": "sm",
            "contents": [
                {
                    "type": "text",
                    "text": f"可信度 {percentage}%",
                    "size": "xs",
                    "color": color,
                    "flex": 0
                },
                {
                    "type": "box",
                    "layout": "vertical",
                    "flex": 1,
                    "margin": "sm",
                    "contents": [
                        {
                            "type": "box",
                            "layout": "horizontal",
                            "backgroundColor": "#F0F0F0",
                            "height": "4px",
                            "contents": [
                                {
                                    "type": "box",
                                    "layout": "vertical",
                                    "backgroundColor": color,
                                    "width": f"{percentage}%",
                                    "contents": []
                                }
                            ]
                        }
                    ]
                }
            ]
        }

    def _create_xai_section(self, explanation_data: Dict) -> Dict[str, Any]:
        """創建 XAI 解釋區塊"""
        return {
            "type": "box",
            "layout": "vertical",
            "backgroundColor": "#F8F9FA",
            "paddingAll": "12px",
            "cornerRadius": "8px",
            "contents": [
                {
                    "type": "text",
                    "text": "🧠 AI 分析說明",
                    "weight": "bold",
                    "size": "sm",
                    "color": "#4ECDC4"
                },
                {
                    "type": "text",
                    "text": explanation_data.get('reasoning', '基於專業知識庫分析'),
                    "size": "xs",
                    "color": "#666666",
                    "wrap": True,
                    "margin": "sm"
                },
                {
                    "type": "text",
                    "text": f"證據強度：{explanation_data.get('evidence_strength', 'medium')}",
                    "size": "xs",
                    "color": "#999999",
                    "margin": "xs"
                }
            ]
        }

    def _create_enhanced_footer(self, chunk: Dict[str, Any]) -> Dict[str, Any]:
        """創建增強版頁尾"""
        return {
            "type": "box",
            "layout": "horizontal",
            "paddingAll": "12px",
            "contents": [
                {
                    "type": "button",
                    "style": "primary",
                    "height": "sm",
                    "action": {
                        "type": "message",
                        "label": "詳細說明",  # 👈 添加這行
                        "text": f"詳細說明 {chunk.get('chunk_id', '')}"
                    },
                    "color": "#4ECDC4",
                    "flex": 1
                },
                {
                    "type": "button",
                    "style": "secondary", 
                    "height": "sm",
                    "action": {
                        "type": "message",
                        "label": "相關資源",  # 👈 添加這行
                        "text": f"相關資源 {chunk.get('chunk_id', '')}"
                    },
                    "flex": 1,
                    "margin": "sm"
                }
            ]
        }

    def _get_colors_by_type(self, chunk_type: str) -> Dict[str, str]:
        """根據類型取得顏色配置"""
        color_schemes = {
            'warning_sign': {'header_bg': '#FFE5E5', 'header_text': '#FF6B6B'},
            'service_info': {'header_bg': '#E5F7F6', 'header_text': '#4ECDC4'},
            'info': {'header_bg': '#F5F5F5', 'header_text': '#666666'}
        }
        return color_schemes.get(chunk_type, color_schemes['info'])

    def _create_empty_message(self) -> Dict[str, Any]:
        """創建空狀態訊息"""
        return {
            "type": "flex",
            "altText": "很抱歉，目前找不到相關資訊",
            "contents": {
                "type": "bubble",
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "text",
                            "text": "🔍 找不到相關資訊",
                            "weight": "bold",
                            "size": "lg",
                            "align": "center"
                        },
                        {
                            "type": "text",
                            "text": "請嘗試重新描述您的問題",
                            "wrap": True,
                            "margin": "md",
                            "size": "sm",
                            "color": "#666666",
                            "align": "center"
                        }
                    ]
                }
            }
        }

    def get_stats(self) -> Dict[str, Any]:
        """取得生成統計"""
        return self.generation_stats.copy()

# ===== 6. API 模型定義 =====

class AnalyzeRequest(BaseModel):
    query: str = Field(..., min_length=1, max_length=500)
    module: str = "hybrid"
    max_chunks: int = Field(5, ge=1, le=20)
    include_xai: bool = True

class FlexMessageRequest(BaseModel):
    chunk_ids: List[str] = Field(..., min_items=1)
    options: Optional[Dict[str, Any]] = None

# ===== 7. 增強版 FastAPI 應用 =====

# 全域配置和服務
config = SimpleConfig()
error_handler = ErrorHandler(config)
knowledge_base = EnhancedKnowledgeBase(config)
flex_generator = EnhancedFlexGenerator(config)

app = FastAPI(
    title=config.get('api.title'),
    version=config.get('api.version'),
    description="增強版 XAI Flex Message API - 整合 PRD 實用概念"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

logger = logging.getLogger(__name__)

@app.get("/")
async def root():
    return {
        "message": "Enhanced XAI Flex Message API",
        "version": config.get('api.version'),
        "features": [
            "統一資料格式",
            "配置管理",
            "錯誤處理",
            "增強搜尋",
            "XAI 解釋"
        ],
        "docs": "/docs"
    }

@app.get("/api/v1/health")
async def health_check():
    """增強版健康檢查"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": config.get('api.version'),
        "services": {
            "api": "running",
            "knowledge_base": "ready",
            "flex_generator": "ready"
        },
        "stats": {
            "search": knowledge_base.get_stats(),
            "flex_generation": flex_generator.get_stats()
        }
    }

@app.post("/api/v1/analyze/{module}")
async def analyze_query(module: str, request: AnalyzeRequest):
    """增強版查詢分析 - 保持你的 API 介面"""

    try:
        logger.info(f"查詢: {request.query}, 模組: {module}")

        # 使用增強版搜尋
        results = knowledge_base.search(
            query=request.query,
            module=module,
            max_results=request.max_chunks
        )

        return {
            "chunks": results,
            "total_found": len(results),
            "query_analysis": {
                "original_query": request.query,
                "processed_query": request.query.lower().strip(),
                "detected_keywords": [word for word in request.query.split() if len(word) > 2],
                "search_module": module
            },
            "processing_time": 0.1,
            "metadata": {
                "search_stats": knowledge_base.get_stats(),
                "timestamp": datetime.now().isoformat(),
                "xai_enabled": request.include_xai
            }
        }

    except Exception as e:
        error_response = error_handler.handle_error(e, {
            'query': request.query,
            'module': module
        })
        raise HTTPException(status_code=500, detail=error_response)

@app.post("/api/v1/flex-message")
async def generate_flex_message(request: FlexMessageRequest):
    """增強版 Flex Message 生成"""

    try:
        # 根據 chunk_ids 取得完整資料
        chunks_data = []

        for chunk_id in request.chunk_ids:
            # 在知識庫中尋找對應的 chunk
            found = False
            for module_data in knowledge_base.knowledge_base.values():
                for item in module_data:
                    if item['chunk_id'] == chunk_id:
                        chunks_data.append(item)
                        found = True
                        break
                if found:
                    break

        if not chunks_data:
            raise FlexMessageError("找不到指定的 chunk 資料")

        # 生成 Flex Message
        flex_result = flex_generator.generate_flex_message(
            chunks_data,
            request.options
        )

        return {
            "flex_message": flex_result["contents"],
            "fallback_text": flex_result["altText"],
            "metadata": {
                "generated_at": datetime.now().isoformat(),
                "chunk_count": len(chunks_data),
                "generation_stats": flex_generator.get_stats()
            }
        }

    except Exception as e:
        error_response = error_handler.handle_error(e, {
            'chunk_ids': request.chunk_ids
        })
        raise HTTPException(status_code=500, detail=error_response)

@app.get("/api/v1/stats")
async def get_system_stats():
    """系統統計資訊"""
    return {
        "knowledge_base": knowledge_base.get_stats(),
        "flex_generator": flex_generator.get_stats(),
        "config_summary": {
            "max_results": config.get('knowledge_base.max_results'),
            "confidence_threshold": config.get('knowledge_base.confidence_threshold'),
            "debug_mode": config.get('api.debug')
        },
        "timestamp": datetime.now().isoformat()
    }

@app.get("/api/v1/config")
async def get_config():
    """取得當前配置（除敏感資訊外）"""
    safe_config = config.config.copy()
    return {
        "config": safe_config,
        "config_file": config.config_file,
        "timestamp": datetime.now().isoformat()
    }

# ===== 8. 簡化測試框架 =====

@app.post("/api/v1/test")
async def run_system_tests():
    """運行系統測試"""

    test_results = {
        'timestamp': datetime.now().isoformat(),
        'tests': {}
    }

    # 測試 1: 知識庫搜尋
    try:
        search_result = knowledge_base.search("記憶力", "dementia", 2)
        test_results['tests']['knowledge_base_search'] = {
            'status': 'passed' if len(search_result) > 0 else 'failed',
            'results_count': len(search_result),
            'message': '知識庫搜尋正常'
        }
    except Exception as e:
        test_results['tests']['knowledge_base_search'] = {
            'status': 'failed',
            'error': str(e)
        }

    # 測試 2: Flex Message 生成
    try:
        test_chunk = {
            'chunk_id': 'TEST-001',
            'title': '測試標題',
            'content': '測試內容',
            'confidence_score': 0.8,
            'chunk_type': 'info'
        }
        flex_result = flex_generator.generate_flex_message([test_chunk])
        test_results['tests']['flex_generation'] = {
            'status': 'passed' if 'contents' in flex_result else 'failed',
            'message': 'Flex Message 生成正常'
        }
    except Exception as e:
        test_results['tests']['flex_generation'] = {
            'status': 'failed',
            'error': str(e)
        }

    # 測試 3: 配置載入
    try:
        debug_mode = config.get('api.debug')
        test_results['tests']['config_loading'] = {
            'status': 'passed',
            'debug_mode': debug_mode,
            'message': '配置載入正常'
        }
    except Exception as e:
        test_results['tests']['config_loading'] = {
            'status': 'failed',
            'error': str(e)
        }

    # 測試 4: 錯誤處理
    try:
        test_error = Exception("測試錯誤")
        error_result = error_handler.handle_error(test_error)
        test_results['tests']['error_handling'] = {
            'status': 'passed' if not error_result['success'] else 'failed',
            'message': '錯誤處理正常'
        }
    except Exception as e:
        test_results['tests']['error_handling'] = {
            'status': 'failed',
            'error': str(e)
        }

    # 計算總體結果
    passed_tests = sum(1 for test in test_results['tests'].values() if test['status'] == 'passed')
    total_tests = len(test_results['tests'])

    test_results['summary'] = {
        'total_tests': total_tests,
        'passed_tests': passed_tests,
        'success_rate': passed_tests / total_tests if total_tests > 0 else 0,
        'overall_status': 'healthy' if passed_tests == total_tests else 'degraded'
    }

    return test_results

# ===== 9. 演示頁面 =====

@app.get("/demo", response_class=HTMLResponse)
async def demo_page():
    """增強版演示頁面"""
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Enhanced XAI Flex API Demo</title>
        <script src="https://unpkg.com/axios/dist/axios.min.js"></script>
        <style>
            body { 
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
                margin: 0; 
                padding: 20px; 
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
            }
            .container { 
                max-width: 1000px; 
                margin: 0 auto; 
                background: white; 
                padding: 30px; 
                border-radius: 15px; 
                box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            }
            .header {
                text-align: center;
                margin-bottom: 30px;
                padding: 20px;
                background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
                color: white;
                border-radius: 10px;
            }
            .test-section {
                margin: 20px 0;
                padding: 20px;
                border: 2px solid #e0e0e0;
                border-radius: 10px;
                background: #f9f9f9;
            }
            button { 
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white; 
                border: none; 
                padding: 12px 24px; 
                border-radius: 8px; 
                cursor: pointer; 
                margin: 8px; 
                font-weight: bold;
                transition: transform 0.2s;
            }
            button:hover { 
                transform: translateY(-2px);
                box-shadow: 0 5px 15px rgba(0,0,0,0.2);
            }
            .result {
                margin: 15px 0;
                padding: 15px;
                border-radius: 8px;
                border-left: 4px solid #4facfe;
                background: white;
            }
            .success { border-left-color: #28a745; background: #f8fff9; }
            .error { border-left-color: #dc3545; background: #fff8f8; }
            .stats {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                gap: 15px;
                margin: 20px 0;
            }
            .stat-card {
                background: white;
                padding: 15px;
                border-radius: 8px;
                text-align: center;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            }
            .stat-number {
                font-size: 2em;
                font-weight: bold;
                color: #667eea;
            }
            pre { 
                background: #f4f4f4; 
                padding: 15px; 
                border-radius: 8px; 
                overflow-x: auto; 
                max-height: 400px;
                border: 1px solid #ddd;
            }
            .loading {
                text-align: center;
                padding: 40px;
                color: #666;
            }
            .flex-preview {
                border: 2px solid #4facfe;
                border-radius: 10px;
                padding: 15px;
                margin: 10px 0;
                background: linear-gradient(135deg, #f8fbff 0%, #e8f4ff 100%);
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🚀 Enhanced XAI Flex API</h1>
                <p>整合 PRD 實用概念的增強版本</p>
                <div class="stats" id="headerStats"></div>
            </div>

            <div class="test-section">
                <h2>📋 系統測試</h2>
                <button onclick="runSystemTests()">完整系統測試</button>
                <button onclick="getSystemStats()">系統統計</button>
                <button onclick="getConfig()">查看配置</button>
                <div id="systemResults"></div>
            </div>

            <div class="test-section">
                <h2>🔍 知識庫測試</h2>
                <button onclick="testSearch('記憶力', 'dementia')">搜尋「記憶力」</button>
                <button onclick="testSearch('長照', 'ltc')">搜尋「長照」</button>
                <button onclick="testSearch('失智症', 'hybrid')">混合搜尋「失智症」</button>
                <div id="searchResults"></div>
            </div>

            <div class="test-section">
                <h2>🎨 Flex Message 測試</h2>
                <button onclick="testFlexGeneration(['D001'])">生成單一卡片</button>
                <button onclick="testFlexGeneration(['D001', 'L001'])">生成輪播卡片</button>
                <button onclick="testFlexGeneration(['INVALID'])">測試錯誤處理</button>
                <div id="flexResults"></div>
            </div>

            <div class="test-section">
                <h2>📊 即時統計</h2>
                <div class="stats" id="liveStats"></div>
            </div>
        </div>

        <script>
        // 頁面載入時更新統計
        window.onload = function() {
            updateHeaderStats();
            updateLiveStats();
        };

        async function updateHeaderStats() {
            try {
                const response = await axios.get('/api/v1/health');
                const data = response.data;

                document.getElementById('headerStats').innerHTML = `
                    <div class="stat-card">
                        <div class="stat-number">${data.stats.search.total_queries || 0}</div>
                        <div>總搜尋次數</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-number">${data.stats.flex_generation.total_generated || 0}</div>
                        <div>生成次數</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-number">${data.version}</div>
                        <div>系統版本</div>
                    </div>
                `;
            } catch (error) {
                console.error('更新統計失敗:', error);
            }
        }

        async function updateLiveStats() {
            try {
                const response = await axios.get('/api/v1/stats');
                const stats = response.data;

                const searchSuccessRate = stats.knowledge_base.success_rate ? 
                    (stats.knowledge_base.success_rate * 100).toFixed(1) : '0';

                document.getElementById('liveStats').innerHTML = `
                    <div class="stat-card">
                        <div class="stat-number">${searchSuccessRate}%</div>
                        <div>搜尋成功率</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-number">${stats.flex_generator.error_count || 0}</div>
                        <div>生成錯誤數</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-number">${stats.config_summary.max_results || 0}</div>
                        <div>最大結果數</div>
                    </div>
                `;
            } catch (error) {
                console.error('更新即時統計失敗:', error);
            }
        }

        async function runSystemTests() {
            showLoading('systemResults', '執行完整系統測試...');

            try {
                const response = await axios.post('/api/v1/test');
                const results = response.data;

                let html = `
                    <div class="result ${results.summary.overall_status === 'healthy' ? 'success' : 'error'}">
                        <h3>🧪 測試結果總覽</h3>
                        <p><strong>總測試數:</strong> ${results.summary.total_tests}</p>
                        <p><strong>通過測試:</strong> ${results.summary.passed_tests}</p>
                        <p><strong>成功率:</strong> ${(results.summary.success_rate * 100).toFixed(1)}%</p>
                        <p><strong>系統狀態:</strong> ${results.summary.overall_status}</p>
                    </div>
                `;

                for (const [testName, testResult] of Object.entries(results.tests)) {
                    html += `
                        <div class="result ${testResult.status === 'passed' ? 'success' : 'error'}">
                            <h4>${testResult.status === 'passed' ? '✅' : '❌'} ${testName}</h4>
                            <p>${testResult.message || testResult.error || '測試完成'}</p>
                        </div>
                    `;
                }

                document.getElementById('systemResults').innerHTML = html;
                updateLiveStats(); // 更新統計

            } catch (error) {
                showError('systemResults', '系統測試失敗: ' + error.message);
            }
        }

        async function testSearch(query, module) {
            showLoading('searchResults', `搜尋「${query}」中...`);

            try {
                const response = await axios.post(`/api/v1/analyze/${module}`, {
                    query: query,
                    module: module,
                    max_chunks: 5
                });

                const data = response.data;

                let html = `
                    <div class="result success">
                        <h3>🔍 搜尋結果</h3>
                        <p><strong>查詢:</strong> ${query}</p>
                        <p><strong>模組:</strong> ${module}</p>
                        <p><strong>找到結果:</strong> ${data.total_found} 筆</p>
                        <p><strong>處理時間:</strong> ${data.processing_time}s</p>
                    </div>
                `;

                data.chunks.forEach((chunk, index) => {
                    html += `
                        <div class="result">
                            <h4>📄 結果 ${index + 1}: ${chunk.title}</h4>
                            <p><strong>ID:</strong> ${chunk.chunk_id}</p>
                            <p><strong>信心度:</strong> ${(chunk.confidence_score * 100).toFixed(1)}%</p>
                            <p><strong>內容:</strong> ${chunk.content.substring(0, 100)}...</p>
                            <p><strong>關鍵字:</strong> ${chunk.keywords.join(', ')}</p>
                            ${chunk.relevance_score ? `<p><strong>相關性:</strong> ${chunk.relevance_score.toFixed(2)}</p>` : ''}
                        </div>
                    `;
                });

                document.getElementById('searchResults').innerHTML = html;
                updateLiveStats();

            } catch (error) {
                showError('searchResults', '搜尋失敗: ' + error.message);
            }
        }

        async function testFlexGeneration(chunkIds) {
            showLoading('flexResults', '生成 Flex Message...');

            try {
                const response = await axios.post('/api/v1/flex-message', {
                    chunk_ids: chunkIds
                });

                const data = response.data;

                let html = `
                    <div class="result success">
                        <h3>🎨 Flex Message 生成成功</h3>
                        <p><strong>Chunk IDs:</strong> ${chunkIds.join(', ')}</p>
                        <p><strong>卡片數量:</strong> ${data.metadata.chunk_count}</p>
                        <p><strong>生成時間:</strong> ${data.metadata.generated_at}</p>
                    </div>
                `;

                html += `
                    <div class="flex-preview">
                        <h4>📱 Flex Message 預覽</h4>
                        <p><strong>Alt Text:</strong> ${data.fallback_text}</p>
                        <details>
                            <summary>查看 JSON 結構</summary>
                            <pre>${JSON.stringify(data.flex_message, null, 2)}</pre>
                        </details>
                    </div>
                `;

                document.getElementById('flexResults').innerHTML = html;
                updateLiveStats();

            } catch (error) {
                showError('flexResults', 'Flex Message 生成失敗: ' + error.message);
            }
        }

        async function getSystemStats() {
            showLoading('systemResults', '載入系統統計...');

            try {
                const response = await axios.get('/api/v1/stats');
                const stats = response.data;

                const html = `
                    <div class="result">
                        <h3>📊 系統統計</h3>
                        <pre>${JSON.stringify(stats, null, 2)}</pre>
                    </div>
                `;

                document.getElementById('systemResults').innerHTML = html;

            } catch (error) {
                showError('systemResults', '統計載入失敗: ' + error.message);
            }
        }

        async function getConfig() {
            showLoading('systemResults', '載入系統配置...');

            try {
                const response = await axios.get('/api/v1/config');
                const config = response.data;

                const html = `
                    <div class="result">
                        <h3>⚙️ 系統配置</h3>
                        <p><strong>配置檔案:</strong> ${config.config_file}</p>
                        <pre>${JSON.stringify(config.config, null, 2)}</pre>
                    </div>
                `;

                document.getElementById('systemResults').innerHTML = html;

            } catch (error) {
                showError('systemResults', '配置載入失敗: ' + error.message);
            }
        }

        function showLoading(elementId, message) {
            document.getElementById(elementId).innerHTML = 
                `<div class="loading">⏳ ${message}</div>`;
        }

        function showError(elementId, message) {
            document.getElementById(elementId).innerHTML = 
                `<div class="result error">❌ ${message}</div>`;
        }

        // 每30秒自動更新統計
        setInterval(updateLiveStats, 30000);
        </script>
    </body>
    </html>
    """

if __name__ == "__main__":
    import uvicorn

    print("🚀 啟動增強版 XAI Flex Message API")
    print(f"📖 文檔: http://localhost:8000/docs")
    print(f"🎨 演示: http://localhost:8000/demo")
    print(f"📊 統計: http://localhost:8000/api/v1/stats")
    print(f"🧪 測試: http://localhost:8000/api/v1/test")

    # 創建範例配置檔案
    if not Path("config.yaml").exists():
        print("📝 創建範例配置檔案...")
        sample_config = {
            'api': {
                'title': 'Enhanced XAI Flex API',
                'version': '2.0.0',
                'debug': True
            },
            'knowledge_base': {
                'cache_enabled': True,
                'max_results': 5,
                'confidence_threshold': 0.5
            },
            'flex_message': {
                'default_template': 'bubble',
                'enable_xai': True,
                'max_components': 5
            },
            'logging': {
                'level': 'INFO',
                'file': 'api.log'
            }
        }

        with open("config.yaml", "w", encoding="utf-8") as f:
            yaml.dump(sample_config, f, default_flow_style=False, allow_unicode=True)
        print("✅ 配置檔案已創建: config.yaml")

    uvicorn.run(app, host="0.0.0.0", port=8001)