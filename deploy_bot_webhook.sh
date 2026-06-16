#!/bin/bash

# 社交媒体机器人 Webhook 服务部署脚本

set -e

echo "🤖 开始部署机器人 Webhook 服务..."

# 检查 Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 未安装"
    exit 1
fi

# 进入 python-engine 目录
cd "$(dirname "$0")/python-engine"

# 创建虚拟环境（如果不存在）
if [ ! -d "venv" ]; then
    echo "📦 创建虚拟环境..."
    python3 -m venv venv
fi

# 激活虚拟环境
echo "🔧 激活虚拟环境..."
source venv/bin/activate

# 安装/更新依赖
echo "📥 安装依赖..."
pip install --upgrade pip
pip install fastapi uvicorn httpx python-multipart

# 检查是否已有进程运行
if [ -f "bot_webhook.pid" ]; then
    OLD_PID=$(cat bot_webhook.pid)
    if ps -p $OLD_PID > /dev/null 2>&1; then
        echo "🛑 停止旧进程 (PID: $OLD_PID)..."
        kill $OLD_PID
        sleep 2
    fi
    rm bot_webhook.pid
fi

# 启动服务
echo "🚀 启动 Webhook 服务..."
nohup python bot_webhook.py > bot_webhook.log 2>&1 &
echo $! > bot_webhook.pid

echo "✅ 部署完成！"
echo ""
echo "📊 服务状态:"
echo "   - PID: $(cat bot_webhook.pid)"
echo "   - 日志: $(pwd)/bot_webhook.log"
echo "   - 端口: 8001"
echo ""
echo "🔍 查看日志:"
echo "   tail -f bot_webhook.log"
echo ""
echo "🛑 停止服务:"
echo "   kill $(cat bot_webhook.pid)"
echo ""
echo "📝 下一步:"
echo "   1. 使用 ngrok 或部署到服务器暴露服务"
echo "   2. 配置各平台的 Webhook URL"
echo "   3. 测试机器人对话功能"
