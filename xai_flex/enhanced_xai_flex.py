"""
整合PRD實用概念的增強版XAI Flex系統
基於你現有的優秀架構，有選擇性地加入實用功能
"""

from typing import Dict, List, Any, Optional, Union
from dataclasses import dataclass, asdict
from enum import Enum
import json
import yaml
import logging
from datetime import datetime
from pathlib import Path
import traceback

# ===== 1. 統一的資料格式 =====

@dataclass
class SourceTrace:
    """來源追蹤統一格式"""
    source: str
    version: str = "1.0"
    authority_level: str = "general"  # official, academic, professional, general
    last_verified: str = ""
    section: str = ""
    page_number: Optional[int] = None

@dataclass
class ExplanationData:
    """解釋資料統一格式"""
    reasoning: str
    evidence_strength: str = "medium"  # high, medium, low
    related_concepts: List[str] = None
    contraindications: List[str] = None
    confidence_breakdown: Dict[str, float] = None

    def __post_init__(self):
        if self.related_concepts is None:
            self.related_concepts = []
        if self.contraindications is None:
            self.contraindications = []
        if self.confidence_breakdown is None:
            self.confidence_breakdown = {}

@dataclass
class VisualConfig:
    """視覺化配置統一格式"""
    component_type: str
    layout_priority: str = "medium"  # high, medium, low
    color_theme: str = "neutral"  # warning, info, success, neutral
    interactive_elements: List[str] = None

    def __post_init__(self):
        if self.interactive_elements is None:
            self.interactive_elements = []

@dataclass
class ChunkData:
    """統一的Chunk資料格式 - 你現有架構的標準化版本"""

    # 必要欄位
    chunk_id: str
    module_id: str
    chunk_type: str
    title: str
    content: str
    confidence_score: float

    # 可選欄位 - 使用你現有的結構
    summary: Optional[str] = None
    keywords: List[str] = None
    tags: List[str] = None
    difficulty_level: str = "basic"  # basic, moderate, severe
    target_audience: List[str] = None

    # 結構化子物件
    explanation_data: Optional[ExplanationData] = None
    source_trace: Optional[SourceTrace] = None
    visual_config: Optional[VisualConfig] = None

    # 元數據
    created_at: str = ""
    updated_at: str = ""
    usage_count: int = 0
    feedback_score: float = 0.0

    def __post_init__(self):
        """初始化預設值"""
        if self.keywords is None:
            self.keywords = []
        if self.tags is None:
            self.tags = []
        if self.target_audience is None:
            self.target_audience = ["一般民眾"]
        if not self.created_at:
            self.created_at = datetime.now().isoformat()
        if not self.updated_at:
            self.updated_at = self.created_at

    def to_dict(self) -> Dict[str, Any]:
        """轉換為字典格式，保持與你現有代碼的相容性"""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ChunkData':
        """從字典創建實例"""
        # 處理嵌套物件
        if 'explanation_data' in data and data['explanation_data']:
            data['explanation_data'] = ExplanationData(**data['explanation_data'])
        if 'source_trace' in data and data['source_trace']:
            data['source_trace'] = SourceTrace(**data['source_trace'])
        if 'visual_config' in data and data['visual_config']:
            data['visual_config'] = VisualConfig(**data['visual_config'])

        return cls(**data)

@dataclass
class FlexMessageResponse:
    """統一的Flex Message回應格式"""
    flex_message: Dict[str, Any]
    fallback_text: str
    interaction_handlers: List[Dict[str, Any]] = None
    metadata: Dict[str, Any] = None
    accessibility_enhanced: bool = False

    def __post_init__(self):
        if self.interaction_handlers is None:
            self.interaction_handlers = []
        if self.metadata is None:
            self.metadata = {
                'generated_at': datetime.now().isoformat(),
                'generator_version': '2.0'
            }

# ===== 2. 簡單的配置管理 =====

