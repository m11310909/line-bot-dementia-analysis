# routers/flex.py
from fastapi import APIRouter, HTTPException
from datetime import datetime
from typing import List

router = APIRouter()

@router.post("/api/v1/flex-message")
async def generate_flex_message(chunk_ids: List[str]):
    try:
        return {
            "flex_message": {
                "type": "bubble",
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {"type": "text", "text": "失智照護資訊", "weight": "bold", "size": "lg"},
                        {"type": "text", "text": "相關資訊已為您準備完成", "size": "sm", "wrap": True}
                    ]
                }
            },
            "fallback_text": "失智照護資訊",
            "metadata": {"generated_at": datetime.now().isoformat()}
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
