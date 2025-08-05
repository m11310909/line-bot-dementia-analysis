"""
🔗 增強版 M1 Flex Message 整合腳本
將新的設計整合到現有的 LINE Bot 系統中
"""

import json
import logging
import requests
from typing import Dict, Any, Optional
from datetime import datetime

# 配置日誌
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class EnhancedM1Integrator:
    """增強版 M1 整合器"""
    
    def __init__(self):
        self.enhanced_api_url = "http://localhost:8002"
        self.line_bot_url = "https://4edba6125304.ngrok-free.app/webhook"
        
    def test_enhanced_api(self) -> bool:
        """測試增強版 API 是否正常運作"""
        try:
            response = requests.get(f"{self.enhanced_api_url}/health", timeout=5)
            if response.status_code == 200:
                logger.info("✅ 增強版 M1 API 正常運作")
                return True
            else:
                logger.error(f"❌ 增強版 M1 API 回應異常：{response.status_code}")
                return False
        except Exception as e:
            logger.error(f"❌ 無法連接到增強版 M1 API：{e}")
            return False
    
    def analyze_with_enhanced_m1(self, user_input: str) -> Optional[Dict[str, Any]]:
        """使用增強版 M1 分析用戶輸入"""
        try:
            response = requests.post(
                f"{self.enhanced_api_url}/analyze",
                json={"user_input": user_input},
                headers={"Content-Type": "application/json"},
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                logger.info(f"✅ 增強版 M1 分析成功")
                return result
            else:
                logger.error(f"❌ 增強版 M1 分析失敗：{response.status_code}")
                return None
                
        except Exception as e:
            logger.error(f"❌ 增強版 M1 分析請求失敗：{e}")
            return None
    
    def get_enhanced_stats(self) -> Optional[Dict[str, Any]]:
        """取得增強版 API 統計"""
        try:
            response = requests.get(f"{self.enhanced_api_url}/stats", timeout=5)
            if response.status_code == 200:
                return response.json()
            else:
                return None
        except Exception as e:
            logger.error(f"❌ 無法取得統計：{e}")
            return None
    
    def create_integration_report(self) -> Dict[str, Any]:
        """創建整合報告"""
        
        report = {
            "timestamp": datetime.now().isoformat(),
            "enhanced_api_status": "unknown",
            "test_results": [],
            "integration_status": "pending"
        }
        
        # 測試增強版 API
        if self.test_enhanced_api():
            report["enhanced_api_status"] = "healthy"
            
            # 測試分析功能
            test_cases = [
                "媽媽最近常重複問同樣的問題",
                "爸爸忘記關瓦斯爐",
                "爺爺偶爾忘記鑰匙放哪裡"
            ]
            
            for test_input in test_cases:
                result = self.analyze_with_enhanced_m1(test_input)
                if result:
                    report["test_results"].append({
                        "input": test_input,
                        "success": True,
                        "flex_message_size": len(json.dumps(result["flex_message"], ensure_ascii=False)),
                        "detected_signs": result["analysis_data"]["detected_signs"]
                    })
                else:
                    report["test_results"].append({
                        "input": test_input,
                        "success": False
                    })
            
            # 取得統計
            stats = self.get_enhanced_stats()
            if stats:
                report["generator_stats"] = stats["generator_stats"]
            
            report["integration_status"] = "success"
        else:
            report["enhanced_api_status"] = "unhealthy"
            report["integration_status"] = "failed"
        
        return report

def main():
    """主函數"""
    print("🔗 增強版 M1 Flex Message 整合測試")
    print("=" * 50)
    
    integrator = EnhancedM1Integrator()
    
    # 創建整合報告
    report = integrator.create_integration_report()
    
    # 顯示報告
    print(f"\n📊 整合報告")
    print(f"時間戳記：{report['timestamp']}")
    print(f"增強版 API 狀態：{report['enhanced_api_status']}")
    print(f"整合狀態：{report['integration_status']}")
    
    if "test_results" in report:
        print(f"\n🧪 測試結果：")
        for i, test_result in enumerate(report["test_results"], 1):
            print(f"  測試 {i}：{test_result['input']}")
            if test_result["success"]:
                print(f"    ✅ 成功 - 檢測到 {len(test_result['detected_signs'])} 個警訊")
                print(f"    📏 Flex Message 大小：{test_result['flex_message_size']} 字符")
            else:
                print(f"    ❌ 失敗")
    
    if "generator_stats" in report:
        stats = report["generator_stats"]
        print(f"\n📈 生成統計：")
        print(f"  總生成次數：{stats['total_generated']}")
        print(f"  錯誤次數：{stats['error_count']}")
        print(f"  成功率：{stats['success_rate']:.1f}%")
        print(f"  風險等級分布：{stats['risk_levels']}")
    
    # 保存報告
    report_file = f"enhanced_m1_integration_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(report_file, 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    
    print(f"\n💾 報告已保存至：{report_file}")
    
    # 顯示下一步建議
    if report["integration_status"] == "success":
        print(f"\n🎉 整合成功！")
        print(f"📋 下一步建議：")
        print(f"  1. 更新 LINE Bot Webhook 處理邏輯")
        print(f"  2. 整合到現有的 M1 模組中")
        print(f"  3. 測試實際的 LINE Bot 訊息")
        print(f"  4. 部署到生產環境")
    else:
        print(f"\n⚠️ 整合失敗，請檢查：")
        print(f"  1. 增強版 M1 API 是否正在運行")
        print(f"  2. 網路連線是否正常")
        print(f"  3. API 端點是否正確")

if __name__ == "__main__":
    main() 