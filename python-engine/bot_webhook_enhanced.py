"""
社交媒体机器人增强版 - 支持图片发送和批注

新功能：
- 生成K线图表
- 添加技术指标
- 图表批注（趋势线、标记等）
- 发送到各平台
"""

from fastapi import FastAPI, Request, BackgroundTasks
from pydantic import BaseModel
from typing import Optional, Dict, Any, List
import json
import io
import base64
from datetime import datetime, timedelta
import matplotlib
matplotlib.use('Agg')  # 无 GUI 后端
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.patches import Rectangle, FancyArrow
import numpy as np

app = FastAPI()

class ChartAnnotation(BaseModel):
    """图表批注"""
    type: str  # 'text', 'arrow', 'line', 'box'
    position: Dict[str, float]  # {'x': timestamp, 'y': price}
    text: Optional[str] = None
    color: str = 'red'
    style: Optional[str] = None

class ChartConfig(BaseModel):
    """图表配置"""
    symbol: str = 'BTC/USDT'
    timeframe: str = '1h'
    periods: int = 100
    indicators: List[str] = ['MA20', 'MA50', 'RSI']
    annotations: List[ChartAnnotation] = []
    title: Optional[str] = None

async def generate_chart(config: ChartConfig) -> bytes:
    """
    生成K线图表（带批注）

    返回：PNG 图片的字节数据
    """
    # 模拟K线数据（实际应该从数据库或API获取）
    np.random.seed(42)
    dates = [datetime.now() - timedelta(hours=i) for i in range(config.periods, 0, -1)]

    # 生成模拟价格数据
    base_price = 67500
    prices = []
    current = base_price

    for _ in range(config.periods):
        change = np.random.randn() * 500
        current = current + change
        prices.append(current)

    # 创建图表
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10),
                                     gridspec_kw={'height_ratios': [3, 1]})
    fig.patch.set_facecolor('#000000')

    # 主图 - K线和均线
    ax1.set_facecolor('#0a0a0a')
    ax1.plot(dates, prices, color='#00f2fe', linewidth=2, label='Price', alpha=0.8)

    # 添加移动平均线
    if 'MA20' in config.indicators:
        ma20 = np.convolve(prices, np.ones(20)/20, mode='valid')
        ax1.plot(dates[19:], ma20, color='#f6d365', linewidth=1.5,
                label='MA20', alpha=0.7)

    if 'MA50' in config.indicators:
        ma50 = np.convolve(prices, np.ones(50)/50, mode='valid')
        ax1.plot(dates[49:], ma50, color='#f857a6', linewidth=1.5,
                label='MA50', alpha=0.7)

    # 添加批注
    for ann in config.annotations:
        if ann.type == 'text':
            # 文字批注
            ax1.annotate(
                ann.text,
                xy=(ann.position['x'], ann.position['y']),
                xytext=(10, 10),
                textcoords='offset points',
                color=ann.color,
                fontsize=12,
                fontweight='bold',
                bbox=dict(boxstyle='round,pad=0.5', fc='black', ec=ann.color, alpha=0.8),
                arrowprops=dict(arrowstyle='->', color=ann.color, lw=2)
            )

        elif ann.type == 'arrow':
            # 箭头批注
            ax1.annotate(
                '',
                xy=(ann.position['x'], ann.position['y']),
                xytext=(ann.position.get('x2', ann.position['x']),
                       ann.position.get('y2', ann.position['y'] * 0.95)),
                arrowprops=dict(
                    arrowstyle='->',
                    color=ann.color,
                    lw=3,
                    connectionstyle='arc3,rad=0.3'
                )
            )

        elif ann.type == 'line':
            # 趋势线
            x_start = ann.position['x']
            x_end = ann.position.get('x2', x_start)
            y_start = ann.position['y']
            y_end = ann.position.get('y2', y_start)
            ax1.plot([x_start, x_end], [y_start, y_end],
                    color=ann.color, linewidth=2, linestyle='--', alpha=0.8)

        elif ann.type == 'box':
            # 方框标记
            width = ann.position.get('width', 10)
            height = ann.position.get('height', 1000)
            rect = Rectangle(
                (ann.position['x'], ann.position['y']),
                width, height,
                linewidth=2,
                edgecolor=ann.color,
                facecolor='none',
                linestyle='--'
            )
            ax1.add_patch(rect)

    # 设置主图样式
    ax1.set_title(config.title or f'{config.symbol} - {config.timeframe}',
                 color='white', fontsize=16, fontweight='bold', pad=20)
    ax1.set_ylabel('Price (USDT)', color='white', fontsize=12)
    ax1.tick_params(colors='white')
    ax1.grid(True, alpha=0.2, color='#333333')
    ax1.legend(loc='upper left', facecolor='#0a0a0a', edgecolor='#333333',
              labelcolor='white')
    ax1.spines['bottom'].set_color('#333333')
    ax1.spines['top'].set_color('#333333')
    ax1.spines['left'].set_color('#333333')
    ax1.spines['right'].set_color('#333333')

    # 副图 - RSI
    if 'RSI' in config.indicators:
        ax2.set_facecolor('#0a0a0a')
        # 模拟 RSI 数据
        rsi = 50 + np.random.randn(config.periods) * 15
        rsi = np.clip(rsi, 0, 100)
        ax2.plot(dates, rsi, color='#0070f3', linewidth=2, label='RSI')
        ax2.axhline(y=70, color='#f857a6', linestyle='--', linewidth=1, alpha=0.5)
        ax2.axhline(y=30, color='#0ba360', linestyle='--', linewidth=1, alpha=0.5)
        ax2.fill_between(dates, 70, 100, color='#f857a6', alpha=0.1)
        ax2.fill_between(dates, 0, 30, color='#0ba360', alpha=0.1)
        ax2.set_ylabel('RSI', color='white', fontsize=12)
        ax2.set_ylim(0, 100)
        ax2.tick_params(colors='white')
        ax2.grid(True, alpha=0.2, color='#333333')
        ax2.legend(loc='upper left', facecolor='#0a0a0a', edgecolor='#333333',
                  labelcolor='white')
        ax2.spines['bottom'].set_color('#333333')
        ax2.spines['top'].set_color('#333333')
        ax2.spines['left'].set_color('#333333')
        ax2.spines['right'].set_color('#333333')

    # 格式化时间轴
    ax2.xaxis.set_major_formatter(mdates.DateFormatter('%m/%d %H:%M'))
    ax2.xaxis.set_major_locator(mdates.HourLocator(interval=12))
    plt.xticks(rotation=45, ha='right', color='white')

    # 添加水印
    fig.text(0.99, 0.01, f'Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}',
            ha='right', va='bottom', fontsize=8, color='#666666', alpha=0.7)

    plt.tight_layout()

    # 保存为字节流
    buf = io.BytesIO()
    plt.savefig(buf, format='png', dpi=150, facecolor='#000000',
               edgecolor='none', bbox_inches='tight')
    plt.close(fig)
    buf.seek(0)

    return buf.read()


