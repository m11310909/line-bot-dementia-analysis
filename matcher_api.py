from fastapi import FastAPI, Request
from pydantic import BaseModel
import google.generativeai as genai
import os
import json

# ─── Initialize FastAPI (only once!) ──────────────────────────────
app = FastAPI()

# ─── LINE webhook healthcheck endpoint ────────────────────────────
@app.post("/callback")
async def callback(request: Request):
    # we don’t care about the body here—just reply 200 OK so LINE’s Verify passes
    return "OK"

# ─── Configure Gemini client ───────────────────────────────────────
# Make sure GOOGLE_API_KEY is set in your env/Replit secrets
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# ─── Shared definitions ────────────────────────────────────────────
class MatchRequest(BaseModel):
    user_input: str

FALLBACK = {
    "matched_warning_code": "UNKNOWN",
    "message": "系統忙碌或無法理解輸入內容，請稍後再試"
}

def load_prompt(filename: str) -> str:
    path = os.path.join("prompts", filename)
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def gpt_call(system_prompt: str, user_msg: str):
    try:
        resp = genai.chat.completions.create(
            model="models/chat-bison-001",  # or your chosen Gemini model
            messages=[
                {"author": "system", "content": system_prompt},
                {"author": "user",   "content": user_msg}
            ],
            temperature=0.3,
        )
        return json.loads(resp.choices[0].message.content)
    except Exception:
        return FALLBACK

# ─── Match endpoints ───────────────────────────────────────────────
@app.post("/m1-match")
async def m1(request: MatchRequest):
    return gpt_call(load_prompt("prompt_m1.txt"), request.user_input)

@app.post("/m2-match")
async def m2(request: MatchRequest):
    return gpt_call(load_prompt("prompt_m2.txt"), request.user_input)

@app.post("/m3-match")
async def m3(request: MatchRequest):
    return gpt_call(load_prompt("prompt_m3.txt"), request.user_input)

@app.post("/m4-match")
async def m4(request: MatchRequest):
    return gpt_call(load_prompt("prompt_m4.txt"), request.user_input)

# ─── Health-check ─────────────────────────────────────────────────
@app.get("/")
def ping():
    return {"status": "ok"}
