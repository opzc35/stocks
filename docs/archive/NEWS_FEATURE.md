# 新闻展示功能说明

## 概述

为股票交易系统添加了全新的新闻展示功能，帮助交易者更好地理解市场动态和价格波动背后的原因。

## 功能亮点

### 1. 📰 新闻面板（右侧）

新闻面板显示在主界面右侧，提供以下功能：

- **实时新闻列表**：显示加密货币市场的最新新闻
- **情绪分类**：每条新闻都标记为利好📈、利空📉或中性📰
- **智能筛选**：一键筛选特定情绪类型的新闻
- **详细信息**：包含标题、内容摘要、来源、时间和标签
- **交互式高亮**：点击新闻项，图表上对应的标记点会高亮显示

### 2. 📍 图表新闻标记

价格图表上直接显示新闻事件标记：

- **彩色圆点**：
  - 🟢 绿色 = 利好消息
  - 🔴 红色 = 利空消息
  - ⚪ 灰色 = 中性消息
- **准确定位**：新闻标记自动对齐到最接近的价格数据点
- **可点击**：点击标记可以查看对应的新闻详情
- **高亮状态**：选中的新闻标记会放大并添加光晕效果

### 3. 🔄 双向联动

新闻面板和图表之间实现了完美的交互联动：

- 点击新闻 → 图表标记高亮
- 点击图表标记 → 新闻面板滚动到对应新闻

## 技术实现

### 新增组件

1. **NewsPanel.tsx** - 新闻面板组件
   - 新闻列表展示
   - 情绪筛选功能
   - 新闻项交互

2. **NewsPanel.css** - 新闻面板样式
   - 响应式布局
   - 悬停效果
   - 滚动条美化

### 组件升级

1. **PriceChart.tsx** - 价格图表组件
   - 添加新闻标记点渲染
   - 实现 ReferenceDot 自定义形状
   - 新闻点击交互

2. **App.tsx** - 主应用组件
   - 新闻数据管理
   - 选中状态同步
   - 布局调整为双栏结构

3. **App.css** - 应用样式
   - 新的 dashboard-layout 布局
   - 响应式新闻列支持
   - 移动端适配

## 数据结构

```typescript
interface NewsItem {
  id: string              // 唯一标识
  timestamp: number       // 新闻时间戳
  title: string          // 新闻标题
  content: string        // 新闻内容
  sentiment: 'positive' | 'negative' | 'neutral'  // 情绪分类
  source: string         // 新闻来源
  tags: string[]         // 相关标签
}
```

## 接入真实新闻 API

目前使用的是模拟数据，要接入真实新闻 API，请修改 `App.tsx` 中的 `fetchNews` 函数：

```typescript
const fetchNews = async () => {
  try {
    // 替换为你的新闻 API
    const response = await fetch('YOUR_NEWS_API_ENDPOINT')
    const data = await response.json()
    
    // 将 API 数据转换为 NewsItem 格式
    const newsItems: NewsItem[] = data.map(item => ({
      id: item.id,
      timestamp: item.timestamp,
      title: item.title,
      content: item.content,
      sentiment: item.sentiment,
      source: item.source,
      tags: item.tags
    }))
    
    setNews(newsItems)
  } catch (error) {
    console.error('Error fetching news:', error)
  }
}
```

### 推荐的新闻 API

- **CryptoCompare News API** - https://min-api.cryptocompare.com/
- **CoinGecko API** - https://www.coingecko.com/api/documentation
- **NewsAPI** - https://newsapi.org/
- **CryptoPanic** - https://cryptopanic.com/developers/api/

## 响应式设计

新闻功能完全支持响应式布局：

- **桌面端（>1200px）**：新闻面板固定在右侧，宽度 400px
- **平板端（768px-1200px）**：新闻面板移到底部，全宽显示
- **移动端（<768px）**：垂直堆叠布局，高度自适应

## 未来优化方向

1. **实时新闻推送**：使用 WebSocket 实现新闻实时推送
2. **AI 情绪分析**：使用 Claude API 自动分析新闻情绪
3. **新闻搜索**：添加关键词搜索功能
4. **新闻详情页**：点击新闻显示完整内容和相关链接
5. **新闻提醒**：重要新闻桌面通知
6. **多语言支持**：自动翻译新闻内容
7. **新闻影响力评分**：根据新闻重要性添加权重

## 使用示例

### 查看所有新闻
打开应用后，右侧新闻面板会自动显示最新新闻。

### 筛选利好消息
点击新闻面板顶部的"📈 利好"按钮，只显示利好新闻。

### 查看新闻对价格的影响
点击任一新闻项，左侧图表上对应时间点的标记会高亮，可以直观看到新闻发布时的价格变化。

### 从图表找新闻
在价格图表上看到异常波动时，查看附近的新闻标记点，点击可以了解导致波动的新闻事件。

## 开发与构建

```bash
# 开发模式
npm run dev

# 构建生产版本
npm run build

# 构建 Tauri 桌面应用
npm run tauri:build
```

## 贡献

欢迎提交 Issue 和 Pull Request 来改进新闻展示功能！
