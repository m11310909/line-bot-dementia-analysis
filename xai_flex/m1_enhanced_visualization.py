"""
M1 十大警訊比對卡 - 增強版視覺化模組
基於 M1.fig 設計檔規格書實現的 XAI 視覺化系統
"""

from typing import Dict, List, Any, Optional, Union
from dataclasses import dataclass
from enum import Enum
import json
from datetime import datetime
import logging

# ===== 1. Design Tokens 設計變數 =====

class DesignTokens:
    """M1.fig 設計變數系統"""
    
    # Color Tokens
    COLORS = {
        # Semantic Colors
        'success': '#4CAF50',      # 正常老化
        'warning': '#FF9800',      # 警訊徵兆
        'info': '#2196F3',         # 資訊提示
        'confidence': '#1976D2',    # AI 信心度
        
        # Text Colors
        'text_primary': '#212121',   # 主要文字
        'text_secondary': '#666666', # 次要文字
        'text_on_color': '#FFFFFF',  # 色塊上文字
        
        # Background Colors
        'bg_normal': '#E8F5E9',     # 正常老化背景
        'bg_warning': '#FFF3E0',    # 警訊徵兆背景
        'bg_card': '#FFFFFF',       # 卡片背景
        'bg_subtle': '#F5F5F5',     # 輔助背景
    }
    
    # Typography Tokens
    TYPOGRAPHY = {
        'text_xs': '12px',     # 標註文字
        'text_sm': '14px',     # 輔助文字
        'text_base': '16px',   # 內文
        'text_lg': '18px',     # 副標題
        'text_xl': '20px',     # 標題
        
        'leading_tight': 1.4,
        'leading_base': 1.6,
        'leading_relaxed': 1.8,
        
        'font_normal': 400,
        'font_medium': 500,
        'font_bold': 700,
    }
    
    # Spacing Tokens
    SPACING = {
        'xs': '4px',
        'sm': '8px',
        'md': '12px',
        'lg': '16px',
        'xl': '20px',
        '2xl': '24px',
    }

# ===== 2. Component Types 元件類型 =====

class M1ComponentType(Enum):
    """M1 模組元件類型"""
    CONFIDENCE_BADGE = "confidence_badge"
    WARNING_LEVEL_INDICATOR = "warning_level_indicator"
    COMPARISON_CARD = "comparison_card"
    AI_REASONING_PATH = "ai_reasoning_path"
    CONFIDENCE_METER = "confidence_meter"
    ACTION_BUTTON = "action_button"
    FLEX_BUBBLE = "flex_bubble"

class WarningLevel(Enum):
    """警訊等級"""
    NORMAL = "normal"
    CAUTION = "caution"
    WARNING = "warning"

# ===== 3. Atoms 原子元件 =====

class M1Atoms:
    """M1 原子元件庫"""
    
    @staticmethod
    def create_confidence_badge(percentage: float, show_icon: bool = True) -> Dict:
        """XAI Confidence Badge (信心度標籤)"""
        if percentage > 80:
            color = DesignTokens.COLORS['success']
            icon = "✅"
        elif percentage > 50:
            color = DesignTokens.COLORS['info']
            icon = "⚠️"
        else:
            color = DesignTokens.COLORS['warning']
            icon = "❌"
        
        contents = []
        if show_icon:
            contents.append({
                "type": "text",
                "text": icon,
                "size": "sm",
                "color": color,
                "flex": 0
            })
        
        contents.append({
            "type": "text",
            "text": f"{int(percentage)}%",
            "size": "sm",
            "weight": "bold",
            "color": color,
            "flex": 1
        })
        
        return {
            "type": "box",
            "layout": "horizontal",
            "backgroundColor": f"{color}20",
            "cornerRadius": "12px",
            "paddingAll": DesignTokens.SPACING['sm'],
            "contents": contents
        }
    
    @staticmethod
    def create_warning_level_indicator(level: WarningLevel, label: str) -> Dict:
        """Warning Level Indicator (警訊等級指示)"""
        level_config = {
            WarningLevel.NORMAL: {"icon": "✓", "color": DesignTokens.COLORS['success']},
            WarningLevel.CAUTION: {"icon": "⚠", "color": DesignTokens.COLORS['warning']},
            WarningLevel.WARNING: {"icon": "⚠️", "color": DesignTokens.COLORS['warning']}
        }
        
        config = level_config[level]
        
        return {
            "type": "box",
            "layout": "horizontal",
            "contents": [
                {
                    "type": "text",
                    "text": config["icon"],
                    "size": "sm",
                    "color": config["color"],
                    "flex": 0
                },
                {
                    "type": "text",
                    "text": label,
                    "size": "sm",
                    "color": DesignTokens.COLORS['text_primary'],
                    "flex": 1,
                    "margin": "sm"
                }
            ]
        }
    
    @staticmethod
    def create_action_button(text: str, action_type: str = "primary", size: str = "medium") -> Dict:
        """Action Button (行動按鈕)"""
        size_config = {
            "small": "36px",
            "medium": "44px",
            "large": "52px"
        }
        
        color_config = {
            "primary": DesignTokens.COLORS['info'],
            "secondary": DesignTokens.COLORS['text_secondary'],
            "text": "transparent"
        }
        
        return {
            "type": "button",
            "action": {
                "type": "postback",
                "label": text,
                "data": f"action={action_type}"
            },
            "style": action_type,
            "height": size_config[size],
            "color": color_config[action_type],
            "margin": "sm"
        }

