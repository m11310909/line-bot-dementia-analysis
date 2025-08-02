#!/usr/bin/env python3
"""
📊 Performance Monitor for Optimized XAI System
Monitors response times, cache hit rates, and system performance
"""

import time
import requests
import statistics
from typing import Dict, List, Any
from dataclasses import dataclass
from datetime import datetime
import json

@dataclass
class PerformanceMetrics:
    """效能指標"""
    response_time: float
    cache_hit: bool
    module: str
    stage: str
    confidence: float
    timestamp: datetime

class XAIPerformanceMonitor:
    """XAI 系統效能監控器"""
    
    def __init__(self):
        self.metrics: List[PerformanceMetrics] = []
        self.xai_wrapper_url = "http://localhost:8009/analyze"
        self.test_cases = [
            {
                "input": "爸爸不會用洗衣機",
                "expected_module": "M1",
                "description": "M1 Warning Signs"
            },
            {
                "input": "媽媽中度失智",
                "expected_module": "M2",
                "description": "M2 Progression"
            },
            {
                "input": "爺爺有妄想症狀",
                "expected_module": "M3",
                "description": "M3 BPSD Symptoms"
            },
            {
                "input": "需要醫療協助",
                "expected_module": "M4",
                "description": "M4 Care Navigation"
            }
        ]
    
    def test_response_time(self, user_input: str, stage: str = "immediate") -> PerformanceMetrics:
        """測試回應時間"""
        start_time = time.time()
        
        try:
            response = requests.post(
                self.xai_wrapper_url,
                json={
                    "user_input": user_input,
                    "user_id": "test_user",
                    "stage": stage
                },
                timeout=10
            )
            
            response_time = time.time() - start_time
            response.raise_for_status()
            
            data = response.json()
            xai_data = data.get("xai_enhanced", {})
            
            return PerformanceMetrics(
                response_time=response_time,
                cache_hit=False,  # 需要從日誌判斷
                module=xai_data.get("module", "unknown"),
                stage=stage,
                confidence=xai_data.get("confidence", 0.0),
                timestamp=datetime.now()
            )
            
        except Exception as e:
            print(f"❌ Test failed: {e}")
            return PerformanceMetrics(
                response_time=time.time() - start_time,
                cache_hit=False,
                module="error",
                stage=stage,
                confidence=0.0,
                timestamp=datetime.now()
            )
    
    def run_performance_test(self, iterations: int = 5) -> Dict[str, Any]:
        """執行效能測試"""
        print(f"🧪 Running performance test with {iterations} iterations per test case...")
        
        all_metrics = []
        
        for test_case in self.test_cases:
            print(f"\n📊 Testing: {test_case['description']}")
            
            case_metrics = []
            for i in range(iterations):
                print(f"  Iteration {i+1}/{iterations}...", end=" ")
                
                # 測試即時階段
                immediate_metric = self.test_response_time(test_case["input"], "immediate")
                case_metrics.append(immediate_metric)
                
                # 測試快速階段
                quick_metric = self.test_response_time(test_case["input"], "quick")
                case_metrics.append(quick_metric)
                
                print(f"✓ ({immediate_metric.response_time:.2f}s, {quick_metric.response_time:.2f}s)")
                
                # 短暫休息避免過載
                time.sleep(0.5)
            
            all_metrics.extend(case_metrics)
        
        return self.analyze_metrics(all_metrics)
    
    def analyze_metrics(self, metrics: List[PerformanceMetrics]) -> Dict[str, Any]:
        """分析效能指標"""
        if not metrics:
            return {"error": "No metrics available"}
        
        # 按模組分組
        module_metrics = {}
        stage_metrics = {}
        
        for metric in metrics:
            # 按模組分組
            if metric.module not in module_metrics:
                module_metrics[metric.module] = []
            module_metrics[metric.module].append(metric)
            
            # 按階段分組
            if metric.stage not in stage_metrics:
                stage_metrics[metric.stage] = []
            stage_metrics[metric.stage].append(metric)
        
        # 計算統計數據
        analysis = {
            "overall": {
                "total_tests": len(metrics),
                "average_response_time": statistics.mean([m.response_time for m in metrics]),
                "median_response_time": statistics.median([m.response_time for m in metrics]),
                "min_response_time": min([m.response_time for m in metrics]),
                "max_response_time": max([m.response_time for m in metrics]),
                "success_rate": len([m for m in metrics if m.module != "error"]) / len(metrics)
            },
            "by_module": {},
            "by_stage": {},
            "performance_targets": {
                "immediate_target": 1.0,  # <1秒
                "quick_target": 3.0,      # <3秒
                "detailed_target": 5.0    # <5秒
            }
        }
        
        # 按模組分析
        for module, module_data in module_metrics.items():
            response_times = [m.response_time for m in module_data]
            analysis["by_module"][module] = {
                "count": len(module_data),
                "average_response_time": statistics.mean(response_times),
                "median_response_time": statistics.median(response_times),
                "min_response_time": min(response_times),
                "max_response_time": max(response_times),
                "success_rate": len([m for m in module_data if m.module != "error"]) / len(module_data)
            }
        
        # 按階段分析
        for stage, stage_data in stage_metrics.items():
            response_times = [m.response_time for m in stage_data]
            analysis["by_stage"][stage] = {
                "count": len(stage_data),
                "average_response_time": statistics.mean(response_times),
                "median_response_time": statistics.median(response_times),
                "min_response_time": min(response_times),
                "max_response_time": max(response_times),
                "target_met": all(rt < analysis["performance_targets"][f"{stage}_target"] for rt in response_times)
            }
        
        return analysis
    
    def print_performance_report(self, analysis: Dict[str, Any]) -> None:
        """打印效能報告"""
        print("\n" + "="*60)
        print("📊 XAI System Performance Report")
        print("="*60)
        
        # 整體統計
        overall = analysis["overall"]
        print(f"\n🎯 Overall Performance:")
        print(f"   Total Tests: {overall['total_tests']}")
        print(f"   Success Rate: {overall['success_rate']:.1%}")
        print(f"   Average Response Time: {overall['average_response_time']:.2f}s")
        print(f"   Median Response Time: {overall['median_response_time']:.2f}s")
        print(f"   Response Time Range: {overall['min_response_time']:.2f}s - {overall['max_response_time']:.2f}s")
        
        # 按模組分析
        print(f"\n🧠 Performance by Module:")
        for module, data in analysis["by_module"].items():
            print(f"   {module}:")
            print(f"     Count: {data['count']}")
            print(f"     Avg Response Time: {data['average_response_time']:.2f}s")
            print(f"     Success Rate: {data['success_rate']:.1%}")
        
        # 按階段分析
        print(f"\n⚡ Performance by Stage:")
        for stage, data in analysis["by_stage"].items():
            target_met = "✅" if data["target_met"] else "❌"
            print(f"   {stage.upper()}:")
            print(f"     Count: {data['count']}")
            print(f"     Avg Response Time: {data['average_response_time']:.2f}s")
            print(f"     Target Met: {target_met}")
        
        # 效能目標檢查
        print(f"\n🎯 Performance Targets:")
        targets = analysis["performance_targets"]
        for stage in ["immediate", "quick", "detailed"]:
            if stage in analysis["by_stage"]:
                avg_time = analysis["by_stage"][stage]["average_response_time"]
                target = targets[f"{stage}_target"]
                status = "✅" if avg_time < target else "❌"
                print(f"   {stage.upper()}: {avg_time:.2f}s / {target}s {status}")
        
        # 建議
        print(f"\n💡 Recommendations:")
        if overall["average_response_time"] > 2.0:
            print("   ⚠️  Average response time is high. Consider optimization.")
        if overall["success_rate"] < 0.95:
            print("   ⚠️  Success rate is below 95%. Check system stability.")
        
        # 檢查各階段效能
        for stage in ["immediate", "quick"]:
            if stage in analysis["by_stage"]:
                avg_time = analysis["by_stage"][stage]["average_response_time"]
                target = targets[f"{stage}_target"]
                if avg_time > target:
                    print(f"   ⚠️  {stage.upper()} stage is slower than target ({avg_time:.2f}s > {target}s)")
        
        print("="*60)
    
    def monitor_system_health(self) -> Dict[str, Any]:
        """監控系統健康狀態"""
        health_checks = {
            "xai_wrapper": "http://localhost:8009/health",
            "chatbot_api": "http://localhost:8008/health",
            "line_bot": "http://localhost:8081/health"
        }
        
        health_status = {}
        
        for service, url in health_checks.items():
            try:
                start_time = time.time()
                response = requests.get(url, timeout=5)
                response_time = time.time() - start_time
                
                health_status[service] = {
                    "status": "healthy" if response.status_code == 200 else "unhealthy",
                    "response_time": response_time,
                    "status_code": response.status_code
                }
            except Exception as e:
                health_status[service] = {
                    "status": "error",
                    "error": str(e),
                    "response_time": None
                }
        
        return health_status
    
    def print_health_report(self, health_status: Dict[str, Any]) -> None:
        """打印健康報告"""
        print("\n🏥 System Health Report:")
        print("="*40)
        
        for service, status in health_status.items():
            if status["status"] == "healthy":
                print(f"   ✅ {service.upper()}: Healthy ({status['response_time']:.2f}s)")
            elif status["status"] == "unhealthy":
                print(f"   ⚠️  {service.upper()}: Unhealthy (Status: {status['status_code']})")
            else:
                print(f"   ❌ {service.upper()}: Error ({status.get('error', 'Unknown')})")

def main():
    """主函數"""
    monitor = XAIPerformanceMonitor()
    
    print("🚀 XAI System Performance Monitor")
    print("="*50)
    
    # 檢查系統健康狀態
    print("\n🔍 Checking system health...")
    health_status = monitor.monitor_system_health()
    monitor.print_health_report(health_status)
    
    # 檢查所有服務是否健康
    unhealthy_services = [s for s, status in health_status.items() if status["status"] != "healthy"]
    if unhealthy_services:
        print(f"\n❌ Unhealthy services detected: {unhealthy_services}")
        print("Please ensure all services are running before performance testing.")
        return
    
    # 執行效能測試
    print("\n🧪 Starting performance test...")
    analysis = monitor.run_performance_test(iterations=3)
    
    # 打印報告
    monitor.print_performance_report(analysis)
    
    # 保存結果
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"performance_report_{timestamp}.json"
    
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(analysis, f, indent=2, default=str)
    
    print(f"\n💾 Performance report saved to: {filename}")

if __name__ == "__main__":
    main() 