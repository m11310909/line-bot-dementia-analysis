#!/usr/bin/env python3
"""
LINE Bot Startup Script - M1 Enhanced
Handles environment setup and bot startup
"""

import os
import sys
import subprocess
import time
import requests
from pathlib import Path

def check_environment():
    """Check if required environment variables are set"""
    print("🔍 Checking environment...")
    
    required_vars = ['LINE_CHANNEL_ACCESS_TOKEN', 'LINE_CHANNEL_SECRET']
    missing_vars = []
    
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print(f"❌ Missing environment variables: {missing_vars}")
        print("💡 Please set them in your environment or .env file")
        return False
    
    print("✅ Environment variables found")
    return True

def check_dependencies():
    """Check if required Python packages are installed"""
    print("🔍 Checking dependencies...")
    
    required_packages = [
        'fastapi',
        'uvicorn',
        'linebot',
        'requests',
        'pyyaml'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print(f"❌ Missing packages: {missing_packages}")
        print("💡 Installing missing packages...")
        
        try:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install'] + missing_packages)
            print("✅ Dependencies installed")
        except subprocess.CalledProcessError:
            print("❌ Failed to install dependencies")
            return False
    
    print("✅ All dependencies available")
    return True

def test_m1_modules():
    """Test M1 visualization modules"""
    print("🔍 Testing M1 modules...")
    
    try:
        from xai_flex.m1_enhanced_visualization import M1EnhancedVisualizationGenerator
        from test_m1_simple import test_m1_visualization
        
        print("✅ M1 modules imported successfully")
        
        # Run a quick test
        print("🧪 Running M1 test...")
        test_m1_visualization()
        print("✅ M1 test completed")
        return True
        
    except ImportError as e:
        print(f"⚠️ M1 modules not available: {e}")
        print("💡 Will use fallback mode")
        return False
    except Exception as e:
        print(f"❌ M1 test failed: {e}")
        return False

def start_rag_api():
    """Start the RAG API if not running"""
    print("🔍 Checking RAG API...")
    
    try:
        response = requests.get('http://localhost:8002/health', timeout=5)
        if response.status_code == 200:
            print("✅ RAG API is running")
            return True
    except:
        pass
    
    print("⚠️ RAG API not running")
    print("💡 You may need to start the RAG API separately")
    return False

def start_line_bot():
    """Start the LINE bot"""
    print("🚀 Starting LINE Bot with M1 integration...")
    
    try:
        # Start the bot
        subprocess.run([
            sys.executable, 'line_bot_m1_integrated.py'
        ], check=True)
    except KeyboardInterrupt:
        print("\n⏹️ Bot stopped by user")
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to start bot: {e}")
        return False
    
    return True

def create_env_template():
    """Create .env template if it doesn't exist"""
    env_file = Path('.env')
    if not env_file.exists():
        print("📝 Creating .env template...")
        
        template = """# LINE Bot Configuration
LINE_CHANNEL_ACCESS_TOKEN=your_channel_access_token_here
LINE_CHANNEL_SECRET=your_channel_secret_here

# Optional: RAG API Configuration
RAG_API_URL=http://localhost:8002
"""
        
        with open('.env', 'w') as f:
            f.write(template)
        
        print("✅ .env template created")
        print("💡 Please edit .env with your LINE Bot credentials")

def load_env_file():
    """Load environment variables from .env file"""
    env_file = Path('.env')
    if env_file.exists():
        print("📝 Loading .env file...")
        
        with open('.env', 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    os.environ[key] = value
        
        print("✅ Environment variables loaded from .env")

def main():
    """Main startup function"""
    print("🧠 LINE Bot M1 Enhanced - Startup")
    print("=" * 50)
    
    # Load environment
    load_env_file()
    
    # Check environment
    if not check_environment():
        create_env_template()
        print("\n❌ Please set up your environment variables and try again")
        return False
    
    # Check dependencies
    if not check_dependencies():
        print("\n❌ Failed to install dependencies")
        return False
    
    # Test M1 modules
    m1_available = test_m1_modules()
    
    # Check RAG API
    rag_available = start_rag_api()
    
    print("\n📊 Status Summary:")
    print(f"  ✅ Environment: Ready")
    print(f"  ✅ Dependencies: Ready")
    print(f"  {'✅' if m1_available else '⚠️'} M1 Modules: {'Ready' if m1_available else 'Fallback mode'}")
    print(f"  {'✅' if rag_available else '⚠️'} RAG API: {'Ready' if rag_available else 'Not available'}")
    
    if not m1_available and not rag_available:
        print("\n⚠️ Warning: Both M1 modules and RAG API are unavailable")
        print("💡 The bot will run in basic mode with limited functionality")
    
    print("\n🚀 Starting LINE Bot...")
    print("💡 Press Ctrl+C to stop the bot")
    
    # Start the bot
    return start_line_bot()

if __name__ == "__main__":
    try:
        success = main()
        if not success:
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
    except Exception as e:
        print(f"\n❌ Startup failed: {e}")
        sys.exit(1) 