# test_rag.py - 直接測試用
import os

# 檢查環境
print("🔍 檢查環境...")
print(f"當前目錄: {os.getcwd()}")
print(f"檔案列表: {os.listdir('.')}")

# 檢查 enhanced 目錄
if os.path.exists('enhanced'):
   print(f"Enhanced 目錄內容: {os.listdir('enhanced')}")
else:
   print("❌ Enhanced 目錄不存在")

# 檢查 API Key
api_key = os.getenv('AISTUDIO_API_KEY')
print(f"API Key: {'已設定' if api_key else '❌ 未設定'}")

# 簡單測試
print("\n🧪 簡單功能測試...")
test_text = "媽媽常忘記關瓦斯"
print(f"測試文本: {test_text}")

# 基本中文分詞測試
import re
chinese_chars = re.findall(r'[\u4e00-\u9fff]+', test_text)
print(f"中文提取: {chinese_chars}")

print("✅ 基本功能正常")