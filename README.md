# 📊 量化交易系统

一个功能完整、支持 AI 智能交互和社交媒体双向对话的现代化量化交易平台。

[![CI/CD](https://github.com/yourusername/stocks/workflows/CI%2FCD%20Pipeline/badge.svg)](https://github.com/yourusername/stocks/actions)

## ✨ 核心功能

- 📊 **实时行情监控** - 多交易对、K线图表、技术指标
- 🔔 **智能价格预警** - 突破/跌破预警、多渠道通知
- 🤖 **社交媒体机器人** - 4平台支持、双向对话
- 🧠 **AI 交易助手** - 自然语言交互、自动执行
- 📰 **新闻展示分析** - 情绪分类、图表联动
- 🎯 **策略回测系统** - 多种策略、详细报告

## 🚀 快速开始

```bash
# 安装依赖
npm install

# 启动开发服务器
npm run dev

# 访问应用
http://localhost:5173/
```

## 📚 完整文档

查看 [完整文档](./docs/DOCUMENTATION.md) 了解：
- 详细功能说明
- 配置指南（Telegram/Discord/Slack 机器人）
- 部署教程
- 开发文档

## 🎯 主要特性

### 🧠 AI 交易助手

与 AI 对话，自动执行操作：
```
你: 帮我创建一个策略
AI: 策略已创建 ✅

你: 运行回测
AI: 回测完成，收益 +15.6% ✅

你: 价格涨到70000时提醒我
AI: 预警已设置 ✅
```

### 🤖 社交媒体机器人

**单向通知**：价格预警推送到 Telegram/Discord/Slack  
**双向对话**：在社交平台直接与 AI 交互

支持平台：📱 Telegram | 💬 Discord | 💼 Slack | 💚 企业微信

示例对话：
```
你: 分析市场
机器人: 技术分析：趋势上涨，RSI 62... ✅
```

### 🔔 价格预警系统

- 设置突破/跌破预警
- 多渠道通知（浏览器 + 机器人）
- 实时状态追踪
- 预警管理

## 🛠️ 技术栈

- **前端**: React 19 + TypeScript + Vite
- **后端**: Python + FastAPI
- **桌面**: Tauri 2 + Rust
- **AI**: MCP 协议集成
- **CI/CD**: GitHub Actions

## 📦 部署

### Web 应用
```bash
npm run build
```

### 桌面应用
```bash
npm run tauri:build
```

### Docker
```bash
docker build -t stocks-trading ./python-engine
```

### 机器人 Webhook（可选）
```bash
./deploy_bot_webhook.sh
```

## 📸 截图

（TODO: 添加截图）

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

1. Fork 本项目
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

## 📄 许可证

ISC License

## 📞 支持

- 📖 [完整文档](./docs/DOCUMENTATION.md)
- 🐛 [提交 Issue](https://github.com/yourusername/stocks/issues)
- 💬 [Discussions](https://github.com/yourusername/stocks/discussions)

---

**版本**: v2.0.1  
**更新**: 2026-06-16  
**作者**: Powered by Claude Code

© 2026 量化交易系统
