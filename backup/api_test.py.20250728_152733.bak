import requests
import json

def test_new_api():
    """測試新的 M1+M2+M3 API"""
    
    api_url = "http://localhost:8005/comprehensive-analysis"
    
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
            "input": "爺爺晚上不睡覺，白天一直想睡"
        }
    ]
    
    print("🧪 開始測試新的 M1+M2+M3 API")
    print("=" * 50)
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n📋 測試 {i}：{test_case['name']}")
        print(f"📝 輸入：{test_case['input']}")
        
        try:
            response = requests.post(
                api_url,
                json={"user_input": test_case['input']},
                timeout=15
            )
            
            if response.status_code == 200:
                data = response.json()
                analysis = data.get("comprehensive_analysis", {})
                
                print(f"✅ 狀態：成功")
                print(f"🔍 檢測代碼：{', '.join(analysis.get('matched_codes', [])[:3])}")
                print(f"🧠 使用模組：{', '.join(analysis.get('modules_used', []))}")
                print(f"📊 總發現：{analysis.get('total_findings', 0)} 項")
                
                # 檢查 BPSD 分析
                if analysis.get('bpsd_analysis'):
                    bpsd = analysis['bpsd_analysis']
                    categories = bpsd.get('detected_categories', [])
                    if categories:
                        print(f"🧠 BPSD 症狀：{len(categories)} 種")
                        for cat in categories[:2]:
                            print(f"   - {cat.get('code')}: {cat.get('title')}")
                
                # 顯示摘要
                summary = analysis.get('comprehensive_summary', '')
                if summary:
                    print(f"📄 摘要：{summary[:50]}...")
                
            else:
                print(f"❌ 狀態：失敗 ({response.status_code})")
                
        except requests.exceptions.ConnectionError:
            print("❌ 狀態：連接失敗 - API 服務可能未運行")
        except Exception as e:
            print(f"❌ 狀態：錯誤 - {str(e)}")
        
        print("-" * 40)
    
    print("\n🎯 測試總結：")
    print("新 API 端點：http://localhost:8005/comprehensive-analysis")
    print("向後相容端點：http://localhost:8005/m1-flex")

def quick_health_check():
    """快速健康檢查"""
    print("🔍 檢查 API 狀態...")
    try:
        response = requests.get("http://localhost:8005/health", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ 狀態：{data.get('status')}")
            engine_info = data.get('engine_info', {})
            print(f"📊 總片段：{engine_info.get('total_chunks', 0)}")
            print(f"🚨 M1：{engine_info.get('m1_chunks', 0)} 片段")
            print(f"🧠 M3：{engine_info.get('m3_chunks', 0)} 片段")
            return True
        else:
            print(f"❌ 健康檢查失敗：{response.status_code}")
            return False
    except Exception as e:
        print(f"❌ 無法連接：{str(e)}")
        return False

if __name__ == "__main__":
    print("🚀 M1+M2+M3 API 測試")
    print("=" * 50)
    
    if quick_health_check():
        print("\n" + "=" * 50)
        test_new_api()
    else:
        print("\n💡 請確認 API 服務運行在端口 8005")
