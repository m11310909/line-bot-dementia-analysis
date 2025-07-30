#!/usr/bin/env python3
"""
優化 Gemini API 客戶端
降低成本、提升效能、智能快取
"""

import google.generativeai as genai
import time
import json
import logging
from typing import Dict, Any, List, Optional, Tuple
from functools import wraps
import os
from redis_cache_manager import RedisCacheManager

# 配置日誌
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class OptimizedGeminiClient:
    """優化 Gemini API 客戶端"""
    
    def __init__(self, api_key: str = None):
        """初始化優化 Gemini 客戶端"""
        self.api_key = api_key or os.getenv('GEMINI_API_KEY')
        self.cache_manager = RedisCacheManager()
        
        # 成本優化配置
        self.model_config = {
            'gemini-1.5-flash': {
                'max_tokens': 1000,
                'temperature': 0.3,
                'top_p': 0.8,
                'cost_per_1k_tokens': 0.000075  # 美元
            },
            'gemini-1.5-pro': {
                'max_tokens': 2000,
                'temperature': 0.4,
                'top_p': 0.9,
                'cost_per_1k_tokens': 0.00375  # 美元
            }
        }
        
        # 使用統計
        self.usage_stats = {
            'total_requests': 0,
            'cache_hits': 0,
            'total_tokens': 0,
            'estimated_cost': 0.0
        }
        
        # 初始化 Gemini
        self._init_gemini()
    
    def _init_gemini(self):
        """初始化 Gemini API"""
        if not self.api_key or self.api_key == 'your_actual_gemini_api_key_here':
            logger.error("❌ 缺少 Gemini API 金鑰")
            self.model = None
            return
        
        try:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel('gemini-1.5-flash')
            logger.info("✅ Gemini API 初始化成功")
        except Exception as e:
            logger.error(f"❌ Gemini API 初始化失敗: {e}")
            self.model = None
    
    def _estimate_tokens(self, text: str) -> int:
        """估算 token 數量（粗略估算）"""
        # 中文約 1.5 字元/token，英文約 4 字元/token
        chinese_chars = sum(1 for c in text if '\u4e00' <= c <= '\u9fff')
        english_chars = len(text) - chinese_chars
        
        return int(chinese_chars / 1.5 + english_chars / 4)
    
    def _calculate_cost(self, input_tokens: int, output_tokens: int, model: str = 'gemini-1.5-flash') -> float:
        """計算 API 呼叫成本"""
        config = self.model_config.get(model, self.model_config['gemini-1.5-flash'])
        cost_per_1k = config['cost_per_1k_tokens']
        
        total_tokens = input_tokens + output_tokens
        return (total_tokens / 1000) * cost_per_1k
    
    def _optimize_prompt(self, prompt: str, max_tokens: int = 1000) -> str:
        """優化提示詞，減少 token 使用"""
        # 移除多餘空白
        prompt = ' '.join(prompt.split())
        
        # 截斷過長的提示詞
        estimated_tokens = self._estimate_tokens(prompt)
        if estimated_tokens > max_tokens * 0.7:  # 保留 30% 給回應
            # 智能截斷，保留重要部分
            words = prompt.split()
            target_words = int(max_tokens * 0.7 / 2)  # 粗略估算
            if len(words) > target_words:
                prompt = ' '.join(words[:target_words]) + '...'
        
        return prompt
    
    def _get_cached_response(self, prompt: str) -> Optional[str]:
        """獲取快取的回應"""
        return self.cache_manager.get_cached_gemini_response(prompt)
    
    def _cache_response(self, prompt: str, response: str) -> bool:
        """快取回應"""
        return self.cache_manager.cache_gemini_response(prompt, response)
    
    def generate_response(self, prompt: str, model: str = 'gemini-1.5-flash', 
                         max_tokens: int = None, use_cache: bool = True) -> Dict[str, Any]:
        """生成回應（優化版本）"""
        start_time = time.time()
        
        # 更新使用統計
        self.usage_stats['total_requests'] += 1
        
        # 檢查快取
        if use_cache:
            cached_response = self._get_cached_response(prompt)
            if cached_response:
                self.usage_stats['cache_hits'] += 1
                logger.info(f"✅ 快取命中，節省 API 呼叫")
                return {
                    'response': cached_response,
                    'cached': True,
                    'tokens_used': 0,
                    'cost': 0.0,
                    'response_time': time.time() - start_time
                }
        
        # 優化提示詞
        optimized_prompt = self._optimize_prompt(prompt, max_tokens or 1000)
        
        # 估算輸入 tokens
        input_tokens = self._estimate_tokens(optimized_prompt)
        
        try:
            # 配置模型參數
            config = self.model_config.get(model, self.model_config['gemini-1.5-flash'])
            generation_config = genai.types.GenerationConfig(
                max_output_tokens=max_tokens or config['max_tokens'],
                temperature=config['temperature'],
                top_p=config['top_p']
            )
            
            # 生成回應
            response = self.model.generate_content(
                optimized_prompt,
                generation_config=generation_config
            )
            
            # 計算統計
            output_tokens = self._estimate_tokens(response.text)
            total_tokens = input_tokens + output_tokens
            cost = self._calculate_cost(input_tokens, output_tokens, model)
            
            # 更新統計
            self.usage_stats['total_tokens'] += total_tokens
            self.usage_stats['estimated_cost'] += cost
            
            # 快取回應
            if use_cache:
                self._cache_response(prompt, response.text)
            
            response_time = time.time() - start_time
            
            logger.info(f"💡 API 呼叫完成 - Tokens: {total_tokens}, 成本: ${cost:.6f}, 時間: {response_time:.2f}s")
            
            return {
                'response': response.text,
                'cached': False,
                'tokens_used': total_tokens,
                'input_tokens': input_tokens,
                'output_tokens': output_tokens,
                'cost': cost,
                'response_time': response_time,
                'model': model
            }
            
        except Exception as e:
            logger.error(f"❌ Gemini API 呼叫失敗: {e}")
            return {
                'response': f"抱歉，處理您的請求時發生錯誤: {str(e)}",
                'cached': False,
                'error': str(e),
                'tokens_used': 0,
                'cost': 0.0,
                'response_time': time.time() - start_time
            }
    
    def batch_generate(self, prompts: List[str], model: str = 'gemini-1.5-flash') -> List[Dict[str, Any]]:
        """批次生成回應（成本優化）"""
        results = []
        
        for i, prompt in enumerate(prompts):
            logger.info(f"🔄 處理批次請求 {i+1}/{len(prompts)}")
            result = self.generate_response(prompt, model)
            results.append(result)
            
            # 批次間隔，避免速率限制
            if i < len(prompts) - 1:
                time.sleep(0.5)
        
        return results
    
    def get_usage_stats(self) -> Dict[str, Any]:
        """獲取使用統計"""
        cache_stats = self.cache_manager.get_cache_stats()
        
        return {
            'api_usage': self.usage_stats,
            'cache_stats': cache_stats,
            'cost_optimization': {
                'cache_hit_rate': (self.usage_stats['cache_hits'] / max(self.usage_stats['total_requests'], 1)) * 100,
                'estimated_savings': self.usage_stats['cache_hits'] * 0.001,  # 估算節省
                'total_cost': self.usage_stats['estimated_cost']
            }
        }
    
    def clear_cache(self) -> bool:
        """清除快取"""
        return self.cache_manager.clear_pattern("cache:gemini*")
    
    def reset_stats(self):
        """重置統計"""
        self.usage_stats = {
            'total_requests': 0,
            'cache_hits': 0,
            'total_tokens': 0,
            'estimated_cost': 0.0
        }