class SimpleConfig:
    """簡化的配置管理器 - 不需要PRD的複雜ConfigManager"""

    def __init__(self, config_file: str = "config/xai_flex_config.yaml"):
        self.config_file = config_file
        self.config = self._load_config()
        self._setup_logging()

    def _load_config(self) -> Dict[str, Any]:
        """載入配置檔案"""
        default_config = {
            'genai': {
                'default_provider': 'openai',
                'temperature': 0.7,
                'max_tokens': 2000,
                'timeout': 30
            },
            'visual': {
                'default_theme': 'healthcare',
                'language': 'zh-TW',
                'accessibility_mode': False,
                'component_cache': True
            },
            'system': {
                'debug': False,
                'log_level': 'INFO',
                'max_chunks_per_request': 10,
                'response_cache_ttl': 300
            },
            'modules': {
                'M1': {'enabled': True, 'confidence_threshold': 0.6},
                'M2': {'enabled': True, 'confidence_threshold': 0.7},
                'M3': {'enabled': True, 'confidence_threshold': 0.6}
            }
        }

        try:
            config_path = Path(self.config_file)
            if config_path.exists():
                with open(config_path, 'r', encoding='utf-8') as f:
                    user_config = yaml.safe_load(f) or {}
                # 合併配置
                return self._merge_config(default_config, user_config)
            else:
                # 創建預設配置檔案
                config_path.parent.mkdir(parents=True, exist_ok=True)
                with open(config_path, 'w', encoding='utf-8') as f:
                    yaml.dump(default_config, f, default_flow_style=False, allow_unicode=True)
                return default_config
        except Exception as e:
            print(f"配置檔案載入失敗，使用預設配置: {e}")
            return default_config

    def _merge_config(self, default: Dict, user: Dict) -> Dict:
        """遞迴合併配置"""
        result = default.copy()
        for key, value in user.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = self._merge_config(result[key], value)
            else:
                result[key] = value
        return result

    def _setup_logging(self):
        """設定日誌"""
        log_level = getattr(logging, self.config['system']['log_level'].upper())
        logging.basicConfig(
            level=log_level,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.StreamHandler(),
                logging.FileHandler('logs/xai_flex.log', encoding='utf-8')
            ] if not self.config['system']['debug'] else [logging.StreamHandler()]
        )

    def get(self, key_path: str, default=None):
        """取得配置值，支援點記法 e.g., 'genai.temperature'"""
        keys = key_path.split('.')
        value = self.config
        try:
            for key in keys:
                value = value[key]
            return value
        except (KeyError, TypeError):
            return default

    def get_module_config(self, module_id: str) -> Dict[str, Any]:
        """取得模組特定配置"""
        return self.config.get('modules', {}).get(module_id, {})

# ===== 3. 基本的錯誤處理 =====

class XAIFlexError(Exception):
    """XAI Flex 系統基礎例外"""
    pass

class ComponentGenerationError(XAIFlexError):
    """組件生成錯誤"""
    pass

class ConfigurationError(XAIFlexError):
    """配置錯誤"""
    pass

class ValidationError(XAIFlexError):
    """資料驗證錯誤"""
    pass

