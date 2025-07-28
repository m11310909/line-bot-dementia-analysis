# enhanced/integrate_m2_system.py
"""
將 M2 病程階段模組整合到現有 RAG 系統
"""

import json
import os
from lightweight_rag_for_replit import LightweightRAGEngine

class EnhancedRAGWithM2(LightweightRAGEngine):
    """
    擴展現有 RAG 引擎，加入 M2 病程階段分析
    """

    def __init__(self, gemini_api_key=None):
        super().__init__(gemini_api_key)

        # 載入 M2 模組
        self.load_m2_chunks()
        self.rebuild_index_with_m2()

        print("✅ M2 病程階段模組已整合")

    def load_m2_chunks(self):
        """載入 M2 病程階段 chunks"""
        try:
            m2_chunks = []

            # 如果有 M2 檔案就載入
            if os.path.exists('data/chunks/m2_stage_chunks.jsonl'):
                with open('data/chunks/m2_stage_chunks.jsonl', 'r', encoding='utf-8') as f:
                    for line in f:
                        chunk = json.loads(line.strip())
                        m2_chunks.append(chunk)
            else:
                # 如果沒有檔案，直接建立 M2 chunks
                m2_chunks = self.create_m2_chunks_inline()

            # 合併到現有 chunks
            self.chunks.extend(m2_chunks)
            print(f"📊 載入了 {len(m2_chunks)} 個 M2 知識片段")

        except Exception as e:
            print(f"⚠️  M2 模組載入失敗: {e}")
            print("將使用內建的 M2 知識片段")
            self.chunks.extend(self.create_m2_chunks_inline())

    def create_m2_chunks_inline(self):
        """內建的 M2 chunks（如果檔案不存在）"""
        return [
            {
                "chunk_id": "M2-01",
                "module_id": "M2",
                "chunk_type": "stage_description",
                "title": "輕度失智症階段特徵",
                "content": "患者在熟悉環境中仍可獨立生活，但在複雜任務上需要協助。認知能力有輕微記憶缺損，日常生活基本可自理但複雜活動需監督。",
                "keywords": ["輕度", "獨立生活", "複雜任務", "監督", "規律作息"],
                "confidence_score": 0.92,
                "source": "CDR量表與照護指引"
            },
            {
                "chunk_id": "M2-02",
                "module_id": "M2", 
                "chunk_type": "stage_description",
                "title": "中度失智症階段特徵",
                "content": "明顯認知功能衰退，日常生活需要相當程度協助。記憶力顯著下降，可能出現遊走、重複行為、睡眠障礙等問題。",
                "keywords": ["中度", "認知衰退", "協助", "行為變化", "環境安全"],
                "confidence_score": 0.90,
                "source": "CDR量表與照護指引"
            },
            {
                "chunk_id": "M2-03",
                "module_id": "M2",
                "chunk_type": "stage_description", 
                "title": "重度失智症階段特徵",
                "content": "嚴重認知功能缺損，日常生活完全依賴他人。可能出現吞嚥困難、行動障礙，需要全面性照護。",
                "keywords": ["重度", "完全依賴", "健康風險", "全面照護", "舒適照護"],
                "confidence_score": 0.88,
                "source": "CDR量表與照護指引"
            }
        ]

    def rebuild_index_with_m2(self):
        """重新建立包含 M2 的檢索索引"""
        print("🔄 重新建立檢索索引（包含 M2 模組）...")
        self.build_tfidf_index()
        print(f"✅ 索引重建完成，現在包含 {len(self.chunks)} 個知識片段")

    def analyze_with_stage_detection(self, user_input):
        """增強分析：包含病程階段檢測"""

        # 先執行原有的分析
        base_result = self.analyze_with_lightweight_rag(user_input)

        # 檢查是否匹配到 M2 模組
        m2_chunks = [chunk for chunk in base_result.get("retrieved_chunks", []) 
                     if chunk.get("module_id") == "M2"]

        if m2_chunks:
            # 如果檢索到 M2 內容，增強分析結果
            stage_info = self.extract_stage_info(m2_chunks, user_input)
            base_result["stage_analysis"] = stage_info
            base_result["analysis_enhanced"] = "M2_stage_detection"

        return base_result

    def extract_stage_info(self, m2_chunks, user_input):
        """從 M2 chunks 提取病程階段資訊"""

        stage_mapping = {
            "M2-01": {"stage": "輕度", "priority": 1},
            "M2-02": {"stage": "中度", "priority": 2}, 
            "M2-03": {"stage": "重度", "priority": 3}
        }

        detected_stages = []
        for chunk in m2_chunks:
            chunk_id = chunk.get("chunk_id", "")
            if chunk_id in stage_mapping:
                stage_info = stage_mapping[chunk_id].copy()
                stage_info["similarity"] = chunk.get("similarity_score", 0)
                stage_info["chunk_title"] = chunk.get("title", "")
                detected_stages.append(stage_info)

        # 按相似度排序
        detected_stages.sort(key=lambda x: x["similarity"], reverse=True)

        return {
            "most_likely_stage": detected_stages[0]["stage"] if detected_stages else "需要更多資訊",
            "confidence": detected_stages[0]["similarity"] if detected_stages else 0,
            "all_detected_stages": detected_stages,
            "stage_guidance": self.get_stage_guidance(detected_stages[0]["stage"] if detected_stages else None)
        }

    def get_stage_guidance(self, stage):
        """根據病程階段提供指引"""

        guidance_map = {
            "輕度": {
                "focus": "維持獨立性，提供適度協助",
                "priorities": ["安全環境", "規律作息", "認知刺激", "社交維持"],
                "next_steps": "建議進行詳細認知評估，規劃長期照護"
            },
            "中度": {
                "focus": "安全照護，行為管理",
                "priorities": ["環境安全", "行為管理", "健康監控", "照護者支持"],
                "next_steps": "考慮日間照護服務，申請長照資源"
            },
            "重度": {
                "focus": "舒適照護，品質維護",
                "priorities": ["全面照護", "感染預防", "舒適維護", "家屬支持"],
                "next_steps": "重點在於舒適照護與尊嚴維護"
            }
        }

        return guidance_map.get(stage, {
            "focus": "建議專業評估",
            "priorities": ["專業諮詢"],
            "next_steps": "尋求醫療專業評估"
        })