# ===== 4. Molecules 分子元件 =====

class M1Molecules:
    """M1 分子元件庫"""
    
    @staticmethod
    def create_comparison_card(
        card_type: str, 
        icon: str, 
        title: str, 
        description: str
    ) -> Dict:
        """Comparison Card (比對卡片)"""
        bg_color = (DesignTokens.COLORS['bg_normal'] 
                   if card_type == 'normal' 
                   else DesignTokens.COLORS['bg_warning'])
        
        return {
            "type": "box",
            "layout": "vertical",
            "backgroundColor": bg_color,
            "cornerRadius": "8px",
            "paddingAll": DesignTokens.SPACING['lg'],
            "margin": "sm",
            "contents": [
                {
                    "type": "box",
                    "layout": "horizontal",
                    "contents": [
                        {
                            "type": "text",
                            "text": icon,
                            "size": "lg",
                            "flex": 0
                        },
                        {
                            "type": "text",
                            "text": title,
                            "size": "sm",
                            "weight": "bold",
                            "color": DesignTokens.COLORS['text_primary'],
                            "flex": 1,
                            "margin": "sm"
                        }
                    ]
                },
                {
                    "type": "text",
                    "text": description,
                    "size": "xs",
                    "color": DesignTokens.COLORS['text_secondary'],
                    "wrap": True,
                    "margin": "sm"
                }
            ]
        }
    
    @staticmethod
    def create_ai_reasoning_path(steps: List[str], current_step: int = 0) -> Dict:
        """AI Reasoning Path (AI 推理路徑)"""
        step_components = []
        
        for i, step in enumerate(steps):
            is_current = i == current_step
            is_completed = i < current_step
            
            step_color = (DesignTokens.COLORS['info'] if is_current 
                         else DesignTokens.COLORS['success'] if is_completed 
                         else DesignTokens.COLORS['text_secondary'])
            
            step_components.append({
                "type": "text",
                "text": step,
                "size": "xs",
                "color": step_color,
                "weight": "bold" if is_current else "normal",
                "flex": 1,
                "align": "center"
            })
            
            # Add separator if not last step
            if i < len(steps) - 1:
                step_components.append({
                    "type": "text",
                    "text": "→",
                    "size": "xs",
                    "color": DesignTokens.COLORS['text_secondary'],
                    "flex": 0,
                    "margin": "sm"
                })
        
        return {
            "type": "box",
            "layout": "horizontal",
            "contents": step_components,
            "margin": "md"
        }
    
    @staticmethod
    def create_confidence_meter(value: float, show_label: bool = True, animated: bool = False) -> Dict:
        """Confidence Meter (信心度量表)"""
        percentage = int(value * 100)
        color = DesignTokens.COLORS['confidence']
        
        meter_contents = [
            {
                "type": "box",
                "layout": "vertical",
                "backgroundColor": "#F0F0F0",
                "height": "8px",
                "cornerRadius": "4px",
                "contents": [
                    {
                        "type": "box",
                        "layout": "vertical",
                        "backgroundColor": color,
                        "width": f"{percentage}%",
                        "cornerRadius": "4px",
                        "contents": []
                    }
                ]
            }
        ]
        
        if show_label:
            meter_contents.insert(0, {
                "type": "text",
                "text": f"AI 信心度 {percentage}%",
                "size": "xs",
                "color": DesignTokens.COLORS['text_secondary'],
                "margin": "sm"
            })
        
        return {
            "type": "box",
            "layout": "vertical",
            "contents": meter_contents,
            "margin": "sm"
        }