async def send_telegram_photo(bot_token: str, chat_id: int, photo_bytes: bytes, caption: str = None):
    """发送 Telegram 图片"""
    import httpx

    url = f"https://api.telegram.org/bot{bot_token}/sendPhoto"

    files = {'photo': ('chart.png', photo_bytes, 'image/png')}
    data = {'chat_id': chat_id}

    if caption:
        data['caption'] = caption
        data['parse_mode'] = 'Markdown'

    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.post(url, files=files, data=data)
        return response.json()


async def send_discord_photo(webhook_url: str, photo_bytes: bytes, content: str = None):
    """发送 Discord 图片"""
    import httpx

    files = {'file': ('chart.png', photo_bytes, 'image/png')}
    data = {}

    if content:
        data['content'] = content

    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.post(webhook_url, files=files, data=data)
        return response.json()


async def send_slack_photo(webhook_url: str, photo_bytes: bytes, text: str = None):
    """发送 Slack 图片（需要使用 files.upload API）"""
    import httpx

    # 注意：Slack Webhook 不支持直接发送文件
    # 需要使用 Slack API 的 files.upload 端点
    # 这里提供一个基础实现

    # 将图片转为 base64
    import base64
    photo_base64 = base64.b64encode(photo_bytes).decode()

    # 作为消息附件发送（简化版）
    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.post(webhook_url, json={
            'text': text or '📊 市场分析图表',
            'blocks': [
                {
                    'type': 'section',
                    'text': {
                        'type': 'mrkdwn',
                        'text': text or '📊 市场分析图表'
                    }
                },
                {
                    'type': 'image',
                    'image_url': f'data:image/png;base64,{photo_base64[:100]}...',  # 简化
                    'alt_text': '图表'
                }
            ]
        })
        return response.json()


