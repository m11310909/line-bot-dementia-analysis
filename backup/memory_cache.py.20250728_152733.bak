# memory_cache.py - 内存缓存替代 Redis
import time
from typing import Any, Optional, Dict

class MemoryCache:
    def __init__(self, default_ttl: int = 3600, max_size: int = 1000):
        self.cache: Dict[str, Dict] = {}
        self.default_ttl = default_ttl
        self.max_size = max_size
    
    def set(self, key: str, value: Any, ttl: Optional[int] = None):
        if len(self.cache) >= self.max_size:
            oldest_key = min(self.cache.keys(), 
                           key=lambda k: self.cache[k]['created_at'])
            del self.cache[oldest_key]
        
        expires_at = time.time() + (ttl or self.default_ttl)
        self.cache[key] = {
            'value': value,
            'expires_at': expires_at,
            'created_at': time.time()
        }
    
    def get(self, key: str) -> Any:
        if key in self.cache:
            item = self.cache[key]
            if time.time() < item['expires_at']:
                return item['value']
            else:
                del self.cache[key]
        return None

# 全局缓存实例
cache = MemoryCache()
