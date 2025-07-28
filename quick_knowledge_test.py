#!/usr/bin/env python3
from pinecone import Pinecone
import hashlib, random

# 初始化 Pinecone
pc = Pinecone(api_key="pcsk_4WvWXx_G5bRUFdFNzLzRHNM9rkvFMvC18TMRTaeYXVCxmWSPQLmKr4xAs4UaZg5NvVb69m")
index = pc.Index("dementia-care-knowledge")

def create_embedding(text, dimension=1024):
    text_hash = hashlib.md5(text.encode()).hexdigest()
    vector = []
    for i in range(dimension):
        seed = int(text_hash[i % len(text_hash)], 16) + i
        random.seed(seed)
        vector.append(random.uniform(-1, 1))
    mag = sum(x*x for x in vector) ** 0.5
    return [x/mag for x in vector] if mag > 0 else [1.0/dimension] * dimension

def upload_samples():
    samples = [
        {"id":"quick-001","title":"失智症早期症狀識別","content":"失智症早期症狀包括記憶力減退、判斷力下降、語言表達困難等。","type":"early_symptoms"},
        {"id":"quick-002","title":"BPSD行為心理症狀管理","content":"BPSD包括妄想、幻覺、激動、焦慮等，需要非藥物與藥物干預。","type":"bpsd_management"},
        {"id":"quick-003","title":"家庭照護安全指南","content":"家庭照護要防跌倒、防走失、用藥安全，並優化居住環境。","type":"safety_guide"},
    ]
    vectors = []
    for item in samples:
        emb = create_embedding(item["title"] + " " + item["content"])
        vectors.append({
            "id": item["id"],
            "values": emb,
            "metadata": {"title": item["title"], "type": item["type"]}
        })
        print(f"✅ 準備: {item['title']}")
    resp = index.upsert(vectors=vectors)
    print(f"🎉 成功上傳 {resp.upserted_count} 個向量")

def check_status():
    stats = index.describe_index_stats()
    print(f"📊 總向量: {stats.total_vector_count}, 維度: {stats.dimension}")

def test_query():
    print("🔍 測試搜尋: '失智症症狀'")
    qv = create_embedding("失智症症狀")
    res = index.query(vector=qv, top_k=3, include_metadata=True)
    for i, m in enumerate(res.matches, 1):
        print(f"  {i}. {m.metadata['title']} (score: {m.score:.3f})")

if __name__ == "__main__":
    print("🚀 Quick Knowledge Test")
    check_status()
    upload_samples()
    print()
    check_status()
    print()
    test_query()
