import os
from dataclasses import dataclass
from typing import Optional

@dataclass
class AppConfig:
    """Lightweight app configuration"""
    # GenAI Settings (choose ONE provider to save memory)
    GENAI_PROVIDER = os.getenv("GENAI_PROVIDER", "openai")  # or "claude"
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    CLAUDE_API_KEY = os.getenv("CLAUDE_API_KEY")
    
    # LINE Settings
    LINE_CHANNEL_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")
    LINE_CHANNEL_SECRET = os.getenv("LINE_CHANNEL_SECRET")
    
    # Memory optimizations
    MAX_WORKERS = 1  # Single worker for Replit
    REQUEST_TIMEOUT = 15  # Shorter timeout
    CACHE_SIZE = 50  # Small cache
    LOG_LEVEL = "WARNING"  # Reduce logging overhead

config = AppConfig()
