# 🌍 多市场数据 & 全球新闻

## 概述

系统现已支持**多个金融市场**和**全球新闻聚合**，用户可以自由添加和监控全球各类资产。

---

## 🎯 支持的市场

### 1. ₿ 加密货币 (Crypto)

**数据源**: Binance API

**支持交易对**:
- BTC/USDT - Bitcoin
- ETH/USDT - Ethereum
- BNB/USDT - Binance Coin
- XRP/USDT - Ripple
- ADA/USDT - Cardano
- SOL/USDT - Solana
- DOGE/USDT - Dogecoin
- 以及 Binance 上所有交易对

**特点**:
- 实时价格数据
- 24小时交易
- 高流动性
- 支持多种时间周期

### 2. 🇺🇸 美股 (US Stock)

**数据源**: Yahoo Finance API

**支持股票**:
- AAPL - Apple Inc.
- MSFT - Microsoft Corporation
- GOOGL - Alphabet Inc.
- AMZN - Amazon.com Inc.
- TSLA - Tesla Inc.
- NVDA - NVIDIA Corporation
- META - Meta Platforms Inc.
- 以及所有美股市场股票

**特点**:
- 纳斯达克、纽交所
- 盘前盘后数据
- 公司基本面信息
- 历史数据丰富

### 3. 🇭🇰 港股 (Hong Kong Stock)

**数据源**: Yahoo Finance API

**支持股票**:
- 0700.HK - 腾讯控股
- 9988.HK - 阿里巴巴
- 0941.HK - 中国移动
- 1299.HK - 友邦保险
- 以及所有港交所上市股票

**特点**:
- 港币计价
- 支持A+H股对比
- 实时行情
- 财务数据

**代码格式**: `0700.HK`, `9988.HK`

### 4. 🇨🇳 A股 (China A-Share)

**数据源**: Yahoo Finance API

**支持股票**:
- 600519.SS - 贵州茅台 (上交所)
- 000858.SZ - 五粮液 (深交所)
- 600036.SS - 招商银行
- 000001.SZ - 平安银行
- 以及所有A股市场股票

**特点**:
- 上海证券交易所 (SS)
- 深圳证券交易所 (SZ)
- 人民币计价
- T+1交易制度

**代码格式**:
- 上海: `600519.SS`
- 深圳: `000858.SZ`

---

## 📊 API 接口

### 获取实时行情

```bash
GET /api/multi-market/quote?symbol=BTC/USDT&market=crypto

响应:
{
  "success": true,
  "data": {
    "symbol": "BTC/USDT",
    "name": "Bitcoin",
    "market": "crypto",
    "price": 67532.45,
    "change": 1234.56,
    "change_percent": 1.86,
    "volume": 12345678.90,
    "timestamp": 1718529625000,
    "currency": "USDT"
  }
}
```

### 获取K线数据

```bash
GET /api/multi-market/klines?symbol=AAPL&market=us&interval=1h&limit=100

响应:
{
  "success": true,
  "data": [
    {
      "timestamp": 1718529600000,
      "open": 190.50,
      "high": 191.20,
      "low": 190.10,
      "close": 190.80,
      "volume": 1234567
    },
    ...
  ],
  "count": 100
}
```

### 搜索交易对

```bash
GET /api/multi-market/search?q=tesla&markets=us,crypto

响应:
{
  "success": true,
  "data": [
    {
      "symbol": "TSLA",
      "name": "Tesla Inc.",
      "market": "us",
      "exchange": "NASDAQ",
      "currency": "USD"
    }
  ],
  "count": 1
}
```

### 获取市场列表

```bash
GET /api/multi-market/markets

响应:
{
  "success": true,
  "data": [
    {
      "id": "crypto",
      "name": "加密货币",
      "icon": "₿",
      "examples": ["BTC/USDT", "ETH/USDT"]
    },
    ...
  ]
}
```

---

## 📰 全球新闻

### 新闻来源

