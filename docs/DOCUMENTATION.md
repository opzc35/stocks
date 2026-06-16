# 📚 量化交易系统 - 完整文档

## 目录

- [快速开始](#快速开始)
- [功能特性](#功能特性)
- [部署指南](#部署指南)
- [开发文档](#开发文档)

---

## 快速开始

### 安装和运行

```bash
# 1. 安装依赖
npm install

# 2. 启动开发服务器
npm run dev

# 3. 访问应用
http://localhost:5173/
```

### 5分钟体验

1. **查看实时行情** - 首页即可看到 BTC/USDT 价格
2. **设置价格预警** - 右侧面板点击"添加预警"
3. **与 AI 对话** - 顶部点击"🧠 AI助手"
4. **配置机器人** - 顶部点击"🤖 机器人"（可选）

---

## 功能特性

### 1. 📊 实时行情监控
- 多交易对支持（BTC、ETH、BNB）
- K线图表可视化
- 技术指标（RSI、MACD、SMA）
- 10秒自动更新

### 2. 🔔 价格预警系统

**设置预警**
1. 选择类型：突破 ▲ 或跌破 ▼
2. 输入目标价格
3. 点击"添加"

**通知方式**
- 浏览器弹窗 + 音频
- 社交媒体推送（需配置）

**管理预警**
- 查看状态（等待中/已触发）
- 重置预警
- 删除预警

### 3. 🤖 社交媒体机器人

**支持平台**
- 📱 Telegram - 个人使用
- 💬 Discord - 团队协作
- 💼 Slack - 企业团队
- 💚 企业微信 - 国内企业

**两种模式**

1. **单向通知**（预警触发推送）
   ```
   价格触发 → 机器人推送 → 你收到通知
   ```

2. **双向对话**（与 AI 交互）
   ```
   你: 帮我创建一个策略
   机器人: 策略已创建... ✅
   
   你: 运行回测
   机器人: 回测完成，收益 +15.6% ✅
   ```

**配置步骤**

**Telegram 快速配置**:
1. 搜索 @BotFather，发送 `/newbot`
2. 获取 Bot Token
3. 发送 `/start` 给你的机器人
4. 访问 `https://api.telegram.org/bot<TOKEN>/getUpdates` 获取 Chat ID
5. 在应用中添加机器人配置

**启用双向对话**（可选）:
```bash
# 启动 Webhook 服务
./deploy_bot_webhook.sh

# 使用 ngrok 暴露服务
ngrok http 8001

# 设置 Webhook
curl -X POST "https://api.telegram.org/bot<TOKEN>/setWebhook" \
  -d '{"url": "https://your-ngrok-url.ngrok.io/webhook/telegram/<TOKEN>"}'
```

### 4. 🧠 AI 交易助手

**功能**
- 创建交易策略
- 运行策略回测
- 设置价格预警
- 分析市场行情
- 优化策略参数

**使用方式**

**Web 界面**:
1. 点击顶部"🧠 AI助手"
2. 输入问题或指令
3. AI 自动处理并执行

**社交平台**（需配置 Webhook）:
```
在 Telegram/Discord/Slack 直接发消息
你: 分析市场
机器人: 技术分析：趋势上涨... ✅
```

### 5. 📰 新闻展示与分析
- 实时新闻列表
- 情绪分类（利好/利空/中性）
- 图表标记联动
- 新闻筛选

### 6. 🎯 策略回测系统
- MA 移动平均线策略
- RSI 策略
- 详细回测报告
- 性能指标

---

## 部署指南

### 开发环境

```bash
# 前端
npm run dev

# 后端 API（可选）
cd python-engine
python main.py

# Webhook 服务（可选，用于机器人对话）
./deploy_bot_webhook.sh
```

### 生产构建

```bash
# Web 版本
npm run build

# 桌面应用
npm run tauri:build

# Docker
docker build -t stocks-trading .
```

### CI/CD

**GitHub Actions 自动运行**:
- 测试 Python 后端
- 测试前端构建
- 构建多平台版本
- 构建 Docker 镜像

**配置 Docker Hub 推送**（可选）:
1. 在 GitHub 仓库设置中添加 Secrets:
   - `DOCKER_USERNAME`
   - `DOCKER_PASSWORD`

---

## 开发文档

### 项目结构

```
stocks/
├── src/                    # 前端源码
│   ├── components/         # React 组件
│   │   ├── AlertPanel.tsx      # 价格预警
│   │   ├── BotSettings.tsx     # 机器人配置
│   │   ├── AIAssistant.tsx     # AI 助手
│   │   ├── NewsPanel.tsx       # 新闻面板
│   │   └── ...
│   ├── App.tsx            # 主应用
│   └── main.tsx
├── python-engine/         # Python 后端
│   ├── main.py           # 主 API 服务
│   └── bot_webhook.py    # Webhook 服务
├── .github/workflows/     # CI/CD
└── docs/                  # 文档
```

### 技术栈

**前端**:
- React 19 + TypeScript
- Vite
- Recharts (图表)
- Monaco Editor (代码编辑)

**后端**:
- Python + FastAPI
- CCXT (交易所接口)
- SQLite (数据存储)

**桌面应用**:
- Tauri 2 + Rust

### 添加新功能

**1. 添加新的 MCP 工具**

编辑 `src/components/AIAssistant.tsx`:
```typescript
// 添加新工具处理逻辑
if (lowerPrompt.includes('新功能')) {
  return AIResponse({
    message: "处理结果...",
    actions: [{
      type: 'new_action',
      data: { ... }
    }]
  })
}
```

**2. 添加新的社交平台**

编辑 `python-engine/bot_webhook.py`:
```python
@app.post("/webhook/newplatform")
async def newplatform_webhook(request: Request):
    data = await request.json()
    # 处理消息
    ai_response = await process_ai_request(...)
    # 发送回复
    return {"ok": True}
```

### 本地测试

```bash
# 测试前端
npm run build

# 测试 Python 后端
cd python-engine
pip install pytest
pytest

# 测试 Webhook 服务
python test_bot_webhook.py
```

---

## 常见问题

### Q: 如何配置 Telegram 机器人？
A: 参考上面的"社交媒体机器人"章节。

### Q: 双向对话和单向通知有什么区别？
A: 
- 单向通知：只能接收预警推送
- 双向对话：可以发消息与 AI 交互

### Q: 必须配置机器人吗？
A: 不是必须的，机器人是可选功能。

### Q: CI/CD 失败怎么办？
A: 
- Rust/Tauri: 会自动跳过（如果没有 src-tauri）
- Docker: 会只构建不推送（如果没有配置凭证）

### Q: 如何接入真实 AI API？
A: 修改 `AIAssistant.tsx` 中的 `callAI` 函数，调用 Claude/GPT-4 API。

---

## 贡献指南

欢迎提交 PR！

1. Fork 项目
2. 创建功能分支
3. 提交更改
4. 推送到分支
5. 创建 Pull Request

---

## 许可证

ISC License

---

## 更新日志

### v2.0.1 (2026-06-16)
- ✅ 修复 GitHub Actions CI 错误
- ✅ 添加 Rust/Tauri 目录检查
- ✅ 添加 Docker 凭证检查

### v2.0.0 (2026-06-16)
- ✅ 添加社交媒体机器人双向对话
- ✅ 添加 AI 交易助手
- ✅ 添加 Webhook 服务

### v1.0.0 (2026-06-15)
- ✅ 初始版本发布
- ✅ 实时行情、价格预警、新闻分析

---

**版本**: v2.0.1  
**更新**: 2026-06-16  
**作者**: Powered by Claude Code

© 2026 量化交易系统