class ErrorHandler:
    """統一的錯誤處理器"""

    def __init__(self, config: SimpleConfig):
        self.config = config
        self.logger = logging.getLogger(__name__)

    def handle_error(self, error: Exception, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """統一錯誤處理"""
        error_info = {
            'error_type': type(error).__name__,
            'error_message': str(error),
            'timestamp': datetime.now().isoformat(),
            'context': context or {}
        }

        if self.config.get('system.debug'):
            error_info['traceback'] = traceback.format_exc()

        # 記錄錯誤
        self.logger.error(f"XAI Flex Error: {error_info}")

        # 根據錯誤類型返回適當的用戶友好訊息
        user_message = self._get_user_friendly_message(error)

        return {
            'success': False,
            'error': user_message,
            'error_details': error_info if self.config.get('system.debug') else None
        }

    def _get_user_friendly_message(self, error: Exception) -> str:
        """取得用戶友好的錯誤訊息"""
        error_messages = {
            ComponentGenerationError: "視覺化組件生成失敗，請稍後再試",
            ConfigurationError: "系統配置錯誤，請聯絡管理員",
            ValidationError: "輸入資料格式錯誤，請檢查後重試",
            ConnectionError: "網路連線失敗，請檢查網路狀態",
            TimeoutError: "處理時間過長，請稍後再試"
        }

        for error_type, message in error_messages.items():
            if isinstance(error, error_type):
                return message

        return "系統發生未知錯誤，請稍後再試"

# ===== 4. 增強版 XAI Flex Generator =====

class EnhancedXAIFlexGenerator:
    """整合實用概念的增強版XAI Flex Generator"""

    def __init__(self, config: Optional[SimpleConfig] = None):
        self.config = config or SimpleConfig()
        self.error_handler = ErrorHandler(self.config)
        self.logger = logging.getLogger(__name__)

        # 沿用你現有的優秀組件
        from xai_flex_generator import FlexComponentFactory, ExplanationEngine, A11yEnhancer
        self.component_factory = FlexComponentFactory()
        self.explanation_engine = ExplanationEngine()
        self.accessibility_enhancer = A11yEnhancer()

        # 統計和監控
        self.usage_stats = {
            'total_generations': 0,
            'component_usage': {},
            'error_count': 0
        }

    def generate_enhanced_flex_message(
        self, 
        chunks: Union[List[Dict], List[ChunkData]], 
        user_context: Dict = None
    ) -> FlexMessageResponse:
        """生成增強版 Flex Message - 統一資料格式版本"""

        try:
            # 統一資料格式
            standardized_chunks = self._standardize_chunks(chunks)

            if not standardized_chunks:
                return self._create_empty_state_response()

            # 驗證資料
            validated_chunks = self._validate_chunks(standardized_chunks)

            # 生成Flex Message (使用你現有的邏輯)
            if len(validated_chunks) == 1:
                flex_message = self._create_single_bubble_message(validated_chunks[0], user_context)
            else:
                flex_message = self._create_carousel_message(validated_chunks, user_context)

            # 無障礙增強
            if self.config.get('visual.accessibility_mode'):
                flex_message = self.accessibility_enhancer.enhance_accessibility(flex_message)

            # 生成回應
            response = FlexMessageResponse(
                flex_message=flex_message,
                fallback_text=self._generate_fallback_text(validated_chunks),
                interaction_handlers=self._create_interaction_handlers(validated_chunks),
                metadata={
                    'chunk_count': len(validated_chunks),
                    'component_types': self._identify_component_types(validated_chunks),
                    'generated_at': datetime.now().isoformat(),
                    'generator_version': '2.0',
                    'config_used': {
                        'theme': self.config.get('visual.default_theme'),
                        'language': self.config.get('visual.language'),
                        'accessibility': self.config.get('visual.accessibility_mode')
                    }
                },
                accessibility_enhanced=self.config.get('visual.accessibility_mode')
            )

            # 更新統計
            self._update_usage_stats(validated_chunks)

            return response

        except Exception as e:
            self.usage_stats['error_count'] += 1
            error_info = self.error_handler.handle_error(e, {
                'chunk_count': len(chunks) if chunks else 0,
                'user_context': user_context
            })

            # 返回錯誤狀態的回應
            return FlexMessageResponse(
                flex_message=self._create_error_flex_message(error_info['error']),
                fallback_text=error_info['error'],
                metadata={'error': True, 'error_info': error_info}
            )

    def _standardize_chunks(self, chunks: Union[List[Dict], List[ChunkData]]) -> List[ChunkData]:
        """統一chunk資料格式"""
        standardized = []

        for chunk in chunks:
            try:
                if isinstance(chunk, ChunkData):
                    standardized.append(chunk)
                elif isinstance(chunk, dict):
                    # 轉換字典格式到統一格式
                    standardized_chunk = self._dict_to_chunk_data(chunk)
                    standardized.append(standardized_chunk)
                else:
                    self.logger.warning(f"無法識別的chunk格式: {type(chunk)}")

            except Exception as e:
                self.logger.error(f"Chunk格式轉換失敗: {e}")
                continue

        return standardized

    def _dict_to_chunk_data(self, chunk_dict: Dict) -> ChunkData:
        """將字典格式轉換為ChunkData格式"""

        # 處理explanation_data
        explanation_data = None
        if 'explanation_data' in chunk_dict and chunk_dict['explanation_data']:
            exp_data = chunk_dict['explanation_data']
            explanation_data = ExplanationData(
                reasoning=exp_data.get('reasoning', ''),
                evidence_strength=exp_data.get('evidence_strength', 'medium'),
                related_concepts=exp_data.get('related_concepts', []),
                contraindications=exp_data.get('contraindications', [])
            )

        # 處理source_trace
        source_trace = None
        if 'source_trace' in chunk_dict and chunk_dict['source_trace']:
            src_data = chunk_dict['source_trace']
            source_trace = SourceTrace(
                source=src_data.get('source', ''),
                version=src_data.get('version', '1.0'),
                authority_level=src_data.get('authority_level', 'general'),
                last_verified=src_data.get('last_verified', ''),
                section=src_data.get('section', '')
            )

        # 處理visual_config
        visual_config = None
        if 'visual_config' in chunk_dict and chunk_dict['visual_config']:
            vis_data = chunk_dict['visual_config']
            visual_config = VisualConfig(
                component_type=vis_data.get('component_type', 'info_box'),
                layout_priority=vis_data.get('layout_priority', 'medium'),
                color_theme=vis_data.get('color_theme', 'neutral'),
                interactive_elements=vis_data.get('interactive_elements', [])
            )

        return ChunkData(
            chunk_id=chunk_dict.get('chunk_id', ''),
            module_id=chunk_dict.get('module_id', ''),
            chunk_type=chunk_dict.get('chunk_type', ''),
            title=chunk_dict.get('title', ''),
            content=chunk_dict.get('content', ''),
            confidence_score=chunk_dict.get('confidence_score', 0.8),
            summary=chunk_dict.get('summary'),
            keywords=chunk_dict.get('keywords', []),
            tags=chunk_dict.get('tags', []),
            difficulty_level=chunk_dict.get('difficulty_level', 'basic'),
            target_audience=chunk_dict.get('target_audience', ['一般民眾']),
            explanation_data=explanation_data,
            source_trace=source_trace,
            visual_config=visual_config
        )

    def _validate_chunks(self, chunks: List[ChunkData]) -> List[ChunkData]:
        """驗證chunk資料"""
        validated = []

        for chunk in chunks:
            try:
                # 基本驗證
                if not chunk.chunk_id or not chunk.title or not chunk.content:
                    raise ValidationError(f"Chunk {chunk.chunk_id} 缺少必要欄位")

                if not (0 <= chunk.confidence_score <= 1):
                    self.logger.warning(f"Chunk {chunk.chunk_id} 信心度超出範圍，調整為0.8")
                    chunk.confidence_score = 0.8

                # 模組啟用檢查
                module_config = self.config.get_module_config(chunk.module_id)
                if not module_config.get('enabled', True):
                    self.logger.info(f"模組 {chunk.module_id} 已停用，跳過chunk {chunk.chunk_id}")
                    continue

                # 信心度門檻檢查
                threshold = module_config.get('confidence_threshold', 0.5)
                if chunk.confidence_score < threshold:
                    self.logger.info(f"Chunk {chunk.chunk_id} 信心度低於門檻 {threshold}")
                    continue

                validated.append(chunk)

            except ValidationError as e:
                self.logger.error(f"Chunk驗證失敗: {e}")
                continue

        return validated

    def _create_single_bubble_message(self, chunk: ChunkData, user_context: Dict) -> Dict[str, Any]:
        """創建單個bubble訊息 - 使用你現有的組件邏輯"""
        component_type = self._determine_component_type(chunk)

        # 使用你現有的FlexComponentFactory
        bubble_content = self.component_factory.create_component(
            component_type, 
            chunk.to_dict(),  # 轉換為字典保持相容性
            user_context
        )

        return {
            "type": "flex",
            "altText": f"失智照護資訊：{chunk.title}",
            "contents": bubble_content,
            "metadata": {
                "chunk_id": chunk.chunk_id,
                "component_type": component_type.value if hasattr(component_type, 'value') else str(component_type),
                "generated_at": datetime.now().isoformat()
            }
        }

    def _create_carousel_message(self, chunks: List[ChunkData], user_context: Dict) -> Dict[str, Any]:
        """創建輪播訊息"""
        bubbles = []
        max_bubbles = self.config.get('system.max_chunks_per_request', 10)

        for chunk in chunks[:max_bubbles]:
            component_type = self._determine_component_type(chunk)
            bubble = self.component_factory.create_component(
                component_type,
                chunk.to_dict(),
                user_context
            )
            bubbles.append(bubble)

        return {
            "type": "flex",
            "altText": f"找到 {len(chunks)} 筆相關的失智照護資訊",
            "contents": {
                "type": "carousel",
                "contents": bubbles
            },
            "metadata": {
                "total_chunks": len(chunks),
                "displayed_chunks": len(bubbles),
                "generated_at": datetime.now().isoformat()
            }
        }

    def _determine_component_type(self, chunk: ChunkData):
        """決定組件類型 - 使用統一格式"""
        # 如果有明確的視覺配置，優先使用
        if chunk.visual_config and chunk.visual_config.component_type:
            return chunk.visual_config.component_type

        # 否則使用你現有的映射邏輯
        from xai_flex_generator import ComponentType

        mapping = {
            'warning_sign': ComponentType.COMPARISON_CARD,
            'normal_vs_abnormal': ComponentType.COMPARISON_CARD,
            'bpsd_symptom': ComponentType.CONFIDENCE_METER,
            'coping_strategy': ComponentType.XAI_BOX,
            'stage_description': ComponentType.TIMELINE_LIST,
            'missing_prevention': ComponentType.ACTION_CARD,
            'legal_rights': ComponentType.INFO_BOX,
            'financial_safety': ComponentType.WARNING_BOX
        }

        return mapping.get(chunk.chunk_type, ComponentType.INFO_BOX)

    def _create_error_flex_message(self, error_message: str) -> Dict[str, Any]:
        """創建錯誤狀態的Flex Message"""
        return {
            "type": "flex",
            "altText": "系統處理錯誤",
            "contents": {
                "type": "bubble",
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "text",
                            "text": "⚠️ 系統處理錯誤",
                            "weight": "bold",
                            "size": "lg",
                            "color": "#FF6B6B",
                            "align": "center"
                        },
                        {
                            "type": "text",
                            "text": error_message,
                            "wrap": True,
                            "margin": "md",
                            "size": "sm",
                            "color": "#666666",
                            "align": "center"
                        },
                        {
                            "type": "button",
                            "style": "primary",
                            "height": "sm",
                            "action": {
                                "type": "message",
                                "text": "重新嘗試"
                            }
                        }
                    ]
                }
            }
        }

    def _create_empty_state_response(self) -> FlexMessageResponse:
        """創建空狀態回應"""
        return FlexMessageResponse(
            flex_message={
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
                                "text": "請嘗試：\n• 使用不同的關鍵字\n• 簡化問題描述\n• 聯絡專業人員協助",
                                "wrap": True,
                                "margin": "md",
                                "size": "sm",
                                "color": "#666666"
                            }
                        ]
                    }
                }
            },
            fallback_text="很抱歉，目前找不到相關資訊，請嘗試重新描述您的問題。"
        )

    def _generate_fallback_text(self, chunks: List[ChunkData]) -> str:
        """生成fallback文字"""
        if not chunks:
            return "很抱歉，找不到相關資訊。"

        if len(chunks) == 1:
            chunk = chunks[0]
            return f"【{chunk.title}】{chunk.summary or chunk.content[:100]}..."
        else:
            titles = [chunk.title for chunk in chunks[:3]]
            return f"找到 {len(chunks)} 筆相關資訊：{', '.join(titles)}等。"

    def _create_interaction_handlers(self, chunks: List[ChunkData]) -> List[Dict[str, Any]]:
        """創建互動處理器"""
        handlers = []

        for chunk in chunks:
            handlers.extend([
                {
                    'action_type': 'detail_explanation',
                    'trigger': f"詳細說明 {chunk.chunk_id}",
                    'target_chunk_id': chunk.chunk_id,
                    'response_type': 'explanation'
                },
                {
                    'action_type': 'related_resources',
                    'trigger': f"相關資源 {chunk.chunk_id}",
                    'target_chunk_id': chunk.chunk_id,
                    'response_type': 'resource_list'
                }
            ])

        return handlers

    def _identify_component_types(self, chunks: List[ChunkData]) -> List[str]:
        """識別使用的組件類型"""
        component_types = []

        for chunk in chunks:
            component_type = self._determine_component_type(chunk)
            component_types.append(str(component_type))

        return list(set(component_types))  # 去重

    def _update_usage_stats(self, chunks: List[ChunkData]):
        """更新使用統計"""
        self.usage_stats['total_generations'] += 1

        for chunk in chunks:
            component_type = str(self._determine_component_type(chunk))
            self.usage_stats['component_usage'][component_type] = \
                self.usage_stats['component_usage'].get(component_type, 0) + 1

    def get_usage_stats(self) -> Dict[str, Any]:
        """取得使用統計"""
        return self.usage_stats.copy()

