#!/usr/bin/env python3
"""
簡單專業分析測試
"""

import requests
import json

def test_professional_analysis_simple():
    """簡單測試專業分析"""
    print("🎯 簡單專業分析測試")
    print("=" * 40)
    
    # 測試基礎端點
    try:
        response = requests.get("http://localhost:8005/health", timeout=5)
        if response.status_code == 200:
            print("✅ 服務器運行正常")
        else:
            print(f"❌ 服務器狀態異常: {response.status_code}")
            return
    except Exception as e:
        print(f"❌ 無法連接到服務器: {e}")
        return
    
    # 測試綜合分析端點
    try:
        response = requests.post(
            "http://localhost:8005/comprehensive-analysis",
            json={"user_input": "爸爸不會用洗衣機"},
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        if response.status_code == 200:
            print("✅ 綜合分析端點正常")
            result = response.json()
            print(f"📊 回應包含: {list(result.keys())}")
        else:
            print(f"❌ 綜合分析端點錯誤: {response.status_code}")
            print(f"錯誤內容: {response.text}")
            
    except Exception as e:
        print(f"❌ 綜合分析測試失敗: {e}")
    
    # 測試專業分析端點
    try:
        response = requests.post(
            "http://localhost:8005/professional-analysis",
            json={"user_input": "爸爸不會用洗衣機"},
            headers={"Content-Type": "application/json"},
            timeout=15
        )
        
        if response.status_code == 200:
            print("✅ 專業分析端點正常")
            result = response.json()
            print(f"📊 專業分析回應包含: {list(result.keys())}")
            
            if "professional_analysis" in result:
                professional_data = result["professional_analysis"]
                selected_modules = professional_data.get("selected_modules", [])
                print(f"🎯 選擇的模組: {selected_modules}")
                
                best_answer = professional_data.get("best_answer", "")
                print(f"💡 最佳答案: {best_answer[:100]}...")
                
                comprehensive_score = professional_data.get("comprehensive_score", 0)
                print(f"📈 綜合評分: {comprehensive_score:.1%}")
                
            if "text_response" in result:
                text_response = result["text_response"]
                print(f"📝 文字回應長度: {len(text_response)} 字符")
                print("📄 文字回應預覽:")
                print(text_response[:200] + "..." if len(text_response) > 200 else text_response)
                
        else:
            print(f"❌ 專業分析端點錯誤: {response.status_code}")
            print(f"錯誤內容: {response.text}")
            
    except Exception as e:
        print(f"❌ 專業分析測試失敗: {e}")
    
    print("\n" + "=" * 40)
    print("🎉 簡單測試完成!")

if __name__ == "__main__":
    test_professional_analysis_simple() 