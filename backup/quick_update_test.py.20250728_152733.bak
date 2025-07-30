# 快速測試新 API 的 Python 腳本
import requests
import json

def test_new_api():
    """測試新的 M1+M2+M3 API"""
    
    # 新的 API 端點
    api_url = "http://localhost:8005/comprehensive-analysis"
    
    # 測試案例
    test_cases = [
        {
            "name": "記憶力測試",
            "input": "媽媽常忘記關瓦斯爐，會重複問同樣的問題"
        },
        {
            "name": "妄想症狀測試", 
            "input": "爸爸懷疑有人偷他的東西，不信任家人"
        },
        {
            "name": "激動行為測試",
            "input": "奶奶會打人和大聲叫罵，脾氣很暴躁"
        },
        {
            "name": "睡眠障礙測試",
            "input": "爺爺晚上不睡覺，白天一直想睡，日夜完全顛倒"
        },
        {
            "name": "綜合症狀測試",
            "input": "記憶力差，需要協助日常活動，情緒低落，懷疑別人偷東西"
        }
    ]
    
    print("🧪 開始測試新的 M1+M2+M3 API")
    print("=" * 60)
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n📋 測試 {i}：{test_case['name']}")
        print(f"📝 輸入：{test_case['input']}")
        
        try:
            # 發送請求
            response = requests.post(
                api_url,
                json={"user_input": test_case['input']},
                timeout=15
            )
            
            if response.status_code == 200:
                data = response.json()
                
                # 提取關鍵資訊
                analysis = data.get("comprehensive_analysis", {})
                
                print(f"✅ 狀態：成功")
                print(f"🔍 檢測代碼：{', '.join(analysis.get('matched_codes', [])[:3])}")
                print(f"🧠 使用模組：{', '.join(analysis.get('modules_used', []))}")
                print(f"📊 總發現：{analysis.get('total_findings', 0)} 項")
                print(f"📱 Flex Message：{'✅ 已生成' if data.get('flex_message') else '❌ 生成失敗'}")
                
                # 顯示綜合摘要（截短）
                summary = analysis.get('comprehensive_summary', '')
                if summary:
                    print(f"📄 摘要：{summary[:60]}...")
                
                # 檢查新功能
                if analysis.get('bpsd_analysis'):
                    bpsd = analysis['bpsd_analysis']
                    categories = bpsd.get('detected_categories', [])
                    if categories:
                        print(f"🧠 BPSD 症狀：{len(categories)} 種")
                        for cat in categories[:2]:  # 顯示前2個
                            print(f"   - {cat.get('code')}: {cat.get('title')}")
                
                if analysis.get('stage_detection'):
                    stage_info = analysis['stage_detection']
                    stage = stage_info.get('detected_stage', 'unknown')
                    confidence = stage_info.get('confidence', 0)
                    print(f"🏥 病程階段：{stage} (信心度：{confidence:.3f})")
                
                # 顯示行動建議
                suggestions = analysis.get('action_suggestions', [])
                if suggestions:
                    print(f"💡 建議：{suggestions[0][:40]}...")
                
            else:
                print(f"❌ 狀態：失敗 ({response.status_code})")
                print(f"錯誤：{response.text[:100]}")
                
        except requests.exceptions.Timeout:
            print("❌ 狀態：請求超時")
        except requests.exceptions.ConnectionError:
            print("❌ 狀態：連接失敗 - 請確認 API 服務是否運行")
        except Exception as e:
            print(f"❌ 狀態：錯誤 - {str(e)}")
        
        print("-" * 50)
    
    print("\n🎯 測試總結：")
    print("如果看到 '✅ 狀態：成功' 和 'Flex Message：✅ 已生成'")
    print("代表新 API 運作正常，可以進行 LINE Bot 更新！")
    
    # 顯示更新建議
    print(f"\n📱 LINE Bot 更新建議：")
    print(f"舊端點：http://localhost:8001/m1-flex")
    print(f"新端點：{api_url}")
    print(f"向後相容：http://localhost:8005/m1-flex")
    
    print(f"\n🔧 更新代碼示例：")
    print("# 只需要改這一行：")
    print(f"API_URL = '{api_url}'")
    
    print(f"\n🧠 新功能特色：")
    print("✅ M1: 失智症警訊識別")
    print("✅ M3: BPSD 行為心理症狀（7大類）")
    print("✅ 跨模組整合分析")
    print("✅ 智能綜合評估")
    print("✅ 個人化管理建議")

def check_api_health():
    """檢查 API 健康狀態"""
    print("🔍 檢查 API 健康狀態...")
    
    try:
        response = requests.get("http://localhost:8005/health", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ API 狀態：{data.get('status')}")
            
            engine_info = data.get('engine_info', {})
            print(f"📊 總知識片段：{engine_info.get('total_chunks', 0)}")
            print(f"🚨 M1 片段：{engine_info.get('m1_chunks', 0)}")
            print(f"🧠 M3 片段：{engine_info.get('m3_chunks', 0)}")
            print(f"📚 詞彙量：{engine_info.get('vocabulary_size', 0)}")
            return True
        else:
            print(f"❌ API 健康檢查失敗：{response.status_code}")
            return False
    except Exception as e:
        print(f"❌ 無法連接 API：{str(e)}")
        return False

if __name__ == "__main__":
    print("🚀 M1+M2+M3 API 功能測試")
    print("=" * 60)
    
    # 先檢查 API 健康狀態
    if check_api_health():
        print("\n" + "=" * 60)
        test_new_api()
    else:
        print("\n❌ API 服務未運行或有問題")
        print("💡 請確認 M1+M2+M3 API 服務已啟動在端口 8005")
        print("🚀 啟動命令：python3 m1_m2_m3_integrated_api.py")
