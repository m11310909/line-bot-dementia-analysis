#!/usr/bin/env python3
# verify_installation.py - 验证优化后的安装

def verify_packages():
    """验证关键包是否正确安装"""
    tests = {
        "FastAPI": "from fastapi import FastAPI",
        "Uvicorn": "import uvicorn",
        "Pinecone": "from pinecone import Pinecone",
        "LINE Bot": "from linebot import LineBotApi",
        "Pydantic": "from pydantic import BaseModel",
        "Requests": "import requests",
        "HTTPX": "import httpx",
        "Simple Embedding": "from simple_embedding import SimpleEmbedding",
        "Memory Cache": "from memory_cache import MemoryCache"
    }
    
    print("🧪 验证包安装状态:")
    print("=" * 40)
    
    passed = 0
    for name, import_stmt in tests.items():
        try:
            exec(import_stmt)
            print(f"✅ {name}: OK")
            passed += 1
        except ImportError as e:
            print(f"❌ {name}: FAILED - {str(e)}")
    
    print(f"\n📊 结果: {passed}/{len(tests)} 通过")
    return passed == len(tests)

def check_space_usage():
    """检查空间使用情况"""
    import subprocess
    
    print("\n💾 空间使用情况:")
    print("=" * 40)
    
    try:
        # 检查包大小
        result = subprocess.run(['du', '-sh', '.pythonlibs'], 
                              capture_output=True, text=True)
        if result.stdout:
            print(f"📦 Python packages: {result.stdout.strip()}")
        
        # 检查总空间
        result = subprocess.run(['df', '-h', '.'], 
                              capture_output=True, text=True)
        if result.stdout:
            lines = result.stdout.strip().split('\n')
            if len(lines) > 1:
                print(f"💽 Total disk usage: {lines[1]}")
    
    except Exception as e:
        print(f"⚠️ Could not check space: {str(e)}")

def test_pinecone_connection():
    """测试 Pinecone 连接"""
    print("\n🔌 测试 Pinecone 连接:")
    print("=" * 40)
    
    try:
        from pinecone import Pinecone
        pc = Pinecone(api_key="pcsk_4WvWXx_G5bRUFdFNzLzRHNM9rkvFMvC18TMRTaeYXVCxmWSPQLmKr4xAs4UaZg5NvVb69m")
        index = pc.Index("dementia-care-knowledge")
        stats = index.describe_index_stats()
        
        print(f"✅ Pinecone connected!")
        print(f"📊 Index vectors: {stats.total_vector_count}")
        print(f"📏 Dimension: {stats.dimension}")
        
        return True
    except Exception as e:
        print(f"❌ Pinecone connection failed: {str(e)}")
        return False

if __name__ == "__main__":
    print("🚀 验证优化后的安装")
    print("=" * 50)
    
    # 验证包
    packages_ok = verify_packages()
    
    # 检查空间
    check_space_usage()
    
    # 测试 Pinecone
    pinecone_ok = test_pinecone_connection()
    
    print(f"\n🎯 总体状态:")
    if packages_ok and pinecone_ok:
        print("✅ 优化成功! 系统可以正常运行")
    else:
        print("⚠️ 部分问题需要解决")
