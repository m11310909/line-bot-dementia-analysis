# 🚀 Quick Start Guide - Test Your LINE Bot

## ✅ **System is Ready!**

Your LINE Bot dementia analysis system is fully operational:

- **✅ ngrok Tunnel**: `https://9d189967bd36.ngrok-free.app`
- **✅ Webhook Server**: Running and responding
- **✅ LINE Bot Credentials**: Configured
- **✅ RAG API**: All modules active

## 📱 **Step-by-Step Testing**

### **1. Update LINE Developer Console**

1. Go to [LINE Developer Console](https://developers.line.biz/)
2. Select your bot channel
3. Go to **Messaging API** settings
4. Set **Webhook URL** to:
   ```
   https://9d189967bd36.ngrok-free.app/webhook
   ```
5. **Enable** "Use webhook"
6. Click **Save**

### **2. Add Bot as Friend**

1. In LINE Developer Console, go to **Messaging API**
2. Copy the **QR Code** or **Bot ID**
3. Open your LINE app
4. Add the bot as a friend using the QR code or bot ID

### **3. Test with Real Messages**

Send these messages to your bot:

#### **Test 1: Memory Issues**
```
我媽媽最近經常忘記事情，會重複問同樣的問題
```

#### **Test 2: Behavior Changes**
```
我爸爸最近變得比較容易生氣，而且睡眠時間變得不規律
```

#### **Test 3: Navigation Problems**
```
我爺爺最近在熟悉的地方也會迷路，這正常嗎？
```

#### **Test 4: Care Navigation**
```
我奶奶最近不太愛說話，而且對以前喜歡的活動失去興趣
```

## 🎯 **What You Should See**

The bot will respond with:
- **Rich Flex Messages** with visual analysis
- **Confidence scores** for each assessment
- **Detailed explanations** of findings
- **Actionable recommendations**

## 🔧 **If Bot Doesn't Respond**

1. **Check ngrok status**:
   ```bash
   curl https://9d189967bd36.ngrok-free.app/health
   ```

2. **Verify webhook URL** in LINE Developer Console

3. **Check server logs** for incoming messages

## 📊 **Monitor System Status**

### **Health Check**
```bash
curl https://9d189967bd36.ngrok-free.app/health
```

### **RAG API Status**
```bash
curl https://9d189967bd36.ngrok-free.app/rag-status
```

## 🎉 **Success Indicators**

✅ **Bot responds to your messages**
✅ **Flex messages display correctly**
✅ **Dementia analysis provides insights**
✅ **Confidence scores are shown**
✅ **Recommendations are provided**

---

**Current ngrok URL**: `https://9d189967bd36.ngrok-free.app`
**Webhook URL**: `https://9d189967bd36.ngrok-free.app/webhook`
**Status**: Ready for testing! 🚀 