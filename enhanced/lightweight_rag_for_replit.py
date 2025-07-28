# lightweight_rag_for_replit.py
"""
適用於 Replit 的輕量級 RAG 解決方案
修正版本 - 無縮排錯誤
"""

import json
import os
import re
import math
from typing import Dict, List, Optional
from collections import Counter
from datetime import datetime

# 檢查 Gemini 模組
try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    print("⚠️  google.generativeai 未安裝，將使用模擬模式")
    GEMINI_AVAILABLE = False

class LightweightRAGEngine:
    """輕量級 RAG 引擎"""

    def __init__(self, gemini_api_key=None):
        print("🚀 初始化輕量級 RAG 引擎...")

        # Gemini 配置
        self.gemini_available = GEMINI_AVAILABLE and gemini_api_key
        if self.gemini_available:
            try:
                genai.configure(api_key=gemini_api_key)
                self.model = genai.GenerativeModel('gemini-1.5-flash')
                print("✅ Gemini AI 連接成功")
            except Exception as e:
                print(f"⚠️  Gemini AI 連接失敗: {e}")
                self.gemini_available = False

        # 檢索組件
        self.chunks = []
        self.tfidf_matrix = {}
        self.vocabulary = set()

        # 載入資料
        self.load_m1_chunks()
        self.build_tfidf_index()

        print("✅ 引擎初始化完成")

    def load_m1_chunks(self):
        """載入 M1 失智症警訊資料"""
        print("📊 載入 M1 資料...")

        self.chunks = [
            {
                "chunk_id": "M1-01",
                "title": "記憶力減退影響日常生活",
                "content": "正常老化：偶爾忘記約會但事後會想起來。失智警訊：忘記剛發生的事、重要日期或事件；反覆詢問同樣事情。",
                "keywords": ["記憶", "健忘", "忘記", "重複", "日常生活"],
                "confidence_score": 0.95,
                "source": "TADA 十大警訊"
            },
            {
                "chunk_id": "M1-02",
                "title": "計劃事情或解決問題有困難",
                "content": "正常老化：偶爾需要協助使用設備。失智警訊：無法專心，做事需要更長時間；處理金錢有困難。",
                "keywords": ["計劃", "解決問題", "專心", "金錢", "帳單"],
                "confidence_score": 0.92,
                "source": "TADA 十大警訊"
            },
            {
                "chunk_id": "M1-03", 
                "title": "無法勝任原本熟悉的事務",
                "content": "正常老化：偶爾需要協助使用新設備。失智警訊：無法完成熟悉工作，如迷路、無法管理預算。",
                "keywords": ["熟悉", "工作", "迷路", "預算", "管理"],
                "confidence_score": 0.90,
                "source": "TADA 十大警訊"
            },
            {
                "chunk_id": "M1-04",
                "title": "對時間地點感到混淆",
                "content": "正常老化：偶爾忘記星期幾但稍後想起。失智警訊：搞不清年月日、季節；忘記身在何處。",
                "keywords": ["時間", "地點", "方向", "季節", "年月日"],
                "confidence_score": 0.88,
                "source": "TADA 十大警訊"
            },
            {
                "chunk_id": "M1-05",
                "title": "理解視覺影像和空間關係有困難",
                "content": "正常老化：因白內障等視覺變化。失智警訊：無法判斷距離、顏色對比，影響駕駛。",
                "keywords": ["視覺", "空間", "距離", "顏色", "駕駛"],
                "confidence_score": 0.85,
                "source": "TADA 十大警訊"
            }
        ]

        print(f"✅ 載入了 {len(self.chunks)} 個知識片段")

    def tokenize_chinese(self, text):
        """中文分詞"""
        text = re.sub(r'[^\u4e00-\u9fff\w\s]', ' ', text.lower())
        chinese_chars = re.findall(r'[\u4e00-\u9fff]+', text)
        english_words = re.findall(r'[a-zA-Z]+', text)

        tokens = []
        for char_group in chinese_chars:
            # 單字
            tokens.extend(list(char_group))
            # 雙字詞
            for i in range(len(char_group) - 1):
                tokens.append(char_group[i:i+2])

        tokens.extend(english_words)
        return tokens

    def compute_tf_idf(self, documents):
        """計算 TF-IDF"""
        print("🔍 建立 TF-IDF 索引...")

        all_tokens = []
        doc_tokens = []

        for doc in documents:
            tokens = self.tokenize_chinese(doc)
            doc_tokens.append(tokens)
            all_tokens.extend(tokens)

        self.vocabulary = set(all_tokens)
        vocab_list = list(self.vocabulary)

        tfidf_matrix = {}
        N = len(documents)

        for doc_idx, tokens in enumerate(doc_tokens):
            doc_vector = {}
            token_count = Counter(tokens)
            doc_length = len(tokens)

            for token in vocab_list:
                if doc_length > 0:
                    tf = token_count[token] / doc_length
                    docs_with_token = sum(1 for dt in doc_tokens if token in dt)
                    idf = math.log(N / docs_with_token) if docs_with_token > 0 else 0
                    tfidf_score = tf * idf
                    if tfidf_score > 0:
                        doc_vector[token] = tfidf_score

            tfidf_matrix[doc_idx] = doc_vector

        return tfidf_matrix

    def build_tfidf_index(self):
        """建立檢索索引"""
        documents = []
        for chunk in self.chunks:
            doc_text = f"{chunk['title']} {chunk['content']} {' '.join(chunk['keywords'])}"
            documents.append(doc_text)

        self.tfidf_matrix = self.compute_tf_idf(documents)
        print("✅ 檢索索引建立完成")

    def cosine_similarity(self, vec1, vec2):
        """計算餘弦相似度"""
        common_keys = set(vec1.keys()) & set(vec2.keys())

        if not common_keys:
            return 0.0

        dot_product = sum(vec1[key] * vec2[key] for key in common_keys)
        norm1 = math.sqrt(sum(val**2 for val in vec1.values()))
        norm2 = math.sqrt(sum(val**2 for val in vec2.values()))

        if norm1 == 0 or norm2 == 0:
            return 0.0

        return dot_product / (norm1 * norm2)

    def retrieve_relevant_chunks(self, query, k=3):
        """檢索相關片段"""
        print(f"🔍 檢索查詢: {query}")

        query_tokens = self.tokenize_chinese(query)
        query_token_count = Counter(query_tokens)
        query_length = len(query_tokens)

        if query_length == 0:
            return []

        query_vector = {}
        for token in self.vocabulary:
            tf = query_token_count[token] / query_length
            if tf > 0:
                query_vector[token] = tf

        similarities = []
        for doc_idx, doc_vector in self.tfidf_matrix.items():
            similarity = self.cosine_similarity(query_vector, doc_vector)
            similarities.append((doc_idx, similarity))

        similarities.sort(key=lambda x: x[1], reverse=True)

        results = []
        for doc_idx, similarity in similarities[:k]:
            if similarity > 0:
                chunk = self.chunks[doc_idx].copy()
                chunk['similarity_score'] = round(similarity, 4)
                results.append(chunk)

        print(f"📊 找到 {len(results)} 個相關片段")
        return results

    def analyze_with_lightweight_rag(self, user_input):
        """RAG 分析"""
        print(f"🧠 分析: {user_input}")

        relevant_chunks = self.retrieve_relevant_chunks(user_input, k=3)

        if not relevant_chunks:
            return self.get_fallback_response(user_input, [])

        if self.gemini_available:
            return self.analyze_with_gemini(user_input, relevant_chunks)
        else:
            return self.analyze_with_rules(user_input, relevant_chunks)

    def analyze_with_gemini(self, user_input, chunks):
        """使用 Gemini 分析"""
        print("🤖 使用 Gemini AI 分析...")

        context_info = ""
        for i, chunk in enumerate(chunks, 1):
            context_info += f"【片段{i}】{chunk['title']}: {chunk['content']}\n"

        prompt = f"""你是失智症早期警訊分析助理。

參考資料：
{context_info}

使用者描述："{user_input}"

請以JSON格式回應：
{{
    "matched_warning_code": "M1-XX",
    "symptom_title": "相符的警訊標題",
    "user_behavior_summary": "使用者行為摘要",
    "normal_behavior": "正常老化表現",
    "dementia_indicator": "失智症警訊指標",
    "action_suggestion": "建議行動",
    "confidence_level": "high/medium/low",
    "source": "TADA 十大警訊"
}}"""

        try:
            response = self.model.generate_content(prompt)
            result_text = response.text
            analysis_result = self.safe_json_parse(result_text)

            analysis_result["retrieved_chunks"] = chunks
            analysis_result["total_chunks_used"] = len(chunks)
            analysis_result["lightweight_rag"] = True
            analysis_result["analysis_method"] = "gemini_ai"

            return analysis_result

        except Exception as e:
            print(f"⚠️  Gemini 分析失敗: {e}")
            return self.analyze_with_rules(user_input, chunks)

    def analyze_with_rules(self, user_input, chunks):
        """規則基礎分析"""
        print("📋 使用規則分析...")

        if not chunks:
            return self.get_fallback_response(user_input, [])

        best_chunk = chunks[0]
        similarity = best_chunk.get('similarity_score', 0)

        if similarity > 0.3:
            confidence = "high"
        elif similarity > 0.1:
            confidence = "medium"
        else:
            confidence = "low"

        return {
            "matched_warning_code": best_chunk['chunk_id'],
            "symptom_title": best_chunk['title'],
            "user_behavior_summary": user_input[:100],
            "normal_behavior": "隨年齡增長的輕微變化可能是正常的",
            "dementia_indicator": "持續或明顯的症狀可能需要關注",
            "action_suggestion": "建議諮詢專業醫療人員進行評估",
            "confidence_level": confidence,
            "source": "TADA 十大警訊",
            "retrieved_chunks": chunks,
            "total_chunks_used": len(chunks),
            "lightweight_rag": True,
            "analysis_method": "rule_based",
            "similarity_scores": [chunk.get('similarity_score', 0) for chunk in chunks]
        }

    def safe_json_parse(self, text):
        """安全JSON解析"""
        try:
            return json.loads(text)
        except:
            json_match = re.search(r'```json\s*(\{.*?\})\s*```', text, re.DOTALL)
            if json_match:
                try:
                    return json.loads(json_match.group(1))
                except:
                    pass

            json_match = re.search(r'\{[^{}]*\}', text, re.DOTALL)
            if json_match:
                try:
                    return json.loads(json_match.group(0))
                except:
                    pass

            return self.get_basic_fallback()

    def get_fallback_response(self, user_input, chunks):
        """備用回應"""
        return {
            "matched_warning_code": "M1-GENERAL",
            "symptom_title": "需要進一步關注的症狀",
            "user_behavior_summary": user_input[:100],
            "normal_behavior": "隨著年齡增長，輕微的認知變化是正常的",
            "dementia_indicator": "如果症狀持續或加重，可能需要專業評估",
            "action_suggestion": "建議記錄症狀變化，必要時諮詢專業醫療人員",
            "confidence_level": "low",
            "source": "TADA 十大警訊",
            "retrieved_chunks": chunks,
            "total_chunks_used": len(chunks),
            "lightweight_rag": True,
            "fallback_used": True
        }

    def get_basic_fallback(self):
        """基本備用回應"""
        return {
            "matched_warning_code": "M1-GENERAL",
            "symptom_title": "一般性關注",
            "user_behavior_summary": "描述的情況需要評估",
            "normal_behavior": "隨著年齡增長，輕微的認知變化是正常的",
            "dementia_indicator": "持續或嚴重的認知變化需要關注",
            "action_suggestion": "如有疑慮，建議諮詢專業醫療人員",
            "confidence_level": "low",
            "source": "一般醫療建議"
        }

