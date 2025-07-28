from fastapi import HTTPException

class AnalysisError(Exception):
    """分析錯誤"""
    pass

class GeminiAPIError(Exception):
    """Gemini API 錯誤"""
    pass

class FlexMessageError(Exception):
    """Flex Message 建構錯誤"""
    pass

def handle_analysis_error(error: Exception) -> HTTPException:
    """統一錯誤處理"""
    if isinstance(error, GeminiAPIError):
        return HTTPException(503, "AI 分析服務暫時無法使用，請稍後再試")
    elif isinstance(error, FlexMessageError):
        return HTTPException(500, "回應格式建構失敗")
    else:
        return HTTPException(500, "系統處理錯誤，請稍後再試")
