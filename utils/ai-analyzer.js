function parseAIResponse(aiResponse) {
  const { matched_warning_code, symptom_title, confidence_score } = aiResponse;

  // 判斷跳轉目標模組
  if (confidence_score < 0.6) {
    return { targetModule: 'FALLBACK', data: aiResponse };
  }

  if (matched_warning_code.includes('stage_')) {
    const stage = extractStageFromCode(matched_warning_code);
    return { 
      targetModule: 'M2', 
      data: { stage, symptom_title, confidence_score }
    };
  }

  if (matched_warning_code.includes('bpsd_')) {
    const bpsdType = extractBPSDType(matched_warning_code);
    return { 
      targetModule: 'M3', 
      data: { bpsdType, symptom_title, confidence_score }
    };
  }

  if (symptom_title.includes('照護') || symptom_title.includes('協助')) {
    return { 
      targetModule: 'M4', 
      data: { careContext: 'general', symptom_title }
    };
  }

  return { targetModule: 'M1', data: aiResponse };
}

// 輔助函數
function extractStageFromCode(code) {
  const stageMap = {
    'stage_early': 'early',
    'stage_middle': 'middle', 
    'stage_late': 'late'
  };
  return stageMap[code] || 'early';
}

function extractBPSDType(code) {
  const typeMap = {
    'bpsd_emotional': 'emotional',
    'bpsd_behavioral': 'behavioral',
    'bpsd_cognitive': 'cognitive'
  };
  return typeMap[code] || 'emotional';
}