#### 英文新闻
- **CryptoCompare** - 加密货币新闻
- **NewsAPI** - 全球财经新闻
- **Bloomberg RSS** - 彭博财经
- **Reuters RSS** - 路透社

#### 中文新闻
- **新华财经** - 宏观经济
- **财经网** - A股市场
- **香港经济日报** - 港股市场
- **证券时报** - 证券市场

### 新闻分类

- **crypto** - 加密货币新闻
- **stock** - 股票市场新闻
- **forex** - 外汇市场新闻
- **commodity** - 大宗商品新闻
- **general** - 综合财经新闻

### 情感分析

每条新闻都包含自动情感分析：

- 📈 **positive** - 利好消息
- 📉 **negative** - 利空消息
- 📊 **neutral** - 中性消息

### 新闻 API

#### 获取最新新闻

```bash
GET /api/news/latest?category=all&language=all&limit=20

响应:
{
  "success": true,
  "data": [
    {
      "id": "news-1",
      "title": "Fed Holds Interest Rates Steady",
      "summary": "The Federal Reserve decided...",
      "url": "https://...",
      "source": "Bloomberg",
      "published_at": 1718529625000,
      "image_url": "https://...",
      "category": "stock",
      "sentiment": "neutral",
      "tags": ["Fed", "Interest Rates"],
      "language": "en"
    },
    ...
  ],
  "count": 20
}
```

#### 获取加密货币新闻

```bash
GET /api/news/crypto?limit=20
```

#### 获取中文新闻

```bash
GET /api/news/chinese?limit=20
```

#### 搜索新闻

```bash
GET /api/news/search?q=bitcoin&category=crypto&limit=20
```

---

## 🚀 使用方法

### 前端使用

#### 1. 市场选择器

```tsx
import { MarketSelector } from './components/MarketSelector'

function App() {
  const [symbol, setSymbol] = useState('BTC/USDT')
  const [market, setMarket] = useState('crypto')

  const handleSymbolChange = (newSymbol: string, newMarket: string) => {
    setSymbol(newSymbol)
    setMarket(newMarket)
    // 加载新数据...
  }

  return (
    <MarketSelector
      currentSymbol={symbol}
      onSymbolChange={handleSymbolChange}
    />
  )
}
```

#### 2. 新闻面板

```tsx
import { NewsPanel } from './components/NewsPanel'

function App() {
  return (
    <div className="side-panel">
      <NewsPanel />
    </div>
  )
}
```

### 添加自定义交易对

1. **点击交易对选择器**
2. **选择市场类型**
   - 加密货币
   - 美股
   - 港股
   - A股
3. **输入交易对代码**
   - 加密货币: `BTC/USDT`
   - 美股: `AAPL`
   - 港股: `0700.HK`
   - A股: `600519.SS`
4. **点击添加**

### 搜索功能

在搜索框输入：
- **公司名称**: `Tesla`, `腾讯`
- **股票代码**: `TSLA`, `0700`
- **币种名称**: `Bitcoin`, `以太坊`

系统会自动搜索并显示结果。

---

## 💡 使用场景

### 场景 1: 全球资产配置

**需求**: 同时监控多个市场

**使用**:
1. 添加 BTC/USDT (加密货币)
2. 添加 AAPL (美股)
3. 添加 0700.HK (港股)
4. 添加 600519.SS (A股)

**收益**: 一站式监控全球资产

### 场景 2: 跨市场套利

**需求**: 对比不同市场价格

**使用**:
1. 同时监控同一公司的不同市场
2. 例如：阿里巴巴 (BABA 美股 vs 9988.HK 港股)
3. 寻找价差套利机会

### 场景 3: 新闻驱动交易

**需求**: 根据新闻快速反应

**使用**:
1. 启用新闻面板
2. 筛选相关类别
3. 查看情感分析
4. 及时调整仓位

### 场景 4: 多语言投资者

**需求**: 同时关注中英文新闻

**使用**:
1. 选择 "全部语言"
2. 获取中英文双语新闻
3. 全面了解市场动态

---

## 🔧 技术实现

