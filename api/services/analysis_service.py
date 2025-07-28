from api.modules.m1_analyzer import M1Analyzer
from api.services.gemini_service import GeminiService
from api.core.security import sanitize_input, check_memory_usage
from api.core.exceptions import AnalysisError

class AnalysisService:
    def __init__(self):
        self.gemini_service = GeminiService()
        self.analyzers = {
            'm1': M1Analyzer(self.gemini_service)
        }
    
    async def analyze(self, module: str, user_input: str):
        """執行分析"""
        # 記憶體檢查
        check_memory_usage()
        
        # 輸入清理
        clean_input = sanitize_input(user_input)
        
        # 取得分析器
        analyzer = self.analyzers.get(module.lower())
        if not analyzer:
            raise AnalysisError(f"不支援的分析模組: {module}")
        
        # 執行分析
        result = await analyzer.analyze(clean_input)
        return result
    
    def get_available_modules(self):
        """取得可用模組"""
        return list(self.analyzers.keys())
