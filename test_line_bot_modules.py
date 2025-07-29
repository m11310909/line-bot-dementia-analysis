#!/usr/bin/env python3
"""
LINE Bot M1-M3 模組測試腳本
測試 LINE Bot 與 M1-M3 模組的整合
"""

import requests
import json
import time
import os
from datetime import datetime

class LINEBotModuleTester:
    """LINE Bot 模組測試器"""
    
    def __init__(self, line_bot_url="http://localhost:5000"):
        self.line_bot_url = line_bot_url
        self.test_messages = [
            # M1 測試訊息
            "媽媽常忘記關瓦斯",
            "爸爸會迷路找不到回家的路", 
            "奶奶忘記吃藥",
            "爺爺無法處理財務",
            
            # M2 測試訊息
            "可以自己洗澡但需要提醒吃藥",
            "需要協助穿衣，會迷路，晚上不睡覺",
            "已經不認得家人，需要餵食",
            
            # M3 測試訊息
            "懷疑有人偷東西",
            "看到已故的親人",
            "大聲叫罵，推人",
            "整天悶悶不樂，擔心",
            "晚上不睡覺，到處走動"
        ]
    
    def test_line_bot_health(self):
        """測試 LINE Bot 健康狀態"""
        print("🏥 測試 LINE Bot 健康狀態...")
        try:
            response = requests.get(f"{self.line_bot_url}/health", timeout=10)
            if response.status_code == 200:
                data = response.json()
                print(f"✅ LINE Bot 健康檢查通過")
                print(f"   狀態: {data.get('status')}")
                return True
            else:
                print(f"❌ LINE Bot 健康檢查失敗: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ LINE Bot 健康檢查錯誤: {e}")
            return False
    
    def test_line_bot_info(self):
        """測試 LINE Bot 基本資訊"""
        print("\n📋 測試 LINE Bot 基本資訊...")
        try:
            response = requests.get(f"{self.line_bot_url}/", timeout=10)
            if response.status_code == 200:
                data = response.json()
                print(f"✅ LINE Bot 資訊:")
                print(f"   版本: {data.get('version', 'N/A')}")
                print(f"   狀態: {data.get('status', 'N/A')}")
                features = data.get('features', [])
                if features:
                    print("   功能:")
                    for feature in features[:3]:  # 只顯示前3個
                        print(f"     - {feature}")
                return True
            else:
                print(f"❌ LINE Bot 資訊獲取失敗: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ LINE Bot 資訊測試錯誤: {e}")
            return False
    
    def test_message_processing(self):
        """測試訊息處理"""
        print("\n💬 測試訊息處理...")
        
        passed = 0
        total = len(self.test_messages)
        
        for i, message in enumerate(self.test_messages, 1):
            print(f"   測試 {i}/{total}: {message[:30]}...")
            try:
                # 模擬 LINE Bot 訊息處理
                response = requests.post(
                    f"{self.line_bot_url}/webhook",
                    json={
                        "events": [{
                            "type": "message",
                            "message": {
                                "type": "text",
                                "text": message
                            },
                            "source": {
                                "userId": "test_user_123"
                            }
                        }]
                    },
                    timeout=15
                )
                
                if response.status_code in [200, 204]:
                    print(f"      ✅ 訊息處理成功")
                    passed += 1
                else:
                    print(f"      ❌ 訊息處理失敗: {response.status_code}")
                    
            except Exception as e:
                print(f"      ❌ 訊息處理錯誤: {e}")
        
        print(f"   📊 訊息處理結果: {passed}/{total} 通過")
        return passed > 0
    
    def test_flex_message_generation(self):
        """測試 Flex Message 生成"""
        print("\n🎨 測試 Flex Message 生成...")
        
        test_message = "媽媽常忘記關瓦斯，需要協助穿衣"
        
        try:
            # 測試 Flex Message 端點
            response = requests.post(
                f"{self.line_bot_url}/analyze",
                json={"message": test_message},
                timeout=15
            )
            
            if response.status_code == 200:
                data = response.json()
                if 'flex_message' in data or 'message' in data:
                    print("      ✅ Flex Message 生成成功")
                    return True
                else:
                    print("      ⚠️  回應格式不包含 Flex Message")
                    return False
            else:
                print(f"      ❌ Flex Message 生成失敗: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"      ❌ Flex Message 測試錯誤: {e}")
            return False
    
    def test_module_integration(self):
        """測試模組整合"""
        print("\n🔗 測試模組整合...")
        
        # 測試不同模組的訊息
        module_tests = [
            ("M1", "媽媽常忘記關瓦斯"),
            ("M2", "需要協助穿衣，會迷路"),
            ("M3", "懷疑有人偷東西")
        ]
        
        passed = 0
        for module, message in module_tests:
            print(f"   測試 {module}: {message}")
            try:
                response = requests.post(
                    f"{self.line_bot_url}/analyze",
                    json={"message": message},
                    timeout=15
                )
                
                if response.status_code == 200:
                    data = response.json()
                    # 檢查回應是否包含相關資訊
                    if data.get('message') or data.get('flex_message'):
                        print(f"      ✅ {module} 模組回應正常")
                        passed += 1
                    else:
                        print(f"      ⚠️  {module} 模組回應格式異常")
                else:
                    print(f"      ❌ {module} 模組請求失敗: {response.status_code}")
                    
            except Exception as e:
                print(f"      ❌ {module} 模組測試錯誤: {e}")
        
        print(f"   📊 模組整合結果: {passed}/{len(module_tests)} 通過")
        return passed > 0
    
    def check_line_bot_files(self):
        """檢查 LINE Bot 檔案"""
        print("\n📁 檢查 LINE Bot 檔案...")
        
        line_bot_files = [
            "updated_line_bot_webhook.py",
            "enhanced_line_bot.py", 
            "line_bot_app.py",
            "line_bot_webhook_v2.py"
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
    
    def run_line_bot_test(self):
        """執行 LINE Bot 完整測試"""
        print("🤖 LINE Bot M1-M3 模組測試")
        print("=" * 50)
        print(f"測試時間: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"測試目標: {self.line_bot_url}")
        print()
        
        tests = [
            ("LINE Bot 健康檢查", self.test_line_bot_health),
            ("LINE Bot 基本資訊", self.test_line_bot_info),
            ("訊息處理", self.test_message_processing),
            ("Flex Message 生成", self.test_flex_message_generation),
            ("模組整合", self.test_module_integration),
            ("檔案檢查", self.check_line_bot_files)
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
        print("📊 LINE Bot 測試報告")
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
            print("\n🎉 LINE Bot 所有測試通過！")
            print("📱 現在可以在 LINE 上正常使用 M1-M3 模組")
        else:
            print(f"\n⚠️  {total - passed} 個測試失敗")
            print("🔧 請檢查 LINE Bot 配置和 API 連接")
        
        return results

def main():
    """主函數"""
    import sys
    
    # 檢查命令行參數
    if len(sys.argv) > 1:
        line_bot_url = sys.argv[1]
    else:
        line_bot_url = "http://localhost:5000"
    
    # 創建測試器
    tester = LINEBotModuleTester(line_bot_url)
    
    # 執行測試
    results = tester.run_line_bot_test()
    
    # 返回測試結果
    return all(results.values())

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1) 