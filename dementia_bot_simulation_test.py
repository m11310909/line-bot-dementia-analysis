#!/usr/bin/env python3
"""
失智症小幫手模擬測試腳本
測試4種不同類型的用戶問題和回應
"""

import requests
import json
import time
from datetime import datetime

class DementiaBotSimulationTest:
    """失智症小幫手模擬測試器"""
    
    def __init__(self, base_url: str = "http://localhost:8008"):
        self.base_url = base_url
        self.test_cases = {
            "症狀警訊檢測": {
                "description": "描述症狀希望知道是不是失智警訊",
                "messages": [
                    "媽媽最近常常忘記關瓦斯",
                    "爸爸不會用洗衣機了",
                    "奶奶忘記吃藥",
                    "爺爺走失過一次",
                    "媽媽最近常重複問同樣的問題"
                ],
                "expected_module": "M1"
            },
            "照護階段評估": {
                "description": "描述生活行為想知道照護階段",
                "messages": [
                    "媽媽輕度失智",
                    "爸爸中度失智",
                    "奶奶重度失智",
                    "爺爺病程進展",
                    "媽媽記憶力退化"
                ],
                "expected_module": "M2"
            },
            "異常行為處理": {
                "description": "描述情緒或行為想知道是否異常及如何處理",
                "messages": [
                    "爺爺有妄想症狀",
                    "爸爸有攻擊行為",
                    "奶奶有躁動不安",
                    "媽媽有幻覺",
                    "爺爺晚上不睡覺"
                ],
                "expected_module": "M3"
            },
            "照護資源指引": {
                "description": "想知道下一步任務尋找照顧指引與資源",
                "messages": [
                    "需要醫療協助",
                    "需要照護資源",
                    "需要社會支持",
                    "需要經濟協助",
                    "需要專業諮詢"
                ],
                "expected_module": "M4"
            }
        }
    
    def test_single_message(self, message: str, expected_module: str = None) -> dict:
        """測試單個訊息"""
        print(f"\n📝 測試訊息: {message}")
        
        try:
            # 發送到智能分析端點
            response = requests.post(
                f"{self.base_url}/analyze",
                json={
                    "message": message,
                    "user_id": "simulation_test"
                },
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                
                # 分析回應
                analysis = {
                    "message": message,
                    "response_type": result.get("type", "unknown"),
                    "has_flex_message": result.get("type") == "flex",
                    "response_length": len(json.dumps(result)),
                    "timestamp": datetime.now().isoformat()
                }
                
                # 提取模組信息
                if "contents" in result and "body" in result["contents"]:
                    body_content = result["contents"]["body"]
                    if "contents" in body_content:
                        for content in body_content["contents"]:
                            if "text" in content:
                                text = content["text"]
                                if "M1" in text:
                                    analysis["detected_module"] = "M1"
                                elif "M2" in text:
                                    analysis["detected_module"] = "M2"
                                elif "M3" in text:
                                    analysis["detected_module"] = "M3"
                                elif "M4" in text:
                                    analysis["detected_module"] = "M4"
                
                # 檢查模組匹配
                if expected_module and "detected_module" in analysis:
                    analysis["module_match"] = analysis["detected_module"] == expected_module
                
                print(f"✅ 回應類型: {analysis['response_type']}")
                print(f"📊 回應長度: {analysis['response_length']} 字符")
                if "detected_module" in analysis:
                    print(f"🎯 檢測模組: {analysis['detected_module']}")
                    if expected_module:
                        match_status = "✅" if analysis.get("module_match") else "❌"
                        print(f"{match_status} 模組匹配: {expected_module}")
                
                return analysis
                
            else:
                print(f"❌ 請求失敗: {response.status_code}")
                return {"error": f"HTTP {response.status_code}"}
                
        except Exception as e:
            print(f"❌ 測試錯誤: {e}")
            return {"error": str(e)}
    
    def run_comprehensive_test(self):
        """執行完整測試"""
        print("🧠 失智症小幫手模擬測試")
        print("=" * 60)
        
        all_results = {}
        
        for test_name, test_config in self.test_cases.items():
            print(f"\n🎯 測試類別: {test_name}")
            print(f"📋 描述: {test_config['description']}")
            print(f"🎯 預期模組: {test_config['expected_module']}")
            print("-" * 40)
            
            test_results = []
            correct_matches = 0
            
            for i, message in enumerate(test_config["messages"], 1):
                print(f"\n📝 測試 {i}/{len(test_config['messages'])}")
                result = self.test_single_message(message, test_config["expected_module"])
                
                if "error" not in result:
                    test_results.append(result)
                    if result.get("module_match"):
                        correct_matches += 1
                
                time.sleep(0.5)  # 避免請求過於頻繁
            
            # 計算準確率
            accuracy = (correct_matches / len(test_config["messages"])) * 100 if test_results else 0
            
            all_results[test_name] = {
                "description": test_config["description"],
                "expected_module": test_config["expected_module"],
                "total_tests": len(test_config["messages"]),
                "correct_matches": correct_matches,
                "accuracy": accuracy,
                "results": test_results
            }
            
            print(f"\n📊 {test_name} 測試結果:")
            print(f"  總測試數: {len(test_config['messages'])}")
            print(f"  正確匹配: {correct_matches}")
            print(f"  準確率: {accuracy:.1f}%")
        
        # 生成測試報告
        self.generate_test_report(all_results)
        
        return all_results
    
    def generate_test_report(self, results: dict):
        """生成測試報告"""
        print("\n" + "=" * 60)
        print("📊 測試報告摘要")
        print("=" * 60)
        
        total_tests = 0
        total_correct = 0
        
        for test_name, test_result in results.items():
            total_tests += test_result["total_tests"]
            total_correct += test_result["correct_matches"]
            
            print(f"\n🎯 {test_name}")
            print(f"   描述: {test_result['description']}")
            print(f"   預期模組: {test_result['expected_module']}")
            print(f"   準確率: {test_result['accuracy']:.1f}%")
            print(f"   結果: {test_result['correct_matches']}/{test_result['total_tests']}")
        
        overall_accuracy = (total_correct / total_tests) * 100 if total_tests > 0 else 0
        
        print(f"\n🎯 整體測試結果")
        print(f"   總測試數: {total_tests}")
        print(f"   總正確數: {total_correct}")
        print(f"   整體準確率: {overall_accuracy:.1f}%")
        
        # 保存詳細報告
        report = {
            "timestamp": datetime.now().isoformat(),
            "overall_accuracy": overall_accuracy,
            "total_tests": total_tests,
            "total_correct": total_correct,
            "test_results": results
        }
        
        with open("dementia_bot_simulation_report.json", "w", encoding="utf-8") as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        
        print(f"\n📄 詳細報告已保存: dementia_bot_simulation_report.json")
    
    def show_sample_responses(self):
        """顯示示例回應"""
        print("\n🎨 示例回應展示")
        print("=" * 60)
        
        sample_messages = {
            "M1 警訊檢測": "媽媽忘記關瓦斯",
            "M2 階段評估": "媽媽輕度失智", 
            "M3 異常處理": "爺爺有妄想症狀",
            "M4 資源指引": "需要醫療協助"
        }
        
        for test_name, message in sample_messages.items():
            print(f"\n📝 {test_name}: {message}")
            result = self.test_single_message(message)
            
            if "error" not in result:
                print(f"✅ 回應成功")
                if "detected_module" in result:
                    print(f"🎯 檢測模組: {result['detected_module']}")
            else:
                print(f"❌ 回應失敗: {result['error']}")
            
            time.sleep(1)

def main():
    """主函數"""
    print("🚀 啟動失智症小幫手模擬測試...")
    
    # 檢查服務狀態
    try:
        health_response = requests.get("http://localhost:8008/health", timeout=5)
        if health_response.status_code == 200:
            print("✅ 服務狀態正常")
        else:
            print("⚠️  服務狀態異常")
            return
    except Exception as e:
        print(f"❌ 無法連接到服務: {e}")
        return
    
    # 創建測試器
    tester = DementiaBotSimulationTest()
    
    # 顯示示例回應
    tester.show_sample_responses()
    
    # 執行完整測試
    print("\n" + "=" * 60)
    print("🧪 開始完整測試...")
    results = tester.run_comprehensive_test()
    
    print("\n✅ 測試完成!")

if __name__ == "__main__":
    main() 