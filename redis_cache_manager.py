#!/usr/bin/env python3
"""
Redis 快取管理器
提升 API 效能，減少重複計算和 API 呼叫
"""

import redis
import json
import hashlib
import time
import logging
from typing import Optional, Dict, Any, List, Union
from functools import wraps
import os

# 配置日誌
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RedisCacheManager:
    """Redis 快取管理器"""
    
    def __init__(self, redis_url: str = None, password: str = None, db: int = 0):
        """初始化 Redis 快取管理器"""
        self.redis_url = redis_url or os.getenv('REDIS_URL', 'redis://localhost:6379')
        self.password = password or os.getenv('REDIS_PASSWORD')
        self.db = db or int(os.getenv('REDIS_DB', '0'))
        
        # 快取配置
        self.default_ttl = 3600  # 1 小時
        self.analysis_ttl = 1800  # 30 分鐘
        self.user_session_ttl = 7200  # 2 小時
        self.flex_message_ttl = 3600  # 1 小時
        
        # 初始化 Redis 連接
        self.redis_client = None
        self._connect_redis()
    
    def _connect_redis(self):
        """連接 Redis"""
        try:
            if self.redis_url.startswith('redis://'):
                # 解析 Redis URL
                from urllib.parse import urlparse
                parsed = urlparse(self.redis_url)
                host = parsed.hostname or 'localhost'
                port = parsed.port or 6379
                password = parsed.password or self.password
                db = parsed.path.lstrip('/') if parsed.path else str(self.db)
                db = int(db) if db.isdigit() else self.db
                
                self.redis_client = redis.Redis(
                    host=host,
                    port=port,
                    password=password,
                    db=db,
                    decode_responses=True,
                    socket_connect_timeout=5,
                    socket_timeout=5
                )
            else:
                # 直接連接
                self.redis_client = redis.Redis(
                    host='localhost',
                    port=6379,
                    password=self.password,
                    db=self.db,
                    decode_responses=True
                )
            
            # 測試連接
            self.redis_client.ping()
            logger.info("✅ Redis 連接成功")
            
        except redis.ConnectionError as e:
            logger.warning(f"⚠️  Redis 連接失敗: {e}")
            self.redis_client = None
        except Exception as e:
            logger.error(f"❌ Redis 初始化錯誤: {e}")
            self.redis_client = None
    
    def is_available(self) -> bool:
        """檢查 Redis 是否可用"""
        if not self.redis_client:
            return False
        
        try:
            self.redis_client.ping()
            return True
        except:
            return False
    
    def _generate_cache_key(self, prefix: str, *args, **kwargs) -> str:
        """生成快取鍵值"""
        # 將參數轉換為字串
        key_parts = [prefix]
        
        # 添加位置參數
        for arg in args:
            key_parts.append(str(arg))
        
        # 添加關鍵字參數（排序以確保一致性）
        for key in sorted(kwargs.keys()):
            key_parts.append(f"{key}:{kwargs[key]}")
        
        # 生成 MD5 雜湊
        key_string = "|".join(key_parts)
        return f"cache:{hashlib.md5(key_string.encode()).hexdigest()}"
    
    def get(self, key: str) -> Optional[Any]:
        """獲取快取值"""
        if not self.is_available():
            return None
        
        try:
            value = self.redis_client.get(key)
            if value:
                return json.loads(value)
            return None
        except Exception as e:
            logger.error(f"❌ Redis 讀取錯誤: {e}")
            return None
    
    def set(self, key: str, value: Any, ttl: int = None) -> bool:
        """設置快取值"""
        if not self.is_available():
            return False
        
        try:
            ttl = ttl or self.default_ttl
            serialized_value = json.dumps(value, ensure_ascii=False)
            return self.redis_client.setex(key, ttl, serialized_value)
        except Exception as e:
            logger.error(f"❌ Redis 寫入錯誤: {e}")
            return False
    
    def delete(self, key: str) -> bool:
        """刪除快取值"""
        if not self.is_available():
            return False
        
        try:
            return bool(self.redis_client.delete(key))
        except Exception as e:
            logger.error(f"❌ Redis 刪除錯誤: {e}")
            return False
    
    def exists(self, key: str) -> bool:
        """檢查鍵是否存在"""
        if not self.is_available():
            return False
        
        try:
            return bool(self.redis_client.exists(key))
        except Exception as e:
            logger.error(f"❌ Redis 檢查錯誤: {e}")
            return False
    
    def clear_pattern(self, pattern: str) -> int:
        """清除符合模式的鍵"""
        if not self.is_available():
            return 0
        
        try:
            keys = self.redis_client.keys(pattern)
            if keys:
                return self.redis_client.delete(*keys)
            return 0
        except Exception as e:
            logger.error(f"❌ Redis 清除模式錯誤: {e}")
            return 0
    
    # 特定功能的快取方法
    
    def cache_analysis_result(self, user_input: str, result: Dict[str, Any]) -> bool:
        """快取分析結果"""
        key = self._generate_cache_key("analysis", user_input)
        return self.set(key, result, self.analysis_ttl)
    
    def get_cached_analysis(self, user_input: str) -> Optional[Dict[str, Any]]:
        """獲取快取的分析結果"""
        key = self._generate_cache_key("analysis", user_input)
        return self.get(key)
    
    def cache_flex_message(self, user_input: str, flex_message: Dict[str, Any]) -> bool:
        """快取 Flex Message"""
        key = self._generate_cache_key("flex", user_input)
        return self.set(key, flex_message, self.flex_message_ttl)
    
    def get_cached_flex_message(self, user_input: str) -> Optional[Dict[str, Any]]:
        """獲取快取的 Flex Message"""
        key = self._generate_cache_key("flex", user_input)
        return self.get(key)
    
    def cache_user_session(self, user_id: str, session_data: Dict[str, Any]) -> bool:
        """快取用戶會話"""
        key = f"session:{user_id}"
        return self.set(key, session_data, self.user_session_ttl)
    
    def get_user_session(self, user_id: str) -> Optional[Dict[str, Any]]:
        """獲取用戶會話"""
        key = f"session:{user_id}"
        return self.get(key)
    
    def cache_gemini_response(self, prompt: str, response: str) -> bool:
        """快取 Gemini API 回應"""
        key = self._generate_cache_key("gemini", prompt)
        return self.set(key, response, self.analysis_ttl)
    
    def get_cached_gemini_response(self, prompt: str) -> Optional[str]:
        """獲取快取的 Gemini API 回應"""
        key = self._generate_cache_key("gemini", prompt)
        return self.get(key)
    
    def cache_similarity_search(self, query: str, results: List[Dict[str, Any]]) -> bool:
        """快取相似度搜尋結果"""
        key = self._generate_cache_key("similarity", query)
        return self.set(key, results, self.analysis_ttl)
    
    def get_cached_similarity_search(self, query: str) -> Optional[List[Dict[str, Any]]]:
        """獲取快取的相似度搜尋結果"""
        key = self._generate_cache_key("similarity", query)
        return self.get(key)
    
    # 統計和監控方法
    
    def get_cache_stats(self) -> Dict[str, Any]:
        """獲取快取統計資訊"""
        if not self.is_available():
            return {"status": "unavailable"}
        
        try:
            info = self.redis_client.info()
            return {
                "status": "available",
                "total_keys": info.get('db0', {}).get('keys', 0),
                "memory_usage": info.get('used_memory_human', 'N/A'),
                "hit_rate": info.get('keyspace_hits', 0),
                "miss_rate": info.get('keyspace_misses', 0)
            }
        except Exception as e:
            logger.error(f"❌ 獲取快取統計錯誤: {e}")
            return {"status": "error", "error": str(e)}
    
    def clear_all_cache(self) -> bool:
        """清除所有快取"""
        if not self.is_available():
            return False
        
        try:
            self.redis_client.flushdb()
            logger.info("✅ 所有快取已清除")
            return True
        except Exception as e:
            logger.error(f"❌ 清除快取錯誤: {e}")
            return False

