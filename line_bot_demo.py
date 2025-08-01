#!/usr/bin/env python3
"""
LINE Bot Demo - M1 Enhanced Visualization
Demo version that works without LINE credentials
"""

from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
import requests
import os
import logging
import traceback
import json
from typing import Optional, Dict, Any
from datetime import datetime

# Import M1 visualization modules
try:
    from xai_flex.m1_enhanced_visualization import M1EnhancedVisualizationGenerator, WarningLevel
    M1_AVAILABLE = True
except ImportError:
    M1_AVAILABLE = False
    print("⚠️ M1 modules not available, using fallback")

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="LINE Bot Demo - M1 Enhanced v3.0",
    description="Demo LINE Bot with M1 visualization integration",
    version="3.0.0"
)

# Initialize M1 modules
m1_generator = None

if M1_AVAILABLE:
    try:
        m1_generator = M1EnhancedVisualizationGenerator()
        logger.info("✅ M1 visualization modules initialized")
    except Exception as e:
        logger.error(f"❌ M1 modules initialization failed: {e}")

# Simple M1 generator as fallback
class SimpleM1Generator:
    """Simple M1 generator for demo"""
    
    def generate_m1_flex_message(self, analysis_result: dict) -> dict:
        """Generate simple M1 Flex Message"""
        try:
            confidence_score = analysis_result.get('confidence_score', 0.0)
            comparison_data = analysis_result.get('comparison_data', {})
            key_finding = analysis_result.get('key_finding', '')
            warning_level = analysis_result.get('warning_level', 'normal')
            
            # Generate confidence percentage
            confidence_percentage = int(confidence_score * 100)
            if confidence_percentage > 80:
                confidence_color = "#4CAF50"
            elif confidence_percentage > 50:
                confidence_color = "#2196F3"
            else:
                confidence_color = "#FF9800"
            
            # Create Flex Bubble
            flex_bubble = {
                "type": "bubble",
                "size": "mega",
                "header": {
                    "type": "box",
                    "layout": "vertical",
                    "backgroundColor": "#FFFFFF",
                    "contents": [
                        {
                            "type": "text",
                            "text": "AI 分析結果",
                            "size": "lg",
                            "weight": "bold",
                            "color": "#212121"
                        },
                        {
                            "type": "text",
                            "text": "記憶力評估",
                            "size": "sm",
                            "color": "#666666",
                            "margin": "sm"
                        }
                    ]
                },
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "backgroundColor": "#F5F5F5",
                    "contents": [
                        # Confidence meter
                        {
                            "type": "box",
                            "layout": "vertical",
                            "contents": [
                                {
                                    "type": "text",
                                    "text": f"AI 信心度 {confidence_percentage}%",
                                    "size": "xs",
                                    "color": "#666666",
                                    "margin": "sm"
                                },
                                {
                                    "type": "box",
                                    "layout": "horizontal",
                                    "backgroundColor": "#F0F0F0",
                                    "height": "8px",
                                    "cornerRadius": "4px",
                                    "contents": [
                                        {
                                            "type": "box",
                                            "layout": "vertical",
                                            "backgroundColor": confidence_color,
                                            "width": f"{confidence_percentage}%",
                                            "cornerRadius": "4px",
                                            "contents": []
                                        }
                                    ]
                                }
                            ]
                        },
                        # Comparison cards
                        {
                            "type": "box",
                            "layout": "horizontal",
                            "contents": [
                                # Normal aging card
                                {
                                    "type": "box",
                                    "layout": "vertical",
                                    "backgroundColor": "#E8F5E9",
                                    "cornerRadius": "8px",
                                    "paddingAll": "16px",
                                    "margin": "sm",
                                    "contents": [
                                        {
                                            "type": "box",
                                            "layout": "horizontal",
                                            "contents": [
                                                {
                                                    "type": "text",
                                                    "text": "👴",
                                                    "size": "lg",
                                                    "flex": 0
                                                },
                                                {
                                                    "type": "text",
                                                    "text": "正常老化",
                                                    "size": "sm",
                                                    "weight": "bold",
                                                    "color": "#212121",
                                                    "flex": 1,
                                                    "margin": "sm"
                                                }
                                            ]
                                        },
                                        {
                                            "type": "text",
                                            "text": comparison_data.get("normal_aging", "一般記憶力衰退"),
                                            "size": "xs",
                                            "color": "#666666",
                                            "wrap": True,
                                            "margin": "sm"
                                        }
                                    ]
                                },
                                # Dementia warning card
                                {
                                    "type": "box",
                                    "layout": "vertical",
                                    "backgroundColor": "#FFF3E0",
                                    "cornerRadius": "8px",
                                    "paddingAll": "16px",
                                    "margin": "sm",
                                    "contents": [
                                        {
                                            "type": "box",
                                            "layout": "horizontal",
                                            "contents": [
                                                {
                                                    "type": "text",
                                                    "text": "⚠️",
                                                    "size": "lg",
                                                    "flex": 0
                                                },
                                                {
                                                    "type": "text",
                                                    "text": "失智警訊",
                                                    "size": "sm",
                                                    "weight": "bold",
                                                    "color": "#212121",
                                                    "flex": 1,
                                                    "margin": "sm"
                                                }
                                            ]
                                        },
                                        {
                                            "type": "text",
                                            "text": comparison_data.get("dementia_warning", "需要關注的徵兆"),
                                            "size": "xs",
                                            "color": "#666666",
                                            "wrap": True,
                                            "margin": "sm"
                                        }
                                    ]
                                }
                            ]
                        },
                        # Key finding
                        {
                            "type": "text",
                            "text": f"💡 {key_finding}",
                            "size": "sm",
                            "color": "#2196F3",
                            "wrap": True,
                            "margin": "md"
                        }
                    ]
                },
                "footer": {
                    "type": "box",
                    "layout": "vertical",
                    "backgroundColor": "#FFFFFF",
                    "contents": [
                        {
                            "type": "button",
                            "action": {
                                "type": "postback",
                                "label": "查看詳細分析",
                                "data": "m1_detail"
                            },
                            "style": "primary",
                            "height": "44px",
                            "color": "#2196F3",
                            "margin": "sm"
                        }
                    ]
                }
            }
            
            return {
                "type": "flex",
                "altText": f"失智照護分析：{key_finding}",
                "contents": flex_bubble,
                "metadata": {
                    "module": "M1",
                    "confidence_score": confidence_score,
                    "warning_level": warning_level,
                    "generated_at": datetime.now().isoformat()
                }
            }
            
        except Exception as e:
            logger.error(f"M1 Flex Message generation failed: {e}")
            return {
                "type": "flex",
                "altText": "分析暫時無法使用",
                "contents": {
                    "type": "bubble",
                    "body": {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {
                                "type": "text",
                                "text": "⚠️ 暫時無法分析",
                                "size": "lg",
                                "weight": "bold",
                                "color": "#FF9800"
                            },
                            {
                                "type": "text",
                                "text": "請稍後再試",
                                "size": "sm",
                                "color": "#666666",
                                "margin": "sm"
                            }
                        ]
                    }
                }
            }

