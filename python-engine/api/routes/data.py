from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from core.data.history import get_data_manager

router = APIRouter()


class DataSyncRequest(BaseModel):
    symbol: str
    exchange: str = "binance"
    timeframe: str = "1h"
    days_back: int = 30


class DataQueryRequest(BaseModel):
    symbol: str
    exchange: str = "binance"
    timeframe: str = "1h"
    start_time: Optional[int] = None
    end_time: Optional[int] = None
    limit: int = 1000


@router.post("/sync")
async def sync_historical_data(request: DataSyncRequest):
    """同步历史数据到数据库"""
    try:
        manager = await get_data_manager()
        result = await manager.sync_data(
            request.symbol,
            request.exchange,
            request.timeframe,
            request.days_back
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/query")
async def query_historical_data(request: DataQueryRequest):
    """从数据库查询历史数据"""
    try:
        manager = await get_data_manager()
        data = await manager.get_data(
            request.symbol,
            request.exchange,
            request.timeframe,
            request.start_time,
            request.end_time,
            request.limit
        )
        return {"data": data, "count": len(data)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
