const ERROR_CODES = require('../schemas/error-codes.json').ERROR_CODES;

class ResponseHandler {
  static success(module, data, metadata = {}) {
    return {
      status: 'success',
      timestamp: new Date().toISOString(),
      module: module,
      version: 'v1.0.0',
      data: data,
      metadata: {
        processing_time: Date.now() % 1000, // Mock 處理時間
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

module.exports = {
  success: (module, data, meta = {}) => ({
    status: 'success',
    module,
    data,
    meta
  }),
  error: (module, code, message = 'Invalid input') => ({
    status: 'error',
    module,
    error: {
      code,
      message
    }
  })
};
module.exports = {
  success: (module, data, meta = {}) => ({
    status: 'success',
    module,
    data,
    meta
  }),
  error: (module, code, message = 'Invalid input') => ({
    status: 'error',
    module,
    error: {
      code,
      message
    }
  })
};
