#!/usr/bin/env python3
"""
🧪 M1 視覺化模組測試腳本
測試失智症警訊徵兆檢測的視覺化功能
"""

import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "services", "line-bot"))

from visualization.modules.m1_visualization import M1VisualizationProcessor


def test_m1_visualization():
    """測試 M1 視覺化模組"""

    print("🧪 開始測試 M1 視覺化模組...")

    # 創建處理器
    processor = M1VisualizationProcessor()

    # 測試案例
    test_cases = [
        {
            "name": "輕微症狀測試",
            "text": "我最近偶爾會忘記一些小事",
            "expected_level": 2,
        },
        {
            "name": "中等症狀測試",
            "text": "我經常忘記重要的事情，而且會迷路",
            "expected_level": 3,
        },
        {
            "name": "嚴重症狀測試",
            "text": "我最近非常健忘，經常忘記家人的名字，而且會在家裡迷路",
            "expected_level": 4,
        },
        {
            "name": "高齡風險測試",
            "text": "我今年75歲，最近記憶力明顯下降",
            "expected_level": 3,
        },
        {
            "name": "綜合症狀測試",
            "text": "我今年80歲，最近經常忘記事情，說話時會找不到詞彙，而且情緒容易焦慮",
            "expected_level": 4,
        },
    ]

    print("\n📊 測試結果：")
    print("=" * 60)

    for i, test_case in enumerate(test_cases, 1):
        print(f"\n🔍 測試 {i}: {test_case['name']}")
        print(f"📝 輸入文本: {test_case['text']}")

        # 執行分析
        result = processor.analyze_text(test_case["text"])

        # 顯示結果
        print(
            f"🎯 警訊等級: {result['warning_level']} (預期: {test_case['expected_level']})"
        )
        print(f"📋 警訊訊息: {result['warning_message']}")

        # 顯示症狀
        if result["symptoms"]:
            print("🏥 檢測到的症狀:")
            for symptom, severity in result["symptoms"].items():
                print(f"  - {symptom}: {severity}/5")

        # 顯示風險因素
        if result["risk_factors"]:
            print("⚠️ 風險因素:")
            for factor, risk in result["risk_factors"].items():
                print(f"  - {factor}: {risk:.2f}")

        # 驗證結果
        if result["warning_level"] == test_case["expected_level"]:
            print("✅ 測試通過")
        else:
            print(
                f"❌ 測試失敗 - 預期等級 {test_case['expected_level']}，實際等級 {result['warning_level']}"
            )

        print("-" * 40)

    # 測試視覺化生成
    print("\n🎨 測試視覺化生成...")

    # 使用最後一個測試案例的結果
    final_result = processor.analyze_text(test_cases[-1]["text"])

    try:
        flex_message = processor.create_visualization(final_result)
        print("✅ Flex Message 生成成功")
        print(f"📱 Alt Text: {flex_message.alt_text}")
        print(f"📦 內容類型: {type(flex_message.contents)}")
    except Exception as e:
        print(f"❌ Flex Message 生成失敗: {e}")

    print("\n🎉 M1 視覺化模組測試完成！")


def test_symptom_extraction():
    """測試症狀提取功能"""

    print("\n🔬 測試症狀提取功能...")

    processor = M1VisualizationProcessor()

    # 測試症狀關鍵詞
    test_texts = [
        "我經常忘記事情",
        "我會在家裡迷路",
        "我說話時找不到詞彙",
        "我情緒容易焦慮",
        "我注意力無法集中",
    ]

    for text in test_texts:
        symptoms = processor._extract_symptoms(text)
        print(f"\n📝 文本: {text}")
        print(f"🏥 提取的症狀: {symptoms}")


def test_risk_factor_extraction():
    """測試風險因素提取功能"""

    print("\n⚠️ 測試風險因素提取功能...")

    processor = M1VisualizationProcessor()

    # 測試風險因素關鍵詞
    test_texts = [
        "我今年75歲",
        "我家族有失智症病史",
        "我有高血壓",
        "我之前跌倒過",
        "我很少運動",
    ]

    for text in test_texts:
        risk_factors = processor._extract_risk_factors(text)
        print(f"\n📝 文本: {text}")
        print(f"⚠️ 提取的風險因素: {risk_factors}")


if __name__ == "__main__":
    print("🚀 啟動 M1 視覺化模組測試")
    print("=" * 60)

    # 執行所有測試
    test_m1_visualization()
    test_symptom_extraction()
    test_risk_factor_extraction()

    print("\n🎊 所有測試完成！")
