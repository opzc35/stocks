# 社交媒体机器人双向对话功能

## 概述

现在你的社交媒体机器人不仅可以发送通知，还可以接收用户消息并智能回复。用户可以直接在 Telegram、Discord、Slack、企业微信中与 AI 助手对话。

## 功能特性

### 双向通信

```
用户 → Telegram/Discord/Slack → Webhook → AI处理 → 回复 → 用户
```

### 支持的操作

用户可以在社交平台上直接对话：

1. **创建策略**
   ```
   用户: 帮我创建一个交易策略
   机器人: 策略已创建...
   ```

2. **运行回测**
   ```
   用户: 运行回测
   机器人: 回测结果: 收益 +15.6%...
   ```

3. **设置预警**
   ```
   用户: 价格涨到70000时提醒我
   机器人: 预警已设置...
   ```

4. **市场分析**
   ```
   用户: 分析一下市场
   机器人: 技术分析: 趋势上涨...
   ```

5. **优化策略**
   ```
   用户: 优化策略参数
   机器人: 最佳参数: 短期18, 长期52...
   ```

## 平台配置

### 1. Telegram Bot

#### 步骤 1：创建 Bot（如之前）
1. 搜索 `@BotFather`
2. 发送 `/newbot`
3. 获取 Bot Token

#### 步骤 2：设置 Webhook

```bash
curl -X POST "https://api.telegram.org/bot<YOUR_BOT_TOKEN>/setWebhook" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://your-domain.com/webhook/telegram/<YOUR_BOT_TOKEN>"
  }'
```

#### 步骤 3：测试对话

1. 在 Telegram 搜索你的机器人
2. 发送 `/start`
3. 发送任意消息，如"帮我创建一个策略"
4. 机器人会智能回复

---

### 2. Discord Bot

#### 步骤 1：创建 Discord Application

