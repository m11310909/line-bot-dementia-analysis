from abc import ABC, abstractmethod
from typing import Dict, Any, List
import yaml
from pathlib import Path

class AnalysisResult:
    def __init__(self, **kwargs):
        self.matched_categories = kwargs.get('matched_categories', [])
        self.category_name = kwargs.get('category_name', '')
        self.confidence = kwargs.get('confidence', 0.0)
        self.severity = kwargs.get('severity', 1)
        self.user_description = kwargs.get('user_description', '')
        self.normal_aging = kwargs.get('normal_aging', '')
        self.warning_sign = kwargs.get('warning_sign', '')
        self.recommendations = kwargs.get('recommendations', [])
        self.require_medical_attention = kwargs.get('require_medical_attention', False)
        self.disclaimer = kwargs.get('disclaimer', '此分析僅供參考，請諮詢專業醫師進行正式評估')
    
    def dict(self):
        return {
            'matched_categories': self.matched_categories,
            'category_name': self.category_name,
            'confidence': self.confidence,
            'severity': self.severity,
            'user_description': self.user_description,
            'normal_aging': self.normal_aging,
            'warning_sign': self.warning_sign,
            'recommendations': self.recommendations,
            'require_medical_attention': self.require_medical_attention,
            'disclaimer': self.disclaimer
        }

class BaseAnalyzer(ABC):
    def __init__(self, gemini_service=None):
        self.gemini_service = gemini_service
        self.module_name = self.__class__.__name__.replace('Analyzer', '').lower()
        self.prompts = self._load_prompts()
    
    def _load_prompts(self) -> Dict[str, Any]:
        """載入 Prompt 模板"""
        try:
            prompt_file = Path(f"data/prompts/{self.module_name}_prompts.yaml")
            if prompt_file.exists():
                with open(prompt_file, 'r', encoding='utf-8') as f:
                    return yaml.safe_load(f)
        except Exception as e:
            print(f"載入 prompt 失敗: {e}")
        return {}
    
    @abstractmethod
    async def analyze(self, user_input: str) -> AnalysisResult:
        """分析用戶輸入"""
        pass
    
    def format_prompt(self, user_input: str, **kwargs) -> str:
        """格式化 Prompt"""
        template = self.prompts.get('analysis_prompt', '')
        return template.format(user_input=user_input, **kwargs)
