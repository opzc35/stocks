from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from core.ai.analyzer import get_analyzer
from core.data.history import get_data_manager
from core.indicators import IndicatorEngine

router = APIRouter()


class AnalyzeRequest(BaseModel):
    symbol: str
    exchange: str = "binance"
    timeframe: str = "1h"
    limit: int = 100


class BacktestAnalyzeRequest(BaseModel):
    results: dict


@router.post("/analyze")
async def analyze_market(request: AnalyzeRequest):
    """AI市场分析"""
    try:
        # 获取历史数据
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
                detail=f"Insufficient data for analysis. Found {len(data) if data else 0} candles."
            )

        # 反转数据并计算指标
        data.reverse()
        engine = IndicatorEngine(data)
        engine.add_all_indicators()
        latest_indicators = engine.get_latest_indicators()

        # 获取当前价格
        current_price = latest_indicators['close']

        # 使用Claude AI分析
        analyzer = get_analyzer()
        analysis = analyzer.analyze_market(
            request.symbol,
            current_price,
            latest_indicators,
            data[-50:]  # 最近50条数据
        )

        return analysis

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/analyze-backtest")
async def analyze_backtest(request: BacktestAnalyzeRequest):
    """分析回测结果"""
    try:
        analyzer = get_analyzer()
        analysis = analyzer.analyze_backtest_results(request.results)

        return analysis

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/status")
async def ai_status():
    """检查AI功能状态"""
    analyzer = get_analyzer()

    return {
        "available": analyzer.available,
        "model": "claude-opus-4-8" if analyzer.available else "rule-based-fallback",
        "message": "Claude AI is configured and ready" if analyzer.available else "ANTHROPIC_API_KEY not set, using fallback analysis"
    }
