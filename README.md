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
- ✅ 价格预警系统
  - 🔔 设置价格突破/跌破预警
  - 🚨 触发时弹窗通知
  - 📊 预警状态实时监控
  - 🔄 支持重置和管理预警
- ✅ 新闻展示与分析
  - 📰 新闻面板：实时查看市场新闻
  - 📍 图表标记：新闻事件直接标注在价格图表上
  - 🎯 情绪分析：利好/利空/中性新闻分类
  - 🔍 新闻筛选：按情绪类型快速过滤
- ✅ K线图表与技术指标
- ✅ 策略回测引擎
- 🚧 AI市场分析（Claude集成）

## 新功能：价格预警系统

### 功能说明

价格预警功能帮助你及时捕捉市场机会：

1. **设置预警**
   - 选择突破(▲)或跌破(▼)条件
   - 输入目标价格
   - 一键添加预警

2. **实时监控**
   - 自动监测当前价格
   - 达到目标价格时立即触发
   - 预警状态实时显示

3. **触发通知**
   - 🚨 右上角弹窗提醒
   - 📢 提示音通知（浏览器支持时）
   - 🎯 显示触发价格和时间
   - 💡 可查看详情或关闭通知

4. **预警管理**
   - 查看所有预警列表
   - 已触发预警自动高亮
   - 支持重置预警继续使用
   - 一键删除不需要的预警

### 使用场景

- **买入机会**：设置跌破预警，价格下跌到目标位时通知买入
- **止盈止损**：设置突破预警，价格达到目标后及时卖出
- **关键位监控**：在重要支撑位/阻力位设置预警
- **多点位布局**：同时设置多个价格预警，全方位监控市场

## 新功能：社交媒体机器人通知

### 功能说明

将价格预警自动推送到社交平台，随时随地接收通知：

1. **支持平台**
   - 📱 Telegram：个人使用，全球可访问
   - 💬 Discord：游戏社区、技术团队
   - 💼 Slack：企业团队、工作协作
   - 💚 企业微信：国内企业、移动办公

2. **配置简单**
   - 点击顶部"🤖 机器人"按钮
   - 添加并配置机器人
   - 测试连接确认
   - 启用后自动推送

3. **消息格式**
   - 包含交易对、价格、时间
   - 突破/跌破类型区分
   - 富文本格式（Discord/Slack）

4. **灵活管理**
   - 支持多个机器人
   - 独立开关控制
   - 编辑和删除配置

### 配置指南

详细的平台配置教程请查看 [BOT_NOTIFICATION.md](./BOT_NOTIFICATION.md)

**快速开始：**

1. 选择平台（推荐 Telegram）
2. 按照文档获取必要信息（Token、Webhook URL 等）
3. 在应用中添加机器人配置
4. 测试连接
5. 启用机器人

## 新功能：新闻展示

### 功能说明

新增的新闻展示功能让你可以：

1. **新闻总览面板**（右侧）
   - 实时查看加密货币市场新闻
   - 按情绪筛选：利好📈、利空📉、中性📰
   - 点击新闻高亮对应时间点

2. **图表上的新闻标记**（左侧图表）
   - 新闻事件在价格图表上以彩色圆点标记
   - 绿色点 = 利好消息
   - 红色点 = 利空消息
   - 灰色点 = 中性消息
   - 点击标记查看新闻详情

3. **交互体验**
   - 点击新闻项，图表上对应标记会高亮
   - 点击图表标记，新闻面板会滚动到对应新闻
   - 响应式布局，适配不同屏幕尺寸

### 如何使用

运行开发服务器后，主界面会自动显示新闻面板：

```bash
npm run dev
```

目前使用的是模拟新闻数据，你可以在 `App.tsx` 的 `fetchNews` 函数中接入真实的新闻 API。

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
