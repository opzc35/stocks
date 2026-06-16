import { useState, useEffect } from 'react'
import './App.css'
import { PriceChart } from './components/PriceChart'
import { StrategyEditor } from './components/StrategyEditor'
import { NewsPanel, type NewsItem } from './components/NewsPanel'
import { AlertPanel, AlertNotification, type PriceAlert, type BotConfig } from './components/AlertPanel'
import { BotSettings } from './components/BotSettings'

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
  const [news, setNews] = useState<NewsItem[]>([])
  const [selectedNewsId, setSelectedNewsId] = useState<string | undefined>()
  const [triggeredAlert, setTriggeredAlert] = useState<PriceAlert | null>(null)
  const [botConfigs, setBotConfigs] = useState<BotConfig[]>([])
  const [showBotSettings, setShowBotSettings] = useState(false)

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

  // 获取新闻数据（模拟数据，后续可以接入真实API）
  const fetchNews = async () => {
    // 模拟新闻数据
    const mockNews: NewsItem[] = [
      {
        id: '1',
        timestamp: Date.now() - 3600000 * 24, // 1天前
        title: '比特币突破重要阻力位',
        content: '比特币价格突破关键阻力位 $65,000，交易量显著增加，市场情绪乐观。技术分析显示可能继续上涨至 $70,000。',
        sentiment: 'positive',
        source: 'CoinDesk',
        tags: ['BTC', '突破', '技术分析']
      },
      {
        id: '2',
        timestamp: Date.now() - 3600000 * 12, // 12小时前
        title: 'SEC 推迟比特币 ETF 决定',
        content: '美国证券交易委员会再次推迟对现货比特币 ETF 的决定，市场短期承压。分析师认为这是正常流程。',
        sentiment: 'negative',
        source: 'Bloomberg',
        tags: ['监管', 'ETF', 'SEC']
      },
      {
        id: '3',
        timestamp: Date.now() - 3600000 * 6, // 6小时前
        title: '主要交易所公布储备金证明',
        content: '多家主要加密货币交易所发布储备金证明报告，提高透明度，增强用户信心。',
        sentiment: 'neutral',
        source: 'CoinTelegraph',
        tags: ['交易所', '透明度']
      },
      {
        id: '4',
        timestamp: Date.now() - 3600000 * 2, // 2小时前
        title: '机构投资者持续增持比特币',
        content: 'Grayscale 和 MicroStrategy 等机构投资者继续增持比特币，显示长期看好态度。链上数据显示大额转账增加。',
        sentiment: 'positive',
        source: 'The Block',
        tags: ['机构', '链上数据', '增持']
      },
      {
        id: '5',
        timestamp: Date.now() - 3600000 * 48, // 2天前
        title: '以太坊网络升级成功完成',
        content: '以太坊成功完成最新网络升级，Gas 费用降低 30%，交易速度提升，DeFi 生态受益。',
        sentiment: 'positive',
        source: 'Ethereum Foundation',
        tags: ['ETH', '升级', 'DeFi']
      }
    ]
    setNews(mockNews)
  }

  // 处理新闻点击
  const handleNewsClick = (newsItem: NewsItem) => {
    setSelectedNewsId(newsItem.id === selectedNewsId ? undefined : newsItem.id)
  }

  // 处理预警触发
  const handleAlertTriggered = (alert: PriceAlert) => {
    setTriggeredAlert(alert)

    // 5秒后自动消失
    setTimeout(() => {
      setTriggeredAlert(null)
    }, 10000)
  }

  // 关闭预警通知
  const dismissAlert = () => {
    setTriggeredAlert(null)
  }

  // 查看预警详情
  const viewAlertDetails = () => {
    setTriggeredAlert(null)
    // 可以滚动到预警面板或高亮预警项
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
    fetchNews()
    loadBotConfigs()

    // 每10秒更新一次价格
    const interval = setInterval(fetchTicker, 10000)
    return () => clearInterval(interval)
  }, [symbol])

  // 加载机器人配置
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

  // 保存机器人配置
  const saveBotConfigs = (configs: BotConfig[]) => {
    setBotConfigs(configs)
    localStorage.setItem('botConfigs', JSON.stringify(configs))
  }

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
            <button
              className="tab-btn"
              onClick={() => setShowBotSettings(true)}
            >
              🤖 机器人
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
        <main className="main-content dashboard-layout">
        {/* 左侧：图表和指标 */}
        <div className="main-column">
          {/* 价格图表 */}
          {chartData.length > 0 && (
            <section className="card chart-card">
              <PriceChart
                data={chartData}
                symbol={symbol}
                news={news}
                onNewsClick={handleNewsClick}
                selectedNewsId={selectedNewsId}
              />
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
        </div>

        {/* 右侧：新闻和预警面板 */}
        <aside className="side-column">
          <section className="card alert-card">
            <AlertPanel
              symbol={symbol}
              currentPrice={ticker?.price || 0}
              onAlertTriggered={handleAlertTriggered}
              botConfigs={botConfigs}
            />
          </section>
          <section className="card news-card">
            <NewsPanel
              news={news}
              onNewsClick={handleNewsClick}
              selectedNewsId={selectedNewsId}
            />
          </section>
        </aside>
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

      {/* 预警通知弹窗 */}
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
          <div className="modal-content bot-settings-modal" onClick={e => e.stopPropagation()}>
            <div className="modal-header">
              <h2>🤖 机器人通知设置</h2>
              <button className="btn-close-modal" onClick={() => setShowBotSettings(false)}>
                ×
              </button>
            </div>
            <div className="modal-body-wrapper">
              <BotSettings onSave={saveBotConfigs} />
            </div>
          </div>
        </div>
      )}
    </div>
  )
}

export default App
