#!/usr/bin/env python3
"""
Enhanced LINE Bot Demo - M1, M2, M3 Integrated Analysis
Comprehensive demo with multiple dementia analysis modules
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

# Import all modules
try:
    from xai_flex.m1_enhanced_visualization import M1EnhancedVisualizationGenerator, WarningLevel
    from modules.m2_progression_matrix import M2ProgressionMatrixModule
    from modules.m3_bpsd_classification import M3BPSDClassificationModule
    ALL_MODULES_AVAILABLE = True
except ImportError as e:
    ALL_MODULES_AVAILABLE = False
    print(f"⚠️ Some modules not available: {e}")

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="Enhanced LINE Bot Demo - M1+M2+M3 Integration",
    description="Comprehensive dementia analysis with multiple modules",
    version="4.0.0"
)

# Initialize all modules
m1_generator = None
m2_module = None
m3_module = None

if ALL_MODULES_AVAILABLE:
    try:
        m1_generator = M1EnhancedVisualizationGenerator()
        m2_module = M2ProgressionMatrixModule()
        m3_module = M3BPSDClassificationModule()
        logger.info("✅ All modules (M1, M2, M3) initialized successfully")
    except Exception as e:
        logger.error(f"❌ Module initialization failed: {e}")

# Simple fallback generators
class SimpleM1Generator:
    """Simple M1 generator for demo"""
    
    def generate_m1_flex_message(self, analysis_result: dict) -> dict:
        """Generate simple M1 Flex Message"""
        try:
            confidence_score = analysis_result.get('confidence_score', 0.0)
            comparison_data = analysis_result.get('comparison_data', {})
            key_finding = analysis_result.get('key_finding', '')
            warning_level = analysis_result.get('warning_level', 'normal')
            
            confidence_percentage = int(confidence_score * 100)
            confidence_color = "#4CAF50" if confidence_percentage > 80 else "#2196F3" if confidence_percentage > 50 else "#FF9800"
            
            return {
                "type": "flex",
                "alt_text": f"失智照護分析：{key_finding}",
                "contents": {
                    "type": "bubble",
                    "size": "mega",
                    "header": {
                        "type": "box",
                        "layout": "vertical",
                        "backgroundColor": "#FFFFFF",
                        "contents": [
                            {"type": "text", "text": "AI 分析結果", "size": "lg", "weight": "bold", "color": "#212121"},
                            {"type": "text", "text": "記憶力評估", "size": "sm", "color": "#666666", "margin": "sm"}
                        ]
                    },
                    "body": {
                        "type": "box",
                        "layout": "vertical",
                        "backgroundColor": "#F5F5F5",
                        "contents": [
                            {
                                "type": "box",
                                "layout": "vertical",
                                "contents": [
                                    {"type": "text", "text": f"AI 信心度 {confidence_percentage}%", "size": "xs", "color": "#666666", "margin": "sm"},
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
                            {
                                "type": "box",
                                "layout": "horizontal",
                                "contents": [
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
                                                    {"type": "text", "text": "👴", "size": "lg", "flex": 0},
                                                    {"type": "text", "text": "正常老化", "size": "sm", "weight": "bold", "color": "#212121", "flex": 1, "margin": "sm"}
                                                ]
                                            },
                                            {"type": "text", "text": comparison_data.get('normal_aging', ''), "size": "xs", "color": "#666666", "wrap": True, "margin": "sm"}
                                        ]
                                    },
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
                                                    {"type": "text", "text": "⚠️", "size": "lg", "flex": 0},
                                                    {"type": "text", "text": "失智警訊", "size": "sm", "weight": "bold", "color": "#212121", "flex": 1, "margin": "sm"}
                                                ]
                                            },
                                            {"type": "text", "text": comparison_data.get('dementia_warning', ''), "size": "xs", "color": "#666666", "wrap": True, "margin": "sm"}
                                        ]
                                    }
                                ]
                            },
                            {"type": "text", "text": f"💡 {key_finding}", "size": "sm", "color": "#2196F3", "wrap": True, "margin": "md"}
                        ]
                    },
                    "footer": {
                        "type": "box",
                        "layout": "vertical",
                        "backgroundColor": "#FFFFFF",
                        "contents": [
                            {
                                "type": "button",
                                "action": {"type": "postback", "label": "查看詳細分析", "data": "m1_detail"},
                                "style": "primary",
                                "height": "44px",
                                "color": "#2196F3",
                                "margin": "sm"
                            }
                        ]
                    }
                },
                "analysis_data": {
                    "confidence_score": confidence_score,
                    "comparison_data": comparison_data,
                    "key_finding": key_finding,
                    "warning_level": warning_level
                }
            }
        except Exception as e:
            logger.error(f"M1 Flex Message generation failed: {e}")
            return create_error_response("M1 分析暫時無法使用")

class SimpleM2Generator:
    """Simple M2 generator for demo"""
    
    def create_progression_card(self, user_input: str, stage_analysis: dict) -> dict:
        """Generate simple M2 progression card"""
        try:
            stage = stage_analysis.get('stage', '輕度')
            confidence = stage_analysis.get('confidence', 0.8)
            symptoms = stage_analysis.get('symptoms', [])
            care_focus = stage_analysis.get('care_focus', [])
            
            return {
                "type": "flex",
                "alt_text": f"病程階段分析：{stage}階段",
                "contents": {
                    "type": "bubble",
                    "size": "mega",
                    "header": {
                        "type": "box",
                        "layout": "vertical",
                        "backgroundColor": "#FFFFFF",
                        "contents": [
                            {"type": "text", "text": "病程階段評估", "size": "lg", "weight": "bold", "color": "#212121"},
                            {"type": "text", "text": f"評估結果：{stage}", "size": "sm", "color": "#666666", "margin": "sm"}
                        ]
                    },
                    "body": {
                        "type": "box",
                        "layout": "vertical",
                        "backgroundColor": "#F5F5F5",
                        "contents": [
                            {
                                "type": "text",
                                "text": f"信心度：{int(confidence * 100)}%",
                                "size": "sm",
                                "color": "#666666",
                                "margin": "sm"
                            },
                            {
                                "type": "text",
                                "text": "主要症狀：",
                                "size": "sm",
                                "weight": "bold",
                                "color": "#212121",
                                "margin": "md"
                            },
                            *[{"type": "text", "text": f"• {symptom}", "size": "xs", "color": "#666666", "wrap": True, "margin": "sm"} for symptom in symptoms[:3]],
                            {
                                "type": "text",
                                "text": "照護重點：",
                                "size": "sm",
                                "weight": "bold",
                                "color": "#212121",
                                "margin": "md"
                            },
                            *[{"type": "text", "text": f"• {care}", "size": "xs", "color": "#666666", "wrap": True, "margin": "sm"} for care in care_focus[:3]]
                        ]
                    }
                }
            }
        except Exception as e:
            logger.error(f"M2 progression card generation failed: {e}")
            return create_error_response("M2 分析暫時無法使用")

class SimpleM3Generator:
    """Simple M3 generator for demo"""
    
    def create_bpsd_card(self, user_input: str, bpsd_analysis: dict) -> dict:
        """Generate simple M3 BPSD card"""
        try:
            category = bpsd_analysis.get('category', '一般症狀')
            severity = bpsd_analysis.get('severity', '輕度')
            symptoms = bpsd_analysis.get('symptoms', [])
            interventions = bpsd_analysis.get('interventions', [])
            
            return {
                "type": "flex",
                "alt_text": f"行為心理症狀分析：{category}",
                "contents": {
                    "type": "bubble",
                    "size": "mega",
                    "header": {
                        "type": "box",
                        "layout": "vertical",
                        "backgroundColor": "#FFFFFF",
                        "contents": [
                            {"type": "text", "text": "行為心理症狀分析", "size": "lg", "weight": "bold", "color": "#212121"},
                            {"type": "text", "text": f"分類：{category} ({severity})", "size": "sm", "color": "#666666", "margin": "sm"}
                        ]
                    },
                    "body": {
                        "type": "box",
                        "layout": "vertical",
                        "backgroundColor": "#F5F5F5",
                        "contents": [
                            {
                                "type": "text",
                                "text": "觀察症狀：",
                                "size": "sm",
                                "weight": "bold",
                                "color": "#212121",
                                "margin": "sm"
                            },
                            *[{"type": "text", "text": f"• {symptom}", "size": "xs", "color": "#666666", "wrap": True, "margin": "sm"} for symptom in symptoms[:3]],
                            {
                                "type": "text",
                                "text": "處理建議：",
                                "size": "sm",
                                "weight": "bold",
                                "color": "#212121",
                                "margin": "md"
                            },
                            *[{"type": "text", "text": f"• {intervention}", "size": "xs", "color": "#666666", "wrap": True, "margin": "sm"} for intervention in interventions[:3]]
                        ]
                    }
                }
            }
        except Exception as e:
            logger.error(f"M3 BPSD card generation failed: {e}")
            return create_error_response("M3 分析暫時無法使用")

def create_error_response(message: str) -> dict:
    """Create error response"""
    return {
        "type": "flex",
        "alt_text": message,
        "contents": {
            "type": "bubble",
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {"type": "text", "text": "⚠️ 暫時無法分析", "size": "lg", "weight": "bold", "color": "#FF9800"},
                    {"type": "text", "text": "請稍後再試", "size": "sm", "color": "#666666", "margin": "sm"}
                ]
            }
        }
    }

def analyze_text_comprehensive(text: str) -> dict:
    """Comprehensive text analysis using all available modules"""
    results = {}
    
    # M1 Analysis (Warning Signs)
    if m1_generator:
        try:
            m1_result = m1_generator.generate_m1_flex_message({
                'confidence_score': 0.85,
                'comparison_data': {
                    'normal_aging': '偶爾忘記但能回想起來',
                    'dementia_warning': '經常忘記且無法回想'
                },
                'key_finding': '觀察到記憶力相關症狀，建議進一步評估',
                'warning_level': 'warning'
            })
            results['m1'] = m1_result
        except Exception as e:
            logger.error(f"M1 analysis failed: {e}")
            results['m1'] = create_error_response("M1 分析失敗")
    
    # M2 Analysis (Progression Stage)
    if m2_module:
        try:
            m2_analysis = m2_module.analyze_progression_stage(text)
            m2_result = m2_module.create_progression_card(text, m2_analysis)
            results['m2'] = m2_result
        except Exception as e:
            logger.error(f"M2 analysis failed: {e}")
            results['m2'] = create_error_response("M2 分析失敗")
    
    # M3 Analysis (BPSD)
    if m3_module:
        try:
            m3_analysis = m3_module.analyze_bpsd_symptoms(text)
            m3_result = m3_module.create_bpsd_card(text, m3_analysis)
            results['m3'] = m3_result
        except Exception as e:
            logger.error(f"M3 analysis failed: {e}")
            results['m3'] = create_error_response("M3 分析失敗")
    
    return results

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Enhanced LINE Bot Demo - M1+M2+M3 Integration",
        "version": "4.0.0",
        "status": "running",
        "modules": {
            "m1": "available" if m1_generator else "unavailable",
            "m2": "available" if m2_module else "unavailable", 
            "m3": "available" if m3_module else "unavailable"
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "mode": "enhanced_demo",
        "services": {
            "m1_modules": {"status": "ok" if m1_generator else "error"},
            "m2_modules": {"status": "ok" if m2_module else "error"},
            "m3_modules": {"status": "ok" if m3_module else "error"}
        },
        "timestamp": datetime.now().isoformat()
    }

@app.post("/demo/message")
async def demo_message(request: Dict[str, Any]):
    """Demo message endpoint with comprehensive analysis"""
    try:
        text = request.get("text", "")
        user_id = request.get("user_id", "demo_user")
        
        logger.info(f"👤 Demo message from {user_id}: {text}")
        
        if not text.strip():
            return create_error_response("請輸入要分析的內容")
        
        # Perform comprehensive analysis
        analysis_results = analyze_text_comprehensive(text)
        
        # Return primary result (M1) with additional data
        primary_result = analysis_results.get('m1', create_error_response("分析失敗"))
        primary_result['comprehensive_analysis'] = {
            'm1_available': 'm1' in analysis_results,
            'm2_available': 'm2' in analysis_results,
            'm3_available': 'm3' in analysis_results,
            'total_modules': len(analysis_results)
        }
        
        return primary_result
        
    except Exception as e:
        logger.error(f"Demo message processing failed: {e}")
        return create_error_response("處理訊息時發生錯誤")

@app.post("/demo/comprehensive")
async def comprehensive_analysis(request: Dict[str, Any]):
    """Comprehensive analysis endpoint returning all module results"""
    try:
        text = request.get("text", "")
        user_id = request.get("user_id", "demo_user")
        
        logger.info(f"🔍 Comprehensive analysis for {user_id}: {text}")
        
        if not text.strip():
            return {"error": "請輸入要分析的內容"}
        
        # Perform comprehensive analysis
        analysis_results = analyze_text_comprehensive(text)
        
        return {
            "status": "success",
            "user_input": text,
            "analysis_results": analysis_results,
            "modules_available": {
                "m1": m1_generator is not None,
                "m2": m2_module is not None,
                "m3": m3_module is not None
            }
        }
        
    except Exception as e:
        logger.error(f"Comprehensive analysis failed: {e}")
        return {"error": "綜合分析失敗"}

@app.get("/info")
async def bot_info():
    """Bot information endpoint"""
    return {
        "name": "Enhanced LINE Bot Demo",
        "version": "4.0.0",
        "description": "Comprehensive dementia analysis with M1, M2, M3 modules",
        "features": [
            "M1: Warning Signs Analysis",
            "M2: Progression Stage Assessment", 
            "M3: BPSD Classification",
            "Flex Message Visualization",
            "Comprehensive Analysis"
        ],
        "modules": {
            "m1": "available" if m1_generator else "unavailable",
            "m2": "available" if m2_module else "unavailable",
            "m3": "available" if m3_module else "unavailable"
        }
    }

@app.get("/ping")
async def ping():
    """Simple ping endpoint"""
    return {"pong": datetime.now().isoformat()}

@app.post("/test")
async def test_endpoint():
    """Test endpoint"""
    try:
        test_text = "媽媽最近常忘記關瓦斯，情緒也不太穩定"
        analysis_results = analyze_text_comprehensive(test_text)
        
        return {
            "status": "success",
            "test_results": {
                "m1_test": analysis_results.get('m1', {"error": "M1 test failed"}),
                "m2_test": analysis_results.get('m2', {"error": "M2 test failed"}),
                "m3_test": analysis_results.get('m3', {"error": "M3 test failed"})
            }
        }
    except Exception as e:
        logger.error(f"Test endpoint failed: {e}")
        return {"error": "測試失敗"}

@app.get("/demo")
async def demo_page():
    """Demo page HTML"""
    return {
        "message": "Enhanced Demo Available",
        "endpoints": {
            "health": "/health",
            "demo_message": "/demo/message",
            "comprehensive": "/demo/comprehensive",
            "test": "/test",
            "info": "/info"
        },
        "usage": "Send POST requests to /demo/message or /demo/comprehensive with JSON body containing 'text' and 'user_id'"
    }

if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting Enhanced LINE Bot Demo with M1+M2+M3 integration...")
    print("💡 This is a demo mode - no LINE credentials required")
    print("🌐 Access demo at: http://localhost:8000/demo")
    print("🔍 Comprehensive analysis at: http://localhost:8000/demo/comprehensive")
    uvicorn.run(app, host="0.0.0.0", port=8000) 