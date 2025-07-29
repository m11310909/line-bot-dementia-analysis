# main.py
from fastapi import FastAPI
import logging
import google.generativeai as genai
import os

# configure logging if you need
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ─── Single FastAPI instance ────────────────────────────────────────
app = FastAPI(title="XAI Flex Message API", version="1.0.0")

# ─── Include routers ───────────────────────────────────────────────
from routers.base    import router as base_router
from routers.analyze import router as analyze_router
from routers.flex    import router as flex_router

app.include_router(base_router)
app.include_router(analyze_router)
app.include_router(flex_router)

# ─── (Optional) configure your Gemini client here ───────────────────
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# ─── If you have other endpoints (e.g. /callback), import & include them too
# from routers.callback import router as callback_router
# app.include_router(callback_router)

# ─── Run ────────────────────────────────────────────────────────────
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
