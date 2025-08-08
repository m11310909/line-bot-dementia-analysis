# 🚀 LINE Bot Real Testing Setup Guide

## ✅ **Current System Status**
Your LINE Bot Dementia Analysis System is running and ready for real testing!

## 📋 **Step-by-Step Setup Instructions**

### **Step 1: Get Your LINE Bot Credentials**

1. **Go to LINE Developer Console**: https://developers.line.biz/
2. **Create a new channel** or use existing one
3. **Get your credentials**:
   - Channel Access Token
   - Channel Secret

### **Step 2: Update Environment Variables**

Update your `.env` file with your actual LINE Bot credentials:

```bash
# LINE Bot Configuration
LINE_CHANNEL_ACCESS_TOKEN=your_actual_channel_access_token_here
LINE_CHANNEL_SECRET=your_actual_channel_secret_here

# External URL (ngrok tunnel)
EXTERNAL_URL=https://6f59006e1132.ngrok-free.app

# Database Configuration
DB_PASSWORD=your_secure_password_here
```

### **Step 3: Configure LINE Developer Console**

1. **Go to your LINE Bot channel** in LINE Developer Console
2. **Set Webhook URL** to: `https://6f59006e1132.ngrok-free.app/webhook`
3. **Enable webhook** in your channel settings
4. **Add webhook events**:
   - `message`
   - `follow`
   - `unfollow`
   - `postback`

### **Step 4: Restart Services with New Configuration**

```bash
# Stop current services
docker-compose down

# Start services with new environment
docker-compose up -d
```

### **Step 5: Test the Webhook**

Test if your webhook is working:

```bash
# Test webhook endpoint
curl -X POST https://6f59006e1132.ngrok-free.app/webhook \
  -H "Content-Type: application/json" \
  -H "X-Line-Signature: test" \
  -d '{"events":[{"type":"message","message":{"type":"text","text":"我最近常常忘記事情"}}]}'
```

## 🔧 **Current System Configuration**

### **✅ Running Services**
- **PostgreSQL**: ✅ Healthy (Port 5432)
- **Redis**: ✅ Healthy (Port 6379)
- **XAI Wrapper**: ✅ Healthy (Port 8005)
- **LINE Bot**: ✅ Healthy (Port 8081)
- **Nginx**: ✅ Running (Port 80)

### **🌐 Public URLs**
- **Webhook URL**: `https://6f59006e1132.ngrok-free.app/webhook`
- **Health Check**: `https://6f59006e1132.ngrok-free.app/health`
- **API Base**: `https://6f59006e1132.ngrok-free.app/api/`

## 🧪 **Testing Commands**

### **1. Health Check**
```bash
curl https://6f59006e1132.ngrok-free.app/health
```

### **2. Test Webhook**
```bash
curl -X POST https://6f59006e1132.ngrok-free.app/webhook \
  -H "Content-Type: application/json" \
  -H "X-Line-Signature: test" \
  -d '{"events":[{"type":"message","message":{"type":"text","text":"我最近常常忘記事情"}}]}'
```

### **3. Test API**
```bash
curl -X POST https://6f59006e1132.ngrok-free.app/api/v1/analyze \
  -H "Content-Type: application/json" \
  -d '{"user_input":"我最近常常忘記事情","user_id":"test_user"}'
```

## 📱 **LINE Bot Features to Test**

### **1. Text Message Analysis**
Send these messages to your LINE Bot:
- "我最近常常忘記事情"
- "爸爸最近變得比較容易生氣"
- "爺爺最近在熟悉的地方也會迷路"
- "奶奶最近不太愛說話"

### **2. Module Navigation**
The bot will automatically detect which analysis module to use:
- **M1**: 警訊徵兆分析 (記憶、忘記、迷路等)
- **M2**: 病程進展評估 (早期、中期、晚期等)
- **M3**: 行為症狀分析 (妄想、幻覺、激動等)
- **M4**: 照護資源導航 (醫生、醫院、照護等)

### **3. Interactive Features**
- **Flex Messages**: Rich interactive responses
- **Postback Actions**: Button-based navigation
- **Knowledge Search**: Access to dementia care resources

## 🔍 **Monitoring and Debugging**

### **View Logs**
```bash
# All services
docker-compose logs -f

# LINE Bot specific
docker-compose logs -f line-bot

# XAI Wrapper specific
docker-compose logs -f xai-wrapper
```

### **Check Service Status**
```bash
docker-compose ps
```

### **Test Individual Services**
```bash
# LINE Bot health
curl http://localhost:8081/health

# XAI Wrapper health
curl http://localhost:8005/health
```

## 🚨 **Troubleshooting**

### **Common Issues**

1. **Webhook Not Receiving Messages**
   - Check if webhook URL is correct in LINE Developer Console
   - Verify ngrok tunnel is active
   - Check LINE Bot logs: `docker-compose logs -f line-bot`

2. **Signature Verification Failed**
   - Ensure Channel Secret is correct in `.env`
   - Check if webhook URL matches exactly

3. **Service Not Responding**
   - Restart services: `docker-compose restart`
   - Check health: `docker-compose ps`

4. **ngrok Tunnel Issues**
   - Restart ngrok: `pkill ngrok && ngrok http 80`
   - Get new URL and update webhook in LINE Developer Console

## 📊 **Expected Behavior**

### **When User Sends Message**
1. LINE sends webhook to your server
2. Bot analyzes message content
3. Determines appropriate analysis module
4. Calls XAI service for analysis
5. Sends rich Flex Message response

### **Sample Response Flow**
```
User: "我最近常常忘記事情"
↓
Bot detects M1 module (警訊徵兆分析)
↓
Calls XAI analysis service
↓
Sends Flex Message with:
- Analysis results
- Confidence score
- Recommendations
- Interactive buttons
```

## 🎯 **Next Steps**

1. **Update your `.env` file** with real LINE Bot credentials
2. **Configure webhook URL** in LINE Developer Console
3. **Test with your LINE Bot** by sending messages
4. **Monitor logs** for any issues
5. **Fine-tune responses** based on testing results

## 📞 **Support**

If you encounter issues:
1. Check the logs: `docker-compose logs -f`
2. Verify webhook URL is accessible
3. Test individual service health
4. Restart services if needed: `docker-compose restart`

---

**Your LINE Bot is ready for real testing!** 🚀

**Current ngrok URL**: `https://6f59006e1132.ngrok-free.app`  
**Webhook URL**: `https://6f59006e1132.ngrok-free.app/webhook`
