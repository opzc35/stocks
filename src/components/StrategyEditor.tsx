import { useState } from 'react'
import Editor from '@monaco-editor/react'
import './StrategyEditor.css'

interface Strategy {
  name: string
  code: string
  description: string
}

const DEFAULT_STRATEGY = `# 策略示例：简单双均线策略
# 定义策略参数
SHORT_PERIOD = 10
LONG_PERIOD = 20

def on_data(data, index):
    """
    处理每个K线数据

    Args:
        data: 完整的OHLCV数据（带指标）
        index: 当前处理的索引

    Returns:
        'BUY', 'SELL', 或 None
    """
    if index < LONG_PERIOD:
        return None

    # 获取当前和前一个均线值
    short_ma = data[f'sma_{SHORT_PERIOD}'].iloc[index]
    long_ma = data[f'sma_{LONG_PERIOD}'].iloc[index]

    prev_short_ma = data[f'sma_{SHORT_PERIOD}'].iloc[index - 1]
    prev_long_ma = data[f'sma_{LONG_PERIOD}'].iloc[index - 1]

    # 检查金叉（买入信号）
    if prev_short_ma <= prev_long_ma and short_ma > long_ma:
        return 'BUY'

    # 检查死叉（卖出信号）
    if prev_short_ma >= prev_long_ma and short_ma < long_ma:
        return 'SELL'

    return None
`

const STRATEGY_TEMPLATES = [
  {
    name: '双均线策略',
    description: '使用短期和长期移动平均线的交叉信号',
    code: DEFAULT_STRATEGY
  },
  {
    name: 'RSI策略',
    description: '基于RSI超买超卖信号的策略',
    code: `# RSI策略
OVERSOLD = 30
OVERBOUGHT = 70

def on_data(data, index):
    if index < 14:  # RSI需要至少14个数据点
        return None

    rsi = data['rsi'].iloc[index]

    if pd.isna(rsi):
        return None

    if rsi < OVERSOLD:
        return 'BUY'
    elif rsi > OVERBOUGHT:
        return 'SELL'

    return None
`
  },
  {
    name: 'MACD策略',
    description: 'MACD与信号线交叉策略',
    code: `# MACD策略
def on_data(data, index):
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
`
  }
]

export function StrategyEditor() {
  const [code, setCode] = useState(DEFAULT_STRATEGY)
  const [strategyName, setStrategyName] = useState('我的策略')
  const [selectedTemplate, setSelectedTemplate] = useState(0)
  const [testing, setTesting] = useState(false)
  const [testResult, setTestResult] = useState<any>(null)

  const handleTemplateChange = (index: number) => {
    setSelectedTemplate(index)
    setCode(STRATEGY_TEMPLATES[index].code)
    setStrategyName(STRATEGY_TEMPLATES[index].name)
  }

  const handleSave = () => {
    // 保存策略到本地存储
    const strategy: Strategy = {
      name: strategyName,
      code,
      description: '用户自定义策略'
    }
    localStorage.setItem(`strategy_${Date.now()}`, JSON.stringify(strategy))
    alert('策略已保存到本地')
  }

  const handleTest = async () => {
    setTesting(true)
    setTestResult(null)

    try {
      // 注意：这里需要后端支持自定义策略代码执行
      // 当前演示使用内置策略
      const response = await fetch('http://localhost:8000/api/backtest/run', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          symbol: 'BTC/USDT',
          strategy: 'simple_ma', // 实际应该传递自定义代码
          initial_capital: 10000
        })
      })

      const data = await response.json()
      setTestResult(data.results)
    } catch (error) {
      console.error('Test error:', error)
      alert('测试失败')
    } finally {
      setTesting(false)
    }
  }

  return (
    <div className="strategy-editor">
      <div className="editor-header">
        <h2>📝 策略编辑器</h2>
        <div className="editor-controls">
          <input
            type="text"
            value={strategyName}
            onChange={(e) => setStrategyName(e.target.value)}
            className="strategy-name-input"
            placeholder="策略名称"
          />
          <select
            value={selectedTemplate}
            onChange={(e) => handleTemplateChange(Number(e.target.value))}
            className="template-select"
          >
            {STRATEGY_TEMPLATES.map((template, index) => (
              <option key={index} value={index}>
                {template.name}
              </option>
            ))}
          </select>
          <button onClick={handleSave} className="btn btn-secondary">
            💾 保存
          </button>
          <button onClick={handleTest} disabled={testing} className="btn btn-primary">
            {testing ? '⏳ 测试中...' : '🧪 测试策略'}
          </button>
        </div>
      </div>

      <div className="editor-content">
        <div className="code-editor">
          <Editor
            height="400px"
            defaultLanguage="python"
            theme="vs-dark"
            value={code}
            onChange={(value) => setCode(value || '')}
            options={{
              minimap: { enabled: false },
              fontSize: 14,
              lineNumbers: 'on',
              roundedSelection: false,
              scrollBeyondLastLine: false,
              automaticLayout: true,
            }}
          />
        </div>

        {testResult && (
          <div className="test-results">
            <h3>回测结果</h3>
            <div className="results-grid">
              <div className="result-item">
                <span className="label">总收益</span>
                <span className={`value ${testResult.total_return >= 0 ? 'positive' : 'negative'}`}>
                  {testResult.total_return}%
                </span>
              </div>
              <div className="result-item">
                <span className="label">夏普比率</span>
                <span className="value">{testResult.sharpe_ratio}</span>
              </div>
              <div className="result-item">
                <span className="label">最大回撤</span>
                <span className="value negative">{testResult.max_drawdown}%</span>
              </div>
              <div className="result-item">
                <span className="label">胜率</span>
                <span className="value">{testResult.win_rate}%</span>
              </div>
              <div className="result-item">
                <span className="label">总交易</span>
                <span className="value">{testResult.total_trades}笔</span>
              </div>
            </div>
          </div>
        )}
      </div>

      <div className="editor-help">
        <h3>💡 策略编写指南</h3>
        <ul>
          <li>策略必须包含 <code>on_data(data, index)</code> 函数</li>
          <li>返回 'BUY' 表示买入信号</li>
          <li>返回 'SELL' 表示卖出信号</li>
          <li>返回 None 表示无操作</li>
          <li>可使用的指标：close, sma_10, sma_20, sma_50, rsi, macd, macd_signal 等</li>
          <li>使用 data['指标名'].iloc[index] 访问数据</li>
        </ul>
      </div>
    </div>
  )
}
