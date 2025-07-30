#!/usr/bin/env python3
"""
Comprehensive Testing Script for M1-M3 Modules on LINE
測試 M1-M3 模組的完整腳本
"""

import requests
import json
import time
import os
from datetime import datetime

class M1M2M3ModuleTester:
    """M1-M3 模組測試器"""
    
    def __init__(self, base_url="http://localhost:8005"):
        self.base_url = base_url
        self.test_results = []
        
    def test_health_check(self):
        """測試健康檢查"""
        print("🏥 測試健康檢查...")
        try:
            response = requests.get(f"{self.base_url}/health", timeout=10)
            if response.status_code == 200:
                data = response.json()
                print(f"✅ 健康檢查通過")
                print(f"   狀態: {data.get('status')}")
                print(f"   引擎資訊: {data.get('engine_info', {})}")
                return True
            else:
                print(f"❌ 健康檢查失敗: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ 健康檢查錯誤: {e}")
            return False
    
    def test_module_status(self):
        """測試模組狀態"""
        print("\n📋 測試模組狀態...")
        try:
            response = requests.get(f"{self.base_url}/modules/status", timeout=10)
            if response.status_code == 200:
                data = response.json()
                modules = data.get('modules', {})
                print("✅ 模組狀態:")
                for module_id, info in modules.items():
                    status = "🟢" if info.get('status') == 'active' else "🔴"
                    print(f"   {status} {module_id}: {info.get('name')} ({info.get('chunks')} chunks)")
                return True
            else:
                print(f"❌ 模組狀態檢查失敗: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ 模組狀態檢查錯誤: {e}")
            return False
    
    def test_m1_warning_signs(self):
        """測試 M1 警訊識別"""
        print("\n🚨 測試 M1 警訊識別...")
        
        test_cases = [
            "媽媽常忘記關瓦斯",
            "爸爸會迷路找不到回家的路",
            "奶奶忘記吃藥",
            "爺爺無法處理財務",
            "外婆對時間地點感到混亂"
        ]
        
        passed = 0
        for i, test_input in enumerate(test_cases, 1):
            print(f"   測試 {i}: {test_input}")
            try:
                response = requests.post(
                    f"{self.base_url}/comprehensive-analysis",
                    json={"user_input": test_input},
                    timeout=15
                )
                
                if response.status_code == 200:
                    data = response.json()
                    analysis = data.get('comprehensive_analysis', {})
                    matched_codes = analysis.get('matched_codes', [])
                    modules_used = analysis.get('modules_used', [])
                    
                    if 'M1' in modules_used:
                        print(f"      ✅ M1 檢測成功: {matched_codes}")
                        passed += 1
                    else:
                        print(f"      ⚠️  未檢測到 M1 模組")
                else:
                    print(f"      ❌ 請求失敗: {response.status_code}")
                    
            except Exception as e:
                print(f"      ❌ 測試錯誤: {e}")
        
        print(f"   📊 M1 測試結果: {passed}/{len(test_cases)} 通過")
        return passed > 0
    
    def test_m2_stage_analysis(self):
        """測試 M2 階段分析"""
        print("\n🏥 測試 M2 階段分析...")
        
        test_cases = [
            ("輕度症狀", "可以自己洗澡但需要提醒吃藥"),
            ("中度症狀", "需要協助穿衣，會迷路，晚上不睡覺"),
            ("重度症狀", "已經不認得家人，需要餵食")
        ]
        
        passed = 0
        for stage, test_input in test_cases:
            print(f"   測試 {stage}: {test_input}")
            try:
                response = requests.post(
                    f"{self.base_url}/comprehensive-analysis",
                    json={"user_input": test_input},
                    timeout=15
                )
                
                if response.status_code == 200:
                    data = response.json()
                    analysis = data.get('comprehensive_analysis', {})
                    stage_detection = analysis.get('stage_detection', {})
                    modules_used = analysis.get('modules_used', [])
                    
                    if 'M2' in modules_used and stage_detection:
                        detected_stage = stage_detection.get('detected_stage', '')
                        confidence = stage_detection.get('confidence', 0)
                        print(f"      ✅ M2 階段檢測: {detected_stage} (信心度: {confidence:.3f})")
                        passed += 1
                    else:
                        print(f"      ⚠️  未檢測到 M2 階段資訊")
                else:
                    print(f"      ❌ 請求失敗: {response.status_code}")
                    
            except Exception as e:
                print(f"      ❌ 測試錯誤: {e}")
        
        print(f"   📊 M2 測試結果: {passed}/{len(test_cases)} 通過")
        return passed > 0
    
    def test_m3_bpsd_symptoms(self):
        """測試 M3 BPSD 症狀分析"""
        print("\n🧠 測試 M3 BPSD 症狀分析...")
        
        test_cases = [
            ("妄想症狀", "懷疑有人偷東西"),
            ("幻覺症狀", "看到已故的親人"),
            ("激動行為", "大聲叫罵，推人"),
            ("憂鬱焦慮", "整天悶悶不樂，擔心"),
            ("睡眠障礙", "晚上不睡覺，到處走動")
        ]
        
        passed = 0
        for symptom, test_input in test_cases:
            print(f"   測試 {symptom}: {test_input}")
            try:
                response = requests.post(
                    f"{self.base_url}/comprehensive-analysis",
                    json={"user_input": test_input},
                    timeout=15
                )
                
                if response.status_code == 200:
                    data = response.json()
                    analysis = data.get('comprehensive_analysis', {})
                    bpsd_analysis = analysis.get('bpsd_analysis', {})
                    modules_used = analysis.get('modules_used', [])
                    
                    if 'M3' in modules_used and bpsd_analysis:
                        detected_categories = bpsd_analysis.get('detected_categories', [])
                        print(f"      ✅ M3 BPSD 檢測: {detected_categories}")
                        passed += 1
                    else:
                        print(f"      ⚠️  未檢測到 M3 BPSD 資訊")
                else:
                    print(f"      ❌ 請求失敗: {response.status_code}")
                    
            except Exception as e:
                print(f"      ❌ 測試錯誤: {e}")
        
        print(f"   📊 M3 測試結果: {passed}/{len(test_cases)} 通過")
        return passed > 0
    
    def test_flex_message_generation(self):
        """測試 Flex Message 生成"""
        print("\n🎨 測試 Flex Message 生成...")
        
        test_input = "媽媽常忘記關瓦斯，需要協助穿衣"
        
        try:
            response = requests.post(
                f"{self.base_url}/m1-flex",
                json={"user_input": test_input},
                timeout=15
            )
            
            if response.status_code == 200:
                data = response.json()
                flex_message = data.get('flex_message', {})
                
                if flex_message and flex_message.get('type') == 'flex':
                    print("      ✅ Flex Message 生成成功")
                    print(f"      類型: {flex_message.get('type')}")
                    print(f"      內容結構: {list(flex_message.keys())}")
                    return True
                else:
                    print("      ⚠️  Flex Message 格式不正確")
                    return False
            else:
                print(f"      ❌ Flex Message 生成失敗: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"      ❌ Flex Message 測試錯誤: {e}")
            return False
    
    def test_line_bot_integration(self):
        """測試 LINE Bot 整合"""
        print("\n🤖 測試 LINE Bot 整合...")
        
        # 檢查 LINE Bot 相關檔案
        line_bot_files = [
            "updated_line_bot_webhook.py",
            "enhanced_line_bot.py",
            "line_bot_app.py"
        ]
        
        found_files = []
        for file in line_bot_files:
            if os.path.exists(file):
                found_files.append(file)
        
        if found_files:
            print(f"      ✅ 找到 LINE Bot 檔案: {', '.join(found_files)}")
            return True
        else:
            print("      ❌ 未找到 LINE Bot 檔案")
            return False
    
    def run_comprehensive_test(self):
        """執行完整測試套件"""
        print("🚀 M1-M3 模組完整測試")
        print("=" * 50)
        print(f"測試時間: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"測試目標: {self.base_url}")
        print()
        
        tests = [
            ("健康檢查", self.test_health_check),
            ("模組狀態", self.test_module_status),
            ("M1 警訊識別", self.test_m1_warning_signs),
            ("M2 階段分析", self.test_m2_stage_analysis),
            ("M3 BPSD 症狀", self.test_m3_bpsd_symptoms),
            ("Flex Message", self.test_flex_message_generation),
            ("LINE Bot 整合", self.test_line_bot_integration)
        ]
        
        results = {}
        for test_name, test_func in tests:
            try:
                result = test_func()
                results[test_name] = result
                status = "✅ 通過" if result else "❌ 失敗"
                print(f"{status} {test_name}")
            except Exception as e:
                print(f"❌ {test_name} 執行錯誤: {e}")
                results[test_name] = False
        
        # 生成測試報告
        print("\n" + "=" * 50)
        print("📊 測試報告")
        print("=" * 50)
        
        passed = sum(1 for result in results.values() if result)
        total = len(results)
        
        print(f"總測試數: {total}")
        print(f"通過數: {passed}")
        print(f"失敗數: {total - passed}")
        print(f"成功率: {passed/total*100:.1f}%")
        
        print("\n詳細結果:")
        for test_name, result in results.items():
            status = "✅" if result else "❌"
            print(f"  {status} {test_name}")
        
        if passed == total:
            print("\n🎉 所有測試通過！M1-M3 模組運行正常")
        else:
            print(f"\n⚠️  {total - passed} 個測試失敗，請檢查相關配置")
        
        return results

def main():
    """主函數"""
    import sys
    
    # 檢查命令行參數
    if len(sys.argv) > 1:
        base_url = sys.argv[1]
    else:
        base_url = "http://localhost:8005"
    
    # 創建測試器
    tester = M1M2M3ModuleTester(base_url)
    
    # 執行測試
    results = tester.run_comprehensive_test()
    
    # 返回測試結果
    return all(results.values())

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1) 