# Initialize simple M1 generator
simple_m1_generator = SimpleM1Generator()

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "LINE Bot Demo - M1 Enhanced v3.0",
        "status": "running",
        "mode": "demo",
        "m1_modules_ready": M1_AVAILABLE and m1_generator is not None,
        "version": "3.0.0",
        "features": [
            "🧠 M1 Enhanced Visualization",
            "🎨 Design System Integration",
            "🔍 XAI Confidence Display",
            "📊 Comparison Cards",
            "♿ Accessibility Features"
        ],
        "note": "This is a demo mode. Set LINE credentials to enable full functionality."
    }

@app.get("/health")
async def health_check():
    """Health check with M1 status"""
    health = {
        "status": "healthy",
        "mode": "demo",
        "services": {},
        "timestamp": datetime.now().isoformat()
    }

    # Check M1 modules
    if M1_AVAILABLE and m1_generator:
        health["services"]["m1_modules"] = {"status": "ok"}
    else:
        health["services"]["m1_modules"] = {"status": "not_available"}

    return health

@app.post("/demo/message")
async def demo_message(request: Dict[str, Any]):
    """Demo endpoint to simulate LINE message handling"""
    try:
        user_text = request.get("text", "")
        user_id = request.get("user_id", "demo_user")
        
        logger.info(f"👤 Demo message from {user_id}: {user_text}")

        # Input validation
        if len(user_text) < 5:
            return {
                "type": "text",
                "text": "請提供更詳細的描述（至少5個字）\n\n💡 範例：\n• 媽媽最近常忘記關瓦斯\n• 爸爸重複問同樣問題"
            }

        if len(user_text) > 1000:
            return {
                "type": "text",
                "text": "描述過長，請簡化在1000字以內"
            }

        # Handle commands
        if user_text.lower() in ['help', '幫助', 'start', '開始', 'm1']:
            welcome_flex = create_m1_welcome_message()
            return {
                "type": "flex",
                "alt_text": "AI 失智症警訊分析 - 使用說明",
                "contents": welcome_flex
            }

        # Generate M1 analysis
        analysis_data = create_m1_fallback_response(user_text)
        flex_message_data = simple_m1_generator.generate_m1_flex_message(analysis_data)
        
        return {
            "type": "flex",
            "alt_text": flex_message_data.get("altText", "失智症警訊分析結果"),
            "contents": flex_message_data.get("contents", {}),
            "analysis_data": analysis_data
        }

    except Exception as e:
        logger.error(f"❌ Demo message handler error: {e}")
        return {
            "type": "text",
            "text": "抱歉，演示服務暫時無法使用。"
        }

