# 开发指南

## 项目概述

这是一个基于 Tauri + React + Python 的全平台股票交易客户端，支持多交易所数据获取、历史数据管理、实时行情推送、策略回测等功能。

## 已实现功能 (8/15)

### 1. 架构基础
- ✅ Tauri 2 桌面应用框架
- ✅ React 19 + TypeScript 前端
- ✅ Python FastAPI 交易引擎
- ✅ SQLite 数据存储
- ✅ Rust 后端服务

### 2. 市场数据
- ✅ 实时Ticker获取
- ✅ K线(OHLCV)数据获取
- ✅ 历史数据同步与存储
- ✅ WebSocket实时推送
- ✅ 多交易所支持 (Binance, OKX)

### 3. 数据管理
- ✅ SQLite数据库 (market_data, strategies, backtest_results, trades)
- ✅ 历史数据管理系统
- ✅ 数据持久化与查询

## API端点

### REST API

**市场数据**
```bash
# 获取实时ticker
GET /api/market/ticker?symbol=BTC/USDT&exchange=binance

# 获取K线数据
GET /api/market/ohlcv?symbol=BTC/USDT&timeframe=1h&limit=100

# 列出支持的交易所
GET /api/market/exchanges
```

**历史数据管理**
```bash
# 同步历史数据到数据库
POST /api/data/sync
Content-Type: application/json
{
  "symbol": "BTC/USDT",
  "exchange": "binance",
  "timeframe": "1h",
  "days_back": 30
}

# 查询历史数据
POST /api/data/query
Content-Type: application/json
{
  "symbol": "BTC/USDT",
  "exchange": "binance",
  "timeframe": "1h",
  "limit": 1000
}
```

### WebSocket API

**实时行情推送**
```javascript
// 连接WebSocket
ws://localhost:8000/api/market/ws/ticker?symbol=BTC/USDT&exchange=binance

// 接收实时ticker数据
{
  "symbol": "BTC/USDT",
  "price": 65000.00,
  "volume": 30000.00,
  "timestamp": 1781531180935
}

// 心跳
send: "ping"
receive: "pong"
```

## 开发环境

### 启动开发服务器

1. **启动Python引擎**
```bash
source python-engine/venv/bin/activate
python python-engine/main.py
```

2. **启动Tauri开发服务器**
```bash
npm run tauri:dev
```

### 测试API

```bash
# 健康检查
curl http://localhost:8000/health

# 获取实时价格
curl "http://localhost:8000/api/market/ticker?symbol=BTC/USDT"

# 同步历史数据
curl -X POST "http://localhost:8000/api/data/sync" \
  -H "Content-Type: application/json" \
  -d '{"symbol": "BTC/USDT", "timeframe": "1h", "days_back": 7}'

# 查询数据库
sqlite3 data/stocks.db "SELECT COUNT(*) FROM market_data"
```

## 项目结构

```
stocks/
├── src/                           # React前端
│   ├── App.tsx                    # 主组件
│   └── main.tsx                   # 入口文件
│
├── src-tauri/                     # Rust Tauri后端
│   ├── src/
│   │   ├── main.rs                # 主入口（启动Python引擎）
│   │   ├── commands/              # Tauri命令
│   │   │   ├── market.rs          # 市场数据命令
│   │   │   ├── strategy.rs        # 策略命令
│   │   │   └── ai.rs              # AI分析命令
│   │   └── services/
│   │       ├── python_bridge.rs   # Python进程管理
│   │       └── database.rs        # 数据库服务
│   └── icons/                     # 应用图标
│
├── python-engine/                 # Python交易引擎
│   ├── main.py                    # FastAPI应用入口
│   ├── config.py                  # 配置文件
│   ├── api/routes/                # API路由
│   │   ├── market.py              # 市场数据API (含WebSocket)
│   │   ├── data.py                # 历史数据API
│   │   ├── backtest.py            # 回测API
│   │   └── ai.py                  # AI分析API
│   ├── core/                      # 核心功能
│   │   ├── exchanges/             # 交易所适配器
│   │   │   └── adapter.py         # Binance, OKX适配器
│   │   ├── data/                  # 数据管理
│   │   │   ├── database.py        # SQLite数据库
│   │   │   ├── history.py         # 历史数据管理
│   │   │   └── realtime.py        # 实时数据流
│   │   ├── strategy/              # 策略引擎
│   │   ├── backtest/              # 回测引擎
│   │   └── ai/                    # AI分析
│   ├── models/                    # 数据模型
│   ├── utils/                     # 工具函数
│   └── venv/                      # Python虚拟环境
│
└── data/                          # 数据存储
    └── stocks.db                  # SQLite数据库
```

## 数据库Schema

### market_data 表
```sql
CREATE TABLE market_data (
    id INTEGER PRIMARY KEY,
    symbol TEXT NOT NULL,
    exchange TEXT NOT NULL,
    timestamp INTEGER NOT NULL,
    open REAL NOT NULL,
    high REAL NOT NULL,
    low REAL NOT NULL,
    close REAL NOT NULL,
    volume REAL NOT NULL,
    timeframe TEXT NOT NULL,
    created_at INTEGER,
    UNIQUE(symbol, exchange, timestamp, timeframe)
);
```

### strategies 表
```sql
CREATE TABLE strategies (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,
    code TEXT NOT NULL,
    description TEXT,
    parameters TEXT,
    created_at INTEGER,
    updated_at INTEGER
);
```

### backtest_results 表
```sql
CREATE TABLE backtest_results (
    id INTEGER PRIMARY KEY,
    strategy_id INTEGER NOT NULL,
    symbol TEXT NOT NULL,
    timeframe TEXT NOT NULL,
    start_date INTEGER NOT NULL,
    end_date INTEGER NOT NULL,
    initial_capital REAL NOT NULL,
    final_capital REAL,
    total_return REAL,
    sharpe_ratio REAL,
    max_drawdown REAL,
    total_trades INTEGER,
    win_rate REAL,
    results_data TEXT,
    created_at INTEGER,
    FOREIGN KEY (strategy_id) REFERENCES strategies(id)
);
```

## 下一步开发计划

### 即将实现 (剩余7个任务)
9. 集成TradingView图表
10. 构建主界面布局
11. 实现技术指标引擎
12. 实现回测引擎
13. 实现策略编辑器UI
14. 集成Claude AI分析
15. 配置GitHub Actions CI/CD

## 注意事项

1. **Python引擎启动**: Tauri应用启动时会自动启动Python引擎
2. **地理限制**: Binance API可能受地理位置限制，程序会自动fallback到模拟数据
3. **数据库**: 首次运行时会自动创建数据库和表结构
4. **环境变量**: 复制`.env.example`为`.env`并配置API密钥（可选）

## 贡献

欢迎提交Issue和Pull Request！
