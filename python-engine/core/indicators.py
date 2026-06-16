"""
技术指标计算引擎
"""
import pandas as pd
import numpy as np
from typing import List, Dict, Optional


class TechnicalIndicators:
    """技术指标计算类"""

    @staticmethod
    def calculate_sma(data: pd.Series, period: int) -> pd.Series:
        """
        计算简单移动平均线 (SMA)

        Args:
            data: 价格序列
            period: 周期

        Returns:
            SMA序列
        """
        return data.rolling(window=period).mean()

    @staticmethod
    def calculate_ema(data: pd.Series, period: int) -> pd.Series:
        """
        计算指数移动平均线 (EMA)

        Args:
            data: 价格序列
            period: 周期

        Returns:
            EMA序列
        """
        return data.ewm(span=period, adjust=False).mean()

    @staticmethod
    def calculate_rsi(data: pd.Series, period: int = 14) -> pd.Series:
        """
        计算相对强弱指标 (RSI)

        Args:
            data: 价格序列
            period: 周期（默认14）

        Returns:
            RSI序列
        """
        delta = data.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()

        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))

        return rsi

    @staticmethod
    def calculate_macd(data: pd.Series,
                       fast_period: int = 12,
                       slow_period: int = 26,
                       signal_period: int = 9) -> Dict[str, pd.Series]:
        """
        计算MACD指标

        Args:
            data: 价格序列
            fast_period: 快线周期
            slow_period: 慢线周期
            signal_period: 信号线周期

        Returns:
            包含macd, signal, histogram的字典
        """
        ema_fast = data.ewm(span=fast_period, adjust=False).mean()
        ema_slow = data.ewm(span=slow_period, adjust=False).mean()

        macd_line = ema_fast - ema_slow
        signal_line = macd_line.ewm(span=signal_period, adjust=False).mean()
        histogram = macd_line - signal_line

        return {
            'macd': macd_line,
            'signal': signal_line,
            'histogram': histogram
        }

    @staticmethod
    def calculate_bollinger_bands(data: pd.Series,
                                   period: int = 20,
                                   std_dev: float = 2.0) -> Dict[str, pd.Series]:
        """
        计算布林带

        Args:
            data: 价格序列
            period: 周期
            std_dev: 标准差倍数

        Returns:
            包含upper, middle, lower的字典
        """
        middle = data.rolling(window=period).mean()
        std = data.rolling(window=period).std()

        upper = middle + (std * std_dev)
        lower = middle - (std * std_dev)

        return {
            'upper': upper,
            'middle': middle,
            'lower': lower
        }

    @staticmethod
    def calculate_atr(high: pd.Series,
                      low: pd.Series,
                      close: pd.Series,
                      period: int = 14) -> pd.Series:
        """
        计算平均真实波幅 (ATR)

        Args:
            high: 最高价序列
            low: 最低价序列
            close: 收盘价序列
            period: 周期

        Returns:
            ATR序列
        """
        tr1 = high - low
        tr2 = abs(high - close.shift())
        tr3 = abs(low - close.shift())

        tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
        atr = tr.rolling(window=period).mean()

        return atr

    @staticmethod
    def calculate_stochastic(high: pd.Series,
                            low: pd.Series,
                            close: pd.Series,
                            k_period: int = 14,
                            d_period: int = 3) -> Dict[str, pd.Series]:
        """
        计算随机指标 (Stochastic)

        Args:
            high: 最高价序列
            low: 最低价序列
            close: 收盘价序列
            k_period: K线周期
            d_period: D线周期

        Returns:
            包含k和d的字典
        """
        lowest_low = low.rolling(window=k_period).min()
        highest_high = high.rolling(window=k_period).max()

        k = 100 * (close - lowest_low) / (highest_high - lowest_low)
        d = k.rolling(window=d_period).mean()

        return {
            'k': k,
            'd': d
        }

    @staticmethod
    def calculate_adx(high: pd.Series,
                     low: pd.Series,
                     close: pd.Series,
                     period: int = 14) -> pd.Series:
        """
        计算平均趋向指标 (ADX)

        Args:
            high: 最高价序列
            low: 最低价序列
            close: 收盘价序列
            period: 周期

        Returns:
            ADX序列
        """
        # 计算+DM和-DM
        high_diff = high.diff()
        low_diff = -low.diff()

        plus_dm = high_diff.where((high_diff > low_diff) & (high_diff > 0), 0)
        minus_dm = low_diff.where((low_diff > high_diff) & (low_diff > 0), 0)

        # 计算TR
        tr1 = high - low
        tr2 = abs(high - close.shift())
        tr3 = abs(low - close.shift())
        tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)

        # 平滑
        atr = tr.rolling(window=period).mean()
        plus_di = 100 * (plus_dm.rolling(window=period).mean() / atr)
        minus_di = 100 * (minus_dm.rolling(window=period).mean() / atr)

        # 计算DX和ADX
        dx = 100 * abs(plus_di - minus_di) / (plus_di + minus_di)
        adx = dx.rolling(window=period).mean()

        return adx


