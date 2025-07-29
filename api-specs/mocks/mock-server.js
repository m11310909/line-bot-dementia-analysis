const express = require('express');
const ResponseHandler = require('./response-handler');
const fs = require('fs');
const path = require('path');

const app = express();
app.use(express.json());

// Mock M1 API - 警訊比對
app.post('/api/v1/m1/analyze', (req, res) => {
  const { text } = req.body;
  
  if (!text || text.length < 3) {
    return res.json(ResponseHandler.error('M1', 'E2001'));
  }
  
  let matchedCase = null;
  
  if (text.includes('找東西') || text.includes('偷')) {
    matchedCase = { code: 'M1-07', severity: 'medium', title: '物品擺放混亂與被偷妄想' };
  } else if (text.includes('吃藥') || text.includes('重複')) {
    matchedCase = { code: 'M1-01', severity: 'high', title: '記憶力明顯衰退' };
  } else if (text.includes('手機') || text.includes('不會用')) {
    matchedCase = { code: 'M1-03', severity: 'medium', title: '熟悉事務操作困難' };
  } else {
    return res.json(ResponseHandler.error('M1', 'E4001'));
  }
  
  const responseData = {
    matched_warning_code: matchedCase.code,
    symptom_title: matchedCase.title,
    symptom_description: `檢測到 ${matchedCase.title} 相關症狀`,
    severity_level: matchedCase.severity,
    suggestions: ['建議觀察記錄', '適時給予協助', '必要時諮詢專業人員'],
    flex_message: { type: 'bubble', body: { type: 'box', layout: 'vertical' } }
  };
  
  res.json(ResponseHandler.success('M1', responseData, { confidence_score: 0.85 }));
});

// Mock M2 API - 病程分析
app.post('/api/v1/m2/analyze', (req, res) => {
  const { text } = req.body;
  
  let stage = 'early';
  let symptoms = ['cognitive'];
  
  if (text.includes('不認得') || text.includes('日夜顛倒')) {
    stage = 'middle';
    symptoms = ['behavioral', 'cognitive'];
  } else if (text.includes('無法進食') || text.includes('全天候照護')) {
    stage = 'late';
    symptoms = ['behavioral', 'cognitive', 'psychological'];
  }
  
  const responseData = {
    identified_stage: stage,
    stage_description: `已識別為${stage === 'early' ? '早期' : stage === 'middle' ? '中期' : '晚期'}階段`,
    symptoms_matrix: {
      cognitive: stage !== 'early' ? ['記憶困難', '認知下降'] : ['輕微健忘'],
      behavioral: symptoms.includes('behavioral') ? ['行為改變', '睡眠問題'] : [],
      psychological: symptoms.includes('psychological') ? ['情緒不穩'] : []
    },
    care_focus: ['日常協助', '安全環境', '情感支持']
  };
  
  res.json(ResponseHandler.success('M2', responseData, { confidence_score: 0.78 }));
});

// Mock M3 API - BPSD 分類
app.post('/api/v1/m3/analyze', (req, res) => {
  const { text } = req.body;
  
  let category = 'anxiety';
  let categoryZh = '焦慮症狀';
  
  if (text.includes('害她') || text.includes('妄想')) {
    category = 'delusion';
    categoryZh = '妄想症狀';
  } else if (text.includes('暴躁') || text.includes('發脾氣')) {
    category = 'agitation';
    categoryZh = '激動行為';
  } else if (text.includes('沮喪') || text.includes('不想做')) {
    category = 'depression';
    categoryZh = '憂鬱情緒';
  }
  
  const responseData = {
    symptom_category: category,
    category_name_zh: categoryZh,
    description: `識別出 ${categoryZh} 相關表現`,
    triggers: ['環境變化', '身體不適', '溝通困難'],
    coping_strategies: {
      immediate: ['保持冷靜', '溫和回應'],
      long_term: ['建立規律', '專業諮詢'],
      environmental: ['安全空間', '減少刺激']
    },
    professional_help_needed: category === 'delusion'
  };
  
  res.json(ResponseHandler.success('M3', responseData, { confidence_score: 0.82 }));
});

// 健康檢查
app.get('/api/health', (req, res) => {
  res.json(ResponseHandler.success('SYSTEM', { 
    status: 'healthy',
    uptime: process.uptime(),
    version: 'v1.0.0',
    modules: ['M1', 'M2', 'M3']
  }));
});

const PORT = process.env.PORT || 3001;
app.listen(PORT, () => {
  console.log(`🚀 Mock API Server 運行在 http://localhost:${PORT}`);
  console.log('📝 可用端點:');
  console.log('  POST /api/v1/m1/analyze - M1 警訊比對');
  console.log('  POST /api/v1/m2/analyze - M2 病程分析');
  console.log('  POST /api/v1/m3/analyze - M3 BPSD 分類');
  console.log('  GET  /api/health - 健康檢查');
});
