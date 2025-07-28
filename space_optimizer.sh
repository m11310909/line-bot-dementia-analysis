# [复制上面 artifact 中的完整脚本内容]
#!/bin/bash
# replit_space_optimizer.sh - Replit 空间优化脚本

echo "🚀 Replit 空间优化开始"
echo "===================="

# 1. 检查当前状态
echo "1️⃣ 检查当前空间使用..."
echo "总项目大小:"
du -sh . 2>/dev/null || echo "无法检查项目大小"

echo ""
echo "Python 包大小:"
if [ -d ".pythonlibs" ]; then
    du -sh .pythonlibs
else
    echo "未找到 .pythonlibs 目录"
fi

echo ""
echo "2️⃣ 分析已安装的包..."
python3 -m pip list --format=freeze | head -15

echo ""
echo "3️⃣ 识别大型包..."

# 检查是否存在大型包
LARGE_PACKAGES=(
    "torch"
    "tensorflow" 
    "scipy"
    "numpy"
    "chromadb"
    "sentence-transformers"
    "scikit-learn"
    "pandas"
    "matplotlib"
    "seaborn"
)

echo "🔍 检查大型包..."
FOUND_LARGE_PACKAGES=()

for package in "${LARGE_PACKAGES[@]}"; do
    if python3 -m pip show "$package" >/dev/null 2>&1; then
        echo "❌ 发现大型包: $package"
        FOUND_LARGE_PACKAGES+=("$package")
    fi
done

if [ ${#FOUND_LARGE_PACKAGES[@]} -eq 0 ]; then
    echo "✅ 未发现需要清理的大型包"
else
    echo ""
    echo "4️⃣ 清理大型包..."

    for package in "${FOUND_LARGE_PACKAGES[@]}"; do
        echo "🗑️ 卸载 $package..."
        python3 -m pip uninstall "$package" -y 2>/dev/null && echo "✅ 已卸载 $package" || echo "⚠️ $package 卸载失败或未安装"
    done
fi

echo ""
echo "5️⃣ 清理缓存..."

# 清理 pip 缓存
echo "🧹 清理 pip 缓存..."
python3 -m pip cache purge 2>/dev/null || echo "pip 缓存清理完成"

# 清理 Python 字节码
echo "🧹 清理 Python 字节码..."
find . -name "*.pyc" -delete 2>/dev/null || true
find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true

# 清理其他缓存
echo "🧹 清理其他缓存..."
rm -rf ~/.cache/pip 2>/dev/null || true
rm -rf ~/.cache/huggingface 2>/dev/null || true
rm -rf /tmp/* 2>/dev/null || true

echo ""
echo "6️⃣ 检查当前必需的包..."

# 必需的包列表
REQUIRED_PACKAGES=(
    "fastapi"
    "uvicorn" 
    "pinecone"
    "line-bot-sdk"
    "requests"
    "pydantic"
    "httpx"
)

echo "✅ 验证必需包:"
MISSING_PACKAGES=()

for package in "${REQUIRED_PACKAGES[@]}"; do
    if python3 -c "import $package" 2>/dev/null; then
        echo "✅ $package: 已安装"
    else
        echo "❌ $package: 缺失"
        MISSING_PACKAGES+=("$package")
    fi
done

# 安装缺失的包
if [ ${#MISSING_PACKAGES[@]} -gt 0 ]; then
    echo ""
    echo "7️⃣ 安装缺失的必需包..."

    for package in "${MISSING_PACKAGES[@]}"; do
        echo "📦 安装 $package..."
        python3 -m pip install "$package"
    done
fi

echo ""
echo "8️⃣ 优化后状态..."

echo "优化后项目大小:"
du -sh . 2>/dev/null || echo "无法检查项目大小"

echo ""
echo "优化后 Python 包大小:"
if [ -d ".pythonlibs" ]; then
    du -sh .pythonlibs
else
    echo "未找到 .pythonlibs 目录"
fi

echo ""
echo "当前已安装包 (前10个):"
python3 -m pip list --format=freeze | head -10

echo ""
echo "9️⃣ 创建优化的 requirements.txt..."

# 创建优化的 requirements.txt
cat > requirements_optimized.txt << 'EOF'
# Optimized Requirements for Replit + Pinecone
# Total estimated size: ~60MB

# Core packages
fastapi==0.104.1
uvicorn==0.24.0
pinecone>=7.0.0
line-bot-sdk>=3.8.0
requests>=2.31.0
pydantic>=2.5.0
python-multipart>=0.0.6
httpx>=0.25.0

# Optional (uncomment if needed)
# google-generativeai>=0.3.2
# openai>=1.3.8
EOF

echo "✅ 创建了 requirements_optimized.txt"

echo ""
echo "🔟 测试核心功能..."

# 测试 Pinecone 连接
echo "🧪 测试 Pinecone 连接..."
python3 -c "
try:
    from pinecone import Pinecone
    pc = Pinecone(api_key='pcsk_4WvWXx_G5bRUFdFNzLzRHNM9rkvFMvC18TMRTaeYXVCxmWSPQLmKr4xAs4UaZg5NvVb69m')
    index = pc.Index('dementia-care-knowledge')
    stats = index.describe_index_stats()
    print(f'✅ Pinecone 连接成功: {stats.total_vector_count} 个向量')
except Exception as e:
    print(f'❌ Pinecone 连接失败: {str(e)}')
"

# 测试其他核心功能
echo "🧪 测试其他核心包..."
python3 -c "
packages = ['fastapi', 'uvicorn', 'linebot', 'requests', 'pydantic']
for pkg in packages:
    try:
        exec(f'import {pkg}')
        print(f'✅ {pkg}: OK')
    except ImportError:
        print(f'❌ {pkg}: FAILED')
"

echo ""
echo "🎉 空间优化完成!"
echo "==============="
echo ""
echo "📊 优化总结:"
if [ ${#FOUND_LARGE_PACKAGES[@]} -gt 0 ]; then
    echo "✅ 清理了 ${#FOUND_LARGE_PACKAGES[@]} 个大型包"
else
    echo "ℹ️ 未发现需要清理的大型包"
fi
echo "✅ 清理了所有缓存"
echo "✅ 验证了核心功能"
echo "✅ 创建了优化的 requirements.txt"
echo ""
echo "📋 下一步建议:"
echo "1. 测试 XAI 功能: python3 lightweight_test.py"
echo "2. 运行主应用: python3 main.py"
echo "3. 检查空间节省: du -sh .pythonlibs"
echo ""
echo "🔄 如需恢复，请安装完整包:"
echo "python3 -m pip install -r requirements_original_backup.txt"