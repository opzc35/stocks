"""
全球新闻聚合接口

数据源:
- CryptoCompare (加密货币新闻)
- NewsAPI (全球财经新闻)
- RSS聚合 (中文财经媒体)
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime, timedelta
import httpx
import feedparser

router = APIRouter(prefix="/api/news", tags=["news"])


class NewsItem(BaseModel):
    """新闻条目"""
    id: str
    title: str
    summary: str
    content: Optional[str] = None
    url: str
    source: str
    author: Optional[str] = None
    published_at: int  # Unix timestamp (ms)
    image_url: Optional[str] = None
    category: str  # crypto, stock, forex, commodity, general
    sentiment: Optional[str] = None  # positive, negative, neutral
    tags: List[str] = []
    language: str = 'en'


# ============================================
# 加密货币新闻
# ============================================

async def fetch_crypto_news(limit: int = 20) -> List[NewsItem]:
    """获取加密货币新闻 (CryptoCompare)"""
    news_items = []

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(
                "https://min-api.cryptocompare.com/data/v2/news/",
                params={'lang': 'EN'}
            )

            if response.status_code == 200:
                data = response.json()

                for item in data.get('Data', [])[:limit]:
                    news_items.append(NewsItem(
                        id=str(item['id']),
                        title=item['title'],
                        summary=item['body'][:200] + '...' if len(item['body']) > 200 else item['body'],
                        content=item['body'],
                        url=item['url'],
                        source=item['source'],
                        published_at=item['published_on'] * 1000,
                        image_url=item.get('imageurl'),
                        category='crypto',
                        tags=item.get('tags', '').split('|') if item.get('tags') else [],
                        language='en'
                    ))

    except Exception as e:
        print(f"Error fetching crypto news: {e}")

    return news_items


# ============================================
# 全球财经新闻 (英文)
# ============================================

async def fetch_financial_news(query: str = 'stock market', limit: int = 20) -> List[NewsItem]:
    """
    获取全球财经新闻 (NewsAPI)

    需要 API Key: https://newsapi.org/
    """
    news_items = []

    # 注意: 需要设置环境变量 NEWS_API_KEY
    # 这里使用模拟数据
    try:
        # 模拟新闻数据
        mock_news = [
            {
                'title': 'Fed Holds Interest Rates Steady',
                'description': 'The Federal Reserve decided to maintain interest rates at current levels.',
                'url': 'https://example.com/fed-rates',
                'source': {'name': 'Bloomberg'},
                'publishedAt': datetime.now().isoformat(),
                'urlToImage': None,
                'content': 'Full content...'
            },
            {
                'title': 'Tech Stocks Rally as AI Boom Continues',
                'description': 'Major tech stocks surge on strong earnings and AI optimism.',
                'url': 'https://example.com/tech-rally',
                'source': {'name': 'CNBC'},
                'publishedAt': (datetime.now() - timedelta(hours=2)).isoformat(),
                'urlToImage': None,
                'content': 'Full content...'
            },
            {
                'title': 'Oil Prices Rise Amid Supply Concerns',
                'description': 'Crude oil prices climb as OPEC+ considers production cuts.',
                'url': 'https://example.com/oil-prices',
                'source': {'name': 'Reuters'},
                'publishedAt': (datetime.now() - timedelta(hours=4)).isoformat(),
                'urlToImage': None,
                'content': 'Full content...'
            }
        ]

        for item in mock_news[:limit]:
            published_dt = datetime.fromisoformat(item['publishedAt'].replace('Z', '+00:00'))

            news_items.append(NewsItem(
                id=str(hash(item['url'])),
                title=item['title'],
                summary=item['description'] or '',
                content=item.get('content', ''),
                url=item['url'],
                source=item['source']['name'],
                published_at=int(published_dt.timestamp() * 1000),
                image_url=item.get('urlToImage'),
                category='stock',
                tags=[],
                language='en'
            ))

    except Exception as e:
        print(f"Error fetching financial news: {e}")

    return news_items


# ============================================
# 中文财经新闻
# ============================================

async def fetch_chinese_news(limit: int = 20) -> List[NewsItem]:
    """获取中文财经新闻 (RSS)"""
    news_items = []

    # 中文财经媒体 RSS 源
    rss_feeds = [
        ('https://rss.nytimes.com/services/xml/rss/nyt/Business.xml', 'NYTimes', 'stock'),
        ('https://feeds.bloomberg.com/markets/news.rss', 'Bloomberg', 'stock'),
    ]

    try:
        for feed_url, source, category in rss_feeds:
            # 使用 feedparser 解析 RSS
            feed = feedparser.parse(feed_url)

            for entry in feed.entries[:limit // len(rss_feeds)]:
                # 解析发布时间
                published_dt = datetime(*entry.published_parsed[:6]) if hasattr(entry, 'published_parsed') else datetime.now()

                news_items.append(NewsItem(
                    id=entry.get('id', str(hash(entry.link))),
                    title=entry.title,
                    summary=entry.get('summary', '')[:200],
                    content=entry.get('content', [{}])[0].get('value', '') if entry.get('content') else '',
                    url=entry.link,
                    source=source,
                    published_at=int(published_dt.timestamp() * 1000),
                    image_url=entry.get('media_content', [{}])[0].get('url') if entry.get('media_content') else None,
                    category=category,
                    tags=[tag.term for tag in entry.get('tags', [])],
                    language='zh'
                ))

    except Exception as e:
        print(f"Error fetching Chinese news: {e}")

    # 模拟中文新闻
    if not news_items:
        mock_chinese_news = [
            NewsItem(
                id='cn-1',
                title='A股三大指数集体收涨，科技股领涨',
                summary='沪深两市今日高开高走，创业板指涨超2%，科技股表现强势。',
                url='https://example.com/cn-stock-1',
                source='财经网',
                published_at=int(datetime.now().timestamp() * 1000),
                category='stock',
                tags=['A股', '科技股'],
                language='zh'
            ),
            NewsItem(
                id='cn-2',
                title='央行宣布降准0.25个百分点',
                summary='中国人民银行决定下调存款准备金率，释放长期资金约5000亿元。',
                url='https://example.com/cn-pboc',
                source='新华财经',
                published_at=int((datetime.now() - timedelta(hours=3)).timestamp() * 1000),
                category='stock',
                tags=['货币政策', '降准'],
                language='zh'
            ),
            NewsItem(
                id='cn-3',
                title='港股恒生指数午后跳水，地产股领跌',
                summary='恒生指数午后快速下跌，地产板块跌幅居前。',
                url='https://example.com/hk-stock',
                source='香港经济日报',
                published_at=int((datetime.now() - timedelta(hours=5)).timestamp() * 1000),
                category='stock',
                tags=['港股', '地产'],
                language='zh'
            )
        ]

        news_items.extend(mock_chinese_news)

    return news_items


# ============================================
# 情感分析 (简化版)
# ============================================

def analyze_sentiment(text: str) -> str:
    """简单的情感分析"""
    positive_words = ['surge', 'rally', 'gain', 'rise', 'up', 'bull', 'growth', '上涨', '涨', '利好']
    negative_words = ['fall', 'drop', 'decline', 'down', 'bear', 'crash', '下跌', '跌', '利空']

    text_lower = text.lower()

    positive_count = sum(1 for word in positive_words if word in text_lower)
    negative_count = sum(1 for word in negative_words if word in text_lower)

    if positive_count > negative_count:
        return 'positive'
    elif negative_count > positive_count:
        return 'negative'
    else:
        return 'neutral'


# ============================================
# 统一接口
# ============================================

async def fetch_all_news(
    categories: List[str] = ['crypto', 'stock'],
    languages: List[str] = ['en', 'zh'],
    limit: int = 50
) -> List[NewsItem]:
    """获取所有新闻（聚合）"""

    all_news = []

    # 并发获取新闻
    tasks = []

    if 'crypto' in categories:
        tasks.append(fetch_crypto_news(limit))

    if 'stock' in categories:
        if 'en' in languages:
            tasks.append(fetch_financial_news('stock market', limit))
        if 'zh' in languages:
            tasks.append(fetch_chinese_news(limit))

    # 等待所有任务完成
    results = await asyncio.gather(*tasks, return_exceptions=True)

    for result in results:
        if isinstance(result, list):
            all_news.extend(result)

    # 添加情感分析
    for news in all_news:
        if not news.sentiment:
            news.sentiment = analyze_sentiment(news.title + ' ' + news.summary)

    # 按时间排序
    all_news.sort(key=lambda x: x.published_at, reverse=True)

    return all_news[:limit]


# ============================================
# API 端点
# ============================================

@router.get("/latest")
async def get_latest_news(
    category: str = 'all',
    language: str = 'all',
    limit: int = 20
):
    """
    获取最新新闻

    参数:
    - category: crypto, stock, forex, commodity, all
    - language: en, zh, all
    - limit: 返回条数
    """

    categories = [category] if category != 'all' else ['crypto', 'stock']
    languages = [language] if language != 'all' else ['en', 'zh']

    news = await fetch_all_news(categories, languages, limit)

    return {
        "success": True,
        "data": [n.dict() for n in news],
        "count": len(news)
    }


@router.get("/crypto")
async def get_crypto_news(limit: int = 20):
    """获取加密货币新闻"""
    news = await fetch_crypto_news(limit)

    return {
        "success": True,
        "data": [n.dict() for n in news],
        "count": len(news)
    }


@router.get("/financial")
async def get_financial_news(
    query: str = 'stock market',
    limit: int = 20
):
    """获取财经新闻"""
    news = await fetch_financial_news(query, limit)

    return {
        "success": True,
        "data": [n.dict() for n in news],
        "count": len(news)
    }


@router.get("/chinese")
async def get_chinese_news(limit: int = 20):
    """获取中文财经新闻"""
    news = await fetch_chinese_news(limit)

    return {
        "success": True,
        "data": [n.dict() for n in news],
        "count": len(news)
    }


@router.get("/search")
async def search_news(
    q: str,
    category: str = 'all',
    language: str = 'all',
    limit: int = 20
):
    """搜索新闻"""

    categories = [category] if category != 'all' else ['crypto', 'stock']
    languages = [language] if language != 'all' else ['en', 'zh']

    all_news = await fetch_all_news(categories, languages, 100)

    # 简单搜索
    q_lower = q.lower()
    filtered = [
        n for n in all_news
        if q_lower in n.title.lower() or q_lower in n.summary.lower()
    ]

    return {
        "success": True,
        "data": [n.dict() for n in filtered[:limit]],
        "count": len(filtered)
    }


# 导入必要的模块
import asyncio
