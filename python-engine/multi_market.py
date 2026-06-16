"""
多市场数据接口 - 支持加密货币、美股、港股、A股

数据源：
- 加密货币: Binance, CoinGecko
- 美股: Alpha Vantage, Yahoo Finance
- 港股: Yahoo Finance
- A股: Tushare, AKShare
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
import httpx
import asyncio

router = APIRouter(prefix="/api/multi-market", tags=["multi-market"])


class MarketData(BaseModel):
    """市场数据模型"""
    symbol: str
    name: str
    market: str  # crypto, us, hk, cn
    price: float
    change: float
    change_percent: float
    volume: float
    timestamp: int
    currency: str  # USD, HKD, CNY


class Candlestick(BaseModel):
    """K线数据"""
    timestamp: int
    open: float
    high: float
    low: float
    close: float
    volume: float


class SearchResult(BaseModel):
    """搜索结果"""
    symbol: str
    name: str
    market: str
    exchange: str
    currency: str


# ============================================
# 加密货币数据
# ============================================

async def fetch_crypto_data(symbol: str) -> Optional[MarketData]:
    """获取加密货币数据"""
    try:
        # Binance API
        async with httpx.AsyncClient(timeout=10.0) as client:
            # 格式化交易对
            binance_symbol = symbol.replace('/', '').upper()

            # 获取24小时行情
            response = await client.get(
                f"https://api.binance.com/api/v3/ticker/24hr",
                params={'symbol': binance_symbol}
            )

            if response.status_code == 200:
                data = response.json()

                return MarketData(
                    symbol=symbol,
                    name=symbol.split('/')[0],
                    market='crypto',
                    price=float(data['lastPrice']),
                    change=float(data['priceChange']),
                    change_percent=float(data['priceChangePercent']),
                    volume=float(data['volume']),
                    timestamp=int(datetime.now().timestamp() * 1000),
                    currency='USDT'
                )
    except Exception as e:
        print(f"Error fetching crypto data: {e}")

    return None


async def fetch_crypto_klines(symbol: str, interval: str = '1h', limit: int = 100) -> List[Candlestick]:
    """获取加密货币K线"""
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            binance_symbol = symbol.replace('/', '').upper()

            response = await client.get(
                f"https://api.binance.com/api/v3/klines",
                params={
                    'symbol': binance_symbol,
                    'interval': interval,
                    'limit': limit
                }
            )

            if response.status_code == 200:
                data = response.json()
                return [
                    Candlestick(
                        timestamp=int(k[0]),
                        open=float(k[1]),
                        high=float(k[2]),
                        low=float(k[3]),
                        close=float(k[4]),
                        volume=float(k[5])
                    )
                    for k in data
                ]
    except Exception as e:
        print(f"Error fetching crypto klines: {e}")

    return []


# ============================================
# 美股数据
# ============================================

async def fetch_us_stock_data(symbol: str) -> Optional[MarketData]:
    """获取美股数据 (Yahoo Finance)"""
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            # Yahoo Finance API
            response = await client.get(
                f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}",
                params={'interval': '1d', 'range': '1d'}
            )

            if response.status_code == 200:
                data = response.json()
                result = data['chart']['result'][0]
                meta = result['meta']
                quote = result['indicators']['quote'][0]

                current_price = meta['regularMarketPrice']
                previous_close = meta['previousClose']
                change = current_price - previous_close
                change_percent = (change / previous_close) * 100

                return MarketData(
                    symbol=symbol,
                    name=meta.get('longName', symbol),
                    market='us',
                    price=current_price,
                    change=change,
                    change_percent=change_percent,
                    volume=quote['volume'][-1] if quote['volume'] else 0,
                    timestamp=int(datetime.now().timestamp() * 1000),
                    currency='USD'
                )
    except Exception as e:
        print(f"Error fetching US stock data: {e}")

    return None


async def fetch_us_stock_klines(symbol: str, interval: str = '1h', days: int = 7) -> List[Candlestick]:
    """获取美股K线"""
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            # 转换时间间隔
            yahoo_interval = {
                '1m': '1m',
                '5m': '5m',
                '15m': '15m',
                '1h': '1h',
                '1d': '1d'
            }.get(interval, '1h')

            response = await client.get(
                f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}",
                params={
                    'interval': yahoo_interval,
                    'range': f'{days}d'
                }
            )

            if response.status_code == 200:
                data = response.json()
                result = data['chart']['result'][0]
                timestamps = result['timestamp']
                quote = result['indicators']['quote'][0]

                return [
                    Candlestick(
                        timestamp=ts * 1000,
                        open=o or 0,
                        high=h or 0,
                        low=l or 0,
                        close=c or 0,
                        volume=v or 0
                    )
                    for ts, o, h, l, c, v in zip(
                        timestamps,
                        quote['open'],
                        quote['high'],
                        quote['low'],
                        quote['close'],
                        quote['volume']
                    )
                    if o and h and l and c
                ]
    except Exception as e:
        print(f"Error fetching US stock klines: {e}")

    return []


# ============================================
# 港股数据
# ============================================

async def fetch_hk_stock_data(symbol: str) -> Optional[MarketData]:
    """获取港股数据"""
    try:
        # 港股代码格式: 0001.HK
        if not symbol.endswith('.HK'):
            symbol = f"{symbol}.HK"

        return await fetch_us_stock_data(symbol)  # Yahoo Finance 也支持港股
    except Exception as e:
        print(f"Error fetching HK stock data: {e}")

    return None


async def fetch_hk_stock_klines(symbol: str, interval: str = '1h', days: int = 7) -> List[Candlestick]:
    """获取港股K线"""
    if not symbol.endswith('.HK'):
        symbol = f"{symbol}.HK"

    return await fetch_us_stock_klines(symbol, interval, days)


# ============================================
# A股数据
# ============================================

async def fetch_cn_stock_data(symbol: str) -> Optional[MarketData]:
    """获取A股数据"""
    try:
        # A股代码格式: 600000.SS (上海) 或 000001.SZ (深圳)
        if not (symbol.endswith('.SS') or symbol.endswith('.SZ')):
            # 默认上海
            symbol = f"{symbol}.SS"

        return await fetch_us_stock_data(symbol)  # Yahoo Finance 也支持A股
    except Exception as e:
        print(f"Error fetching CN stock data: {e}")

    return None


async def fetch_cn_stock_klines(symbol: str, interval: str = '1h', days: int = 7) -> List[Candlestick]:
    """获取A股K线"""
    if not (symbol.endswith('.SS') or symbol.endswith('.SZ')):
        symbol = f"{symbol}.SS"

    return await fetch_us_stock_klines(symbol, interval, days)


# ============================================
# 统一接口
# ============================================

async def fetch_market_data(symbol: str, market: str = 'auto') -> Optional[MarketData]:
    """
    获取市场数据（统一接口）

    Args:
        symbol: 交易对/股票代码
        market: 市场类型 (auto, crypto, us, hk, cn)
    """
    # 自动检测市场
    if market == 'auto':
        if '/' in symbol:
            market = 'crypto'
        elif '.HK' in symbol:
            market = 'hk'
        elif '.SS' in symbol or '.SZ' in symbol:
            market = 'cn'
        else:
            # 尝试美股
            market = 'us'

    # 根据市场获取数据
    if market == 'crypto':
        return await fetch_crypto_data(symbol)
    elif market == 'us':
        return await fetch_us_stock_data(symbol)
    elif market == 'hk':
        return await fetch_hk_stock_data(symbol)
    elif market == 'cn':
        return await fetch_cn_stock_data(symbol)

    return None


async def fetch_klines(symbol: str, market: str = 'auto', interval: str = '1h', limit: int = 100) -> List[Candlestick]:
    """获取K线数据（统一接口）"""

    # 自动检测市场
    if market == 'auto':
        if '/' in symbol:
            market = 'crypto'
        elif '.HK' in symbol:
            market = 'hk'
        elif '.SS' in symbol or '.SZ' in symbol:
            market = 'cn'
        else:
            market = 'us'

    # 根据市场获取K线
    if market == 'crypto':
        return await fetch_crypto_klines(symbol, interval, limit)
    elif market == 'us':
        days = min(limit // 6, 30)  # 粗略计算天数
        return await fetch_us_stock_klines(symbol, interval, days)
    elif market == 'hk':
        days = min(limit // 6, 30)
        return await fetch_hk_stock_klines(symbol, interval, days)
    elif market == 'cn':
        days = min(limit // 6, 30)
        return await fetch_cn_stock_klines(symbol, interval, days)

    return []


# ============================================
# 搜索功能
# ============================================

async def search_symbols(query: str, markets: List[str] = ['crypto', 'us', 'hk', 'cn']) -> List[SearchResult]:
    """搜索交易对/股票"""
    results = []

    # 加密货币搜索
    if 'crypto' in markets:
        crypto_pairs = [
            ('BTC/USDT', 'Bitcoin', 'Binance'),
            ('ETH/USDT', 'Ethereum', 'Binance'),
            ('BNB/USDT', 'Binance Coin', 'Binance'),
            ('XRP/USDT', 'Ripple', 'Binance'),
            ('ADA/USDT', 'Cardano', 'Binance'),
            ('SOL/USDT', 'Solana', 'Binance'),
            ('DOGE/USDT', 'Dogecoin', 'Binance'),
        ]

        for symbol, name, exchange in crypto_pairs:
            if query.upper() in symbol or query.upper() in name.upper():
                results.append(SearchResult(
                    symbol=symbol,
                    name=name,
                    market='crypto',
                    exchange=exchange,
                    currency='USDT'
                ))

    # 美股搜索
    if 'us' in markets:
        us_stocks = [
            ('AAPL', 'Apple Inc.', 'NASDAQ'),
            ('MSFT', 'Microsoft Corporation', 'NASDAQ'),
            ('GOOGL', 'Alphabet Inc.', 'NASDAQ'),
            ('AMZN', 'Amazon.com Inc.', 'NASDAQ'),
            ('TSLA', 'Tesla Inc.', 'NASDAQ'),
            ('NVDA', 'NVIDIA Corporation', 'NASDAQ'),
            ('META', 'Meta Platforms Inc.', 'NASDAQ'),
        ]

        for symbol, name, exchange in us_stocks:
            if query.upper() in symbol or query.upper() in name.upper():
                results.append(SearchResult(
                    symbol=symbol,
                    name=name,
                    market='us',
                    exchange=exchange,
                    currency='USD'
                ))

    # 港股搜索
    if 'hk' in markets:
        hk_stocks = [
            ('0700.HK', '腾讯控股', 'HKEX'),
            ('9988.HK', '阿里巴巴', 'HKEX'),
            ('0941.HK', '中国移动', 'HKEX'),
            ('1299.HK', '友邦保险', 'HKEX'),
        ]

        for symbol, name, exchange in hk_stocks:
            if query.upper() in symbol or query in name:
                results.append(SearchResult(
                    symbol=symbol,
                    name=name,
                    market='hk',
                    exchange=exchange,
                    currency='HKD'
                ))

    # A股搜索
    if 'cn' in markets:
        cn_stocks = [
            ('600519.SS', '贵州茅台', 'SSE'),
            ('000858.SZ', '五粮液', 'SZSE'),
            ('600036.SS', '招商银行', 'SSE'),
            ('000001.SZ', '平安银行', 'SZSE'),
        ]

        for symbol, name, exchange in cn_stocks:
            if query.upper() in symbol or query in name:
                results.append(SearchResult(
                    symbol=symbol,
                    name=name,
                    market='cn',
                    exchange=exchange,
                    currency='CNY'
                ))

    return results


# ============================================
# API 端点
# ============================================

@router.get("/quote")
async def get_quote(symbol: str, market: str = 'auto'):
    """获取实时行情"""
    data = await fetch_market_data(symbol, market)

    if data:
        return {
            "success": True,
            "data": data.dict()
        }
    else:
        raise HTTPException(status_code=404, detail="Symbol not found")


@router.get("/klines")
async def get_klines(
    symbol: str,
    market: str = 'auto',
    interval: str = '1h',
    limit: int = 100
):
    """获取K线数据"""
    klines = await fetch_klines(symbol, market, interval, limit)

    if klines:
        return {
            "success": True,
            "data": [k.dict() for k in klines],
            "count": len(klines)
        }
    else:
        raise HTTPException(status_code=404, detail="No data found")


@router.get("/search")
async def search(
    q: str,
    markets: str = 'crypto,us,hk,cn'
):
    """搜索交易对/股票"""
    market_list = markets.split(',')
    results = await search_symbols(q, market_list)

    return {
        "success": True,
        "data": [r.dict() for r in results],
        "count": len(results)
    }


@router.get("/markets")
async def list_markets():
    """获取支持的市场列表"""
    return {
        "success": True,
        "data": [
            {
                "id": "crypto",
                "name": "加密货币",
                "icon": "₿",
                "examples": ["BTC/USDT", "ETH/USDT"]
            },
            {
                "id": "us",
                "name": "美股",
                "icon": "🇺🇸",
                "examples": ["AAPL", "TSLA", "GOOGL"]
            },
            {
                "id": "hk",
                "name": "港股",
                "icon": "🇭🇰",
                "examples": ["0700.HK", "9988.HK"]
            },
            {
                "id": "cn",
                "name": "A股",
                "icon": "🇨🇳",
                "examples": ["600519.SS", "000858.SZ"]
            }
        ]
    }
