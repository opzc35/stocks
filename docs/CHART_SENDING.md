# 📊 图表发送功能 - 社交媒体机器人增强

## 概述

为社交媒体机器人添加了**自动生成和发送K线图表**的功能，支持：
- 📈 实时K线图生成
- 🎨 图表批注（文字、箭头、趋势线、方框）
- 🤖 一键发送到各平台
- 💬 自定义说明文字

---

## 🎯 功能特点

### 1. 图表生成

**支持的配置**：
- 交易对选择（BTC/USDT, ETH/USDT等）
- 时间周期（1m, 5m, 15m, 1h, 4h, 1d）
- K线数量（20-500根）
- 技术指标（MA20, MA50, RSI, MACD, BOLL）
- 自定义标题

**样式特点**：
- Vercel 黑色主题
- 高清分辨率（150 DPI）
- 专业配色方案
- 自动水印

### 2. 批注功能

#### 📝 文字标注
```typescript
{
  type: 'text',
  position: { x: 50, y: 68000 },
  text: '📈 突破阻力位',
  color: '#0ba360'
}
```
- 自定义文字内容
- 箭头指向价格点
- 背景框突出显示

#### ➡️ 箭头批注
```typescript
{
  type: 'arrow',
  position: { x: 70, y: 69000, x2: 70, y2: 67500 },
  color: '#f857a6'
}
```
- 标记趋势方向
- 指示重要位置
- 弧形连接线

#### 📏 趋势线
```typescript
{
  type: 'line',
  position: { x: 30, y: 66000, x2: 90, y: 70000 },
  color: '#0070f3'
}
```
- 连接高低点
- 虚线样式
- 标记趋势通道

#### ⬜ 方框标记
```typescript
{
  type: 'box',
  position: { x: 40, y: 67000, width: 20, height: 2000 },
  color: '#f5a623'
}
```
- 标记重要区域
- 框选价格范围
- 虚线边框

### 3. 平台支持

#### 📱 Telegram
```python
await send_telegram_photo(
    bot_token='YOUR_TOKEN',
    chat_id=123456789,
    photo_bytes=image,
    caption='📊 市场分析'
)
```

#### 💬 Discord
```python
await send_discord_photo(
    webhook_url='https://discord.com/api/webhooks/...',
    photo_bytes=image,
    content='📊 市场分析'
)
```

#### 💼 Slack
```python
await send_slack_photo(
    webhook_url='https://hooks.slack.com/services/...',
    photo_bytes=image,
    text='📊 市场分析'
)
```

#### 💚 企业微信
```python
await send_wechat_photo(
    webhook_url='https://qyapi.weixin.qq.com/...',
    photo_bytes=image,
    content='📊 市场分析'
)
```

---

## 🚀 使用方法

### 方式 1: 前端界面

1. **打开图表工具**
   - 点击"机器人"按钮
   - 切换到"图表发送"标签

2. **配置图表**
   - 选择交易对和时间周期
   - 勾选需要的技术指标
   - 设置K线数量

3. **添加批注**
   - 点击批注工具按钮（文字、箭头、线、框）
   - 设置位置和颜色
   - 输入批注文字

4. **预览和发送**
   - 点击"预览图表"查看效果
   - 输入说明文字
   - 选择目标机器人平台
   - 点击"发送"

### 方式 2: API 调用

#### 生成图表
```bash
curl -X POST http://localhost:8001/api/chart/generate \
  -H "Content-Type: application/json" \
  -d '{
    "symbol": "BTC/USDT",
    "timeframe": "1h",
    "periods": 100,
    "indicators": ["MA20", "MA50", "RSI"],
    "annotations": [
      {
        "type": "text",
        "position": {"x": 50, "y": 68000},
        "text": "📈 突破阻力位",
        "color": "#0ba360"
      }
    ]
  }'
```

#### 发送图表
```bash
curl -X POST http://localhost:8001/api/chart/send \
  -H "Content-Type: application/json" \
  -d '{
    "platform": "telegram",
    "config": {...},
    "bot_config": {
      "bot_token": "YOUR_TOKEN",
      "chat_id": "YOUR_CHAT_ID"
    },
    "caption": "📊 BTC/USDT 技术分析"
  }'
```

### 方式 3: Webhook 自动回复

用户在机器人对话中输入关键词：
```
发送图表
显示K线
技术分析图
走势图
```

机器人自动生成并发送图表。

---

## 🎨 批注示例

### 示例 1: 突破分析
```python
annotations = [
    # 突破点标记
    {
        'type': 'text',
        'position': {'x': 70, 'y': 69500},
        'text': '🔥 突破前高',
        'color': '#0ba360'
    },
    # 支撑位箭头
    {
        'type': 'arrow',
        'position': {'x': 80, 'y': 69000, 'x2': 80, 'y2': 67500},
        'color': '#0070f3'
    },
    # 趋势线
    {
        'type': 'line',
        'position': {'x': 30, 'y': 66000, 'x2': 90, 'y': 69000},
        'color': '#0070f3'
    }
]
```

### 示例 2: 回调分析
```python
annotations = [
    # 回调区域
    {
        'type': 'box',
        'position': {'x': 50, 'y': 66000, 'width': 20, 'height': 1500},
        'color': '#f5a623'
    },
    # 买入提示
    {
        'type': 'text',
        'position': {'x': 60, 'y': 66500},
        'text': '💰 买入区域',
        'color': '#0ba360'
    }
]
```

