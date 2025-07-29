const express = require('express');
const line = require('@line/bot-sdk');
require('dotenv').config();

const app = express();
const port = process.env.PORT || 3000;

// LINE Bot 設定
const config = {
  channelAccessToken: process.env.CHANNEL_ACCESS_TOKEN,
  channelSecret: process.env.CHANNEL_SECRET,
};

const client = new line.Client(config);

// 基本路由
app.get('/', (req, res) => {
  res.send('🤖 失智症照護機器人運行中...');
});

// Webhook 處理
app.post('/callback', line.middleware(config), (req, res) => {
  Promise
    .all(req.body.events.map(handleEvent))
    .then((result) => res.json(result))
    .catch((err) => {
      console.error(err);
      res.status(500).end();
    });
});

// 事件處理函數
function handleEvent(event) {
  if (event.type !== 'message' || event.message.type !== 'text') {
    return Promise.resolve(null);
  }

  // 簡單回應 (之後會整合 AI 和 Flex Message)
  return client.replyMessage(event.replyToken, {
    type: 'text',
    text: `收到您的訊息：${event.message.text}\n\n系統正在準備中...`
  });
}

app.listen(port, () => {
  console.log(`🚀 伺服器運行在 port ${port}`);
});
