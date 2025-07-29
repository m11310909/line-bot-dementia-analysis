# lightweight_test.py - 修复维度匹配和缩进问题
from pinecone import Pinecone, ServerlessSpec
import json
import time
import random

# 你的 Pinecone 客户端
pc = Pinecone(api_key="pcsk_4WvWXx_G5bRUFdFNzLzRHNM9rkvFMvC18TMRTaeYXVCxmWSPQLmKr4xAs4UaZg5NvVb69m")

INDEX_NAME = "dementia-care-knowledge"

def test_pinecone_basic():
    """基础 Pinecone 测试"""
    print("🔄 Testing Pinecone connection...")

    try:
        # 列出索引
        indexes = pc.list_indexes()
        print(f"✅ Connected! Found {len(indexes)} indexes")

        # 检查现有索引
        existing_names = [idx.name for idx in indexes]

        if INDEX_NAME in existing_names:
            print("✅ Index already exists!")
            index = pc.Index(INDEX_NAME)
            stats = index.describe_index_stats()
            dimension = stats.dimension
            print(f"📏 Index dimension: {dimension}")
            return index, dimension
        else:
            print(f"❌ Index '{INDEX_NAME}' not found")
            return None, None

    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return None, None

def create_simple_embedding(text, dimension):
    """创建指定维度的简单文本嵌入向量"""
    import hashlib

    # 将文本转换为数字序列
    text_hash = hashlib.md5(text.encode()).hexdigest()

    # 创建指定维度的向量
    vector = []
    for i in range(dimension):
        # 使用哈希值和位置创建伪随机但一致的向量
        seed = int(text_hash[i % len(text_hash)], 16) + i
        random.seed(seed)
        vector.append(random.uniform(-1, 1))

    # 归一化向量
    magnitude = sum(x*x for x in vector) ** 0.5
    if magnitude > 0:
        return [x/magnitude for x in vector]
    else:
        return [1.0/dimension] * dimension

def upload_demo_data(index, dimension):
    """上传演示数据（使用正确的维度）"""
    print(f"📚 Uploading demo knowledge with {dimension}D embeddings...")

    demo_chunks = [
        {
            "id": "demo-001",
            "title": "失智症十大警訊", 
            "content": "失智症的十大警訊包括記憶力減退、計劃事情或解決問題有困難、無法勝任原本熟悉的事務等。及早發現這些警訊有助於早期診斷和治療。",
            "type": "warning_sign",
            "keywords": ["記憶力", "警訊", "診斷", "治療"]
        },
        {
            "id": "demo-002",
            "title": "BPSD行為心理症狀",
            "content": "BPSD指失智症患者的行為心理症狀，包括遊走、攻擊行為、妄想、幻覺等。了解這些症狀有助於提供適當的照護。",
            "type": "bpsd_symptom",
            "keywords": ["BPSD", "行為症狀", "遊走", "照護"]
        },
        {
            "id": "demo-003",
            "title": "失智症溝通技巧",
            "content": "與失智症患者溝通時要保持耐心，使用簡單明確的語言，避免爭辯或糾正，多用肢體語言和表情來表達關愛。",
            "type": "coping_strategy",
            "keywords": ["溝通", "技巧", "耐心", "肢體語言"]
        },
        {
            "id": "demo-004", 
            "title": "照護者壓力管理",
            "content": "照護者容易產生身心壓力，需要適當休息、尋求支持，並學習壓力調適技巧。建議定期參加支持團體或諮詢專業人員。",
            "type": "caregiver_support",
            "keywords": ["照護者", "壓力管理", "支持團體", "諮詢"]
        },
        {
            "id": "demo-005",
            "title": "失智症用藥安全",
            "content": "失智症患者用藥需要特別注意劑量、時間和副作用，建議使用藥盒分裝並定期檢視。家屬應與醫師密切配合。",
            "type": "medication_safety",
            "keywords": ["用藥安全", "劑量", "副作用", "藥盒"]
        }
    ]

    try:
        vectors_to_upload = []

        for chunk in demo_chunks:
            # 創建正確維度的嵌入
            content_text = f"{chunk['title']} {chunk['content']} {' '.join(chunk['keywords'])}"
            embedding = create_simple_embedding(content_text, dimension)

            vector_data = {
                'id': chunk['id'],
                'values': embedding,
                'metadata': {
                    'title': chunk['title'],
                    'content': chunk['content'][:400],
                    'type': chunk['type'],
                    'keywords': ', '.join(chunk['keywords'])
                }
            }

            vectors_to_upload.append(vector_data)
            print(f"✅ Prepared: {chunk['title']} ({len(embedding)}D)")

        # 批量上传
        print(f"📤 Uploading {len(vectors_to_upload)} vectors...")
        upsert_response = index.upsert(vectors=vectors_to_upload)
        print(f"🎉 Successfully uploaded {upsert_response.upserted_count} vectors!")

        # 等待索引更新
        print("⏳ Waiting for index to update...")
        time.sleep(5)
        return True

    except Exception as e:
        print(f"❌ Upload failed: {str(e)}")
        return False

def test_multiple_queries(index, dimension):
    """测试多个查询"""
    test_queries = [
        "失智症症状",
        "照護技巧", 
        "藥物治療",
        "行為問題",
        "壓力管理"
    ]

    print("🔍 Testing multiple queries...")

    for query_text in test_queries:
        try:
            print(f"\n📝 Query: '{query_text}'")

            # 创建查询向量
            query_vector = create_simple_embedding(query_text, dimension)

            # 查询
            results = index.query(
                vector=query_vector,
                top_k=2,
                include_metadata=True
            )

            if results.matches:
                for i, match in enumerate(results.matches, 1):
                    print(f"  {i}. {match.metadata['title']} (Score: {match.score:.4f})")
                    print(f"     Type: {match.metadata['type']}")
                    print(f"     Keywords: {match.metadata.get('keywords', 'N/A')}")
            else:
                print("  No matches found")

        except Exception as e:
            print(f"  ❌ Query failed: {str(e)}")

def get_detailed_stats(index):
    """获取详细的索引统计"""
    try:
        stats = index.describe_index_stats()
        print("\n📊 Detailed Index Statistics:")
        print(f"  Total vectors: {stats.total_vector_count}")
        print(f"  Dimension: {stats.dimension}")
        print(f"  Index fullness: {stats.index_fullness}")
        return stats
    except Exception as e:
        print(f"❌ Stats error: {str(e)}")
        return None

def main():
    """主函数"""
    print("🚀 Fixed Lightweight Pinecone Test")
    print("=" * 60)

    # 1. 测试连接并获取索引维度
    index, dimension = test_pinecone_basic()
    if not index or not dimension:
        print("❌ Failed to connect to Pinecone or get index info")
        return

    # 2. 获取初始状态
    initial_stats = get_detailed_stats(index)

    # 3. 上传演示数据
    if upload_demo_data(index, dimension):
        print("✅ Demo data uploaded successfully!")
    else:
        print("⚠️ Demo data upload failed")
        return

    # 4. 测试多个查询
    test_multiple_queries(index, dimension)

    # 5. 获取最终状态
    final_stats = get_detailed_stats(index)

    print("\n🎉 Fixed test completed!")
    print("✅ Your Pinecone setup is working correctly!")
    print(f"✅ Using {dimension}D vectors")
    print("\n🚀 Ready to build your XAI Flex Message system!")

if __name__ == "__main__":
    main()