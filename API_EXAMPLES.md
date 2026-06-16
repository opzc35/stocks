# API使用示例

## 基础配置

**Base URL**: `http://localhost:8000`

## 1. 市场数据API

### 获取实时Ticker
```bash
curl -X GET "http://localhost:8000/api/market/ticker?symbol=BTC/USDT&exchange=binance"
```

**响应示例**:
```json
{
  "symbol": "BTC/USDT",
  "price": 65859.73,
  "volume": 39225.49,
  "timestamp": 1781531180935
}
```

### 获取K线数据
```bash
curl -X GET "http://localhost:8000/api/market/ohlcv?symbol=BTC/USDT&timeframe=1h&limit=100"
```

**响应示例**:
```json
[
  {
    "timestamp": 1781513249713,
    "open": 64693.48,
    "high": 64721.68,
    "low": 64620.80,
    "close": 64663.69,
    "volume": 3557.99
  }
]
```

### WebSocket实时推送
```javascript
const ws = new WebSocket('ws://localhost:8000/api/market/ws/ticker?symbol=BTC/USDT');

ws.onmessage = (event) => {
  const ticker = JSON.parse(event.data);
  console.log('Real-time price:', ticker.price);
};

// 心跳
setInterval(() => {
  ws.send('ping');
}, 30000);
```

---

## 2. 历史数据API

### 同步历史数据
```bash
curl -X POST "http://localhost:8000/api/data/sync" \
  -H "Content-Type: application/json" \
  -d '{
    "symbol": "BTC/USDT",
    "exchange": "binance",
    "timeframe": "1h",
    "days_back": 30
  }'
```

**响应示例**:
```json
{
  "success": true,
  "message": "Successfully stored 720 candles",
  "count": 720,
  "symbol": "BTC/USDT",
  "exchange": "binance",
  "timeframe": "1h"
}
```

### 查询历史数据
```bash
curl -X POST "http://localhost:8000/api/data/query" \
  -H "Content-Type: application/json" \
  -d '{
    "symbol": "BTC/USDT",
    "exchange": "binance",
    "timeframe": "1h",
    "limit": 100
  }'
```

---

## 3. 技术指标API

### 计算技术指标
```bash
curl -X POST "http://localhost:8000/api/indicators/latest" \
  -H "Content-Type: application/json" \
  -d '{
    "symbol": "BTC/USDT",
    "exchange": "binance",
    "timeframe": "1h",
    "limit": 100
  }'
```

**响应示例**:
```json
{
  "timestamp": 1781528515158,
  "close": 64629.12,
  "sma_20": 65096.34,
  "sma_50": 65039.80,
  "ema_12": 65012.86,
  "ema_26": 65054.59,
  "rsi": 41.77,
  "macd": -41.73,
  "macd_signal": 5.35,
  "bb_upper": 65604.87,
  "bb_middle": 65096.34,
  "bb_lower": 64587.80,
  "atr": 422.22,
  "stoch_k": 6.66,
  "stoch_d": 25.08,
  "adx": 8.08
}
```

---

## 4. 回测API

### 运行策略回测
```bash
curl -X POST "http://localhost:8000/api/backtest/run" \
  -H "Content-Type: application/json" \
  -d '{
    "symbol": "BTC/USDT",
    "exchange": "binance",
    "timeframe": "1h",
    "strategy": "simple_ma",
    "initial_capital": 10000,
    "limit": 500
  }'
```

**响应示例**:
```json
{
  "success": true,
  "strategy": "simple_ma",
  "symbol": "BTC/USDT",
  "timeframe": "1h",
  "data_points": 168,
  "results": {
    "initial_capital": 10000.0,
    "final_capital": 9264.68,
    "total_return": -7.35,
    "max_drawdown": 7.35,
    "sharpe_ratio": -1.69,
    "total_trades": 11,
    "winning_trades": 2,
    "losing_trades": 9,
    "win_rate": 18.18,
    "trades": [...],
    "equity_curve": [...],
    "timestamps": [...]
  }
}
```

### 列出可用策略
```bash
curl -X GET "http://localhost:8000/api/backtest/strategies"
```

**响应示例**:
```json
{
  "strategies": [
    {
      "id": "simple_ma",
      "name": "Simple MA Strategy",
      "description": "双均线交叉策略：短期均线上穿长期均线买入，下穿卖出"
    },
    {
      "id": "rsi",
      "name": "RSI Strategy",
      "description": "RSI策略：RSI < 30超卖买入，RSI > 70超买卖出"
    },
    {
      "id": "macd",
      "name": "MACD Strategy",
      "description": "MACD策略：MACD上穿信号线买入，下穿卖出"
    }
  ]
}
```

---

## 5. AI分析API

### AI市场分析
```bash
curl -X POST "http://localhost:8000/api/ai/analyze" \
  -H "Content-Type: application/json" \
  -d '{
    "symbol": "BTC/USDT",
    "exchange": "binance",
    "timeframe": "1h",
    "limit": 100
  }'
```

