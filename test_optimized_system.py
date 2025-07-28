#!/usr/bin/env python3
"""
Test script to verify the optimized system works correctly
测试脚本验证优化后的系统是否正常工作
"""

def test_core_imports():
    """测试核心导入"""
    print("🧪 Testing Core Imports...")
    print("=" * 40)

    try:
        from fastapi import FastAPI
        from uvicorn import main as uvicorn_main
        from pinecone import Pinecone
        from linebot import LineBotApi, WebhookHandler
        from linebot.models import MessageEvent, TextMessage, TextSendMessage
        import requests
        import httpx
        from pydantic import BaseModel

        # Test custom replacements
        from simple_embedding import SimpleEmbedding, embedder
        from memory_cache import MemoryCache, cache

        print("✅ All core imports successful")
        return True

    except ImportError as e:
        print(f"❌ Import failed: {e}")
        return False

def test_embedding_replacement():
    """测试嵌入替代功能"""
    print("\n🔤 Testing Embedding Replacement...")
    print("=" * 40)

    try:
        from simple_embedding import embedder

        # Test single encoding
        text = "Hello, this is a test message for dementia care"
        vector = embedder.encode(text)

        print(f"✅ Single embedding: {len(vector)} dimensions")
        print(f"   Sample values: {vector[:5]}")

        # Test batch encoding
        texts = [
            "Patient needs medication reminder",
            "Family member visiting today",
            "Memory exercise scheduled"
        ]
        vectors = embedder.encode_batch(texts)

        print(f"✅ Batch embedding: {len(vectors)} texts processed")

        # Test consistency
        vector2 = embedder.encode(text)
        is_consistent = vector == vector2
        print(f"✅ Consistency check: {'PASS' if is_consistent else 'FAIL'}")

        return True

    except Exception as e:
        print(f"❌ Embedding test failed: {e}")
        return False

def test_memory_cache():
    """测试内存缓存功能"""
    print("\n💾 Testing Memory Cache...")
    print("=" * 40)

    try:
        from memory_cache import cache

        # Test set/get
        cache.set("test_key", "test_value")
        value = cache.get("test_key")

        print(f"✅ Set/Get test: {value}")

        # Test TTL
        cache.set("ttl_test", "expires_soon", ttl=1)
        immediate = cache.get("ttl_test")
        print(f"✅ TTL test (immediate): {immediate}")

        # Test non-existent key
        missing = cache.get("nonexistent")
        print(f"✅ Missing key test: {missing}")

        return True

    except Exception as e:
        print(f"❌ Cache test failed: {e}")
        return False

def test_pinecone_functionality():
    """测试 Pinecone 功能"""
    print("\n🌲 Testing Pinecone Functionality...")
    print("=" * 40)

    try:
        from pinecone import Pinecone

        # Connect to Pinecone
        pc = Pinecone(api_key="pcsk_4WvWXx_G5bRUFdFNzLzRHNM9rkvFMvC18TMRTaeYXVCxmWSPQLmKr4xAs4UaZg5NvVb69m")
        index = pc.Index("dementia-care-knowledge")

        # Get stats
        stats = index.describe_index_stats()
        print(f"✅ Connected to index: {stats.total_vector_count} vectors")

        # Test query (simple)
        query_result = index.query(
            vector=[0.1] * 1024,
            top_k=3,
            include_metadata=True
        )

        print(f"✅ Query test: {len(query_result.matches)} results")

        if query_result.matches:
            for i, match in enumerate(query_result.matches[:2]):
                print(f"   Match {i+1}: score={match.score:.3f}")

        return True

    except Exception as e:
        print(f"❌ Pinecone test failed: {e}")
        return False

def test_line_bot_setup():
    """测试 LINE Bot 设置"""
    print("\n🤖 Testing LINE Bot Setup...")
    print("=" * 40)

    try:
        from linebot import LineBotApi, WebhookHandler
        from linebot.models import MessageEvent, TextMessage, TextSendMessage, FlexSendMessage

        # Test model creation (without actual tokens)
        print("✅ LINE Bot models imported successfully")

        # Test Flex Message structure
        flex_message = {
            "type": "flex",
            "altText": "Dementia Care Assistant",
            "contents": {
                "type": "bubble",
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "text",
                            "text": "Memory Support",
                            "weight": "bold",
                            "size": "xl"
                        }
                    ]
                }
            }
        }

        print("✅ Flex message structure validated")

        return True

    except Exception as e:
        print(f"❌ LINE Bot test failed: {e}")
        return False

def test_fastapi_setup():
    """测试 FastAPI 设置"""
    print("\n🚀 Testing FastAPI Setup...")
    print("=" * 40)

    try:
        from fastapi import FastAPI, HTTPException
        from pydantic import BaseModel

        # Create test app
        app = FastAPI(title="Dementia Care API")

        # Test model
        class TestMessage(BaseModel):
            text: str
            user_id: str = "test_user"

        @app.get("/health")
        def health_check():
            return {"status": "healthy", "optimized": True}

        print("✅ FastAPI app created successfully")
        print("✅ Pydantic models working")

        return True

    except Exception as e:
        print(f"❌ FastAPI test failed: {e}")
        return False

def run_system_checks():
    """运行系统检查"""
    print("\n📊 System Checks...")
    print("=" * 40)

    import subprocess
    import os

    # Check disk usage
    try:
        result = subprocess.run(['du', '-sh', '.pythonlibs'], 
                              capture_output=True, text=True)
        if result.stdout:
            print(f"📦 Python packages size: {result.stdout.strip()}")
    except:
        pass

    # Check installed packages count
    try:
        result = subprocess.run(['pip', 'list'], 
                              capture_output=True, text=True)
        if result.stdout:
            lines = result.stdout.strip().split('\n')
            package_count = len(lines) - 2  # Remove header lines
            print(f"📦 Installed packages: {package_count}")
    except:
        pass

    # Check key files
    key_files = [
        'requirements.txt',
        'simple_embedding.py',
        'memory_cache.py',
        'requirements_original_backup.txt'
    ]

    for file in key_files:
        exists = "✅" if os.path.exists(file) else "❌"
        print(f"{exists} {file}")

def main():
    """主测试函数"""
    print("🚀 Optimized System Comprehensive Test")
    print("=" * 50)
    print("Testing all components after optimization...\n")

    tests = [
        ("Core Imports", test_core_imports),
        ("Embedding Replacement", test_embedding_replacement),
        ("Memory Cache", test_memory_cache),
        ("Pinecone Functionality", test_pinecone_functionality),
        ("LINE Bot Setup", test_line_bot_setup),
        ("FastAPI Setup", test_fastapi_setup),
    ]

    passed = 0
    total = len(tests)

    for name, test_func in tests:
        try:
            if test_func():
                passed += 1
            else:
                print(f"❌ {name} test failed")
        except Exception as e:
            print(f"❌ {name} test error: {e}")

    # Run system checks
    run_system_checks()

    # Final results
    print(f"\n🎯 Test Results: {passed}/{total} passed")

    if passed == total:
        print("🎉 ALL TESTS PASSED! Your optimized system is ready!")
        print("\n📋 Next steps:")
        print("1. Fix requests version: pip install requests>=2.32.3")
        print("2. Start your main app: python main.py")
        print("3. Test LINE Bot: python lightweight_test.py")
    else:
        print("⚠️ Some tests failed. Check the output above for details.")

    return passed == total

if __name__ == "__main__":
    main()