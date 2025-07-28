print("🚀 FastAPI 快速測試")
from fastapi import FastAPI
import uvicorn

app = FastAPI()

@app.get("/")
def root():
    return {"status": "working", "message": "FastAPI is ready!"}

if __name__ == "__main__":
    print("✅ 啟動測試服務...")
    uvicorn.run(app, host="0.0.0.0", port=8888)
