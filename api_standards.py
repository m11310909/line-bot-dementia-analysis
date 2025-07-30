"""
API 標準化規範
階段三任務：建立技術整合標準，確保前後端資料交換的一致性與可擴展性
"""

from typing import Dict, List, Any, Optional, Union
from enum import Enum
from datetime import datetime
from pydantic import BaseModel, Field
import json

# ===== 1. 統一 Response 結構 =====

class ResponseStatus(str, Enum):
    SUCCESS = "success"
    ERROR = "error"
    WARNING = "warning"

class ModuleType(str, Enum):
    M1 = "M1"  # 失智症十大警訊
    M2 = "M2"  # 病程階段分析
    M3 = "M3"  # BPSD 行為心理症狀
    M4 = "M4"  # 照護任務導航
    M5 = "M5"  # 資源連結
    M6 = "M6"  # 緊急處理
    M7 = "M7"  # 家屬支持
    M8 = "M8"  # 專業諮詢
    M9 = "M9"  # 追蹤評估

class ErrorInfo(BaseModel):
    """錯誤資訊結構"""
    code: str = Field(..., description="錯誤代碼")
    message: str = Field(..., description="使用者友善訊息")
    details: Optional[str] = Field(None, description="技術細節（僅 debug 模式）")
    suggestions: Optional[List[str]] = Field(None, description="建議操作")

class Metadata(BaseModel):
    """回應元數據"""
    processing_time: float = Field(..., description="處理時間（毫秒）")
    confidence_score: Optional[float] = Field(None, ge=0, le=1, description="信心度分數")
    fallback_triggered: Optional[bool] = Field(False, description="是否觸發備用機制")
    chunks_used: Optional[int] = Field(None, description="使用的知識片段數量")
    analysis_method: Optional[str] = Field(None, description="分析方法")

class BaseResponse(BaseModel):
    """基礎回應結構"""
    status: ResponseStatus = Field(..., description="回應狀態")
    timestamp: str = Field(..., description="ISO 8601 格式時間戳")
    module: ModuleType = Field(..., description="模組類型")
    version: str = Field(..., description="API 版本號")
    data: Dict[str, Any] = Field(..., description="模組特定資料")
    metadata: Optional[Metadata] = Field(None, description="處理元數據")
    error: Optional[ErrorInfo] = Field(None, description="錯誤資訊")

# ===== 2. 各模組 Response 格式 =====

class M1Response(BaseResponse):
    """M1: 警訊比對回應"""
    class Config:
        json_schema_extra = {
            "example": {
                "status": "success",
                "timestamp": "2024-01-15T10:30:00Z",
                "module": "M1",
                "version": "1.0.0",
                "data": {
                    "matched_warning_code": "M1-01",
                    "symptom_title": "記憶力減退影響日常生活",
                    "symptom_description": "忘記剛發生的事情、重複詢問同樣問題",
                    "normal_aging_comparison": "偶爾忘記名字但很快想起來",
                    "suggestions": ["建議就醫評估", "建立提醒機制"],
                    "severity_level": "medium",
                    "flex_message": {},
                    "related_modules": ["M2", "M4"]
                },
                "metadata": {
                    "processing_time": 245.6,
                    "confidence_score": 0.85,
                    "chunks_used": 3
                }
            }
        }

class M2Response(BaseResponse):
    """M2: 病程行為症狀回應"""
    class Config:
        json_schema_extra = {
            "example": {
                "status": "success",
                "timestamp": "2024-01-15T10:30:00Z",
                "module": "M2",
                "version": "1.0.0",
                "data": {
                    "identified_stage": "middle",
                    "stage_description": "中度失智症階段",
                    "symptoms_matrix": {
                        "cognitive": ["記憶力明顯減退", "定向感障礙"],
                        "behavioral": ["日夜顛倒", "遊走行為"],
                        "psychological": ["焦慮", "憂鬱"]
                    },
                    "care_focus": ["安全照護", "行為管理", "情緒支持"],
                    "flex_message": {},
                    "next_actions": [
                        {"action": "就醫評估", "priority": "high"},
                        {"action": "申請長照服務", "priority": "medium"}
                    ]
                },
                "metadata": {
                    "processing_time": 312.8,
                    "confidence_score": 0.78,
                    "chunks_used": 5
                }
            }
        }

