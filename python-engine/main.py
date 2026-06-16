from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes import market, backtest, ai, data, indicators, openai_compat, bot
from core.data.database import get_database, close_database
from contextlib import asynccontextmanager

# 导入多市场和新闻模块
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent))
from multi_market import router as multi_market_router
from global_news import router as global_news_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # 启动时初始化数据库
    db = await get_database()
    print(f"Database initialized at {db.db_path}")
    yield
    # 关闭时清理数据库连接
    await close_database()
    print("Database connection closed")

app = FastAPI(title="Stocks Trading Engine", version="0.1.0", lifespan=lifespan)

# CORS配置，允许Tauri前端访问
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "tauri://localhost"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(market.router, prefix="/api/market", tags=["market"])
app.include_router(backtest.router, prefix="/api/backtest", tags=["backtest"])
app.include_router(ai.router, prefix="/api/ai", tags=["ai"])
app.include_router(data.router, prefix="/api/data", tags=["data"])
app.include_router(indicators.router, prefix="/api/indicators", tags=["indicators"])
app.include_router(openai_compat.router, tags=["openai-compat"])
app.include_router(bot.router, prefix="/api", tags=["bot"])

# 新增路由
app.include_router(multi_market_router, tags=["multi-market"])
app.include_router(global_news_router, tags=["news"])


@app.get("/")
async def root():
    return {"message": "Stocks Trading Engine API", "version": "0.1.0"}


@app.get("/health")
async def health():
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
