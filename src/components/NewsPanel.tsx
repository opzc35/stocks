import { useState, useEffect } from 'react'
import './NewsPanel.css'

interface NewsItem {
  id: string
  title: string
  summary: string
  url: string
  source: string
  published_at: number
  image_url?: string
  category: string
  sentiment?: string
  tags: string[]
  language: string
}

export function NewsPanel() {
  const [news, setNews] = useState<NewsItem[]>([])
  const [loading, setLoading] = useState(false)
  const [selectedCategory, setSelectedCategory] = useState('all')
  const [selectedLanguage, setSelectedLanguage] = useState('all')

  useEffect(() => {
    loadNews()

    // 每5分钟刷新一次
    const interval = setInterval(loadNews, 5 * 60 * 1000)
    return () => clearInterval(interval)
  }, [selectedCategory, selectedLanguage])

  const loadNews = async () => {
    setLoading(true)
    try {
      const response = await fetch(
        `http://localhost:8000/api/news/latest?category=${selectedCategory}&language=${selectedLanguage}&limit=20`
      )
      const result = await response.json()

      if (result.success) {
        setNews(result.data)
      }
    } catch (error) {
      console.error('Error loading news:', error)
    } finally {
      setLoading(false)
    }
  }

  const formatTime = (timestamp: number) => {
    const date = new Date(timestamp)
    const now = new Date()
    const diff = now.getTime() - date.getTime()

    const minutes = Math.floor(diff / 60000)
    const hours = Math.floor(diff / 3600000)
    const days = Math.floor(diff / 86400000)

    if (minutes < 60) {
      return `${minutes}分钟前`
    } else if (hours < 24) {
      return `${hours}小时前`
    } else if (days < 7) {
      return `${days}天前`
    } else {
      return date.toLocaleDateString('zh-CN')
    }
  }

  const getSentimentIcon = (sentiment?: string) => {
    switch (sentiment) {
      case 'positive':
        return '📈'
      case 'negative':
        return '📉'
      default:
        return '📊'
    }
  }

  const getSentimentClass = (sentiment?: string) => {
    switch (sentiment) {
      case 'positive':
        return 'sentiment-positive'
      case 'negative':
        return 'sentiment-negative'
      default:
        return 'sentiment-neutral'
    }
  }

  return (
    <div className="news-panel">
      <div className="news-header">
        <h2 className="news-title">📰 全球新闻</h2>
        <button className="btn btn-ghost btn-sm" onClick={loadNews} disabled={loading}>
          {loading ? '🔄' : '刷新'}
        </button>
      </div>

      {/* 过滤器 */}
      <div className="news-filters">
        <div className="filter-group">
          <label className="filter-label">类别</label>
          <select
            className="filter-select"
            value={selectedCategory}
            onChange={(e) => setSelectedCategory(e.target.value)}
          >
            <option value="all">全部</option>
            <option value="crypto">加密货币</option>
            <option value="stock">股票</option>
            <option value="forex">外汇</option>
            <option value="commodity">大宗商品</option>
          </select>
        </div>

        <div className="filter-group">
          <label className="filter-label">语言</label>
          <select
            className="filter-select"
            value={selectedLanguage}
            onChange={(e) => setSelectedLanguage(e.target.value)}
          >
            <option value="all">全部</option>
            <option value="en">English</option>
            <option value="zh">中文</option>
          </select>
        </div>
      </div>

      {/* 新闻列表 */}
      <div className="news-list">
        {loading && news.length === 0 ? (
          <div className="news-loading">
            <div className="loading-spinner">🔄</div>
            <p>加载新闻中...</p>
          </div>
        ) : news.length === 0 ? (
          <div className="news-empty">
            <p>暂无新闻</p>
          </div>
        ) : (
          news.map((item) => (
            <div key={item.id} className={`news-item ${getSentimentClass(item.sentiment)}`}>
              <div className="news-item-header">
                <span className="news-sentiment">{getSentimentIcon(item.sentiment)}</span>
                <span className="news-source">{item.source}</span>
                <span className="news-time">{formatTime(item.published_at)}</span>
              </div>

              <a
                href={item.url}
                target="_blank"
                rel="noopener noreferrer"
                className="news-item-title"
              >
                {item.title}
              </a>

              <p className="news-item-summary">{item.summary}</p>

              {item.tags.length > 0 && (
                <div className="news-tags">
                  {item.tags.slice(0, 3).map((tag, index) => (
                    <span key={index} className="news-tag">
                      {tag}
                    </span>
                  ))}
                </div>
              )}
            </div>
          ))
        )}
      </div>
    </div>
  )
}