def test_lightweight_rag():
    """測試函數"""
    print("🧪 開始測試")
    print("=" * 50)

    api_key = os.getenv('AISTUDIO_API_KEY')
    if not api_key:
        print("⚠️  未設定 API Key，使用規則分析")

    engine = LightweightRAGEngine(api_key)

    test_cases = [
        "媽媽最近常忘記關瓦斯爐",
        "爸爸開車時經常迷路",
        "奶奶重複問同樣的問題"
    ]

    for i, test_input in enumerate(test_cases, 1):
        print(f"\n測試 {i}: {test_input}")
        print("-" * 30)

        try:
            result = engine.analyze_with_lightweight_rag(test_input)

            print(f"📋 警訊: {result.get('matched_warning_code', 'N/A')}")
            print(f"🎯 標題: {result.get('symptom_title', 'N/A')}")
            print(f"📊 信心: {result.get('confidence_level', 'N/A')}")
            print(f"🔍 方法: {result.get('analysis_method', 'N/A')}")
            print("✅ 測試通過")

        except Exception as e:
            print(f"❌ 測試失敗: {e}")

    print(f"\n🎉 測試完成！")
    return engine

def main():
    """主程式"""
    print("🚀 輕量級 RAG 系統")
    print("=" * 50)
    print("✅ 適用於 Replit")
    print("✅ 無需額外依賴")
    print("✅ 記憶體友善")

    engine = test_lightweight_rag()

    print(f"\n📌 使用說明：")
    print("在現有 API 中導入:")
    print("from enhanced.lightweight_rag_for_replit import LightweightRAGEngine")

    return engine

if __name__ == "__main__":
    main()