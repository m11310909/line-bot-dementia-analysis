"""
統一錯誤處理系統
階段四任務 7.2：改善錯誤處理機制
"""

from typing import Dict, List, Any, Optional
from enum import Enum
import logging
import traceback
from datetime import datetime

class ErrorType(str, Enum):
    NETWORK_ERROR = "network_error"
    AI_CONFIDENCE_LOW = "ai_confidence_low"
    MODULE_NOT_READY = "module_not_ready"
    INPUT_TOO_SHORT = "input_too_short"
    INPUT_UNINTELLIGIBLE = "input_unintelligible"
    API_TIMEOUT = "api_timeout"
    SYSTEM_MAINTENANCE = "system_maintenance"
    UNKNOWN_ERROR = "unknown_error"

class ErrorHandler:
    """統一錯誤處理與使用者友善回應"""
    
    def __init__(self):
        self.error_messages = {
            ErrorType.NETWORK_ERROR: {
                'user_message': '網路連線不穩定，請稍後再試',
                'quick_replies': ['重試', '離線模式', '聯繫客服'],
                'retry_count': 3,
                'backoff_time': 2
            },
            ErrorType.AI_CONFIDENCE_LOW: {
                'user_message': '我不太確定您的狀況，可以選擇以下選項',
                'quick_replies': ['十大警訊', '照護資源', '專業諮詢', '重新描述'],
                'retry_count': 1,
                'backoff_time': 0
            },
            ErrorType.MODULE_NOT_READY: {
                'user_message': '此功能正在準備中，請稍後再試',
                "quick_replies": ['返回主選單', '其他協助', '稍後再試'],
                'retry_count': 0,
                'backoff_time': 0
            },
            ErrorType.INPUT_TOO_SHORT: {
                'user_message': '請提供更多描述，這樣我才能給您更準確的建議',
                'quick_replies': ['重新輸入', '查看範例', '快速選項'],
                'retry_count': 0,
                'backoff_time': 0
            },
            ErrorType.INPUT_UNINTELLIGIBLE: {
                'user_message': '我無法理解您的描述，請用其他方式說明',
                'quick_replies': ['重新描述', '選擇症狀', '尋求協助'],
                'retry_count': 0,
                'backoff_time': 0
            },
            ErrorType.API_TIMEOUT: {
                'user_message': '處理時間較長，請稍等片刻',
                'quick_replies': ['重試', '簡化描述', '稍後再試'],
                'retry_count': 2,
                'backoff_time': 5
            },
            ErrorType.SYSTEM_MAINTENANCE: {
                'user_message': '系統正在維護中，請稍後再試',
                'quick_replies': ['稍後再試', '聯繫客服', '查看狀態'],
                'retry_count': 0,
                'backoff_time': 0
            },
            ErrorType.UNKNOWN_ERROR: {
                'user_message': '發生未知錯誤，請稍後再試',
                'quick_replies': ['重試', '聯繫客服', '返回主選單'],
                'retry_count': 1,
                'backoff_time': 1
            }
        }
        
        # 設置日誌
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
    
    def handle_error(self, error_type: str, context: dict = None) -> Dict[str, Any]:
        """產生錯誤處理的回應"""
        
        error_info = self.error_messages.get(error_type, self.error_messages[ErrorType.UNKNOWN_ERROR])
        
        # 記錄錯誤
        self._log_error(error_type, context)
        
        # 生成 Flex Message
        flex_message = self._create_error_flex_message(error_info, context)
        
        return {
            "error_type": error_type,
            "user_message": error_info['user_message'],
            "quick_replies": error_info['quick_replies'],
            "flex_message": flex_message,
            "retry_config": {
                "max_retries": error_info['retry_count'],
                "backoff_time": error_info['backoff_time']
            },
            "timestamp": datetime.now().isoformat(),
            "context": context or {}
        }
    
    def _create_error_flex_message(self, error_info: dict, context: dict = None) -> Dict[str, Any]:
        """創建錯誤處理的 Flex Message"""
        
        quick_replies = []
        for reply in error_info['quick_replies']:
            quick_replies.append({
                "type": "action",
                "action": {
                    "type": "message",
                    "label": reply,
                    "text": reply
                }
            })
        
        return {
            "type": "flex",
            "altText": error_info['user_message'],
            "contents": {
                "type": "bubble",
                "size": "kilo",
                "header": {
                    "type": "box",
                    "layout": "horizontal",
                    "contents": [
                        {
                            "type": "text",
                            "text": "⚠️ 系統提示",
                            "weight": "bold",
                            "color": "#FF6B6B",
                            "size": "sm"
                        }
                    ]
                },
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "text",
                            "text": error_info['user_message'],
                            "wrap": True,
                            "size": "sm",
                            "color": "#666666"
                        }
                    ]
                },
                "footer": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "box",
                            "layout": "horizontal",
                            "contents": quick_replies[:3]  # 最多顯示 3 個選項
                        }
                    ]
                }
            }
        }
    
    def _log_error(self, error_type: str, context: dict = None):
        """記錄錯誤"""
        error_msg = f"Error Type: {error_type}"
        if context:
            error_msg += f", Context: {context}"
        
        self.logger.error(error_msg)
    
    def classify_error(self, exception: Exception, context: dict = None) -> str:
        """根據異常類型分類錯誤"""
        
        error_msg = str(exception).lower()
        
        if "timeout" in error_msg or "timed out" in error_msg:
            return ErrorType.API_TIMEOUT
        elif "connection" in error_msg or "network" in error_msg:
            return ErrorType.NETWORK_ERROR
        elif "confidence" in error_msg or "uncertain" in error_msg:
            return ErrorType.AI_CONFIDENCE_LOW
        elif "module" in error_msg or "not ready" in error_msg:
            return ErrorType.MODULE_NOT_READY
        elif "input" in error_msg and ("short" in error_msg or "empty" in error_msg):
            return ErrorType.INPUT_TOO_SHORT
        elif "unintelligible" in error_msg or "cannot understand" in error_msg:
            return ErrorType.INPUT_UNINTELLIGIBLE
        else:
            return ErrorType.UNKNOWN_ERROR

