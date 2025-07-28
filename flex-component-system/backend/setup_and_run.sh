#!/usr/bin/env bash
set -e

# 确保下面这些环境变量已经被导出：
# GOOGLE_APPLICATION_CREDENTIALS, PROJECT_ID, LOCATION,
# PINECONE_API_KEY, PINECONE_ENV, INDEX_NAME

echo ">>> 1. 创建并激活 Python 虚拟环境"
python -m venv venv
source venv/bin/activate
pip install --upgrade pip

echo ">>> 2. 安装后端依赖"
pip install fastapi uvicorn pydantic asyncio \
            google-cloud-aiplatform \
            pinecone-client \
            google-generativeai

echo ">>> 3. 生成 config.py"
cat > config.py <<'EOF'
import os
import pinecone
from google.cloud import aiplatform

# 1. Vertex AI
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
PROJECT_ID = os.environ["PROJECT_ID"]
LOCATION   = os.environ["LOCATION"]
EMBED_MODEL = f"projects/{PROJECT_ID}/locations/{LOCATION}/publishers/google/models/textembedding-gecko@001"

# 2. Pinecone
PINECONE_API_KEY = os.environ["PINECONE_API_KEY"]
PINECONE_ENV     = os.environ["PINECONE_ENV"]
INDEX_NAME       = os.environ["INDEX_NAME"]

pinecone.init(api_key=PINECONE_API_KEY, environment=PINECONE_ENV)
if INDEX_NAME not in pinecone.list_indexes():
    pinecone.create_index(
        name=INDEX_NAME, dimension=1536, metric="cosine", pods=1, replicas=1
    )
pinecone_index = pinecone.Index(INDEX_NAME)
EOF

echo ">>> 4. 生成 embeddings.py"
cat > embeddings.py <<'EOF'
from typing import List
from google.cloud import aiplatform
from config import LOCATION, PROJECT_ID

# Vertex AI embedding client
embed_client = aiplatform.gapic.EmbeddingServiceClient(
    client_options={"api_endpoint": f"{LOCATION}-aiplatform.googleapis.com"}
)
EMBED_MODEL = f"projects/{PROJECT_ID}/locations/{LOCATION}/publishers/google/models/textembedding-gecko@001"

def embed_texts(texts: List[str]) -> List[List[float]]:
    request = {"model": EMBED_MODEL, "contents": texts}
    response = embed_client.embed_text(request=request)
    return [e.values for e in response.embeddings]
EOF

echo ">>> 5. 生成 pinecone_utils.py"
cat > pinecone_utils.py <<'EOF'
from typing import List, Dict
from config import pinecone_index
from embeddings import embed_texts

def upsert_documents(docs: List[Dict]):
    batch_size = 50
    for i in range(0, len(docs), batch_size):
        batch = docs[i : i + batch_size]
        texts = [d["text"] for d in batch]
        vectors = embed_texts(texts)
        to_upsert = [(d["id"], vec, d["metadata"]) for d, vec in zip(batch, vectors)]
        pinecone_index.upsert(vectors=to_upsert)
EOF

echo ">>> 6. 生成 upsert_templates.py"
cat > upsert_templates.py <<'EOF'
import json
from pinecone_utils import upsert_documents

def chunk_text(text: str, size: int = 2000) -> list:
    return [text[i:i+size] for i in range(0, len(text), size)]

def main():
    with open("../docs/flex_templates.json", "r", encoding="utf-8") as f:
        raw = json.load(f)
    docs = []
    for item in raw:
        for idx, chunk in enumerate(chunk_text(item["template"])):
            docs.append({
                "id": f"{item['id']}-{idx}",
                "text": chunk,
                "metadata": {"source_id": item["id"]}
            })
    echo_count=${#docs[@]}
    echo "Upserting $echo_count chunks..."
    upsert_documents(docs)
    echo "✅ Upsert complete."

if __name__ == "__main__":
    main()
EOF

echo ">>> 7. 生成 main.py"
cat > main.py <<'EOF'
from fastapi import FastAPI
from pydantic import BaseModel
from config import pinecone_index
from embeddings import embed_texts
import google.generativeai as genai
import os

# 配置 Gemini API
genai.configure(api_key=os.getenv("GOOGLE_APPLICATION_CREDENTIALS"))

app = FastAPI(title="Flex Component System API")

class FlexRequest(BaseModel):
    text: str

class FlexResponse(BaseModel):
    flex_json: dict

@app.get("/")
async def root():
    return {"message": "Service is up."}

@app.post("/m1-flex", response_model=FlexResponse)
async def m1_flex(req: FlexRequest):
    vec = embed_texts([req.text])[0]
    res = pinecone_index.query(vector=vec, top_k=5, include_metadata=True)
    templates = [m["metadata"]["source_id"] for m in res["matches"]]
    system = "你是資深 LINE Flex Message JSON 專家"
    user = (
        f"根據這些模板 ID：{templates}，"
        f"將使用者輸入「{req.text}」轉成符合 LINE Flex Message 規格的 JSON。"
    )
    gpt_res = genai.ChatCompletion.create(
        model="gemini-pro",
        messages=[{"role":"system","content":system},
                  {"role":"user","content":user}]
    )
    return FlexResponse(flex_json=gpt_res.choices[0].message.content)
EOF

echo ">>> 8. 执行模板上载到 Pinecone"
python upsert_templates.py

echo ">>> 9. 启动 FastAPI 服务"
exec uvicorn main:app --reload --host 0.0.0.0 --port 8000
