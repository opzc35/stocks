# 📐 画线工具 - TradingView 风格

## 概述

为图表添加了完整的**画线工具集**，类似 TradingView，支持 13 种绘图工具，让技术分析更专业。

---

## 🎯 支持的工具

### 1. 📏 直线 (Line)
**快捷键**: `L`

- 连接两点的直线
- 用于标记支撑/阻力位
- 可设置颜色和线宽

**使用场景**:
- 连接高点和低点
- 标记关键价格位

### 2. ➡️ 射线 (Ray)
**快捷键**: `R`

- 从起点向一个方向延伸的线
- 自动延长到图表边缘
- 适合趋势跟踪

**使用场景**:
- 趋势线延伸
- 动态支撑/阻力

### 3. → 箭头 (Arrow)
**快捷键**: `A`

- 带箭头的直线
- 明确指向方向
- 标注买卖点

**使用场景**:
- 标记入场/出场点
- 指示趋势方向

### 4. — 水平线 (Horizontal Line)
**快捷键**: `H`

- 横穿整个图表的水平线
- 自动显示价格标签
- 最常用的工具之一

**使用场景**:
- 标记关键价格位
- 止损/止盈位
- 心理价位

### 5. | 垂直线 (Vertical Line)
**快捷键**: `V`

- 纵穿整个图表的垂直线
- 标记重要时间点
- 事件标注

**使用场景**:
- 重大新闻发布时间
- 财报日期
- 政策公告

### 6. 📈 趋势线 (Trend Line)
**快捷键**: `T`

- 连接高点或低点
- 显示角度和涨跌幅
- 最重要的技术工具

**特点**:
- 自动计算角度
- 显示价格变化百分比
- 用于判断趋势强度

**使用场景**:
- 上升趋势线（连接低点）
- 下降趋势线（连接高点）
- 趋势突破判断

### 7. ⚌ 平行通道 (Parallel Channel)
**快捷键**: `C`

- 两条平行的趋势线
- 标记价格波动区间
- 可填充颜色

**绘制方法**:
1. 点击第一个点（下轨起点）
2. 点击第二个点（下轨终点）
3. 点击第三个点（确定通道宽度）

**使用场景**:
- 上升通道
- 下降通道
- 震荡区间

### 8. φ 斐波那契回调 (Fibonacci Retracement)
**快捷键**: `F`

- 自动绘制关键回调位
- 包含标准斐波那契比例
- 23.6%, 38.2%, 50%, 61.8%, 78.6%

**使用场景**:
- 寻找回调支撑位
- 确定目标位
- 波段交易

### 9. ▭ 矩形 (Rectangle)
**快捷键**: `S`

- 标记价格区间
- 可填充半透明颜色
- 整理形态标注

**使用场景**:
- 盘整区间
- 价格箱体
- 突破后的回踩区域

### 10. △ 三角形 (Triangle)
**快捷键**: `G`

- 标记三角形整理形态
- 三个点确定形态
- 可填充颜色

**使用场景**:
- 上升三角形
- 下降三角形
- 对称三角形

### 11. ○ 圆形 (Circle)
**快捷键**: `O`

- 标记圆形区域
- 突出重要价格区间
- 可填充颜色

**使用场景**:
- 突出关键K线
- 标记转折点
- 形态标注

### 12. T 文字标注 (Text)
**快捷键**: `X`

- 添加文字说明
- 自定义颜色和大小
- 详细注释

**使用场景**:
- 添加交易笔记
- 标记重要事件
- 策略说明

### 13. 📐 测量工具 (Measure)
**快捷键**: `M`

- 测量两点之间的距离
- 显示价格变化和百分比
- 虚线连接

**显示信息**:
- 价格变化值
- 变化百分比
- 像素距离

**使用场景**:
- 计算涨跌幅
- 测量波动幅度
- 确定目标位距离

---

## 🎨 设置选项

### 颜色选择

