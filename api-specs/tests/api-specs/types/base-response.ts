export interface BaseResponse {
  status: 'success' | 'error' | 'warning';
  timestamp: string;
  module: 'M1' | 'M2' | 'M3' | 'M4' | 'M5' | 'M6' | 'M7' | 'M8' | 'M9';
  version: string;
  data: any;
  metadata?: {
    processing_time: number;
    confidence_score?: number;
    fallback_triggered?: boolean;
  };
  error?: ErrorInfo;
}

export interface ErrorInfo {
  code: string;
  message: string;
  details?: string;
  suggestions?: string[];
}