### 后端架构

```
multi_market.py
├── fetch_crypto_data()      # 加密货币
├── fetch_us_stock_data()    # 美股
├── fetch_hk_stock_data()    # 港股
├── fetch_cn_stock_data()    # A股
└── fetch_market_data()      # 统一接口

global_news.py
├── fetch_crypto_news()      # 加密货币新闻
├── fetch_financial_news()   # 财经新闻
├── fetch_chinese_news()     # 中文新闻
└── fetch_all_news()         # 聚合新闻
```

### 数据流

```
用户输入交易对
    ↓
自动检测市场类型
    ↓
调用对应API
    ↓
格式化数据
    ↓
返回统一格式
    ↓
前端展示
```

### 缓存策略

- **行情数据**: 无缓存（实时）
- **K线数据**: 缓存5分钟
- **新闻数据**: 缓存5分钟
- **搜索结果**: 缓存1小时

---

## ⚙️ 配置说明

### 环境变量

```bash
# 可选：NewsAPI Key（英文新闻）
NEWS_API_KEY=your_api_key_here

# 可选：Alpha Vantage Key（美股增强数据）
ALPHA_VANTAGE_KEY=your_api_key_here
```

### 依赖安装

```bash
cd python-engine

# 安装必要的库
pip install httpx feedparser

# 可选：RSS解析增强
pip install beautifulsoup4 lxml
```

---

## 📈 数据格式规范

### 交易对格式

| 市场 | 格式 | 示例 |
|------|------|------|
| 加密货币 | COIN/QUOTE | BTC/USDT, ETH/USDT |
| 美股 | SYMBOL | AAPL, TSLA, GOOGL |
| 港股 | CODE.HK | 0700.HK, 9988.HK |
| A股(上海) | CODE.SS | 600519.SS, 600036.SS |
| A股(深圳) | CODE.SZ | 000858.SZ, 000001.SZ |

### 时间周期

| 周期 | Crypto | US/HK/CN | 说明 |
|------|--------|----------|------|
| 1m | ✅ | ❌ | 1分钟 |
| 5m | ✅ | ✅ | 5分钟 |
| 15m | ✅ | ✅ | 15分钟 |
| 1h | ✅ | ✅ | 1小时 |
| 4h | ✅ | ❌ | 4小时 |
| 1d | ✅ | ✅ | 1天 |

---

## ⚠️ 限制说明

### API 限制

- **Binance**: 1200请求/分钟
- **Yahoo Finance**: 2000请求/小时
- **CryptoCompare**: 100000请求/月
- **NewsAPI**: 1000请求/天（免费）

### 数据延迟

- **加密货币**: 实时 (~100ms)
- **美股**: 延迟15分钟（免费）
- **港股**: 延迟15分钟（免费）
- **A股**: 延迟15分钟（免费）

### 交易时间

| 市场 | 交易时间 | 时区 |
|------|----------|------|
| 加密货币 | 24/7 | UTC |
| 美股 | 9:30-16:00 | EST |
| 港股 | 9:30-16:00 | HKT |
| A股 | 9:30-15:00 | CST |

---

## 🔮 未来计划

### v2.2
- ✅ 多市场支持
- ✅ 全球新闻聚合
- ⏳ WebSocket 实时推送
- ⏳ 深度数据（Level 2）

### v2.3
- ⏳ 期货市场
- ⏳ 外汇市场
- ⏳ 商品期货
- ⏳ ETF 基金

### v2.4
- ⏳ 新闻情感分析增强
- ⏳ AI 新闻摘要
- ⏳ 自定义新闻源
- ⏳ 新闻预警

---

## 📚 相关文档

- [README.md](../README.md) - 项目总览
- [IMAGE_RECOGNITION.md](./IMAGE_RECOGNITION.md) - 图片识别
- [CHART_SENDING.md](./CHART_SENDING.md) - 图表发送

---

**版本**: v2.2.0  
**日期**: 2026-06-16  
**功能**: 多市场数据 + 全球新闻 🌍