**预设颜色**:
- 🔵 蓝色 (#0070f3) - 默认
- 🟢 绿色 (#0ba360) - 上涨/支撑
- 🔴 红色 (#f857a6) - 下跌/阻力
- 🟡 黄色 (#f5a623) - 警告/重要
- 🟣 紫色 (#9b59b6) - 特殊标记
- ⚪ 白色 (#ffffff) - 清晰对比
- ⚫ 灰色 (#a1a1aa) - 次要标记

### 线宽调整

- **1px** - 细线（默认视图）
- **2px** - 标准（推荐）
- **3px** - 中等（重要线条）
- **4px** - 粗线（强调）
- **5px** - 最粗（特别强调）

### 线型样式

- **实线 (solid)** - 标准线条
- **虚线 (dashed)** - 预测或假设
- **点线 (dotted)** - 辅助线

---

## ⌨️ 键盘快捷键

### 工具选择
```
L - 直线
R - 射线
A - 箭头
H - 水平线
V - 垂直线
T - 趋势线
C - 平行通道
F - 斐波那契
S - 矩形
G - 三角形
O - 圆形
X - 文字
M - 测量

ESC - 取消选择
```

### 操作快捷键
```
Ctrl + Z - 撤销
Delete - 删除选中
Backspace - 删除最后一个
Ctrl + A - 全选
Ctrl + D - 复制
```

---

## 🖱️ 使用方法

### 基础操作

#### 1. 选择工具
```
点击工具栏中的图标
或
按下对应的快捷键
```

#### 2. 绘制图形
```
单击工具:
1. 点击起点
2. 移动鼠标
3. 点击终点

多点工具（如通道、三角形）:
1. 点击第一个点
2. 点击第二个点
3. 点击第三个点（如需要）
```

#### 3. 完成绘制
```
释放鼠标
或
按 Enter 键
```

### 高级技巧

#### 精确绘制
- 按住 `Shift` - 锁定角度（45°倍数）
- 按住 `Ctrl` - 从中心点绘制
- 按住 `Alt` - 复制模式

#### 编辑图形
1. 点击选择工具（箭头）
2. 点击要编辑的图形
3. 拖动控制点调整
4. 右键打开属性菜单

#### 多选操作
1. 按住 `Ctrl` 点击多个图形
2. 或拖动选择框
3. 批量修改颜色/样式

---

## 💡 实战案例

### 案例 1: 上升趋势线

**步骤**:
1. 按 `T` 选择趋势线
2. 点击第一个低点
3. 点击第二个低点
4. 系统自动显示角度和涨幅

**解读**:
- 角度 > 45° - 强势上涨
- 角度 30-45° - 标准上涨
- 角度 < 30° - 缓慢上涨

### 案例 2: 平行通道

**步骤**:
1. 按 `C` 选择通道工具
2. 连接两个低点（下轨）
3. 点击一个高点（确定通道宽度）
4. 通道自动绘制

**交易策略**:
- 通道下轨买入
- 通道上轨卖出
- 突破后顺势交易

### 案例 3: 斐波那契回调

**步骤**:
1. 按 `F` 选择斐波那契
2. 点击波段低点
3. 点击波段高点
4. 自动显示关键回调位

**关键位置**:
- **38.2%** - 浅回调（强势）
- **50%** - 中位回调
- **61.8%** - 深回调（黄金分割）
- **78.6%** - 极深回调

### 案例 4: 水平支撑阻力

**步骤**:
1. 按 `H` 选择水平线
2. 点击关键价格位
3. 自动延伸到整个图表

**识别方法**:
- 多次触及未破 - 强支撑/阻力
- 成交量大的价位
- 整数关口（如 70000）

### 案例 5: 三角形整理

**步骤**:
1. 按 `G` 选择三角形
2. 点击三个关键点
3. 标记整理形态

**突破方向**:
- 上升三角 - 看涨
- 下降三角 - 看跌
- 对称三角 - 方向不明

---

## 🎓 技术分析技巧

### 趋势判断

**上升趋势**:
- 连接低点绘制上升趋势线
- 价格在趋势线上方运行
- 跌破趋势线 → 趋势改变

**下降趋势**:
- 连接高点绘制下降趋势线
- 价格在趋势线下方运行
- 突破趋势线 → 可能反转

### 支撑阻力

**支撑位识别**:
- 前期低点
- 密集成交区
- 整数关口

**阻力位识别**:
- 前期高点
- 套牢盘区域
- 心理价位

### 形态分析

**整理形态**:
- 矩形整理
- 三角形整理
- 旗形整理

**反转形态**:
- 头肩顶/底
- 双顶/双底
- V型反转

---

## 🔧 技术实现

### 组件结构

```typescript
DrawingTools
├── Toolbar (工具栏)
│   ├── Tool Buttons (工具按钮)
│   └── Settings Button (设置)
├── Settings Panel (设置面板)
│   ├── Color Picker (颜色)
│   ├── Line Width (线宽)
│   └── Line Style (线型)
├── Canvas (绘图画布)
└── Drawings List (图形列表)
```

### 数据结构

```typescript
interface Drawing {
  id: string              // 唯一ID
  type: DrawingType       // 工具类型
  points: Point[]         // 坐标点
  color: string           // 颜色
  lineWidth: number       // 线宽
  style: LineStyle        // 线型
  filled?: boolean        // 是否填充
  text?: string           // 文字内容
  locked?: boolean        // 是否锁定
}
```

### 绘制流程

```
1. 选择工具
   ↓
2. 鼠标按下 (记录起点)
   ↓
3. 鼠标移动 (实时预览)
   ↓
4. 鼠标释放 (完成绘制)
   ↓
5. 保存到列表
   ↓
6. 重绘所有图形
```

---

## 📊 与图表集成

### Chart.js 集成

```typescript
import { Chart } from 'chart.js'
import { DrawingTools } from './components/DrawingTools'

const chartRef = useRef<Chart>(null)
const [drawings, setDrawings] = useState<Drawing[]>([])

// 绘图变化回调
const handleDrawingChange = (newDrawings: Drawing[]) => {
  setDrawings(newDrawings)
  // 更新图表插件
  if (chartRef.current) {
    chartRef.current.options.plugins.drawings = newDrawings
    chartRef.current.update()
  }
}

<DrawingTools
  onDrawingChange={handleDrawingChange}
  chartRef={chartRef.current}
/>
```

### TradingView 集成

```typescript
import { widget } from 'tradingview/charting_library'

const tvWidget = new widget({
  // ... 配置
  drawings_access: {
    type: 'black',
    tools: [
      { name: 'LineTool.Ray' },
      { name: 'LineTool.Trend' },
      { name: 'LineTool.Channel' },
      // ... 更多工具
    ]
  }
})
```

---

## 💾 数据持久化

### 保存到本地

```typescript
// 保存
localStorage.setItem(
  'chart-drawings',
  JSON.stringify(drawings)
)

// 加载
const savedDrawings = JSON.parse(
  localStorage.getItem('chart-drawings') || '[]'
)
setDrawings(savedDrawings)
```

### 导出/导入

```typescript
// 导出 JSON
const exportDrawings = () => {
  const json = JSON.stringify(drawings, null, 2)
  const blob = new Blob([json], { type: 'application/json' })
  const url = URL.createObjectURL(blob)
  // 下载文件
}

// 导入 JSON
const importDrawings = (file: File) => {
  const reader = new FileReader()
  reader.onload = (e) => {
    const drawings = JSON.parse(e.target.result as string)
    setDrawings(drawings)
  }
  reader.readAsText(file)
}
```

---

## 🎯 最佳实践

### 1. 简洁为美
- 不要画太多线条
- 只保留关键的趋势线和价位
- 定期清理过时的标注

### 2. 颜色规范
- 🟢 绿色 - 支撑、买入
- 🔴 红色 - 阻力、卖出
- 🔵 蓝色 - 趋势线
- 🟡 黄色 - 警告、关注

### 3. 多时间周期
- 在不同周期使用不同颜色
- 日线用粗线
- 小时线用细线

### 4. 标注说明
- 重要位置添加文字说明
- 记录关键事件
- 交易计划备注

---

## 🔮 未来计划

### v2.3
- ✅ 13种基础工具
- ⏳ 图形编辑功能
- ⏳ 图形复制/粘贴
- ⏳ 图层管理

### v2.4
- ⏳ 更多形态工具
- ⏳ 江恩角度线
- ⏳ 艾略特波浪
- ⏳ 和谐形态

### v2.5
- ⏳ 画线模板
- ⏳ 云端同步
- ⏳ 协作绘图
- ⏳ AI 辅助画线

---

## 📚 相关文档

- [MULTI_MARKET.md](./MULTI_MARKET.md) - 多市场数据
- [CHART_SENDING.md](./CHART_SENDING.md) - 图表发送
- [README.md](../README.md) - 项目总览

---

**版本**: v2.3.0  
**日期**: 2026-06-16  
**功能**: 画线工具集 📐
