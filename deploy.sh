#!/bin/bash
# deploy.sh

echo "🚀 開始部署失智症照護機器人..."

# 檢查必要檔案
if [ ! -f "templates/m2_carousel.json" ]; then
  echo "❌ M2 樣板檔案缺失"
  exit 1
fi

if [ ! -f "templates/m3_bubble.json" ]; then
  echo "❌ M3 樣板檔案缺失"
  exit 1
fi

if [ ! -f "templates/m4_carousel.json" ]; then
  echo "❌ M4 樣板檔案缺失"
  exit 1
fi

# 安裝依賴套件
npm install

# 驗證 JSON 格式
echo "📋 驗證 JSON 格式..."
node -e "
  const fs = require('fs');
  const templates = ['m2_carousel', 'm3_bubble', 'm4_carousel'];
  templates.forEach(template => {
    try {
      JSON.parse(fs.readFileSync(\`templates/\${template}.json\`, 'utf8'));
      console.log(\`✅ \${template}.json 格式正確\`);
    } catch (error) {
      console.error(\`❌ \${template}.json 格式錯誤:\`, error.message);
      process.exit(1);
    }
  });
"

# 啟動服務
echo "🎉 部署完成！啟動服務..."
npm start