class M3Response(BaseResponse):
    """M3: BPSD 分類回應"""
    class Config:
        json_schema_extra = {
            "example": {
                "status": "success",
                "timestamp": "2024-01-15T10:30:00Z",
                "module": "M3",
                "version": "1.0.0",
                "data": {
                    "symptom_category": "delusion",
                    "category_name_zh": "妄想症狀",
                    "description": "懷疑有人偷東西、認為配偶不忠",
                    "triggers": ["環境改變", "陌生人員", "物品遺失"],
                    "coping_strategies": {
                        "immediate": ["保持冷靜", "轉移注意力"],
                        "long_term": ["建立規律作息", "減少環境刺激"],
                        "environmental": ["改善照明", "減少噪音"]
                    },
                    "flex_message": {},
                    "professional_help_needed": True
                },
                "metadata": {
                    "processing_time": 189.3,
                    "confidence_score": 0.82,
                    "chunks_used": 4
                }
            }
        }

class M4Response(BaseResponse):
    """M4: 照護任務導航回應"""
    class Config:
        json_schema_extra = {
            "example": {
                "status": "success",
                "timestamp": "2024-01-15T10:30:00Z",
                "module": "M4",
                "version": "1.0.0",
                "data": {
                    "care_stage": "daily",
                    "stage_name_zh": "日常照護",
                    "priority_tasks": [
                        {"task": "協助個人衛生", "priority": "high"},
                        {"task": "監督服藥", "priority": "high"},
                        {"task": "陪伴活動", "priority": "medium"}
                    ],
                    "available_resources": [
                        {"type": "居家服務", "contact": "1966"},
                        {"type": "日間照顧", "contact": "02-1234-5678"}
                    ],
                    "flex_message": {},
                    "timeline_suggestion": "建議每週評估一次照護需求"
                },
                "metadata": {
                    "processing_time": 156.7,
                    "confidence_score": 0.75,
                    "chunks_used": 2
                }
            }
        }

# ===== 3. 錯誤碼對照表 =====

