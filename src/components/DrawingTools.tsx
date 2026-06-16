import { useState, useRef, useEffect } from 'react'
import './DrawingTools.css'

export type DrawingType =
  | 'none'
  | 'line'           // 直线
  | 'ray'            // 射线
  | 'arrow'          // 箭头
  | 'horizontal'     // 水平线
  | 'vertical'       // 垂直线
  | 'trend'          // 趋势线
  | 'channel'        // 平行通道
  | 'fibonacci'      // 斐波那契回调
  | 'rectangle'      // 矩形
  | 'triangle'       // 三角形
  | 'circle'         // 圆形
  | 'text'           // 文字标注
  | 'measure'        // 测量工具

export interface Drawing {
  id: string
  type: DrawingType
  points: { x: number; y: number; price?: number; time?: number }[]
  color: string
  lineWidth: number
  text?: string
  style?: 'solid' | 'dashed' | 'dotted'
  filled?: boolean
  locked?: boolean
}

interface DrawingToolsProps {
  onDrawingChange: (drawings: Drawing[]) => void
  chartRef: any // Chart.js 实例
}

export function DrawingTools({ onDrawingChange, chartRef }: DrawingToolsProps) {
  const [selectedTool, setSelectedTool] = useState<DrawingType>('none')
  const [drawings, setDrawings] = useState<Drawing[]>([])
  const [currentDrawing, setCurrentDrawing] = useState<Drawing | null>(null)
  const [selectedColor, setSelectedColor] = useState('#0070f3')
  const [lineWidth, setLineWidth] = useState(2)
  const [lineStyle, setLineStyle] = useState<'solid' | 'dashed' | 'dotted'>('solid')
  const [showSettings, setShowSettings] = useState(false)

  const canvasRef = useRef<HTMLCanvasElement>(null)
  const isDrawing = useRef(false)

  // 工具列表
  const tools = [
    { type: 'line' as DrawingType, icon: '📏', label: '直线', hotkey: 'L' },
    { type: 'ray' as DrawingType, icon: '➡️', label: '射线', hotkey: 'R' },
    { type: 'arrow' as DrawingType, icon: '→', label: '箭头', hotkey: 'A' },
    { type: 'horizontal' as DrawingType, icon: '—', label: '水平线', hotkey: 'H' },
    { type: 'vertical' as DrawingType, icon: '|', label: '垂直线', hotkey: 'V' },
    { type: 'trend' as DrawingType, icon: '📈', label: '趋势线', hotkey: 'T' },
    { type: 'channel' as DrawingType, icon: '⚌', label: '平行通道', hotkey: 'C' },
    { type: 'fibonacci' as DrawingType, icon: 'φ', label: '斐波那契', hotkey: 'F' },
    { type: 'rectangle' as DrawingType, icon: '▭', label: '矩形', hotkey: 'S' },
    { type: 'triangle' as DrawingType, icon: '△', label: '三角形', hotkey: 'G' },
    { type: 'circle' as DrawingType, icon: '○', label: '圆形', hotkey: 'O' },
    { type: 'text' as DrawingType, icon: 'T', label: '文字', hotkey: 'X' },
    { type: 'measure' as DrawingType, icon: '📐', label: '测量', hotkey: 'M' },
  ]

  // 颜色预设
  const colorPresets = [
    '#0070f3', // 蓝色
    '#0ba360', // 绿色
    '#f857a6', // 红色
    '#f5a623', // 黄色
    '#9b59b6', // 紫色
    '#ffffff', // 白色
    '#a1a1aa', // 灰色
  ]

  // 选择工具
  const selectTool = (type: DrawingType) => {
    setSelectedTool(type)
    if (canvasRef.current) {
      canvasRef.current.style.cursor = type === 'none' ? 'default' : 'crosshair'
    }
  }

  // 鼠标按下
  const handleMouseDown = (e: React.MouseEvent<HTMLCanvasElement>) => {
    if (selectedTool === 'none') return

    const rect = canvasRef.current?.getBoundingClientRect()
    if (!rect) return

    const x = e.clientX - rect.left
    const y = e.clientY - rect.top

    const point = { x, y, price: getPriceFromY(y), time: getTimeFromX(x) }

    // 创建新绘图
    const newDrawing: Drawing = {
      id: Date.now().toString(),
      type: selectedTool,
      points: [point],
      color: selectedColor,
      lineWidth: lineWidth,
      style: lineStyle,
    }

    setCurrentDrawing(newDrawing)
    isDrawing.current = true
  }

  // 鼠标移动
  const handleMouseMove = (e: React.MouseEvent<HTMLCanvasElement>) => {
    if (!isDrawing.current || !currentDrawing) return

    const rect = canvasRef.current?.getBoundingClientRect()
    if (!rect) return

    const x = e.clientX - rect.left
    const y = e.clientY - rect.top

    const point = { x, y, price: getPriceFromY(y), time: getTimeFromX(x) }

    // 更新当前绘图
    const updated = { ...currentDrawing }

    if (updated.points.length === 1) {
      updated.points.push(point)
    } else {
      updated.points[updated.points.length - 1] = point
    }

    // 特殊处理
    if (updated.type === 'horizontal') {
      updated.points[1].y = updated.points[0].y
    } else if (updated.type === 'vertical') {
      updated.points[1].x = updated.points[0].x
    }

    setCurrentDrawing(updated)
    redraw()
  }

  // 鼠标释放
  const handleMouseUp = () => {
    if (!isDrawing.current || !currentDrawing) return

    // 保存绘图
    if (currentDrawing.points.length >= 2) {
      const newDrawings = [...drawings, currentDrawing]
      setDrawings(newDrawings)
      onDrawingChange(newDrawings)
    }

    setCurrentDrawing(null)
    isDrawing.current = false

    // 完成后取消工具选择
    selectTool('none')
  }

  // 重绘所有图形
  const redraw = () => {
    const canvas = canvasRef.current
    if (!canvas) return

    const ctx = canvas.getContext('2d')
    if (!ctx) return

    // 清空画布
    ctx.clearRect(0, 0, canvas.width, canvas.height)

    // 绘制已保存的图形
    drawings.forEach((drawing) => {
      drawShape(ctx, drawing)
    })

    // 绘制当前正在画的图形
    if (currentDrawing) {
      drawShape(ctx, currentDrawing)
    }
  }

  // 绘制图形
  const drawShape = (ctx: CanvasRenderingContext2D, drawing: Drawing) => {
    ctx.strokeStyle = drawing.color
    ctx.lineWidth = drawing.lineWidth
    ctx.fillStyle = drawing.color + '20' // 20% 透明度

    // 设置线条样式
    if (drawing.style === 'dashed') {
      ctx.setLineDash([5, 5])
    } else if (drawing.style === 'dotted') {
      ctx.setLineDash([2, 3])
    } else {
      ctx.setLineDash([])
    }

    const points = drawing.points

    switch (drawing.type) {
      case 'line':
      case 'ray':
      case 'arrow':
        if (points.length >= 2) {
          ctx.beginPath()
          ctx.moveTo(points[0].x, points[0].y)
          ctx.lineTo(points[1].x, points[1].y)
          ctx.stroke()

          // 箭头
          if (drawing.type === 'arrow') {
            drawArrowHead(ctx, points[0], points[1])
          }
        }
        break

      case 'horizontal':
        if (points.length >= 1) {
          ctx.beginPath()
          ctx.moveTo(0, points[0].y)
          ctx.lineTo(ctx.canvas.width, points[0].y)
          ctx.stroke()

          // 显示价格标签
          drawPriceLabel(ctx, points[0].y, points[0].price)
        }
        break

      case 'vertical':
        if (points.length >= 1) {
          ctx.beginPath()
          ctx.moveTo(points[0].x, 0)
          ctx.lineTo(points[0].x, ctx.canvas.height)
          ctx.stroke()
        }
        break

      case 'trend':
        if (points.length >= 2) {
          ctx.beginPath()
          ctx.moveTo(points[0].x, points[0].y)
          ctx.lineTo(points[1].x, points[1].y)
          ctx.stroke()

          // 显示角度和价格变化
          drawTrendInfo(ctx, points[0], points[1])
        }
        break

      case 'channel':
        if (points.length >= 3) {
          // 主趋势线
          ctx.beginPath()
          ctx.moveTo(points[0].x, points[0].y)
          ctx.lineTo(points[1].x, points[1].y)
          ctx.stroke()

          // 平行线
          const dy = points[2].y - points[0].y
          ctx.beginPath()
          ctx.moveTo(points[0].x, points[0].y + dy)
          ctx.lineTo(points[1].x, points[1].y + dy)
          ctx.stroke()

          // 填充通道
          if (drawing.filled) {
            ctx.beginPath()
            ctx.moveTo(points[0].x, points[0].y)
            ctx.lineTo(points[1].x, points[1].y)
            ctx.lineTo(points[1].x, points[1].y + dy)
            ctx.lineTo(points[0].x, points[0].y + dy)
            ctx.closePath()
            ctx.fill()
          }
        }
        break

      case 'fibonacci':
        if (points.length >= 2) {
          const levels = [0, 0.236, 0.382, 0.5, 0.618, 0.786, 1]
          const y1 = points[0].y
          const y2 = points[1].y
          const range = y2 - y1

          levels.forEach((level) => {
            const y = y1 + range * level
            ctx.beginPath()
            ctx.moveTo(0, y)
            ctx.lineTo(ctx.canvas.width, y)
            ctx.stroke()

            // 显示百分比标签
            ctx.fillStyle = drawing.color
            ctx.font = '12px monospace'
            ctx.fillText(`${(level * 100).toFixed(1)}%`, 5, y - 5)
          })
        }
        break

      case 'rectangle':
        if (points.length >= 2) {
          const width = points[1].x - points[0].x
          const height = points[1].y - points[0].y

          ctx.beginPath()
          ctx.rect(points[0].x, points[0].y, width, height)
          ctx.stroke()

          if (drawing.filled) {
            ctx.fill()
          }
        }
        break

      case 'triangle':
        if (points.length >= 3) {
          ctx.beginPath()
          ctx.moveTo(points[0].x, points[0].y)
          ctx.lineTo(points[1].x, points[1].y)
          ctx.lineTo(points[2].x, points[2].y)
          ctx.closePath()
          ctx.stroke()

          if (drawing.filled) {
            ctx.fill()
          }
        }
        break

      case 'circle':
        if (points.length >= 2) {
          const dx = points[1].x - points[0].x
          const dy = points[1].y - points[0].y
          const radius = Math.sqrt(dx * dx + dy * dy)

          ctx.beginPath()
          ctx.arc(points[0].x, points[0].y, radius, 0, Math.PI * 2)
          ctx.stroke()

          if (drawing.filled) {
            ctx.fill()
          }
        }
        break

      case 'text':
        if (points.length >= 1 && drawing.text) {
          ctx.fillStyle = drawing.color
          ctx.font = '14px sans-serif'
          ctx.fillText(drawing.text, points[0].x, points[0].y)
        }
        break

      case 'measure':
        if (points.length >= 2) {
          // 绘制测量线
          ctx.setLineDash([3, 3])
          ctx.beginPath()
          ctx.moveTo(points[0].x, points[0].y)
          ctx.lineTo(points[1].x, points[1].y)
          ctx.stroke()

          // 显示测量信息
          const dx = points[1].x - points[0].x
          const dy = points[1].y - points[0].y
          const distance = Math.sqrt(dx * dx + dy * dy)
          const priceDiff = (points[1].price || 0) - (points[0].price || 0)
          const pricePercent = ((priceDiff / (points[0].price || 1)) * 100).toFixed(2)

          const midX = (points[0].x + points[1].x) / 2
          const midY = (points[0].y + points[1].y) / 2

          ctx.fillStyle = drawing.color
          ctx.font = '12px monospace'
          ctx.fillText(
            `${priceDiff.toFixed(2)} (${pricePercent}%)`,
            midX,
            midY - 5
          )
        }
        break
    }
  }

  // 绘制箭头
  const drawArrowHead = (
    ctx: CanvasRenderingContext2D,
    from: { x: number; y: number },
    to: { x: number; y: number }
  ) => {
    const headLength = 15
    const angle = Math.atan2(to.y - from.y, to.x - from.x)

    ctx.beginPath()
    ctx.moveTo(to.x, to.y)
    ctx.lineTo(
      to.x - headLength * Math.cos(angle - Math.PI / 6),
      to.y - headLength * Math.sin(angle - Math.PI / 6)
    )
    ctx.moveTo(to.x, to.y)
    ctx.lineTo(
      to.x - headLength * Math.cos(angle + Math.PI / 6),
      to.y - headLength * Math.sin(angle + Math.PI / 6)
    )
    ctx.stroke()
  }

  // 绘制价格标签
  const drawPriceLabel = (ctx: CanvasRenderingContext2D, y: number, price?: number) => {
    if (!price) return

    ctx.fillStyle = ctx.strokeStyle
    ctx.font = '12px monospace'
    ctx.fillText(price.toFixed(2), ctx.canvas.width - 80, y - 5)
  }

  // 绘制趋势信息
  const drawTrendInfo = (
    ctx: CanvasRenderingContext2D,
    from: { x: number; y: number; price?: number },
    to: { x: number; y: number; price?: number }
  ) => {
    const angle = Math.atan2(to.y - from.y, to.x - from.x) * (180 / Math.PI)
    const priceDiff = (to.price || 0) - (from.price || 0)
    const percent = ((priceDiff / (from.price || 1)) * 100).toFixed(2)

    const midX = (from.x + to.x) / 2
    const midY = (from.y + to.y) / 2

    ctx.fillStyle = ctx.strokeStyle
    ctx.font = '11px monospace'
    ctx.fillText(`${angle.toFixed(1)}° | ${percent}%`, midX, midY - 10)
  }

  // 坐标转换（需要根据实际图表实现）
  const getPriceFromY = (y: number): number => {
    // 这里需要根据实际的图表范围计算
    // 暂时返回模拟值
    return 67000 + (1 - y / 400) * 5000
  }

  const getTimeFromX = (x: number): number => {
    return Date.now() - (800 - x) * 60000
  }

  // 清除所有绘图
  const clearAll = () => {
    setDrawings([])
    onDrawingChange([])
    redraw()
  }

  // 撤销最后一个
  const undo = () => {
    const newDrawings = drawings.slice(0, -1)
    setDrawings(newDrawings)
    onDrawingChange(newDrawings)
  }

  // 键盘快捷键
  useEffect(() => {
    const handleKeyPress = (e: KeyboardEvent) => {
      const tool = tools.find((t) => t.hotkey.toLowerCase() === e.key.toLowerCase())
      if (tool) {
        selectTool(tool.type)
      } else if (e.key === 'Escape') {
        selectTool('none')
      } else if (e.key === 'Delete' || e.key === 'Backspace') {
        undo()
      }
    }

    window.addEventListener('keypress', handleKeyPress)
    return () => window.removeEventListener('keypress', handleKeyPress)
  }, [])

  // 重绘
  useEffect(() => {
    redraw()
  }, [drawings, currentDrawing])

  return (
    <div className="drawing-tools">
      {/* 工具栏 */}
      <div className="drawing-toolbar">
        <div className="toolbar-section">
          <button
            className={`tool-btn ${selectedTool === 'none' ? 'active' : ''}`}
            onClick={() => selectTool('none')}
            title="选择工具 (ESC)"
          >
            ↖️
          </button>

          {tools.map((tool) => (
            <button
              key={tool.type}
              className={`tool-btn ${selectedTool === tool.type ? 'active' : ''}`}
              onClick={() => selectTool(tool.type)}
              title={`${tool.label} (${tool.hotkey})`}
            >
              {tool.icon}
            </button>
          ))}
        </div>

        <div className="toolbar-section">
          <button className="tool-btn" onClick={() => setShowSettings(!showSettings)}>
            ⚙️
          </button>
          <button className="tool-btn" onClick={undo} title="撤销 (Ctrl+Z)">
            ↶
          </button>
          <button className="tool-btn" onClick={clearAll} title="清除全部">
            🗑️
          </button>
        </div>
      </div>

      {/* 设置面板 */}
      {showSettings && (
        <div className="drawing-settings">
          <div className="setting-group">
            <label>颜色</label>
            <div className="color-picker">
              {colorPresets.map((color) => (
                <button
                  key={color}
                  className={`color-btn ${selectedColor === color ? 'active' : ''}`}
                  style={{ background: color }}
                  onClick={() => setSelectedColor(color)}
                />
              ))}
            </div>
          </div>

          <div className="setting-group">
            <label>线宽</label>
            <input
              type="range"
              min="1"
              max="5"
              value={lineWidth}
              onChange={(e) => setLineWidth(parseInt(e.target.value))}
            />
            <span>{lineWidth}px</span>
          </div>

          <div className="setting-group">
            <label>线型</label>
            <select value={lineStyle} onChange={(e) => setLineStyle(e.target.value as any)}>
              <option value="solid">实线</option>
              <option value="dashed">虚线</option>
              <option value="dotted">点线</option>
            </select>
          </div>
        </div>
      )}

      {/* 绘图画布 */}
      <canvas
        ref={canvasRef}
        className="drawing-canvas"
        width={800}
        height={400}
        onMouseDown={handleMouseDown}
        onMouseMove={handleMouseMove}
        onMouseUp={handleMouseUp}
        onMouseLeave={handleMouseUp}
      />
    </div>
  )
}
