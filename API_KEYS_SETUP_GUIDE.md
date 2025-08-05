# 🔑 API Keys Setup Guide

## 📋 Required Environment Variables

You need to create a `.env` file in your project root with the following variables:

```bash
# LINE Bot Configuration
LINE_CHANNEL_ACCESS_TOKEN=your_line_channel_access_token_here
LINE_CHANNEL_SECRET=your_line_channel_secret_here

# Third-Party API Configuration
API_TYPE=openai  # openai, gemini, custom
API_KEY=your_openai_api_key_here
THIRD_PARTY_API_KEY=your_third_party_api_key_here
GOOGLE_GEMINI_API_KEY=your_google_gemini_api_key_here

# RAG API Configuration (if needed)
RAG_API_URL=http://localhost:8005/analyze/M1
RAG_HEALTH_URL=http://localhost:8005/health
```

## 🔧 How to Set Up Your .env File

### **1. Create the .env file:**

```bash
# In your project directory
touch .env
```

### **2. Add your API keys:**

Copy the template above and replace the placeholder values with your actual API keys:

```bash
# LINE Bot Configuration
LINE_CHANNEL_ACCESS_TOKEN=sk-1234567890abcdef...  # Your LINE Channel Access Token
LINE_CHANNEL_SECRET=abcdef1234567890...           # Your LINE Channel Secret

# Third-Party API Configuration
API_TYPE=openai                                    # Choose: openai, gemini, custom
API_KEY=sk-1234567890abcdef...                    # Your OpenAI API Key
THIRD_PARTY_API_KEY=your_custom_api_key_here      # Your Custom API Key
GOOGLE_GEMINI_API_KEY=AIzaSyC...                  # Your Google Gemini API Key
```

## 🎯 API Key Sources

### **1. LINE Bot API Keys:**
- Go to [LINE Developers Console](https://developers.line.biz/)
- Create a new channel or use existing one
- Get your **Channel Access Token** and **Channel Secret**

### **2. OpenAI API Key:**
- Go to [OpenAI Platform](https://platform.openai.com/)
- Sign up or log in
- Go to API Keys section
- Create a new API key
- Copy the key (starts with `sk-`)

### **3. Google Gemini API Key:**
- Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
- Sign in with your Google account
- Create a new API key
- Copy the key (starts with `AIzaSy`)

### **4. Custom Third-Party API Key:**
- Use your own API service
- Get the API key from your service provider
- Update the `CUSTOM_API_CONFIG` in `third_party_api_config.py` if needed

## 🧪 Testing Your API Keys

### **1. Check Health Status:**
```bash
curl http://localhost:8082/health
```

Expected response:
```json
{
  "status": "healthy",
  "service": "Enhanced Third-Party API Webhook",
  "api_type": "openai",
  "api_key_configured": true,
  "openai_configured": true,
  "gemini_configured": true,
  "custom_configured": true,
  "line_bot_configured": true,
  "supported_apis": ["openai", "gemini", "custom"]
}
```

### **2. Test API Functionality:**
```bash
curl -X POST http://localhost:8082/test \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello, how are you?"}'
```

### **3. Switch API Type:**
```bash
# Switch to OpenAI
curl -X POST http://localhost:8082/switch_api \
  -H "Content-Type: application/json" \
  -d '{"api_type": "openai"}'

# Switch to Gemini
curl -X POST http://localhost:8082/switch_api \
  -H "Content-Type: application/json" \
  -d '{"api_type": "gemini"}'

# Switch to Custom
curl -X POST http://localhost:8082/switch_api \
  -H "Content-Type: application/json" \
  -d '{"api_type": "custom"}'
```

## 🔍 API Key Configuration Status

The system will automatically detect which API keys are configured:

- **✅ OpenAI API Key:** Used when `API_TYPE=openai`
- **✅ Google Gemini API Key:** Used when `API_TYPE=gemini`
- **✅ Custom API Key:** Used when `API_TYPE=custom`

## 🚀 Quick Setup Commands

### **1. Create .env file:**
```bash
cp env_template.txt .env
```

### **2. Edit .env file:**
```bash
nano .env
# or
code .env
```

### **3. Start the webhook:**
```bash
python3 enhanced_third_party_api_webhook.py
```

### **4. Test the setup:**
```bash
curl http://localhost:8082/health
```

## 🔒 Security Notes

### **⚠️ Important Security Practices:**

1. **Never commit .env to git:**
   ```bash
   # Add to .gitignore
   echo ".env" >> .gitignore
   ```

2. **Use environment-specific keys:**
   - Development: Use test API keys
   - Production: Use production API keys

3. **Rotate keys regularly:**
   - Change API keys periodically
   - Monitor usage and costs

4. **Limit API permissions:**
   - Use minimal required permissions
   - Set usage limits where possible

## 🎯 API Type Selection

### **Choose your preferred API:**

1. **OpenAI (GPT):**
   ```bash
   API_TYPE=openai
   API_KEY=sk-your-openai-key
   ```

2. **Google Gemini:**
   ```bash
   API_TYPE=gemini
   GOOGLE_GEMINI_API_KEY=AIza-your-gemini-key
   ```

3. **Custom API:**
   ```bash
   API_TYPE=custom
   THIRD_PARTY_API_KEY=your-custom-key
   ```

## 📊 Monitoring API Usage

### **Check API Status:**
```bash
# Health check
curl http://localhost:8082/health

# Test API response
curl -X POST http://localhost:8082/test \
  -H "Content-Type: application/json" \
  -d '{"message": "test"}'
```

### **View Logs:**
```bash
# Webhook logs
tail -f third_party_webhook.log

# ngrok logs
tail -f ngrok_third_party.log
```

## 🎉 Success Criteria

Your setup is complete when:

- ✅ **Health check** shows all API keys configured
- ✅ **Test endpoint** returns successful responses
- ✅ **LINE webhook** receives and processes messages
- ✅ **ngrok tunnel** is active and accessible
- ✅ **No error messages** in logs

## 🚀 Next Steps

1. **Configure your API keys** in `.env`
2. **Test the webhook** with health check
3. **Update LINE Developer Console** with ngrok URL
4. **Send test messages** to your LINE bot
5. **Monitor logs** for any issues

**Your third-party API integration is ready to use!** 🎉 