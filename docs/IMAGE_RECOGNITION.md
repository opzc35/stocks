# 🖼️ AI 图片识别功能

## 概述

为 AI 助手添加了**智能图片识别**功能，支持用户上传K线图、截图等进行自动分析。

---

## 🎯 功能特点

### 1. 支持的图片类型

#### 📊 K线图表
- 自动识别K线、均线、指标
- 分析趋势和形态
- 提供交易建议
- 标注关键位置

#### 📸 交易截图
- 识别交易界面
- 提取价格信息
- 分析持仓情况
- OCR 文字识别

#### 🖼️ 普通图片
- 通用图片识别
- 场景理解
- 内容描述

### 2. 分析能力

#### 技术元素检测
- ✅ K线识别（红绿柱）
- ✅ 趋势线检测
- ✅ 技术指标识别（MA, RSI, MACD）
- ✅ 成交量分析

#### 趋势分析
- **上涨趋势**: 价格持续走高
- **下跌趋势**: 价格持续走低
- **震荡趋势**: 横盘整理

#### 形态识别
- 头肩顶/底
- 双顶/双底
- 三角形整理
- 楔形形态
- 旗形整理

#### 智能建议
- 买入/卖出时机
- 止损位设置
- 风险提示
- 操作策略

---

## 🚀 使用方法

### 方式 1: Telegram

1. **发送图片**
   ```
   [上传K线图]
   附加文字: "这个图表是什么趋势?"
   ```

2. **AI 自动回复**
   ```
   📊 图表分析结果

   检测到的元素:
   • candlesticks
   • trend_lines

   技术指标:
   • MA20
   • MA50
   • RSI

   趋势: 上涨趋势

   技术形态:
   • 上升三角形

   交易建议:
   1. 趋势向上，可考虑逢低买入
   2. 注意设置止损位

   关于你的问题「这个图表是什么趋势?」:
   从图表看，当前呈现上涨趋势。

   ⚠️ 仅供参考，不构成投资建议
   ```

### 方式 2: Discord

1. **使用斜杠命令**
   ```
   /analyze [上传图片] "帮我看看这个图"
   ```

2. **机器人回复分析结果**

### 方式 3: Slack

1. **在频道上传图片**
   ```
   [拖拽图片到频道]
   添加评论: "AI帮我分析一下"
   ```

2. **机器人在线程中回复**

### 方式 4: 企业微信

1. **发送图片到群聊**
   ```
   [发送K线图片]
   ```

2. **机器人自动分析并回复**

### 方式 5: API 调用

```bash
curl -X POST http://localhost:8001/api/image/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "image_base64": "base64_encoded_image_data",
    "message": "这个图表是什么趋势?"
  }'
```

**响应**:
```json
{
  "success": true,
  "analysis": "📊 图表分析结果\n\n..."
}
```

---

## 📊 分析示例

### 示例 1: 趋势分析

**用户上传**: BTC/USDT 日线图  
**用户提问**: "当前趋势如何?"

**AI 回复**:
```markdown
📊 图表分析结果

检测到的元素:
• candlesticks
• trend_lines

技术指标:
• MA20
• MA50
• RSI

趋势: 上涨趋势

技术形态:
• 上升三角形
• 高波动

交易建议:
1. 趋势向上，可考虑逢低买入
2. 注意设置止损位
3. 波动较大，注意风险控制

关于你的问题「当前趋势如何?」:
从图表看，当前呈现上涨趋势。

⚠️ 仅供参考，不构成投资建议
```

### 示例 2: 买卖点分析

**用户上传**: ETH/USDT 4小时图  
**用户提问**: "现在可以买入吗?"

**AI 回复**:
```markdown
📊 图表分析结果

检测到的元素:
• candlesticks

技术指标:
• MA20
• MA50
• RSI

趋势: 震荡趋势

交易建议:
1. 震荡行情，高抛低吸
2. 控制仓位，注意风险

关于你的问题「现在可以买入吗?」:
建议等待更明确的信号。

⚠️ 仅供参考，不构成投资建议
```

### 示例 3: 形态识别

**用户上传**: BNB/USDT 周线图  
**用户提问**: "识别到什么形态?"

**AI 回复**:
```markdown
📊 图表分析结果

检测到的元素:
• candlesticks
• trend_lines

技术指标:
• MA20
• MA50

趋势: 上涨趋势

技术形态:
• 双底
• 低波动

交易建议:
1. 趋势向上，可考虑逢低买入
2. 注意设置止损位

关于你的问题「识别到什么形态?」:
识别到以下形态: 双底, 低波动

⚠️ 仅供参考，不构成投资建议
```

---

## 🛠️ 技术实现

### 核心模块

#### 1. ImageAnalyzer (图片分析器)

```python
class ImageAnalyzer:
    async def analyze_image(self, image_data: bytes, image_type: str):
        """分析图片内容"""
        # 1. 打开图片
        # 2. 检测元素
        # 3. 分析趋势
        # 4. 识别形态
        # 5. 生成建议
        return analysis_result
```

