from abc import ABC, abstractmethod
from typing import Dict, Any, List
from pydantic import BaseModel
import yaml
from pathlib import Path

class AnalysisResult(BaseModel):
    matched_categories: List[str] = []
    category_name: str = ""
    confidence: float = 0.0
    severity: int = 1  # 1-5
    user_description: str = ""
    normal_aging: str = ""
    warning_sign: str = ""
    recommendations: List[str] = []
    require_medical_attention: bool = False
    disclaimer: str = "此分析僅供參考，請諮詢專業醫師進行正式評估"

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
