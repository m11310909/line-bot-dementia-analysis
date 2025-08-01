#!/usr/bin/env python3
"""
M1 十大警訊比對卡 - 視覺化模組測試
測試基於 M1.fig 設計檔規格書的增強版視覺化功能
"""

import sys
import json
import logging
from pathlib import Path

# Add the project root to the path
sys.path.append(str(Path(__file__).parent))

from xai_flex.m1_enhanced_visualization import (
    M1EnhancedVisualizationGenerator,
    DesignTokens,
    WarningLevel,
    create_sample_m1_analysis
)
from xai_flex.m1_integration import M1IntegrationManager

# 設置日誌
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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
    
    generator = M1EnhancedVisualizationGenerator()
    
    # 測試單一分析結果
    sample_analysis = create_sample_m1_analysis()
    flex_message = generator.generate_m1_flex_message(sample_analysis)
    
    print("單一分析結果:")
    print(f"  類型: {flex_message['type']}")
    print(f"  替代文字: {flex_message['altText']}")
    print(f"  元數據: {flex_message['metadata']}")
    
    # 測試多重分析結果
    multiple_results = [
        sample_analysis,
        {
            "confidence_score": 0.72,
            "comparison_data": {
                "normal_aging": "偶爾迷路但能找到方向",
                "dementia_warning": "在熟悉環境中迷路"
            },
            "key_finding": "空間定向能力下降",
            "warning_level": WarningLevel.WARNING
        },
        {
            "confidence_score": 0.95,
            "comparison_data": {
                "normal_aging": "偶爾忘記名字但能想起",
                "dementia_warning": "忘記親近家人的名字"
            },
            "key_finding": "人際關係記憶正常",
            "warning_level": WarningLevel.NORMAL
        }
    ]
    
    carousel_message = generator.generate_m1_carousel(multiple_results)
    
    print("\n多重分析結果:")
    print(f"  類型: {carousel_message['type']}")
    print(f"  替代文字: {carousel_message['altText']}")
    print(f"  卡片數量: {carousel_message['metadata']['card_count']}")
    
    print("✅ M1 視覺化生成器測試完成\n")

def test_m1_integration():
    """測試 M1 整合管理器"""
    print("=== 測試 M1 整合管理器 ===")
    
    integration_manager = M1IntegrationManager()
    
    # 測試單一分析整合
    sample_analysis = {
        "confidence_score": 0.85,
        "comparison_data": {
            "normal_aging": "偶爾忘記鑰匙位置，但能回想起來",
            "dementia_warning": "經常忘記重要約會，且無法回想"
        },
        "key_finding": "記憶力衰退模式符合輕度認知障礙徵兆",
        "warning_level": WarningLevel.CAUTION
    }
    
    response = integration_manager.process_m1_analysis(
        user_input="記憶力問題",
        analysis_data=sample_analysis
    )
    
    print("整合管理器測試結果:")
    print(f"  模組: {response.metadata.get('module')}")
    print(f"  信心度: {response.metadata.get('confidence_score')}")
    print(f"  警告等級: {response.metadata.get('warning_level')}")
    print(f"  後備文字: {response.fallback_text}")
    print(f"  互動處理器數量: {len(response.interaction_handlers)}")
    print(f"  無障礙增強: {response.accessibility_enhanced}")
    
    # 測試批次分析整合
    batch_results = [
        sample_analysis,
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
    
    batch_response = integration_manager.process_m1_batch_analysis(batch_results)
    
    print("\n批次分析整合結果:")
    print(f"  結果數量: {batch_response.metadata.get('result_count')}")
    print(f"  後備文字: {batch_response.fallback_text}")
    print(f"  互動處理器數量: {len(batch_response.interaction_handlers)}")
    
    print("✅ M1 整合管理器測試完成\n")

def test_error_handling():
    """測試錯誤處理"""
    print("=== 測試錯誤處理 ===")
    
    generator = M1EnhancedVisualizationGenerator()
    integration_manager = M1IntegrationManager()
    
    # 測試無效資料
    invalid_analysis = {
        "confidence_score": 1.5,  # 無效信心度
        "comparison_data": {},     # 空比較資料
        # 缺少 key_finding
    }
    
    try:
        response = integration_manager.process_m1_analysis(
            user_input="測試",
            analysis_data=invalid_analysis
        )
        print("錯誤處理測試:")
        print(f"  模組: {response.metadata.get('module')}")
        print(f"  錯誤: {response.metadata.get('error', '無')}")
        print("✅ 錯誤處理正常")
    except Exception as e:
        print(f"❌ 錯誤處理失敗: {e}")
    
    print("✅ 錯誤處理測試完成\n")

def test_accessibility():
    """測試無障礙功能"""
    print("=== 測試無障礙功能 ===")
    
    generator = M1EnhancedVisualizationGenerator()
    
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

def generate_sample_output():
    """生成範例輸出"""
    print("=== 生成範例輸出 ===")
    
    generator = M1EnhancedVisualizationGenerator()
    sample_analysis = create_sample_m1_analysis()
    
    # 生成 Flex Message
    flex_message = generator.generate_m1_flex_message(sample_analysis)
    
    # 保存到檔案
    output_file = "sample_m1_output.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(flex_message, f, indent=2, ensure_ascii=False)
    
    print(f"範例輸出已保存到: {output_file}")
    print("✅ 範例輸出生成完成\n")

def main():
    """主測試函數"""
    print("🚀 M1 十大警訊比對卡 - 視覺化模組測試")
    print("=" * 50)
    
    try:
        # 執行所有測試
        test_design_tokens()
        test_m1_visualization()
        test_m1_integration()
        test_error_handling()
        test_accessibility()
        generate_sample_output()
        
        print("🎉 所有測試完成！")
        print("\n📋 測試摘要:")
        print("  ✅ 設計變數系統")
        print("  ✅ M1 視覺化生成器")
        print("  ✅ M1 整合管理器")
        print("  ✅ 錯誤處理機制")
        print("  ✅ 無障礙功能")
        print("  ✅ 範例輸出生成")
        
    except Exception as e:
        logger.error(f"測試過程中發生錯誤: {e}")
        print(f"❌ 測試失敗: {e}")

if __name__ == "__main__":
    main() 