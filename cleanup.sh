#!/bin/bash
echo "清除 pip 快取、Python 暫存與虛擬環境…"
rm -rf ~/.cache/pip
find . -type d -name "__pycache__" -exec rm -rf {} +
rm -rf .cache .venv venv *.log *.out
echo "完成。請重新檢查空間："
du -h --max-depth=1 . | sort -hr | head -n 10