import { useState } from 'react'
import './NewsPanel.css'

export interface NewsItem {
  id: string
  timestamp: number
  title: string
  content: string
  sentiment: 'positive' | 'negative' | 'neutral'
  source: string
  tags: string[]
}

interface NewsPanelProps {
  news: NewsItem[]
  onNewsClick?: (newsItem: NewsItem) => void
  selectedNewsId?: string
}

export function NewsPanel({ news, onNewsClick, selectedNewsId }: NewsPanelProps) {
  const [filterSentiment, setFilterSentiment] = useState<string>('all')

  const filteredNews = filterSentiment === 'all'
    ? news
    : news.filter(item => item.sentiment === filterSentiment)

  const formatDate = (timestamp: number) => {
    const date = new Date(timestamp)
    return date.toLocaleString('zh-CN', {
      month: '2-digit',
      day: '2-digit',
      hour: '2-digit',
      minute: '2-digit'
    })
  }

  const getSentimentIcon = (sentiment: string) => {
    switch (sentiment) {
      case 'positive': return '📈'
      case 'negative': return '📉'
      default: return '📰'
    }
  }

  const getSentimentColor = (sentiment: string) => {
    switch (sentiment) {
      case 'positive': return 'sentiment-positive'
      case 'negative': return 'sentiment-negative'
      default: return 'sentiment-neutral'
    }
  }

  return (
    <div className="news-panel">
      <div className="news-header">
        <h3>📰 新闻动态</h3>
        <div className="news-filters">
          <button
            className={`filter-btn ${filterSentiment === 'all' ? 'active' : ''}`}
            onClick={() => setFilterSentiment('all')}
          >
            全部
          </button>
          <button
            className={`filter-btn ${filterSentiment === 'positive' ? 'active' : ''}`}
            onClick={() => setFilterSentiment('positive')}
          >
            📈 利好
          </button>
          <button
            className={`filter-btn ${filterSentiment === 'negative' ? 'active' : ''}`}
            onClick={() => setFilterSentiment('negative')}
          >
            📉 利空
          </button>
          <button
            className={`filter-btn ${filterSentiment === 'neutral' ? 'active' : ''}`}
            onClick={() => setFilterSentiment('neutral')}
          >
            📰 中性
          </button>
        </div>
      </div>

      <div className="news-list">
        {filteredNews.length > 0 ? (
          filteredNews.map(item => (
            <div
              key={item.id}
              className={`news-item ${getSentimentColor(item.sentiment)} ${selectedNewsId === item.id ? 'selected' : ''}`}
              onClick={() => onNewsClick?.(item)}
            >
              <div className="news-item-header">
                <span className="news-icon">{getSentimentIcon(item.sentiment)}</span>
                <span className="news-time">{formatDate(item.timestamp)}</span>
              </div>
              <h4 className="news-title">{item.title}</h4>
              <p className="news-content">{item.content}</p>
              <div className="news-footer">
                <span className="news-source">{item.source}</span>
                <div className="news-tags">
                  {item.tags.map((tag, idx) => (
                    <span key={idx} className="news-tag">#{tag}</span>
                  ))}
                </div>
              </div>
            </div>
          ))
        ) : (
          <div className="no-news">
            <p>暂无{filterSentiment !== 'all' ? '相关' : ''}新闻</p>
          </div>
        )}
      </div>
    </div>
  )
}
