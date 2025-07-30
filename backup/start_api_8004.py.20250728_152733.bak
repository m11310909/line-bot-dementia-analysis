import sys
import os

# 修改原始文件使用端口 8004
with open('integrated_m1_m2_api.py', 'r') as f:
    content = f.read()

# 替換端口
content = content.replace('port=8003', 'port=8004')
content = content.replace('port=8002', 'port=8004')

# 寫入新文件
with open('integrated_m1_m2_api_8004.py', 'w') as f:
    f.write(content)

print("✅ 已創建使用端口 8004 的 API 文件")
