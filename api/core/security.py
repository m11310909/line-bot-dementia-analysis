import hmac
import hashlib
import base64
import re
from fastapi import HTTPException
from api.core.config import settings

def verify_line_signature(body: bytes, signature: str) -> bool:
    """驗證 LINE webhook 簽名"""
    if not signature or not settings.line_channel_secret:
        return True  # 開發模式跳過驗證
        
    hash_digest = hmac.new(
        settings.line_channel_secret.encode('utf-8'),
        body,
        hashlib.sha256
    ).digest()
    expected_signature = base64.b64encode(hash_digest).decode()
    
    if not hmac.compare_digest(signature, expected_signature):
        raise HTTPException(401, "Invalid LINE signature")
    return True

def sanitize_input(user_input: str) -> str:
    """清理和驗證用戶輸入"""
    if not user_input or not user_input.strip():
        raise HTTPException(400, "輸入內容不能為空")
        
    user_input = user_input.strip()
    
    if len(user_input) > settings.max_input_length:
        raise HTTPException(400, f"輸入內容過長，限制 {settings.max_input_length} 字元")
    
    # 移除潛在危險字符但保留中文
    user_input = re.sub(r'[<>"\'\&\|\;]', '', user_input)
    
    return user_input

def check_memory_usage():
    """檢查記憶體使用（Replit 優化）"""
    if not settings.enable_memory_monitor:
        return
        
    try:
        import psutil
        import gc
        
        memory = psutil.virtual_memory()
        if memory.percent > 85:
            gc.collect()  # 強制垃圾回收
            print(f"⚠️ 記憶體使用過高: {memory.percent:.1f}%，已執行垃圾回收")
            
        if memory.percent > 95:
            raise HTTPException(503, "系統記憶體不足，請稍後再試")
            
    except ImportError:
        pass  # psutil 不可用時跳過
