# 🔧 Third-Party API Integration Setup Guide

## 📋 Overview

This guide shows how to integrate third-party APIs directly with your LINE bot without visualization modules for testing purposes.

## 🚀 Quick Start

### 1. **Environment Setup**

Add these variables to your `.env` file:

```bash
# LINE Bot Configuration
LINE_CHANNEL_ACCESS_TOKEN=your_line_channel_access_token
LINE_CHANNEL_SECRET=your_line_channel_secret

# Third-Party API Configuration
API_TYPE=openai  # openai, gemini, custom
API_KEY=your_api_key_here
```

### 2. **Start the Webhook Server**

```bash
# Start the enhanced third-party API webhook
python3 enhanced_third_party_api_webhook.py
```

The server will run on `http://localhost:8082`

### 3. **Test the Integration**

```bash
# Run the test script
python3 test_third_party_api_integration.py
```

## 🔧 Supported APIs

### **1. OpenAI API**

**Configuration:**
```bash
API_TYPE=openai
API_KEY=your_openai_api_key
```

**Features:**
- GPT-3.5-turbo model
- Traditional Chinese responses
- 500 token limit
- Temperature: 0.7

### **2. Google Gemini API**

**Configuration:**
```bash
API_TYPE=gemini
API_KEY=your_gemini_api_key
```

**Features:**
- Gemini Pro model
- Traditional Chinese responses
- 500 token limit
- Temperature: 0.7

### **3. Custom API**

**Configuration:**
```bash
API_TYPE=custom
API_KEY=your_custom_api_key
```

**Features:**
- Custom endpoint support
- Flexible response parsing
- Configurable parameters

## 📱 LINE Integration

### **Webhook URL Setup**

1. **Get your webhook URL:**
   ```
   http://localhost:8082/webhook
   ```

2. **Update LINE Developer Console:**
   - Go to LINE Developer Console
   - Set webhook URL to your server
   - Enable webhook

### **Message Flow**

```
User Message → LINE → Webhook → Third-Party API → Response → LINE → User
```

## 🧪 Testing

### **1. Health Check**

```bash
curl http://localhost:8082/health
```

**Expected Response:**
```json
{
  "status": "healthy",
  "service": "Enhanced Third-Party API Webhook",
  "api_type": "openai",
  "line_bot_configured": true,
  "api_key_configured": true,
  "supported_apis": ["openai", "gemini", "custom"]
}
```

### **2. API Test**

```bash
curl -X POST http://localhost:8082/test \
  -H "Content-Type: application/json" \
  -d '{"message": "你好，請介紹一下你自己"}'
```

### **3. Switch API Type**

```bash
curl -X POST http://localhost:8082/switch_api \
  -H "Content-Type: application/json" \
  -d '{"api_type": "gemini"}'
```

## 🔄 API Switching

### **Runtime API Switching**

You can switch APIs during runtime:

```python
import requests

# Switch to OpenAI
response = requests.post("http://localhost:8082/switch_api", 
                       json={"api_type": "openai"})

# Switch to Gemini
response = requests.post("http://localhost:8082/switch_api", 
                       json={"api_type": "gemini"})

# Switch to Custom API
response = requests.post("http://localhost:8082/switch_api", 
                       json={"api_type": "custom"})
```

## 📊 Monitoring

### **Logs**

The webhook server provides detailed logging:

```
INFO:__main__:🔄 Calling openai API: https://api.openai.com/v1/chat/completions
INFO:__main__:📤 Sending message: 你好，請介紹一下你自己...
INFO:__main__:✅ openai API response: 你好！我是一個AI助手...
INFO:__main__:✅ Sent response to user_id: 你好！我是一個AI助手...
```

### **Error Handling**

The system handles various errors gracefully:

- **API Timeout:** Returns timeout message
- **Network Error:** Returns connection error message
- **Invalid Response:** Returns error with details
- **Missing API Key:** Returns configuration error

## 🎯 Benefits

### **✅ Advantages:**

1. **No Visualization Modules:** Direct text responses
2. **Multiple API Support:** Easy switching between APIs
3. **Simple Testing:** Direct API testing without LINE
4. **Error Handling:** Graceful error management
5. **Flexible Configuration:** Easy to customize

### **🔧 Use Cases:**

1. **API Testing:** Test different APIs quickly
2. **Development:** Simple development workflow
3. **Prototyping:** Rapid prototyping without complex UI
4. **Debugging:** Easy to debug API responses

## 🚀 Advanced Configuration

### **Custom API Configuration**

Edit `third_party_api_config.py` to add your custom API:

```python
CUSTOM_API_CONFIG = {
    'url': 'https://your-api-endpoint.com/chat',
    'headers': {
        'Authorization': 'Bearer {api_key}',
        'Content-Type': 'application/json'
    },
    'data_template': {
        'message': '{user_message}',
        'language': 'zh-TW',
        'max_length': 500
    }
}
```

### **Response Parsing**

Add your custom response parser:

```python
def parse_custom_response(response_data):
    """Parse your custom API response"""
    try:
        return response_data.get('response', str(response_data))
    except Exception as e:
        raise Exception(f"Invalid custom API response: {e}")
```

## 🔍 Troubleshooting

### **Common Issues:**

1. **API Key Not Configured:**
   - Check your `.env` file
   - Verify API_KEY is set correctly

2. **Webhook Not Responding:**
   - Check if server is running on port 8082
   - Verify LINE webhook URL is correct

3. **API Errors:**
   - Check API key validity
   - Verify API endpoint is accessible
   - Check network connectivity

### **Debug Commands:**

```bash
# Check server status
curl http://localhost:8082/health

# Test API directly
curl -X POST http://localhost:8082/test \
  -H "Content-Type: application/json" \
  -d '{"message": "test"}'

# Check logs
tail -f webhook.log
```

## 🎉 Conclusion

This setup provides a clean, simple way to integrate third-party APIs with your LINE bot for testing purposes. The system is:

- **Easy to configure**
- **Flexible for different APIs**
- **Simple to test and debug**
- **Ready for production use**

**Your LINE bot is now ready for direct third-party API integration!** 🚀 