// 基礎回應結構
export interface BaseResponse {
  status: 'success' | 'error' | 'warning';
  timestamp: string;  // ISO 8601 格式
  module: 'M1' | 'M2' | 'M3' | 'M4' | 'M5' | 'M6' | 'M7' | 'M8' | 'M9';
  version: string;    // API 版本號
  data: any;          // 模組特定資料
  metadata?: {
    processing_time: number;  // 毫秒
    confidence_score?: number; // 0-1
    fallback_triggered?: boolean;
  };
  error?: ErrorInfo;
}

export interface ErrorInfo {
  code: string;       // 錯誤代碼
  message: string;    // 使用者友善訊息
  details?: string;   // 技術細節（僅 debug 模式）
  suggestions?: string[]; // 建議操作
}
