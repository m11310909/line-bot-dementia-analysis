try:
    import google.generativeai as genai
    GENAI_AVAILABLE = True
except ImportError:
    GENAI_AVAILABLE = False

from api.core.config import settings
from api.core.exceptions import GeminiAPIError
import asyncio

class GeminiService:
    def __init__(self):
        if GENAI_AVAILABLE and settings.aistudio_api_key:
            try:
                genai.configure(api_key=settings.aistudio_api_key)
                self.model = genai.GenerativeModel('gemini-pro')
                self.configured = True
                print("✅ Google Gemini 已配置")
            except Exception as e:
                self.configured = False
                print(f"⚠️ Google Gemini 配置失敗: {e}")
        else:
            self.configured = False
            if not GENAI_AVAILABLE:
                print("⚠️ Google Generative AI 套件未安裝")
            else:
                print("⚠️ Google Gemini API Key 未設定")
    
    async def analyze(self, prompt: str) -> str:
        """分析文本"""
        if not self.configured:
            raise GeminiAPIError("Gemini API 未配置")
        
        try:
            # 使用 asyncio 包裝同步 API
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(
                None, 
                lambda: self.model.generate_content(prompt)
            )
            return response.text
            
        except Exception as e:
            print(f"Gemini API 錯誤: {e}")
            raise GeminiAPIError(f"API 呼叫失敗: {str(e)}")
    
    def health_check(self) -> bool:
        """健康檢查"""
        return self.configured
