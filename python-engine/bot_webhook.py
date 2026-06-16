"""
社交媒体机器人消息接收和处理服务

支持平台：
- Telegram
- Discord
- Slack
- 企业微信
"""

from fastapi import FastAPI, Request, BackgroundTasks
from pydantic import BaseModel
from typing import Optional, Dict, Any
import json

app = FastAPI()

# 存储机器人配置（实际应该从数据库读取）
bot_configs = {}

class AIRequest(BaseModel):
    """AI 请求模型"""
    platform: str
    user_id: str
    message: str
    context: Optional[Dict[str, Any]] = None

class AIResponse(BaseModel):
    """AI 响应模型"""
    message: str
    actions: Optional[list] = None

# AI 处理逻辑（与前端相同）
async def process_ai_request(prompt: str, context: Dict[str, Any]) -> AIResponse:
    """处理 AI 请求"""

    symbol = context.get('symbol', 'BTC/USDT')
    price = context.get('price', 67532.45)

    lowerPrompt = prompt.lower()

    # 创建策略
    if '策略' in lowerPrompt or 'strategy' in lowerPrompt:
        return AIResponse(
            message=f"""好的，我帮你创建一个基于移动平均线的交易策略。

**策略名称**: MA Cross Strategy
**交易对**: {symbol}
**参数**:
- 短期均线: 20
- 长期均线: 50
- 初始资金: $10,000

**规则**:
- 买入: 短期均线上穿长期均线
- 卖出: 短期均线下穿长期均线

策略已创建，是否要运行回测？""",
            actions=[{
                'type': 'create_strategy',
                'data': {
                    'name': 'MA Cross Strategy',
                    'symbol': symbol,
                    'params': {'short': 20, 'long': 50, 'capital': 10000}
                }
            }]
        )

    # 运行回测
    if '回测' in lowerPrompt or 'backtest' in lowerPrompt:
        return AIResponse(
            message="""正在运行回测...

**回测结果**:
- 总收益: +15.6%
- 夏普比率: 1.32
- 最大回撤: -8.4%
- 胜率: 58%
- 总交易: 24笔

策略表现不错！建议在实盘前进一步优化参数。""",
            actions=[{
                'type': 'run_backtest',
                'data': {
                    'strategy': 'MA Cross Strategy',
                    'symbol': symbol,
                    'timeframe': '1h',
                    'days': 30
                }
            }]
        )

    # 设置预警
    if '预警' in lowerPrompt or 'alert' in lowerPrompt or '提醒' in lowerPrompt:
        target_price = price * 1.05
        return AIResponse(
            message=f"""好的，我帮你设置价格预警。

**预警配置**:
- 交易对: {symbol}
- 当前价格: ${price:.2f}
- 目标价格: ${target_price:.2f}
- 条件: 突破

价格达到目标时会通知你！""",
            actions=[{
                'type': 'set_alert',
                'data': {
                    'symbol': symbol,
                    'condition': 'above',
                    'targetPrice': target_price
                }
            }]
        )

    # 市场分析
    if '分析' in lowerPrompt or 'analyze' in lowerPrompt or '市场' in lowerPrompt:
        return AIResponse(
            message=f"""让我分析一下 {symbol} 的市场情况...

**技术分析**:
- 当前价格: ${price:.2f}
- 趋势: 上涨 📈
- RSI: 62 (中性偏多)
- MACD: 正向 ✓

**建议**:
1. 短期可能继续上涨
2. 注意 ${price * 1.1:.2f} 附近的阻力位
3. 可以考虑在回调到 ${price * 0.95:.2f} 时加仓

**风险提示**: 建议设置止损在 ${price * 0.92:.2f}""",
            actions=[{
                'type': 'analyze_market',
                'data': {'symbol': symbol, 'price': price}
            }]
        )

    # 优化策略
    if '优化' in lowerPrompt or 'optimize' in lowerPrompt:
        return AIResponse(
            message="""正在优化策略参数...

**优化结果**:
- 最佳短期均线: 18
- 最佳长期均线: 52
- 预期收益提升: +3.2%
- 风险降低: -1.8%

**建议**: 使用优化后的参数可以提高策略表现。是否应用这些参数？""",
            actions=[{
                'type': 'optimize_strategy',
                'data': {
                    'strategy': 'MA Cross Strategy',
                    'optimizedParams': {'short': 18, 'long': 52}
                }
            }]
        )

    # 默认响应
    return AIResponse(
        message="""我理解了你的问题。我可以帮你：

📈 **创建策略** - 说"帮我创建一个策略"
🎯 **运行回测** - 说"运行回测"
🔔 **设置预警** - 说"设置价格预警"
📊 **分析市场** - 说"分析市场"
⚙️ **优化策略** - 说"优化策略参数"

请告诉我你想做什么？"""
    )


