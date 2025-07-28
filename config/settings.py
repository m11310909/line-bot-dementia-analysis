from pydantic import BaseSettings, validator
from typing import Optional
import os

class Settings(BaseSettings):
    # LINE Bot 設定
    line_channel_access_token: str = ""
    line_channel_secret: str = ""
    
    # Google AI 設定
    aistudio_api_key: str = ""
    
    # 服務設定
    api_port: int = 8000
    webhook_port: int = 8002
    debug: bool = False
    
    # 安全設定
    rate_limit_per_minute: int = 60
    max_input_length: int = 1000
    
    # Replit 最佳化
    memory_limit_mb: int = 400
    enable_memory_monitor: bool = True
    
    @validator('max_input_length')
    def validate_input_length(cls, v):
        return min(v, 2000)  # Replit 記憶體限制
    
    class Config:
        env_file = ".env"
        case_sensitive = False

# 單例模式
settings = Settings()
