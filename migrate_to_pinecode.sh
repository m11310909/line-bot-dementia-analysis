#!/bin/bash
echo "📦 準備搬移到 Pinecode..."

# 建立精簡版本目錄
mkdir -p pinecode_version/{backend,frontend_static,docs}

echo "🔧 處理後端文件..."
# 複製後端核心文件（排除 venv 和 __pycache__）
rsync -av --exclude='venv' --exclude='__pycache__' --exclude='*.pyc' \
    backend/ pinecode_version/backend/

echo "🎨 處理前端文件..."
# 只複製前端源碼，不複製 node_modules
rsync -av --exclude='node_modules' --exclude='build' --exclude='.git' \
    frontend/ pinecode_version/frontend_static/

# 建立 Pinecode 專用的 requirements.txt
cat > pinecode_version/backend/requirements_pinecode.txt << 'REQS'
fastapi==0.104.1
uvicorn==0.24.0
pydantic==2.5.0
python-multipart==0.0.6
httpx==0.25.0
pytest==7.4.3
pytest-asyncio==0.21.1
python-dotenv==1.0.0
loguru==0.7.2
REQS

echo "📋 建立 Pinecode 安裝腳本..."
cat > pinecode_version/setup_pinecode.sh << 'SETUP'
#!/bin/bash
echo "🚀 在 Pinecode 中設置 FlexComponent 系統"

# 安裝 Python 依賴（無虛擬環境）
echo "📦 安裝 Python 套件..."
pip install --user -r backend/requirements_pinecode.txt

# 建立必要目錄
mkdir -p logs temp

# 測試安裝
echo "🧪 測試環境..."
python3 << 'TEST'
try:
    import fastapi, uvicorn, pydantic
    print("✅ 核心套件安裝成功")
except ImportError as e:
    print(f"❌ 套件安裝失敗: {e}")
TEST

echo "✅ Pinecode 環境設置完成！"
echo "🚀 執行: python backend/main.py"
SETUP

chmod +x pinecode_version/setup_pinecode.sh

echo "📦 建立部署包..."
tar -czf flex_component_pinecode.tar.gz pinecode_version/

echo "✅ 搬移包準備完成: flex_component_pinecode.tar.gz"
