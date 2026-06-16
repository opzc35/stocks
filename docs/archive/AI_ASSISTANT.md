# AI 交易助手功能说明

## 概述

AI 交易助手是一个智能对话界面，通过自然语言与你交互，帮助你完成各种交易相关任务，包括创建策略、运行回测、设置预警、分析市场等。

## 功能特性

### 1. 🤖 自然语言交互

使用日常语言与 AI 对话：
- "帮我创建一个交易策略"
- "运行回测看看效果"
- "设置一个价格预警"
- "分析一下当前市场"
- "优化策略参数"

### 2. 📈 支持的操作

#### 创建策略 (create_strategy)
- 基于移动平均线策略
- 基于 RSI 策略
- 自定义参数配置
- 策略模板选择

#### 运行回测 (run_backtest)
- 指定时间范围
- 选择交易对
- 设置初始资金
- 查看回测结果

#### 设置预警 (set_alert)
- 价格突破预警
- 价格跌破预警
- 自动推荐目标价格
- 集成到预警系统

#### 市场分析 (analyze_market)
- 技术指标分析
- 趋势判断
- 支撑阻力位识别
- 交易建议

#### 优化策略 (optimize_strategy)
- 参数网格搜索
- 收益最大化
- 风险最小化
- 夏普比率优化

### 3. 🎯 智能动作执行

AI 不仅回答问题，还能直接执行操作：

```
用户: "帮我设置一个价格预警"
  ↓
AI 分析意图
  ↓
生成预警配置
  ↓
自动执行设置
  ↓
返回执行结果
```

### 4. 📊 可视化反馈

- **动作卡片**：显示 AI 正在执行的操作
- **状态指示**：实时显示执行状态
  - ⏳ 待执行
  - 🔄 执行中
  - ✅ 已完成
  - ❌ 失败
- **结果展示**：执行完成后显示结果

## 使用指南

### 打开 AI 助手

1. 点击顶部导航栏的 **"🧠 AI助手"** 按钮
2. AI 助手对话窗口会弹出
3. 开始与 AI 对话

### 对话示例

#### 示例 1：创建交易策略

**用户输入：**
```
帮我创建一个基于移动平均线的交易策略
```

**AI 响应：**
```
好的，我帮你创建一个基于移动平均线的交易策略。

策略名称: MA Cross Strategy
交易对: BTC/USDT
参数:
- 短期均线: 20
- 长期均线: 50
- 初始资金: $10,000

规则:
- 买入: 短期均线上穿长期均线
- 卖出: 短期均线下穿长期均线

策略已创建，是否要运行回测？
```

**动作卡片：**
```
📝 创建策略 ✅
```

---

#### 示例 2：运行回测

**用户输入：**
```
运行回测
```

**AI 响应：**
```
正在运行回测...

回测结果:
- 总收益: +15.6%
- 夏普比率: 1.32
- 最大回撤: -8.4%
- 胜率: 58%
- 总交易: 24笔

策略表现不错！建议在实盘前进一步优化参数。
```

**动作卡片：**
```
🎯 运行回测 ✅
```

---

#### 示例 3：设置价格预警

**用户输入：**
```
价格涨到70000时提醒我
```

**AI 响应：**
```
好的，我帮你设置价格预警。

预警配置:
- 交易对: BTC/USDT
- 当前价格: $67,532.45
- 目标价格: $70,000.00
- 条件: 突破

价格达到目标时会通知你！
```

**动作卡片：**
```
🔔 设置预警 ✅
```

---

#### 示例 4：市场分析

**用户输入：**
```
分析一下现在的市场
```

**AI 响应：**
```
让我分析一下 BTC/USDT 的市场情况...

技术分析:
- 当前价格: $67,532.45
- 趋势: 上涨 📈
- RSI: 62 (中性偏多)
- MACD: 正向 ✓

建议:
1. 短期可能继续上涨
2. 注意 $74,285.70 附近的阻力位
3. 可以考虑在回调到 $64,155.83 时加仓

风险提示: 建议设置止损在 $62,129.85
```

**动作卡片：**
```
📊 市场分析 ✅
```

---

#### 示例 5：优化策略

**用户输入：**
```
优化一下策略参数
```

**AI 响应：**
```
正在优化策略参数...

优化结果:
- 最佳短期均线: 18
- 最佳长期均线: 52
- 预期收益提升: +3.2%
- 风险降低: -1.8%

建议: 使用优化后的参数可以提高策略表现。是否应用这些参数？
```

**动作卡片：**
```
⚙️ 优化策略 ✅
```

## MCP 集成

AI 助手通过 Model Context Protocol (MCP) 与系统功能深度集成：

### 支持的 MCP 工具

1. **create_strategy**
   - 创建新的交易策略
   - 配置策略参数
   - 保存策略模板

2. **run_backtest**
   - 执行策略回测
   - 调用后端 API
   - 返回回测结果

3. **set_alert**
   - 创建价格预警
   - 集成预警系统
   - 配置通知渠道

4. **analyze_market**
   - 技术指标分析
   - 趋势识别
   - 生成交易建议

5. **optimize_strategy**
   - 参数优化
   - 网格搜索
   - 性能评估

### MCP 工作流程

```
用户输入
    ↓
AI 解析意图
    ↓
选择合适的 MCP 工具
    ↓
生成工具调用参数
    ↓
执行 MCP 工具
    ↓
返回执行结果
    ↓
格式化响应
    ↓
展示给用户
```

## 高级功能

### 1. 上下文记忆

AI 会记住对话上下文：

