# Webhook 405 Method Not Allowed Fix

## 🔍 Problem Analysis

The error `09:24:04.691 CST GET /webhook 405 Method Not Allowed` indicates that:

1. **Something is making a GET request** to your `/webhook` endpoint
2. **Your webhook endpoint only accepts POST requests** (which is correct for LINE webhooks)
3. **The server is rejecting GET requests** with a 405 error

## 🎯 Root Causes

This can happen due to:

1. **Browser Access**: Someone accessing the webhook URL directly in a browser
2. **LINE Developer Console**: LINE testing the webhook URL
3. **Health Checks**: Monitoring systems checking the endpoint
4. **Manual Testing**: Developers testing the endpoint manually
5. **Previous Server**: A webhook server that was running and has since stopped

## ✅ Solution Implemented

I've added **GET endpoints** to all major webhook files to handle GET requests gracefully:

### Files Updated:
- `line_bot_webhook_v2.py`
- `services/line-bot/main.py` 
- `enhanced_m1_m2_m3_integrated_api.py`

### New GET Endpoint Response:
```json
{
  "message": "LINE Bot Webhook is running",
  "status": "active", 
  "note": "This endpoint only accepts POST requests from LINE",
  "webhook_url": "POST /webhook",
  "health_check": "GET /health",
  "bot_info": "GET /info"
}
```

## 🚀 How to Start a Webhook Server

### Option 1: Enhanced Integrated API (Recommended)
```bash
python3 enhanced_m1_m2_m3_integrated_api.py
```
- **Port**: 8005
- **Features**: Full M1+M2+M3 analysis with XAI
- **Webhook**: POST /webhook (with GET support)

### Option 2: Simple Webhook Server
```bash
python3 line_bot_webhook_v2.py
```
- **Port**: 8000
- **Features**: Basic LINE webhook with RAG integration
- **Webhook**: POST /webhook (with GET support)

### Option 3: Docker Services
```bash
docker-compose up line-bot
```
- **Port**: 8081
- **Features**: Containerized LINE bot service
- **Webhook**: POST /webhook (with GET support)

## 🔧 Environment Setup

### 1. Create .env file:
```bash
cp env.example .env
```

### 2. Configure LINE Bot credentials:
```env
LINE_CHANNEL_ACCESS_TOKEN=your_line_channel_access_token_here
LINE_CHANNEL_SECRET=your_line_channel_secret_here
```

### 3. Configure external URL (for ngrok):
```env
EXTERNAL_URL=https://your-ngrok-url.ngrok-free.app
```

## 🧪 Testing

### Test GET endpoint:
```bash
python3 test_webhook_get.py
```

### Test POST endpoint (simulate LINE):
```bash
curl -X POST http://localhost:8005/webhook \
  -H "Content-Type: application/json" \
  -H "X-Line-Signature: test" \
  -d '{"events":[]}'
```

## 📊 Expected Behavior

### GET /webhook (New):
- ✅ Returns 200 OK with status information
- ✅ No more 405 errors
- ✅ Helpful response for debugging

### POST /webhook (LINE):
- ✅ Accepts LINE webhook events
- ✅ Validates signatures
- ✅ Processes messages normally

## 🔍 Troubleshooting

### If you still get 405 errors:

1. **Check if server is running**:
   ```bash
   lsof -i :8005
   ```

2. **Check server logs**:
   ```bash
   tail -f logs/webhook.log
   ```

3. **Verify environment variables**:
   ```bash
   python3 -c "import os; print('LINE_CHANNEL_ACCESS_TOKEN:', bool(os.getenv('LINE_CHANNEL_ACCESS_TOKEN')))"
   ```

4. **Test with curl**:
   ```bash
   curl -X GET http://localhost:8005/webhook
   ```

## 🎉 Benefits

- ✅ **No more 405 errors** for GET requests
- ✅ **Better debugging** with informative responses
- ✅ **Maintains security** - POST still required for actual LINE events
- ✅ **Backward compatible** - existing LINE webhook functionality unchanged
- ✅ **Developer friendly** - helpful error messages and status info

## 📝 Notes

- The GET endpoint is **informational only** and doesn't process LINE events
- **Real LINE webhooks** still use POST with proper signatures
- This fix **prevents 405 errors** while maintaining security
- All webhook servers now have **consistent behavior**

## 🔄 Next Steps

1. **Start your preferred webhook server**
2. **Configure LINE Developer Console** with your webhook URL
3. **Test with the provided test script**
4. **Monitor logs** for any issues

The 405 error should now be resolved! 🎉