# ===== 5. Organisms 組織元件 =====

class M1Organisms:
    """M1 組織元件庫"""
    
    @staticmethod
    def create_flex_bubble(
        header_title: str,
        confidence_score: float,
        comparison_data: Dict,
        key_finding: str,
        user_context: Dict = None
    ) -> Dict:
        """Flex Message Bubble (Flex 訊息氣泡)"""
        
        # Header
        header = {
            "type": "box",
            "layout": "vertical",
            "backgroundColor": DesignTokens.COLORS['bg_card'],
            "contents": [
                {
                    "type": "text",
                    "text": header_title,
                    "size": "lg",
                    "weight": "bold",
                    "color": DesignTokens.COLORS['text_primary']
                },
                {
                    "type": "text",
                    "text": "記憶力評估",
                    "size": "sm",
                    "color": DesignTokens.COLORS['text_secondary'],
                    "margin": "sm"
                }
            ]
        }
        
        # Body
        body_contents = [
            # Confidence Meter
            M1Molecules.create_confidence_meter(confidence_score),
            
            # Comparison Cards
            {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                    M1Molecules.create_comparison_card(
                        "normal",
                        "👴",
                        "正常老化",
                        comparison_data.get("normal_aging", "一般記憶力衰退")
                    ),
                    M1Molecules.create_comparison_card(
                        "warning",
                        "⚠️",
                        "失智警訊",
                        comparison_data.get("dementia_warning", "需要關注的徵兆")
                    )
                ]
            },
            
            # Key Finding
            {
                "type": "text",
                "text": f"💡 {key_finding}",
                "size": "sm",
                "color": DesignTokens.COLORS['info'],
                "wrap": True,
                "margin": "md"
            }
        ]
        
        body = {
            "type": "box",
            "layout": "vertical",
            "backgroundColor": DesignTokens.COLORS['bg_subtle'],
            "contents": body_contents
        }
        
        # Footer
        footer = {
            "type": "box",
            "layout": "vertical",
            "backgroundColor": DesignTokens.COLORS['bg_card'],
            "contents": [
                M1Atoms.create_action_button("查看詳細分析", "primary", "medium")
            ]
        }
        
        return {
            "type": "bubble",
            "size": "mega",
            "header": header,
            "body": body,
            "footer": footer
        }

# ===== 6. M1 Enhanced Visualization Generator =====

