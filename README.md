# LINE Bot Dementia Analysis System

## 🚀 Quick Start

### 1. Setup Environment
```bash
cp .env.example .env
# Edit .env with your credentials
```

### 2. Start Services
```bash
./start.sh
```

### 3. Configure LINE Webhook
Set your webhook URL to: `https://your-domain.com/webhook`

### 4. Test System
```bash
python test_system.py
```

## 📁 Project Structure
```
.
├── services/
│   ├── line-bot/          # LINE Bot service
│   └── xai-wrapper/        # XAI analysis service
├── data/                   # Data storage
├── logs/                   # Application logs
├── docker-compose.yml      # Docker configuration
├── .env                    # Environment variables
└── README.md              # This file
```

## 🛠️ Available Commands
- `./start.sh` - Start all services
- `./stop.sh` - Stop all services
- `./logs.sh [service]` - View logs
- `python test_system.py` - Run tests

## 📊 Modules
- **M1**: Warning Signs Detection (警訊比對)
- **M2**: Disease Progression (病程評估)
- **M3**: BPSD Symptoms (行為症狀)
- **M4**: Care Navigation (任務導航)

## 🔧 Development
```bash
# Install dependencies locally for development
pip install -r services/xai-wrapper/requirements.txt
pip install -r services/line-bot/requirements.txt

# Run services locally
uvicorn services.xai-wrapper.app.main:app --reload --port 8005
python services/line-bot/app/main.py
```

## 📝 API Documentation
- XAI Analysis: `POST /api/v1/analyze`
- Health Check: `GET /health`

## 🐛 Troubleshooting
1. Check logs: `./logs.sh [service-name]`
2. Verify health: `curl http://localhost:8005/health`
3. Test webhook: Use LINE Developer Console

## 📄 License
MIT
