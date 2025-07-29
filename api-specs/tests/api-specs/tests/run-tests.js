const fs = require('fs');
const path = require('path');
const ResponseHandler = require('../mocks/response-handler');

console.log('🧪 開始執行 API 格式測試...\n');

// 測試成功回應格式
console.log('✅ 測試成功回應格式:');
const successResponse = ResponseHandler.success('M1', {
  matched_warning_code: 'M1-01',
  symptom_title: '記憶力明顯衰退',
  severity_level: 'high'
});
console.log(JSON.stringify(successResponse, null, 2));

console.log('\n❌ 測試錯誤回應格式:');
const errorResponse = ResponseHandler.error('M1', 'E2001', '輸入: "忘記"');
console.log(JSON.stringify(errorResponse, null, 2));

// 載入並測試所有測試案例
const testFiles = ['m1-test-cases.json', 'm2-test-cases.json', 'm3-test-cases.json'];

testFiles.forEach(file => {
  try {
    const testData = JSON.parse(fs.readFileSync(path.join(__dirname, file), 'utf8'));
    console.log(`\n📊 ${testData.module} 模組測試案例:`);
    testData.test_cases.forEach(testCase => {
      console.log(`- ${testCase.id}: ${testCase.input.slice(0, 30)}...`);
      if (testCase.expected_code) {
        console.log(`  期望: ${testCase.expected_code} (${testCase.expected_severity})`);
      } else if (testCase.expected_stage) {
        console.log(`  期望: ${testCase.expected_stage} 階段`);
      } else if (testCase.expected_category) {
        console.log(`  期望: ${testCase.expected_category} 類型`);
      }
    });
  } catch (err) {
    console.error(`❌ 無法載入 ${file}:`, err.message);
  }
});

console.log('\n🎉 所有格式測試完成！');
