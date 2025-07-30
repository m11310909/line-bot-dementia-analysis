from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Flex Message API", version="1.0.0")

# Request/Response Models
class FlexMessageRequest(BaseModel):
    chunk_ids: List[str] = Field(..., description="List of chunk IDs to process")
    user_context: Optional[Dict[str, Any]] = Field(default={}, description="User context information")

class FlexMessageResponse(BaseModel):
    flex_message: Dict[str, Any] = Field(..., description="Generated LINE Flex Message")
    fallback_text: str = Field(..., description="Fallback text for unsupported clients")
    interaction_handlers: Dict[str, Any] = Field(..., description="Interaction handlers configuration")

class Chunk(BaseModel):
    id: str
    content: str
    metadata: Dict[str, Any] = {}
    timestamp: datetime = Field(default_factory=datetime.now)

# Mock database - replace with your actual database implementation
MOCK_CHUNKS_DB = {
    "chunk_1": Chunk(id="chunk_1", content="This is sample content for chunk 1", metadata={"type": "text"}),
    "chunk_2": Chunk(id="chunk_2", content="This is sample content for chunk 2", metadata={"type": "image"}),
    "chunk_3": Chunk(id="chunk_3", content="This is sample content for chunk 3", metadata={"type": "video"})
}

# Database operations
async def get_chunks_by_ids(chunk_ids: List[str]) -> List[Chunk]:
    """
    Retrieve chunks by their IDs from the database
    Replace this with your actual database query
    """
    try:
        chunks = []
        for chunk_id in chunk_ids:
            if chunk_id in MOCK_CHUNKS_DB:
                chunks.append(MOCK_CHUNKS_DB[chunk_id])
            else:
                logger.warning(f"Chunk ID {chunk_id} not found")
        
        if not chunks:
            raise ValueError("No valid chunks found")
        
        return chunks
    except Exception as e:
        logger.error(f"Error retrieving chunks: {str(e)}")
        raise

# XAI Explanation Engine
class ExplanationEngine:
    def generate_explanations(self, chunks: List[Chunk]) -> Dict[str, Any]:
        """
        Generate XAI explanations for the given chunks
        Replace this with your actual XAI implementation
        """
        try:
            explanations = {}
            for chunk in chunks:
                explanations[chunk.id] = {
                    "confidence_score": 0.85,
                    "key_features": ["feature_1", "feature_2", "feature_3"],
                    "reasoning": f"This content was selected based on relevance to user query",
                    "metadata": chunk.metadata
                }
            return explanations
        except Exception as e:
            logger.error(f"Error generating explanations: {str(e)}")
            raise

