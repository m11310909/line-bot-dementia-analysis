const path = require('path');
const fs = require('fs');

// 讀取錯誤碼
const errorCodesPath = path.join(__dirname, '../schemas/error-codes.json');
const ERROR_CODES = JSON.parse(fs.readFileSync(errorCodesPath, 'utf8')).ERROR_CODES;

class ResponseHandler {
  static success(module, data, metadata = {}) {
    return {
      status: 'success',
      timestamp: new Date().toISOString(),
      module: module,
      version: 'v1.0.0',
      data: data,
      metadata: {
        processing_time: Math.floor(Math.random() * 1000) + 100,
        ...metadata
      }
    };
  }

  static error(module, errorCode, details = null) {
    const errorInfo = ERROR_CODES[errorCode] || ERROR_CODES['E1001'];
    
    return {
      status: 'error',
      timestamp: new Date().toISOString(),
      module: module,
      version: 'v1.0.0',
      data: null,
      error: {
        code: errorCode,
        message: errorInfo.message,
        details: details,
        suggestions: [errorInfo.suggestion]
      }
    };
  }
}

module.exports = ResponseHandler;
