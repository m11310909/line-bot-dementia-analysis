# 🧠 LINE Bot Dementia Analysis - Testing Guide

## ✅ **Current System Status**

### **Infrastructure**
- **✅ ngrok Tunnel**: `https://9d189967bd36.ngrok-free.app`
- **✅ Webhook Server**: Running on port 8081
- **✅ LINE Bot Credentials**: Configured in `.env`
- **✅ RAG API**: All modules active (M1, M2, M3, M4)

### **Test Results**
- **✅ Health Check**: Server healthy
- **✅ RAG Status**: All modules active
- **✅ Webhook Endpoint**: Responding correctly

## 🚀 **How to Test the Bot**

### **Step 1: Update LINE Developer Console**

1. Go to [LINE Developer Console](https://developers.line.biz/)
2. Select your bot channel
3. Go to **Messaging API** settings
4. Update the **Webhook URL** to:
   ```
   https://9d189967bd36.ngrok-free.app/webhook
   ```
5. Enable **Use webhook**
6. Save the changes

### **Step 2: Add Bot as Friend**

1. Get your bot's QR code from LINE Developer Console
2. Scan the QR code with your LINE app
3. Add the bot as a friend

### **Step 3: Test Messages**

Send these test messages to your bot:

#### **Memory Issues (M1 Module)**
```
我媽媽最近經常忘記事情，會重複問同樣的問題
```

#### **Behavior Changes (M2 Module)**
```
我爸爸最近變得比較容易生氣，而且睡眠時間變得不規律
```

#### **Navigation Problems (M3 Module)**
```
我爺爺最近在熟悉的地方也會迷路，這正常嗎？
```

#### **Care Navigation (M4 Module)**
```
我奶奶最近不太愛說話，而且對以前喜歡的活動失去興趣
```

#### **Financial Issues**
```
我媽媽最近在處理金錢方面有困難，她以前很會理財的
```

## 📊 **Expected Responses**

The bot should respond with:
- **Flex Messages** with visual analysis
- **Confidence scores** for each assessment
- **Detailed explanations** of findings
- **Recommendations** for next steps

## 🔧 **Troubleshooting**

### **If Bot Doesn't Respond**
1. Check if ngrok is still running: `lsof -i :8081`
2. Restart ngrok if needed: `ngrok http 8081`
3. Verify webhook URL in LINE Developer Console
4. Check server logs for errors

### **If RAG API is Down**
1. Check if RAG API is running on port 8005
2. Restart the RAG API service if needed
3. Verify environment variables

### **If ngrok URL Changes**
1. Get new URL: `curl -s http://localhost:4040/api/tunnels | python3 -m json.tool`
2. Update LINE Developer Console webhook URL
3. Update `ngrok_url.txt` file

## 📱 **Monitoring**

### **Check Server Status**
```bash
curl https://9d189967bd36.ngrok-free.app/health
```

### **Check RAG API Status**
```bash
curl https://9d189967bd36.ngrok-free.app/rag-status
```

### **View Server Logs**
The server logs will show:
- Incoming messages
- RAG API calls
- Response generation
- Any errors

## 🎯 **Success Criteria**

✅ **Bot responds to messages**
✅ **Flex messages display correctly**
✅ **Dementia analysis provides insights**
✅ **Confidence scores are shown**
✅ **Recommendations are provided**

## 📞 **Support**

If you encounter issues:
1. Check the server logs
2. Verify all services are running
3. Test individual endpoints
4. Restart services if needed

---

**Last Updated**: 2025-08-01 22:40
**Current ngrok URL**: `https://9d189967bd36.ngrok-free.app`
**Webhook URL**: `https://9d189967bd36.ngrok-free.app/webhook` 