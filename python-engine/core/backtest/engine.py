"""
回测引擎
"""
import pandas as pd
import numpy as np
from typing import List, Dict, Optional
from core.strategy.base import Strategy
from core.indicators import IndicatorEngine


class Trade:
    """交易记录"""

    def __init__(self, side: str, price: float, quantity: float, timestamp: int):
        self.side = side  # 'BUY' or 'SELL'
        self.price = price
        self.quantity = quantity
        self.timestamp = timestamp
        self.pnl = 0.0


class BacktestEngine:
    """回测引擎"""

    def __init__(self,
                 initial_capital: float = 10000.0,
                 commission: float = 0.001):
        """
        初始化回测引擎

        Args:
            initial_capital: 初始资金
            commission: 手续费率（默认0.1%）
        """
        self.initial_capital = initial_capital
        self.commission = commission
        self.reset()

    def reset(self):
        """重置回测状态"""
        self.capital = self.initial_capital
        self.position = 0.0  # 持仓数量
        self.position_value = 0.0  # 持仓价值
        self.trades: List[Trade] = []
        self.equity_curve: List[float] = []
        self.timestamps: List[int] = []

    def run(self, data: List[Dict], strategy: Strategy) -> Dict:
        """
        运行回测

        Args:
            data: OHLCV数据列表
            strategy: 交易策略

        Returns:
            回测结果字典
        """
        self.reset()

        # 添加技术指标
        engine = IndicatorEngine(data)
        df = engine.add_all_indicators()

        # 遍历每个K线
        for i in range(len(df)):
            timestamp = int(df['timestamp'].iloc[i])
            close_price = float(df['close'].iloc[i])

            # 获取策略信号
            signal = strategy.on_data(df, i)

            # 执行交易
            if signal == 'BUY' and self.position == 0:
                self._execute_buy(close_price, timestamp)
            elif signal == 'SELL' and self.position > 0:
                self._execute_sell(close_price, timestamp)

            # 记录权益曲线
            equity = self.capital + (self.position * close_price)
            self.equity_curve.append(equity)
            self.timestamps.append(timestamp)

        # 如果还有持仓，按最后价格平仓
        if self.position > 0:
            final_price = float(df['close'].iloc[-1])
            final_timestamp = int(df['timestamp'].iloc[-1])
            self._execute_sell(final_price, final_timestamp)

        # 计算回测指标
        results = self._calculate_metrics()

        return results

    def _execute_buy(self, price: float, timestamp: int):
        """执行买入"""
        # 扣除手续费后可用资金
        available = self.capital * (1 - self.commission)
        quantity = available / price

        self.position = quantity
        self.position_value = price * quantity
        self.capital = 0

        trade = Trade('BUY', price, quantity, timestamp)
        self.trades.append(trade)

    def _execute_sell(self, price: float, timestamp: int):
        """执行卖出"""
        if self.position == 0:
            return

        # 卖出获得的资金（扣除手续费）
        proceeds = self.position * price * (1 - self.commission)

        # 计算该笔交易的盈亏
        pnl = proceeds - self.position_value

        self.capital = proceeds
        self.position = 0
        self.position_value = 0

        trade = Trade('SELL', price, self.position, timestamp)
        trade.pnl = pnl
        self.trades.append(trade)

    def _calculate_metrics(self) -> Dict:
        """计算回测指标"""
        if not self.equity_curve:
            return self._empty_results()

        final_equity = self.equity_curve[-1]
        total_return = ((final_equity - self.initial_capital) / self.initial_capital) * 100

        # 计算最大回撤
        max_drawdown = self._calculate_max_drawdown()

        # 计算夏普比率
        sharpe_ratio = self._calculate_sharpe_ratio()

        # 统计交易
        total_trades = len([t for t in self.trades if t.side == 'BUY'])
        winning_trades = len([t for t in self.trades if t.side == 'SELL' and t.pnl > 0])
        win_rate = (winning_trades / total_trades * 100) if total_trades > 0 else 0

        return {
            'initial_capital': self.initial_capital,
            'final_capital': final_equity,
            'total_return': round(total_return, 2),
            'max_drawdown': round(max_drawdown, 2),
            'sharpe_ratio': round(sharpe_ratio, 2),
            'total_trades': total_trades,
            'winning_trades': winning_trades,
            'losing_trades': total_trades - winning_trades,
            'win_rate': round(win_rate, 2),
            'trades': [
                {
                    'side': t.side,
                    'price': t.price,
                    'quantity': t.quantity,
                    'timestamp': t.timestamp,
                    'pnl': t.pnl
                }
                for t in self.trades
            ],
            'equity_curve': self.equity_curve,
            'timestamps': self.timestamps
        }

    def _calculate_max_drawdown(self) -> float:
        """计算最大回撤"""
        if not self.equity_curve:
            return 0.0

        equity = np.array(self.equity_curve)
        running_max = np.maximum.accumulate(equity)
        drawdown = (equity - running_max) / running_max * 100

        return abs(drawdown.min())

    def _calculate_sharpe_ratio(self) -> float:
        """计算夏普比率（简化版）"""
        if len(self.equity_curve) < 2:
            return 0.0

        returns = pd.Series(self.equity_curve).pct_change().dropna()

        if returns.std() == 0:
            return 0.0

        # 假设无风险利率为0
        sharpe = returns.mean() / returns.std() * np.sqrt(252)  # 年化

        return sharpe

    def _empty_results(self) -> Dict:
        """返回空结果"""
        return {
            'initial_capital': self.initial_capital,
            'final_capital': self.initial_capital,
            'total_return': 0.0,
            'max_drawdown': 0.0,
            'sharpe_ratio': 0.0,
            'total_trades': 0,
            'winning_trades': 0,
            'losing_trades': 0,
            'win_rate': 0.0,
            'trades': [],
            'equity_curve': [],
            'timestamps': []
        }
