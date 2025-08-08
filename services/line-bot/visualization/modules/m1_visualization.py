"""
🎯 M1 模組視覺化處理器
失智症警訊徵兆檢測的視覺化功能
"""

from typing import Dict, List, Any, Optional
import re
import sys
import os

# 添加父目錄到 Python 路徑
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from components.charts import FlexMessageBuilder, ChartComponents


class M1VisualizationProcessor:
    """M1 模組視覺化處理器"""

    # 失智症相關症狀關鍵詞
    SYMPTOMS_KEYWORDS = {
        "記憶力": ["忘記", "記憶", "記不住", "健忘", "失憶"],
        "語言能力": ["說話", "語言", "表達", "詞彙", "溝通"],
        "定向力": ["迷路", "方向", "時間", "地點", "混淆"],
        "執行功能": ["計劃", "組織", "決策", "解決問題"],
        "視覺空間": ["空間", "視覺", "距離", "方向感"],
        "注意力": ["專注", "注意力", "分心", "集中"],
        "情緒": ["情緒", "心情", "焦慮", "憂鬱", "易怒"],
        "行為": ["行為", "性格", "習慣", "社交"],
    }

    # 風險因素關鍵詞
    RISK_FACTORS = {
        "年齡": ["年紀", "年齡", "老年", "高齡"],
        "家族史": ["家族", "遺傳", "父母", "親戚"],
        "心血管疾病": ["心臟", "血管", "高血壓", "糖尿病"],
        "頭部創傷": ["撞頭", "跌倒", "受傷", "創傷"],
        "生活方式": ["運動", "飲食", "睡眠", "壓力"],
    }

    def __init__(self):
        """初始化處理器"""
        pass

    def analyze_text(self, text: str) -> Dict[str, Any]:
        """
        分析文本並提取症狀和風險因素

        Args:
            text: 用戶輸入的文本

        Returns:
            分析結果字典
        """
        # 提取症狀
        symptoms = self._extract_symptoms(text)

        # 提取風險因素
        risk_factors = self._extract_risk_factors(text)

        # 計算警訊等級
        warning_level = self._calculate_warning_level(symptoms, risk_factors)

        # 生成警訊訊息
        warning_message = self._generate_warning_message(warning_level, symptoms)

        return {
            "symptoms": symptoms,
            "risk_factors": risk_factors,
            "warning_level": warning_level,
            "warning_message": warning_message,
            "timeline_events": self._generate_timeline_events(text),
        }

    def _extract_symptoms(self, text: str) -> Dict[str, int]:
        """
        從文本中提取症狀及其嚴重程度

        Args:
            text: 用戶輸入的文本

        Returns:
            症狀字典，格式為 {"症狀名": 嚴重程度(1-5)}
        """
        symptoms = {}

        for symptom_category, keywords in self.SYMPTOMS_KEYWORDS.items():
            severity = 0

            # 檢查關鍵詞出現頻率
            for keyword in keywords:
                if keyword in text:
                    severity += 1

            # 根據出現頻率和強度詞調整嚴重程度
            if severity > 0:
                # 檢查強度詞
                intensity_words = {
                    "很": 2,
                    "非常": 3,
                    "極度": 4,
                    "嚴重": 4,
                    "輕微": 1,
                    "稍微": 1,
                    "一點": 1,
                }

                for word, intensity in intensity_words.items():
                    if word in text:
                        severity = max(severity, intensity)
                        break

                # 限制在 1-5 範圍內
                severity = min(max(severity, 1), 5)
                symptoms[symptom_category] = severity

        return symptoms

    def _extract_risk_factors(self, text: str) -> Dict[str, float]:
        """
        從文本中提取風險因素

        Args:
            text: 用戶輸入的文本

        Returns:
            風險因素字典，格式為 {"風險因素": 風險值(0-1)}
        """
        risk_factors = {}

        for factor, keywords in self.RISK_FACTORS.items():
            risk = 0.0

            # 檢查關鍵詞出現
            for keyword in keywords:
                if keyword in text:
                    risk += 0.2

            # 根據年齡相關詞調整風險
            if "年齡" in factor:
                age_patterns = [
                    (r"(\d+)歲", lambda x: min(float(x) / 100, 1.0)),
                    (r"年紀大", lambda x: 0.8),
                    (r"老年", lambda x: 0.7),
                    (r"高齡", lambda x: 0.9),
                ]

                for pattern, risk_func in age_patterns:
                    match = re.search(pattern, text)
                    if match:
                        risk = max(
                            risk, risk_func(match.group(1) if match.groups() else 0)
                        )

            if risk > 0:
                risk_factors[factor] = min(risk, 1.0)

        return risk_factors

    def _calculate_warning_level(
        self, symptoms: Dict[str, int], risk_factors: Dict[str, float]
    ) -> int:
        """
        計算警訊等級

        Args:
            symptoms: 症狀字典
            risk_factors: 風險因素字典

        Returns:
            警訊等級 (1-5)
        """
        # 計算症狀嚴重程度總分
        symptom_score = sum(symptoms.values()) / len(symptoms) if symptoms else 0

        # 計算風險因素總分
        risk_score = (
            sum(risk_factors.values()) / len(risk_factors) if risk_factors else 0
        )

        # 綜合評分
        total_score = (symptom_score * 0.7 + risk_score * 0.3) * 5

        # 轉換為警訊等級
        if total_score < 1.5:
            return 1  # 正常
        elif total_score < 2.5:
            return 2  # 注意
        elif total_score < 3.5:
            return 3  # 警告
        elif total_score < 4.5:
            return 4  # 危險
        else:
            return 5  # 緊急

    def _generate_warning_message(
        self, warning_level: int, symptoms: Dict[str, int]
    ) -> str:
        """
        生成警訊訊息

        Args:
            warning_level: 警訊等級
            symptoms: 症狀字典

        Returns:
            警訊訊息
        """
        messages = {
            1: "目前症狀輕微，建議定期觀察",
            2: "需要關注症狀變化，建議諮詢醫生",
            3: "症狀明顯，建議盡快就醫檢查",
            4: "症狀嚴重，建議立即就醫",
            5: "症狀非常嚴重，建議緊急就醫",
        }

        base_message = messages.get(warning_level, messages[1])

        # 添加具體症狀建議
        if symptoms:
            top_symptoms = sorted(symptoms.items(), key=lambda x: x[1], reverse=True)[
                :3
            ]
            symptom_text = "、".join([f"{symptom}" for symptom, _ in top_symptoms])
            base_message += f"\n主要症狀：{symptom_text}"

        return base_message

    def _generate_timeline_events(self, text: str) -> List[Dict[str, Any]]:
        """
        生成時間軸事件（模擬數據）

        Args:
            text: 用戶輸入的文本

        Returns:
            時間軸事件列表
        """
        # 這裡可以根據實際需求從數據庫或分析結果中提取
        # 目前使用模擬數據
        events = []

        # 根據文本內容生成模擬時間軸
        if "最近" in text or "這幾天" in text:
            events.append({"date": "最近幾天", "symptom": "症狀加重", "severity": 4})

        if "以前" in text or "之前" in text:
            events.append({"date": "之前", "symptom": "症狀輕微", "severity": 2})

        return events

    def create_visualization(self, analysis_result: Dict[str, Any]) -> FlexSendMessage:
        """
        創建 M1 模組的視覺化 Flex Message

        Args:
            analysis_result: 分析結果字典

        Returns:
            FlexSendMessage
        """
        return FlexMessageBuilder.create_m1_analysis_message(
            symptoms=analysis_result.get("symptoms", {}),
            risk_factors=analysis_result.get("risk_factors", {}),
            warning_level=analysis_result.get("warning_level", 1),
            warning_message=analysis_result.get("warning_message", ""),
            timeline_events=analysis_result.get("timeline_events", []),
        )