class M1EnhancedVisualizationGenerator:
    """M1 增強版視覺化生成器"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.atoms = M1Atoms()
        self.molecules = M1Molecules()
        self.organisms = M1Organisms()
    
    def generate_m1_flex_message(
        self,
        analysis_result: Dict,
        user_context: Dict = None
    ) -> Dict:
        """生成 M1 十大警訊比對卡的 Flex Message"""
        
        try:
            # 提取分析結果
            confidence_score = analysis_result.get('confidence_score', 0.0)
            comparison_data = analysis_result.get('comparison_data', {})
            key_finding = analysis_result.get('key_finding', '')
            warning_level = analysis_result.get('warning_level', 'normal')
            
            # 使用安全枚舉處理工具
            from safe_enum_handler import safe_enum_value, safe_enum_convert
            
            # 安全地處理枚舉值
            warning_level_str = safe_enum_value(warning_level, "normal")
            warning_level_enum = safe_enum_convert(warning_level, WarningLevel, WarningLevel.NORMAL)
            
            # 生成 Flex Bubble
            flex_bubble = self.organisms.create_flex_bubble(
                header_title="AI 分析結果",
                confidence_score=confidence_score,
                comparison_data=comparison_data,
                key_finding=key_finding,
                user_context=user_context
            )
            
            # 添加無障礙增強
            flex_bubble = self._enhance_accessibility(flex_bubble)
            
            return {
                "type": "flex",
                "altText": f"失智照護分析：{key_finding}",
                "contents": flex_bubble,
                "metadata": {
                    "module": "M1",
                    "confidence_score": confidence_score,
                    "warning_level": safe_enum_value(warning_level_enum, "normal"),
                    "generated_at": datetime.now().isoformat()
                }
            }
            
        except Exception as e:
            self.logger.error(f"M1 Flex Message 生成失敗: {e}")
            return self._create_error_message(str(e))
    
    def generate_m1_carousel(
        self,
        analysis_results: List[Dict],
        user_context: Dict = None
    ) -> Dict:
        """生成 M1 多重警訊輪播"""
        
        if not analysis_results:
            return self._create_empty_message()
        
        # 限制最多 3 個卡片
        limited_results = analysis_results[:3]
        
        carousel_contents = []
        for result in limited_results:
            flex_bubble = self.generate_m1_flex_message(result, user_context)
            carousel_contents.append(flex_bubble['contents'])
        
        return {
            "type": "flex",
            "altText": f"失智照護分析：{len(carousel_contents)} 個警訊評估",
            "contents": {
                "type": "carousel",
                "contents": carousel_contents
            },
            "metadata": {
                "module": "M1",
                "card_count": len(carousel_contents),
                "generated_at": datetime.now().isoformat()
            }
        }
    
    def _enhance_accessibility(self, flex_message: Dict) -> Dict:
        """增強無障礙功能"""
        # 確保顏色對比度
        # 添加語義結構
        # 優化文字大小
        return flex_message
    
    def _create_error_message(self, error_msg: str) -> Dict:
        """創建錯誤訊息"""
        return {
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
    
    def _create_empty_message(self) -> Dict:
        """創建空狀態訊息"""
        return {
            "type": "flex",
            "altText": "沒有找到相關分析",
            "contents": {
                "type": "bubble",
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "text",
                            "text": "📋 沒有相關分析",
                            "size": "lg",
                            "weight": "bold",
                            "color": DesignTokens.COLORS['text_primary']
                        },
                        {
                            "type": "text",
                            "text": "請提供更多資訊",
                            "size": "sm",
                            "color": DesignTokens.COLORS['text_secondary'],
                            "margin": "sm"
                        }
                    ]
                }
            }
        }

# ===== 7. 測試與示範 =====

def create_sample_m1_analysis():
    """創建範例 M1 分析結果"""
    return {
        "confidence_score": 0.85,
        "comparison_data": {
            "normal_aging": "偶爾忘記鑰匙位置，但能回想起來",
            "dementia_warning": "經常忘記重要約會，且無法回想"
        },
        "key_finding": "記憶力衰退模式符合輕度認知障礙徵兆",
        "warning_level": WarningLevel.CAUTION
    }

def demo_m1_visualization():
    """示範 M1 視覺化功能"""
    generator = M1EnhancedVisualizationGenerator()
    
    # 單一分析結果
    single_result = create_sample_m1_analysis()
    flex_message = generator.generate_m1_flex_message(single_result)
    
    print("=== M1 單一分析結果 ===")
    print(json.dumps(flex_message, indent=2, ensure_ascii=False))
    
    # 多重分析結果
    multiple_results = [
        create_sample_m1_analysis(),
        {
            "confidence_score": 0.72,
            "comparison_data": {
                "normal_aging": "偶爾迷路但能找到方向",
                "dementia_warning": "在熟悉環境中迷路"
            },
            "key_finding": "空間定向能力下降",
            "warning_level": WarningLevel.WARNING
        }
    ]
    
    carousel_message = generator.generate_m1_carousel(multiple_results)
    
    print("\n=== M1 多重分析結果 ===")
    print(json.dumps(carousel_message, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    demo_m1_visualization() 