def create_m1_welcome_message() -> Dict[str, Any]:
    """Create welcome message with M1 design"""
    return {
        "type": "bubble",
        "size": "mega",
        "header": {
            "type": "box",
            "layout": "vertical",
            "backgroundColor": "#FFFFFF",
            "contents": [
                {
                    "type": "text",
                    "text": "🧠 AI 失智症警訊分析",
                    "size": "lg",
                    "weight": "bold",
                    "color": "#212121"
                },
                {
                    "type": "text",
                    "text": "M1 十大警訊比對卡 (Demo)",
                    "size": "sm",
                    "color": "#666666",
                    "margin": "sm"
                }
            ]
        },
        "body": {
            "type": "box",
            "layout": "vertical",
            "backgroundColor": "#F5F5F5",
            "contents": [
                {
                    "type": "text",
                    "text": "請描述您觀察到的症狀，AI 將協助分析是否為失智症警訊。",
                    "size": "sm",
                    "color": "#666666",
                    "wrap": True,
                    "margin": "md"
                },
                {
                    "type": "text",
                    "text": "💡 範例：\n• 媽媽最近常忘記關瓦斯\n• 爸爸重複問同樣問題\n• 爺爺在熟悉環境中迷路",
                    "size": "xs",
                    "color": "#2196F3",
                    "wrap": True,
                    "margin": "md"
                }
            ]
        },
        "footer": {
            "type": "box",
            "layout": "vertical",
            "backgroundColor": "#FFFFFF",
            "contents": [
                {
                    "type": "text",
                    "text": "開始分析 (Demo)",
                    "size": "sm",
                    "color": "#2196F3",
                    "align": "center",
                    "margin": "md"
                }
            ]
        }
    }

