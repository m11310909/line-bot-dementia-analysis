#!/usr/bin/env bash
set -e

echo ">>> 移除所有 Python 檔案的行尾空白"
find api/ -type f -name '*.py' -exec sed -i 's/[ \t]\+$//' {} \;

echo ">>> 用 isort 自動修正 import 排序"
python3 -m isort --profile black api/

echo ">>> 用 Black 格式化並限制行長為 100 字元"
python3 -m black --line-length 100 api/

echo ">>> 用 autoflake 移除未使用的 imports"
python3 -m autoflake --remove-all-unused-imports --in-place --recursive api/

echo ">>> 自動化格式化完成，請再跑一次 pylint 檢查結果"