```
用户: 帮我创建一个策略
AI: 好的，策略已创建...

用户: 运行回测
AI: (理解是对刚创建的策略进行回测)
```

### 2. 多步骤任务

AI 可以执行多步骤的复杂任务：

```
用户: 创建一个策略并运行回测
  ↓
AI: 
1. 创建策略
2. 运行回测
3. 展示结果
```

### 3. 智能推荐

AI 会根据当前市场情况给出建议：

- 推荐合适的策略参数
- 建议最佳的入场/出场点
- 提供风险管理建议

### 4. 错误处理

当操作失败时，AI 会：
- 解释失败原因
- 提供解决方案
- 建议替代方案

## 最佳实践

### 1. 清晰表达意图

**好的示例：**
- "帮我创建一个基于 RSI 的策略"
- "运行最近 30 天的回测"
- "当价格突破 70000 时提醒我"

**不好的示例：**
- "做点什么"
- "看看"
- "那个"

### 2. 提供必要信息

当 AI 需要更多信息时，主动提供：

```
AI: 您想设置什么价格的预警？
用户: 70000
```

### 3. 确认关键操作

对于重要操作，AI 会要求确认：

```
AI: 是否确认删除策略？
用户: 确认
```

### 4. 利用上下文

利用对话上下文，简化输入：

```
用户: 创建策略
AI: 策略已创建...

用户: 优化参数 (AI 理解是优化刚创建的策略)
```

## 技术实现

### 前端组件

```typescript
<AIAssistant
  symbol={symbol}
  currentPrice={currentPrice}
  onExecuteAction={handleAIAction}
/>
```

### 动作处理

```typescript
const handleAIAction = async (action: AIAction) => {
  switch (action.type) {
    case 'create_strategy':
      return await createStrategy(action.data)
    case 'run_backtest':
      return await runBacktest(action.data)
    case 'set_alert':
      return await setAlert(action.data)
    case 'analyze_market':
      return await analyzeMarket(action.data)
    case 'optimize_strategy':
      return await optimizeStrategy(action.data)
  }
}
```

### AI API 集成

```typescript
const callAI = async (prompt: string, context: any) => {
  const response = await fetch('/api/ai/chat', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      prompt,
      context,
      tools: ['create_strategy', 'run_backtest', 'set_alert', ...]
    })
  })
  return response.json()
}
```

## 接入真实 AI API

### 使用 Claude API

```typescript
const callAI = async (prompt: string, symbol: string, price: number) => {
  const response = await fetch('https://api.anthropic.com/v1/messages', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'x-api-key': 'your-api-key',
      'anthropic-version': '2023-06-01'
    },
    body: JSON.stringify({
      model: 'claude-3-opus-20240229',
      max_tokens: 1024,
      messages: [{
        role: 'user',
        content: `你是一个专业的交易助手。当前交易对: ${symbol}, 当前价格: $${price}。用户请求: ${prompt}`
      }],
      tools: [
        {
          name: 'create_strategy',
          description: '创建交易策略',
          input_schema: {
            type: 'object',
            properties: {
              name: { type: 'string' },
              params: { type: 'object' }
            }
          }
        },
        // 其他工具定义...
      ]
    })
  })
  
  return response.json()
}
```

### 使用 OpenAI API

```typescript
const callAI = async (prompt: string, symbol: string, price: number) => {
  const response = await fetch('https://api.openai.com/v1/chat/completions', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer your-api-key`
    },
    body: JSON.stringify({
      model: 'gpt-4',
      messages: [{
        role: 'system',
        content: '你是一个专业的交易助手...'
      }, {
        role: 'user',
        content: prompt
      }],
      functions: [
        {
          name: 'create_strategy',
          description: '创建交易策略',
          parameters: {
            type: 'object',
            properties: {
              name: { type: 'string' },
              params: { type: 'object' }
            }
          }
        },
        // 其他函数定义...
      ]
    })
  })
  
  return response.json()
}
```

## 未来增强

### 短期
1. **语音输入** - 支持语音对话
2. **快捷命令** - 预设常用命令
3. **历史记录** - 保存对话历史
4. **导出对话** - 导出为文本/PDF

### 中期
1. **多语言支持** - 支持英文、中文等
2. **个性化学习** - 学习用户习惯
3. **智能提示** - 自动补全建议
4. **批量操作** - 一次执行多个任务

### 长期
1. **自主交易** - AI 自动执行交易
2. **情绪分析** - 分析市场情绪
3. **新闻解读** - 自动解读新闻影响
4. **策略生成** - 完全自动化策略创建

## 安全注意事项

1. **API 密钥保护** - 不要在前端暴露 API 密钥
2. **权限控制** - 限制 AI 可执行的操作
3. **金额限制** - 设置交易金额上限
4. **人工确认** - 关键操作需要人工确认
5. **日志记录** - 记录所有 AI 操作

## 常见问题

### Q: AI 会自动执行交易吗？
**A:** 不会。AI 只会创建策略和预警，不会直接执行真实交易。

### Q: AI 的建议可靠吗？
**A:** AI 提供参考建议，但不构成投资建议。请自行判断和决策。

### Q: 可以自定义 AI 行为吗？
**A:** 可以通过修改系统提示词和工具定义来自定义 AI 行为。

### Q: 支持哪些语言？
**A:** 目前主要支持中文，未来将支持更多语言。

### Q: AI 会记住之前的对话吗？
**A:** 当前会话内会记住，刷新页面后会清空。未来将支持持久化。

---

**开始与 AI 助手对话，体验智能交易！** 🤖✨
