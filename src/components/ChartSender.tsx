import { useState } from 'react'
import './ChartSender.css'

interface ChartAnnotation {
  type: 'text' | 'arrow' | 'line' | 'box'
  position: { x: number; y: number; x2?: number; y2?: number }
  text?: string
  color: string
}

interface ChartConfig {
  symbol: string
  timeframe: string
  periods: number
  indicators: string[]
  annotations: ChartAnnotation[]
  title?: string
}

interface BotConfig {
  platform: string
  bot_token?: string
  chat_id?: string
  webhook_url?: string
}

export function ChartSender() {
  const [chartConfig, setChartConfig] = useState<ChartConfig>({
    symbol: 'BTC/USDT',
    timeframe: '1h',
    periods: 100,
    indicators: ['MA20', 'MA50', 'RSI'],
    annotations: [],
    title: ''
  })

  const [annotations, setAnnotations] = useState<ChartAnnotation[]>([])
  const [selectedBots, setSelectedBots] = useState<string[]>([])
  const [caption, setCaption] = useState('')
  const [previewImage, setPreviewImage] = useState<string | null>(null)
  const [sending, setSending] = useState(false)

  // 添加批注
  const addAnnotation = (type: ChartAnnotation['type']) => {
    const newAnnotation: ChartAnnotation = {
      type,
      position: { x: 50, y: 67000 },
      color: type === 'text' ? '#0ba360' : '#f857a6',
      text: type === 'text' ? '批注文字' : undefined
    }

    if (type === 'arrow' || type === 'line') {
      newAnnotation.position.x2 = 70
      newAnnotation.position.y2 = 66000
    }

    setAnnotations([...annotations, newAnnotation])
  }

  // 更新批注
  const updateAnnotation = (index: number, updates: Partial<ChartAnnotation>) => {
    const updated = [...annotations]
    updated[index] = { ...updated[index], ...updates }
    setAnnotations(updated)
  }

  // 删除批注
  const removeAnnotation = (index: number) => {
    setAnnotations(annotations.filter((_, i) => i !== index))
  }

  // 预览图表
  const previewChart = async () => {
    try {
      const response = await fetch('http://localhost:8001/api/chart/generate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          ...chartConfig,
          annotations
        })
      })

      const result = await response.json()

      if (result.success) {
        setPreviewImage(`data:image/png;base64,${result.data.image}`)
      } else {
        alert('预览失败: ' + result.error)
      }
    } catch (error) {
      console.error('Preview error:', error)
      alert('预览失败')
    }
  }

  // 发送到机器人
  const sendToBot = async (botConfig: BotConfig) => {
    setSending(true)
    try {
      const response = await fetch('http://localhost:8001/api/chart/send', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          platform: botConfig.platform,
          config: {
            ...chartConfig,
            annotations
          },
          bot_config: botConfig,
          caption
        })
      })

      const result = await response.json()

      if (result.success) {
        alert(`✅ 图表已发送到 ${botConfig.platform}`)
      } else {
        alert('发送失败: ' + result.error)
      }
    } catch (error) {
      console.error('Send error:', error)
      alert('发送失败')
    } finally {
      setSending(false)
    }
  }

  return (
    <div className="chart-sender">
      <div className="chart-sender-header">
        <h2>📊 图表发送工具</h2>
        <p className="text-muted">生成带批注的K线图，发送到社交媒体机器人</p>
      </div>

      <div className="chart-sender-content">
        {/* 基础配置 */}
        <section className="config-section">
          <h3>基础配置</h3>
          <div className="config-grid">
            <div className="input-group">
              <label className="input-label">交易对</label>
              <select
                className="input"
                value={chartConfig.symbol}
                onChange={(e) => setChartConfig({ ...chartConfig, symbol: e.target.value })}
              >
                <option value="BTC/USDT">BTC/USDT</option>
                <option value="ETH/USDT">ETH/USDT</option>
                <option value="BNB/USDT">BNB/USDT</option>
              </select>
            </div>

            <div className="input-group">
              <label className="input-label">时间周期</label>
              <select
                className="input"
                value={chartConfig.timeframe}
                onChange={(e) => setChartConfig({ ...chartConfig, timeframe: e.target.value })}
              >
                <option value="1m">1分钟</option>
                <option value="5m">5分钟</option>
                <option value="15m">15分钟</option>
                <option value="1h">1小时</option>
                <option value="4h">4小时</option>
                <option value="1d">1天</option>
              </select>
            </div>

            <div className="input-group">
              <label className="input-label">K线数量</label>
              <input
                type="number"
                className="input"
                value={chartConfig.periods}
                onChange={(e) => setChartConfig({ ...chartConfig, periods: parseInt(e.target.value) })}
                min={20}
                max={500}
              />
            </div>

            <div className="input-group">
              <label className="input-label">图表标题</label>
              <input
                type="text"
                className="input"
                value={chartConfig.title}
                onChange={(e) => setChartConfig({ ...chartConfig, title: e.target.value })}
                placeholder="留空使用默认"
              />
            </div>
          </div>

          {/* 技术指标 */}
          <div className="input-group">
            <label className="input-label">技术指标</label>
            <div className="checkbox-group">
              {['MA20', 'MA50', 'RSI', 'MACD', 'BOLL'].map((indicator) => (
                <label key={indicator} className="checkbox-label">
                  <input
                    type="checkbox"
                    checked={chartConfig.indicators.includes(indicator)}
                    onChange={(e) => {
                      if (e.target.checked) {
                        setChartConfig({
                          ...chartConfig,
                          indicators: [...chartConfig.indicators, indicator]
                        })
                      } else {
                        setChartConfig({
                          ...chartConfig,
                          indicators: chartConfig.indicators.filter((i) => i !== indicator)
                        })
                      }
                    }}
                  />
                  {indicator}
                </label>
              ))}
            </div>
          </div>
        </section>

        {/* 批注工具 */}
        <section className="config-section">
          <h3>图表批注</h3>
          <div className="annotation-tools">
            <button className="btn btn-sm btn-secondary" onClick={() => addAnnotation('text')}>
              📝 文字标注
            </button>
            <button className="btn btn-sm btn-secondary" onClick={() => addAnnotation('arrow')}>
              ➡️ 箭头
            </button>
            <button className="btn btn-sm btn-secondary" onClick={() => addAnnotation('line')}>
              📏 趋势线
            </button>
            <button className="btn btn-sm btn-secondary" onClick={() => addAnnotation('box')}>
              ⬜ 方框
            </button>
          </div>

          {/* 批注列表 */}
          <div className="annotations-list">
            {annotations.map((ann, index) => (
              <div key={index} className="annotation-item">
                <div className="annotation-header">
                  <span className="annotation-type">
                    {ann.type === 'text' && '📝'}
                    {ann.type === 'arrow' && '➡️'}
                    {ann.type === 'line' && '📏'}
                    {ann.type === 'box' && '⬜'}
                    {' '}{ann.type}
                  </span>
                  <button
                    className="btn btn-ghost btn-icon btn-sm"
                    onClick={() => removeAnnotation(index)}
                  >
                    ×
                  </button>
                </div>

                <div className="annotation-fields">
                  {ann.type === 'text' && (
                    <div className="input-group">
                      <label className="input-label">文字内容</label>
                      <input
                        type="text"
                        className="input input-sm"
                        value={ann.text || ''}
                        onChange={(e) => updateAnnotation(index, { text: e.target.value })}
                      />
                    </div>
                  )}

                  <div className="input-group">
                    <label className="input-label">颜色</label>
                    <select
                      className="input input-sm"
                      value={ann.color}
                      onChange={(e) => updateAnnotation(index, { color: e.target.value })}
                    >
                      <option value="#0ba360">绿色（上涨）</option>
                      <option value="#f857a6">红色（下跌）</option>
                      <option value="#0070f3">蓝色（信息）</option>
                      <option value="#f5a623">黄色（警告）</option>
                    </select>
                  </div>

                  <div className="position-grid">
                    <div className="input-group">
                      <label className="input-label">位置 X</label>
                      <input
                        type="number"
                        className="input input-sm"
                        value={ann.position.x}
                        onChange={(e) =>
                          updateAnnotation(index, {
                            position: { ...ann.position, x: parseInt(e.target.value) }
                          })
                        }
                      />
                    </div>
                    <div className="input-group">
                      <label className="input-label">位置 Y</label>
                      <input
                        type="number"
                        className="input input-sm"
                        value={ann.position.y}
                        onChange={(e) =>
                          updateAnnotation(index, {
                            position: { ...ann.position, y: parseInt(e.target.value) }
                          })
                        }
                      />
                    </div>
                  </div>
                </div>
              </div>
            ))}

            {annotations.length === 0 && (
              <div className="empty-state">
                <p className="text-muted">暂无批注，点击上方按钮添加</p>
              </div>
            )}
          </div>
        </section>

        {/* 消息内容 */}
        <section className="config-section">
          <h3>消息内容</h3>
          <div className="input-group">
            <label className="input-label">图片说明文字</label>
            <textarea
              className="input"
              rows={5}
              value={caption}
              onChange={(e) => setCaption(e.target.value)}
              placeholder="输入图片的说明文字..."
            />
          </div>
          <div className="caption-templates">
            <button
              className="btn btn-sm btn-ghost"
              onClick={() =>
                setCaption(
                  `📊 ${chartConfig.symbol} 技术分析\n\n📈 趋势: 上涨\n📊 RSI: 62 (中性)\n\n批注说明:\n• 绿色标记: 突破阻力位\n• 红色箭头: 回调支撑位`
                )
              }
            >
              使用模板1
            </button>
            <button
              className="btn btn-sm btn-ghost"
              onClick={() =>
                setCaption(
                  `🔥 ${chartConfig.symbol} 行情分析\n\n当前价格走势强劲，建议关注关键位置。\n\n⚠️ 风险提示: 注意止损设置`
                )
              }
            >
              使用模板2
            </button>
          </div>
        </section>

        {/* 预览和发送 */}
        <section className="config-section">
          <h3>预览和发送</h3>

          <div className="action-buttons">
            <button className="btn btn-primary" onClick={previewChart}>
              👁️ 预览图表
            </button>
          </div>

          {previewImage && (
            <div className="chart-preview">
              <img src={previewImage} alt="Chart Preview" />
            </div>
          )}

          <div className="send-section">
            <p className="text-muted">
              选择要发送的机器人（需要先在机器人设置中配置）
            </p>
            <div className="bot-list">
              <button
                className="btn btn-success"
                onClick={() => {
                  // 这里应该从配置中读取实际的 bot 配置
                  sendToBot({
                    platform: 'telegram',
                    bot_token: 'YOUR_BOT_TOKEN',
                    chat_id: 'YOUR_CHAT_ID'
                  })
                }}
                disabled={sending || !previewImage}
              >
                📱 发送到 Telegram
              </button>
              <button className="btn btn-success" disabled={sending || !previewImage}>
                💬 发送到 Discord
              </button>
              <button className="btn btn-success" disabled={sending || !previewImage}>
                💼 发送到 Slack
              </button>
              <button className="btn btn-success" disabled={sending || !previewImage}>
                💚 发送到企业微信
              </button>
            </div>
          </div>
        </section>
      </div>
    </div>
  )
}
