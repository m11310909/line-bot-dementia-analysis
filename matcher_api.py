from fastapi import FastAPI
from pydantic import BaseModel
import google.generativeai as genai
import os
import json

# 1️⃣ Initialize FastAPI
app = FastAPI()

# 2️⃣ Configure Gemini client
#    Make sure you have set GOOGLE_API_KEY in your environment (or Replit secrets).
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

class MatchRequest(BaseModel):
    user_input: str

# 3️⃣ Fallback in case of errors
FALLBACK = {
    "matched_warning_code": "UNKNOWN",
    "message": "系統忙碌或無法理解輸入內容，請稍後再試"
}

# 4️⃣ Helper to load your prompts
def load_prompt(filename: str) -> str:
    path = os.path.join("prompts", filename)
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

# 5️⃣ Wrapper around Gemini chat
def gpt_call(system_prompt: str, user_msg: str):
    try:
        resp = genai.chat.completions.create(
            model="models/chat-bison-001",        # or your chosen Gemini chat model
            messages=[
                {"author": "system", "content": system_prompt},
                {"author": "user",   "content": user_msg}
            ],
            temperature=0.3,
            # you can tweak max_output_tokens, top_p, etc. here
        )
        # Gemini returns .choices, each with .message.content
        return json.loads(resp.choices[0].message.content)
    except Exception:
        return FALLBACK

# 6️⃣ Define your endpoints
@app.post("/m1-match")
async def m1(request: MatchRequest):
    prompt = load_prompt("prompt_m1.txt")
    return gpt_call(prompt, request.user_input)

@app.post("/m2-match")
async def m2(request: MatchRequest):
    prompt = load_prompt("prompt_m2.txt")
    return gpt_call(prompt, request.user_input)

@app.post("/m3-match")
async def m3(request: MatchRequest):
    prompt = load_prompt("prompt_m3.txt")
    return gpt_call(prompt, request.user_input)

@app.post("/m4-match")
async def m4(request: MatchRequest):
    prompt = load_prompt("prompt_m4.txt")
    return gpt_call(prompt, request.user_input)

@app.get("/")
def ping():
    return {"status": "ok"}