### 示例 3: 止损位标记
```python
annotations = [
    # 止损线
    {
        'type': 'line',
        'position': {'x': 0, 'y': 65000, 'x2': 100, 'y2': 65000},
        'color': '#f857a6'
    },
    # 止损说明
    {
        'type': 'text',
        'position': {'x': 10, 'y': 65000},
        'text': '⛔ 止损位 $65,000',
        'color': '#f857a6'
    }
]
```

---

## 📝 消息模板

### 模板 1: 技术分析
```markdown
📊 BTC/USDT 技术分析

📈 当前价格: $67,532.45
📊 24h 涨跌: +2.5%
🔥 趋势: 上涨

**技术指标**:
• MA20: $66,800 ✓
• MA50: $65,200 ✓
• RSI: 62 (中性)

**批注说明**:
• 绿色标记: 突破阻力位
• 红色箭头: 回调支撑位
```

### 模板 2: 行情简报
```markdown
🔥 BTC/USDT 行情分析

当前价格走势强劲，已突破关键阻力位 $68,000。

**关键位置**:
• 阻力: $70,000
• 支撑: $66,500

⚠️ 风险提示: 注意止损设置
```

### 模板 3: 交易信号
```markdown
🚨 交易信号提醒

交易对: BTC/USDT
信号: 买入
价格: $67,500
止损: $65,000
目标: $72,000

**理由**: 
突破上升三角形形态，成交量放大
```

---

## 🛠️ 技术实现

### 后端 (Python)

**依赖库**：
```bash
pip install matplotlib numpy fastapi httpx pillow
```

**核心代码**：
```python
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

async def generate_chart(config: ChartConfig) -> bytes:
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10))
    
    # 绘制K线
    ax1.plot(dates, prices, color='#00f2fe', linewidth=2)
    
    # 添加批注
    for ann in config.annotations:
        if ann.type == 'text':
            ax1.annotate(ann.text, xy=(ann.position['x'], ann.position['y']),
                        color=ann.color, ...)
    
    # 保存为字节流
    buf = io.BytesIO()
    plt.savefig(buf, format='png', dpi=150)
    return buf.read()
```

### 前端 (React + TypeScript)

**组件**：`ChartSender.tsx`

**功能**：
- 配置界面
- 批注编辑
- 实时预览
- 一键发送

---

## 🚦 API 端点

### 生成图表
```
POST /api/chart/generate
Content-Type: application/json

{
  "symbol": "BTC/USDT",
  "timeframe": "1h",
  "periods": 100,
  "indicators": ["MA20", "MA50", "RSI"],
  "annotations": [...]
}

Response:
{
  "success": true,
  "data": {
    "image": "base64_encoded_image",
    "format": "png",
    "size": 123456
  }
}
```

### 发送图表
```
POST /api/chart/send
Content-Type: application/json

{
  "platform": "telegram",
  "config": {...},
  "bot_config": {...},
  "caption": "说明文字"
}

Response:
{
  "success": true,
  "platform": "telegram",
  "result": {...}
}
```

---

## 📊 示例效果

### 生成的图表包含：

1. **主图**
   - K线价格走势（蓝色）
   - MA20均线（黄色）
   - MA50均线（粉色）
   - 批注标记

2. **副图**
   - RSI指标
   - 超买/超卖区域标记
   - 70/30参考线

3. **批注层**
   - 文字标注（带箭头）
   - 趋势线
   - 区域标记
   - 箭头指示

4. **信息栏**
   - 图表标题
   - 时间戳水印
   - 技术指标图例

---

## 🎯 使用场景

### 场景 1: 每日行情分析
- 自动生成今日K线图
- 标记关键支撑阻力位
- 发送到 Telegram 频道
- 订阅用户自动接收

### 场景 2: 交易信号通知
- 检测到突破信号
- 生成带批注的图表
- 标记买卖点位
- 推送到所有订阅用户

### 场景 3: 策略回测报告
- 回测完成后生成
- 标记买卖点
- 显示收益曲线
- 发送报告到企业微信

### 场景 4: AI 分析结果
- AI 分析完成
- 生成可视化图表
- 添加分析批注
- 推送到 Discord 社区

---

## 🔧 配置说明

### Python 环境
```bash
cd python-engine
pip install -r requirements.txt
python bot_webhook_enhanced.py
```

### 访问地址
```
后端: http://localhost:8001
健康检查: http://localhost:8001/health
```

---

## 💡 最佳实践

### 1. 批注使用建议
- ✅ 使用清晰的文字说明
- ✅ 颜色统一（绿=上涨，红=下跌）
- ✅ 批注不要过多（3-5个）
- ✅ 位置精确标记关键点

### 2. 消息文字建议
- ✅ 简洁明了
- ✅ 包含关键数据
- ✅ 提供操作建议
- ✅ 标注风险提示

### 3. 发送频率控制
- ⚠️ 避免频繁发送
- ⚠️ 合并相似图表
- ⚠️ 设置冷却时间
- ⚠️ 尊重用户体验

---

## 📚 相关文档

- [BOT_NOTIFICATION.md](./BOT_NOTIFICATION.md) - 机器人通知功能
- [README.md](../README.md) - 项目总体说明
- [API文档](./API.md) - 完整API参考

---

**版本**: v2.1.0  
**日期**: 2026-06-16  
**功能**: 图表发送 + 批注支持 ✨