**响应示例（规则引擎模式）**:
```json
{
  "success": true,
  "symbol": "BTC/USDT",
  "current_price": 64629.12,
  "analysis": "# BTC/USDT 技术分析报告...",
  "model": "rule-based-fallback",
  "note": "Claude API not configured, using rule-based analysis"
}
```

### 检查AI功能状态
```bash
curl -X GET "http://localhost:8000/api/ai/status"
```

**响应示例**:
```json
{
  "available": false,
  "model": "rule-based-fallback",
  "message": "ANTHROPIC_API_KEY not set, using fallback analysis"
}
```

---

## 6. OpenAI兼容API

### Chat Completions
```bash
curl -X POST "http://localhost:8000/v1/chat/completions" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -d '{
    "model": "claude-opus-4-8",
    "messages": [
      {
        "role": "user",
        "content": "分析BTC/USDT当前走势"
      }
    ],
    "max_tokens": 2000
  }'
```

**响应示例**:
```json
{
  "id": "chatcmpl-1781531180",
  "object": "chat.completion",
  "created": 1781531180,
  "model": "claude-opus-4-8",
  "choices": [
    {
      "index": 0,
      "message": {
        "role": "assistant",
        "content": "根据技术指标分析..."
      },
      "finish_reason": "stop"
    }
  ],
  "usage": {
    "prompt_tokens": 25,
    "completion_tokens": 150,
    "total_tokens": 175
  }
}
```

### 使用OpenAI SDK
```python
from openai import OpenAI

# 将base_url指向本地API
client = OpenAI(
    api_key="dummy",  # 本地不需要真实的key
    base_url="http://localhost:8000/v1"
)

response = client.chat.completions.create(
    model="claude-opus-4-8",
    messages=[
        {"role": "user", "content": "分析BTC走势"}
    ]
)

print(response.choices[0].message.content)
```

### 列出模型
```bash
curl -X GET "http://localhost:8000/v1/models"
```

**响应示例**:
```json
{
  "object": "list",
  "data": [
    {
      "id": "claude-opus-4-8",
      "object": "model",
      "created": 1677610602,
      "owned_by": "anthropic"
    },
    {
      "id": "claude-sonnet-4-6",
      "object": "model",
      "created": 1677610602,
      "owned_by": "anthropic"
    }
  ]
}
```

---

## 7. Python SDK示例

### 完整交易流程
```python
import requests
import time

BASE_URL = "http://localhost:8000"

# 1. 同步历史数据
print("同步历史数据...")
response = requests.post(f"{BASE_URL}/api/data/sync", json={
    "symbol": "BTC/USDT",
    "exchange": "binance",
    "timeframe": "1h",
    "days_back": 7
})
print(response.json())

# 2. 计算技术指标
print("\n计算技术指标...")
response = requests.post(f"{BASE_URL}/api/indicators/latest", json={
    "symbol": "BTC/USDT",
    "exchange": "binance",
    "timeframe": "1h"
})
indicators = response.json()
print(f"RSI: {indicators['rsi']}")
print(f"MACD: {indicators['macd']}")

# 3. 运行回测
print("\n运行回测...")
response = requests.post(f"{BASE_URL}/api/backtest/run", json={
    "symbol": "BTC/USDT",
    "strategy": "simple_ma",
    "initial_capital": 10000
})
results = response.json()
print(f"总收益: {results['results']['total_return']}%")
print(f"胜率: {results['results']['win_rate']}%")

# 4. AI分析
print("\nAI市场分析...")
response = requests.post(f"{BASE_URL}/api/ai/analyze", json={
    "symbol": "BTC/USDT"
})
analysis = response.json()
print(analysis['analysis'])
```

---

## 8. 配置Claude API（可选）

如果要使用完整的Claude AI分析功能，需要配置API密钥：

### 方法1: 环境变量
```bash
export ANTHROPIC_API_KEY="sk-ant-..."
python python-engine/main.py
```

### 方法2: .env文件
```bash
# python-engine/.env
ANTHROPIC_API_KEY=sk-ant-...
```

### 验证配置
```bash
curl http://localhost:8000/api/ai/status
```

如果配置成功，会看到：
```json
{
  "available": true,
  "model": "claude-opus-4-8",
  "message": "Claude AI is configured and ready"
}
```

---

## 错误处理

所有API都遵循统一的错误格式：

```json
{
  "detail": "错误描述信息"
}
```

常见HTTP状态码：
- `200` - 成功
- `400` - 请求参数错误
- `404` - 资源不存在
- `500` - 服务器内部错误
- `503` - 服务不可用

---

## 性能建议

1. **历史数据同步**: 首次同步建议限制在30天内
2. **WebSocket**: 使用心跳保持连接活跃
3. **回测**: 大数据量回测建议limit在1000以内
4. **并发请求**: API支持并发，但建议控制在合理范围

---

## 完整示例项目

查看 `examples/` 目录获取更多完整示例：
- `trading_bot.py` - 简单交易机器人
- `backtest_optimizer.py` - 策略参数优化
- `market_monitor.py` - 实时市场监控

---

**更新日期**: 2026-06-15  
**API版本**: v0.1.0
