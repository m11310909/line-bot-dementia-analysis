# 🚀 Gemini Flex LIFF Complete Flow Setup

## 📋 Overview

This guide sets up the complete flow: **LINE → Webhook → Third Party API (小幫手) → Gemini → Visualization (Flex Message + LIFF) → LINE**

## 🎯 Complete Flow Architecture

```
📱 LINE User
    ↓
🔗 Webhook (Port 8083)
    ↓
🤖 Third Party API (小幫手)
    ↓
🧠 Google Gemini AI
    ↓
🎨 Flex Message + LIFF
    ↓
📱 LINE Response
```

## 🔧 Setup Instructions

### **1. Environment Configuration**

Create a `.env` file with the following variables:

```bash
# LINE Bot Configuration
LINE_CHANNEL_ACCESS_TOKEN=your_line_channel_access_token_here
LINE_CHANNEL_SECRET=your_line_channel_secret_here

# Google Gemini API
GOOGLE_GEMINI_API_KEY=your_google_gemini_api_key_here

# LIFF Configuration
LIFF_URL=https://your-liff-app.com
```

### **2. Install Dependencies**

```bash
pip install flask line-bot-sdk requests python-dotenv
```

### **3. Start the Webhook Server**

```bash
python3 gemini_flex_liff_webhook.py
```

The server will run on `http://localhost:8083`

### **4. Expose with ngrok**

```bash
ngrok http 8083
```

### **5. Configure LINE Developer Console**

1. Go to your LINE Developer Console
2. Set webhook URL to: `https://your-ngrok-url.ngrok.io/webhook`
3. Enable webhook
4. Save changes

## 🧪 Testing

### **Test the Complete Flow**

```bash
python3 test_gemini_flex_liff_flow.py
```

### **Manual Testing**

1. **Health Check:**
   ```bash
   curl http://localhost:8083/health
   ```

2. **API Test:**
   ```bash
   curl -X POST http://localhost:8083/test \
     -H "Content-Type: application/json" \
     -d '{"message": "爸爸不會用洗衣機"}'
   ```

3. **Service Info:**
   ```bash
   curl http://localhost:8083/
   ```

## 🎨 Features

### **🧠 Enhanced Gemini AI Integration**
- Specialized prompt for 小幫手 (Little Helper) functionality
- Dementia warning sign analysis
- Professional recommendations
- Care reminders

### **🎨 Rich Flex Message Visualization**
- Beautiful bubble container design
- Structured information display
- Interactive buttons
- Professional styling

### **📱 LIFF Integration**
- Detailed analysis reports
- User-specific context
- Professional consultation links
- Enhanced user experience

### **🔗 Complete LINE Ecosystem**
- Real-time message processing
- Seamless user interaction
- Professional response formatting
- Error handling and fallbacks

## 📊 Response Flow

### **1. User Input**
```
User: "爸爸不會用洗衣機"
```

### **2. Gemini Analysis**
```
🧠 小幫手 AI 分析結果

根據您的描述，這可能是失智症的早期警訊：

📋 分析結果：
- 記憶力下降
- 日常生活技能退化
- 需要進一步評估

💡 建議：
- 安排專業醫療評估
- 記錄症狀變化
- 尋求家人支持
```

### **3. Flex Message Response**
- Rich visual presentation
- Interactive buttons
- LIFF integration for detailed reports
- Professional consultation options

## 🔧 Configuration Options

### **Gemini API Settings**
- **Model:** gemini-pro
- **Temperature:** 0.7 (balanced creativity)
- **Max Tokens:** 1000
- **Language:** Traditional Chinese

### **Flex Message Design**
- **Size:** giga (large)
- **Color Scheme:** LINE Green (#1DB446)
- **Layout:** Vertical with footer buttons
- **Interactive Elements:** LIFF integration

### **LIFF Integration**
- **User Context:** User ID and analysis data
- **Detailed Reports:** Full analysis results
- **Professional Consultation:** Doctor bot integration
- **Enhanced UX:** Rich interactive experience

## 🚨 Troubleshooting

### **Common Issues**

1. **Gemini API Error (403/401)**
   - Check API key configuration
   - Verify API key permissions
   - Ensure proper quota allocation

2. **Flex Message Error (400)**
   - Check Flex Message structure
   - Verify component properties
   - Ensure proper layout configuration

3. **LIFF URL Issues**
   - Verify LIFF app configuration
   - Check URL accessibility
   - Ensure proper parameter passing

4. **Webhook Connection Issues**
   - Verify ngrok tunnel status
   - Check LINE Developer Console settings
   - Ensure webhook URL accessibility

### **Debug Commands**

```bash
# Check webhook health
curl http://localhost:8083/health

# Test API functionality
curl -X POST http://localhost:8083/test \
  -H "Content-Type: application/json" \
  -d '{"message": "test"}'

# Check ngrok tunnels
curl http://localhost:4040/api/tunnels
```

## 📈 Performance Optimization

### **Response Time Optimization**
- Efficient Gemini API calls
- Optimized Flex Message creation
- Minimal processing overhead

### **Error Handling**
- Graceful fallbacks to text messages
- Comprehensive error logging
- User-friendly error messages

### **Scalability**
- Stateless webhook design
- Efficient resource usage
- Modular architecture

## 🎉 Success Indicators

### **✅ Working Flow**
1. User sends message to LINE bot
2. Webhook receives and processes message
3. Gemini API analyzes with 小幫手 prompt
4. Flex Message created with LIFF integration
5. Rich response sent back to LINE
6. User receives professional analysis

### **📊 Metrics to Monitor**
- Response time < 3 seconds
- Success rate > 95%
- User engagement with LIFF
- Error rate < 5%

## 🔄 Next Steps

1. **Deploy to Production**
   - Set up proper hosting
   - Configure SSL certificates
   - Implement monitoring

2. **Enhance LIFF App**
   - Create detailed analysis pages
   - Add interactive features
   - Implement user tracking

3. **Scale the Service**
   - Add more AI models
   - Implement caching
   - Add analytics

4. **Professional Integration**
   - Connect with medical professionals
   - Add appointment booking
   - Implement follow-up systems

---

**🎯 Complete Flow Successfully Implemented!**

Your LINE bot now provides:
- ✅ Professional AI analysis
- ✅ Rich visual responses  
- ✅ LIFF integration
- ✅ Complete user experience 