async def send_wechat_photo(webhook_url: str, photo_bytes: bytes, content: str = None):
    """发送企业微信图片"""
    import httpx
    import base64

    # 企业微信需要先上传图片，获取 media_id
    # 这里提供一个简化实现，实际需要调用上传接口

    photo_base64 = base64.b64encode(photo_bytes).decode()

    async with httpx.AsyncClient(timeout=30.0) as client:
        # 发送图片消息（简化版，实际需要 media_id）
        response = await client.post(webhook_url, json={
            'msgtype': 'image',
            'image': {
                'base64': photo_base64,
                'md5': ''  # 需要计算 MD5
            }
        })
        return response.json()


# API 端点

@app.post("/api/chart/generate")
async def generate_chart_api(config: ChartConfig):
    """生成图表 API"""
    try:
        image_bytes = await generate_chart(config)

        # 转为 base64 返回
        image_base64 = base64.b64encode(image_bytes).decode()

        return {
            "success": True,
            "data": {
                "image": image_base64,
                "format": "png",
                "size": len(image_bytes)
            }
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


@app.post("/api/chart/send")
async def send_chart_api(
    platform: str,
    config: ChartConfig,
    bot_config: Dict[str, Any],
    caption: Optional[str] = None
):
    """发送图表到社交媒体平台"""
    try:
        # 生成图表
        image_bytes = await generate_chart(config)

        # 根据平台发送
        if platform == 'telegram':
            result = await send_telegram_photo(
                bot_config['bot_token'],
                bot_config['chat_id'],
                image_bytes,
                caption
            )

        elif platform == 'discord':
            result = await send_discord_photo(
                bot_config['webhook_url'],
                image_bytes,
                caption
            )

        elif platform == 'slack':
            result = await send_slack_photo(
                bot_config['webhook_url'],
                image_bytes,
                caption
            )

        elif platform == 'wechat':
            result = await send_wechat_photo(
                bot_config['webhook_url'],
                image_bytes,
                caption
            )

        else:
            return {
                "success": False,
                "error": f"Unsupported platform: {platform}"
            }

        return {
            "success": True,
            "platform": platform,
            "result": result
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


# Webhook 端点更新 - 支持图表请求

@app.post("/webhook/telegram/{bot_token}")
async def telegram_webhook_enhanced(bot_token: str, request: Request, background_tasks: BackgroundTasks):
    """处理 Telegram 消息（增强版）"""

    data = await request.json()

    if 'message' in data:
        message = data['message']
        chat_id = message['chat']['id']
        text = message.get('text', '')

        # 检查是否请求图表
        if any(keyword in text.lower() for keyword in ['图表', 'chart', 'k线', '走势图', '分析图']):

            # 创建图表配置
            chart_config = ChartConfig(
                symbol='BTC/USDT',
                timeframe='1h',
                periods=100,
                indicators=['MA20', 'MA50', 'RSI'],
                annotations=[
                    ChartAnnotation(
                        type='text',
                        position={'x': 50, 'y': 68000},
                        text='📈 突破阻力位',
                        color='#0ba360'
                    ),
                    ChartAnnotation(
                        type='arrow',
                        position={'x': 70, 'y': 69000, 'x2': 70, 'y2': 67500},
                        color='#f857a6'
                    )
                ],
                title='BTC/USDT 技术分析'
            )

            # 生成并发送图表
            image_bytes = await generate_chart(chart_config)

            caption = """📊 **BTC/USDT 技术分析**

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
"""

            await send_telegram_photo(bot_token, chat_id, image_bytes, caption)

            return {"ok": True}

    return {"ok": True}


@app.get("/health")
async def health_check():
    return {
        "status": "ok",
        "service": "bot-webhook-enhanced",
        "features": ["chart_generation", "annotations", "multi_platform"]
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
