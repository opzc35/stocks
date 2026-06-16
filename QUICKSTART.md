# 快速开始指南

## 5分钟快速启动

### 1. 启动Python后端
```bash
cd python-engine
source venv/bin/activate
python main.py
```

服务将在 `http://localhost:8000` 启动

### 2. 验证服务
```bash
# 健康检查
curl http://localhost:8000/health

# 获取实时价格
curl "http://localhost:8000/api/market/ticker?symbol=BTC/USDT"
```

### 3. 同步历史数据
```bash
curl -X POST "http://localhost:8000/api/data/sync" \
  -H "Content-Type: application/json" \
  -d '{"symbol": "BTC/USDT", "timeframe": "1h", "days_back": 7}'
```

### 4. 运行策略回测
```bash
curl -X POST "http://localhost:8000/api/backtest/run" \
  -H "Content-Type: application/json" \
  -d '{"symbol": "BTC/USDT", "strategy": "simple_ma"}'
```

### 5. 查看API文档
浏览器打开: http://localhost:8000/docs

---

## 核心功能速查

### 市场数据
```bash
# 实时价格
GET /api/market/ticker?symbol=BTC/USDT

# K线数据
GET /api/market/ohlcv?symbol=BTC/USDT&timeframe=1h&limit=100

# WebSocket推送
ws://localhost:8000/api/market/ws/ticker?symbol=BTC/USDT
```

### 技术指标
```bash
# 计算所有指标
POST /api/indicators/latest
{
  "symbol": "BTC/USDT",
  "timeframe": "1h"
}
```

### 策略回测
```bash
# 运行回测
POST /api/backtest/run
{
  "symbol": "BTC/USDT",
  "strategy": "simple_ma",  # 或 "rsi", "macd"
  "initial_capital": 10000
}
```

### AI分析
```bash
# 市场分析
POST /api/ai/analyze
{
  "symbol": "BTC/USDT"
}

# OpenAI兼容格式
POST /v1/chat/completions
{
  "model": "claude-opus-4-8",
  "messages": [{"role": "user", "content": "分析BTC走势"}]
}
```

---

## 项目结构速览

```
stocks/
├── python-engine/          # Python后端 ✅
│   ├── main.py            # 入口
│   ├── api/routes/        # API路由
│   ├── core/              # 核心模块
│   └── venv/              # 虚拟环境
│
├── src-tauri/             # Rust Tauri ✅
│   └── src/main.rs        # 自动启动Python
│
├── src/                   # React前端 ⏳
├── data/                  # SQLite数据库 ✅
│   └── stocks.db
│
└── 文档/
    ├── README.md
    ├── DEVELOPMENT.md
    ├── API_EXAMPLES.md
    └── PROJECT_SUMMARY.md
```

---

## 可用策略

1. **simple_ma** - 双均线策略 (MA 10/20)
2. **rsi** - RSI超买超卖策略
3. **macd** - MACD交叉策略

---

## 支持的交易所

- Binance (币安)
- OKX (欧易)

---

## 技术指标列表

- SMA (10, 20, 50)
- EMA (12, 26)
- RSI
- MACD
- 布林带
- ATR
- Stochastic
- ADX

---

## 配置Claude AI（可选）

```bash
# 设置环境变量
export ANTHROPIC_API_KEY="sk-ant-..."

# 或在 .env 文件中
echo "ANTHROPIC_API_KEY=sk-ant-..." > python-engine/.env

# 验证
curl http://localhost:8000/api/ai/status
```

---

## 常见问题

**Q: Python服务启动失败？**
A: 确保虚拟环境已激活，依赖已安装：
```bash
source python-engine/venv/bin/activate
pip install -r python-engine/requirements.txt
```

**Q: 如何查看详细日志？**
A: 日志文件在 `/tmp/fastapi.log`
```bash
tail -f /tmp/fastapi.log
```

**Q: 数据库在哪里？**
A: `data/stocks.db`
```bash
sqlite3 data/stocks.db ".tables"
```

**Q: 如何添加新策略？**
A: 编辑 `python-engine/core/strategy/base.py`，继承 `Strategy` 类

---

## 更多帮助

- 开发指南: `DEVELOPMENT.md`
- API示例: `API_EXAMPLES.md`
- 项目总结: `PROJECT_SUMMARY.md`

---

**版本**: 0.1.0  
**更新**: 2026-06-15
