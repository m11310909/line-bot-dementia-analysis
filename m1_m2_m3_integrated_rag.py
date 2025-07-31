# 簡化版 M1+M2+M3 整合引擎
import json
import re
from datetime import datetime
from typing import Dict, List, Any, Optional

class AnalysisResult:
    """分析結果資料結構"""
    def __init__(self):
        self.matched_codes = []
        self.symptom_titles = []
        self.confidence_levels = []
        self.bpsd_analysis = None
        self.stage_detection = None
        self.comprehensive_summary = ""
        self.action_suggestions = []
        self.retrieved_chunks = []
        self.modules_used = []

class M1M2M3IntegratedEngine:
    """M1+M2+M3 整合分析引擎"""
    
    def __init__(self, api_key=None):
        self.api_key = api_key
        self.chunks = []
        self.vocabulary = set()
        
        print("🚀 初始化 M1+M2+M3 整合引擎...")
        self._load_all_modules()
        self._build_search_index()
        print("✅ M1+M2+M3 整合引擎初始化完成")
    
    def _load_all_modules(self):
        """載入所有模組資料"""
        
        # 載入 M1 資料
        print("📊 載入 M1 資料...")
        m1_data = self._create_m1_data()
        self.chunks.extend(m1_data)
        print(f"✅ M1 載入：{len(m1_data)} 個知識片段")
        
        # 載入 M2 資料
        print("📊 載入 M2 資料...")
        try:
            with open('m2_stage_data.json', 'r', encoding='utf-8') as f:
                m2_data = json.load(f)
                self.chunks.extend(m2_data)
                print(f"✅ M2 載入：{len(m2_data)} 個知識片段")
        except FileNotFoundError:
            print("⚠️  M2 資料檔案未找到，跳過 M2 模組")
        
        # 載入 M3 資料  
        print("📊 載入 M3 BPSD 資料...")
        try:
            with open('m3_bpsd_data.json', 'r', encoding='utf-8') as f:
                m3_data = json.load(f)
                self.chunks.extend(m3_data)
                print(f"✅ M3 載入：{len(m3_data)} 個知識片段")
        except FileNotFoundError:
            print("⚠️  M3 資料檔案未找到")
        
        total_chunks = len(self.chunks)
        print(f"🎯 總計載入：{total_chunks} 個知識片段")
        
        # 統計各模組
        m1_count = len([c for c in self.chunks if c.get("chunk_id", "").startswith("M1")])
        m2_count = len([c for c in self.chunks if c.get("module_id") == "M2"])
        m3_count = len([c for c in self.chunks if c.get("module_id") == "M3"])
        
        print(f"📋 模組分布：M1({m1_count}) + M2({m2_count}) + M3({m3_count}) = {total_chunks}")
    
    def _create_m1_data(self):
        """創建 M1 十大警訊資料"""
        return [
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
                "title": "無法勝任原本熟悉的事務",
                "content": "正常老化：偶爾需要協助使用新設備。失智警訊：無法完成熟悉工作，如迷路、無法管理預算。",
                "keywords": ["熟悉", "工作", "迷路", "預算", "管理"],
                "confidence_score": 0.9,
                "source": "TADA 十大警訊"
            },
            {
                "chunk_id": "M1-03",
                "title": "語言表達出現問題",
                "content": "正常老化：偶爾想不起適當用詞。失智警訊：用錯詞彙、說話內容混亂、無法理解對話。",
                "keywords": ["語言", "表達", "用詞", "混亂", "對話"],
                "confidence_score": 0.88,
                "source": "TADA 十大警訊"
            }
        ]
    
    def _build_search_index(self):
        """建立檢索索引"""
        print("🔍 建立檢索索引...")
        for chunk in self.chunks:
            content = chunk.get("content", "")
            keywords = chunk.get("keywords", [])
            title = chunk.get("title", "")
            words = re.findall(r'[\u4e00-\u9fff]+', content + title + " ".join(keywords))
            self.vocabulary.update(words)
        print(f"✅ 詞彙庫建立完成：{len(self.vocabulary)} 個詞彙")
    
    def analyze_comprehensive(self, user_input: str):
        """綜合分析：M1+M2+M3"""
        print(f"🧠 綜合分析: {user_input}")
        
        # 檢索相關片段
        retrieved_chunks = self._retrieve_relevant_chunks(user_input, top_k=5)
        
        result = AnalysisResult()
        result.retrieved_chunks = retrieved_chunks
        
        # 分析 M1 警訊
        m1_chunks = [c for c in retrieved_chunks if c.get("chunk_id", "").startswith("M1")]
        if m1_chunks:
            # 根據用戶輸入選擇最相關的 M1 片段
            best_match = self._select_best_m1_chunk(user_input, m1_chunks)
            result.matched_codes.append(best_match["chunk_id"])
            result.symptom_titles.append(best_match["title"])
            result.confidence_levels.append(self._get_confidence_level(best_match.get("similarity_score", 0)))
            result.modules_used.append("M1")
        
        # 分析 M2 階段
        m2_chunks = [c for c in retrieved_chunks if c.get("module_id") == "M2"]
        if m2_chunks:
            best_m2 = max(m2_chunks, key=lambda x: x.get("similarity_score", 0))
            stage = self._extract_stage_from_title(best_m2.get("title", ""))
            if stage:
                result.stage_detection = {
                    "detected_stage": stage,
                    "confidence": best_m2.get("similarity_score", 0)
                }
                result.matched_codes.append(f"M2-{stage[:2].upper()}")
                result.symptom_titles.append(f"{stage}失智症特徵")
                result.confidence_levels.append(self._get_confidence_level(best_m2.get("similarity_score", 0)))
                result.modules_used.append("M2")
        
        # 分析 M3 BPSD
        m3_chunks = [c for c in retrieved_chunks if c.get("module_id") == "M3"]
        if m3_chunks:
            detected_categories = []
            for chunk in m3_chunks[:2]:  # 最多檢測 2 個 BPSD 症狀
                category = {
                    "code": chunk["chunk_id"],
                    "title": chunk["title"],
                    "confidence_level": self._get_confidence_level(chunk.get("similarity_score", 0)),
                    "severity_analysis": self._analyze_severity(user_input, chunk),
                    "management_strategies": chunk.get("management_strategies", [])
                }
                detected_categories.append(category)
                result.matched_codes.append(chunk["chunk_id"])
                result.symptom_titles.append(chunk["title"])
                result.confidence_levels.append(category["confidence_level"])
            
            if detected_categories:
                result.bpsd_analysis = {
                    "detected_categories": detected_categories,
                    "primary_category": detected_categories[0]
                }
                result.modules_used.append("M3")
        
        # 生成綜合摘要和建議
        result.comprehensive_summary = self._generate_summary(result, user_input)
        result.action_suggestions = self._generate_suggestions(result)
        
        return result
    
    def _retrieve_relevant_chunks(self, query: str, top_k: int = 5):
        """檢索相關知識片段"""
        print(f"🔍 檢索查詢: {query}")
        query_words = set(re.findall(r'[\u4e00-\u9fff]+', query))
        
        # 根據查詢內容調整檢索策略
        if any(word in query for word in ["迷路", "方向", "找不到"]):
            # 方向感問題，優先檢索 M1-02
            priority_chunk_ids = ["M1-02"]
        elif any(word in query for word in ["重複", "同樣", "一樣", "反覆"]):
            # 重複行為，優先檢索 M1-01
            priority_chunk_ids = ["M1-01"]
        elif any(word in query for word in ["語言", "說話", "表達", "詞彙"]):
            # 語言問題，優先檢索 M1-03
            priority_chunk_ids = ["M1-03"]
        else:
            # 默認策略
            priority_chunk_ids = []
        
        scored_chunks = []
        for chunk in self.chunks:
            chunk_keywords = set(chunk.get("keywords", []))
            content_words = set(re.findall(r'[\u4e00-\u9fff]+', chunk.get("content", "")))
            title_words = set(re.findall(r'[\u4e00-\u9fff]+', chunk.get("title", "")))
            
            all_chunk_words = chunk_keywords | content_words | title_words
            
            # 計算相似度
            overlap = len(query_words & all_chunk_words)
            total_words = len(query_words | all_chunk_words)
            
            if total_words > 0:
                similarity = overlap / total_words
                # 關鍵字匹配加權
                keyword_bonus = len(query_words & chunk_keywords) * 0.3
                similarity += keyword_bonus
                
                # 優先級加權
                if chunk.get("chunk_id") in priority_chunk_ids:
                    similarity += 0.5  # 大幅提升優先級
                
                chunk_copy = chunk.copy()
                chunk_copy["similarity_score"] = round(similarity, 4)
                scored_chunks.append(chunk_copy)
        
        scored_chunks.sort(key=lambda x: x["similarity_score"], reverse=True)
        top_chunks = scored_chunks[:top_k]
        
        print(f"📊 找到 {len(top_chunks)} 個相關片段")
        return top_chunks
    
    def _select_best_m1_chunk(self, user_input: str, m1_chunks: List[Dict]) -> Dict:
        """根據用戶輸入選擇最相關的 M1 片段"""
        user_lower = user_input.lower()
        
        # 根據關鍵詞匹配選擇最相關的片段
        if any(word in user_lower for word in ["迷路", "方向", "找不到", "熟悉"]):
            # 方向感問題 -> M1-02
            for chunk in m1_chunks:
                if chunk.get("chunk_id") == "M1-02":
                    return chunk
        elif any(word in user_lower for word in ["重複", "同樣", "一樣", "反覆", "總是"]):
            # 重複行為 -> M1-01
            for chunk in m1_chunks:
                if chunk.get("chunk_id") == "M1-01":
                    return chunk
        elif any(word in user_lower for word in ["語言", "說話", "表達", "詞彙", "用詞"]):
            # 語言問題 -> M1-03
            for chunk in m1_chunks:
                if chunk.get("chunk_id") == "M1-03":
                    return chunk
        
        # 如果沒有明確匹配，選擇相似度最高的
        return max(m1_chunks, key=lambda x: x.get("similarity_score", 0))
    
    def _get_confidence_level(self, score: float) -> str:
        """轉換數值為信心度等級"""
        if score >= 0.3:
            return "high"
        elif score >= 0.15:
            return "medium"
        else:
            return "low"
    
    def _extract_stage_from_title(self, title: str) -> str:
        """從標題提取階段"""
        if "輕度" in title:
            return "輕度"
        elif "中度" in title:
            return "中度"
        elif "重度" in title:
            return "重度"
        return ""
    
    def _analyze_severity(self, user_input: str, bpsd_chunk: Dict) -> Dict:
        """分析 BPSD 症狀嚴重程度"""
        severity_indicators = bpsd_chunk.get("severity_indicators", {})
        user_lower = user_input.lower()
        
        severity_scores = {"輕度": 0, "中度": 0, "重度": 0}
        
        for severity, indicators in severity_indicators.items():
            for indicator in indicators:
                if any(word in user_lower for word in indicator.lower().split()):
                    severity_scores[severity] += 1
        
        if max(severity_scores.values()) > 0:
            detected_severity = max(severity_scores, key=severity_scores.get)
            return {
                "severity": detected_severity,
                "scores": severity_scores,
                "confidence": severity_scores[detected_severity]
            }
        
        return {"severity": "未確定", "scores": severity_scores, "confidence": 0}
    
    def _generate_summary(self, result: AnalysisResult, user_input: str = "") -> str:
        """生成綜合分析摘要"""
        summary_parts = []
        
        # 根據具體症狀和用戶輸入生成摘要
        if result.symptom_titles:
            # 提取主要症狀
            main_symptoms = []
            for title in result.symptom_titles[:2]:  # 最多取前2個症狀
                # 根據用戶輸入和症狀標題判斷具體症狀
                if "記憶力減退" in title:
                    if any(word in user_input for word in ["重複", "同樣", "一樣", "反覆", "總是"]):
                        main_symptoms.append("重複行為")
                    else:
                        main_symptoms.append("記憶力減退")
                elif "無法勝任" in title or "熟悉" in title:
                    main_symptoms.append("方向感問題")
                elif "語言表達" in title or "表達" in title:
                    main_symptoms.append("語言表達困難")
                elif "重複" in title or "反覆" in title:
                    main_symptoms.append("重複行為")
                else:
                    main_symptoms.append(title.split("：")[0] if "：" in title else title)
            
            if main_symptoms:
                summary_parts.append(f"觀察到{', '.join(main_symptoms)}等症狀")
        
        # 階段評估
        if "M2" in result.modules_used and result.stage_detection:
            stage = result.stage_detection.get("detected_stage", "")
            if stage:
                summary_parts.append(f"評估為{stage}階段")
        
        # BPSD 症狀
        if "M3" in result.modules_used and result.bpsd_analysis:
            bpsd_count = len(result.bpsd_analysis.get("detected_categories", []))
            if bpsd_count > 0:
                summary_parts.append(f"發現{bpsd_count}種行為心理症狀")
        
        # 生成最終摘要
        if summary_parts:
            summary = "；".join(summary_parts) + "。"
            
            # 根據症狀嚴重程度添加建議
            if any("重度" in part for part in summary_parts):
                summary += "建議立即尋求專業醫療評估。"
            elif any("中度" in part for part in summary_parts):
                summary += "建議盡快諮詢醫療專業人員。"
            else:
                summary += "建議尋求專業醫療評估。"
        else:
            summary = "建議持續觀察並適時諮詢醫療專業人員。"
        
        return summary
    
    def _generate_suggestions(self, result: AnalysisResult) -> List[str]:
        """生成行動建議"""
        suggestions = []
        
        # M3 BPSD 管理建議
        if result.bpsd_analysis:
            primary_category = result.bpsd_analysis.get("primary_category")
            if primary_category:
                strategies = primary_category.get("management_strategies", [])
                suggestions.extend(strategies[:2])  # 取前 2 個建議
        
        # 基本建議
        if not suggestions:
            suggestions.append("建議諮詢專業醫療人員進行詳細評估")
        
        if "M2" in result.modules_used:
            suggestions.append("考慮申請長照 2.0 服務")
        
        return suggestions
