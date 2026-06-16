import { useState, useEffect } from 'react'
import './AlertPanel.css'

export interface PriceAlert {
  id: string
  symbol: string
  condition: 'above' | 'below'
  targetPrice: number
  currentPrice?: number
  isTriggered: boolean
  createdAt: number
  triggeredAt?: number
  message?: string
}

export interface BotConfig {
  id: string
  platform: 'telegram' | 'discord' | 'slack' | 'wechat'
  name: string
  enabled: boolean
  config: {
    botToken?: string
    chatId?: string
    webhookUrl?: string
    channelId?: string
    apiKey?: string
  }
}

interface AlertPanelProps {
  symbol: string
  currentPrice: number
  onAlertTriggered?: (alert: PriceAlert) => void
  botConfigs?: BotConfig[]
}

export function AlertPanel({ symbol, currentPrice, onAlertTriggered, botConfigs = [] }: AlertPanelProps) {
  const [alerts, setAlerts] = useState<PriceAlert[]>([])
  const [targetPrice, setTargetPrice] = useState('')
  const [condition, setCondition] = useState<'above' | 'below'>('above')

  // 发送到机器人
  const sendToBots = async (alert: PriceAlert) => {
    const enabledBots = botConfigs.filter(bot => bot.enabled)

    if (enabledBots.length === 0) return

    const message = formatAlertMessage(alert)

    for (const bot of enabledBots) {
      try {
        await sendBotNotification(bot, message, alert)
      } catch (error) {
        console.error(`Failed to send to ${bot.platform}:`, error)
      }
    }
  }

  // 格式化预警消息
  const formatAlertMessage = (alert: PriceAlert) => {
    const emoji = alert.condition === 'above' ? '🚀' : '⚠️'
    const action = alert.condition === 'above' ? '突破' : '跌破'

    return `${emoji} 价格预警触发！

交易对: ${alert.symbol}
类型: ${action}
目标价格: $${alert.targetPrice.toFixed(2)}
当前价格: $${alert.currentPrice?.toFixed(2)}
时间: ${new Date(alert.triggeredAt || Date.now()).toLocaleString('zh-CN')}

${alert.message || ''}`
  }

  // 发送机器人通知
  const sendBotNotification = async (bot: BotConfig, message: string, alert: PriceAlert) => {
    switch (bot.platform) {
      case 'telegram':
        return sendTelegramMessage(bot, message)
      case 'discord':
        return sendDiscordMessage(bot, message, alert)
      case 'slack':
        return sendSlackMessage(bot, message, alert)
      case 'wechat':
        return sendWechatMessage(bot, message)
    }
  }

  // Telegram 通知
  const sendTelegramMessage = async (bot: BotConfig, message: string) => {
    const url = `https://api.telegram.org/bot${bot.config.botToken}/sendMessage`

    await fetch(url, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        chat_id: bot.config.chatId,
        text: message,
        parse_mode: 'HTML'
      })
    })
  }

  // Discord 通知
  const sendDiscordMessage = async (bot: BotConfig, message: string, alert: PriceAlert) => {
    const color = alert.condition === 'above' ? 0x10b981 : 0xf59e0b

    await fetch(bot.config.webhookUrl!, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        embeds: [{
          title: '🔔 价格预警触发',
          description: message,
          color: color,
          timestamp: new Date().toISOString()
        }]
      })
    })
  }

  // Slack 通知
  const sendSlackMessage = async (bot: BotConfig, message: string, alert: PriceAlert) => {
    const color = alert.condition === 'above' ? '#10b981' : '#f59e0b'

    await fetch(bot.config.webhookUrl!, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        text: '🔔 价格预警触发',
        attachments: [{
          color: color,
          text: message,
          footer: '量化交易系统',
          ts: Math.floor(Date.now() / 1000)
        }]
      })
    })
  }

  // 企业微信通知
  const sendWechatMessage = async (bot: BotConfig, message: string) => {
    await fetch(bot.config.webhookUrl!, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        msgtype: 'text',
        text: {
          content: message
        }
      })
    })
  }

  // 检查预警触发
  useEffect(() => {
    alerts.forEach(alert => {
      if (alert.isTriggered) return

      const shouldTrigger =
        (alert.condition === 'above' && currentPrice >= alert.targetPrice) ||
        (alert.condition === 'below' && currentPrice <= alert.targetPrice)

      if (shouldTrigger) {
        const triggeredAlert = {
          ...alert,
          isTriggered: true,
          triggeredAt: Date.now(),
          currentPrice,
          message: `${symbol} 价格已${alert.condition === 'above' ? '突破' : '跌破'} $${alert.targetPrice.toFixed(2)}`
        }

        setAlerts(prev => prev.map(a => a.id === alert.id ? triggeredAlert : a))

        // 通知父组件
        onAlertTriggered?.(triggeredAlert)

        // 发送到机器人
        sendToBots(triggeredAlert)

        // 播放提示音（如果浏览器支持）
        try {
          const audio = new Audio('data:audio/wav;base64,UklGRnoGAABXQVZFZm10IBAAAAABAAEAQB8AAEAfAAABAAgAZGF0YQoGAACBhYqFbF1fdJivrJBhNjVgodDbq2EcBj+a2/LDciUFLIHO8tiJNwgZaLvt559NEAxQp+PwtmMcBjiR1/LMeSwFJHfH8N2QQAoUXrTp66hVFApGn+DyvmwhBjJ+0fPTgjMGHm7A7+OZSA0PVqzn77BdGAg+ltryxnMnBSp50O/cjT0JGF+17OahUhENTKXh8bllHAU2jdXzzn0vBSF1xe/glEILElyx6OyhUBEMSp/e8sFtIgYug8zvz34xBBxqwO7ol0QNEFK06Oy0Yh0HNI/Y88qBMgUfc8Tv04U1Bxlgsevoo1QSDU2o4vLAaR8GK4DM79N+LwQebL7s5Z5NDg5Qque2Zhwi')
          audio.play().catch(() => {}) // 忽略自动播放限制错误
        } catch (e) {
          // 忽略音频播放错误
        }
      }
    })
  }, [currentPrice, alerts, symbol, onAlertTriggered])

  // 添加预警
  const addAlert = () => {
    const price = parseFloat(targetPrice)
    if (isNaN(price) || price <= 0) {
      alert('请输入有效的价格')
      return
    }

    const newAlert: PriceAlert = {
      id: Date.now().toString(),
      symbol,
      condition,
      targetPrice: price,
      isTriggered: false,
      createdAt: Date.now()
    }

    setAlerts(prev => [...prev, newAlert])
    setTargetPrice('')
  }

  // 删除预警
  const deleteAlert = (id: string) => {
    setAlerts(prev => prev.filter(a => a.id !== id))
  }

  // 重置预警
  const resetAlert = (id: string) => {
    setAlerts(prev => prev.map(a =>
      a.id === id ? { ...a, isTriggered: false, triggeredAt: undefined, currentPrice: undefined } : a
    ))
  }

  // 格式化时间
  const formatTime = (timestamp: number) => {
    const date = new Date(timestamp)
    return date.toLocaleString('zh-CN', {
      month: '2-digit',
      day: '2-digit',
      hour: '2-digit',
      minute: '2-digit'
    })
  }

  return (
    <div className="alert-panel">
      <div className="alert-header">
        <h3>🔔 价格预警</h3>
        <div className="alert-add-form">
          <div className="alert-form-row">
            <select
              className="alert-select"
              value={condition}
              onChange={(e) => setCondition(e.target.value as 'above' | 'below')}
            >
              <option value="above">突破 ▲</option>
              <option value="below">跌破 ▼</option>
            </select>
            <input
              type="number"
              className="alert-input"
              placeholder="目标价格"
              value={targetPrice}
              onChange={(e) => setTargetPrice(e.target.value)}
              onKeyPress={(e) => e.key === 'Enter' && addAlert()}
            />
            <button
              className="btn-add-alert"
              onClick={addAlert}
              disabled={!targetPrice}
            >
              添加
            </button>
          </div>
          <div style={{ fontSize: '12px', color: '#94a3b8' }}>
            当前价格: ${currentPrice.toFixed(2)}
          </div>
        </div>
      </div>

      <div className="alert-list">
        {alerts.length > 0 ? (
          alerts.map(alert => (
            <div
              key={alert.id}
              className={`alert-item ${alert.condition} ${alert.isTriggered ? 'triggered' : ''}`}
            >
              <div className="alert-item-header">
                <div className="alert-condition">
                  {alert.condition === 'above' ? '突破 ▲' : '跌破 ▼'}
                </div>
                <div className="alert-actions">
                  {alert.isTriggered && (
                    <button
                      className="btn-icon"
                      onClick={() => resetAlert(alert.id)}
                      title="重置预警"
                    >
                      🔄
                    </button>
                  )}
                  <button
                    className="btn-icon btn-delete"
                    onClick={() => deleteAlert(alert.id)}
                    title="删除预警"
                  >
                    🗑️
                  </button>
                </div>
              </div>

              <div className="alert-target">
                ${alert.targetPrice.toFixed(2)}
              </div>

              <div className="alert-info">
                <div className="alert-status">
                  <span className="alert-status-dot"></span>
                  <span>
                    {alert.isTriggered
                      ? `已触发 (${alert.currentPrice?.toFixed(2)})`
                      : '等待中'}
                  </span>
                </div>
                <div className="alert-time">
                  {alert.isTriggered && alert.triggeredAt
                    ? formatTime(alert.triggeredAt)
                    : formatTime(alert.createdAt)}
                </div>
              </div>
            </div>
          ))
        ) : (
          <div className="no-alerts">
            <p>暂无价格预警</p>
            <p style={{ fontSize: '12px' }}>设置预警，价格触发时立即通知</p>
          </div>
        )}
      </div>
    </div>
  )
}

// 预警通知组件
interface AlertNotificationProps {
  alert: PriceAlert
  onDismiss: () => void
  onView: () => void
}

export function AlertNotification({ alert, onDismiss, onView }: AlertNotificationProps) {
  return (
    <div className="alert-notification">
      <div className="alert-notification-header">
        <div className="alert-notification-title">
          <span className="alert-notification-icon">🚨</span>
          <span>价格预警触发</span>
        </div>
        <button className="btn-close-notification" onClick={onDismiss}>
          ×
        </button>
      </div>

      <div className="alert-notification-content">
        <div>{alert.message}</div>
        <div className="alert-notification-detail">
          当前价格: ${alert.currentPrice?.toFixed(2)}
        </div>
      </div>

      <div className="alert-notification-footer">
        <button className="btn-notification btn-dismiss" onClick={onDismiss}>
          知道了
        </button>
        <button className="btn-notification btn-view" onClick={onView}>
          查看详情
        </button>
      </div>
    </div>
  )
}
