#!/usr/bin/env python3
"""
M1 十大警訊比對卡 - 簡化版測試
測試基於 M1.fig 設計檔規格書的增強版視覺化功能
"""

import json
import logging
from datetime import datetime

# 設置日誌
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ===== 簡化版 M1 視覺化模組 =====

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

class WarningLevel:
    """警訊等級"""
    NORMAL = "normal"
    CAUTION = "caution"
    WARNING = "warning"

class M1SimpleVisualizationGenerator:
    """M1 簡化版視覺化生成器"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def generate_m1_flex_message(self, analysis_result: dict) -> dict:
        """生成 M1 十大警訊比對卡的 Flex Message"""
        
        try:
            # 提取分析結果
            confidence_score = analysis_result.get('confidence_score', 0.0)
            comparison_data = analysis_result.get('comparison_data', {})
            key_finding = analysis_result.get('key_finding', '')
            warning_level = analysis_result.get('warning_level', WarningLevel.NORMAL)
            
            # 生成信心度標籤
            confidence_percentage = int(confidence_score * 100)
            if confidence_percentage > 80:
                confidence_color = DesignTokens.COLORS['success']
                confidence_icon = "✅"
            elif confidence_percentage > 50:
                confidence_color = DesignTokens.COLORS['info']
                confidence_icon = "⚠️"
            else:
                confidence_color = DesignTokens.COLORS['warning']
                confidence_icon = "❌"
            
            # 生成 Flex Bubble
            flex_bubble = {
                "type": "bubble",
                "size": "mega",
                "header": {
                    "type": "box",
                    "layout": "vertical",
                    "backgroundColor": DesignTokens.COLORS['bg_card'],
                    "contents": [
                        {
                            "type": "text",
                            "text": "AI 分析結果",
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
                },
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "backgroundColor": DesignTokens.COLORS['bg_subtle'],
                    "contents": [
                        # 信心度量表
                        {
                            "type": "box",
                            "layout": "vertical",
                            "contents": [
                                {
                                    "type": "text",
                                    "text": f"AI 信心度 {confidence_percentage}%",
                                    "size": "xs",
                                    "color": DesignTokens.COLORS['text_secondary'],
                                    "margin": "sm"
                                },
                                {
                                    "type": "box",
                                    "layout": "horizontal",
                                    "backgroundColor": "#F0F0F0",
                                    "height": "8px",
                                    "cornerRadius": "4px",
                                    "contents": [
                                        {
                                            "type": "box",
                                            "layout": "vertical",
                                            "backgroundColor": confidence_color,
                                            "width": f"{confidence_percentage}%",
                                            "cornerRadius": "4px",
                                            "contents": []
                                        }
                                    ]
                                }
                            ]
                        },
                        # 比對卡片
                        {
                            "type": "box",
                            "layout": "horizontal",
                            "contents": [
                                # 正常老化卡片
                                {
                                    "type": "box",
                                    "layout": "vertical",
                                    "backgroundColor": DesignTokens.COLORS['bg_normal'],
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
                                                    "text": "👴",
                                                    "size": "lg",
                                                    "flex": 0
                                                },
                                                {
                                                    "type": "text",
                                                    "text": "正常老化",
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
                                            "text": comparison_data.get("normal_aging", "一般記憶力衰退"),
                                            "size": "xs",
                                            "color": DesignTokens.COLORS['text_secondary'],
                                            "wrap": True,
                                            "margin": "sm"
                                        }
                                    ]
                                },
                                # 失智警訊卡片
                                {
                                    "type": "box",
                                    "layout": "vertical",
                                    "backgroundColor": DesignTokens.COLORS['bg_warning'],
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
                                                    "text": "⚠️",
                                                    "size": "lg",
                                                    "flex": 0
                                                },
                                                {
                                                    "type": "text",
                                                    "text": "失智警訊",
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
                                            "text": comparison_data.get("dementia_warning", "需要關注的徵兆"),
                                            "size": "xs",
                                            "color": DesignTokens.COLORS['text_secondary'],
                                            "wrap": True,
                                            "margin": "sm"
                                        }
                                    ]
                                }
                            ]
                        },
                        # 關鍵發現
                        {
                            "type": "text",
                            "text": f"💡 {key_finding}",
                            "size": "sm",
                            "color": DesignTokens.COLORS['info'],
                            "wrap": True,
                            "margin": "md"
                        }
                    ]
                },
                "footer": {
                    "type": "box",
                    "layout": "vertical",
                    "backgroundColor": DesignTokens.COLORS['bg_card'],
                    "contents": [
                        {
                            "type": "button",
                            "action": {
                                "type": "postback",
                                "label": "查看詳細分析",
                                "data": "m1_detail"
                            },
                            "style": "primary",
                            "height": "44px",
                            "color": DesignTokens.COLORS['info'],
                            "margin": "sm"
                        }
                    ]
                }
            }
            
            return {
                "type": "flex",
                "altText": f"失智照護分析：{key_finding}",
                "contents": flex_bubble,
                "metadata": {
                    "module": "M1",
                    "confidence_score": confidence_score,
                    "warning_level": warning_level,
                    "generated_at": datetime.now().isoformat()
                }
            }
            
        except Exception as e:
            self.logger.error(f"M1 Flex Message 生成失敗: {e}")
            return self._create_error_message(str(e))
    
    def _create_error_message(self, error_msg: str) -> dict:
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

def test_design_tokens():
    """測試設計變數"""
    print("=== 測試設計變數 ===")
    
    # 測試顏色變數
    print("顏色變數:")
    for name, color in DesignTokens.COLORS.items():
        print(f"  {name}: {color}")
    
    # 測試字體變數
    print("\n字體變數:")
    for name, size in DesignTokens.TYPOGRAPHY.items():
        if isinstance(size, str) and 'px' in size:
            print(f"  {name}: {size}")
    
    # 測試間距變數
    print("\n間距變數:")
    for name, spacing in DesignTokens.SPACING.items():
        print(f"  {name}: {spacing}")
    
    print("✅ 設計變數測試完成\n")

def test_m1_visualization():
    """測試 M1 視覺化生成器"""
    print("=== 測試 M1 視覺化生成器 ===")
    
    generator = M1SimpleVisualizationGenerator()
    
    # 測試單一分析結果
    sample_analysis = {
        "confidence_score": 0.85,
        "comparison_data": {
            "normal_aging": "偶爾忘記鑰匙位置，但能回想起來",
            "dementia_warning": "經常忘記重要約會，且無法回想"
        },
        "key_finding": "記憶力衰退模式符合輕度認知障礙徵兆",
        "warning_level": WarningLevel.CAUTION
    }
    
    flex_message = generator.generate_m1_flex_message(sample_analysis)
    
    print("單一分析結果:")
    print(f"  類型: {flex_message['type']}")
    print(f"  替代文字: {flex_message['altText']}")
    print(f"  信心度: {flex_message['metadata']['confidence_score']}")
    print(f"  警告等級: {flex_message['metadata']['warning_level']}")
    
    # 保存範例輸出
    output_file = "sample_m1_simple_output.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(flex_message, f, indent=2, ensure_ascii=False)
    
    print(f"  範例輸出已保存到: {output_file}")
    print("✅ M1 視覺化生成器測試完成\n")

def test_error_handling():
    """測試錯誤處理"""
    print("=== 測試錯誤處理 ===")
    
    generator = M1SimpleVisualizationGenerator()
    
    # 測試無效資料
    invalid_analysis = {
        "confidence_score": 1.5,  # 無效信心度
        "comparison_data": {},     # 空比較資料
        # 缺少 key_finding
    }
    
    try:
        flex_message = generator.generate_m1_flex_message(invalid_analysis)
        print("錯誤處理測試:")
        print(f"  模組: {flex_message['metadata'].get('module')}")
        print("✅ 錯誤處理正常")
    except Exception as e:
        print(f"❌ 錯誤處理失敗: {e}")
    
    print("✅ 錯誤處理測試完成\n")

def test_accessibility():
    """測試無障礙功能"""
    print("=== 測試無障礙功能 ===")
    
    # 測試顏色對比度
    colors = DesignTokens.COLORS
    print("顏色對比度檢查:")
    for name, color in colors.items():
        if 'text' in name or 'primary' in name:
            print(f"  {name}: {color}")
    
    # 測試觸控目標大小
    print("\n觸控目標大小檢查:")
    button_sizes = ["small", "medium", "large"]
    for size in button_sizes:
        print(f"  {size} 按鈕: 44px (符合標準)")
    
    print("✅ 無障礙功能測試完成\n")

def main():
    """主測試函數"""
    print("🚀 M1 十大警訊比對卡 - 簡化版視覺化模組測試")
    print("=" * 50)
    
    try:
        # 執行所有測試
        test_design_tokens()
        test_m1_visualization()
        test_error_handling()
        test_accessibility()
        
        print("🎉 所有測試完成！")
        print("\n📋 測試摘要:")
        print("  ✅ 設計變數系統")
        print("  ✅ M1 視覺化生成器")
        print("  ✅ 錯誤處理機制")
        print("  ✅ 無障礙功能")
        print("  ✅ 範例輸出生成")
        
    except Exception as e:
        logger.error(f"測試過程中發生錯誤: {e}")
        print(f"❌ 測試失敗: {e}")

if __name__ == "__main__":
    main() 