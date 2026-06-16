import { useState } from 'react'
import './AIAssistant.css'

interface Message {
  id: string
  role: 'user' | 'assistant' | 'system'
  content: string
  timestamp: number
  actions?: AIAction[]
}

interface AIAction {
  type: 'create_strategy' | 'run_backtest' | 'set_alert' | 'analyze_market' | 'optimize_strategy'
  data: any
  status: 'pending' | 'executing' | 'completed' | 'failed'
  result?: any
}

interface AIAssistantProps {
  symbol: string
  currentPrice: number
  onExecuteAction?: (action: AIAction) => Promise<any>
}

export function AIAssistant({ symbol, currentPrice, onExecuteAction }: AIAssistantProps) {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: '1',
      role: 'system',
      content: '你好！我是 AI 交易助手，可以帮你：\n\n📈 创建交易策略\n🎯 运行策略回测\n🔔 设置价格预警\n📊 分析市场行情\n⚙️ 优化策略参数\n\n请告诉我你需要什么帮助？',
      timestamp: Date.now()
    }
  ])
  const [input, setInput] = useState('')
  const [isProcessing, setIsProcessing] = useState(false)

  // 处理用户输入
  const handleSend = async () => {
    if (!input.trim() || isProcessing) return

    const userMessage: Message = {
      id: Date.now().toString(),
      role: 'user',
      content: input,
      timestamp: Date.now()
    }

    setMessages(prev => [...prev, userMessage])
    setInput('')
    setIsProcessing(true)

    try {
      // 调用 AI API
      const response = await callAI(input, symbol, currentPrice)

      const assistantMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: response.message,
        timestamp: Date.now(),
        actions: response.actions
      }

      setMessages(prev => [...prev, assistantMessage])

      // 自动执行动作（如果有）
      if (response.actions && response.actions.length > 0) {
        for (const action of response.actions) {
          await executeAction(action, assistantMessage.id)
        }
      }
    } catch (error) {
      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: '抱歉，处理请求时出错了。请稍后重试。',
        timestamp: Date.now()
      }
      setMessages(prev => [...prev, errorMessage])
    } finally {
      setIsProcessing(false)
    }
  }

  // 执行 AI 动作
  const executeAction = async (action: AIAction, messageId: string) => {
    // 更新动作状态为执行中
    setMessages(prev => prev.map(msg => {
      if (msg.id === messageId && msg.actions) {
        return {
          ...msg,
          actions: msg.actions.map(a =>
            a === action ? { ...a, status: 'executing' } : a
          )
        }
      }
      return msg
    }))

    try {
      const result = await onExecuteAction?.(action)

      // 更新动作状态为完成
      setMessages(prev => prev.map(msg => {
        if (msg.id === messageId && msg.actions) {
          return {
            ...msg,
            actions: msg.actions.map(a =>
              a === action ? { ...a, status: 'completed', result } : a
            )
          }
        }
        return msg
      }))
    } catch (error) {
      // 更新动作状态为失败
      setMessages(prev => prev.map(msg => {
        if (msg.id === messageId && msg.actions) {
          return {
            ...msg,
            actions: msg.actions.map(a =>
              a === action ? { ...a, status: 'failed' } : a
            )
          }
        }
        return msg
      }))
    }
  }

  // 调用 AI API（示例实现）
  const callAI = async (prompt: string, symbol: string, price: number): Promise<{ message: string, actions?: AIAction[] }> => {
    // 这里应该调用真实的 AI API，目前使用模拟响应
    await new Promise(resolve => setTimeout(resolve, 1000))

    // 解析用户意图
    const lowerPrompt = prompt.toLowerCase()

    if (lowerPrompt.includes('策略') || lowerPrompt.includes('strategy')) {
      return {
        message: `好的，我帮你创建一个基于移动平均线的交易策略。

**策略名称**: MA Cross Strategy
**交易对**: ${symbol}
**参数**:
- 短期均线: 20
- 长期均线: 50
- 初始资金: $10,000

**规则**:
- 买入: 短期均线上穿长期均线
- 卖出: 短期均线下穿长期均线

策略已创建，是否要运行回测？`,
        actions: [{
          type: 'create_strategy',
          data: {
            name: 'MA Cross Strategy',
            symbol,
            params: { short: 20, long: 50, capital: 10000 }
          },
          status: 'pending'
        }]
      }
    }

    if (lowerPrompt.includes('回测') || lowerPrompt.includes('backtest')) {
      return {
        message: `正在运行回测...

**回测结果**:
- 总收益: +15.6%
- 夏普比率: 1.32
- 最大回撤: -8.4%
- 胜率: 58%
- 总交易: 24笔

策略表现不错！建议在实盘前进一步优化参数。`,
        actions: [{
          type: 'run_backtest',
          data: {
            strategy: 'MA Cross Strategy',
            symbol,
            timeframe: '1h',
            days: 30
          },
          status: 'pending'
        }]
      }
    }

    if (lowerPrompt.includes('预警') || lowerPrompt.includes('alert') || lowerPrompt.includes('提醒')) {
      const targetPrice = price * 1.05 // 示例：当前价格的 105%
      return {
        message: `好的，我帮你设置价格预警。

**预警配置**:
- 交易对: ${symbol}
- 当前价格: $${price.toFixed(2)}
- 目标价格: $${targetPrice.toFixed(2)}
- 条件: 突破

价格达到目标时会通知你！`,
        actions: [{
          type: 'set_alert',
          data: {
            symbol,
            condition: 'above',
            targetPrice
          },
          status: 'pending'
        }]
      }
    }

    if (lowerPrompt.includes('分析') || lowerPrompt.includes('analyze') || lowerPrompt.includes('市场')) {
      return {
        message: `让我分析一下 ${symbol} 的市场情况...

**技术分析**:
- 当前价格: $${price.toFixed(2)}
- 趋势: 上涨 📈
- RSI: 62 (中性偏多)
- MACD: 正向 ✓

**建议**:
1. 短期可能继续上涨
2. 注意 $${(price * 1.1).toFixed(2)} 附近的阻力位
3. 可以考虑在回调到 $${(price * 0.95).toFixed(2)} 时加仓

**风险提示**: 建议设置止损在 $${(price * 0.92).toFixed(2)}`,
        actions: [{
          type: 'analyze_market',
          data: { symbol, price },
          status: 'pending'
        }]
      }
    }

    if (lowerPrompt.includes('优化') || lowerPrompt.includes('optimize')) {
      return {
        message: `正在优化策略参数...

**优化结果**:
- 最佳短期均线: 18
- 最佳长期均线: 52
- 预期收益提升: +3.2%
- 风险降低: -1.8%

**建议**: 使用优化后的参数可以提高策略表现。是否应用这些参数？`,
        actions: [{
          type: 'optimize_strategy',
          data: {
            strategy: 'MA Cross Strategy',
            optimizedParams: { short: 18, long: 52 }
          },
          status: 'pending'
        }]
      }
    }

    // 默认响应
    return {
      message: `我理解了你的问题。我可以帮你：

📈 **创建策略** - 说"帮我创建一个策略"
🎯 **运行回测** - 说"运行回测"
🔔 **设置预警** - 说"设置价格预警"
📊 **分析市场** - 说"分析市场"
⚙️ **优化策略** - 说"优化策略参数"

请告诉我你想做什么？`
    }
  }

  return (
    <div className="ai-assistant">
      <div className="ai-header">
        <div className="ai-title">
          <span className="ai-icon">🤖</span>
          <span>AI 交易助手</span>
        </div>
        <div className="ai-status">
          <span className={`status-dot ${isProcessing ? 'processing' : 'online'}`}></span>
          <span>{isProcessing ? '思考中...' : '在线'}</span>
        </div>
      </div>

      <div className="ai-messages">
        {messages.map(msg => (
          <MessageBubble key={msg.id} message={msg} />
        ))}
      </div>

      <div className="ai-input-container">
        <input
          type="text"
          className="ai-input"
          placeholder="输入你的问题..."
          value={input}
          onChange={e => setInput(e.target.value)}
          onKeyPress={e => e.key === 'Enter' && handleSend()}
          disabled={isProcessing}
        />
        <button
          className="ai-send-btn"
          onClick={handleSend}
          disabled={isProcessing || !input.trim()}
        >
          {isProcessing ? '⏳' : '📤'}
        </button>
      </div>
    </div>
  )
}

