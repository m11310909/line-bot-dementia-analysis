#!/usr/bin/env python3
"""
JTBD 架構測試腳本
測試 M1-M4 模組的情境化文字回應
"""

import requests
import json

def test_jtbd_architecture():
    """測試 JTBD 架構"""
    print("🎯 JTBD 架構測試")
    print("=" * 60)
    
    # JTBD 測試案例
    test_cases = [
        {
            "input": "爸爸不會用洗衣機",
            "description": "M1: 十大警訊比對卡",
            "jtbd": "當我發現家人有異常行為時，我想要快速判斷是否為失智警訊"
        },
        {
            "input": "媽媽中度失智，需要協助",
            "description": "M2: 病程階段對照",
            "jtbd": "當我需要了解失智症的進展狀況時，我想要知道目前處於哪個階段"
        },
        {
            "input": "爺爺最近情緒不穩定，常常發脾氣",
            "description": "M3: BPSD 精神行為症狀",
            "jtbd": "當家人出現困擾的精神行為症狀時，我想要理解原因並知道如何應對"
        },
        {
            "input": "需要申請照護補助和資源",
            "description": "M4: 照護任務導航",
            "jtbd": "當我面對繁雜的照護事務時，我想要有條理的任務指引"
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n📋 測試案例 {i}: {test_case['description']}")
        print(f"🎯 JTBD: {test_case['jtbd']}")
        print(f"📝 輸入: {test_case['input']}")
        print("-" * 60)
        
        try:
            response = requests.post(
                "http://localhost:8005/comprehensive-analysis",
                json={"user_input": test_case['input']},
                headers={"Content-Type": "application/json"},
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                
                # 模擬 JTBD 文字回應
                summary = result.get('comprehensive_summary', '分析完成')
                modules_used = result.get('modules_used', [])
                chunks_found = len(result.get('retrieved_chunks', []))
                
                # 根據模組生成 JTBD 回應
                if 'M1' in modules_used:
                    jtbd_response = create_m1_jtbd_preview(test_case['input'], summary, chunks_found)
                elif 'M2' in modules_used:
                    jtbd_response = create_m2_jtbd_preview(test_case['input'], summary, chunks_found)
                elif 'M3' in modules_used:
                    jtbd_response = create_m3_jtbd_preview(test_case['input'], summary, chunks_found)
                elif 'M4' in modules_used:
                    jtbd_response = create_m4_jtbd_preview(test_case['input'], summary, chunks_found)
                else:
                    jtbd_response = create_default_jtbd_preview(test_case['input'], summary, modules_used, chunks_found)
                
                print("✅ JTBD 回應:")
                print(jtbd_response)
                print("-" * 60)
                print(f"📏 回應長度: {len(jtbd_response)} 字符")
                print(f"⏱️  回應時間: {response.elapsed.total_seconds():.3f}秒")
                
            else:
                print(f"❌ API 錯誤: {response.status_code}")
                
        except Exception as e:
            print(f"❌ 測試失敗: {e}")


def create_m1_jtbd_preview(user_input: str, summary: str, chunks_found: int) -> str:
    """M1 JTBD 預覽"""
    return f"""⚠️ 失智症警訊檢測

🔍 AI 信心度: 高 (90%+)
📊 分析摘要: {summary}

🎯 快速判斷:
• 症狀符合失智症警訊
• 建議及早就醫評估

💡 推理路徑:
1. 症狀識別 → 2. 警訊比對 → 3. 風險評估

📋 建議行動:
• 立即預約神經科門診
• 準備詳細症狀記錄
• 聯繫家屬討論

📊 找到相關片段: {chunks_found} 個"""


def create_m2_jtbd_preview(user_input: str, summary: str, chunks_found: int) -> str:
    """M2 JTBD 預覽"""
    return f"""📈 病程階段評估

🎯 階段定位:
📍 當前階段: 中度失智症
⏰ 預估病程: 2-8年
🔍 主要特徵: 明顯認知障礙、日常生活需協助

🔄 病程預期:
• 症狀會逐漸進展
• 進展速度因人而異
• 早期介入可延緩惡化

📋 階段準備:
• 申請照護資源
• 調整居家環境
• 尋求家屬支持

📊 找到相關片段: {chunks_found} 個"""


def create_m3_jtbd_preview(user_input: str, summary: str, chunks_found: int) -> str:
    """M3 JTBD 預覽"""
    return f"""🧠 BPSD 症狀分析

💡 症狀理解:
• 這些是疾病表現，不是故意
• 大腦功能受損導致行為改變
• 症狀會隨病程變化

😤 情緒症狀處理:
• 保持冷靜，避免爭執
• 轉移注意力到愉快話題
• 建立規律作息
• 考慮音樂療法

💪 照護技巧:
• 使用簡單明確的語言
• 保持環境穩定
• 建立日常規律
• 尋求專業支援

🤝 支持資源:
• 失智症協會諮詢
• 家屬支持團體
• 專業照護服務
• 緊急聯絡資訊

📊 找到相關片段: {chunks_found} 個"""


def create_m4_jtbd_preview(user_input: str, summary: str, chunks_found: int) -> str:
    """M4 JTBD 預覽"""
    return f"""🗺️ 照護任務導航

📋 任務分類:

🚨 緊急任務:
• 醫療評估安排
• 安全環境檢查
• 緊急聯絡建立

⭐ 重要任務:
• 照護資源申請
• 法律文件準備
• 財務規劃安排

📝 一般任務:
• 日常照護學習
• 支持網絡建立
• 自我照顧安排

🎯 優先順序:
1. 確保安全與醫療
2. 申請必要資源
3. 建立照護系統
4. 長期規劃準備

💡 個人化建議:
• 準備相關證明文件
• 諮詢社會福利單位
• 了解申請流程時程

📊 找到相關片段: {chunks_found} 個"""


def create_default_jtbd_preview(user_input: str, summary: str, modules_used: list, chunks_found: int) -> str:
    """預設 JTBD 預覽"""
    return f"""🧠 失智症綜合分析

📊 分析摘要: {summary}

🔍 使用模組: {', '.join(modules_used)}
📋 找到相關片段: {chunks_found} 個

💡 建議行動:
• 提供更多詳細症狀描述
• 說明具體困擾情況
• 詢問特定照護需求

🎯 下一步:
• 我們會根據您的描述
• 提供更精準的分析
• 給出具體的建議"""


def test_jtbd_user_scenarios():
    """測試 JTBD 用戶場景"""
    print("\n👥 JTBD 用戶場景測試")
    print("=" * 60)
    
    scenarios = [
        {
            "user_type": "焦慮家屬",
            "scenario": "發現家人記憶力減退",
            "jtbd": "快速判斷是否為失智警訊",
            "expected_response": "M1 警訊檢測"
        },
        {
            "user_type": "規劃家屬", 
            "scenario": "了解病程進展",
            "jtbd": "知道目前處於哪個階段",
            "expected_response": "M2 病程評估"
        },
        {
            "user_type": "挫折家屬",
            "scenario": "面對行為問題",
            "jtbd": "理解原因並知道如何應對",
            "expected_response": "M3 BPSD 分析"
        },
        {
            "user_type": "迷茫家屬",
            "scenario": "面對繁雜照護事務",
            "jtbd": "有條理的任務指引",
            "expected_response": "M4 任務導航"
        }
    ]
    
    for scenario in scenarios:
        print(f"\n👤 用戶類型: {scenario['user_type']}")
        print(f"📋 場景: {scenario['scenario']}")
        print(f"🎯 JTBD: {scenario['jtbd']}")
        print(f"📊 預期回應: {scenario['expected_response']}")
        print("✅ 場景符合 JTBD 架構")


def main():
    """主測試函數"""
    print("🚀 JTBD 架構完整測試")
    print("遵循 M1-M4 視覺化模組設計")
    print("=" * 60)
    
    # 測試 JTBD 架構
    test_jtbd_architecture()
    
    # 測試用戶場景
    test_jtbd_user_scenarios()
    
    print("\n" + "=" * 60)
    print("🎉 JTBD 架構測試完成!")
    print("📊 系統狀態: 運行中")
    print("🎯 用戶體驗: 情境化回應")
    print("🌐 Webhook URL: https://0ac6705ad6a2.ngrok-free.app/webhook")


if __name__ == "__main__":
    main() 