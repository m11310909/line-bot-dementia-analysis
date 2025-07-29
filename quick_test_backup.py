# quick_test.py - 快速测试 Pinecone 连接和功能
from pinecone import Pinecone, ServerlessSpec
import json
import time

# 初始化 Pinecone 客户端
pc = Pinecone(api_key="pcsk_4WvWXx_G5bRUFdFNzLzRHNM9rkvFMvC18TMRTaeYXVCxmWSPQLmKr4xAs4UaZg5NvVb69m")

# 索引配置
INDEX_NAME = "dementia-care-knowledge"
DIMENSION = 384  # all-MiniLM-L6-v2 模型的维度

def test_pinecone_connection():
    """测试 Pinecone 连接"""
    print("🔄 Testing Pinecone connection...")

    try:
        # 列出现有索引
        indexes = pc.list_indexes()
        print(f"✅ Connected to Pinecone! Found {len(indexes)} indexes.")

        for idx in indexes:
            print(f"  - Index: {idx.name}")

        return True
    except Exception as e:
        print(f"❌ Connection failed: {str(e)}")
        return False

def create_index_if_not_exists():
    """创建索引（如果不存在）"""
    print(f"🔄 Checking if index '{INDEX_NAME}' exists...")

    try:
        existing_indexes = [idx.name for idx in pc.list_indexes()]

        if INDEX_NAME not in existing_indexes:
            print(f"📝 Creating new index: {INDEX_NAME}")

            pc.create_index(
                name=INDEX_NAME,
                dimension=DIMENSION,
                metric="cosine",
                spec=ServerlessSpec(
                    cloud="aws", 
                    region="us-east-1"
                )
            )

            print("⏳ Waiting for index to be ready...")
            time.sleep(10)  # 等待索引初始化

            print("✅ Index created successfully!")
        else:
            print("✅ Index already exists!")

        return pc.Index(INDEX_NAME)

    except Exception as e:
        print(f"❌ Failed to create index: {str(e)}")
        return None

def test_basic_operations(index):
    """测试基本的向量操作"""
    print("🧪 Testing basic vector operations...")

    try:
        # 测试向量数据
        test_vectors = [
            {
                'id': 'test-001',
                'values': [0.1] * DIMENSION,  # 简单的测试向量
                'metadata': {
                    'title': '测试向量1',
                    'content': '这是一个测试向量',
                    'type': 'test'
                }
            },
            {
                'id': 'test-002', 
                'values': [0.2] * DIMENSION,
                'metadata': {
                    'title': '测试向量2',
                    'content': '这是另一个测试向量',
                    'type': 'test'
                }
            }
        ]

        # 1. 上传向量
        print("📤 Uploading test vectors...")
        upsert_response = index.upsert(vectors=test_vectors)
        print(f"✅ Uploaded {upsert_response.upserted_count} vectors")

        # 等待更新
        time.sleep(2)

        # 2. 查询向量
        print("🔍 Querying vectors...")
        query_response = index.query(
            vector=[0.15] * DIMENSION,  # 查询向量
            top_k=2,
            include_metadata=True
        )

        print(f"✅ Found {len(query_response.matches)} similar vectors:")
        for match in query_response.matches:
            print(f"  - ID: {match.id}, Score: {match.score:.4f}")
            print(f"    Title: {match.metadata.get('title', 'N/A')}")

        # 3. 获取索引统计
        print("📊 Getting index statistics...")
        stats = index.describe_index_stats()
        print(f"✅ Index contains {stats.total_vector_count} vectors")

        # 4. 清理测试数据
        print("🧹 Cleaning up test data...")
        index.delete(ids=['test-001', 'test-002'])
        print("✅ Test data cleaned up")

        return True

    except Exception as e:
        print(f"❌ Test operations failed: {str(e)}")
        return False

