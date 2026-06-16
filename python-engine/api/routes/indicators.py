from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List
from core.data.history import get_data_manager
from core.indicators import IndicatorEngine

router = APIRouter()


class IndicatorRequest(BaseModel):
    symbol: str
    exchange: str = "binance"
    timeframe: str = "1h"
    limit: int = 100


@router.post("/calculate")
async def calculate_indicators(request: IndicatorRequest):
    """计算技术指标"""
    try:
        # 从数据库获取历史数据
        manager = await get_data_manager()
        data = await manager.get_data(
            request.symbol,
            request.exchange,
            request.timeframe,
            limit=request.limit
        )

        if not data:
            raise HTTPException(
                status_code=404,
                detail="No data found. Please sync data first."
            )

        # 反转数据（从旧到新）
        data.reverse()

        # 计算指标
        engine = IndicatorEngine(data)
        df = engine.add_all_indicators()

        # 获取最新指标值
        latest = engine.get_latest_indicators()

        return {
            "success": True,
            "symbol": request.symbol,
            "latest_indicators": latest,
            "data_points": len(df)
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/latest")
async def get_latest_indicators(request: IndicatorRequest):
    """获取最新的技术指标值"""
    try:
        manager = await get_data_manager()
        data = await manager.get_data(
            request.symbol,
            request.exchange,
            request.timeframe,
            limit=request.limit
        )

        if not data:
            raise HTTPException(
                status_code=404,
                detail="No data found"
            )

        data.reverse()

        engine = IndicatorEngine(data)
        engine.add_all_indicators()
        latest = engine.get_latest_indicators()

        return latest

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
