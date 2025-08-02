#!/usr/bin/env python3
"""
🧪 實測素材 - M1-M4 優化 XAI 系統
提供完整的測試案例、效能基準和驗證腳本
"""

import time
import requests
import json
import statistics
from typing import Dict, List, Any
from dataclasses import dataclass
from datetime import datetime
import asyncio

@dataclass
class TestCase:
    """測試案例"""
    input_text: str
    expected_module: str
    description: str
    category: str
    expected_confidence_range: tuple

class XAITestMaterials:
    """XAI 系統實測素材"""
    
    def __init__(self):
        self.xai_wrapper_url = "http://localhost:8009/analyze"
        self.chatbot_api_url = "http://localhost:8008/analyze"
        self.line_bot_url = "http://localhost:8081/health"
        
        # 真實測試案例
        self.test_cases = [
            # M1 警訊測試案例
            TestCase(
                input_text="爸爸忘記關瓦斯爐",
                expected_module="M1",
                description="M1-01 忘記關瓦斯爐",
                category="memory_warning",
                expected_confidence_range=(0.7, 0.9)
            ),
            TestCase(
                input_text="媽媽重複問同樣的問題",
                expected_module="M1",
                description="M1-02 重複發問",
                category="memory_warning",
                expected_confidence_range=(0.8, 0.95)
            ),
            TestCase(
                input_text="爺爺忘記回家的路",
                expected_module="M1",
                description="M1-03 空間定向障礙",
                category="memory_warning",
                expected_confidence_range=(0.75, 0.9)
            ),
            TestCase(
                input_text="奶奶不會使用洗衣機",
                expected_module="M1",
                description="M1-04 工具使用困難",
                category="memory_warning",
                expected_confidence_range=(0.7, 0.85)
            ),
            
            # M2 病程測試案例
            TestCase(
                input_text="媽媽輕度失智症狀",
                expected_module="M2",
                description="M2-01 早期階段",
                category="progression",
                expected_confidence_range=(0.6, 0.8)
            ),
            TestCase(
                input_text="爸爸中度失智",
                expected_module="M2",
                description="M2-02 中期階段",
                category="progression",
                expected_confidence_range=(0.7, 0.85)
            ),
            TestCase(
                input_text="爺爺重度失智",
                expected_module="M2",
                description="M2-03 晚期階段",
                category="progression",
                expected_confidence_range=(0.8, 0.95)
            ),
            TestCase(
                input_text="奶奶病程進展快速",
                expected_module="M2",
                description="M2-04 快速進展",
                category="progression",
                expected_confidence_range=(0.75, 0.9)
            ),
            
            # M3 BPSD 測試案例
            TestCase(
                input_text="爺爺有妄想症狀",
                expected_module="M3",
                description="M3-01 妄想症狀",
                category="bpsd",
                expected_confidence_range=(0.8, 0.95)
            ),
            TestCase(
                input_text="媽媽有幻覺",
                expected_module="M3",
                description="M3-02 幻覺症狀",
                category="bpsd",
                expected_confidence_range=(0.75, 0.9)
            ),
            TestCase(
                input_text="爸爸有攻擊行為",
                expected_module="M3",
                description="M3-03 攻擊行為",
                category="bpsd",
                expected_confidence_range=(0.8, 0.95)
            ),
            TestCase(
                input_text="奶奶有躁動不安",
                expected_module="M3",
                description="M3-04 躁動症狀",
                category="bpsd",
                expected_confidence_range=(0.7, 0.85)
            ),
            
            # M4 照護測試案例
            TestCase(
                input_text="需要醫療協助",
                expected_module="M4",
                description="M4-01 醫療需求",
                category="care_navigation",
                expected_confidence_range=(0.7, 0.85)
            ),
            TestCase(
                input_text="需要照護資源",
                expected_module="M4",
                description="M4-02 照護資源",
                category="care_navigation",
                expected_confidence_range=(0.75, 0.9)
            ),
            TestCase(
                input_text="需要社會支持",
                expected_module="M4",
                description="M4-03 社會支持",
                category="care_navigation",
                expected_confidence_range=(0.6, 0.8)
            ),
            TestCase(
                input_text="需要經濟協助",
                expected_module="M4",
                description="M4-04 經濟協助",
                category="care_navigation",
                expected_confidence_range=(0.65, 0.8)
            )
        ]
        
        # 邊界測試案例
        self.edge_cases = [
            TestCase(
                input_text="",
                expected_module="general",
                description="空字串測試",
                category="edge_case",
                expected_confidence_range=(0.0, 0.3)
            ),
            TestCase(
                input_text="今天天氣很好",
                expected_module="general",
                description="無關內容測試",
                category="edge_case",
                expected_confidence_range=(0.0, 0.4)
            ),
            TestCase(
                input_text="失智症患者需要專業醫療照護和社會支持",
                expected_module="M4",
                description="複雜描述測試",
                category="edge_case",
                expected_confidence_range=(0.7, 0.9)
            )
        ]
        
        # 效能基準
        self.performance_benchmarks = {
            "immediate": {"target": 1.0, "acceptable": 1.5},
            "quick": {"target": 3.0, "acceptable": 4.0},
            "detailed": {"target": 5.0, "acceptable": 6.0}
        }
    
    def test_single_case(self, test_case: TestCase, stage: str = "immediate") -> Dict[str, Any]:
        """測試單一案例"""
        start_time = time.time()
        
        try:
            response = requests.post(
                self.xai_wrapper_url,
                json={
                    "user_input": test_case.input_text,
                    "user_id": "test_user",
                    "stage": stage
                },
                timeout=10
            )
            
            response_time = time.time() - start_time
            response.raise_for_status()
            
            data = response.json()
            xai_data = data.get("xai_enhanced", {})
            
            # 驗證結果
            actual_module = xai_data.get("module", "unknown")
            actual_confidence = xai_data.get("confidence", 0.0)
            expected_min, expected_max = test_case.expected_confidence_range
            
            # 評估結果
            module_correct = actual_module == test_case.expected_module
            confidence_in_range = expected_min <= actual_confidence <= expected_max
            performance_ok = response_time <= self.performance_benchmarks[stage]["acceptable"]
            
            return {
                "test_case": test_case.description,
                "input": test_case.input_text,
                "expected_module": test_case.expected_module,
                "actual_module": actual_module,
                "module_correct": module_correct,
                "expected_confidence_range": test_case.expected_confidence_range,
                "actual_confidence": actual_confidence,
                "confidence_in_range": confidence_in_range,
                "response_time": response_time,
                "performance_ok": performance_ok,
                "stage": stage,
                "success": module_correct and confidence_in_range and performance_ok
            }
            
        except Exception as e:
            return {
                "test_case": test_case.description,
                "input": test_case.input_text,
                "error": str(e),
                "response_time": time.time() - start_time,
                "success": False
            }
    
    def run_comprehensive_test(self, iterations: int = 3) -> Dict[str, Any]:
        """執行綜合測試"""
        print("🧪 開始綜合測試...")
        print(f"📊 測試案例數量: {len(self.test_cases)}")
        print(f"🔄 每案例重複次數: {iterations}")
        print("="*60)
        
        all_results = []
        
        # 測試主要案例
        for i, test_case in enumerate(self.test_cases, 1):
            print(f"\n📋 測試案例 {i}/{len(self.test_cases)}: {test_case.description}")
            print(f"   輸入: {test_case.input_text}")
            print(f"   預期模組: {test_case.expected_module}")
            
            case_results = []
            for j in range(iterations):
                print(f"   迭代 {j+1}/{iterations}...", end=" ")
                
                # 測試即時階段
                immediate_result = self.test_single_case(test_case, "immediate")
                case_results.append(immediate_result)
                
                # 測試快速階段
                quick_result = self.test_single_case(test_case, "quick")
                case_results.append(quick_result)
                
                print(f"✓ ({immediate_result.get('response_time', 0):.2f}s, {quick_result.get('response_time', 0):.2f}s)")
                
                # 短暫休息
                time.sleep(0.5)
            
            all_results.extend(case_results)
        
        # 測試邊界案例
        print(f"\n🔍 測試邊界案例...")
        for edge_case in self.edge_cases:
            print(f"   邊界測試: {edge_case.description}")
            edge_result = self.test_single_case(edge_case, "immediate")
            all_results.append(edge_result)
        
        return self.analyze_test_results(all_results)
    
    def analyze_test_results(self, results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """分析測試結果"""
        if not results:
            return {"error": "No test results available"}
        
        # 分類結果
        successful_results = [r for r in results if r.get("success", False)]
        failed_results = [r for r in results if not r.get("success", False)]
        
        # 按模組分組
        module_results = {}
        for result in results:
            module = result.get("actual_module", "unknown")
            if module not in module_results:
                module_results[module] = []
            module_results[module].append(result)
        
        # 按階段分組
        stage_results = {}
        for result in results:
            stage = result.get("stage", "unknown")
            if stage not in stage_results:
                stage_results[stage] = []
            stage_results[stage].append(result)
        
        # 計算統計數據
        response_times = [r.get("response_time", 0) for r in results if "response_time" in r]
        confidences = [r.get("actual_confidence", 0) for r in results if "actual_confidence" in r]
        
        analysis = {
            "summary": {
                "total_tests": len(results),
                "successful_tests": len(successful_results),
                "failed_tests": len(failed_results),
                "success_rate": len(successful_results) / len(results) if results else 0,
                "average_response_time": statistics.mean(response_times) if response_times else 0,
                "median_response_time": statistics.median(response_times) if response_times else 0,
                "average_confidence": statistics.mean(confidences) if confidences else 0
            },
            "by_module": {},
            "by_stage": {},
            "performance_analysis": {},
            "detailed_results": results
        }
        
        # 按模組分析
        for module, module_data in module_results.items():
            module_success = len([r for r in module_data if r.get("success", False)])
            module_response_times = [r.get("response_time", 0) for r in module_data if "response_time" in r]
            
            analysis["by_module"][module] = {
                "count": len(module_data),
                "success_count": module_success,
                "success_rate": module_success / len(module_data) if module_data else 0,
                "average_response_time": statistics.mean(module_response_times) if module_response_times else 0
            }
        
        # 按階段分析
        for stage, stage_data in stage_results.items():
            stage_response_times = [r.get("response_time", 0) for r in stage_data if "response_time" in r]
            target_time = self.performance_benchmarks.get(stage, {}).get("target", 5.0)
            
            analysis["by_stage"][stage] = {
                "count": len(stage_data),
                "average_response_time": statistics.mean(stage_response_times) if stage_response_times else 0,
                "target_time": target_time,
                "target_met": all(rt <= target_time for rt in stage_response_times) if stage_response_times else False
            }
        
        # 效能分析
        for stage in ["immediate", "quick", "detailed"]:
            if stage in stage_results:
                stage_times = [r.get("response_time", 0) for r in stage_results[stage] if "response_time" in r]
                if stage_times:
                    analysis["performance_analysis"][stage] = {
                        "average_time": statistics.mean(stage_times),
                        "target_time": self.performance_benchmarks[stage]["target"],
                        "acceptable_time": self.performance_benchmarks[stage]["acceptable"],
                        "target_met": all(t <= self.performance_benchmarks[stage]["target"] for t in stage_times),
                        "acceptable_met": all(t <= self.performance_benchmarks[stage]["acceptable"] for t in stage_times)
                    }
        
        return analysis
    
    def print_test_report(self, analysis: Dict[str, Any]) -> None:
        """打印測試報告"""
        print("\n" + "="*80)
        print("📊 XAI 系統實測報告")
        print("="*80)
        
        summary = analysis["summary"]
        print(f"\n🎯 整體測試結果:")
        print(f"   總測試數: {summary['total_tests']}")
        print(f"   成功測試: {summary['successful_tests']}")
        print(f"   失敗測試: {summary['failed_tests']}")
        print(f"   成功率: {summary['success_rate']:.1%}")
        print(f"   平均回應時間: {summary['average_response_time']:.2f}秒")
        print(f"   平均信心度: {summary['average_confidence']:.1%}")
        
        # 按模組分析
        print(f"\n🧠 模組分析:")
        for module, data in analysis["by_module"].items():
            status = "✅" if data["success_rate"] > 0.8 else "⚠️" if data["success_rate"] > 0.6 else "❌"
            print(f"   {status} {module}: {data['count']} 測試, 成功率 {data['success_rate']:.1%}, 平均時間 {data['average_response_time']:.2f}s")
        
        # 按階段分析
        print(f"\n⚡ 階段分析:")
        for stage, data in analysis["by_stage"].items():
            target_status = "✅" if data["target_met"] else "❌"
            print(f"   {target_status} {stage.upper()}: {data['count']} 測試, 平均時間 {data['average_response_time']:.2f}s / 目標 {data['target_time']}s")
        
        # 效能分析
        print(f"\n🎯 效能目標達成:")
        for stage, data in analysis["performance_analysis"].items():
            target_icon = "✅" if data["target_met"] else "❌"
            acceptable_icon = "✅" if data["acceptable_met"] else "❌"
            print(f"   {target_icon} {stage.upper()}: {data['average_time']:.2f}s / {data['target_time']}s (目標) / {data['acceptable_time']}s (可接受)")
        
        # 建議
        print(f"\n💡 改進建議:")
        if summary["success_rate"] < 0.9:
            print("   ⚠️  成功率低於 90%，建議檢查模組檢測邏輯")
        if summary["average_response_time"] > 2.0:
            print("   ⚠️  平均回應時間過長，建議優化效能")
        
        # 檢查各階段效能
        for stage, data in analysis["performance_analysis"].items():
            if not data["target_met"]:
                print(f"   ⚠️  {stage.upper()} 階段未達目標時間，建議優化")
        
        print("="*80)
    
    def generate_test_data(self) -> Dict[str, Any]:
        """生成測試數據"""
        return {
            "test_cases": [
                {
                    "input": tc.input_text,
                    "expected_module": tc.expected_module,
                    "description": tc.description,
                    "category": tc.category,
                    "confidence_range": tc.expected_confidence_range
                }
                for tc in self.test_cases
            ],
            "edge_cases": [
                {
                    "input": tc.input_text,
                    "expected_module": tc.expected_module,
                    "description": tc.description,
                    "category": tc.category,
                    "confidence_range": tc.expected_confidence_range
                }
                for tc in self.edge_cases
            ],
            "performance_benchmarks": self.performance_benchmarks
        }
    
    def save_test_results(self, analysis: Dict[str, Any], filename: str = None) -> str:
        """保存測試結果"""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"xai_test_results_{timestamp}.json"
        
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(analysis, f, indent=2, ensure_ascii=False, default=str)
        
        return filename

def main():
    """主函數"""
    tester = XAITestMaterials()
    
    print("🧪 XAI 系統實測素材")
    print("="*50)
    
    # 檢查系統健康狀態
    print("\n🔍 檢查系統健康狀態...")
    try:
        health_response = requests.get("http://localhost:8009/health", timeout=5)
        if health_response.status_code == 200:
            print("✅ XAI Wrapper 服務正常")
        else:
            print("❌ XAI Wrapper 服務異常")
            return
    except Exception as e:
        print(f"❌ 無法連接到 XAI Wrapper: {e}")
        return
    
    # 執行綜合測試
    print("\n🚀 開始執行綜合測試...")
    analysis = tester.run_comprehensive_test(iterations=2)
    
    # 打印報告
    tester.print_test_report(analysis)
    
    # 保存結果
    filename = tester.save_test_results(analysis)
    print(f"\n💾 測試結果已保存至: {filename}")
    
    # 生成測試數據
    test_data = tester.generate_test_data()
    test_data_filename = f"test_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(test_data_filename, "w", encoding="utf-8") as f:
        json.dump(test_data, f, indent=2, ensure_ascii=False)
    print(f"📋 測試數據已保存至: {test_data_filename}")

if __name__ == "__main__":
    main() 