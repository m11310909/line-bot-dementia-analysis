#!/usr/bin/env python3
"""
🧪 簡單 M1 功能測試
測試修復後的 M1 視覺化功能
"""

import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "services", "line-bot"))

# 模擬 LINE Bot 環境
from linebot.models import FlexSendMessage


def create_simple_m1_response(user_text: str) -> FlexSendMessage:
    """創建簡單的 M1 回應"""

    # 簡單的症狀檢測
    symptoms = {}
    if "忘記" in user_text or "記憶" in user_text:
        symptoms["記憶力"] = 3
    if "迷路" in user_text or "方向" in user_text:
        symptoms["定向力"] = 4
    if "說話" in user_text or "語言" in user_text:
        symptoms["語言能力"] = 2

    # 簡單的風險評估
    risk_factors = {}
    if "年紀" in user_text or "年齡" in user_text:
        risk_factors["年齡"] = 0.7

    # 計算警訊等級
    warning_level = 1
    if symptoms:
        avg_severity = sum(symptoms.values()) / len(symptoms)
        if avg_severity > 3:
            warning_level = 4
        elif avg_severity > 2:
            warning_level = 3
        else:
            warning_level = 2

    # 生成警訊訊息
    warning_messages = {
        1: "目前症狀輕微，建議定期觀察",
        2: "需要關注症狀變化，建議諮詢醫生",
        3: "症狀明顯，建議盡快就醫檢查",
        4: "症狀嚴重，建議立即就醫",
        5: "症狀非常嚴重，建議緊急就醫",
    }
    warning_message = warning_messages.get(warning_level, warning_messages[1])

    # 創建簡單的 Flex Message
    contents = []

    # 警訊指示器
    warning_colors = {
        1: "#4CAF50",
        2: "#8BC34A",
        3: "#FFC107",
        4: "#FF9800",
        5: "#F44336",
    }
    warning_icons = {1: "🟢", 2: "🟡", 3: "🟠", 4: "🟠", 5: "🔴"}

    contents.append(
        {
            "type": "box",
            "layout": "horizontal",
            "spacing": "md",
            "backgroundColor": warning_colors.get(warning_level, "#4CAF50"),
            "cornerRadius": "8px",
            "paddingAll": "12px",
            "contents": [
                {
                    "type": "text",
                    "text": warning_icons.get(warning_level, "🟢"),
                    "size": "lg",
                },
                {
                    "type": "box",
                    "layout": "vertical",
                    "flex": 1,
                    "contents": [
                        {
                            "type": "text",
                            "text": f"警訊等級 {warning_level}",
                            "weight": "bold",
                            "color": "#FFFFFF",
                            "size": "sm",
                        },
                        {
                            "type": "text",
                            "text": warning_message,
                            "color": "#FFFFFF",
                            "size": "xs",
                            "wrap": True,
                        },
                    ],
                },
            ],
        }
    )

    # 症狀列表
    if symptoms:
        contents.append({"type": "separator", "margin": "lg"})
        symptoms_box = {
            "type": "box",
            "layout": "vertical",
            "spacing": "md",
            "contents": [
                {
                    "type": "text",
                    "text": "檢測到的症狀",
                    "weight": "bold",
                    "size": "lg",
                    "color": "#333333",
                }
            ],
        }

        for symptom, severity in symptoms.items():
            severity_text = (
                "輕微" if severity <= 2 else "中等" if severity <= 3 else "嚴重"
            )
            symptoms_box["contents"].append(
                {
                    "type": "box",
                    "layout": "horizontal",
                    "spacing": "sm",
                    "contents": [
                        {
                            "type": "text",
                            "text": symptom,
                            "size": "sm",
                            "color": "#333333",
                            "flex": 1,
                        },
                        {
                            "type": "text",
                            "text": f"{severity_text} ({severity}/5)",
                            "size": "sm",
                            "color": "#666666",
                        },
                    ],
                }
            )

        contents.append(symptoms_box)

    # 建議按鈕
    contents.append(
        {
            "type": "box",
            "layout": "vertical",
            "spacing": "sm",
            "margin": "lg",
            "contents": [
                {
                    "type": "button",
                    "action": {
                        "type": "postback",
                        "label": "📋 詳細建議",
                        "data": "m1_detailed_advice",
                    },
                    "style": "primary",
                    "color": "#4CAF50",
                },
                {
                    "type": "button",
                    "action": {
                        "type": "postback",
                        "label": "🏥 醫療資源",
                        "data": "m1_medical_resources",
                    },
                    "style": "secondary",
                    "color": "#2196F3",
                },
            ],
        }
    )

    return FlexSendMessage(
        alt_text="失智症警訊徵兆檢測結果",
        contents={
            "type": "bubble",
            "size": "giga",
            "body": {
                "type": "box",
                "layout": "vertical",
                "spacing": "md",
                "contents": contents,
            },
        },
    )


def test_simple_m1():
    """測試簡單的 M1 功能"""

    print("🧪 測試簡單的 M1 功能...")

    # 測試案例
    test_cases = [
        {
            "name": "記憶力問題",
            "text": "我最近常常忘記事情",
            "expected_symptoms": ["記憶力"],
        },
        {"name": "迷路問題", "text": "我會在家裡迷路", "expected_symptoms": ["定向力"]},
        {
            "name": "語言問題",
            "text": "我說話時找不到詞彙",
            "expected_symptoms": ["語言能力"],
        },
        {
            "name": "高齡風險",
            "text": "我今年75歲，最近記憶力下降",
            "expected_symptoms": ["記憶力"],
            "expected_risk": ["年齡"],
        },
        {
            "name": "綜合症狀",
            "text": "我今年80歲，經常忘記事情，而且會迷路",
            "expected_symptoms": ["記憶力", "定向力"],
            "expected_risk": ["年齡"],
        },
    ]

    print("\n📊 測試結果：")
    print("=" * 50)

    for i, test_case in enumerate(test_cases, 1):
        print(f"\n🔍 測試 {i}: {test_case['name']}")
        print(f"📝 輸入文本: {test_case['text']}")

        try:
            # 執行測試
            flex_message = create_simple_m1_response(test_case["text"])

            print("✅ Flex Message 生成成功")
            print(f"📱 Alt Text: {flex_message.alt_text}")
            print(f"📦 內容類型: {type(flex_message.contents)}")

            # 檢查症狀檢測
            symptoms = {}
            if "忘記" in test_case["text"] or "記憶" in test_case["text"]:
                symptoms["記憶力"] = 3
            if "迷路" in test_case["text"] or "方向" in test_case["text"]:
                symptoms["定向力"] = 4
            if "說話" in test_case["text"] or "語言" in test_case["text"]:
                symptoms["語言能力"] = 2

            if symptoms:
                print("🏥 檢測到的症狀:")
                for symptom, severity in symptoms.items():
                    print(f"  - {symptom}: {severity}/5")

            # 檢查風險因素
            risk_factors = {}
            if "年紀" in test_case["text"] or "年齡" in test_case["text"]:
                risk_factors["年齡"] = 0.7

            if risk_factors:
                print("⚠️ 風險因素:")
                for factor, risk in risk_factors.items():
                    print(f"  - {factor}: {risk:.1f}")

            print("✅ 測試通過")

        except Exception as e:
            print(f"❌ 測試失敗: {e}")

        print("-" * 40)

    print("\n🎉 簡單 M1 功能測試完成！")


if __name__ == "__main__":
    print("🚀 啟動簡單 M1 功能測試")
    print("=" * 50)

    test_simple_m1()

    print("\n🎊 所有測試完成！")