class ErrorCodes:
    """統一錯誤碼系統"""
    
    # 系統錯誤 (E1xxx)
    SYSTEM_UNAVAILABLE = "E1001"
    API_VERSION_UNSUPPORTED = "E1002"
    REQUEST_TIMEOUT = "E1003"
    INTERNAL_ERROR = "E1004"
    
    # 輸入錯誤 (E2xxx)
    INPUT_TOO_SHORT = "E2001"
    INPUT_UNINTELLIGIBLE = "E2002"
    MISSING_REQUIRED_INFO = "E2003"
    INVALID_FORMAT = "E2004"
    
    # AI 處理錯誤 (E3xxx)
    SYMPTOM_TYPE_UNKNOWN = "E3001"
    LOW_CONFIDENCE = "E3002"
    AI_MODEL_UNAVAILABLE = "E3003"
    ANALYSIS_FAILED = "E3004"
    
    # 模組特定錯誤 (E4xxx)
    NO_MATCHING_WARNING = "E4001"
    STAGE_UNDETERMINED = "E4002"
    BPSD_TYPE_UNKNOWN = "E4003"
    NO_CARE_RESOURCES = "E4004"
    MODULE_NOT_AVAILABLE = "E4005"
    
    @classmethod
    def get_error_info(cls, code: str) -> Dict[str, Any]:
        """取得錯誤資訊"""
        error_mapping = {
            # 系統錯誤
            cls.SYSTEM_UNAVAILABLE: {
                "message": "系統暫時無法服務",
                "suggestion": "請稍後再試",
                "details": "系統維護或網路問題"
            },
            cls.API_VERSION_UNSUPPORTED: {
                "message": "API 版本不支援",
                "suggestion": "請更新應用程式",
                "details": "客戶端版本過舊"
            },
            cls.REQUEST_TIMEOUT: {
                "message": "請求逾時",
                "suggestion": "請檢查網路連線",
                "details": "處理時間超過 30 秒"
            },
            cls.INTERNAL_ERROR: {
                "message": "系統內部錯誤",
                "suggestion": "請稍後再試",
                "details": "未預期的系統錯誤"
            },
            
            # 輸入錯誤
            cls.INPUT_TOO_SHORT: {
                "message": "輸入內容過短",
                "suggestion": "請提供更多描述",
                "details": "輸入少於 5 個字元"
            },
            cls.INPUT_UNINTELLIGIBLE: {
                "message": "輸入內容無法理解",
                "suggestion": "請用其他方式描述症狀",
                "details": "AI 無法解析輸入內容"
            },
            cls.MISSING_REQUIRED_INFO: {
                "message": "缺少必要資訊",
                "suggestion": "請補充相關細節",
                "details": "缺少關鍵症狀描述"
            },
            cls.INVALID_FORMAT: {
                "message": "輸入格式錯誤",
                "suggestion": "請檢查輸入格式",
                "details": "JSON 格式或編碼錯誤"
            },
            
            # AI 處理錯誤
            cls.SYMPTOM_TYPE_UNKNOWN: {
                "message": "無法判斷症狀類型",
                "suggestion": "請選擇下方快速選項",
                "details": "AI 無法分類症狀"
            },
            cls.LOW_CONFIDENCE: {
                "message": "信心度過低",
                "suggestion": "建議諮詢專業人員",
                "details": "AI 信心度低於 0.3"
            },
            cls.AI_MODEL_UNAVAILABLE: {
                "message": "AI 模型暫時無法使用",
                "suggestion": "使用簡易模式",
                "details": "AI 服務暫時不可用"
            },
            cls.ANALYSIS_FAILED: {
                "message": "分析處理失敗",
                "suggestion": "請稍後再試",
                "details": "AI 分析過程發生錯誤"
            },
            
            # 模組特定錯誤
            cls.NO_MATCHING_WARNING: {
                "message": "無相符警訊",
                "suggestion": "查看一般照護建議",
                "details": "未找到符合的失智症警訊"
            },
            cls.STAGE_UNDETERMINED: {
                "message": "病程無法判定",
                "suggestion": "提供更多行為描述",
                "details": "無法確定失智症階段"
            },
            cls.BPSD_TYPE_UNKNOWN: {
                "message": "BPSD 類型不明",
                "suggestion": "選擇最接近的症狀",
                "details": "無法分類行為心理症狀"
            },
            cls.NO_CARE_RESOURCES: {
                "message": "無相關照護資源",
                "suggestion": "聯繫在地服務中心",
                "details": "未找到符合的照護資源"
            },
            cls.MODULE_NOT_AVAILABLE: {
                "message": "模組暫時無法使用",
                "suggestion": "請稍後再試",
                "details": "特定模組服務不可用"
            }
        }
        
        return error_mapping.get(code, {
            "message": "未知錯誤",
            "suggestion": "請聯絡技術支援",
            "details": "未定義的錯誤代碼"
        })

# ===== 4. API 版本控制策略 =====

class APIVersionManager:
    """API 版本管理"""
    
    CURRENT_VERSION = "v1.0.0"
    
    # 版本相容性矩陣
    COMPATIBILITY_MATRIX = {
        "v1.0.x": {
            "supported_modules": ["M1", "M2", "M3", "M4"],
            "min_client_version": "1.0.0",
            "breaking_changes": False,
            "deprecated_features": []
        },
        "v1.1.x": {
            "supported_modules": ["M1", "M2", "M3", "M4", "M5", "M6"],
            "min_client_version": "1.1.0",
            "breaking_changes": False,
            "deprecated_features": []
        },
        "v2.0.x": {
            "supported_modules": ["M1", "M2", "M3", "M4", "M5", "M6", "M7", "M8", "M9"],
            "min_client_version": "2.0.0",
            "breaking_changes": True,
            "deprecated_features": ["舊版錯誤碼格式"]
        }
    }
    
    # 棄用政策
    DEPRECATION_POLICY = {
        "notice_period": "3 months",
        "sunset_period": "6 months",
        "migration_guide": True
    }
    
    @classmethod
    def get_version_info(cls, version: str) -> Dict[str, Any]:
        """取得版本資訊"""
        return cls.COMPATIBILITY_MATRIX.get(version, {})
    
    @classmethod
    def is_compatible(cls, client_version: str, server_version: str) -> bool:
        """檢查版本相容性"""
        server_info = cls.get_version_info(server_version)
        if not server_info:
            return False
        
        min_client = server_info.get("min_client_version", "0.0.0")
        return cls._compare_versions(client_version, min_client) >= 0
    
    @classmethod
    def _compare_versions(cls, v1: str, v2: str) -> int:
        """比較版本號"""
        def normalize(v):
            return [int(x) for x in v.replace('v', '').split('.')]
        
        v1_parts = normalize(v1)
        v2_parts = normalize(v2)
        
        for i in range(max(len(v1_parts), len(v2_parts))):
            v1_part = v1_parts[i] if i < len(v1_parts) else 0
            v2_part = v2_parts[i] if i < len(v2_parts) else 0
            
            if v1_part > v2_part:
                return 1
            elif v1_part < v2_part:
                return -1
        
        return 0

