import { useState, useEffect } from 'react'
import './App.css'
import { PriceChart } from './components/PriceChart'
import { StrategyEditor } from './components/StrategyEditor'
import { NewsPanel, type NewsItem } from './components/NewsPanel'
import { AlertPanel, AlertNotification, type PriceAlert, type BotConfig } from './components/AlertPanel'
import { BotSettings } from './components/BotSettings'
import { AIAssistant } from './components/AIAssistant'

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
  const [previousPrice, setPreviousPrice] = useState<number>(0)
  const [indicators, setIndicators] = useState<Indicator | null>(null)
  const [chartData, setChartData] = useState<ChartData[]>([])
  const [loading, setLoading] = useState(false)
  const [symbol, setSymbol] = useState('BTC/USDT')
  const [activeTab, setActiveTab] = useState<'dashboard' | 'editor'>('dashboard')
  const [news, setNews] = useState<NewsItem[]>([])
  const [selectedNewsId, setSelectedNewsId] = useState<string | undefined>()
  const [triggeredAlert, setTriggeredAlert] = useState<PriceAlert | null>(null)
  const [botConfigs, setBotConfigs] = useState<BotConfig[]>([])
  const [showBotSettings, setShowBotSettings] = useState(false)
  const [showAIAssistant, setShowAIAssistant] = useState(false)

  // 获取实时价格
  const fetchTicker = async () => {
    try {
      const response = await fetch(`http://localhost:8000/api/market/ticker?symbol=${symbol}`)
      const data = await response.json()
      if (ticker) {
        setPreviousPrice(ticker.price)
      }
      setTicker(data)
    } catch (error) {
      console.error('Error fetching ticker:', error)
    }
  }

  // 计算价格变化百分比
  const getPriceChange = () => {
    if (!ticker || !previousPrice) return { value: 0, percent: 0 }
    const change = ticker.price - previousPrice
    const percent = (change / previousPrice) * 100
    return { value: change, percent }
  }

  const priceChange = getPriceChange()

  // ... 其他函数保持不变 ...
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

  const fetchNews = async () => {
    const mockNews: NewsItem[] = [
      {
        id: '1',
        timestamp: Date.now() - 3600000 * 2,
        title: '比特币突破关键阻力位 $70,000',
        content: '在强劲的买盘支撑下，比特币价格突破关键阻力位，市场情绪转为乐观。',
        sentiment: 'positive',
        source: 'CoinDesk',
        tags: ['BTC', '突破']
      },
      {
        id: '2',
        timestamp: Date.now() - 3600000 * 6,
        title: '美联储维持利率不变',
        content: 'FOMC 会议决定维持当前利率水平，加密市场获得短期支撑。',
        sentiment: 'neutral',
        source: 'Bloomberg',
        tags: ['宏观', '利率']
      },
      {
        id: '3',
        timestamp: Date.now() - 3600000 * 12,
        title: '大型机构增持比特币',
        content: '链上数据显示，大型机构持续增持比特币，市场信心增强。',
        sentiment: 'positive',
        source: 'CryptoQuant',
        tags: ['机构', '链上数据']
      }
    ]
    setNews(mockNews)
  }

  const handleNewsClick = (newsId: string) => {
    setSelectedNewsId(newsId === selectedNewsId ? undefined : newsId)
  }

  const handleAlertTriggered = (alert: PriceAlert) => {
    setTriggeredAlert(alert)
  }

  const dismissAlert = () => {
    setTriggeredAlert(null)
  }

  const viewAlertDetails = () => {
    setTriggeredAlert(null)
  }

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
        const sortedData = result.data.reverse()
        setChartData(sortedData.map((item: any, index: number) => {
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
    fetchNews()
    loadBotConfigs()

    const interval = setInterval(fetchTicker, 10000)
    return () => clearInterval(interval)
  }, [symbol])

  const loadBotConfigs = () => {
    const saved = localStorage.getItem('botConfigs')
    if (saved) {
      try {
        setBotConfigs(JSON.parse(saved))
      } catch (e) {
        console.error('Failed to load bot configs:', e)
      }
    }
  }

  const saveBotConfigs = (configs: BotConfig[]) => {
    setBotConfigs(configs)
    localStorage.setItem('botConfigs', JSON.stringify(configs))
  }

  const handleAIAction = async (action: any) => {
    switch (action.type) {
      case 'create_strategy':
        console.log('Creating strategy:', action.data)
        return { success: true, message: '策略已创建' }
      case 'run_backtest':
        try {
          const response = await fetch('http://localhost:8000/api/backtest/run', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
              symbol: action.data.symbol,
              strategy: 'simple_ma',
              initial_capital: 10000
            })
          })
          const data = await response.json()
          return { success: true, data }
        } catch (error) {
          return { success: false, error: '回测失败' }
        }
      case 'set_alert':
        console.log('Setting alert:', action.data)
        return { success: true, message: '预警已设置' }
      case 'analyze_market':
        console.log('Analyzing market:', action.data)
        return { success: true, message: '分析完成' }
      case 'optimize_strategy':
        console.log('Optimizing strategy:', action.data)
        return { success: true, message: '优化完成' }
      default:
        return { success: false, error: '未知动作' }
    }
  }

  return (
    <div className="app">
      {/* 现代化 Header */}
      <header className="header">
        <h1>量化交易系统</h1>
        <div className="header-controls">
          <div className="tab-nav">
            <button
              className={`tab-btn ${activeTab === 'dashboard' ? 'active' : ''}`}
              onClick={() => setActiveTab('dashboard')}
            >
              Dashboard
            </button>
            <button
              className={`tab-btn ${activeTab === 'editor' ? 'active' : ''}`}
              onClick={() => setActiveTab('editor')}
            >
              Strategy
            </button>
            <button
              className="tab-btn"
              onClick={() => setShowBotSettings(true)}
            >
              Bots
            </button>
            <button
              className="tab-btn"
              onClick={() => setShowAIAssistant(true)}
            >
              AI
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
          {/* 图表区域 */}
          <div className="chart-section">
            {/* 价格统计卡片组 */}
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: '1.5rem', marginBottom: '2rem' }}>
              <div className="stat-card">
                <div className="stat-label">Current Price</div>
                <div className="stat-value">
                  ${ticker?.price.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 }) || '0.00'}
                </div>
                <div className={`stat-change ${priceChange.percent >= 0 ? 'positive' : 'negative'}`}>
                  {priceChange.percent >= 0 ? '↗' : '↘'} {Math.abs(priceChange.percent).toFixed(2)}%
                </div>
              </div>

              <div className="stat-card">
                <div className="stat-label">24h Volume</div>
                <div className="stat-value" style={{ fontSize: '1.5rem' }}>
                  {ticker?.volume.toLocaleString() || '0'}
                </div>
                <div className="stat-change positive">
                  ↗ High Activity
                </div>
              </div>

              <div className="stat-card">
                <div className="stat-label">RSI</div>
                <div className="stat-value" style={{ fontSize: '1.75rem' }}>
                  {indicators?.rsi?.toFixed(1) || 'N/A'}
                </div>
                <div className={`stat-change ${indicators?.rsi && indicators.rsi < 30 ? 'positive' : indicators?.rsi && indicators.rsi > 70 ? 'negative' : ''}`}>
                  {indicators?.rsi && indicators.rsi < 30 ? 'Oversold' : indicators?.rsi && indicators.rsi > 70 ? 'Overbought' : 'Neutral'}
                </div>
              </div>

              <div className="stat-card">
                <div className="stat-label">MACD</div>
                <div className="stat-value" style={{ fontSize: '1.75rem' }}>
                  {indicators?.macd?.toFixed(2) || 'N/A'}
                </div>
                <div className={`stat-change ${indicators?.macd && indicators.macd > 0 ? 'positive' : 'negative'}`}>
                  {indicators?.macd && indicators.macd > 0 ? '↗ Bullish' : '↘ Bearish'}
                </div>
              </div>
            </div>

            {/* 价格图表 */}
            {chartData.length > 0 && (
              <div className="glass-card" style={{ marginBottom: '2rem' }}>
                <div className="card-header">
                  <h2 className="card-title">Price Chart</h2>
                  <div style={{ display: 'flex', gap: '1rem' }}>
                    <button onClick={fetchChartData} disabled={loading} className="btn btn-ghost btn-sm">
                      🔄 Refresh
                    </button>
                    <button onClick={syncData} disabled={loading} className="btn btn-primary btn-sm">
                      📥 Sync Data
                    </button>
                  </div>
                </div>
                <PriceChart
                  data={chartData}
                  symbol={symbol}
                  news={news}
                  onNewsClick={handleNewsClick}
                  selectedNewsId={selectedNewsId}
                />
              </div>
            )}

            {/* 快速操作 */}
            <div className="glass-card">
              <div className="card-header">
                <h2 className="card-title">Quick Actions</h2>
              </div>
              <div style={{ display: 'grid', gridTemplateColumns: 'repeat(2, 1fr)', gap: '1rem' }}>
                <button onClick={() => runBacktest('simple_ma')} disabled={loading} className="btn btn-success">
                  📈 MA Strategy Backtest
                </button>
                <button onClick={() => runBacktest('rsi')} disabled={loading} className="btn btn-success">
                  📊 RSI Strategy Backtest
                </button>
              </div>
            </div>
          </div>

          {/* 侧边栏 */}
          <div className="side-panel">
            {/* 价格预警 */}
            <div className="glass-card">
              <AlertPanel
                symbol={symbol}
                currentPrice={ticker?.price || 0}
                onAlertTriggered={handleAlertTriggered}
                botConfigs={botConfigs}
              />
            </div>

            {/* 新闻面板 */}
            <div className="glass-card">
              <NewsPanel
                news={news}
                onNewsClick={handleNewsClick}
                selectedNewsId={selectedNewsId}
              />
            </div>
          </div>
        </main>
      ) : (
        <main className="main-content" style={{ gridTemplateColumns: '1fr', padding: '2rem 5rem' }}>
          <div className="glass-card">
            <div className="card-header">
              <h2 className="card-title">Strategy Editor</h2>
            </div>
            <StrategyEditor />
          </div>
        </main>
      )}

      {/* 预警通知 */}
      {triggeredAlert && (
        <AlertNotification
          alert={triggeredAlert}
          onDismiss={dismissAlert}
          onView={viewAlertDetails}
        />
      )}

      {/* 机器人设置模态框 */}
      {showBotSettings && (
        <div className="modal-overlay" onClick={() => setShowBotSettings(false)}>
          <div className="glass-card" style={{ maxWidth: '800px', width: '90%', maxHeight: '90vh', overflow: 'auto' }} onClick={e => e.stopPropagation()}>
            <div className="card-header" style={{ position: 'sticky', top: 0, background: 'var(--glass-bg)', backdropFilter: 'blur(20px)', zIndex: 10 }}>
              <h2 className="card-title">Bot Notifications</h2>
              <button className="btn btn-ghost btn-icon" onClick={() => setShowBotSettings(false)}>
                ×
              </button>
            </div>
            <BotSettings onSave={saveBotConfigs} />
          </div>
        </div>
      )}

      {/* AI 助手侧边栏 */}
      <div className={`ai-sidebar ${showAIAssistant ? 'open' : ''}`}>
        <div className="ai-sidebar-header">
          <h2 className="ai-sidebar-title">AI Trading Assistant</h2>
          <button className="btn btn-ghost btn-icon" onClick={() => setShowAIAssistant(false)}>
            ×
          </button>
        </div>
        <div className="ai-sidebar-content">
          <AIAssistant
            symbol={symbol}
            currentPrice={ticker?.price || 0}
            onExecuteAction={handleAIAction}
          />
        </div>
      </div>

      {/* AI 侧边栏遮罩 */}
      {showAIAssistant && (
        <div className="sidebar-overlay" onClick={() => setShowAIAssistant(false)} />
      )}
    </div>
  )
}

export default App
