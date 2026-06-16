"""
SQLite数据库管理
"""
import aiosqlite
from typing import Optional, List, Dict
from datetime import datetime


class Database:
    """数据库管理类"""

    def __init__(self, db_path: str = "data/stocks.db"):
        self.db_path = db_path
        self.conn: Optional[aiosqlite.Connection] = None

    async def connect(self):
        """连接数据库"""
        self.conn = await aiosqlite.connect(self.db_path)
        self.conn.row_factory = aiosqlite.Row
        await self.init_tables()

    async def close(self):
        """关闭数据库连接"""
        if self.conn:
            await self.conn.close()
            self.conn = None

    async def init_tables(self):
        """初始化数据库表"""
        if not self.conn:
            return

        # 市场数据表
        await self.conn.execute("""
            CREATE TABLE IF NOT EXISTS market_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                symbol TEXT NOT NULL,
                exchange TEXT NOT NULL,
                timestamp INTEGER NOT NULL,
                open REAL NOT NULL,
                high REAL NOT NULL,
                low REAL NOT NULL,
                close REAL NOT NULL,
                volume REAL NOT NULL,
                timeframe TEXT NOT NULL,
                created_at INTEGER DEFAULT (strftime('%s', 'now')),
                UNIQUE(symbol, exchange, timestamp, timeframe)
            )
        """)

        # 创建索引
        await self.conn.execute("""
            CREATE INDEX IF NOT EXISTS idx_market_data_symbol
            ON market_data(symbol, exchange, timeframe, timestamp)
        """)

        # 策略表
        await self.conn.execute("""
            CREATE TABLE IF NOT EXISTS strategies (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                code TEXT NOT NULL,
                description TEXT,
                parameters TEXT,
                created_at INTEGER DEFAULT (strftime('%s', 'now')),
                updated_at INTEGER DEFAULT (strftime('%s', 'now'))
            )
        """)

        # 回测结果表
        await self.conn.execute("""
            CREATE TABLE IF NOT EXISTS backtest_results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                strategy_id INTEGER NOT NULL,
                symbol TEXT NOT NULL,
                timeframe TEXT NOT NULL,
                start_date INTEGER NOT NULL,
                end_date INTEGER NOT NULL,
                initial_capital REAL NOT NULL,
                final_capital REAL,
                total_return REAL,
                sharpe_ratio REAL,
                max_drawdown REAL,
                total_trades INTEGER,
                win_rate REAL,
                results_data TEXT,
                created_at INTEGER DEFAULT (strftime('%s', 'now')),
                FOREIGN KEY (strategy_id) REFERENCES strategies(id)
            )
        """)

        # 交易记录表
        await self.conn.execute("""
            CREATE TABLE IF NOT EXISTS trades (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                backtest_id INTEGER,
                symbol TEXT NOT NULL,
                side TEXT NOT NULL,
                price REAL NOT NULL,
                quantity REAL NOT NULL,
                timestamp INTEGER NOT NULL,
                pnl REAL,
                created_at INTEGER DEFAULT (strftime('%s', 'now')),
                FOREIGN KEY (backtest_id) REFERENCES backtest_results(id)
            )
        """)

        await self.conn.commit()

    async def save_market_data(self, symbol: str, exchange: str, timeframe: str,
                               ohlcv_data: List[List]) -> int:
        """保存市场数据"""
        if not self.conn:
            return 0

        count = 0
        for candle in ohlcv_data:
            try:
                await self.conn.execute("""
                    INSERT OR IGNORE INTO market_data
                    (symbol, exchange, timestamp, open, high, low, close, volume, timeframe)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (symbol, exchange, candle[0], candle[1], candle[2],
                      candle[3], candle[4], candle[5], timeframe))
                count += 1
            except Exception as e:
                print(f"Error saving candle: {e}")

        await self.conn.commit()
        return count

    async def get_market_data(self, symbol: str, exchange: str, timeframe: str,
                             start_time: Optional[int] = None,
                             end_time: Optional[int] = None,
                             limit: int = 1000) -> List[Dict]:
        """获取市场数据"""
        if not self.conn:
            return []

        query = """
            SELECT timestamp, open, high, low, close, volume
            FROM market_data
            WHERE symbol = ? AND exchange = ? AND timeframe = ?
        """
        params = [symbol, exchange, timeframe]

        if start_time:
            query += " AND timestamp >= ?"
            params.append(start_time)

        if end_time:
            query += " AND timestamp <= ?"
            params.append(end_time)

        query += " ORDER BY timestamp DESC LIMIT ?"
        params.append(limit)

        cursor = await self.conn.execute(query, params)
        rows = await cursor.fetchall()

        return [dict(row) for row in rows]

    async def save_strategy(self, name: str, code: str, description: str = "",
                           parameters: str = "") -> int:
        """保存策略"""
        if not self.conn:
            return 0

        cursor = await self.conn.execute("""
            INSERT OR REPLACE INTO strategies (name, code, description, parameters)
            VALUES (?, ?, ?, ?)
        """, (name, code, description, parameters))

        await self.conn.commit()
        return cursor.lastrowid

    async def get_strategy(self, strategy_id: int) -> Optional[Dict]:
        """获取策略"""
        if not self.conn:
            return None

        cursor = await self.conn.execute("""
            SELECT * FROM strategies WHERE id = ?
        """, (strategy_id,))

        row = await cursor.fetchone()
        return dict(row) if row else None

    async def list_strategies(self) -> List[Dict]:
        """列出所有策略"""
        if not self.conn:
            return []

        cursor = await self.conn.execute("""
            SELECT id, name, description, created_at, updated_at
            FROM strategies
            ORDER BY updated_at DESC
        """)

        rows = await cursor.fetchall()
        return [dict(row) for row in rows]

    async def save_backtest_result(self, strategy_id: int, symbol: str,
                                   timeframe: str, start_date: int, end_date: int,
                                   initial_capital: float, results: Dict) -> int:
        """保存回测结果"""
        if not self.conn:
            return 0

        import json

        cursor = await self.conn.execute("""
            INSERT INTO backtest_results
            (strategy_id, symbol, timeframe, start_date, end_date, initial_capital,
             final_capital, total_return, sharpe_ratio, max_drawdown, total_trades,
             win_rate, results_data)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            strategy_id, symbol, timeframe, start_date, end_date, initial_capital,
            results.get('final_capital'),
            results.get('total_return'),
            results.get('sharpe_ratio'),
            results.get('max_drawdown'),
            results.get('total_trades'),
            results.get('win_rate'),
            json.dumps(results)
        ))

        await self.conn.commit()
        return cursor.lastrowid

    async def get_backtest_results(self, strategy_id: Optional[int] = None,
                                   limit: int = 100) -> List[Dict]:
        """获取回测结果"""
        if not self.conn:
            return []

        if strategy_id:
            cursor = await self.conn.execute("""
                SELECT * FROM backtest_results
                WHERE strategy_id = ?
                ORDER BY created_at DESC
                LIMIT ?
            """, (strategy_id, limit))
        else:
            cursor = await self.conn.execute("""
                SELECT * FROM backtest_results
                ORDER BY created_at DESC
                LIMIT ?
            """, (limit,))

        rows = await cursor.fetchall()
        return [dict(row) for row in rows]


# 全局数据库实例
_db_instance: Optional[Database] = None


async def get_database() -> Database:
    """获取数据库实例（单例模式）"""
    global _db_instance

    if _db_instance is None:
        _db_instance = Database()
        await _db_instance.connect()

    return _db_instance


async def close_database():
    """关闭数据库连接"""
    global _db_instance

    if _db_instance:
        await _db_instance.close()
        _db_instance = None
