"""
Claude AI市场分析模块
"""
from typing import Dict, List, Optional
import os
from anthropic import Anthropic


class MarketAnalyzer:
    """使用Claude AI进行市场分析"""

    def __init__(self):
        """初始化Claude客户端"""
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if api_key:
            self.client = Anthropic(api_key=api_key)
            self.available = True
        else:
            self.client = None
            self.available = False

    def analyze_market(
        self,
        symbol: str,
        current_price: float,
        indicators: Dict,
        ohlcv_data: Optional[List[Dict]] = None
    ) -> Dict:
        """
        分析市场趋势和给出交易建议

        Args:
            symbol: 交易对符号
            current_price: 当前价格
            indicators: 技术指标数据
            ohlcv_data: 历史OHLCV数据（可选）

        Returns:
            分析结果字典
        """
        if not self.available:
            return self._fallback_analysis(symbol, current_price, indicators)

        try:
            # 构建分析提示词
            prompt = self._build_analysis_prompt(
                symbol, current_price, indicators, ohlcv_data
            )

            # 调用Claude API
            message = self.client.messages.create(
                model="claude-opus-4-8",
                max_tokens=2000,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )

            analysis_text = message.content[0].text

            return {
                "success": True,
                "symbol": symbol,
                "current_price": current_price,
                "analysis": analysis_text,
                "model": "claude-opus-4-8"
            }

        except Exception as e:
            print(f"Claude API error: {e}")
            return self._fallback_analysis(symbol, current_price, indicators)

    def _build_analysis_prompt(
        self,
        symbol: str,
        current_price: float,
        indicators: Dict,
        ohlcv_data: Optional[List[Dict]]
    ) -> str:
        """构建给Claude的分析提示词"""

        prompt = f"""你是一位专业的量化交易分析师。请分析以下市场数据并给出交易建议。

**交易对**: {symbol}
**当前价格**: ${current_price:,.2f}

**技术指标**:
- RSI: {indicators.get('rsi', 'N/A')}
- MACD: {indicators.get('macd', 'N/A')}
- MACD信号线: {indicators.get('macd_signal', 'N/A')}
- SMA(20): ${indicators.get('sma_20', 0):,.2f}
- SMA(50): ${indicators.get('sma_50', 0):,.2f}
- 布林带上轨: ${indicators.get('bb_upper', 0):,.2f}
- 布林带中轨: ${indicators.get('bb_middle', 0):,.2f}
- 布林带下轨: ${indicators.get('bb_lower', 0):,.2f}
- ATR: {indicators.get('atr', 'N/A')}
- ADX: {indicators.get('adx', 'N/A')}

请提供以下内容：

1. **市场趋势分析**：当前市场处于什么趋势（上涨/下跌/横盘）？
2. **技术指标解读**：各项指标显示什么信号？
3. **支撑位和阻力位**：基于技术指标估算关键价位
4. **交易建议**：
   - 操作方向：买入/卖出/观望
   - 建议入场价位
   - 止损价位
   - 止盈目标
   - 风险评估
5. **注意事项**：需要关注的风险因素

请用简洁专业的语言回答，重点突出可操作的建议。"""

        return prompt

    def _fallback_analysis(
        self,
        symbol: str,
        current_price: float,
        indicators: Dict
    ) -> Dict:
        """当Claude API不可用时的备用分析"""

        rsi = indicators.get('rsi')
        macd = indicators.get('macd', 0)
        macd_signal = indicators.get('macd_signal', 0)
        sma_20 = indicators.get('sma_20', 0)
        sma_50 = indicators.get('sma_50', 0)

        # 简单的规则分析
        signals = []

        # RSI分析
        if rsi:
            if rsi < 30:
                signals.append("RSI低于30，市场可能超卖，考虑买入")
            elif rsi > 70:
                signals.append("RSI高于70，市场可能超买，考虑卖出")
            else:
                signals.append(f"RSI为{rsi:.2f}，处于中性区间")

        # MACD分析
        if macd and macd_signal:
            if macd > macd_signal:
                signals.append("MACD位于信号线上方，多头信号")
            else:
                signals.append("MACD位于信号线下方，空头信号")

        # 均线分析
        if sma_20 and sma_50:
            if current_price > sma_20 > sma_50:
                signals.append("价格位于均线上方，趋势向上")
            elif current_price < sma_20 < sma_50:
                signals.append("价格位于均线下方，趋势向下")

        # 布林带分析
        bb_upper = indicators.get('bb_upper')
        bb_lower = indicators.get('bb_lower')
        if bb_upper and bb_lower:
            if current_price > bb_upper:
                signals.append("价格突破布林带上轨，可能超买")
            elif current_price < bb_lower:
                signals.append("价格跌破布林带下轨，可能超卖")

        analysis = f"""# {symbol} 技术分析报告（基于规则引擎）

**当前价格**: ${current_price:,.2f}

## 技术指标信号：
{''.join(f'- {s}\\n' for s in signals)}

## 建议：
基于当前技术指标，建议保持谨慎。这是自动生成的基础分析，建议结合更多市场信息做决策。

*注意：Claude API未配置，这是基于简单规则的分析。配置ANTHROPIC_API_KEY环境变量可获得更详细的AI分析。*
"""

        return {
            "success": True,
            "symbol": symbol,
            "current_price": current_price,
            "analysis": analysis,
            "model": "rule-based-fallback",
            "note": "Claude API not configured, using rule-based analysis"
        }

    def analyze_backtest_results(self, results: Dict) -> Dict:
        """分析回测结果并给出优化建议"""

        if not self.available:
            return {
                "success": False,
                "message": "Claude API not configured"
            }

        try:
            prompt = f"""作为量化交易专家，请分析以下回测结果并给出优化建议：

**回测结果**:
- 初始资金: ${results['initial_capital']:,.2f}
- 最终资金: ${results['final_capital']:,.2f}
- 总收益率: {results['total_return']}%
- 夏普比率: {results['sharpe_ratio']}
- 最大回撤: {results['max_drawdown']}%
- 总交易次数: {results['total_trades']}
- 胜率: {results['win_rate']}%

请提供：
1. 策略表现评估（好/中/差）
2. 主要问题分析
3. 具体优化建议
4. 风险控制建议
"""

            message = self.client.messages.create(
                model="claude-opus-4-8",
                max_tokens=1500,
                messages=[{"role": "user", "content": prompt}]
            )

            return {
                "success": True,
                "analysis": message.content[0].text,
                "model": "claude-opus-4-8"
            }

        except Exception as e:
            return {
                "success": False,
                "message": str(e)
            }


# 全局实例
_analyzer_instance: Optional[MarketAnalyzer] = None


def get_analyzer() -> MarketAnalyzer:
    """获取分析器实例（单例）"""
    global _analyzer_instance

    if _analyzer_instance is None:
        _analyzer_instance = MarketAnalyzer()

    return _analyzer_instance
