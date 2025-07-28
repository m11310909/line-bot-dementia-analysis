import subprocess
import sys
import os

def install_requirements():
    """Install required packages"""
    requirements = [
        "fastapi==0.104.1",
        "uvicorn[standard]==0.24.0",
        "google-generativeai==0.3.2",
        "line-bot-sdk==3.8.0",
        "requests==2.31.0",
        "pydantic==2.5.0",
        "python-multipart==0.0.6"
    ]

    print("📦 Installing requirements...")
    for req in requirements:
        print(f"Installing {req}...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", req])

    print("✅ All packages installed!")

def create_env_template():
    """Create .env template file"""
    env_content = """# LINE Bot Credentials
LINE_CHANNEL_ACCESS_TOKEN=your_line_channel_access_token_here
LINE_CHANNEL_SECRET=your_line_channel_secret_here

# Google AI Studio API Key
AISTUDIO_API_KEY=your_google_ai_studio_api_key_here

# Optional: API URLs
FLEX_API_URL=http://localhost:8001/m1-flex
"""

    with open(".env.template", "w", encoding="utf-8") as f:
        f.write(env_content)

    print("📝 Created .env.template file")
    print("📋 Please copy .env.template to .env and fill in your credentials")

def create_start_scripts():
    """Create convenient start scripts"""

    # Windows batch files
    start_flex_bat = """@echo off
echo Starting M1 Flex API...
python m1_flex_api.py
pause
"""

    start_webhook_bat = """@echo off
echo Starting LINE Bot Webhook...
python line_bot_webhook.py
pause
"""

    # Unix shell scripts
    start_flex_sh = """#!/bin/bash
echo "Starting M1 Flex API..."
python3 m1_flex_api.py
"""

    start_webhook_sh = """#!/bin/bash
echo "Starting LINE Bot Webhook..."
python3 line_bot_webhook.py
"""

    # Create Windows scripts
    with open("start_flex.bat", "w") as f:
        f.write(start_flex_bat)

    with open("start_webhook.bat", "w") as f:
        f.write(start_webhook_bat)

    # Create Unix scripts
    with open("start_flex.sh", "w") as f:
        f.write(start_flex_sh)