# Flex Message Generator
class FlexGenerator:
    def generate_enhanced_flex_message(
        self, 
        chunks: List[Chunk], 
        explanations: Dict[str, Any], 
        user_context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Generate LINE Flex Message with enhanced content
        """
        try:
            # Basic Flex Message structure
            flex_message = {
                "type": "flex",
                "altText": "Enhanced Content Message",
                "contents": {
                    "type": "bubble",
                    "header": {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {
                                "type": "text",
                                "text": "AI-Enhanced Content",
                                "weight": "bold",
                                "size": "lg",
                                "color": "#333333"
                            }
                        ]
                    },
                    "body": {
                        "type": "box",
                        "layout": "vertical",
                        "contents": []
                    },
                    "footer": {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {
                                "type": "button",
                                "action": {
                                    "type": "postback",
                                    "label": "More Details",
                                    "data": f"action=details&chunks={','.join([c.id for c in chunks])}"
                                },
                                "style": "primary"
                            }
                        ]
                    }
                }
            }
            
            # Add content for each chunk
            for chunk in chunks:
                explanation = explanations.get(chunk.id, {})
                
                # Add chunk content
                flex_message["contents"]["body"]["contents"].extend([
                    {
                        "type": "text",
                        "text": chunk.content[:100] + "..." if len(chunk.content) > 100 else chunk.content,
                        "wrap": True,
                        "margin": "md"
                    },
                    {
                        "type": "text",
                        "text": f"Confidence: {explanation.get('confidence_score', 0):.2%}",
                        "size": "sm",
                        "color": "#999999",
                        "margin": "sm"
                    },
                    {
                        "type": "separator",
                        "margin": "md"
                    }
                ])
            
            return flex_message
            
        except Exception as e:
            logger.error(f"Error generating flex message: {str(e)}")
            raise

# Utility functions
def generate_fallback_text(chunks: List[Chunk]) -> str:
    """Generate fallback text for clients that don't support Flex Messages"""
    try:
        content_summary = "\n".join([f"- {chunk.content[:50]}..." for chunk in chunks[:3]])
        return f"AI-Enhanced Content:\n{content_summary}"
    except Exception as e:
        logger.error(f"Error generating fallback text: {str(e)}")
        return "AI-Enhanced Content Available"

def create_interaction_handlers(chunks: List[Chunk]) -> Dict[str, Any]:
    """Create interaction handlers for the Flex Message"""
    try:
        handlers = {
            "postback_handlers": {
                "details": {
                    "action": "show_details",
                    "chunk_ids": [chunk.id for chunk in chunks]
                }
            },
            "quick_replies": [
                {
                    "type": "action",
                    "action": {
                        "type": "postback",
                        "label": "Explain More",
                        "data": "action=explain"
                    }
                }
            ]
        }
        return handlers
    except Exception as e:
        logger.error(f"Error creating interaction handlers: {str(e)}")
        return {}

def handle_flex_generation_error(error: Exception) -> Dict[str, Any]:
    """Handle errors in flex message generation"""
    logger.error(f"Flex generation error: {str(error)}")
    
    error_response = {
        "error": True,
        "message": "Failed to generate flex message",
        "details": str(error),
        "fallback_flex_message": {
            "type": "flex",
            "altText": "Error occurred",
            "contents": {
                "type": "bubble",
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "text",
                            "text": "Sorry, an error occurred while generating content.",
                            "wrap": True
                        }
                    ]
                }
            }
        }
    }
    
    return error_response

# Initialize components
explanation_engine = ExplanationEngine()
flex_generator = FlexGenerator()

# Main API endpoint
@app.post("/api/v1/flex-message", response_model=FlexMessageResponse)
async def generate_flex_message(request: FlexMessageRequest):
    """
    Generate enhanced Flex Message with XAI explanations
    
    - **chunk_ids**: List of chunk IDs to process
    - **user_context**: Optional user context for personalization
    """
    try:
        logger.info(f"Processing flex message request for chunks: {request.chunk_ids}")
        
        # Validate input
        if not request.chunk_ids:
            raise HTTPException(status_code=400, detail="chunk_ids cannot be empty")
        
        # Get chunk data
        chunks = await get_chunks_by_ids(request.chunk_ids)
        logger.info(f"Retrieved {len(chunks)} chunks")
        
        # Generate XAI explanations
        explanations = explanation_engine.generate_explanations(chunks)
        logger.info("Generated XAI explanations")
        
        # Generate Flex Message
        flex_message = flex_generator.generate_enhanced_flex_message(
            chunks, explanations, request.user_context
        )
        logger.info("Generated enhanced flex message")
        
        # Create response
        response = FlexMessageResponse(
            flex_message=flex_message,
            fallback_text=generate_fallback_text(chunks),
            interaction_handlers=create_interaction_handlers(chunks)
        )
        
        logger.info("Successfully generated flex message response")
        return response
        
    except ValueError as e:
        logger.error(f"Validation error: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        error_response = handle_flex_generation_error(e)
        raise HTTPException(status_code=500, detail=error_response)

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

# Additional endpoints for testing
@app.get("/api/v1/chunks/{chunk_id}")
async def get_chunk(chunk_id: str):
    """Get a specific chunk by ID"""
    if chunk_id in MOCK_CHUNKS_DB:
        return MOCK_CHUNKS_DB[chunk_id]
    raise HTTPException(status_code=404, detail="Chunk not found")

@app.get("/api/v1/chunks")
async def list_chunks():
    """List all available chunks"""
    return {"chunks": list(MOCK_CHUNKS_DB.keys())}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)# (paste the entire code from the artifact above)

