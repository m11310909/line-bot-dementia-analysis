print("🚀 開始超級簡單測試...")

try:
    from fastapi import FastAPI
    print("✅ FastAPI 可用")
except ImportError as e:
    print(f"❌ FastAPI 不可用: {e}")
    exit(1)

try:
    import uvicorn
    print("✅ uvicorn 可用")
except ImportError as e:
    print(f"❌ uvicorn 不可用: {e}")
    exit(1)

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello World", "status": "working"}

@app.get("/test")
def test():
    return {"test": "success", "rag": "coming soon"}

if __name__ == "__main__":
    print("🚀 啟動超級簡單 API...")
    print("📍 URL: http://localhost:8888")
    
    try:
        uvicorn.run(app, host="0.0.0.0", port=8888)
    except Exception as e:
        print(f"❌ 啟動失敗: {e}")
