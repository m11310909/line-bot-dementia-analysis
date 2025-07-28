import json
import re
from typing import Dict, Any
from api.modules.base_analyzer import BaseAnalyzer, AnalysisResult
from api.core.exceptions import AnalysisError, GeminiAPIError

class M1Analyzer(BaseAnalyzer):
    """M1 失智症十大警訊分析器"""
    
    WARNING_CATEGORIES = {
        'M1-01': '記憶力減退影響生活',
        'M1-02': '計劃事情或解決問題有困難',
        'M1-03': '無法勝任原本熟悉的事務',
        'M1-04': '對時間地點感到混淆',
        'M1-05': '有困難理解視覺影像和空間關係',
        'M1-06': '言語表達或書寫出現困難',
        'M1-07': '東西擺放錯亂且失去回頭尋找的能力',
        'M1-08': '判斷力變差或減弱',
        'M1-09': '從工作或社交活動中退出',
        'M1-10': '情緒和個性的改變'
    }
    
    async def analyze(self, user_input: str) -> AnalysisResult:
        """分析用戶輸入的失智症警訊"""
        try:
            # 格式化 prompt
            prompt = self.format_prompt(user_input)
            
            # 呼叫 Gemini API
            if self.gemini_service and hasattr(self.gemini_service, 'configured') and self.gemini_service.configured:
                response = await self.gemini_service.analyze(prompt)
                return self._parse_gemini_response(response, user_input)
            else:
                # 備用：基於關鍵字的簡單分析
                return self._keyword_analysis(user_input)
                
        except Exception as e:
            print(f"M1 分析錯誤: {e}")
            # 發生錯誤時返回基本分析結果
            return self._keyword_analysis(user_input)
    
    def _parse_gemini_response(self, response: str, user_input: str) -> AnalysisResult:
        """解析 Gemini API 回應"""
        try:
            # 提取 JSON 部分
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if json_match:
                result_data = json.loads(json_match.group())
                return AnalysisResult(**result_data)
            else:
                # JSON 解析失敗，使用備用分析
                return self._keyword_analysis(user_input)
                
        except json.JSONDecodeError:
            return self._keyword_analysis(user_input)
    
    def _keyword_analysis(self, user_input: str) -> AnalysisResult:
        """基於關鍵字的備用分析"""
        # 簡化的關鍵字匹配邏輯
        keywords_map = {
            'M1-01': ['忘記', '記不住', '重複問', '記憶', '健忘'],
            'M1-02': ['計劃', '解決', '困難', '想不出', '不會'],
            'M1-03': ['不會', '做不到', '熟悉', '原本會'],
            'M1-04': ['時間', '地點', '迷路', '混淆', '不知道'],
            'M1-08': ['判斷', '決定', '選擇困難'],
            'M1-10': ['情緒', '個性', '脾氣', '易怒', '憂鬱']
        }
        
        matched_categories = []
        max_confidence = 0.3
        
        for category, keywords in keywords_map.items():
            if any(keyword in user_input for keyword in keywords):
                matched_categories.append(category)
                max_confidence = max(max_confidence, 0.6)
        
        if not matched_categories:
            matched_categories = ['M1-01']  # 預設分類
        
        category_name = self.WARNING_CATEGORIES.get(matched_categories[0], '')
        
        return AnalysisResult(
            matched_categories=matched_categories,
            category_name=category_name,
            confidence=max_confidence,
            severity=2,
            user_description=user_input[:100] + ('...' if len(user_input) > 100 else ''),
            normal_aging="隨著年齡增長，偶爾出現輕微的記憶問題是正常的",
            warning_sign=f"觀察到的現象可能與 {category_name} 相關",
            recommendations=[
                "建議持續觀察相關症狀的變化",
                "如症狀持續或加重，建議諮詢專業醫師",
                "保持規律作息和適度運動"
            ],
            require_medical_attention=max_confidence > 0.5
        )