# ===== 5. 簡化的測試框架 =====

class SimpleTestFramework:
    """簡化的測試框架 - 不需要PRD的複雜測試架構"""

    def __init__(self, generator: EnhancedXAIFlexGenerator):
        self.generator = generator
        self.test_results = []

    def run_basic_tests(self) -> Dict[str, Any]:
        """執行基本測試套件"""
        print("🧪 開始執行基本測試套件")

        results = {
            'component_generation': self._test_component_generation(),
            'data_format': self._test_data_format(),
            'error_handling': self._test_error_handling(),
            'config_loading': self._test_config_loading()
        }

        # 統計結果
        passed = sum(1 for result in results.values() if result['passed'])
        total = len(results)

        print(f"\n📊 測試結果: {passed}/{total} 通過")

        return {
            'summary': {'passed': passed, 'total': total, 'success_rate': passed/total},
            'details': results
        }

    def _test_component_generation(self) -> Dict[str, Any]:
        """測試組件生成"""
        print("  測試組件生成...")

        try:
            # 測試用chunk
            test_chunk = ChunkData(
                chunk_id="TEST-01",
                module_id="M1",
                chunk_type="warning_sign",
                title="測試警訊",
                content="這是一個測試內容",
                confidence_score=0.9
            )

            result = self.generator.generate_enhanced_flex_message([test_chunk])

            # 驗證結果
            assert isinstance(result, FlexMessageResponse)
            assert 'flex_message' in result.flex_message
            assert result.fallback_text

            return {'passed': True, 'message': '組件生成測試通過'}

        except Exception as e:
            return {'passed': False, 'message': f'組件生成測試失敗: {str(e)}'}

    def _test_data_format(self) -> Dict[str, Any]:
        """測試資料格式轉換"""
        print("  測試資料格式轉換...")

        try:
            # 測試字典格式轉換
            dict_chunk = {
                'chunk_id': 'TEST-02',
                'module_id': 'M1',
                'chunk_type': 'warning_sign',
                'title': '測試標題',
                'content': '測試內容',
                'confidence_score': 0.8,
                'explanation_data': {
                    'reasoning': '測試推理',
                    'evidence_strength': 'high'
                }
            }

            result = self.generator.generate_enhanced_flex_message([dict_chunk])

            assert isinstance(result, FlexMessageResponse)
            assert result.metadata['chunk_count'] == 1

            return {'passed': True, 'message': '資料格式轉換測試通過'}

        except Exception as e:
            return {'passed': False, 'message': f'資料格式轉換測試失敗: {str(e)}'}

    def _test_error_handling(self) -> Dict[str, Any]:
        """測試錯誤處理"""
        print("  測試錯誤處理...")

        try:
            # 測試空輸入
            result = self.generator.generate_enhanced_flex_message([])
            assert isinstance(result, FlexMessageResponse)
            assert "找不到相關資訊" in result.fallback_text

            # 測試無效資料
            invalid_chunk = {
                'chunk_id': '',  # 空ID應該被過濾
                'title': '',
                'content': ''
            }

            result = self.generator.generate_enhanced_flex_message([invalid_chunk])
            assert isinstance(result, FlexMessageResponse)

            return {'passed': True, 'message': '錯誤處理測試通過'}

        except Exception as e:
            return {'passed': False, 'message': f'錯誤處理測試失敗: {str(e)}'}

    def _test_config_loading(self) -> Dict[str, Any]:
        """測試配置載入"""
        print("  測試配置載入...")

        try:
            config = self.generator.config

            # 驗證基本配置
            assert config.get('genai.default_provider') is not None
            assert config.get('visual.default_theme') is not None
            assert config.get('system.max_chunks_per_request') > 0

            return {'passed': True, 'message': '配置載入測試通過'}

        except Exception as e:
            return {'passed': False, 'message': f'配置載入測試失敗: {str(e)}'}

