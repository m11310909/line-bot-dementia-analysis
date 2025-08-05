# 🔧 LINE Bot Troubleshooting Checklist

**Date:** 2025-08-05  
**System:** LINE Bot Dementia Analysis  
**Status:** Ready for troubleshooting

## 1. ✅ Verify Webhook Registration

```bash
# Check if LINE can reach your webhook
curl -X POST https://[your-ngrok-url]/webhook \
  -H "Content-Type: application/json" \
  -d '{"test": "connection"}'
```

**Expected:** Should receive a response (even if it's an error about signature)

## 2. ✅ Check LINE Channel Settings

- [ ] Channel access token is valid and matches `.env` file
- [ ] Channel secret is correct in `.env` file  
- [ ] Webhook is enabled in LINE Developer Console
- [ ] Auto-reply messages are disabled
- [ ] Greeting messages are disabled (if testing basic replies)

## 3. ✅ Verify Process Logs

```bash
# Check webhook server logs for incoming requests
# If using systemd:
journalctl -u webhook -f

# If using pm2:
pm2 logs webhook

# Or check the console where you started the server
# Look for incoming POST requests to /webhook
```

## 4. ✅ Test Individual Components

### Test 1: Verify webhook receives LINE events
```bash
# Check logs when sending a message to the bot
# Expected: POST request to /webhook with LINE event data
```

### Test 2: Manually test the flow
```bash
# Simulate what happens when a message is received
curl -X POST http://localhost:8005/analyze/M1 \
  -H "Content-Type: application/json" \
  -d '{
    "text": "爸爸不會用洗衣機",
    "user_context": {"user_level": "general"}
  }'
```

**Expected Response:**
```json
{
  "flex_message": {
    "type": "flex",
    "altText": "Dementia Analysis",
    "contents": {
      "type": "bubble",
      "body": {
        "type": "box",
        "contents": [
          {
            "type": "text",
            "text": "失智症分析結果",
            "weight": "bold",
            "size": "lg"
          }
        ]
      }
    }
  }
}
```

## 5. ✅ Common Issues & Solutions

### Issue: "Invalid signature" errors
**Solution:** Ensure `LINE_CHANNEL_SECRET` in `.env` matches Developer Console

### Issue: No logs when sending messages
**Solution:**
- Verify webhook URL is exactly: `https://[ngrok-url]/webhook`
- Check ngrok is still running (URLs change on restart)
- Ensure no typos in the webhook URL

### Issue: Bot receives message but doesn't reply
**Solution:** Check if:
- RAG API is returning valid Flex Message format
- LINE SDK is properly sending the reply
- No errors in parsing the response

### Issue: "Connection refused" errors
**Solution:** Ensure both services are running:

```bash
# Check ports
netstat -tlnp | grep -E '8005|8081'

# Restart services if needed
# For webhook server
python3 updated_line_bot_webhook.py

# For RAG API  
python3 enhanced_m1_m2_m3_m4_integrated_api.py
```

## 6. ✅ Debug Mode Testing

Add verbose logging to your webhook handler:

```python
# In your webhook handler (updated_line_bot_webhook.py)
@app.post("/webhook")
async def webhook_handler(request: Request):
    print("=== Incoming Webhook ===")
    print("Headers:", dict(request.headers))
    
    body = await request.body()
    print("Body:", body.decode())
    
    # Your existing code...
```

## 7. ✅ Final Verification Steps

1. **Send "測試" to your LINE bot**
2. **Check webhook logs for incoming POST request**
3. **Verify RAG API receives the request**
4. **Check for the API response**
5. **Verify LINE bot sends the reply**

## 📊 Expected Flow

```
User sends message → LINE Platform
LINE Platform → Webhook (POST /webhook)
Webhook → RAG API (POST /analyze/M1)
RAG API → Returns Flex Message
Webhook → LINE Reply API
User receives Flex Message
```

If any step fails, check the logs for that specific component.

## 🛠️ Quick Diagnostic Commands

```bash
# 1. Check system status
python3 line_bot_validator.py

# 2. Get current webhook URL
python3 get_webhook_url.py

# 3. Monitor real-time activity
./line_bot_monitor.sh

# 4. Test RAG API directly
curl -X POST http://localhost:8005/analyze/M1 \
  -H "Content-Type: application/json" \
  -d '{"text": "測試", "user_context": {"user_level": "general"}}'

# 5. Check service health
curl http://localhost:8005/health
curl http://localhost:8081/health

# 6. Verify environment variables
python3 -c "
from dotenv import load_dotenv
import os
load_dotenv()
print('LINE_CHANNEL_ACCESS_TOKEN:', 'SET' if os.getenv('LINE_CHANNEL_ACCESS_TOKEN') else 'NOT SET')
print('LINE_CHANNEL_SECRET:', 'SET' if os.getenv('LINE_CHANNEL_SECRET') else 'NOT SET')
print('GOOGLE_GEMINI_API_KEY:', 'SET' if os.getenv('GOOGLE_GEMINI_API_KEY') else 'NOT SET')
"
```

## 🎯 Test Messages

Send these messages to your bot to test different scenarios:

1. **"測試"** - Basic functionality test
2. **"爸爸不會用洗衣機"** - M1 module test
3. **"媽媽中度失智"** - M2 module test  
4. **"爺爺有妄想症狀"** - M3 module test

## 📋 Troubleshooting Checklist

- [ ] All services running (RAG API, Webhook, ngrok)
- [ ] Environment variables loaded correctly
- [ ] Webhook URL updated in LINE Developer Console
- [ ] Webhook enabled in LINE Developer Console
- [ ] No conflicting processes
- [ ] Network connectivity (ngrok tunnel active)
- [ ] API endpoints responding correctly
- [ ] Flex Message format valid
- [ ] LINE SDK properly configured

## 🚨 Emergency Fixes

If the system stops responding:

```bash
# 1. Kill all processes
pkill -f python3
pkill -f ngrok

# 2. Restart services
python3 enhanced_m1_m2_m3_m4_integrated_api.py &
python3 updated_line_bot_webhook.py &
ngrok http 8081 &

# 3. Verify
sleep 5
python3 line_bot_validator.py
```

**Remember:** The system is now fully operational. Most issues can be resolved by following this checklist step by step. 