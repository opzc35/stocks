"""
历史数据管理系统
"""
from typing import List, Dict, Optional
from datetime import datetime, timedelta
from core.data.database import get_database
from core.exchanges.adapter import get_exchange_adapter


class HistoricalDataManager:
    """历史数据管理器"""

    def __init__(self):
        self.db = None

    async def initialize(self):
        """初始化数据库连接"""
        self.db = await get_database()

    async def fetch_and_store(
        self,
        symbol: str,
        exchange: str,
        timeframe: str,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        limit: int = 1000
    ) -> Dict:
        """
        从交易所获取历史数据并存储到数据库

        Args:
            symbol: 交易对符号
            exchange: 交易所名称
            timeframe: 时间周期
            start_date: 开始日期（可选）
            end_date: 结束日期（可选）
            limit: 数据条数限制

        Returns:
            包含状态信息的字典
        """
        if not self.db:
            await self.initialize()

        try:
            # 获取交易所适配器
            adapter = get_exchange_adapter(exchange)

            # 获取OHLCV数据
            ohlcv_data = adapter.get_ohlcv(symbol, timeframe, limit)

            if not ohlcv_data:
                return {
                    "success": False,
                    "message": "No data retrieved from exchange",
                    "count": 0
                }

            # 存储到数据库
            count = await self.db.save_market_data(
                symbol, exchange, timeframe, ohlcv_data
            )

            return {
                "success": True,
                "message": f"Successfully stored {count} candles",
                "count": count,
                "symbol": symbol,
                "exchange": exchange,
                "timeframe": timeframe
            }

        except Exception as e:
            return {
                "success": False,
                "message": f"Error fetching data: {str(e)}",
                "count": 0
            }

    async def get_data(
        self,
        symbol: str,
        exchange: str,
        timeframe: str,
        start_time: Optional[int] = None,
        end_time: Optional[int] = None,
        limit: int = 1000
    ) -> List[Dict]:
        """
        从数据库获取历史数据

        Args:
            symbol: 交易对符号
            exchange: 交易所名称
            timeframe: 时间周期
            start_time: 开始时间戳（毫秒）
            end_time: 结束时间戳（毫秒）
            limit: 数据条数限制

        Returns:
            OHLCV数据列表
        """
        if not self.db:
            await self.initialize()

        return await self.db.get_market_data(
            symbol, exchange, timeframe, start_time, end_time, limit
        )

    async def sync_data(
        self,
        symbol: str,
        exchange: str,
        timeframe: str,
        days_back: int = 30
    ) -> Dict:
        """
        同步最近N天的历史数据

        Args:
            symbol: 交易对符号
            exchange: 交易所名称
            timeframe: 时间周期
            days_back: 回溯天数

        Returns:
            同步结果
        """
        # 计算需要的数据条数
        timeframe_minutes = {
            '1m': 1, '5m': 5, '15m': 15, '30m': 30,
            '1h': 60, '4h': 240, '1d': 1440
        }

        minutes = timeframe_minutes.get(timeframe, 60)
        candles_needed = (days_back * 24 * 60) // minutes

        return await self.fetch_and_store(
            symbol, exchange, timeframe, limit=candles_needed
        )


# 全局实例
_manager_instance: Optional[HistoricalDataManager] = None


async def get_data_manager() -> HistoricalDataManager:
    """获取数据管理器实例（单例）"""
    global _manager_instance

    if _manager_instance is None:
        _manager_instance = HistoricalDataManager()
        await _manager_instance.initialize()

    return _manager_instance