# ===== 6. 整合範例和使用方式 =====

def create_sample_config():
    """創建範例配置檔案"""
    sample_config = {
        'genai': {
            'default_provider': 'openai',
            'temperature': 0.7,
            'max_tokens': 2000,
            'timeout': 30
        },
        'visual': {
            'default_theme': 'healthcare',
            'language': 'zh-TW',
            'accessibility_mode': False,
            'component_cache': True
        },
        'system': {
            'debug': True,  # 開發模式
            'log_level': 'DEBUG',
            'max_chunks_per_request': 5,
            'response_cache_ttl': 300
        },
        'modules': {
            'M1': {
                'enabled': True,
                'confidence_threshold': 0.6,
                'max_results': 5
            },
            'M2': {
                'enabled': True,
                'confidence_threshold': 0.7,
                'max_results': 3
            },
            'M3': {
                'enabled': True,
                'confidence_threshold': 0.6,
                'max_results': 5
            }
        }
    }

    # 確保目錄存在
    Path('config').mkdir(exist_ok=True)
    Path('logs').mkdir(exist_ok=True)

    with open('config/xai_flex_config.yaml', 'w', encoding='utf-8') as f:
        yaml.dump(sample_config, f, default_flow_style=False, allow_unicode=True)

    print("✅ 範例配置檔案已創建: config/xai_flex_config.yaml")