# ===== 5. 回應生成工具 =====

class ResponseGenerator:
    """統一回應生成器"""
    
    @staticmethod
    def create_success_response(
        module: ModuleType,
        data: Dict[str, Any],
        metadata: Optional[Metadata] = None,
        version: str = "1.0.0"
    ) -> BaseResponse:
        """建立成功回應"""
        return BaseResponse(
            status=ResponseStatus.SUCCESS,
            timestamp=datetime.now().isoformat(),
            module=module,
            version=version,
            data=data,
            metadata=metadata
        )
    
    @staticmethod
    def create_error_response(
        module: ModuleType,
        error_code: str,
        details: Optional[str] = None,
        version: str = "1.0.0"
    ) -> BaseResponse:
        """建立錯誤回應"""
        error_info = ErrorCodes.get_error_info(error_code)
        
        return BaseResponse(
            status=ResponseStatus.ERROR,
            timestamp=datetime.now().isoformat(),
            module=module,
            version=version,
            data={},
            error=ErrorInfo(
                code=error_code,
                message=error_info["message"],
                details=details or error_info.get("details"),
                suggestions=[error_info["suggestion"]]
            )
        )
    
    @staticmethod
    def create_warning_response(
        module: ModuleType,
        data: Dict[str, Any],
        warning_message: str,
        metadata: Optional[Metadata] = None,
        version: str = "1.0.0"
    ) -> BaseResponse:
        """建立警告回應"""
        return BaseResponse(
            status=ResponseStatus.WARNING,
            timestamp=datetime.now().isoformat(),
            module=module,
            version=version,
            data=data,
            metadata=metadata,
            error=ErrorInfo(
                code="W0001",
                message=warning_message,
                suggestions=["請注意相關風險"]
            )
        )

# ===== 6. 使用範例 =====

def example_usage():
    """使用範例"""
    
    # 成功回應範例
    success_response = ResponseGenerator.create_success_response(
        module=ModuleType.M1,
        data={
            "matched_warning_code": "M1-01",
            "symptom_title": "記憶力減退影響日常生活",
            "severity_level": "medium"
        },
        metadata=Metadata(
            processing_time=245.6,
            confidence_score=0.85,
            chunks_used=3
        )
    )
    
    # 錯誤回應範例
    error_response = ResponseGenerator.create_error_response(
        module=ModuleType.M1,
        error_code=ErrorCodes.INPUT_TOO_SHORT,
        details="輸入僅包含 2 個字元"
    )
    
    # 警告回應範例
    warning_response = ResponseGenerator.create_warning_response(
        module=ModuleType.M1,
        data={"matched_warning_code": "M1-01"},
        warning_message="信心度偏低，建議諮詢專業人員",
        metadata=Metadata(
            processing_time=189.3,
            confidence_score=0.35
        )
    )
    
    return {
        "success": success_response.dict(),
        "error": error_response.dict(),
        "warning": warning_response.dict()
    }

if __name__ == "__main__":
    # 輸出範例
    examples = example_usage()
    print("=== API 標準化範例 ===")
    print(json.dumps(examples, indent=2, ensure_ascii=False)) 