class RetryManager:
    """API 呼叫重試管理"""
    
    DEFAULT_CONFIG = {
        'max_retries': 3,
        'backoff_factor': 2,  # 指數退避
        'timeout': 5000,      # 毫秒
        'retry_on': [500, 502, 503, 504]
    }
    
    def __init__(self, config: dict = None):
        self.config = config or self.DEFAULT_CONFIG
        self.retry_history = {}
    
    def should_retry(self, status_code: int, attempt: int) -> bool:
        """判斷是否應該重試"""
        return (
            status_code in self.config['retry_on'] and
            attempt < self.config['max_retries']
        )
    
    def get_backoff_time(self, attempt: int) -> int:
        """計算退避時間"""
        return self.config['backoff_factor'] ** attempt
    
    def record_retry(self, request_id: str, attempt: int, success: bool):
        """記錄重試歷史"""
        if request_id not in self.retry_history:
            self.retry_history[request_id] = []
        
        self.retry_history[request_id].append({
            "attempt": attempt,
            "success": success,
            "timestamp": datetime.now().isoformat()
        })
    
    def get_retry_stats(self, request_id: str) -> Dict[str, Any]:
        """獲取重試統計"""
        if request_id not in self.retry_history:
            return {"total_attempts": 0, "success_rate": 0.0}
        
        attempts = self.retry_history[request_id]
        total_attempts = len(attempts)
        successful_attempts = len([a for a in attempts if a["success"]])
        
        return {
            "total_attempts": total_attempts,
            "successful_attempts": successful_attempts,
            "success_rate": successful_attempts / total_attempts if total_attempts > 0 else 0.0,
            "last_attempt": attempts[-1] if attempts else None
        }

class ErrorRecovery:
    """錯誤恢復策略"""
    
    def __init__(self):
        self.error_handler = ErrorHandler()
        self.retry_manager = RetryManager()
    
    def handle_api_call(self, api_func, *args, **kwargs):
        """處理 API 呼叫的錯誤恢復"""
        max_retries = self.retry_manager.config['max_retries']
        
        for attempt in range(max_retries + 1):
            try:
                result = api_func(*args, **kwargs)
                self.retry_manager.record_retry("api_call", attempt, True)
                return result
                
            except Exception as e:
                error_type = self.error_handler.classify_error(e)
                error_response = self.error_handler.handle_error(error_type, {
                    "attempt": attempt,
                    "max_retries": max_retries,
                    "exception": str(e)
                })
                
                self.retry_manager.record_retry("api_call", attempt, False)
                
                # 如果還有重試機會
                if attempt < max_retries and self.retry_manager.should_retry(500, attempt):
                    backoff_time = self.retry_manager.get_backoff_time(attempt)
                    import time
                    time.sleep(backoff_time)
                    continue
                else:
                    return error_response
        
        return self.error_handler.handle_error(ErrorType.UNKNOWN_ERROR)

# 使用範例
def example_usage():
    """錯誤處理系統使用範例"""
    
    # 創建錯誤處理器
    error_handler = ErrorHandler()
    retry_manager = RetryManager()
    error_recovery = ErrorRecovery()
    
    # 測試錯誤處理
    error_response = error_handler.handle_error(
        ErrorType.AI_CONFIDENCE_LOW,
        {"confidence": 0.3, "user_input": "頭痛"}
    )
    
    print("錯誤處理回應:", error_response)
    
    # 測試重試管理
    retry_stats = retry_manager.get_retry_stats("test_request")
    print("重試統計:", retry_stats)
    
    return error_response

if __name__ == "__main__":
    example_usage() 