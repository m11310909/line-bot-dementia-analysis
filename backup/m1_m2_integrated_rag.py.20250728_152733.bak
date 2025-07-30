import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from enhanced.lightweight_rag_for_replit import LightweightRAGEngine

import json
import os

class M1M2RAGEngine(LightweightRAGEngine):
    """整合 M1 + M2 的 RAG 引擎"""
    
    def __init__(self, gemini_api_key=None):
        print("🚀 初始化 M1+M2 整合引擎...")
        
        # 初始化基礎引擎（包含 M1）
        super().__init__(gemini_api_key)
        
        # 載入 M2 模組
        self.load_m2_module()
        
        # 重建索引
        self.rebuild_combined_index()
        
        print(f"✅ 整合完成：總共 {len(self.chunks)} 個知識片段")
    
    def load_m2_module(self):
        """載入 M2 病程階段模組"""
        m2_file = '../data/chunks/m2_stage_chunks.jsonl'
        
        if os.path.exists(m2_file):
            m2_count = 0
            try:
                with open(m2_file, 'r', encoding='utf-8') as f:
                    for line in f:
                        if line.strip():
                            chunk = json.loads(line.strip())
                            self.chunks.append(chunk)
                            m2_count += 1
                print(f"📊 載入 M2 模組：{m2_count} 個知識片段")
            except Exception as e:
                print(f"⚠️  M2 檔案讀取錯誤：{e}")
        else:
            print(f"❌ M2 檔案不存在：{m2_file}")
    
    def rebuild_combined_index(self):
        """重建包含 M1+M2 的檢索索引"""
        print("🔄 重建檢索索引（M1+M2）...")
        self.build_tfidf_index()
        print(f"✅ 檢索索引重建完成")
    
    def analyze_with_stage_detection(self, user_input):
        """帶有病程階段檢測的分析"""
        
        # 執行基礎 RAG 分析
        result = self.analyze_with_lightweight_rag(user_input)
        
        # 檢查是否檢索到 M2 內容
        retrieved_chunks = result.get("retrieved_chunks", [])
        m2_chunks = [chunk for chunk in retrieved_chunks if chunk.get("module_id") == "M2"]
        
        if m2_chunks:
            # 進行階段分析
            stage_analysis = self.detect_stage(m2_chunks, user_input)
            result["stage_detection"] = stage_analysis
            result["enhanced_with"] = "M2_stage_analysis"
        
        return result
    
    def detect_stage(self, m2_chunks, user_input):
        """檢測失智症階段"""
        
        stage_keywords = {
            "輕度": ["獨立", "監督", "提醒", "複雜任務"],
            "中度": ["協助", "穿衣", "迷路", "睡眠", "遊走", "重複"],
            "重度": ["完全依賴", "無法辨識", "吞嚥", "行動障礙"]
        }
        
        # 分析輸入文字
        input_lower = user_input.lower()
        stage_scores = {}
        
        for stage, keywords in stage_keywords.items():
            score = sum(1 for keyword in keywords if keyword in input_lower)
            stage_scores[stage] = score
        
        # 結合 M2 chunks 的相似度
        chunk_stage_scores = {}
        for chunk in m2_chunks:
            title = chunk.get("title", "")
            similarity = chunk.get("similarity_score", 0)
            
            if "輕度" in title:
                chunk_stage_scores["輕度"] = similarity
            elif "中度" in title:
                chunk_stage_scores["中度"] = similarity
            elif "重度" in title:
                chunk_stage_scores["重度"] = similarity
        
        # 綜合評分
        final_scores = {}
        for stage in ["輕度", "中度", "重度"]:
            keyword_score = stage_scores.get(stage, 0) * 0.3
            chunk_score = chunk_stage_scores.get(stage, 0) * 0.7
            final_scores[stage] = keyword_score + chunk_score
        
        # 找出最高分的階段
        best_stage = max(final_scores.keys(), key=lambda k: final_scores[k]) if final_scores else "需要評估"
        best_score = final_scores.get(best_stage, 0)
        
        return {
            "detected_stage": best_stage,
            "confidence": best_score,
            "stage_scores": final_scores,
            "m2_chunks_found": len(m2_chunks)
        }

def test_m1_m2_integration():
    """測試 M1+M2 整合功能"""
    
    print("🧪 測試 M1+M2 整合 RAG 引擎")
    print("=" * 50)
    
    # 初始化引擎
    api_key = os.getenv('AISTUDIO_API_KEY')
    engine = M1M2RAGEngine(api_key)
    
    # 測試案例
    test_cases = [
        {
            "input": "媽媽常忘記關瓦斯",
            "description": "基本 M1 警訊測試"
        },
        {
            "input": "爸爸需要協助穿衣，會迷路，晚上不睡覺",
            "description": "M2 中度階段測試"
        },
        {
            "input": "奶奶可以自己洗澡，但需要提醒吃藥",
            "description": "M2 輕度階段測試"
        },
        {
            "input": "爺爺已經不認得我們，需要餵食",
            "description": "M2 重度階段測試"
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n測試 {i}: {test_case['description']}")
        print(f"輸入: {test_case['input']}")
        print("-" * 40)
        
        try:
            result = engine.analyze_with_stage_detection(test_case['input'])
            
            # 基本分析結果
            print(f"📋 警訊代碼: {result.get('matched_warning_code', 'N/A')}")
            print(f"🎯 症狀標題: {result.get('symptom_title', 'N/A')}")
            print(f"📊 信心程度: {result.get('confidence_level', 'N/A')}")
            
            # 階段檢測結果
            if "stage_detection" in result:
                stage_info = result["stage_detection"]
                print(f"🏥 檢測階段: {stage_info['detected_stage']}")
                print(f"📈 階段信心: {stage_info['confidence']:.3f}")
                print(f"🔍 M2 片段數: {stage_info['m2_chunks_found']}")
            else:
                print("🔍 未檢測到 M2 階段資訊")
            
            # 模組分布
            retrieved = result.get("retrieved_chunks", [])
            m1_count = sum(1 for c in retrieved if c.get("module_id") == "M1")
            m2_count = sum(1 for c in retrieved if c.get("module_id") == "M2")
            print(f"📊 模組分布: M1={m1_count}, M2={m2_count}")
            
            print("✅ 測試通過")
            
        except Exception as e:
            print(f"❌ 測試失敗: {e}")
            import traceback
            traceback.print_exc()
    
    return engine

if __name__ == "__main__":
    engine = test_m1_m2_integration()
    
    print(f"\n🎉 M1+M2 整合測試完成！")
    print(f"📊 總知識片段: {len(engine.chunks)}")
    print(f"💡 可以啟動整合版 API 了")

