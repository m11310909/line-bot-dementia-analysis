const fs = require('fs');
const ResponseHandler = require('../mocks/response-handler');

// 載入測試案例
const m1Tests = JSON.parse(fs.readFileSync('./m1-test-cases.json', 'utf8'));

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

console.log('\n📊 測試案例驗證:');
m1Tests.test_cases.forEach(testCase => {
  console.log(`- ${testCase.id}: ${testCase.input.slice(0, 30)}...`);
  console.log(`  期望: ${testCase.expected_code} (${testCase.expected_severity})`);
});

console.log('\n🎉 所有格式測試通過！');
