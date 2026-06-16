import { useState, useEffect } from 'react'
import './MarketSelector.css'

interface Market {
  id: string
  name: string
  icon: string
  examples: string[]
}

interface SearchResult {
  symbol: string
  name: string
  market: string
  exchange: string
  currency: string
}

interface MarketSelectorProps {
  currentSymbol: string
  onSymbolChange: (symbol: string, market: string) => void
}

export function MarketSelector({ currentSymbol, onSymbolChange }: MarketSelectorProps) {
  const [markets, setMarkets] = useState<Market[]>([])
  const [selectedMarket, setSelectedMarket] = useState('crypto')
  const [searchQuery, setSearchQuery] = useState('')
  const [searchResults, setSearchResults] = useState<SearchResult[]>([])
  const [customSymbol, setCustomSymbol] = useState('')
  const [showSearch, setShowSearch] = useState(false)
  const [loading, setLoading] = useState(false)

  // 加载市场列表
  useEffect(() => {
    loadMarkets()
  }, [])

  const loadMarkets = async () => {
    try {
      const response = await fetch('http://localhost:8000/api/multi-market/markets')
      const result = await response.json()

      if (result.success) {
        setMarkets(result.data)
      }
    } catch (error) {
      console.error('Error loading markets:', error)
    }
  }

  // 搜索交易对
  const handleSearch = async (query: string) => {
    setSearchQuery(query)

    if (query.length < 2) {
      setSearchResults([])
      return
    }

    setLoading(true)
    try {
      const response = await fetch(
        `http://localhost:8000/api/multi-market/search?q=${encodeURIComponent(query)}&markets=${selectedMarket}`
      )
      const result = await response.json()

      if (result.success) {
        setSearchResults(result.data)
      }
    } catch (error) {
      console.error('Error searching:', error)
    } finally {
      setLoading(false)
    }
  }

  // 选择交易对
  const selectSymbol = (symbol: string, market: string) => {
    onSymbolChange(symbol, market)
    setShowSearch(false)
    setSearchQuery('')
    setSearchResults([])
  }

  // 添加自定义交易对
  const addCustomSymbol = () => {
    if (customSymbol.trim()) {
      onSymbolChange(customSymbol.trim(), selectedMarket)
      setCustomSymbol('')
      setShowSearch(false)
    }
  }

  return (
    <div className="market-selector">
      {/* 当前选择 */}
      <div className="current-selection">
        <button
          className="current-symbol-btn"
          onClick={() => setShowSearch(!showSearch)}
        >
          <span className="symbol-text">{currentSymbol}</span>
          <span className="dropdown-arrow">▼</span>
        </button>
      </div>

      {/* 搜索面板 */}
      {showSearch && (
        <div className="search-panel">
          <div className="search-panel-header">
            <h3>选择交易对</h3>
            <button
              className="btn btn-ghost btn-icon btn-sm"
              onClick={() => setShowSearch(false)}
            >
              ×
            </button>
          </div>

          {/* 市场选择 */}
          <div className="market-tabs">
            {markets.map((market) => (
              <button
                key={market.id}
                className={`market-tab ${selectedMarket === market.id ? 'active' : ''}`}
                onClick={() => setSelectedMarket(market.id)}
              >
                <span className="market-icon">{market.icon}</span>
                <span className="market-name">{market.name}</span>
              </button>
            ))}
          </div>

          {/* 搜索框 */}
          <div className="search-input-wrapper">
            <input
              type="text"
              className="search-input"
              placeholder="搜索交易对... (例: BTC, AAPL, 腾讯)"
              value={searchQuery}
              onChange={(e) => handleSearch(e.target.value)}
              autoFocus
            />
            {loading && <span className="search-loading">🔄</span>}
          </div>

          {/* 搜索结果 */}
          {searchResults.length > 0 && (
            <div className="search-results">
              <div className="results-header">搜索结果</div>
              {searchResults.map((result, index) => (
                <button
                  key={index}
                  className="result-item"
                  onClick={() => selectSymbol(result.symbol, result.market)}
                >
                  <div className="result-main">
                    <span className="result-symbol">{result.symbol}</span>
                    <span className="result-name">{result.name}</span>
                  </div>
                  <div className="result-meta">
                    <span className="result-exchange">{result.exchange}</span>
                    <span className="result-currency">{result.currency}</span>
                  </div>
                </button>
              ))}
            </div>
          )}

          {/* 常用交易对 */}
          {searchQuery.length === 0 && (
            <div className="popular-symbols">
              <div className="popular-header">
                常用 {markets.find(m => m.id === selectedMarket)?.name}
              </div>
              <div className="popular-list">
                {markets.find(m => m.id === selectedMarket)?.examples.map((symbol) => (
                  <button
                    key={symbol}
                    className="popular-item"
                    onClick={() => selectSymbol(symbol, selectedMarket)}
                  >
                    {symbol}
                  </button>
                ))}
              </div>
            </div>
          )}

          {/* 自定义输入 */}
          <div className="custom-input-section">
            <div className="custom-header">自定义交易对</div>
            <div className="custom-input-wrapper">
              <input
                type="text"
                className="custom-input"
                placeholder="输入交易对代码..."
                value={customSymbol}
                onChange={(e) => setCustomSymbol(e.target.value)}
                onKeyPress={(e) => {
                  if (e.key === 'Enter') {
                    addCustomSymbol()
                  }
                }}
              />
              <button
                className="btn btn-primary btn-sm"
                onClick={addCustomSymbol}
                disabled={!customSymbol.trim()}
              >
                添加
              </button>
            </div>
            <div className="custom-hint">
              提示：
              {selectedMarket === 'crypto' && '加密货币格式如 BTC/USDT'}
              {selectedMarket === 'us' && '美股格式如 AAPL, TSLA'}
              {selectedMarket === 'hk' && '港股格式如 0700.HK, 9988.HK'}
              {selectedMarket === 'cn' && 'A股格式如 600519.SS, 000858.SZ'}
            </div>
          </div>
        </div>
      )}
    </div>
  )
}
