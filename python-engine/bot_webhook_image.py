"""
社交媒体机器人 - 支持图片识别

扩展功能：
- 接收用户发送的图片
- 自动分析K线图
- 智能回复分析结果
"""

from fastapi import FastAPI, Request, BackgroundTasks
from pydantic import BaseModel
from typing import Optional, Dict, Any
import httpx
import base64

# 导入图片分析模块
from image_analyzer import process_image_message, ImageAnalyzer

app = FastAPI()

# Telegram 增强版 - 支持图片
@app.post("/webhook/telegram/{bot_token}")
async def telegram_webhook_with_image(bot_token: str, request: Request, background_tasks: BackgroundTasks):
    """处理 Telegram 消息（支持图片）"""

    data = await request.json()

    if 'message' in data:
        message = data['message']
        chat_id = message['chat']['id']

        # 处理图片消息
        if 'photo' in message:
            # 获取最高清晰度的图片
            photos = message['photo']
            largest_photo = max(photos, key=lambda p: p['file_size'])
            file_id = largest_photo['file_id']

            # 获取用户附带的文字
            caption = message.get('caption', '')

            # 下载图片
            image_data = await download_telegram_photo(bot_token, file_id)

            if image_data:
                # 分析图片
                response = await process_image_message(image_data, caption)

                # 发送回复
                background_tasks.add_task(
                    send_telegram_message,
                    bot_token,
                    chat_id,
                    response
                )
            else:
                background_tasks.add_task(
                    send_telegram_message,
                    bot_token,
                    chat_id,
                    "❌ 图片下载失败，请重试"
                )

        # 处理文字消息
        elif 'text' in message:
            text = message['text']

            # 检查是否请求图表
            if any(keyword in text.lower() for keyword in ['图表', 'chart', 'k线', '走势图']):
                # ... 原有的图表生成逻辑 ...
                pass
            else:
                # ... 原有的AI对话逻辑 ...
                pass

    return {"ok": True}


# Discord 增强版 - 支持图片
@app.post("/webhook/discord")
async def discord_webhook_with_image(request: Request, background_tasks: BackgroundTasks):
    """处理 Discord 消息（支持图片）"""

    data = await request.json()

    # Discord 交互响应
    if data.get('type') == 1:  # PING
        return {"type": 1}

    # 处理消息
    if data.get('type') == 2:  # APPLICATION_COMMAND
        command_data = data.get('data', {})

        # 检查是否有附件
        if 'resolved' in data and 'attachments' in data['resolved']:
            attachments = data['resolved']['attachments']

            for attachment_id, attachment in attachments.items():
                url = attachment.get('url')
                content_type = attachment.get('content_type', '')

                # 只处理图片
                if content_type.startswith('image/'):
                    # 下载图片
                    image_data = await download_image_from_url(url)

                    if image_data:
                        # 分析图片
                        user_message = command_data.get('options', [{}])[0].get('value', '')
                        response = await process_image_message(image_data, user_message)

                        return {
                            "type": 4,
                            "data": {
                                "content": response
                            }
                        }

        # 普通命令处理
        user_input = command_data.get('options', [{}])[0].get('value', '')
        # ... 原有逻辑 ...

    return {"ok": True}


# Slack 增强版 - 支持图片
@app.post("/webhook/slack")
async def slack_webhook_with_image(request: Request, background_tasks: BackgroundTasks):
    """处理 Slack 消息（支持图片）"""

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

        # 处理文件上传
        if event.get('type') == 'message' and 'files' in event:
            files = event['files']

            for file_info in files:
                mime_type = file_info.get('mimetype', '')

                # 只处理图片
                if mime_type.startswith('image/'):
                    # Slack 需要认证才能下载，这里简化处理
                    url_private = file_info.get('url_private')

                    # 下载图片（需要 Slack token）
                    # image_data = await download_slack_file(url_private, slack_token)

                    # 分析图片
                    text = event.get('text', '')
                    # response = await process_image_message(image_data, text)

                    # 发送回复
                    # ...

        # 处理普通消息
        elif event.get('type') == 'message' and 'text' in event:
            # ... 原有逻辑 ...
            pass

    return {"ok": True}


# 企业微信增强版 - 支持图片
@app.post("/webhook/wechat")
async def wechat_webhook_with_image(request: Request, background_tasks: BackgroundTasks):
    """处理企业微信消息（支持图片）"""

    data = await request.json()

    # 处理图片消息
    if data.get('msgtype') == 'image':
        # 企业微信图片消息
        image_info = data.get('image', {})
        media_id = image_info.get('media_id')

        # 下载图片（需要企业微信 access_token）
        # image_data = await download_wechat_media(media_id, access_token)

        # 分析图片
        # response = await process_image_message(image_data, '')

        # 发送回复
        # ...

    # 处理文本消息
    elif data.get('msgtype') == 'text':
        # ... 原有逻辑 ...
        pass

    return {"ok": True}


# 辅助函数

async def download_telegram_photo(bot_token: str, file_id: str) -> Optional[bytes]:
    """下载 Telegram 图片"""
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            # 获取文件路径
            response = await client.get(
                f"https://api.telegram.org/bot{bot_token}/getFile",
                params={'file_id': file_id}
            )
            result = response.json()

            if result.get('ok'):
                file_path = result['result']['file_path']

                # 下载文件
                file_url = f"https://api.telegram.org/file/bot{bot_token}/{file_path}"
                file_response = await client.get(file_url)

                return file_response.content

    except Exception as e:
        print(f"Error downloading Telegram photo: {e}")

    return None


async def download_image_from_url(url: str) -> Optional[bytes]:
    """从URL下载图片"""
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(url)
            return response.content
    except Exception as e:
        print(f"Error downloading image: {e}")
        return None


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


# 测试端点
@app.post("/api/image/analyze")
async def analyze_image_api(
    image_base64: str,
    message: str = ''
):
    """
    图片分析 API（用于测试）

    参数:
    - image_base64: Base64编码的图片
    - message: 用户附带的消息
    """
    try:
        # 解码图片
        image_data = base64.b64decode(image_base64)

        # 分析图片
        response = await process_image_message(image_data, message)

        return {
            "success": True,
            "analysis": response
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


# 健康检查
@app.get("/health")
async def health_check():
    return {
        "status": "ok",
        "service": "bot-webhook-image-recognition",
        "features": [
            "text_chat",
            "image_recognition",
            "chart_analysis",
            "multi_platform"
        ]
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
