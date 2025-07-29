class LIFFIntegrationService {
  constructor(liffBaseUrl) {
    this.baseUrl = liffBaseUrl;
  }

  generateLIFFUrl(module, params = {}) {
    const urlMap = {
      M2: `${this.baseUrl}/stage-guide`,
      M3: `${this.baseUrl}/bpsd-guide`, 
      M4: `${this.baseUrl}/care-map`
    };

    const baseUrl = urlMap[module];
    if (!baseUrl) return null;

    const queryString = Object.keys(params)
      .map(key => `${key}=${encodeURIComponent(params[key])}`)
      .join('&');

    return queryString ? `${baseUrl}?${queryString}` : baseUrl;
  }

  handleLIFFCallback(module, data) {
    // LIFF 頁面回傳資料處理
    switch(module) {
      case 'M2':
        return this.handleStageGuideCallback(data);
      case 'M3':
        return this.handleBPSDGuideCallback(data);
      case 'M4':
        return this.handleCareMapCallback(data);
      default:
        return null;
    }
  }

  handleStageGuideCallback(data) {
    if (data.action === 'request_care_guidance') {
      return {
        targetModule: 'M4',
        data: { stage: data.currentStage, context: 'from_stage_guide' }
      };
    }
    return null;
  }
}