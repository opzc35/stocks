"""
应用配置
"""
import os
from typing import Optional


class Settings:
    """应用设置"""

    # API配置
    API_HOST: str = os.getenv("API_HOST", "127.0.0.1")
    API_PORT: int = int(os.getenv("API_PORT", "8000"))

    # 数据库配置
    DATABASE_PATH: str = os.getenv("DATABASE_PATH", "data/stocks.db")

    # 交易所API密钥（可选）
    BINANCE_API_KEY: Optional[str] = os.getenv("BINANCE_API_KEY")
    BINANCE_API_SECRET: Optional[str] = os.getenv("BINANCE_API_SECRET")

    OKX_API_KEY: Optional[str] = os.getenv("OKX_API_KEY")
    OKX_API_SECRET: Optional[str] = os.getenv("OKX_API_SECRET")

    # Claude API配置
    ANTHROPIC_API_KEY: Optional[str] = os.getenv("ANTHROPIC_API_KEY")

    # 日志配置
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")

    # CORS配置
    CORS_ORIGINS: list = [
        "http://localhost:5173",
        "tauri://localhost",
        "http://tauri.localhost",
    ]


settings = Settings()
