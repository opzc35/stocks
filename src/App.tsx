import { useState, useEffect } from 'react'
import './App.css'
import { PriceChart } from './components/PriceChart'
import { StrategyEditor } from './components/StrategyEditor'

interface Ticker {
  symbol: string
  price: number
  volume: number
  timestamp: number
}

interface Indicator {
  close: number
  rsi: number | null
  macd: number | null
  sma_20: number | null
  sma_50: number | null
}

interface ChartData {
  timestamp: number
  close: number
  sma_20?: number
  sma_50?: number
}

function App() {
  const [ticker, setTicker] = useState<Ticker | null>(null)
  const [indicators, setIndicators] = useState<Indicator | null>(null)
  const [chartData, setChartData] = useState<ChartData[]>([])
  const [loading, setLoading] = useState(false)
  const [symbol, setSymbol] = useState('BTC/USDT')
  const [activeTab, setActiveTab] = useState<'dashboard' | 'editor'>('dashboard')

  // 获取实时价格
  const fetchTicker = async () => {
    try {
      const response = await fetch(`http://localhost:8000/api/market/ticker?symbol=${symbol}`)
      const data = await response.json()
      setTicker(data)
    } catch (error) {
      console.error('Error fetching ticker:', error)
    }
  }

  // 获取技术指标
  const fetchIndicators = async () => {
    setLoading(true)
    try {
      const response = await fetch('http://localhost:8000/api/indicators/latest', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ symbol, timeframe: '1h', limit: 100 })
      })
      const data = await response.json()
      setIndicators(data)
    } catch (error) {
      console.error('Error fetching indicators:', error)
    } finally {
      setLoading(false)
    }
  }

  // 获取图表数据
  const fetchChartData = async () => {
    try {
      const response = await fetch('http://localhost:8000/api/data/query', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          symbol,
          exchange: 'binance',
          timeframe: '1h',
          limit: 50
        })
      })
      const result = await response.json()
      if (result.data && result.data.length > 0) {
        // 反转数据（从旧到新）并计算移动平均线
        const sortedData = result.data.reverse()
        setChartData(sortedData.map((item: any, index: number) => {
          // 简单计算SMA
          let sma_20, sma_50
          if (index >= 19) {
            const sum20 = sortedData.slice(index - 19, index + 1).reduce((acc: number, d: any) => acc + d.close, 0)
            sma_20 = sum20 / 20
          }
          if (index >= 49) {
            const sum50 = sortedData.slice(index - 49, index + 1).reduce((acc: number, d: any) => acc + d.close, 0)
            sma_50 = sum50 / 50
          }
          return {
            timestamp: item.timestamp,
            close: item.close,
            sma_20,
            sma_50
          }
        }))
      }
    } catch (error) {
      console.error('Error fetching chart data:', error)
    }
  }

  // 同步历史数据
  const syncData = async () => {
    setLoading(true)
    try {
      const response = await fetch('http://localhost:8000/api/data/sync', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          symbol,
          exchange: 'binance',
          timeframe: '1h',
          days_back: 7
        })
      })
      const data = await response.json()
      alert(`同步成功: ${data.count} 条数据`)
      fetchIndicators()
      fetchChartData()
    } catch (error) {
      console.error('Error syncing data:', error)
      alert('同步失败')
    } finally {
      setLoading(false)
    }
  }

  // 运行回测
  const runBacktest = async (strategy: string) => {
    setLoading(true)
    try {
      const response = await fetch('http://localhost:8000/api/backtest/run', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          symbol,
          strategy,
          initial_capital: 10000
        })
      })
      const data = await response.json()

      if (data.success) {
        const r = data.results
        alert(
          `回测结果 (${strategy}):\n\n` +
          `总收益: ${r.total_return}%\n` +
          `夏普比率: ${r.sharpe_ratio}\n` +
          `最大回撤: ${r.max_drawdown}%\n` +
          `胜率: ${r.win_rate}%\n` +
          `总交易: ${r.total_trades}笔`
        )
      }
    } catch (error) {
      console.error('Error running backtest:', error)
      alert('回测失败')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchTicker()
    fetchIndicators()
    fetchChartData()

    // 每10秒更新一次价格
    const interval = setInterval(fetchTicker, 10000)
    return () => clearInterval(interval)
  }, [symbol])

  return (
    <div className="app">
      <header className="header">
        <h1>📈 量化交易系统</h1>
        <div className="header-controls">
          <div className="tab-nav">
            <button
              className={`tab-btn ${activeTab === 'dashboard' ? 'active' : ''}`}
              onClick={() => setActiveTab('dashboard')}
            >
              📊 仪表盘
            </button>
            <button
              className={`tab-btn ${activeTab === 'editor' ? 'active' : ''}`}
              onClick={() => setActiveTab('editor')}
            >
              📝 策略编辑器
            </button>
          </div>
          {activeTab === 'dashboard' && (
            <div className="symbol-selector">
              <select value={symbol} onChange={(e) => setSymbol(e.target.value)}>
                <option value="BTC/USDT">BTC/USDT</option>
                <option value="ETH/USDT">ETH/USDT</option>
                <option value="BNB/USDT">BNB/USDT</option>
              </select>
            </div>
          )}
        </div>
      </header>

      {activeTab === 'dashboard' ? (
        <main className="main-content">
        {/* 价格图表 */}
        {chartData.length > 0 && (
          <section className="card chart-card">
            <PriceChart data={chartData} symbol={symbol} />
          </section>
        )}

        {/* 实时价格卡片 */}
        <section className="card price-card">
          <h2>实时价格</h2>
          {ticker ? (
            <div className="price-info">
              <div className="price-large">${ticker.price.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}</div>
              <div className="price-detail">
                <span>交易量: {ticker.volume.toLocaleString()}</span>
                <span className="timestamp">
                  {new Date(ticker.timestamp).toLocaleTimeString()}
                </span>
              </div>
            </div>
          ) : (
            <div className="loading">加载中...</div>
          )}
        </section>

        {/* 技术指标卡片 */}
        <section className="card indicators-card">
          <h2>技术指标</h2>
          {loading && <div className="loading">计算中...</div>}
          {indicators && !loading ? (
            <div className="indicators-grid">
              <div className="indicator">
                <span className="label">RSI</span>
                <span className={`value ${indicators.rsi && indicators.rsi < 30 ? 'oversold' : indicators.rsi && indicators.rsi > 70 ? 'overbought' : ''}`}>
                  {indicators.rsi?.toFixed(2) || 'N/A'}
                </span>
              </div>
              <div className="indicator">
                <span className="label">MACD</span>
                <span className="value">{indicators.macd?.toFixed(2) || 'N/A'}</span>
              </div>
              <div className="indicator">
                <span className="label">SMA(20)</span>
                <span className="value">${indicators.sma_20?.toFixed(2) || 'N/A'}</span>
              </div>
              <div className="indicator">
                <span className="label">SMA(50)</span>
                <span className="value">${indicators.sma_50?.toFixed(2) || 'N/A'}</span>
              </div>
            </div>
          ) : !loading && (
            <div className="no-data">
              <p>暂无数据，请先同步历史数据</p>
            </div>
          )}
        </section>

        {/* 操作按钮区 */}
        <section className="card actions-card">
          <h2>操作</h2>
          <div className="actions-grid">
            <button onClick={syncData} disabled={loading} className="btn btn-primary">
              📥 同步数据
            </button>
            <button onClick={fetchIndicators} disabled={loading} className="btn btn-secondary">
              🔄 刷新指标
            </button>
            <button onClick={() => runBacktest('simple_ma')} disabled={loading} className="btn btn-success">
              🎯 MA策略回测
            </button>
            <button onClick={() => runBacktest('rsi')} disabled={loading} className="btn btn-success">
              📊 RSI策略回测
            </button>
          </div>
        </section>

        {/* 系统状态 */}
        <section className="card status-card">
          <h2>系统状态</h2>
          <div className="status-grid">
            <div className="status-item">
              <span className="status-dot online"></span>
              <span>Python引擎: 运行中</span>
            </div>
            <div className="status-item">
              <span className="status-dot online"></span>
              <span>数据库: 已连接</span>
            </div>
            <div className="status-item">
              <span className="status-dot"></span>
              <span>AI分析: 就绪</span>
            </div>
          </div>
        </section>
      </main>
      ) : (
        <main className="main-content editor-view">
          <div className="card editor-card">
            <StrategyEditor />
          </div>
        </main>
      )}

      <footer className="footer">
        <p>量化交易系统 v0.1.0 | Powered by Claude Code</p>
      </footer>
    </div>
  )
}

export default App