def upload_demo_knowledge(index):
    """上传演示知识数据"""
    print("📚 Uploading demo knowledge...")

    # 需要先安装 sentence-transformers
    try:
        from sentence_transformers import SentenceTransformer
        model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
        print("✅ Embedding model loaded")
    except ImportError:
        print("❌ sentence-transformers not installed. Run: pip install sentence-transformers")
        return False
    except Exception as e:
        print(f"❌ Failed to load model: {str(e)}")
        return False

    # 演示知识数据
    demo_chunks = [
        {
            "chunk_id": "demo-001",
            "title": "失智症十大警訊",
            "content": "失智症的十大警訊包括記憶力減退、計劃事情或解決問題有困難、無法勝任原本熟悉的事務等。及早發現這些警訊有助於早期診斷和治療。",
            "chunk_type": "warning_sign",
            "keywords": ["失智症", "警訊", "記憶力", "診斷"]
        },
        {
            "chunk_id": "demo-002", 
            "title": "BPSD行為心理症狀",
            "content": "BPSD指失智症患者的行為心理症狀，包括遊走、攻擊行為、妄想、幻覺等。了解這些症狀有助於提供適當的照護。",
            "chunk_type": "bpsd_symptom",
            "keywords": ["BPSD", "行為症狀", "遊走", "照護"]
        },
        {
            "chunk_id": "demo-003",
            "title": "失智症溝通技巧", 
            "content": "與失智症患者溝通時要保持耐心，使用簡單明確的語言，避免爭辯或糾正，多用肢體語言和表情來表達關愛。",
            "chunk_type": "coping_strategy",
            "keywords": ["溝通", "技巧", "耐心", "肢體語言"]
        }
    ]

    try:
        vectors_to_upload = []

        for chunk in demo_chunks:
            # 生成嵌入向量
            content = f"{chunk['title']} {chunk['content']} {' '.join(chunk['keywords'])}"
            embedding = model.encode(content).tolist()

            # 准备向量数据
            vector_data = {
                'id': chunk['chunk_id'],
                'values': embedding,
                'metadata': {
                    'title': chunk['title'],
                    'content': chunk['content'][:500],  # 限制长度
                    'chunk_type': chunk['chunk_type'],
                    'keywords': json.dumps(chunk['keywords'])
                }
            }

            vectors_to_upload.append(vector_data)
            print(f"✅ Prepared: {chunk['chunk_id']}")

        # 批量上传
        upsert_response = index.upsert(vectors=vectors_to_upload)
        print(f"🎉 Successfully uploaded {upsert_response.upserted_count} demo vectors!")

        # 等待索引更新
        time.sleep(3)

        # 测试查询
        print("🔍 Testing demo query...")
        test_query = "失智症的症状有哪些？"
        query_embedding = model.encode(test_query).tolist()

        results = index.query(
            vector=query_embedding,
            top_k=3,
            include_metadata=True
        )

        print(f"✅ Query results for '{test_query}':")
        for i, match in enumerate(results.matches, 1):
            print(f"  {i}. {match.metadata['title']} (Score: {match.score:.4f})")
            print(f"     {match.metadata['content'][:100]}...")

        return True

    except Exception as e:
        print(f"❌ Failed to upload demo knowledge: {str(e)}")
        return False

def main():
    """主测试函数"""
    print("🚀 Starting Pinecone Quick Test")
    print("=" * 50)

    # 1. 测试连接
    if not test_pinecone_connection():
        return

    # 2. 创建索引
    index = create_index_if_not_exists()
    if not index:
        return

    # 3. 测试基本操作
    if not test_basic_operations(index):
        return

    # 4. 上传演示知识
    if not upload_demo_knowledge(index):
        print("⚠️ Demo knowledge upload failed, but basic operations work")

    print("\n🎉 All tests completed successfully!")
    print(f"✅ Your Pinecone index '{INDEX_NAME}' is ready to use!")
    print("\nNext steps:")
    print("1. Install dependencies: pip install sentence-transformers fastapi line-bot-sdk")
    print("2. Set up your LINE Bot credentials")
    print("3. Run the main application: python main.py")

if __name__ == "__main__":
    main()

---

# requirements_minimal.txt - 最小依赖版本
pinecone-client==3.0.0
sentence-transformers==2.2.2
fastapi==0.104.1
uvicorn==0.24.0
line-bot-sdk==3.8.0
pydantic==2.5.0
python-multipart==0.0.6

---

# replit_secrets_setup.md
# 在 Replit 中设置这些 Secrets:

PINECONE_API_KEY=pcsk_4WvWXx_G5bRUFdFNzLzRHNM9rkvFMvC18TMRTaeYXVCxmWSPQLmKr4xAs4UaZg5NvVb69m
PINECONE_INDEX_NAME=dementia-care-knowledge
LINE_CHANNEL_ACCESS_TOKEN=your_line_token_here
LINE_CHANNEL_SECRET=your_line_secret_here

# 快速部署命令:
# 1. 运行测试: python quick_test.py
# 2. 如果测试通过，安装完整依赖: pip install -r requirements_minimal.txt  
# 3. 运行主应用: python main.py

---

# simple_main.py - 简化版主应用（用于快速测试）
from fastapi import FastAPI
from pinecone import Pinecone
import json

app = FastAPI()

# 初始化 Pinecone
pc = Pinecone(api_key="pcsk_4WvWXx_G5bRUFdFNzLzRHNM9rkvFMvC18TMRTaeYXVCxmWSPQLmKr4xAs4UaZg5NvVb69m")
index = pc.Index("dementia-care-knowledge")

@app.get("/")
async def root():
    """根路径 - 显示状态"""
    try:
        stats = index.describe_index_stats()
        return {
            "message": "🎉 XAI Dementia Care Bot is running!",
            "status": "healthy",
            "pinecone_vectors": stats.total_vector_count,
            "index_name": "dementia-care-knowledge"
        }
    except Exception as e:
        return {
            "message": "⚠️ Service running but Pinecone connection issues",
            "error": str(e)
        }

@app.get("/test-query")
async def test_query(q: str = "失智症症状"):
    """测试查询功能"""
    try:
        # 简单的文本查询（不使用嵌入模型）
        # 在实际应用中会使用 sentence-transformers

        # 模拟查询结果
        return {
            "query": q,
            "message": "✅ Query endpoint working",
            "note": "Install sentence-transformers for full functionality"
        }
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

---

# 完整部署检查清单:

# ✅ 第一步: 测试 Pinecone 连接
# python quick_test.py

# ✅ 第二步: 安装必要依赖  
# pip install sentence-transformers fastapi uvicorn line-bot-sdk

# ✅ 第三步: 测试简化应用
# python simple_main.py

# ✅ 第四步: 设置 LINE Bot credentials
# 在 Replit Secrets 中添加 LINE_CHANNEL_ACCESS_TOKEN 和 LINE_CHANNEL_SECRET

# ✅ 第五步: 运行完整应用
# python main.py (使用之前提供的完整代码)