def create_m1_fallback_response(user_input: str) -> Dict[str, Any]:
    """Create fallback M1 response when API is unavailable"""
    try:
        # Simple analysis based on keywords
        keywords = {
            "忘記": {"confidence": 0.75, "level": "caution"},
            "迷路": {"confidence": 0.80, "level": "warning"},
            "重複": {"confidence": 0.70, "level": "caution"},
            "瓦斯": {"confidence": 0.85, "level": "warning"},
            "鑰匙": {"confidence": 0.65, "level": "normal"},
            "約會": {"confidence": 0.75, "level": "caution"}
        }
        
        # Find matching keywords
        matched_keywords = []
        for keyword, data in keywords.items():
            if keyword in user_input:
                matched_keywords.append((keyword, data))
        
        if matched_keywords:
            # Use the highest confidence match
            best_match = max(matched_keywords, key=lambda x: x[1]["confidence"])
            keyword, data = best_match
            
            return {
                "confidence_score": data["confidence"],
                "comparison_data": {
                    "normal_aging": "偶爾忘記但能回想起來",
                    "dementia_warning": f"經常{keyword}且無法回想"
                },
                "key_finding": f"觀察到{keyword}相關症狀，建議進一步評估",
                "warning_level": data["level"]
            }
        else:
            # Default response
            return {
                "confidence_score": 0.50,
                "comparison_data": {
                    "normal_aging": "一般記憶力衰退",
                    "dementia_warning": "需要更多資訊評估"
                },
                "key_finding": "請提供更詳細的症狀描述",
                "warning_level": "normal"
            }
    except Exception as e:
        logger.error(f"Fallback analysis failed: {e}")
        return {
            "confidence_score": 0.0,
            "comparison_data": {
                "normal_aging": "無法分析",
                "dementia_warning": "請諮詢專業醫師"
            },
            "key_finding": "分析服務暫時無法使用",
            "warning_level": "normal"
        }

@app.get("/info")
async def bot_info():
    """Get bot information"""
    return {
        "bot_name": "AI 失智症警訊分析 (Demo)",
        "version": "3.0.0",
        "mode": "demo",
        "features": [
            "M1 Enhanced Visualization",
            "XAI Confidence Display",
            "Comparison Cards",
            "Accessibility Features"
        ],
        "m1_available": M1_AVAILABLE,
        "note": "This is a demo mode. Set LINE credentials to enable full functionality."
    }

@app.get("/ping")
async def ping():
    """Simple ping endpoint"""
    return {"pong": "M1 Enhanced v3.0 Demo"}

@app.post("/test")
async def test_endpoint():
    """Test endpoint for M1 visualization"""
    if not M1_AVAILABLE or not m1_generator:
        return {"error": "M1 modules not available"}
    
    try:
        # Test M1 visualization
        test_data = {
            "confidence_score": 0.85,
            "comparison_data": {
                "normal_aging": "偶爾忘記鑰匙位置，但能回想起來",
                "dementia_warning": "經常忘記重要約會，且無法回想"
            },
            "key_finding": "記憶力衰退模式符合輕度認知障礙徵兆",
            "warning_level": "caution"
        }
        
        flex_message = m1_generator.generate_m1_flex_message(test_data)
        return {
            "status": "success",
            "m1_test": flex_message
        }
    except Exception as e:
        return {"error": str(e)}

@app.get("/demo")
async def demo_page():
    """Demo page with test interface"""
    return {
        "message": "LINE Bot M1 Demo",
        "endpoints": {
            "test_message": "POST /demo/message",
            "test_m1": "POST /test",
            "health": "GET /health",
            "info": "GET /info"
        },
        "example_request": {
            "text": "媽媽最近常忘記關瓦斯",
            "user_id": "demo_user"
        }
    }

if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting LINE Bot Demo with M1 integration...")
    print("💡 This is a demo mode - no LINE credentials required")
    print("🌐 Access demo at: http://localhost:8000/demo")
    uvicorn.run(app, host="0.0.0.0", port=8000) 