# 🔍 WEBHOOK TROUBLESHOOTING CHECKLIST

**Current Webhook URL:** `https://a3527fa7720b.ngrok-free.app/webhook`  
**Date:** 2025-08-05 16:14

## ✅ **1. Check ngrok is Running**

### Step 1: Verify ngrok tunnel
```bash
# Check if ngrok is running
ps aux | grep ngrok

# Check ngrok tunnel status
curl -s http://localhost:4040/api/tunnels | python3 -c "
import json, sys
data = json.load(sys.stdin)
if data.get('tunnels'):
    print(f'✅ ngrok tunnel: {data[\"tunnels\"][0][\"public_url\"]}')
else:
    print('❌ No ngrok tunnels found')
"
```

### Step 2: If ngrok is not running, start it:
```bash
# Kill any existing ngrok processes
pkill -f ngrok

# Start ngrok
ngrok http 8081
```

**Expected Result:** Should show a URL like `https://abc123.ngrok-free.app`

---

## ✅ **2. Check LINE Developer Console Settings**

### Step 1: Go to LINE Developer Console
- **URL:** https://developers.line.biz/
- **Login** with your account

### Step 2: Select Your Bot
- Click on your bot name
- Go to **"Messaging API"** section

### Step 3: Check Webhook URL
- **Webhook URL:** Should be exactly `https://a3527fa7720b.ngrok-free.app/webhook`
- **Use webhook:** Should be **enabled** (toggle ON)
- **Verify:** Click "Verify" button - should show "Success"

### Step 4: Check Bot Status
- **Bot Status:** Should be "Published" (not "Development")
- **QR Code:** Should be available for adding friends

---

## ✅ **3. Check Bot Friend Status**

### Step 1: Add Bot as Friend
- **Scan QR code** from LINE Developer Console
- **Add the bot as a friend** in your LINE app
- **Send a test message** like "測試"

### Step 2: Check Bot Response
- **Expected:** Bot should reply with a welcome message
- **If no reply:** Continue to next checks

---

## ✅ **4. Test Webhook Connectivity**

### Step 1: Test from External Network
```bash
# Test if webhook is reachable from internet
curl -X POST https://a3527fa7720b.ngrok-free.app/webhook \
  -H "Content-Type: application/json" \
  -d '{"test": "connection"}'
```

### Step 2: Check Webhook Logs
```bash
# Monitor webhook logs in real-time
tail -f webhook.log
```

**Then send a message to your bot and watch the logs.**

---

## ✅ **5. Check Firewall/Network Issues**

### Step 1: Test Local Connectivity
```bash
# Test if webhook server is responding locally
curl -X POST http://localhost:8081/test-webhook \
  -H "Content-Type: application/json" \
  -d '{"text": "測試"}'
```

### Step 2: Test ngrok Tunnel
```bash
# Test if ngrok tunnel is working
curl -s http://localhost:4040/api/tunnels
```

---

## ✅ **6. Verify Bot Credentials**

### Step 1: Check Environment Variables
```bash
# Verify LINE credentials are set
grep "LINE_CHANNEL" .env
```

### Step 2: Test Bot API
```bash
# Test if bot can send messages
python3 -c "
import os
from dotenv import load_dotenv
load_dotenv()
token = os.getenv('LINE_CHANNEL_ACCESS_TOKEN')
print(f'Token length: {len(token) if token else 0}')
print(f'Token valid: {bool(token and len(token) > 50)}')
"
```

---

## ✅ **7. Monitor Real-time Activity**

### Step 1: Start Monitoring
```bash
# Monitor all services
python3 quick_diagnostic.py

# Monitor webhook logs
tail -f webhook.log

# Monitor ngrok requests
curl -s http://localhost:4040/api/requests | python3 -c "
import json, sys
data = json.load(sys.stdin)
print(f'Recent requests: {len(data.get(\"requests\", []))}')
"
```

### Step 2: Send Test Message
- **Send:** "爸爸不會用洗衣機" to your bot
- **Watch:** The logs for any activity
- **Expected:** Should see webhook request in logs

---

## 🚨 **Common Issues & Solutions**

### Issue 1: "Invalid signature" in logs
- **Cause:** LINE signature verification failing
- **Solution:** Check LINE_CHANNEL_SECRET in .env file

### Issue 2: No webhook requests in logs
- **Cause:** LINE not reaching your webhook
- **Solution:** Check webhook URL in LINE Developer Console

### Issue 3: ngrok tunnel not working
- **Cause:** ngrok process stopped or URL changed
- **Solution:** Restart ngrok and update webhook URL

### Issue 4: Bot not responding
- **Cause:** Bot not published or not added as friend
- **Solution:** Publish bot and add as friend

---

## 📊 **Quick Status Check**

Run this command to get current status:
```bash
python3 quick_diagnostic.py
```

**Expected Output:**
- ✅ All services operational
- ✅ ngrok tunnel active
- ✅ Webhook URL: `https://a3527fa7720b.ngrok-free.app/webhook`

---

## 🎯 **Final Verification**

1. **ngrok is running** ✅
2. **Webhook URL is correct** ✅
3. **Bot is published** ✅
4. **Bot is added as friend** ✅
5. **Send test message** ✅
6. **Check logs for activity** ✅

**If all steps pass but still no reply, the issue is likely:**
- LINE Developer Console webhook URL not updated
- ngrok URL changed and not updated in console
- Bot permissions or friend status

---

## 📞 **Next Steps**

If you still have issues after checking all items:

1. **Restart all services:**
   ```bash
   pkill -f python3 && pkill -f ngrok
   ngrok http 8081 &
   python3 enhanced_m1_m2_m3_m4_integrated_api.py > rag_api.log 2>&1 &
   python3 updated_line_bot_webhook.py > webhook.log 2>&1 &
   ```

2. **Update webhook URL in LINE Developer Console**

3. **Test with simple message:** "測試" 