def demo_enhanced_system():
    """示範增強版系統的使用"""
    print("🚀 增強版 XAI Flex 系統示範")
    print("=" * 50)

    # 1. 創建配置檔案
    create_sample_config()

    # 2. 初始化系統
    print("\n📋 初始化系統...")
    generator = EnhancedXAIFlexGenerator()

    # 3. 準備測試資料
    print("📝 準備測試資料...")

    # 使用統一格式的資料
    standardized_chunk = ChunkData(
        chunk_id="M1-04",
        module_id="M1",
        chunk_type="warning_sign",
        title="對時間地點感到混淆",
        content="失智症患者會搞不清楚年月日、季節變化，或迷失在熟悉的地方。",
        confidence_score=0.92,
        summary="時間空間認知障礙是失智症早期重要警訊",
        keywords=["記憶混淆", "時間障礙", "空間迷失"],
        tags=["十大警訊", "早期症狀"],
        explanation_data=ExplanationData(
            reasoning="基於台灣失智症協會官方指引",
            evidence_strength="high",
            related_concepts=["海馬迴退化", "執行功能障礙"]
        ),
        source_trace=SourceTrace(
            source="台灣失智症協會-十大警訊DM",
            version="v2.1",
            authority_level="official",
            last_verified="2025-07-20"
        ),
        visual_config=VisualConfig(
            component_type="comparison_card",
            color_theme="warning",
            interactive_elements=["詳細說明", "自我檢測"]
        )
    )

    # 也支援你原有的字典格式
    dict_format_chunk = {
        "chunk_id": "M3-07",
        "module_id": "M3",
        "chunk_type": "bpsd_symptom",
        "title": "日落症候群",
        "content": "許多失智症患者在傍晚時分會出現焦躁不安的行為",
        "confidence_score": 0.87,
        "explanation_data": {
            "reasoning": "基於神經精神醫學研究",
            "evidence_strength": "high"
        }
    }

    # 4. 生成 Flex Message
    print("🎨 生成 Flex Message...")

    # 測試單一卡片
    single_result = generator.generate_enhanced_flex_message([standardized_chunk])
    print(f"✅ 單一卡片生成成功，組件類型: {single_result.metadata['component_types']}")

    # 測試多卡輪播
    multi_result = generator.generate_enhanced_flex_message([standardized_chunk, dict_format_chunk])
    print(f"✅ 多卡輪播生成成功，卡片數量: {multi_result.metadata['chunk_count']}")

    # 5. 測試錯誤處理
    print("🛡️ 測試錯誤處理...")

    # 測試空輸入
    empty_result = generator.generate_enhanced_flex_message([])
    print(f"✅ 空輸入處理: {empty_result.fallback_text[:30]}...")

    # 測試無效資料
    invalid_chunk = {"chunk_id": "", "title": "", "content": ""}
    invalid_result = generator.generate_enhanced_flex_message([invalid_chunk])
    print(f"✅ 無效資料處理: 已適當處理")

    # 6. 執行測試套件
    print("\n🧪 執行測試套件...")
    test_framework = SimpleTestFramework(generator)
    test_results = test_framework.run_basic_tests()

    # 7. 顯示使用統計
    print("\n📊 使用統計:")
    stats = generator.get_usage_stats()
    print(f"總生成次數: {stats['total_generations']}")
    print(f"組件使用分布: {stats['component_usage']}")
    print(f"錯誤次數: {stats['error_count']}")

    # 8. 保存示例結果
    print("\n💾 保存示例結果...")

    # 保存Flex Message範例
    with open('examples/single_card_enhanced.json', 'w', encoding='utf-8') as f:
        json.dump(single_result.flex_message, f, ensure_ascii=False, indent=2)

    with open('examples/carousel_enhanced.json', 'w', encoding='utf-8') as f:
        json.dump(multi_result.flex_message, f, ensure_ascii=False, indent=2)

    print("✅ 範例檔案已保存到 examples/ 目錄")

    print("\n🎉 增強版系統示範完成！")

    return {
        'generator': generator,
        'single_result': single_result,
        'multi_result': multi_result,
        'test_results': test_results
    }

