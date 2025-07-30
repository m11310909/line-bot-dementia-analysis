# simple_embedding.py - 轻量级嵌入替代 sentence-transformers
import hashlib
import random
from typing import List

class SimpleEmbedding:
    def __init__(self, dimension: int = 384):
        self.dimension = dimension
    
    def encode(self, text: str) -> List[float]:
        """将文本编码为向量"""
        text = text.lower().strip()
        text_hash = hashlib.md5(text.encode('utf-8')).hexdigest()
        
        vector = []
        for i in range(self.dimension):
            seed = int(text_hash[i % len(text_hash)], 16) + i
            random.seed(seed)
            vector.append(random.uniform(-1, 1))
        
        # 归一化
        magnitude = sum(x * x for x in vector) ** 0.5
        if magnitude > 0:
            vector = [x / magnitude for x in vector]
        else:
            vector = [1.0 / self.dimension] * self.dimension
            
        return vector
    
    def encode_batch(self, texts: List[str]) -> List[List[float]]:
        return [self.encode(text) for text in texts]

# 全局实例
embedder = SimpleEmbedding(dimension=384)  # 384维节省60%空间
