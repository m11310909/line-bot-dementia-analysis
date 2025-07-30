"""
生產環境配置檔案
"""

import os
from typing import Optional

class ProductionConfig:
    """生產環境配置類別"""
    
    # LINE Bot 配置
    LINE_CHANNEL_ACCESS_TOKEN: str = os.getenv('LINE_CHANNEL_ACCESS_TOKEN', '')
    LINE_CHANNEL_SECRET: str = os.getenv('LINE_CHANNEL_SECRET', '')
    
    # API 配置
    FLEX_API_URL: str = os.getenv('FLEX_API_URL', 'http://localhost:8005/comprehensive-analysis')
    RAG_HEALTH_URL: str = os.getenv('RAG_HEALTH_URL', 'http://localhost:8005/health')
    RAG_ANALYZE_URL: str = os.getenv('RAG_ANALYZE_URL', 'http://localhost:8005/comprehensive-analysis')
    
    # 環境配置
    ENVIRONMENT: str = os.getenv('ENVIRONMENT', 'production')
    DEBUG_MODE: bool = os.getenv('DEBUG_MODE', 'false').lower() == 'true'
    LOG_LEVEL: str = os.getenv('LOG_LEVEL', 'INFO')
    
    # Redis 配置
    REDIS_URL: str = os.getenv('REDIS_URL', 'redis://localhost:6379')
    REDIS_PASSWORD: Optional[str] = os.getenv('REDIS_PASSWORD')
    REDIS_DB: int = int(os.getenv('REDIS_DB', '0'))
    
    # Gemini API 配置
    AISTUDIO_API_KEY: str = os.getenv('AISTUDIO_API_KEY', '')
    GEMINI_MODEL: str = os.getenv('GEMINI_MODEL', 'gemini-1.5-flash')
    GEMINI_MAX_TOKENS: int = int(os.getenv('GEMINI_MAX_TOKENS', '1000'))
    
    # 監控配置
    ENABLE_MONITORING: bool = os.getenv('ENABLE_MONITORING', 'true').lower() == 'true'
    ENABLE_LOGGING: bool = os.getenv('ENABLE_LOGGING', 'true').lower() == 'true'
    ENABLE_METRICS: bool = os.getenv('ENABLE_METRICS', 'true').lower() == 'true'
    
    @classmethod
    def validate(cls) -> bool:
        """驗證配置是否完整"""
        required_fields = [
            'LINE_CHANNEL_ACCESS_TOKEN',
            'LINE_CHANNEL_SECRET',
            'AISTUDIO_API_KEY'
        ]
        
        for field in required_fields:
            if not getattr(cls, field):
                print(f"❌ 缺少必要配置: {field}")
                return False
        
        return True
    
    @classmethod
    def get_webhook_url(cls) -> str:
        """獲取 webhook URL"""
        # 這裡需要根據實際部署環境調整
        return "https://your-domain.com/webhook"

# 全域配置實例
config = ProductionConfig()
