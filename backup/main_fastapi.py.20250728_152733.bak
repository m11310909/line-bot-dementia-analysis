#!/usr/bin/env python3
"""
FastAPI-based main application - optimized replacement for Flask version
FastAPI版本的主应用 - Flask版本的优化替代
"""

from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
import uvicorn
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, FlexSendMessage
from pinecone import Pinecone
import os
import json
from datetime import datetime
import hashlib

# Import our optimized components
from simple_embedding import embedder
from memory_cache import cache

# Initialize FastAPI app
app = FastAPI(
    title="Dementia Care Assistant API",
    description="XAI Flex Message API with Pinecone integration",
    version="2.0.0"
)

# Initialize Pinecone
try:
    pc = Pinecone(api_key="pcsk_4WvWXx_G5bRUFdFNzLzRHNM9rkvFMvC18TMRTaeYXVCxmWSPQLmKr4xAs4UaZg5NvVb69m")
    index = pc.Index("dementia-care-knowledge")
    print("✅ Pinecone initialized successfully")
except Exception as e:
    print(f"❌ Pinecone initialization failed: {e}")
    index = None

# LINE Bot credentials (replace with your actual credentials)
LINE_CHANNEL_ACCESS_TOKEN = os.getenv('LINE_CHANNEL_ACCESS_TOKEN', 'your_token_here')
LINE_CHANNEL_SECRET = os.getenv('LINE_CHANNEL_SECRET', 'your_secret_here')

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN) if LINE_CHANNEL_ACCESS_TOKEN != 'your_token_here' else None
handler = WebhookHandler(LINE_CHANNEL_SECRET) if LINE_CHANNEL_SECRET != 'your_secret_here' else None

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "Dementia Care Assistant API",
        "version": "2.0.0",
        "optimized": True,
        "pinecone_connected": index is not None,
        "line_bot_configured": line_bot_api is not None
    }

@app.get("/health")
async def health_check():
    """Detailed health check"""
    pinecone_status = "connected" if index else "disconnected"
    linebot_status = "configured" if line_bot_api else "not_configured"

    if index:
        try:
            stats = index.describe_index_stats()
            vector_count = stats.total_vector_count
        except:
            vector_count = "unknown"
    else:
        vector_count = 0

    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "components": {
            "pinecone": pinecone_status,
            "linebot": linebot_status,
            "embedding": "simple_embedding_ready",
            "cache": "memory_cache_ready"
        },
        "metrics": {
            "vector_count": vector_count,
            "cache_size": len(cache.cache) if hasattr(cache, 'cache') else 0
        }
    }

@app.post("/webhook")
async def line_webhook(request: Request):
    """LINE Bot webhook endpoint"""
    if not handler:
        raise HTTPException(status_code=500, detail="LINE Bot not configured")

    # Get request body and signature
    body = await request.body()
    signature = request.headers.get('X-Line-Signature', '')

    try:
        handler.handle(body.decode('utf-8'), signature)
    except InvalidSignatureError:
        raise HTTPException(status_code=400, detail="Invalid signature")

    return {"status": "success"}