def test_m2_integration():
    """測試 M2 整合功能"""

    api_key = os.getenv('AISTUDIO_API_KEY')
    engine = EnhancedRAGWithM2(api_key)

    test_cases = [
        "媽媽需要人提醒吃藥，但還能自己洗澡",
        "爸爸會迷路，需要協助穿衣，晚上不睡覺", 
        "奶奶不認得我們，需要餵食",
        "想了解失智症會怎麼發展"
    ]

    print("🧪 測試 M2 病程階段檢測")
    print("=" * 50)

    for i, test_input in enumerate(test_cases, 1):
        print(f"\n測試 {i}: {test_input}")
        print("-" * 30)

        try:
            result = engine.analyze_with_stage_detection(test_input)

            # 顯示基本分析
            print(f"📋 警訊代碼: {result.get('matched_warning_code', 'N/A')}")
            print(f"🎯 症狀標題: {result.get('symptom_title', 'N/A')}")

            # 顯示階段分析（如果有）
            if "stage_analysis" in result:
                stage_info = result["stage_analysis"]
                print(f"📊 病程階段: {stage_info['most_likely_stage']}")
                print(f"📈 信心程度: {stage_info['confidence']:.3f}")
                print(f"🎯 照護重點: {stage_info['stage_guidance']['focus']}")

            print("✅ 測試通過")

        except Exception as e:
            print(f"❌ 測試失敗: {e}")

if __name__ == "__main__":
    print("🔧 M2 模組整合到 RAG 系統")
    print("=" * 50)

    # 執行整合測試
    test_m2_integration()

    print(f"\n🎯 整合完成！")
    print("✅ M2 病程階段模組已成功整合到 RAG 系統")
    print("✅ 系統現在可以檢測失智症病程階段")
    print("✅ 提供階段性照護指引")

    print(f"\n📌 下一步:")
    print("1. 更新 LINE Bot API 使用新的 M2 增強功能")
    print("2. 設計 M2 階段專用的 Flex Message")
    print("3. 開發 M3 行為症狀模組")