from __future__ import annotations
from pydantic import BaseSettings, Field, model_validator
from pathlib import Path
from datetime import date
from enum import Enum
from functools import lru_cache

class Provider(str, Enum):
    yf: str = "yf"
    av: str = "av"
    ibkr: str = "ibkr"

class MarketSettings(BaseSettings):
    BASE_CCY: str = Field("AUD", description="Portfolio base currency for reporting")
    TIMEZONE: str = Field("Austrlia/Sydney", description="Local timezone for timestamp")
    HISTORY: date = Field(date(2018, 1, 1), description="Default beginning history for the chat")
    DEFAULT_INTRADAY_INTERVAL: str = Field("60min", description="Default Intraday interval for market trading")


class DataSettings(BaseSettings):
    PROVIDER: Provider = Field(Provider.av, description="Using the adapter to provide the stock information")
    HTTP_TIMEOUT: int = Field(20, description="Time duration for http timeout")
    RATE_LIMIT_PER_MIN: int = Field(5, description="Default per-minute throttle for the API's free version")
    ALPHAVANTAGE_KEY: str | None = Field(None, description="Alpha Vantage's API Key")
    ALPHAVANTAGE_BASE_URL: str = Field("https://www.alphavantage.co/query", description="Base URL For Alpha Vantage")
    CACHE_TTL: int = Field(300, description="Cache Time to live in seconds")
    CACHE_DIR: Path = Field(Path("data/cache"), description="Where API is stored")
    RETRY_COUNT: int = Field(3, description="Retry attemps if API fails")
    RETRY_BACKOFF: float = Field(1.5, description="Retry backoff")
    LOG_LEVEL: str = Field("INFO", description="Logging level for data providers")


    @model_validator(mode="before")
    def _require_keys_when_selected(cls, values):
        prov = values.get("PROVIDER")
        if prov == Provider.av and not values.get("ALPHAVANTAGE_KEY"):
            raise ValueError("ALPHAVANTAGE_KEY is required when PROVIDER=av")
        return values
