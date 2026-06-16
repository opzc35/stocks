# Telegram 机器人配置和测试指南

## 问题解决

之前"测试失败"的问题已经修复！

### 原因
前端调用 `/api/bot/test` 接口，但后端没有实现该接口。

### 解决方案
1. ✅ 创建了 `/python-engine/api/routes/bot.py` - 机器人测试接口
2. ✅ 在 `main.py` 中注册了路由
3. ✅ 主 API 服务已重启（运行在 http://localhost:8000）

## 如何获取 Telegram Bot Token

### 步骤 1: 创建机器人

1. 在 Telegram 中搜索 `@BotFather`
2. 发送命令：`/newbot`
3. 按提示输入机器人名称和用户名
4. BotFather 会返回一个 Token，格式类似：
   ```
   123456789:ABCdefGHIjklMNOpqrsTUVwxyz
   ```

### 步骤 2: 获取 Chat ID

**方法 1: 使用 @userinfobot**
1. 在 Telegram 中搜索 `@userinfobot`
2. 向它发送任意消息
3. 它会返回你的 Chat ID

**方法 2: 使用 API**
1. 先向你的机器人发送一条消息
2. 访问：`https://api.telegram.org/bot<你的token>/getUpdates`
3. 在返回的 JSON 中查找 `"chat":{"id":123456789}`

### 步骤 3: 在前端配置

1. 打开前端页面的**机器人设置**
2. 点击 **"+ 添加机器人"**
3. 选择 **Telegram**
4. 填写：
   - 机器人名称：例如 "交易预警机器人"
   - Bot Token：从 BotFather 获取的 token
   - Chat ID：你的 Chat ID
5. 点击**保存**
6. 点击**测试**按钮

## 测试按钮的工作流程

当你点击测试按钮时：

1. 前端调用 `POST /api/bot/test`
2. 后端验证 Bot Token 是否有效
3. 如果提供了 Chat ID，发送测试消息到 Telegram
4. 返回测试结果

## 测试结果说明

### ✅ 测试成功
- Bot Token 有效
- 成功发送测试消息到你的 Telegram
- 你会收到一条消息：`✅ 测试成功！机器人 @你的机器人 已成功连接。`

### ❌ 测试失败 - 常见原因

1. **"Bot Token 无效或已过期"**
   - Token 输入错误
   - Token 已被撤销
   - 解决：重新从 BotFather 获取 token

2. **"无法发送消息到 Chat ID"**
   - Chat ID 错误
   - 没有向机器人发送过消息（需要先 /start）
   - 解决：确保 Chat ID 正确，并先向机器人发送 /start

3. **"连接 Telegram API 超时"**
   - 网络问题
   - 防火墙阻止
   - 解决：检查网络连接

## 测试 API 接口

### 使用测试脚本
```bash
cd /workspaces/stocks
python test_bot_api.py
```

### 手动测试
```bash
curl -X POST http://localhost:8000/api/bot/test \
  -H "Content-Type: application/json" \
  -d '{
    "id": "test123",
    "platform": "telegram",
    "name": "测试机器人",
    "enabled": true,
    "config": {
      "botToken": "你的token",
      "chatId": "你的chat_id"
    }
  }'
```

## 支持的平台

### ✅ Telegram
- 需要：Bot Token, Chat ID
- 测试：发送实际消息

### ✅ Discord
- 需要：Webhook URL
- 测试：发送测试消息

### ✅ Slack
- 需要：Webhook URL
- 测试：发送测试消息

### ✅ 企业微信
- 需要：Webhook URL
- 测试：发送测试消息

## 服务状态检查

### 检查主 API 服务
```bash
curl http://localhost:8000/health
# 应该返回: {"status": "ok"}
```

### 检查 Webhook 服务
```bash
curl http://localhost:8001/health
# 应该返回: {"status": "ok", "service": "bot-webhook"}
```

### 查看服务进程
```bash
ps aux | grep python | grep -E "main.py|bot_webhook.py"
```

## 故障排除

### 1. API 服务未启动
```bash
cd /workspaces/stocks/python-engine
python main.py
```

### 2. 前端无法连接 API
- 确认 API 运行在 localhost:8000
- 检查 CORS 配置
- 查看浏览器控制台错误

### 3. 测试一直显示"测试中..."
- 检查网络连接
- 查看 API 日志：`cat /tmp/main_api.log`
- 检查 Bot Token 格式是否正确

## 下一步

配置成功后，机器人可以：
- 接收交易预警通知
- 响应用户命令
- 发送市场分析
- 执行策略操作

webhook 服务（8001端口）负责接收来自 Telegram 的消息，主 API 服务（8000端口）负责测试和管理机器人配置。
