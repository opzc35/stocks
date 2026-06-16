# Stocks Trading Client

一个基于Tauri + React + Python的全平台股票交易客户端。

## 技术栈

### 前端
- **Tauri 2** - 桌面应用框架
- **React 19** - UI框架
- **TypeScript** - 类型安全
- **Vite** - 构建工具

### 后端
- **Rust** - Tauri后端和系统调用
- **Python FastAPI** - 交易引擎API
- **CCXT** - 多交易所接口
- **SQLite** - 本地数据库

## 功能特性

- ✅ 多交易所支持（Binance, OKX等）
- ✅ 实时行情数据
- 🚧 K线图表（TradingView集成）
- 🚧 策略回测引擎
- 🚧 技术指标计算
- 🚧 AI市场分析（Claude集成）

## 项目结构

```
stocks/
├── src/                    # React前端源码
├── src-tauri/              # Rust Tauri后端
│   ├── src/
│   │   ├── main.rs         # 主入口
│   │   ├── commands/       # Tauri命令
│   │   └── services/       # 服务层
│   └── Cargo.toml
├── python-engine/          # Python交易引擎
│   ├── main.py             # FastAPI应用
│   ├── api/                # API路由
│   ├── core/               # 核心功能
│   └── requirements.txt
└── data/                   # 数据存储
```

## 开发环境设置

### 前置要求

- Node.js 18+
- Rust 1.70+
- Python 3.12+

### 安装依赖

1. 安装前端依赖：
```bash
npm install
```

2. 创建Python虚拟环境并安装依赖：
```bash
cd python-engine
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 启动开发服务器

1. 启动Python交易引擎：
```bash
source python-engine/venv/bin/activate
python python-engine/main.py
```

2. 启动Tauri开发服务器：
```bash
npm run tauri:dev
```

## API端点

Python FastAPI服务运行在 `http://localhost:8000`

- `GET /health` - 健康检查
- `GET /api/market/ticker?symbol=BTC/USDT` - 获取ticker数据
- `GET /api/market/ohlcv?symbol=BTC/USDT&timeframe=1h` - 获取K线数据
- `POST /api/backtest/run` - 运行策略回测
- `POST /api/ai/analyze` - AI市场分析

## 构建

构建生产版本：

```bash
npm run tauri:build
```

## 许可证

ISC

## 贡献

欢迎提交Issue和Pull Request！
