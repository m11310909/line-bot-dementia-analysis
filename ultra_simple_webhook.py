from fastapi import FastAPI, Request
from fastapi.responses import PlainTextResponse
import uvicorn

app = FastAPI()


@app.get("/")
def root():
    return {"status": "ok", "service": "webhook_ready"}


@app.get("/webhook")
def webhook_get():
    return {"status": "webhook_endpoint_ready"}


@app.post("/webhook")
async def webhook_post(request: Request):
    print("📨 Webhook received!")
    try:
        body = await request.body()
        print(f"Body: {body.decode('utf-8')}")
        return {"status": "ok"}
    except Exception as e:
        print(f"Error: {e}")
        return {"status": "ok"}


if __name__ == "__main__":
    print("🚀 Ultra Simple Webhook")
    uvicorn.run(app, host="0.0.0.0", port=8001)