1. 访问 [Discord Developer Portal](https://discord.com/developers/applications)
2. 点击 "New Application"
3. 进入 "Bot" 页面，点击 "Add Bot"
4. 复制 Bot Token

#### 步骤 2：创建 Slash Command

1. 进入 "OAuth2" → "URL Generator"
2. 选择 `bot` 和 `applications.commands`
3. 添加权限：`Send Messages`, `Read Messages`
4. 使用生成的 URL 邀请 Bot 到服务器

#### 步骤 3：注册 Slash Command

```bash
curl -X POST "https://discord.com/api/v10/applications/<APP_ID>/commands" \
  -H "Authorization: Bot <BOT_TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "ai",
    "description": "与 AI 交易助手对话",
    "options": [
      {
        "name": "message",
        "description": "你的问题或指令",
        "type": 3,
        "required": true
      }
    ]
  }'
```

#### 步骤 4：设置 Interactions Endpoint

在 Discord Developer Portal 设置：
```
Interactions Endpoint URL: https://your-domain.com/webhook/discord
```

#### 步骤 5：使用

在 Discord 中输入：
```
/ai message: 帮我创建一个策略
```

---

### 3. Slack Bot

#### 步骤 1：创建 Slack App

1. 访问 [Slack API](https://api.slack.com/apps)
2. 点击 "Create New App" → "From scratch"
3. 输入 App 名称，选择工作区

#### 步骤 2：启用 Events API

1. 进入 "Event Subscriptions"
2. 启用 "Enable Events"
3. 设置 Request URL: `https://your-domain.com/webhook/slack`
4. 订阅 Bot Events:
   - `message.channels`
   - `message.groups`
   - `message.im`

#### 步骤 3：添加 Bot Scopes

进入 "OAuth & Permissions"，添加权限：
- `chat:write`
- `channels:history`
- `groups:history`
- `im:history`

#### 步骤 4：安装 App

点击 "Install to Workspace"

#### 步骤 5：使用

1. 邀请机器人到频道：`/invite @YourBot`
2. 在频道中发送消息：`帮我创建一个策略`
3. 机器人会回复

---

### 4. 企业微信 Bot

#### 步骤 1：创建群机器人（如之前）

1. 打开企业微信群聊
2. 添加机器人
3. 获取 Webhook URL

#### 步骤 2：接收消息配置

企业微信群机器人目前只支持主动发送，不支持接收消息。

**替代方案：使用企业微信应用**

1. 在企业微信管理后台创建自建应用
2. 配置接收消息 URL
3. 参考企业微信 API 文档

---

## 后端部署

### 安装依赖

```bash
cd python-engine
pip install fastapi uvicorn httpx
```

### 启动 Webhook 服务

```bash
python bot_webhook.py
```

服务将在 `http://localhost:8001` 启动

### 使用 ngrok 暴露本地服务（开发测试）

```bash
# 安装 ngrok
brew install ngrok  # macOS
# 或从 https://ngrok.com/ 下载

# 启动隧道
ngrok http 8001

# 使用生成的 URL 配置 Webhook
# 例如: https://xxxx.ngrok.io/webhook/telegram/<BOT_TOKEN>
```

### 生产部署

**使用 Docker:**

```dockerfile
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY bot_webhook.py .

CMD ["python", "bot_webhook.py"]
```

```bash
docker build -t trading-bot-webhook .
docker run -d -p 8001:8001 trading-bot-webhook
```

**使用 systemd:**

```ini
[Unit]
Description=Trading Bot Webhook Service
After=network.target

[Service]
Type=simple
User=your-user
WorkingDirectory=/path/to/python-engine
ExecStart=/usr/bin/python3 bot_webhook.py
Restart=always

[Install]
WantedBy=multi-user.target
```

---

## API 端点

### Telegram Webhook
- **URL**: `POST /webhook/telegram/{bot_token}`
- **说明**: 接收 Telegram 消息

### Discord Webhook
- **URL**: `POST /webhook/discord`
- **说明**: 接收 Discord 交互

### Slack Webhook
- **URL**: `POST /webhook/slack`
- **说明**: 接收 Slack 事件

### 企业微信 Webhook
- **URL**: `POST /webhook/wechat`
- **说明**: 接收企业微信消息（需要企业应用）

### 健康检查
- **URL**: `GET /health`
- **响应**: `{"status": "ok", "service": "bot-webhook"}`

---

## 对话示例

### Telegram 对话

```
用户: 你好
机器人: 我理解了你的问题。我可以帮你：
      📈 创建策略
      🎯 运行回测
      🔔 设置预警
      📊 分析市场
      ⚙️ 优化策略

用户: 帮我创建一个策略
机器人: 好的，我帮你创建一个基于移动平均线的交易策略。
      
      策略名称: MA Cross Strategy
      交易对: BTC/USDT
      ...

用户: 运行回测
机器人: 正在运行回测...
      
      回测结果:
      - 总收益: +15.6%
      - 夏普比率: 1.32
      ...

用户: 不错，设置个预警吧
机器人: 好的，我帮你设置价格预警。
      
      预警配置:
      - 交易对: BTC/USDT
      - 目标价格: $70,878.07
      ...
```

---

## 安全考虑

### 1. Webhook 验证

**Telegram:**
- 验证请求来自 Telegram 服务器
- 检查 `X-Telegram-Bot-Api-Secret-Token`

**Discord:**
- 验证请求签名
- 使用 Public Key 验证

**Slack:**
- 验证签名头 `X-Slack-Signature`
- 检查时间戳防止重放攻击

### 2. 速率限制

```python
from fastapi import HTTPException
from collections import defaultdict
import time

# 简单的速率限制
rate_limits = defaultdict(list)

def check_rate_limit(user_id: str, max_requests: int = 10, window: int = 60):
    """检查速率限制"""
    now = time.time()
    # 清理过期记录
    rate_limits[user_id] = [t for t in rate_limits[user_id] if now - t < window]
    
    if len(rate_limits[user_id]) >= max_requests:
        raise HTTPException(status_code=429, detail="Too many requests")
    
    rate_limits[user_id].append(now)
```

### 3. 消息过滤

```python
def is_safe_message(text: str) -> bool:
    """过滤不安全消息"""
    # 检查长度
    if len(text) > 1000:
        return False
    
    # 检查敏感词
    blocked_words = ['spam', 'scam', ...]
    if any(word in text.lower() for word in blocked_words):
        return False
    
    return True
```

---

## 监控和日志

### 日志记录

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('bot_webhook.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

@app.post("/webhook/telegram/{bot_token}")
async def telegram_webhook(bot_token: str, request: Request):
    data = await request.json()
    logger.info(f"Received Telegram message: {data}")
    # ...
```

### 监控指标

- 消息接收数量
- 响应时间
- 错误率
- 用户活跃度

---

## 故障排除

### Telegram Webhook 不工作

**检查列表:**
1. Webhook URL 是否正确
2. 服务是否可公开访问
3. SSL 证书是否有效
4. 查看 Webhook 信息：
   ```bash
   curl https://api.telegram.org/bot<TOKEN>/getWebhookInfo
   ```

### Discord 交互失败

**检查列表:**
1. Interactions Endpoint URL 是否正确
2. Public Key 是否正确配置
3. Bot 是否有必要权限
4. 查看 Discord Developer Portal 日志

### Slack 事件未接收

**检查列表:**
1. Event Subscriptions 是否启用
2. Request URL 验证是否通过
3. Bot Scopes 是否正确
4. Bot 是否被邀请到频道

---

## 高级功能

### 1. 会话管理

```python
from collections import defaultdict

# 存储用户会话上下文
user_sessions = defaultdict(dict)

async def process_ai_request(prompt: str, user_id: str, context: Dict):
    # 获取用户会话
    session = user_sessions[user_id]
    
    # 添加历史消息
    if 'history' not in session:
        session['history'] = []
    session['history'].append(prompt)
    
    # 处理请求（可以利用历史上下文）
    response = await ai_process(prompt, session)
    
    return response
```

### 2. 多语言支持

```python
def detect_language(text: str) -> str:
    """检测语言"""
    # 简单实现
    if any('一' <= char <= '鿿' for char in text):
        return 'zh'
    return 'en'

async def process_ai_request(prompt: str, context: Dict):
    lang = detect_language(prompt)
    
    # 根据语言返回响应
    if lang == 'zh':
        return "我理解了你的问题..."
    else:
        return "I understand your question..."
```

### 3. 命令系统

```python
COMMANDS = {
    '/help': '显示帮助信息',
    '/status': '查看系统状态',
    '/alerts': '查看我的预警',
    '/strategies': '查看我的策略'
}

async def handle_command(command: str, user_id: str):
    """处理命令"""
    if command == '/help':
        return "可用命令:\n" + "\n".join(
            f"{cmd} - {desc}" for cmd, desc in COMMANDS.items()
        )
    # 其他命令处理...
```

---

## 总结

现在你的社交媒体机器人具备完整的双向通信能力：

✅ **发送通知** - 价格预警触发时推送  
✅ **接收消息** - 用户可以主动发消息  
✅ **AI 处理** - 智能理解和回复  
✅ **动作执行** - 自动执行用户请求  
✅ **多平台支持** - Telegram/Discord/Slack  

用户可以在任何平台上与 AI 助手对话，无需打开网页！🎉
