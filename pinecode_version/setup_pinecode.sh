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