class IndicatorEngine:
    """指标引擎 - 对OHLCV数据批量计算指标"""

    def __init__(self, ohlcv_data: List[Dict]):
        """
        初始化指标引擎

        Args:
            ohlcv_data: OHLCV数据列表
        """
        self.df = pd.DataFrame(ohlcv_data)
        self.indicators = TechnicalIndicators()

    def add_all_indicators(self) -> pd.DataFrame:
        """添加所有常用指标到DataFrame"""

        # 移动平均线 - 添加更多周期
        self.df['sma_10'] = self.indicators.calculate_sma(self.df['close'], 10)
        self.df['sma_20'] = self.indicators.calculate_sma(self.df['close'], 20)
        self.df['sma_50'] = self.indicators.calculate_sma(self.df['close'], 50)
        self.df['ema_12'] = self.indicators.calculate_ema(self.df['close'], 12)
        self.df['ema_26'] = self.indicators.calculate_ema(self.df['close'], 26)

        # RSI
        self.df['rsi'] = self.indicators.calculate_rsi(self.df['close'])

        # MACD
        macd = self.indicators.calculate_macd(self.df['close'])
        self.df['macd'] = macd['macd']
        self.df['macd_signal'] = macd['signal']
        self.df['macd_histogram'] = macd['histogram']

        # 布林带
        bb = self.indicators.calculate_bollinger_bands(self.df['close'])
        self.df['bb_upper'] = bb['upper']
        self.df['bb_middle'] = bb['middle']
        self.df['bb_lower'] = bb['lower']

        # ATR
        self.df['atr'] = self.indicators.calculate_atr(
            self.df['high'], self.df['low'], self.df['close']
        )

        # 随机指标
        stoch = self.indicators.calculate_stochastic(
            self.df['high'], self.df['low'], self.df['close']
        )
        self.df['stoch_k'] = stoch['k']
        self.df['stoch_d'] = stoch['d']

        # ADX
        self.df['adx'] = self.indicators.calculate_adx(
            self.df['high'], self.df['low'], self.df['close']
        )

        return self.df

    def get_latest_indicators(self) -> Dict:
        """获取最新的指标值"""
        if self.df.empty:
            return {}

        latest = self.df.iloc[-1]
        return {
            'timestamp': int(latest['timestamp']),
            'close': float(latest['close']),
            'sma_20': float(latest['sma_20']) if pd.notna(latest['sma_20']) else None,
            'sma_50': float(latest['sma_50']) if pd.notna(latest['sma_50']) else None,
            'ema_12': float(latest['ema_12']) if pd.notna(latest['ema_12']) else None,
            'ema_26': float(latest['ema_26']) if pd.notna(latest['ema_26']) else None,
            'rsi': float(latest['rsi']) if pd.notna(latest['rsi']) else None,
            'macd': float(latest['macd']) if pd.notna(latest['macd']) else None,
            'macd_signal': float(latest['macd_signal']) if pd.notna(latest['macd_signal']) else None,
            'bb_upper': float(latest['bb_upper']) if pd.notna(latest['bb_upper']) else None,
            'bb_middle': float(latest['bb_middle']) if pd.notna(latest['bb_middle']) else None,
            'bb_lower': float(latest['bb_lower']) if pd.notna(latest['bb_lower']) else None,
            'atr': float(latest['atr']) if pd.notna(latest['atr']) else None,
            'stoch_k': float(latest['stoch_k']) if pd.notna(latest['stoch_k']) else None,
            'stoch_d': float(latest['stoch_d']) if pd.notna(latest['stoch_d']) else None,
            'adx': float(latest['adx']) if pd.notna(latest['adx']) else None,
        }

    def to_dict(self) -> List[Dict]:
        """转换为字典列表"""
        return self.df.to_dict('records')
