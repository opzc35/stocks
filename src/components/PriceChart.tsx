import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, ReferenceDot } from 'recharts'
import type { NewsItem } from './NewsPanel'

interface ChartData {
  timestamp: number
  close: number
  sma_20?: number
  sma_50?: number
}

interface ChartProps {
  data: ChartData[]
  symbol: string
  news?: NewsItem[]
  onNewsClick?: (newsItem: NewsItem) => void
  selectedNewsId?: string
}

export function PriceChart({ data, symbol, news = [], onNewsClick, selectedNewsId }: ChartProps) {
  // 转换时间戳为可读格式
  const formatTimestamp = (timestamp: number) => {
    const date = new Date(timestamp)
    return `${date.getMonth() + 1}/${date.getDate()} ${date.getHours()}:${String(date.getMinutes()).padStart(2, '0')}`
  }

  // 格式化价格
  const formatPrice = (value: number) => {
    return `$${value.toFixed(2)}`
  }

  const chartData = data.map(item => ({
    ...item,
    time: formatTimestamp(item.timestamp)
  }))

  // 将新闻映射到图表数据点
  const newsMarkers = news.map(newsItem => {
    // 找到最接近的数据点
    const closestDataPoint = chartData.reduce((prev, curr) => {
      const prevDiff = Math.abs(prev.timestamp - newsItem.timestamp)
      const currDiff = Math.abs(curr.timestamp - newsItem.timestamp)
      return currDiff < prevDiff ? curr : prev
    })
    return {
      ...newsItem,
      x: closestDataPoint.time,
      y: closestDataPoint.close
    }
  })

  // 自定义新闻标记点
  const NewsMarker = (props: any) => {
    const { cx, cy, newsItem } = props
    const isSelected = selectedNewsId === newsItem.id

    let fill = '#6b7280'
    if (newsItem.sentiment === 'positive') fill = '#10b981'
    if (newsItem.sentiment === 'negative') fill = '#ef4444'

    return (
      <g
        onClick={() => onNewsClick?.(newsItem)}
        style={{ cursor: 'pointer' }}
      >
        <circle
          cx={cx}
          cy={cy}
          r={isSelected ? 8 : 6}
          fill={fill}
          stroke={isSelected ? '#ffffff' : fill}
          strokeWidth={isSelected ? 2 : 0}
          opacity={0.9}
        />
        {isSelected && (
          <circle
            cx={cx}
            cy={cy}
            r={12}
            fill="none"
            stroke={fill}
            strokeWidth={2}
            opacity={0.5}
          />
        )}
      </g>
    )
  }

  return (
    <div className="chart-container">
      <h3>{symbol} 价格走势</h3>
      <ResponsiveContainer width="100%" height={400}>
        <LineChart data={chartData} margin={{ top: 5, right: 30, left: 20, bottom: 5 }}>
          <CartesianGrid strokeDasharray="3 3" stroke="#475569" />
          <XAxis
            dataKey="time"
            stroke="#cbd5e1"
            tick={{ fill: '#cbd5e1', fontSize: 12 }}
          />
          <YAxis
            stroke="#cbd5e1"
            tick={{ fill: '#cbd5e1', fontSize: 12 }}
            tickFormatter={formatPrice}
          />
          <Tooltip
            contentStyle={{
              backgroundColor: '#1e293b',
              border: '1px solid #475569',
              borderRadius: '8px',
              color: '#f1f5f9'
            }}
            formatter={(value: any) => [`$${Number(value).toFixed(2)}`, '']}
          />
          <Legend
            wrapperStyle={{ color: '#cbd5e1' }}
          />
          <Line
            type="monotone"
            dataKey="close"
            stroke="#10b981"
            strokeWidth={2}
            dot={false}
            name="价格"
          />
          {chartData[0]?.sma_20 && (
            <Line
              type="monotone"
              dataKey="sma_20"
              stroke="#3b82f6"
              strokeWidth={2}
              dot={false}
              name="SMA(20)"
            />
          )}
          {chartData[0]?.sma_50 && (
            <Line
              type="monotone"
              dataKey="sma_50"
              stroke="#f59e0b"
              strokeWidth={2}
              dot={false}
              name="SMA(50)"
            />
          )}

          {/* 渲染新闻标记点 */}
          {newsMarkers.map((marker) => (
            <ReferenceDot
              key={marker.id}
              x={marker.x}
              y={marker.y}
              shape={<NewsMarker newsItem={marker} />}
            />
          ))}
        </LineChart>
      </ResponsiveContainer>
    </div>
  )
}
