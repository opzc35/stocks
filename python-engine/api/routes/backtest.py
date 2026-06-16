from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from core.data.history import get_data_manager
from core.backtest.engine import BacktestEngine
from core.strategy.base import SimpleMAStrategy, RSIStrategy, MACDStrategy

router = APIRouter()


class BacktestRequest(BaseModel):
    symbol: str
    exchange: str = "binance"
    timeframe: str = "1h"
    strategy: str = "simple_ma"  # simple_ma, rsi, macd
    initial_capital: float = 10000.0
    limit: int = 500


@router.post("/run")
async def run_backtest(request: BacktestRequest):
    """运行策略回测"""
    try:
        # 从数据库获取历史数据
        manager = await get_data_manager()
        data = await manager.get_data(
            request.symbol,
            request.exchange,
            request.timeframe,
            limit=request.limit
        )

        if not data or len(data) < 50:
            raise HTTPException(
                status_code=404,
                detail=f"Insufficient data. Found {len(data) if data else 0} candles, need at least 50."
            )

        # 反转数据（从旧到新）
        data.reverse()

        # 选择策略
        if request.strategy == "simple_ma":
            strategy = SimpleMAStrategy(short_period=10, long_period=20)
        elif request.strategy == "rsi":
            strategy = RSIStrategy(oversold=30, overbought=70)
        elif request.strategy == "macd":
            strategy = MACDStrategy()
        else:
            raise HTTPException(status_code=400, detail=f"Unknown strategy: {request.strategy}")

        # 运行回测
        engine = BacktestEngine(initial_capital=request.initial_capital)
        results = engine.run(data, strategy)

        return {
            "success": True,
            "strategy": request.strategy,
            "symbol": request.symbol,
            "timeframe": request.timeframe,
            "data_points": len(data),
            "results": results
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/strategies")
async def list_strategies():
    """列出可用的策略"""
    return {
        "strategies": [
            {
                "id": "simple_ma",
                "name": "Simple MA Strategy",
                "description": "双均线交叉策略：短期均线上穿长期均线买入，下穿卖出"
            },
            {
                "id": "rsi",
                "name": "RSI Strategy",
                "description": "RSI策略：RSI < 30超卖买入，RSI > 70超买卖出"
            },
            {
                "id": "macd",
                "name": "MACD Strategy",
                "description": "MACD策略：MACD上穿信号线买入，下穿卖出"
            }
        ]
    }