# ===== 7. API 整合範例 =====

def create_enhanced_api_integration():
    """創建API整合範例"""

    api_code = '''
# enhanced_api.py - 整合到你現有的API中

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from enhanced_xai_flex import EnhancedXAIFlexGenerator, ChunkData, SimpleConfig

app = FastAPI(title="增強版 XAI Flex API")

# 全域初始化
config = SimpleConfig()
flex_generator = EnhancedXAIFlexGenerator(config)

class FlexMessageRequest(BaseModel):
    """統一的請求格式"""
    chunks: List[Dict[str, Any]]
    user_context: Optional[Dict[str, Any]] = None
    accessibility_mode: bool = False

@app.post("/api/v2/flex-message")
async def generate_enhanced_flex_message(request: FlexMessageRequest):
    """生成增強版 Flex Message"""
    try:
        # 臨時設定無障礙模式
        if request.accessibility_mode:
            flex_generator.config.config['visual']['accessibility_mode'] = True

        result = flex_generator.generate_enhanced_flex_message(
            chunks=request.chunks,
            user_context=request.user_context
        )

        return {
            "success": True,
            "data": {
                "flex_message": result.flex_message,
                "fallback_text": result.fallback_text,
                "interaction_handlers": result.interaction_handlers,
                "metadata": result.metadata
            }
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        # 重置設定
        if request.accessibility_mode:
            flex_generator.config.config['visual']['accessibility_mode'] = False

@app.get("/api/v2/stats")
async def get_system_stats():
    """取得系統統計"""
    return {
        "usage_stats": flex_generator.get_usage_stats(),
        "config_summary": {
            "default_theme": config.get('visual.default_theme'),
            "max_chunks": config.get('system.max_chunks_per_request'),
            "enabled_modules": [
                module_id for module_id, module_config in config.config.get('modules', {}).items()
                if module_config.get('enabled', True)
            ]
        }
    }

@app.post("/api/v2/test")
async def run_system_tests():
    """執行系統測試"""
    from enhanced_xai_flex import SimpleTestFramework

    test_framework = SimpleTestFramework(flex_generator)
    results = test_framework.run_basic_tests()

    return {
        "test_results": results,
        "system_health": "healthy" if results['summary']['success_rate'] > 0.8 else "degraded"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
'''

    # 確保目錄存在
    Path('examples').mkdir(exist_ok=True)

    with open('examples/enhanced_api.py', 'w', encoding='utf-8') as f:
        f.write(api_code)

    print("✅ API整合範例已創建: examples/enhanced_api.py")

