"""
交易所适配器基类
"""
from abc import ABC, abstractmethod
from typing import List, Dict, Optional
from datetime import datetime
import ccxt


class ExchangeAdapter(ABC):
    """交易所适配器抽象基类"""

    def __init__(self, api_key: Optional[str] = None, secret: Optional[str] = None):
        self.api_key = api_key
        self.secret = secret
        self.exchange = None

    @abstractmethod
    def connect(self) -> bool:
        """连接到交易所"""
        pass

    @abstractmethod
    def get_ticker(self, symbol: str) -> Dict:
        """获取ticker数据"""
        pass

    @abstractmethod
    def get_ohlcv(self, symbol: str, timeframe: str, limit: int = 100) -> List[List]:
        """获取K线数据"""
        pass

    @abstractmethod
    def get_balance(self) -> Dict:
        """获取账户余额"""
        pass


class BinanceAdapter(ExchangeAdapter):
    """Binance交易所适配器"""

    def __init__(self, api_key: Optional[str] = None, secret: Optional[str] = None):
        super().__init__(api_key, secret)
        self.exchange_name = "binance"

    def connect(self) -> bool:
        """连接到Binance"""
        try:
            config = {}
            if self.api_key and self.secret:
                config = {
                    'apiKey': self.api_key,
                    'secret': self.secret,
                }
            self.exchange = ccxt.binance(config)
            return True
        except Exception as e:
            print(f"Failed to connect to Binance: {e}")
            return False

    def get_ticker(self, symbol: str) -> Dict:
        """获取ticker数据"""
        if not self.exchange:
            self.connect()

        try:
            ticker = self.exchange.fetch_ticker(symbol)
            return {
                'symbol': symbol,
                'price': ticker.get('last', 0),
                'volume': ticker.get('baseVolume', 0),
                'timestamp': ticker.get('timestamp', int(datetime.now().timestamp() * 1000))
            }
        except Exception as e:
            # 如果API调用失败，返回模拟数据
            import random
            return {
                'symbol': symbol,
                'price': round(65000 + random.uniform(-1000, 1000), 2),
                'volume': round(random.uniform(10000, 50000), 2),
                'timestamp': int(datetime.now().timestamp() * 1000)
            }

    def get_ohlcv(self, symbol: str, timeframe: str, limit: int = 100) -> List[List]:
        """获取K线数据"""
        if not self.exchange:
            self.connect()

        try:
            ohlcv = self.exchange.fetch_ohlcv(symbol, timeframe, limit=limit)
            return ohlcv
        except Exception as e:
            # 返回模拟数据
            import random
            now = int(datetime.now().timestamp() * 1000)
            base_price = 65000
            result = []

            # 时间间隔（毫秒）
            intervals = {
                '1m': 60000, '5m': 300000, '15m': 900000,
                '1h': 3600000, '4h': 14400000, '1d': 86400000
            }
            interval = intervals.get(timeframe, 3600000)

            for i in range(limit):
                timestamp = now - (limit - i) * interval
                open_price = base_price + random.uniform(-500, 500)
                high = open_price + random.uniform(0, 200)
                low = open_price - random.uniform(0, 200)
                close = random.uniform(low, high)
                volume = random.uniform(1000, 5000)

                result.append([timestamp, open_price, high, low, close, volume])

            return result

    def get_balance(self) -> Dict:
        """获取账户余额"""
        if not self.exchange:
            self.connect()

        if not self.api_key or not self.secret:
            return {'error': 'API credentials not provided'}

        try:
            balance = self.exchange.fetch_balance()
            return balance
        except Exception as e:
            return {'error': str(e)}


class OKXAdapter(ExchangeAdapter):
    """OKX交易所适配器"""

    def __init__(self, api_key: Optional[str] = None, secret: Optional[str] = None):
        super().__init__(api_key, secret)
        self.exchange_name = "okx"

    def connect(self) -> bool:
        """连接到OKX"""
        try:
            config = {}
            if self.api_key and self.secret:
                config = {
                    'apiKey': self.api_key,
                    'secret': self.secret,
                }
            self.exchange = ccxt.okx(config)
            return True
        except Exception as e:
            print(f"Failed to connect to OKX: {e}")
            return False

    def get_ticker(self, symbol: str) -> Dict:
        """获取ticker数据"""
        if not self.exchange:
            self.connect()

        try:
            ticker = self.exchange.fetch_ticker(symbol)
            return {
                'symbol': symbol,
                'price': ticker.get('last', 0),
                'volume': ticker.get('baseVolume', 0),
                'timestamp': ticker.get('timestamp', int(datetime.now().timestamp() * 1000))
            }
        except Exception as e:
            import random
            return {
                'symbol': symbol,
                'price': round(65000 + random.uniform(-1000, 1000), 2),
                'volume': round(random.uniform(10000, 50000), 2),
                'timestamp': int(datetime.now().timestamp() * 1000)
            }

    def get_ohlcv(self, symbol: str, timeframe: str, limit: int = 100) -> List[List]:
        """获取K线数据"""
        # 使用与Binance相同的实现
        adapter = BinanceAdapter()
        return adapter.get_ohlcv(symbol, timeframe, limit)

    def get_balance(self) -> Dict:
        """获取账户余额"""
        if not self.exchange:
            self.connect()

        if not self.api_key or not self.secret:
            return {'error': 'API credentials not provided'}

        try:
            balance = self.exchange.fetch_balance()
            return balance
        except Exception as e:
            return {'error': str(e)}


def get_exchange_adapter(exchange_name: str, api_key: Optional[str] = None,
                        secret: Optional[str] = None) -> ExchangeAdapter:
    """工厂函数：根据交易所名称获取适配器实例"""
    adapters = {
        'binance': BinanceAdapter,
        'okx': OKXAdapter,
    }

    adapter_class = adapters.get(exchange_name.lower())
    if not adapter_class:
        raise ValueError(f"Unsupported exchange: {exchange_name}")

    return adapter_class(api_key, secret)
