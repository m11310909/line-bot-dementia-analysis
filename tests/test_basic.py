import asyncio
import sys
import os

# 添加項目根目錄到路徑
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

async def test_m1_analyzer():
    """測試 M1 分析器"""
    print("🧪 測試 M1 分析器...")
    
    try:
        from api.modules.m1_analyzer import M1Analyzer
        
        analyzer = M1Analyzer()
        result = await analyzer.analyze("媽媽最近常重複問同樣的問題")
        
        print(f"✅ 分析結果: {result.category_name}")
        print(f"✅ 可信度: {result.confidence:.2f}")
        print(f"✅ 建議數量: {len(result.recommendations)}")
        
        return True
    except Exception as e:
        print(f"❌ M1 分析器測試失敗: {e}")
        return False

async def test_flex_builder():
    """測試 Flex Message 建構器"""
    print("🧪 測試 Flex 建構器...")
    
    try:
        from flex.builders.m1_builder import M1FlexBuilder
        from api.modules.base_analyzer import AnalysisResult
        
        builder = M1FlexBuilder()
        
        # 測試資料
        test_result = AnalysisResult(
            matched_categories=["M1-01"],
            category_name="記憶力減退影響生活",
            confidence=0.8,
            severity=3,
            user_description="測試描述",
            normal_aging="正常老化現象",
            warning_sign="警訊特徵",
            recommendations=["建議1", "建議2"],
            require_medical_attention=True
        )
        
        flex_message = builder.build_analysis_result(test_result)
        
        print(f"✅ Flex Message 類型: {flex_message.get('type')}")
        print(f"✅ 替代文字: {flex_message.get('altText')}")
        
        return True
    except Exception as e:
        print(f"❌ Flex 建構器測試失敗: {e}")
        return False

def test_memory_usage():
    """測試記憶體使用"""
    print("🧪 測試記憶體監控...")
    
    try:
        from api.core.security import check_memory_usage
        
        check_memory_usage()
        print("✅ 記憶體檢查正常")
        return True
    except Exception as e:
        print(f"❌ 記憶體檢查失敗: {e}")
        return False

async def run_all_tests():
    """執行所有測試"""
    print("🚀 開始執行測試...")
    print("="*40)
    
    tests = [
        test_memory_usage(),
        await test_m1_analyzer(),
        await test_flex_builder()
    ]
    
    passed = sum(tests)
    total = len(tests)
    
    print("="*40)
    print(f"📊 測試結果: {passed}/{total} 通過")
    
    if passed == total:
        print("🎉 所有測試通過！")
        return True
    else:
        print("⚠️ 部分測試失敗")
        return False

if __name__ == "__main__":
    asyncio.run(run_all_tests())