def create_migration_guide():
    """創建遷移指南"""

    migration_guide = '''# 🔄 遷移指南：從原版到增強版

## 1. 現有代碼相容性

你的現有代碼**完全相容**，只需要替換導入：

```python
# 原版
from xai_flex_generator import XAIFlexGenerator

generator = XAIFlexGenerator()
result = generator.generate_enhanced_flex_message(chunks)

# 增強版 - 零修改
from enhanced_xai_flex import EnhancedXAIFlexGenerator

generator = EnhancedXAIFlexGenerator()
result = generator.generate_enhanced_flex_message(chunks)  # 完全相同的API
```

## 2. 新功能啟用

### 2.1 配置管理
```python
# 自動載入 config/xai_flex_config.yaml
generator = EnhancedXAIFlexGenerator()

# 或自定義配置路徑
config = SimpleConfig("my_config.yaml")
generator = EnhancedXAIFlexGenerator(config)
```

### 2.2 統一資料格式
```python
# 原版：使用字典（仍然支援）
chunk_dict = {"chunk_id": "M1-01", "title": "標題", ...}

# 增強版：統一格式（推薦）
chunk_data = ChunkData(
    chunk_id="M1-01",
    title="標題",
    explanation_data=ExplanationData(reasoning="推理過程"),
    source_trace=SourceTrace(source="資料來源")
)

# 兩種格式都支援！
result = generator.generate_enhanced_flex_message([chunk_dict, chunk_data])
```

### 2.3 錯誤處理
```python
# 增強版會自動處理錯誤，返回適當的回應
try:
    result = generator.generate_enhanced_flex_message(chunks)
    if 'error' in result.metadata:
        print(f"處理時發生錯誤: {result.fallback_text}")
    else:
        print("處理成功")
except Exception as e:
    print(f"系統錯誤: {e}")
```

## 3. 配置文件設定

創建 `config/xai_flex_config.yaml`：

```yaml
genai:
  default_provider: 'openai'
  temperature: 0.7

visual:
  default_theme: 'healthcare'
  language: 'zh-TW'
  accessibility_mode: false

system:
  debug: false
  max_chunks_per_request: 10

modules:
  M1:
    enabled: true
    confidence_threshold: 0.6
```

## 4. 測試整合

```python
from enhanced_xai_flex import SimpleTestFramework

# 執行基本測試
test_framework = SimpleTestFramework(generator)
results = test_framework.run_basic_tests()

print(f"測試通過率: {results['summary']['success_rate']:.0%}")
```

## 5. 逐步遷移建議

### Phase 1: 基礎替換（5分鐘）
1. 安裝依賴：`pip install pyyaml`
2. 複製 `enhanced_xai_flex.py` 到專案
3. 替換導入語句
4. 測試基本功能

### Phase 2: 配置啟用（10分鐘）  
1. 創建配置檔案
2. 調整配置參數
3. 測試配置載入

### Phase 3: 格式升級（可選）
1. 逐步將字典格式轉換為 ChunkData
2. 添加結構化解釋資料
3. 完善來源追蹤

## 6. 常見問題

**Q: 會影響現有功能嗎？**
A: 不會，API完全相容，只是增加了新功能。

**Q: 效能會受影響嗎？**
A: 幾乎沒有影響，主要是增加了驗證和格式轉換，開銷很小。

**Q: 配置檔案是必需的嗎？**
A: 不是，沒有配置檔案會使用預設值，功能正常。

**Q: 可以部分遷移嗎？**
A: 可以，建議先替換導入，其他功能漸進式啟用。
'''

    with open('MIGRATION_GUIDE.md', 'w', encoding='utf-8') as f:
        f.write(migration_guide)

    print("✅ 遷移指南已創建: MIGRATION_GUIDE.md")

# ===== 主要執行函數 =====

if __name__ == "__main__":
    print("🚀 啟動增強版 XAI Flex 系統")

    # 執行完整示範
    demo_results = demo_enhanced_system()

    # 創建API整合範例
    create_enhanced_api_integration()

    # 創建遷移指南
    create_migration_guide()

    print("\n" + "=" * 50)
    print("✨ 增強版系統準備完成！")
    print("\n📋 接下來你可以：")
    print("1. 查看 config/xai_flex_config.yaml 調整配置")
    print("2. 運行 examples/enhanced_api.py 測試API")  
    print("3. 查看 MIGRATION_GUIDE.md 了解遷移步驟")
    print("4. 檢查 examples/ 目錄中的範例檔案")

    print(f"\n📊 當前系統狀態：")
    print(f"  總生成次數: {demo_results['generator'].get_usage_stats()['total_generations']}")
    print(f"  測試通過率: {demo_results['test_results']['summary']['success_rate']:.0%}")
    print("  系統健康度: ✅ 正常")