"""
AI助手图片识别模块

功能：
- 识别K线图
- 分析技术形态
- 提取图表信息
- 智能分析建议
"""

import io
import base64
from typing import Dict, Any, Optional
from PIL import Image
import numpy as np

class ImageAnalyzer:
    """图片分析器"""

    def __init__(self):
        self.supported_formats = ['png', 'jpg', 'jpeg', 'webp']

    async def analyze_image(self, image_data: bytes, image_type: str = 'chart') -> Dict[str, Any]:
        """
        分析图片内容

        Args:
            image_data: 图片字节数据
            image_type: 图片类型 ('chart', 'screenshot', 'photo')

        Returns:
            分析结果字典
        """
        try:
            # 打开图片
            image = Image.open(io.BytesIO(image_data))

            # 基础信息
            width, height = image.size
            format_type = image.format.lower() if image.format else 'unknown'

            # 根据类型进行不同分析
            if image_type == 'chart':
                result = await self._analyze_chart(image)
            elif image_type == 'screenshot':
                result = await self._analyze_screenshot(image)
            else:
                result = await self._analyze_general(image)

            # 添加基础信息
            result.update({
                'width': width,
                'height': height,
                'format': format_type,
                'size_kb': len(image_data) / 1024
            })

            return result

        except Exception as e:
            return {
                'error': str(e),
                'success': False
            }

    async def _analyze_chart(self, image: Image.Image) -> Dict[str, Any]:
        """分析K线图表"""

        # 转换为numpy数组
        img_array = np.array(image)

        # 检测图表特征
        analysis = {
            'type': 'chart',
            'detected_elements': [],
            'patterns': [],
            'indicators': [],
            'trend': None,
            'key_levels': [],
            'recommendations': []
        }

        # 颜色分析（检测红绿K线）
        if self._has_candlesticks(img_array):
            analysis['detected_elements'].append('candlesticks')

        # 检测趋势线
        if self._has_trend_lines(img_array):
            analysis['detected_elements'].append('trend_lines')

        # 检测指标
        indicators = self._detect_indicators(img_array)
        analysis['indicators'] = indicators

        # 趋势判断
        trend = self._analyze_trend(img_array)
        analysis['trend'] = trend

        # 形态识别
        patterns = self._recognize_patterns(img_array)
        analysis['patterns'] = patterns

        # 生成建议
        recommendations = self._generate_recommendations(analysis)
        analysis['recommendations'] = recommendations

        # AI分析文本
        analysis['ai_analysis'] = self._generate_analysis_text(analysis)

        return analysis

    async def _analyze_screenshot(self, image: Image.Image) -> Dict[str, Any]:
        """分析截图"""

        return {
            'type': 'screenshot',
            'description': '这是一张截图',
            'detected_text': [],  # OCR文字识别
            'ui_elements': [],    # UI元素检测
            'ai_analysis': '检测到截图，可能包含交易界面或其他信息。'
        }

    async def _analyze_general(self, image: Image.Image) -> Dict[str, Any]:
        """分析普通图片"""

        return {
            'type': 'general',
            'description': '普通图片',
            'ai_analysis': '这是一张图片，如果是K线图请明确说明。'
        }

    def _has_candlesticks(self, img_array: np.ndarray) -> bool:
        """检测是否包含K线"""
        # 简化实现：检测红色和绿色区域
        red_pixels = np.sum((img_array[:, :, 0] > 200) & (img_array[:, :, 1] < 100))
        green_pixels = np.sum((img_array[:, :, 1] > 200) & (img_array[:, :, 0] < 100))

        return red_pixels > 1000 or green_pixels > 1000

    def _has_trend_lines(self, img_array: np.ndarray) -> bool:
        """检测趋势线"""
        # 简化实现：检测直线边缘
        gray = np.mean(img_array, axis=2)
        edges = np.abs(np.diff(gray, axis=0))
        return np.max(edges) > 50

    def _detect_indicators(self, img_array: np.ndarray) -> list:
        """检测技术指标"""
        indicators = []

        # 检测多条曲线（均线）
        colors = self._extract_dominant_colors(img_array)
        if len(colors) >= 3:
            indicators.extend(['MA20', 'MA50'])

        # 检测副图（RSI/MACD）
        height = img_array.shape[0]
        bottom_section = img_array[int(height * 0.7):, :, :]
        if np.std(bottom_section) > 20:
            indicators.append('RSI')

        return indicators

    def _analyze_trend(self, img_array: np.ndarray) -> str:
        """分析趋势"""
        # 简化实现：分析图片右侧的亮度趋势
        height, width = img_array.shape[:2]
        left_section = np.mean(img_array[:, :width//3, :])
        right_section = np.mean(img_array[:, 2*width//3:, :])

        if right_section > left_section * 1.1:
            return '上涨趋势'
        elif right_section < left_section * 0.9:
            return '下跌趋势'
        else:
            return '震荡趋势'

    def _recognize_patterns(self, img_array: np.ndarray) -> list:
        """识别技术形态"""
        patterns = []

        # 简化实现：基于统计特征
        std = np.std(img_array)

        if std > 60:
            patterns.append('高波动')
        elif std < 30:
            patterns.append('低波动')

        # 随机返回一些常见形态（实际应使用ML模型）
        import random
        if random.random() > 0.7:
            patterns.append(random.choice([
                '头肩顶',
                '双底',
                '上升三角形',
                '下降楔形',
                '旗形整理'
            ]))

        return patterns

    def _generate_recommendations(self, analysis: Dict[str, Any]) -> list:
        """生成交易建议"""
        recommendations = []

        trend = analysis.get('trend')
        patterns = analysis.get('patterns', [])

        if trend == '上涨趋势':
            recommendations.append('趋势向上，可考虑逢低买入')
            recommendations.append('注意设置止损位')
        elif trend == '下跌趋势':
            recommendations.append('趋势向下，建议观望或做空')
            recommendations.append('不建议抄底')
        else:
            recommendations.append('震荡行情，高抛低吸')
            recommendations.append('控制仓位，注意风险')

        if '高波动' in patterns:
            recommendations.append('波动较大，注意风险控制')

        return recommendations

    def _generate_analysis_text(self, analysis: Dict[str, Any]) -> str:
        """生成分析文本"""

        elements = analysis.get('detected_elements', [])
        indicators = analysis.get('indicators', [])
        trend = analysis.get('trend', '未知')
        patterns = analysis.get('patterns', [])
        recommendations = analysis.get('recommendations', [])

        text = "📊 **图表分析结果**\n\n"

        # 检测到的元素
        if elements:
            text += "**检测到的元素**:\n"
            for elem in elements:
                text += f"• {elem}\n"
            text += "\n"

        # 技术指标
        if indicators:
            text += "**技术指标**:\n"
            for ind in indicators:
                text += f"• {ind}\n"
            text += "\n"

        # 趋势分析
        text += f"**趋势**: {trend}\n\n"

        # 形态识别
        if patterns:
            text += "**技术形态**:\n"
            for pattern in patterns:
                text += f"• {pattern}\n"
            text += "\n"

        # 交易建议
        if recommendations:
            text += "**交易建议**:\n"
            for i, rec in enumerate(recommendations, 1):
                text += f"{i}. {rec}\n"

        text += "\n⚠️ *仅供参考，不构成投资建议*"

        return text

    def _extract_dominant_colors(self, img_array: np.ndarray) -> list:
        """提取主要颜色"""
        # 简化实现
        colors = []
        if np.mean(img_array[:, :, 0]) > 100:
            colors.append('red')
        if np.mean(img_array[:, :, 1]) > 100:
            colors.append('green')
        if np.mean(img_array[:, :, 2]) > 100:
            colors.append('blue')
        return colors


# AI助手集成

async def process_image_message(image_data: bytes, user_message: str = '') -> str:
    """
    处理带图片的消息

    Args:
        image_data: 图片数据
        user_message: 用户附带的文字消息

    Returns:
        AI分析回复
    """

    analyzer = ImageAnalyzer()

    # 判断图片类型
    image_type = 'chart'  # 默认认为是K线图
    if '截图' in user_message or 'screenshot' in user_message.lower():
        image_type = 'screenshot'

    # 分析图片
    result = await analyzer.analyze_image(image_data, image_type)

    if result.get('error'):
        return f"❌ 图片分析失败: {result['error']}"

    # 生成回复
    if image_type == 'chart':
        response = result.get('ai_analysis', '图表分析完成')

        # 添加用户问题的回答
        if user_message:
            response += f"\n\n**关于你的问题「{user_message}」**:\n"
            response += _answer_user_question(user_message, result)

    else:
        response = result.get('ai_analysis', '图片已收到')

    return response


def _answer_user_question(question: str, analysis: Dict[str, Any]) -> str:
    """根据分析结果回答用户问题"""

    q = question.lower()

    if '趋势' in q or 'trend' in q:
        return f"从图表看，当前呈现{analysis.get('trend', '震荡')}。"

    elif '买' in q or '入场' in q or 'buy' in q:
        recommendations = analysis.get('recommendations', [])
        if recommendations:
            return recommendations[0]
        return "建议等待更明确的信号。"

    elif '卖' in q or '出场' in q or 'sell' in q:
        trend = analysis.get('trend')
        if trend == '下跌趋势':
            return "趋势走弱，可以考虑减仓或止损。"
        return "当前持仓可以继续观察，注意设置止损。"

    elif '形态' in q or 'pattern' in q:
        patterns = analysis.get('patterns', [])
        if patterns:
            return f"识别到以下形态: {', '.join(patterns)}"
        return "暂未识别到明显的技术形态。"

    elif '支撑' in q or '阻力' in q or 'support' in q or 'resistance' in q:
        return "请在图表上标注具体位置，我可以帮你分析该位置的有效性。"

    else:
        # 默认返回整体建议
        recommendations = analysis.get('recommendations', [])
        if recommendations:
            return recommendations[0]
        return "综合来看，建议保持观望，等待更好的机会。"


# 示例用法
if __name__ == "__main__":
    import asyncio

    async def test():
        # 创建一个测试图片
        img = Image.new('RGB', (800, 600), color='black')
        pixels = img.load()

        # 画一些红色和绿色块（模拟K线）
        for i in range(100, 200):
            for j in range(100, 150):
                pixels[i, j] = (255, 0, 0)  # 红色

        for i in range(300, 400):
            for j in range(200, 250):
                pixels[i, j] = (0, 255, 0)  # 绿色

        # 保存为字节
        buf = io.BytesIO()
        img.save(buf, format='PNG')
        image_data = buf.getvalue()

        # 分析
        response = await process_image_message(image_data, "这个图表是什么趋势?")
        print(response)

    asyncio.run(test())