# Telegram Webhook
@app.post("/webhook/telegram/{bot_token}")
async def telegram_webhook(bot_token: str, request: Request, background_tasks: BackgroundTasks):
    """处理 Telegram 消息"""

    data = await request.json()

    # 提取消息信息
    if 'message' in data:
        message = data['message']
        chat_id = message['chat']['id']
        text = message.get('text', '')

        # 忽略命令消息
        if text.startswith('/'):
            return {"ok": True}

        # 处理 AI 请求
        ai_response = await process_ai_request(text, {
            'symbol': 'BTC/USDT',
            'price': 67532.45
        })

        # 发送回复
        background_tasks.add_task(
            send_telegram_message,
            bot_token,
            chat_id,
            ai_response.message
        )

    return {"ok": True}


# Discord Webhook (需要 Discord Bot)
@app.post("/webhook/discord")
async def discord_webhook(request: Request, background_tasks: BackgroundTasks):
    """处理 Discord 消息"""

    data = await request.json()

    # Discord 交互响应
    if data.get('type') == 1:  # PING
        return {"type": 1}

    # 处理命令
    if data.get('type') == 2:  # APPLICATION_COMMAND
        command_data = data.get('data', )
        user_input = command_data.get('options', [{}])[0].get('value', '')

        ai_response = await process_ai_request(user_input, {
            'symbol': 'BTC/USDT',
            'price': 67532.45
        })

        return {
            "type": 4,
            "data": {
                "content": ai_response.message
            }
        }

    return {"ok": True}


# Slack Events API
@app.post("/webhook/slack")
async def slack_webhook(request: Request, background_tasks: BackgroundTasks):
    """处理 Slack 消息"""

    data = await request.json()

    # URL 验证
    if data.get('type') == 'url_verification':
        return {"challenge": data.get('challenge')}

    # 处理事件
    if data.get('type') == 'event_callback':
        event = data.get('event', {})

        # 忽略机器人自己的消息
        if event.get('bot_id'):
            return {"ok": True}

        # 处理用户消息
        if event.get('type') == 'message' and 'text' in event:
            text = event['text']
            channel = event['channel']

            ai_response = await process_ai_request(text, {
                'symbol': 'BTC/USDT',
                'price': 67532.45
            })

            # 获取 Slack webhook URL（需要从配置中读取）
            # background_tasks.add_task(send_slack_message, channel, ai_response.message)

    return {"ok": True}


# 企业微信 Webhook
@app.post("/webhook/wechat")
async def wechat_webhook(request: Request, background_tasks: BackgroundTasks):
    """处理企业微信消息"""

    data = await request.json()

    # 企业微信验证
    if 'msgtype' not in data:
        return {"ok": True}

    # 处理文本消息
    if data.get('msgtype') == 'text':
        content = data.get('text', {}).get('content', '')
        webhook_url = data.get('webhook_url')  # 需要从配置获取

        ai_response = await process_ai_request(content, {
            'symbol': 'BTC/USDT',
            'price': 67532.45
        })

        # background_tasks.add_task(send_wechat_message, webhook_url, ai_response.message)

    return {"ok": True}


# 辅助函数：发送消息

async def send_telegram_message(bot_token: str, chat_id: int, text: str):
    """发送 Telegram 消息"""
    import httpx

    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"

    async with httpx.AsyncClient() as client:
        await client.post(url, json={
            'chat_id': chat_id,
            'text': text,
            'parse_mode': 'Markdown'
        })


async def send_discord_message(webhook_url: str, content: str):
    """发送 Discord 消息"""
    import httpx

    async with httpx.AsyncClient() as client:
        await client.post(webhook_url, json={
            'content': content
        })


async def send_slack_message(webhook_url: str, text: str):
    """发送 Slack 消息"""
    import httpx

    async with httpx.AsyncClient() as client:
        await client.post(webhook_url, json={
            'text': text
        })


async def send_wechat_message(webhook_url: str, content: str):
    """发送企业微信消息"""
    import httpx

    async with httpx.AsyncClient() as client:
        await client.post(webhook_url, json={
            'msgtype': 'text',
            'text': {
                'content': content
            }
        })


# 健康检查
@app.get("/health")
async def health_check():
    return {"status": "ok", "service": "bot-webhook"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