@app.post("/chat")
async def chat_endpoint(request: dict):
    """Chat endpoint for testing and API usage"""
    try:
        user_message = request.get('message', '')
        user_id = request.get('user_id', 'api_user')

        if not user_message:
            raise HTTPException(status_code=400, detail="Message is required")

        # Generate response using RAG
        response = await generate_rag_response(user_message, user_id)

        return {
            "status": "success",
            "user_message": user_message,
            "response": response,
            "timestamp": datetime.now().isoformat()
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def generate_rag_response(message: str, user_id: str) -> dict:
    """Generate RAG response using Pinecone and simple embedding"""

    # Check cache first
    cache_key = f"chat:{hashlib.md5(message.encode()).hexdigest()}"
    cached_response = cache.get(cache_key)
    if cached_response:
        return {"text": cached_response, "source": "cache"}

    if not index:
        return {"text": "Sorry, the knowledge base is not available right now.", "source": "fallback"}

    try:
        # Create embedding for the message
        query_vector = embedder.encode(message)

        # Search in Pinecone
        search_results = index.query(
            vector=query_vector,
            top_k=3,
            include_metadata=True
        )

        # Generate response based on search results
        if search_results.matches and search_results.matches[0].score > 0.7:
            # High confidence match
            best_match = search_results.matches[0]
            response_text = f"Based on our knowledge: {best_match.metadata.get('content', 'Information found but content not available.')}"
            source = "knowledge_base"
        else:
            # No good match, provide general support
            response_text = generate_general_response(message)
            source = "general"

        # Cache the response
        cache.set(cache_key, response_text, ttl=3600)  # Cache for 1 hour

        return {"text": response_text, "source": source}

    except Exception as e:
        print(f"Error in RAG generation: {e}")
        return {"text": "I'm here to help. Could you please rephrase your question?", "source": "fallback"}

def generate_general_response(message: str) -> str:
    """Generate general responses for dementia care"""
    message_lower = message.lower()

    if any(word in message_lower for word in ['memory', 'forget', 'remember']):
        return "Memory challenges are common. Try breaking tasks into smaller steps and using visual reminders."

    elif any(word in message_lower for word in ['medication', 'medicine', 'pills']):
        return "For medication management, consider using pill organizers and setting regular reminders."

    elif any(word in message_lower for word in ['confused', 'lost', 'where']):
        return "If feeling confused or lost, stay calm and look for familiar landmarks or ask for help from nearby people."

    elif any(word in message_lower for word in ['family', 'caregiver', 'help']):
        return "Family support is crucial. Regular communication and shared caregiving responsibilities can help everyone."

    else:
        return "I'm here to help with dementia care questions. Feel free to ask about memory, medication, daily activities, or family support."

@handler.add(MessageEvent, message=TextMessage)
def handle_text_message(event):
    """Handle incoming LINE text messages"""
    user_message = event.message.text
    user_id = event.source.user_id

    # Generate response
    import asyncio
    response = asyncio.run(generate_rag_response(user_message, user_id))

    # Create Flex Message for better UI
    flex_message = create_dementia_care_flex_message(response['text'], response['source'])

    # Reply to user
    line_bot_api.reply_message(
        event.reply_token,
        FlexSendMessage(alt_text="Dementia Care Assistant", contents=flex_message)
    )

def create_dementia_care_flex_message(response_text: str, source: str) -> dict:
    """Create Flex Message for dementia care responses"""

    # Color scheme based on source
    colors = {
        "knowledge_base": "#4CAF50",  # Green for authoritative
        "general": "#2196F3",         # Blue for general advice
        "cache": "#FF9800",           # Orange for cached
        "fallback": "#9E9E9E"         # Gray for fallback
    }

    color = colors.get(source, "#2196F3")

    return {
        "type": "bubble",
        "header": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "text",
                    "text": "🧠 Dementia Care Assistant",
                    "weight": "bold",
                    "color": "#FFFFFF",
                    "size": "lg"
                }
            ],
            "backgroundColor": color,
            "paddingAll": "20px"
        },
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "text",
                    "text": response_text,
                    "wrap": True,
                    "size": "md",
                    "color": "#333333"
                },
                {
                    "type": "separator",
                    "margin": "lg"
                },
                {
                    "type": "text",
                    "text": f"💡 Source: {source.replace('_', ' ').title()}",
                    "size": "sm",
                    "color": "#888888",
                    "margin": "md"
                }
            ],
            "paddingAll": "20px"
        },
        "footer": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "button",
                    "action": {
                        "type": "message",
                        "label": "Ask Another Question",
                        "text": "I have another question"
                    },
                    "style": "primary",
                    "color": color
                }
            ],
            "paddingAll": "10px"
        }
    }

@app.get("/test-embedding")
async def test_embedding():
    """Test endpoint for embedding functionality"""
    test_text = "How can I help someone with dementia remember to take medication?"
    vector = embedder.encode(test_text)

    return {
        "text": test_text,
        "vector_length": len(vector),
        "sample_values": vector[:5],
        "status": "success"
    }

@app.get("/test-pinecone")
async def test_pinecone():
    """Test endpoint for Pinecone functionality"""
    if not index:
        raise HTTPException(status_code=500, detail="Pinecone not available")

    try:
        stats = index.describe_index_stats()

        # Test query
        test_vector = embedder.encode("medication reminder")
        results = index.query(
            vector=test_vector,
            top_k=3,
            include_metadata=True
        )

        return {
            "stats": {
                "total_vectors": stats.total_vector_count,
                "dimension": stats.dimension
            },
            "test_query": {
                "matches_found": len(results.matches),
                "top_score": results.matches[0].score if results.matches else 0
            },
            "status": "success"
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    print("🚀 Starting Dementia Care Assistant API (FastAPI)")
    print("=" * 50)
    print("✅ Optimized version running")
    print("✅ Using simple_embedding instead of sentence-transformers")
    print("✅ Using memory_cache instead of Redis")
    print("✅ Pinecone integration active")
    print("\n🌐 Access points:")
    print("• Health: http://localhost:8000/health")
    print("• Chat API: http://localhost:8000/chat")
    print("• LINE Webhook: http://localhost:8000/webhook")
    print("• Docs: http://localhost:8000/docs")

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        reload=True
    )