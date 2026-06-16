from fastapi import APIRouter, HTTPException, WebSocket, WebSocketDisconnect
from pydantic import BaseModel
from typing import List, Optional
import sys
import os

# 添加项目根目录到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

from core.exchanges.adapter import get_exchange_adapter
from core.data.realtime import get_streamer

router = APIRouter()


class Ticker(BaseModel):
    symbol: str
    price: float
    volume: float
    timestamp: int


class OHLCV(BaseModel):
    timestamp: int
    open: float
    high: float
    low: float
    close: float
    volume: float


@router.get("/ticker")
async def get_ticker(symbol: str, exchange: str = "binance") -> Ticker:
    """获取实时ticker数据"""
    try:
        adapter = get_exchange_adapter(exchange)
        ticker_data = adapter.get_ticker(symbol)

        return Ticker(**ticker_data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/ohlcv")
async def get_ohlcv(
    symbol: str,
    timeframe: str,
    exchange: str = "binance",
    limit: int = 100
) -> List[OHLCV]:
    """获取K线数据"""
    try:
        adapter = get_exchange_adapter(exchange)
        ohlcv_data = adapter.get_ohlcv(symbol, timeframe, limit)

        return [
            OHLCV(
                timestamp=candle[0],
                open=candle[1],
                high=candle[2],
                low=candle[3],
                close=candle[4],
                volume=candle[5]
            )
            for candle in ohlcv_data
        ]
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/exchanges")
async def list_exchanges():
    """列出支持的交易所"""
    return {
        "exchanges": ["binance", "okx"],
        "count": 2
    }


@router.websocket("/ws/ticker")
async def websocket_ticker(websocket: WebSocket, symbol: str, exchange: str = "binance"):
    """WebSocket实时ticker推送"""
    streamer = get_streamer()
    await streamer.connect(websocket)

    try:
        # 订阅行情
        await streamer.subscribe(websocket, symbol, exchange)

        # 启动数据流（如果还没启动）
        if not streamer.running:
            await streamer.start()

        # 保持连接
        while True:
            # 接收客户端消息（心跳）
            data = await websocket.receive_text()
            if data == "ping":
                await websocket.send_text("pong")

    except WebSocketDisconnect:
        streamer.disconnect(websocket)
        print(f"Client disconnected from {symbol} stream")