# 快取裝飾器
def cache_result(ttl: int = None, key_prefix: str = "default"):
    """快取結果裝飾器"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # 獲取快取管理器實例
            cache_manager = getattr(wrapper, '_cache_manager', None)
            if not cache_manager:
                cache_manager = RedisCacheManager()
                wrapper._cache_manager = cache_manager
            
            # 生成快取鍵
            cache_key = cache_manager._generate_cache_key(key_prefix, *args, **kwargs)
            
            # 嘗試從快取獲取結果
            cached_result = cache_manager.get(cache_key)
            if cached_result is not None:
                logger.info(f"✅ 快取命中: {func.__name__}")
                return cached_result
            
            # 執行原始函數
            result = func(*args, **kwargs)
            
            # 快取結果
            cache_manager.set(cache_key, result, ttl)
            logger.info(f"💾 快取儲存: {func.__name__}")
            
            return result
        return wrapper
    return decorator

# 全域快取管理器實例
cache_manager = RedisCacheManager()

# 使用範例
if __name__ == "__main__":
    # 測試快取功能
    print("🧪 測試 Redis 快取功能...")
    
    # 測試連接
    if cache_manager.is_available():
        print("✅ Redis 連接成功")
        
        # 測試基本快取操作
        test_key = "test:key"
        test_value = {"message": "Hello Redis!", "timestamp": time.time()}
        
        # 設置快取
        if cache_manager.set(test_key, test_value, 60):
            print("✅ 快取設置成功")
        
        # 獲取快取
        cached_value = cache_manager.get(test_key)
        if cached_value:
            print(f"✅ 快取讀取成功: {cached_value}")
        
        # 獲取統計資訊
        stats = cache_manager.get_cache_stats()
        print(f"📊 快取統計: {stats}")
        
    else:
        print("❌ Redis 連接失敗，請確保 Redis 服務正在運行")
        print("💡 啟動 Redis: brew services start redis") 