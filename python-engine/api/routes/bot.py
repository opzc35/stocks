"""
机器人管理 API
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict, Any
import httpx
import asyncio

router = APIRouter()


class BotConfig(BaseModel):
    """机器人配置模型"""
    id: str
    platform: str  # telegram, discord, slack, wechat
    name: str
    enabled: bool
    config: Dict[str, Any]


class BotTestResponse(BaseModel):
    """机器人测试响应"""
    success: bool
    message: str
    details: Optional[Dict[str, Any]] = None


@router.post("/bot/test", response_model=BotTestResponse)
async def test_bot(bot: BotConfig):
    """
    测试机器人配置是否正确
    """

    try:
        if bot.platform == "telegram":
            return await test_telegram_bot(bot)
        elif bot.platform == "discord":
            return await test_discord_bot(bot)
        elif bot.platform == "slack":
            return await test_slack_bot(bot)
        elif bot.platform == "wechat":
            return await test_wechat_bot(bot)
        else:
            raise HTTPException(status_code=400, detail=f"不支持的平台: {bot.platform}")

    except Exception as e:
        return BotTestResponse(
            success=False,
            message=f"测试失败: {str(e)}"
        )


async def test_telegram_bot(bot: BotConfig) -> BotTestResponse:
    """测试 Telegram 机器人"""

    bot_token = bot.config.get("botToken")
    chat_id = bot.config.get("chatId")

    if not bot_token:
        return BotTestResponse(
            success=False,
            message="缺少 Bot Token"
        )

    # 1. 验证 Bot Token 是否有效
    async with httpx.AsyncClient(timeout=10.0) as client:
        try:
            # 获取机器人信息
            response = await client.get(
                f"https://api.telegram.org/bot{bot_token}/getMe"
            )

            if response.status_code != 200:
                return BotTestResponse(
                    success=False,
                    message="Bot Token 无效或已过期"
                )

            result = response.json()
            if not result.get("ok"):
                return BotTestResponse(
                    success=False,
                    message=f"Bot Token 验证失败: {result.get('description', '未知错误')}"
                )

            bot_info = result.get("result", {})
            bot_username = bot_info.get("username", "Unknown")

            # 2. 如果提供了 Chat ID，尝试发送测试消息
            if chat_id:
                test_message = f"✅ 测试成功！\n\n机器人 @{bot_username} 已成功连接。"

                send_response = await client.post(
                    f"https://api.telegram.org/bot{bot_token}/sendMessage",
                    json={
                        "chat_id": chat_id,
                        "text": test_message,
                        "parse_mode": "Markdown"
                    }
                )

                if send_response.status_code != 200:
                    send_result = send_response.json()
                    return BotTestResponse(
                        success=False,
                        message=f"无法发送消息到 Chat ID: {send_result.get('description', '未知错误')}"
                    )

                return BotTestResponse(
                    success=True,
                    message=f"测试消息已发送到 Telegram！",
                    details={
                        "bot_username": bot_username,
                        "bot_name": bot_info.get("first_name"),
                        "chat_id": chat_id
                    }
                )

            # 如果没有 Chat ID，只验证 Token
            return BotTestResponse(
                success=True,
                message=f"Bot Token 有效！机器人: @{bot_username}",
                details={
                    "bot_username": bot_username,
                    "bot_name": bot_info.get("first_name"),
                    "note": "未提供 Chat ID，无法发送测试消息"
                }
            )

        except httpx.TimeoutException:
            return BotTestResponse(
                success=False,
                message="连接 Telegram API 超时，请检查网络连接"
            )
        except Exception as e:
            return BotTestResponse(
                success=False,
                message=f"测试失败: {str(e)}"
            )


async def test_discord_bot(bot: BotConfig) -> BotTestResponse:
    """测试 Discord Webhook"""

    webhook_url = bot.config.get("webhookUrl")

    if not webhook_url:
        return BotTestResponse(
            success=False,
            message="缺少 Webhook URL"
        )

    async with httpx.AsyncClient(timeout=10.0) as client:
        try:
            # 发送测试消息
            response = await client.post(
                webhook_url,
                json={
                    "content": "✅ 测试成功！Discord Webhook 已成功连接。"
                }
            )

            if response.status_code in [200, 204]:
                return BotTestResponse(
                    success=True,
                    message="测试消息已发送到 Discord！"
                )
            else:
                return BotTestResponse(
                    success=False,
                    message=f"Discord Webhook 返回错误 ({response.status_code})"
                )

        except httpx.TimeoutException:
            return BotTestResponse(
                success=False,
                message="连接 Discord 超时，请检查网络连接"
            )
        except Exception as e:
            return BotTestResponse(
                success=False,
                message=f"测试失败: {str(e)}"
            )


async def test_slack_bot(bot: BotConfig) -> BotTestResponse:
    """测试 Slack Webhook"""

    webhook_url = bot.config.get("webhookUrl")

    if not webhook_url:
        return BotTestResponse(
            success=False,
            message="缺少 Webhook URL"
        )

    async with httpx.AsyncClient(timeout=10.0) as client:
        try:
            # 发送测试消息
            response = await client.post(
                webhook_url,
                json={
                    "text": "✅ 测试成功！Slack Webhook 已成功连接。"
                }
            )

            if response.status_code == 200 and response.text == "ok":
                return BotTestResponse(
                    success=True,
                    message="测试消息已发送到 Slack！"
                )
            else:
                return BotTestResponse(
                    success=False,
                    message=f"Slack Webhook 返回错误: {response.text}"
                )

        except httpx.TimeoutException:
            return BotTestResponse(
                success=False,
                message="连接 Slack 超时，请检查网络连接"
            )
        except Exception as e:
            return BotTestResponse(
                success=False,
                message=f"测试失败: {str(e)}"
            )


async def test_wechat_bot(bot: BotConfig) -> BotTestResponse:
    """测试企业微信 Webhook"""

    webhook_url = bot.config.get("webhookUrl")

    if not webhook_url:
        return BotTestResponse(
            success=False,
            message="缺少 Webhook URL"
        )

    async with httpx.AsyncClient(timeout=10.0) as client:
        try:
            # 发送测试消息
            response = await client.post(
                webhook_url,
                json={
                    "msgtype": "text",
                    "text": {
                        "content": "✅ 测试成功！企业微信 Webhook 已成功连接。"
                    }
                }
            )

            if response.status_code == 200:
                result = response.json()
                if result.get("errcode") == 0:
                    return BotTestResponse(
                        success=True,
                        message="测试消息已发送到企业微信！"
                    )
                else:
                    return BotTestResponse(
                        success=False,
                        message=f"企业微信返回错误: {result.get('errmsg', '未知错误')}"
                    )
            else:
                return BotTestResponse(
                    success=False,
                    message=f"企业微信 Webhook 返回错误 ({response.status_code})"
                )

        except httpx.TimeoutException:
            return BotTestResponse(
                success=False,
                message="连接企业微信超时，请检查网络连接"
            )
        except Exception as e:
            return BotTestResponse(
                success=False,
                message=f"测试失败: {str(e)}"
            )
