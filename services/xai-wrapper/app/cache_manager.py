import redis
import json
from typing import Optional

class CacheManager:
    def __init__(self):
        try:
            self.redis_client = redis.Redis(
                host='localhost',
                port=6379,
                decode_responses=True
            )
            self.redis_client.ping()
        except:
            self.redis_client = None
    
    async def get(self, key: str) -> Optional[str]:
        if not self.redis_client:
            return None
        try:
            return self.redis_client.get(key)
        except:
            return None
    
    async def set(self, key: str, value: str, ttl: int = 3600) -> bool:
        if not self.redis_client:
            return False
        try:
            self.redis_client.setex(key, ttl, value)
            return True
        except:
            return False