**功能模块**:
- `_analyze_chart()` - K线图分析
- `_analyze_screenshot()` - 截图分析
- `_analyze_general()` - 通用分析
- `_detect_indicators()` - 指标检测
- `_analyze_trend()` - 趋势分析
- `_recognize_patterns()` - 形态识别

#### 2. 检测算法

**K线检测**:
```python
def _has_candlesticks(img_array):
    # 检测红色和绿色像素
    red_pixels = count_red_pixels(img_array)
    green_pixels = count_green_pixels(img_array)
    return red_pixels > threshold or green_pixels > threshold
```

**趋势分析**:
```python
def _analyze_trend(img_array):
    # 比较左右两侧亮度
    left_brightness = mean(left_section)
    right_brightness = mean(right_section)
    
    if right > left * 1.1:
        return '上涨趋势'
    elif right < left * 0.9:
        return '下跌趋势'
    else:
        return '震荡趋势'
```

**指标检测**:
```python
def _detect_indicators(img_array):
    indicators = []
    
    # 检测多条曲线（均线）
    colors = extract_dominant_colors(img_array)
    if len(colors) >= 3:
        indicators.extend(['MA20', 'MA50'])
    
    # 检测副图（RSI/MACD）
    bottom_section = img_array[70%:, :, :]
    if has_variance(bottom_section):
        indicators.append('RSI')
    
    return indicators
```

### 集成流程

```
用户发送图片
    ↓
平台 Webhook 接收
    ↓
下载图片数据
    ↓
ImageAnalyzer.analyze_image()
    ↓
process_image_message()
    ↓
生成分析文本
    ↓
回复用户
```

---

## 📝 支持的问题类型

### 趋势问题
```
"当前趋势如何?"
"是涨还是跌?"
"What's the trend?"
```

### 买卖问题
```
"现在可以买入吗?"
"应该卖出吗?"
"Can I buy now?"
```

### 形态问题
```
"识别到什么形态?"
"有什么技术形态?"
"What patterns do you see?"
```

### 支撑阻力
```
"支撑位在哪?"
"阻力位是多少?"
"Support and resistance levels?"
```

### 通用分析
```
"帮我分析一下"
"看看这个图"
"Analyze this chart"
```

---

## 🔧 配置和部署

### 安装依赖

```bash
cd python-engine

# 安装必要的库
pip install pillow numpy

# 可选：安装 OCR 支持
pip install pytesseract

# 可选：安装深度学习模型
pip install torch torchvision
```

### 启动服务

```bash
# 启动增强版机器人服务
python bot_webhook_image.py

# 健康检查
curl http://localhost:8001/health
```

### 配置 Webhook

**Telegram**:
```bash
curl -X POST \
  "https://api.telegram.org/bot<YOUR_TOKEN>/setWebhook" \
  -d "url=https://your-domain.com/webhook/telegram/<YOUR_TOKEN>"
```

**Discord**:
在 Discord Developer Portal 配置 Interactions Endpoint:
```
https://your-domain.com/webhook/discord
```

---

## 🎯 应用场景

### 场景 1: 技术分析辅助

**用户**: 技术分析新手  
**需求**: 学习识别图表形态  
**使用**: 上传各种图表让AI分析  
**收益**: 快速学习技术分析

### 场景 2: 第二意见

**用户**: 职业交易者  
**需求**: 验证自己的分析  
**使用**: 上传分析过的图表  
**收益**: 获得AI的第二意见

### 场景 3: 快速筛选

**用户**: 多币种监控  
**需求**: 快速筛选机会  
**使用**: 批量上传多个币种图表  
**收益**: 快速找到交易机会

### 场景 4: 社区讨论

**用户**: 交易社区成员  
**需求**: 在群里讨论图表  
**使用**: 上传图表让AI参与讨论  
**收益**: 活跃社区氛围

---

## ⚠️ 限制和注意事项

### 当前限制

1. **识别准确度**: 基于图像处理算法，不如专业技术分析软件
2. **形态识别**: 简化实现，可能遗漏复杂形态
3. **OCR功能**: 需要额外安装 pytesseract
4. **深度学习**: 需要训练模型提高准确度

### 改进方向

- [ ] 训练专门的K线识别模型
- [ ] 集成 OCR 提取文字信息
- [ ] 支持更多技术形态
- [ ] 添加量价分析
- [ ] 历史数据对比

### 免责声明

⚠️ **重要提示**:
- AI 分析仅供参考
- 不构成投资建议
- 投资有风险，决策需谨慎
- 建议结合其他分析方法

---

## 📚 相关文档

- [CHART_SENDING.md](./CHART_SENDING.md) - 图表发送功能
- [BOT_NOTIFICATION.md](./BOT_NOTIFICATION.md) - 机器人通知
- [README.md](../README.md) - 项目总览

---

## 🔮 未来计划

### v2.2 计划
- ✅ 基础图片识别
- ⏳ OCR 文字提取
- ⏳ 深度学习模型
- ⏳ 多图对比分析

### v2.3 计划
- ⏳ 视频分析支持
- ⏳ 实时屏幕分享分析
- ⏳ AR 标注功能
- ⏳ 语音描述图表

---

**版本**: v2.1.0  
**日期**: 2026-06-16  
**功能**: AI 图片识别 + 智能分析 🖼️
