#!/usr/bin/env python3
"""
测试机器人 API 接口
"""

import requests
import json

BASE_URL = "http://localhost:8000"

def test_bot_api():
    """测试机器人 API"""
    print("=" * 60)
    print("🤖 测试机器人 API 接口")
    print("=" * 60)
    print()

    # 测试案例 1: 无效的 Telegram Bot Token
    print("📱 测试 1: Telegram - 无效 Token")
    test_config = {
        "id": "test1",
        "platform": "telegram",
        "name": "测试机器人",
        "enabled": True,
        "config": {
            "botToken": "123456:ABC-invalid-token",
            "chatId": "123456789"
        }
    }

    response = requests.post(
        f"{BASE_URL}/api/bot/test",
        json=test_config
    )

    print(f"   状态码: {response.status_code}")
    try:
        result = response.json()
        print(f"   完整响应: {json.dumps(result, ensure_ascii=False, indent=2)}")
        print(f"   成功: {result.get('success', 'N/A')}")
        if 'message' in result:
            print(f"   消息: {result['message']}")
    except Exception as e:
        print(f"   响应解析失败: {e}")
        print(f"   原始响应: {response.text}")
    print()

    # 测试案例 2: Discord Webhook (无效)
    print("💬 测试 2: Discord - 无效 Webhook")
    test_config = {
        "id": "test2",
        "platform": "discord",
        "name": "Discord 机器人",
        "enabled": True,
        "config": {
            "webhookUrl": "https://discord.com/api/webhooks/invalid"
        }
    }

    response = requests.post(
        f"{BASE_URL}/api/bot/test",
        json=test_config
    )

    print(f"   状态码: {response.status_code}")
    try:
        result = response.json()
        print(f"   完整响应: {json.dumps(result, ensure_ascii=False, indent=2)}")
        print(f"   成功: {result.get('success', 'N/A')}")
        if 'message' in result:
            print(f"   消息: {result['message']}")
    except Exception as e:
        print(f"   响应解析失败: {e}")
        print(f"   原始响应: {response.text}")
    print()

    # 测试案例 3: 缺少必填字段
    print("⚠️  测试 3: Telegram - 缺少 Bot Token")
    test_config = {
        "id": "test3",
        "platform": "telegram",
        "name": "测试机器人",
        "enabled": True,
        "config": {
            "chatId": "123456789"
        }
    }

    response = requests.post(
        f"{BASE_URL}/api/bot/test",
        json=test_config
    )

    print(f"   状态码: {response.status_code}")
    try:
        result = response.json()
        print(f"   完整响应: {json.dumps(result, ensure_ascii=False, indent=2)}")
        print(f"   成功: {result.get('success', 'N/A')}")
        if 'message' in result:
            print(f"   消息: {result['message']}")
    except Exception as e:
        print(f"   响应解析失败: {e}")
        print(f"   原始响应: {response.text}")
    print()

    print("=" * 60)
    print("✅ API 接口测试完成！")
    print("=" * 60)
    print()
    print("💡 提示：")
    print("   - 前端点击测试按钮会调用 /api/bot/test 接口")
    print("   - 接口会验证 Bot Token 是否有效")
    print("   - 如果有 Chat ID，会尝试发送测试消息")
    print("   - 需要使用真实的 Bot Token 才能测试成功")
    print()

if __name__ == "__main__":
    try:
        test_bot_api()
    except requests.exceptions.ConnectionError:
        print()
        print("❌ 无法连接到 API 服务")
        print("   请确保主 API 服务正在运行:")
        print("   cd python-engine && python main.py")
        print()
    except Exception as e:
        print()
        print(f"❌ 测试失败: {e}")
        print()