// 消息气泡组件
function MessageBubble({ message }: { message: Message }) {
  return (
    <div className={`message-bubble ${message.role}`}>
      <div className="message-content">
        {message.content.split('\n').map((line, i) => (
          <div key={i}>{line}</div>
        ))}
      </div>

      {message.actions && message.actions.length > 0 && (
        <div className="message-actions">
          {message.actions.map((action, i) => (
            <ActionCard key={i} action={action} />
          ))}
        </div>
      )}

      <div className="message-time">
        {new Date(message.timestamp).toLocaleTimeString('zh-CN', {
          hour: '2-digit',
          minute: '2-digit'
        })}
      </div>
    </div>
  )
}

// 动作卡片组件
function ActionCard({ action }: { action: AIAction }) {
  const getActionIcon = () => {
    switch (action.type) {
      case 'create_strategy': return '📝'
      case 'run_backtest': return '🎯'
      case 'set_alert': return '🔔'
      case 'analyze_market': return '📊'
      case 'optimize_strategy': return '⚙️'
      default: return '🔧'
    }
  }

  const getActionName = () => {
    switch (action.type) {
      case 'create_strategy': return '创建策略'
      case 'run_backtest': return '运行回测'
      case 'set_alert': return '设置预警'
      case 'analyze_market': return '市场分析'
      case 'optimize_strategy': return '优化策略'
      default: return '执行动作'
    }
  }

  const getStatusIcon = () => {
    switch (action.status) {
      case 'pending': return '⏳'
      case 'executing': return '🔄'
      case 'completed': return '✅'
      case 'failed': return '❌'
    }
  }

  return (
    <div className={`action-card ${action.status}`}>
      <div className="action-header">
        <span className="action-icon">{getActionIcon()}</span>
        <span className="action-name">{getActionName()}</span>
        <span className="action-status">{getStatusIcon()}</span>
      </div>
    </div>
  )
}
