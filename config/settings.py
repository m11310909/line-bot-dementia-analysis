import os
from typing import Optional

class Settings:
    def __init__(self):
        # LINE Bot 設定 - 從 Replit secrets 讀取
        self.line_channel_access_token = os.getenv('LINE_CHANNEL_ACCESS_TOKEN', '')
        self.line_channel_secret = os.getenv('LINE_CHANNEL_SECRET', '')
        
        # Google AI 設定
        self.aistudio_api_key = os.getenv('AISTUDIO_API_KEY', '')
        
        # 也檢查其他可能的命名
        if not self.line_channel_access_token:
            self.line_channel_access_token = os.getenv('LINE_ACCESS_TOKEN', '')
        if not self.aistudio_api_key:
            self.aistudio_api_key = os.getenv('GOOGLE_AI_API_KEY', '')
        
        # 服務設定
        self.api_port = int(os.getenv('API_PORT', '8000'))
        self.webhook_port = int(os.getenv('WEBHOOK_PORT', '8002'))
        self.debug = os.getenv('DEBUG', 'false').lower() == 'true'
        
        # 安全設定
        self.rate_limit_per_minute = int(os.getenv('RATE_LIMIT_PER_MINUTE', '60'))
        self.max_input_length = min(int(os.getenv('MAX_INPUT_LENGTH', '1000')), 2000)
        
        # Replit 最佳化
        self.memory_limit_mb = int(os.getenv('MEMORY_LIMIT_MB', '400'))
        self.enable_memory_monitor = os.getenv('ENABLE_MEMORY_MONITOR', 'true').lower() == 'true'

# 單例模式
settings = Settings()
