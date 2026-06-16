"""
交易策略基类
"""
from abc import ABC, abstractmethod
import pandas as pd
from typing import Optional


class Strategy(ABC):
    """策略抽象基类"""

    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def on_data(self, data: pd.DataFrame, index: int) -> Optional[str]:
        """
        处理每个K线数据

        Args:
            data: 完整的OHLCV数据（带指标）
            index: 当前处理的索引

        Returns:
            'BUY', 'SELL', 或 None
        """
        pass


class SimpleMAStrategy(Strategy):
    """简单双均线策略"""

    def __init__(self, short_period: int = 10, long_period: int = 20):
        super().__init__("Simple MA Strategy")
        self.short_period = short_period
        self.long_period = long_period

    def on_data(self, data: pd.DataFrame, index: int) -> Optional[str]:
        """
        双均线交叉策略：
        - 短期均线上穿长期均线 -> 买入
        - 短期均线下穿长期均线 -> 卖出
        """
        if index < self.long_period:
            return None

        # 获取当前和前一个均线值
        short_ma = data[f'sma_{self.short_period}'].iloc[index]
        long_ma = data[f'sma_{self.long_period}'].iloc[index]

        prev_short_ma = data[f'sma_{self.short_period}'].iloc[index - 1]
        prev_long_ma = data[f'sma_{self.long_period}'].iloc[index - 1]

        # 检查金叉（买入信号）
        if prev_short_ma <= prev_long_ma and short_ma > long_ma:
            return 'BUY'

        # 检查死叉（卖出信号）
        if prev_short_ma >= prev_long_ma and short_ma < long_ma:
            return 'SELL'

        return None


class RSIStrategy(Strategy):
    """RSI策略"""

    def __init__(self, oversold: float = 30, overbought: float = 70):
        super().__init__("RSI Strategy")
        self.oversold = oversold
        self.overbought = overbought

    def on_data(self, data: pd.DataFrame, index: int) -> Optional[str]:
        """
        RSI策略：
        - RSI < 30 -> 买入（超卖）
        - RSI > 70 -> 卖出（超买）
        """
        if index < 14:  # RSI需要至少14个数据点
            return None

        rsi = data['rsi'].iloc[index]

        if pd.isna(rsi):
            return None

        if rsi < self.oversold:
            return 'BUY'
        elif rsi > self.overbought:
            return 'SELL'

        return None


class MACDStrategy(Strategy):
    """MACD策略"""

    def __init__(self):
        super().__init__("MACD Strategy")

    def on_data(self, data: pd.DataFrame, index: int) -> Optional[str]:
        """
        MACD策略：
        - MACD上穿信号线 -> 买入
        - MACD下穿信号线 -> 卖出
        """
        if index < 26:  # MACD需要至少26个数据点
            return None

        macd = data['macd'].iloc[index]
        signal = data['macd_signal'].iloc[index]

        prev_macd = data['macd'].iloc[index - 1]
        prev_signal = data['macd_signal'].iloc[index - 1]

        if pd.isna(macd) or pd.isna(signal):
            return None

        # MACD上穿信号线
        if prev_macd <= prev_signal and macd > signal:
            return 'BUY'

        # MACD下穿信号线
        if prev_macd >= prev_signal and macd < signal:
            return 'SELL'

        return None
