"""
实时行情推送系统
"""
import asyncio
import json
from typing import Set, Dict
from fastapi import WebSocket
from core.exchanges.adapter import get_exchange_adapter


class MarketDataStreamer:
    """实时市场数据流"""

    def __init__(self):
        # 存储活跃的WebSocket连接
        self.active_connections: Set[WebSocket] = set()
        # 订阅信息 {websocket: {"symbol": str, "exchange": str}}
        self.subscriptions: Dict[WebSocket, Dict] = {}
        self.running = False

    async def connect(self, websocket: WebSocket):
        """接受新的WebSocket连接"""
        await websocket.accept()
        self.active_connections.add(websocket)

    def disconnect(self, websocket: WebSocket):
        """断开WebSocket连接"""
        self.active_connections.discard(websocket)
        self.subscriptions.pop(websocket, None)

    async def subscribe(self, websocket: WebSocket, symbol: str, exchange: str = "binance"):
        """订阅特定交易对的行情"""
        self.subscriptions[websocket] = {
            "symbol": symbol,
            "exchange": exchange
        }

    async def broadcast_ticker(self):
        """广播ticker数据给所有订阅者"""
        while self.running:
            disconnected = set()

            for websocket, sub_info in list(self.subscriptions.items()):
                try:
                    symbol = sub_info["symbol"]
                    exchange = sub_info["exchange"]

                    # 获取最新ticker
                    adapter = get_exchange_adapter(exchange)
                    ticker = adapter.get_ticker(symbol)

                    # 发送数据
                    await websocket.send_json(ticker)

                except Exception as e:
                    print(f"Error sending data to client: {e}")
                    disconnected.add(websocket)

            # 清理断开的连接
            for ws in disconnected:
                self.disconnect(ws)

            # 每秒更新一次
            await asyncio.sleep(1)

    async def start(self):
        """启动数据流"""
        self.running = True
        asyncio.create_task(self.broadcast_ticker())

    async def stop(self):
        """停止数据流"""
        self.running = False


# 全局流实例
_streamer_instance: MarketDataStreamer = None


def get_streamer() -> MarketDataStreamer:
    """获取流实例（单例）"""
    global _streamer_instance

    if _streamer_instance is None:
        _streamer_instance = MarketDataStreamer()

    return _streamer_instance
