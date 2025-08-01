"""
M1 十大警訊比對卡 - 系統整合模組
整合 M1 增強版視覺化與現有 XAI Flex 系統
"""

from typing import Dict, List, Any, Optional, Union
import yaml
import json
import logging
from datetime import datetime
from pathlib import Path
from safe_enum_handler import safe_enum_value

# Import existing modules
try:
    from .m1_enhanced_visualization import (
        M1EnhancedVisualizationGenerator,
        DesignTokens,
        WarningLevel
    )
    from .enhanced_xai_flex import (
        EnhancedXAIFlexGenerator,
        ChunkData,
        FlexMessageResponse,
        SimpleConfig
    )
except ImportError:
    # Fallback for direct execution
    from m1_enhanced_visualization import (
        M1EnhancedVisualizationGenerator,
        DesignTokens,
        WarningLevel
    )
    from enhanced_xai_flex import (
        EnhancedXAIFlexGenerator,
        ChunkData,
        FlexMessageResponse,
        SimpleConfig
    )

class M1IntegrationManager:
    """M1 整合管理器"""
    
    def __init__(self, config_path: str = "config/m1_config.yaml"):
        self.logger = logging.getLogger(__name__)
        self.config = self._load_m1_config(config_path)
        self.m1_generator = M1EnhancedVisualizationGenerator()
        self.enhanced_generator = EnhancedXAIFlexGenerator()
        
    def _load_m1_config(self, config_path: str) -> Dict[str, Any]:
        """載入 M1 配置"""
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        except Exception as e:
            self.logger.error(f"載入 M1 配置失敗: {e}")
            return self._get_default_config()
    
    def _get_default_config(self) -> Dict[str, Any]:
        """取得預設配置"""
        return {
            "module": {
                "name": "M1",
                "version": "1.0.0"
            },
            "design_tokens": {
                "colors": DesignTokens.COLORS,
                "typography": DesignTokens.TYPOGRAPHY,
                "spacing": DesignTokens.SPACING
            }
        }
    
    def process_m1_analysis(
        self,
        user_input: str,
        analysis_data: Dict[str, Any],
        user_context: Dict = None
    ) -> FlexMessageResponse:
        """處理 M1 分析並生成視覺化回應"""
        
        try:
            # 1. 驗證分析資料
            validated_data = self._validate_analysis_data(analysis_data)
            
            # 2. 生成 M1 專用視覺化
            m1_flex_message = self.m1_generator.generate_m1_flex_message(
                validated_data,
                user_context
            )
            
            # 3. 生成標準化回應
            response = FlexMessageResponse(
                flex_message=m1_flex_message,
                fallback_text=self._generate_m1_fallback_text(validated_data),
                interaction_handlers=self._create_m1_interaction_handlers(validated_data),
                metadata={
                    'module': 'M1',
                    'confidence_score': validated_data.get('confidence_score', 0.0),
                    'warning_level': safe_enum_value(validated_data.get('warning_level', WarningLevel.NORMAL), 'normal'),
                    'generated_at': datetime.now().isoformat(),
                    'integration_version': '1.0.0'
                },
                accessibility_enhanced=self.config.get('accessibility', {}).get('enabled', True)
            )
            
            self.logger.info(f"M1 分析處理完成，信心度: {validated_data.get('confidence_score', 0.0)}")
            return response
            
        except Exception as e:
            self.logger.error(f"M1 分析處理失敗: {e}")
            return self._create_error_response(str(e))
    
    def process_m1_batch_analysis(
        self,
        analysis_results: List[Dict[str, Any]],
        user_context: Dict = None
    ) -> FlexMessageResponse:
        """處理 M1 批次分析"""
        
        try:
            # 驗證所有分析結果
            validated_results = [
                self._validate_analysis_data(result) 
                for result in analysis_results
            ]
            
            # 生成輪播訊息
            carousel_message = self.m1_generator.generate_m1_carousel(
                validated_results,
                user_context
            )
            
            # 生成回應
            response = FlexMessageResponse(
                flex_message=carousel_message,
                fallback_text=self._generate_m1_batch_fallback_text(validated_results),
                interaction_handlers=self._create_m1_batch_interaction_handlers(validated_results),
                metadata={
                    'module': 'M1',
                    'result_count': len(validated_results),
                    'generated_at': datetime.now().isoformat(),
                    'integration_version': '1.0.0'
                },
                accessibility_enhanced=self.config.get('accessibility', {}).get('enabled', True)
            )
            
            self.logger.info(f"M1 批次分析處理完成，結果數量: {len(validated_results)}")
            return response
            
        except Exception as e:
            self.logger.error(f"M1 批次分析處理失敗: {e}")
            return self._create_error_response(str(e))
    
    def _validate_analysis_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """驗證分析資料"""
        required_fields = ['confidence_score', 'comparison_data', 'key_finding']
        
        for field in required_fields:
            if field not in data:
                raise ValueError(f"缺少必要欄位: {field}")
        
        # 確保信心度在有效範圍內
        confidence = data.get('confidence_score', 0.0)
        if not 0.0 <= confidence <= 1.0:
            data['confidence_score'] = max(0.0, min(1.0, confidence))
        
        # 確保警告等級有效
        warning_level = data.get('warning_level', WarningLevel.NORMAL)
        if isinstance(warning_level, str):
            try:
                data['warning_level'] = WarningLevel(warning_level)
            except ValueError:
                data['warning_level'] = WarningLevel.NORMAL
        
        return data
    
    def _generate_m1_fallback_text(self, analysis_data: Dict[str, Any]) -> str:
        """生成 M1 後備文字"""
        confidence = int(analysis_data.get('confidence_score', 0.0) * 100)
        key_finding = analysis_data.get('key_finding', '')
        warning_level = analysis_data.get('warning_level', WarningLevel.NORMAL)
        
        level_text = {
            WarningLevel.NORMAL: "正常",
            WarningLevel.CAUTION: "注意",
            WarningLevel.WARNING: "警告"
        }.get(warning_level, "正常")
        
        return f"AI 分析結果 ({level_text})\n信心度: {confidence}%\n{key_finding}"
    
    def _generate_m1_batch_fallback_text(self, analysis_results: List[Dict[str, Any]]) -> str:
        """生成 M1 批次後備文字"""
        if not analysis_results:
            return "沒有找到相關分析結果"
        
        texts = []
        for i, result in enumerate(analysis_results, 1):
            confidence = int(result.get('confidence_score', 0.0) * 100)
            key_finding = result.get('key_finding', '')
            texts.append(f"{i}. 信心度 {confidence}%: {key_finding}")
        
        return f"AI 分析結果 ({len(analysis_results)} 項):\n" + "\n".join(texts)
    
    def _create_m1_interaction_handlers(self, analysis_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """創建 M1 互動處理器"""
        handlers = [
            {
                "type": "postback",
                "label": "查看詳細分析",
                "data": f"m1_detail_{analysis_data.get('confidence_score', 0.0)}"
            },
            {
                "type": "postback",
                "label": "提供回饋",
                "data": "m1_feedback"
            }
        ]
        
        # 根據警告等級添加特定處理器
        warning_level = analysis_data.get('warning_level', WarningLevel.NORMAL)
        if warning_level in [WarningLevel.CAUTION, WarningLevel.WARNING]:
            handlers.append({
                "type": "postback",
                "label": "尋求專業協助",
                "data": "m1_professional_help"
            })
        
        return handlers
    
    def _create_m1_batch_interaction_handlers(self, analysis_results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """創建 M1 批次互動處理器"""
        return [
            {
                "type": "postback",
                "label": "查看所有詳細分析",
                "data": f"m1_batch_detail_{len(analysis_results)}"
            },
            {
                "type": "postback",
                "label": "提供回饋",
                "data": "m1_batch_feedback"
            }
        ]
    
    def _create_error_response(self, error_message: str) -> FlexMessageResponse:
        """創建錯誤回應"""
        error_flex = {
            "type": "flex",
            "altText": "分析暫時無法使用",
            "contents": {
                "type": "bubble",
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "text",
                            "text": "⚠️ 暫時無法分析",
                            "size": "lg",
                            "weight": "bold",
                            "color": DesignTokens.COLORS['warning']
                        },
                        {
                            "type": "text",
                            "text": "請稍後再試",
                            "size": "sm",
                            "color": DesignTokens.COLORS['text_secondary'],
                            "margin": "sm"
                        }
                    ]
                }
            }
        }
        
        return FlexMessageResponse(
            flex_message=error_flex,
            fallback_text="分析暫時無法使用，請稍後再試",
            interaction_handlers=[],
            metadata={
                'module': 'M1',
                'error': error_message,
                'generated_at': datetime.now().isoformat()
            }
        )

