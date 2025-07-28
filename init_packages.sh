#!/usr/bin/env bash
# init_packages.sh
# 在每個子目錄下建立 __init__.py（如果尚不存在的話）

BASE_DIR="api"

echo ">>> 為 $BASE_DIR 下所有資料夾建立 __init__.py …"

find "$BASE_DIR" -type d | while read dir; do
  init_file="$dir/__init__.py"
  if [ ! -f "$init_file" ]; then
    touch "$init_file"
    echo "# Package marker for Python" >> "$init_file"
    echo "  → 建立 $init_file"
  fi
done

echo ">>> 完成！"
