#!/usr/bin/env python3
"""
測試環境變數讀取
"""

import os
from dotenv import load_dotenv

def test_env_loading():
    """測試環境變數載入"""
    print("🔍 測試環境變數載入...")
    
    # 檢查 .env 檔案
    if os.path.exists('.env'):
        print("✅ .env 檔案存在")
        
        # 讀取 .env 檔案內容
        with open('.env', 'r') as f:
            content = f.read()
            print(f"檔案大小: {len(content)} bytes")
            
            # 檢查關鍵變數
            lines = content.split('\n')
            for line in lines:
                if line.strip() and not line.startswith('#'):
                    if '=' in line:
                        key = line.split('=')[0].strip()
                        value = line.split('=', 1)[1].strip()
                        if value.startswith('your_actual_'):
                            print(f"❌ {key} = {value[:20]}... (未設置)")
                        else:
                            print(f"✅ {key} = {value[:20]}...")
    else:
        print("❌ .env 檔案不存在")
        return False
    
    # 載入環境變數
    print("\n📝 載入環境變數...")
    load_dotenv()
    
    # 檢查關鍵環境變數
    env_vars = {
        'LINE_CHANNEL_ACCESS_TOKEN': os.getenv('LINE_CHANNEL_ACCESS_TOKEN'),
        'LINE_CHANNEL_SECRET': os.getenv('LINE_CHANNEL_SECRET'),
        'AISTUDIO_API_KEY': os.getenv('AISTUDIO_API_KEY'),
        'GEMINI_MODEL': os.getenv('GEMINI_MODEL'),
        'REDIS_URL': os.getenv('REDIS_URL')
    }
    
    print("\n🔍 檢查環境變數值:")
    for var_name, var_value in env_vars.items():
        if var_value:
            if var_value.startswith('your_actual_'):
                print(f"❌ {var_name}: 未正確設置")
            else:
                print(f"✅ {var_name}: 已設置 ({var_value[:10]}...)")
        else:
            print(f"❌ {var_name}: 未設置")
    
    return True

def create_sample_env():
    """創建範例 .env 檔案"""
    print("\n📝 創建範例 .env 檔案...")
    
    sample_content = """# LINE Bot 憑證配置
LINE_CHANNEL_ACCESS_TOKEN=your_actual_channel_access_token_here
LINE_CHANNEL_SECRET=your_actual_channel_secret_here

# API 配置
FLEX_API_URL=http://localhost:8005/comprehensive-analysis
RAG_HEALTH_URL=http://localhost:8005/health
RAG_ANALYZE_URL=http://localhost:8005/comprehensive-analysis

# 生產環境配置
ENVIRONMENT=production
LOG_LEVEL=INFO
DEBUG_MODE=false

# Redis 配置
REDIS_URL=redis://localhost:6379
REDIS_PASSWORD=
REDIS_DB=0

# Gemini API 配置
AISTUDIO_API_KEY=your_actual_gemini_api_key_here
GEMINI_MODEL=gemini-1.5-flash
GEMINI_MAX_TOKENS=1000

# 監控配置
ENABLE_MONITORING=true
ENABLE_LOGGING=true
ENABLE_METRICS=true
"""
    
    with open('.env', 'w') as f:
        f.write(sample_content)
    
    print("✅ .env 檔案已創建")
    print("⚠️  請編輯 .env 檔案並填入實際的憑證")

def main():
    """主函數"""
    print("🧪 環境變數測試")
    print("=" * 50)
    
    # 測試環境變數載入
    if not test_env_loading():
        print("\n❌ 環境變數載入失敗")
        print("正在創建範例 .env 檔案...")
        create_sample_env()
        return
    
    print("\n" + "=" * 50)
    print("🎯 環境變數測試完成！")
    print("\n📋 下一步：")
    print("1. 編輯 .env 檔案並填入實際憑證")
    print("2. 重新執行此腳本驗證")
    print("3. 啟動 API: python3 enhanced_m1_m2_m3_integrated_api.py")

if __name__ == "__main__":
    main() 