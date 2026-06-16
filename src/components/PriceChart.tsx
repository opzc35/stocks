import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts'

interface ChartData {
  timestamp: number
  close: number
  sma_20?: number
  sma_50?: number
}

interface ChartProps {
  data: ChartData[]
  symbol: string
}

export function PriceChart({ data, symbol }: ChartProps) {
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
            formatter={(value: number) => [`$${value.toFixed(2)}`, '']}
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
        </LineChart>
      </ResponsiveContainer>
    </div>
  )
}
