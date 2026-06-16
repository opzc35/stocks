#!/usr/bin/env python3
"""
测试机器人 Webhook 服务
"""

import requests
import json
import time

BASE_URL = "http://localhost:8001"

def test_health():
    """测试健康检查"""
    print("🔍 测试健康检查...")
    response = requests.get(f"{BASE_URL}/health")
    print(f"   状态: {response.status_code}")
    print(f"   响应: {response.json()}")
    print()

def test_telegram_webhook():
    """测试 Telegram Webhook"""
    print("📱 测试 Telegram Webhook...")

    # 模拟 Telegram 消息
    test_message = {
        "update_id": 123456,
        "message": {
            "message_id": 1,
            "from": {
                "id": 123456789,
                "first_name": "测试用户"
            },
            "chat": {
                "id": 123456789,
                "type": "private"
            },
            "date": int(time.time()),
            "text": "帮我创建一个策略"
        }
    }

    response = requests.post(
        f"{BASE_URL}/webhook/telegram/test_bot_token",
        json=test_message
    )

    print(f"   状态: {response.status_code}")
    print(f"   响应: {response.json()}")
    print()

def test_discord_webhook():
    """测试 Discord Webhook"""
    print("💬 测试 Discord Webhook (PING)...")

    # 模拟 Discord PING
    test_ping = {
        "type": 1
    }

    response = requests.post(
        f"{BASE_URL}/webhook/discord",
        json=test_ping
    )

    print(f"   状态: {response.status_code}")
    print(f"   响应: {response.json()}")
    print()

    print("💬 测试 Discord Webhook (命令)...")

    # 模拟 Discord 命令
    test_command = {
        "type": 2,
        "data": {
            "name": "ai",
            "options": [
                {
                    "name": "message",
                    "value": "分析市场"
                }
            ]
        }
    }

    response = requests.post(
        f"{BASE_URL}/webhook/discord",
        json=test_command
    )

    print(f"   状态: {response.status_code}")
    print(f"   响应: {response.json()}")
    print()

def test_slack_webhook():
    """测试 Slack Webhook"""
    print("💼 测试 Slack Webhook (验证)...")

    # 模拟 Slack 验证
    test_challenge = {
        "type": "url_verification",
        "challenge": "test_challenge_string"
    }

    response = requests.post(
        f"{BASE_URL}/webhook/slack",
        json=test_challenge
    )

    print(f"   状态: {response.status_code}")
    print(f"   响应: {response.json()}")
    print()

def test_ai_responses():
    """测试不同的 AI 响应"""
    print("🧠 测试 AI 响应...")

    test_cases = [
        "帮我创建一个策略",
        "运行回测",
        "设置价格预警",
        "分析市场",
        "优化策略"
    ]

    for i, text in enumerate(test_cases, 1):
        print(f"   {i}. 测试: '{text}'")

        test_message = {
            "update_id": 123456 + i,
            "message": {
                "message_id": i,
                "from": {"id": 123456789, "first_name": "测试"},
                "chat": {"id": 123456789, "type": "private"},
                "date": int(time.time()),
                "text": text
            }
        }

        response = requests.post(
            f"{BASE_URL}/webhook/telegram/test_token",
            json=test_message
        )

        if response.status_code == 200:
            print(f"      ✅ 成功")
        else:
            print(f"      ❌ 失败 ({response.status_code})")

        time.sleep(0.5)

    print()

def main():
    print("=" * 50)
    print("🤖 机器人 Webhook 服务测试")
    print("=" * 50)
    print()

    try:
        # 测试健康检查
        test_health()

        # 测试各平台 Webhook
        test_telegram_webhook()
        test_discord_webhook()
        test_slack_webhook()

        # 测试 AI 响应
        test_ai_responses()

        print("=" * 50)
        print("✅ 所有测试完成！")
        print("=" * 50)

    except requests.exceptions.ConnectionError:
        print()
        print("❌ 无法连接到服务")
        print("   请确保 Webhook 服务正在运行:")
        print("   python python-engine/bot_webhook.py")
        print()
    except Exception as e:
        print()
        print(f"❌ 测试失败: {e}")
        print()

if __name__ == "__main__":
    main()