# 成本優化裝飾器
def optimize_gemini_call(cache: bool = True, max_tokens: int = 1000):
    """Gemini API 呼叫優化裝飾器"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # 獲取 Gemini 客戶端
            client = getattr(wrapper, '_gemini_client', None)
            if not client:
                client = OptimizedGeminiClient()
                wrapper._gemini_client = client
            
            # 提取提示詞參數
            prompt = None
            if 'prompt' in kwargs:
                prompt = kwargs['prompt']
            elif args:
                prompt = args[0]
            
            if prompt:
                # 使用優化客戶端
                result = client.generate_response(prompt, max_tokens=max_tokens, use_cache=cache)
                return result['response']
            else:
                # 回退到原始函數
                return func(*args, **kwargs)
        
        return wrapper
    return decorator

# 全域優化客戶端實例
optimized_client = OptimizedGeminiClient()

# 使用範例
if __name__ == "__main__":
    print("🧪 測試優化 Gemini API 客戶端...")
    
    # 測試基本功能
    test_prompts = [
        "請簡短說明失智症的早期症狀",
        "什麼是記憶力減退？",
        "如何照顧失智症患者？"
    ]
    
    for prompt in test_prompts:
        print(f"\n📝 測試提示詞: {prompt[:50]}...")
        result = optimized_client.generate_response(prompt)
        print(f"✅ 回應: {result['response'][:100]}...")
        print(f"📊 Tokens: {result['tokens_used']}, 成本: ${result['cost']:.6f}")
    
    # 顯示統計
    stats = optimized_client.get_usage_stats()
    print(f"\n📈 使用統計: {stats}") 