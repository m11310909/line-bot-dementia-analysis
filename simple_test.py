from fastapi import FastAPI
import uvicorn
import os

app = FastAPI()

@app.get("/")
def read_root():
    return {
        "message": "LINE Bot 失智症分析系統 - 簡化版",
        "status": "運行中",
        "secrets_check": {
            "LINE_TOKEN": "已設定" if os.getenv('LINE_CHANNEL_ACCESS_TOKEN') else "未設定",
            "LINE_SECRET": "已設定" if os.getenv('LINE_CHANNEL_SECRET') else "未設定",
            "GEMINI_KEY": "已設定" if os.getenv('AISTUDIO_API_KEY') else "未設定"
        }
    }

@app.get("/health")
def health():
    return {"status": "healthy", "port": 8000}

@app.get("/test")
def test():
    return {"test": "成功", "environment": "Replit"}

if __name__ == "__main__":
    print("🚀 啟動簡化測試服務器...")
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