class M1DataAdapter:
    """M1 資料適配器"""
    
    @staticmethod
    def adapt_chunk_to_m1_analysis(chunk: ChunkData) -> Dict[str, Any]:
        """將 ChunkData 適配為 M1 分析格式"""
        return {
            "confidence_score": chunk.confidence_score,
            "comparison_data": {
                "normal_aging": chunk.content[:100] + "..." if len(chunk.content) > 100 else chunk.content,
                "dementia_warning": chunk.summary or "需要進一步評估"
            },
            "key_finding": chunk.title,
            "warning_level": M1DataAdapter._determine_warning_level(chunk.confidence_score)
        }
    
    @staticmethod
    def _determine_warning_level(confidence_score: float) -> WarningLevel:
        """根據信心度確定警告等級"""
        if confidence_score >= 0.8:
            return WarningLevel.NORMAL
        elif confidence_score >= 0.6:
            return WarningLevel.CAUTION
        else:
            return WarningLevel.WARNING

# ===== 測試與示範 =====

def demo_m1_integration():
    """示範 M1 整合功能"""
    integration_manager = M1IntegrationManager()
    
    # 範例分析資料
    sample_analysis = {
        "confidence_score": 0.85,
        "comparison_data": {
            "normal_aging": "偶爾忘記鑰匙位置，但能回想起來",
            "dementia_warning": "經常忘記重要約會，且無法回想"
        },
        "key_finding": "記憶力衰退模式符合輕度認知障礙徵兆",
        "warning_level": WarningLevel.CAUTION
    }
    
    # 處理單一分析
    response = integration_manager.process_m1_analysis(
        user_input="記憶力問題",
        analysis_data=sample_analysis
    )
    
    print("=== M1 整合測試結果 ===")
    print(f"模組: {response.metadata.get('module')}")
    print(f"信心度: {response.metadata.get('confidence_score')}")
    print(f"警告等級: {response.metadata.get('warning_level')}")
    print(f"後備文字: {response.fallback_text}")
    print(f"互動處理器數量: {len(response.interaction_handlers)}")

if __name__ == "__main__":
    demo_m1_integration() 