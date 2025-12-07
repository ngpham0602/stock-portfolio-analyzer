import json 
from datetime import datetime
from decimal import Decimal
from typing import Any, List, Dict, Optional, Tuple

def _to_decimal(val: str | None) -> Optional[Decimal]:
    if val is None:
        return None
    try:
        return Decimal(val)
    except Exception:
        return None
    
def _parse_timestamp(ts: str) -> datetime:
    return datetime.isoformat(ts)

def parse_daily_adjusted(symbol: str, data: dict[str]) -> dict[str]:
    series_key: str = "Time Series (Daily)"
    bars: list[dict[str]] = [] 
    raw = data.get(series_key, {})
    for ts, row in raw.items():
        bars.append = {
            "symbol": symbol,
            "timestamp": _parse_timestamp(ts),
            "open": _to_decimal(row.get("1. open")),
            "high": _to_decimal(row.get("2. high")),
            "low": _to_decimal(row.get("3. low")),
            "close": _to_decimal(row.get("4. close")),
            "adj_close": _to_decimal(row.get("5. adj_close")),
            "volume": int(row.get("6. volume", 0)),
            "dividend": _to_decimal(row.get("7. dividend")),
            "split": _to_decimal(row.get("8. split"))
        }
    return bars

def parse_intraday(symbol: str, interval: int, data: dict[str]) -> dict[str]:
    series_key = f"Time series {interval}"
    bars: list[dict[str]] = []
    raw = data.get(series_key, {})
    for ts, row in raw.items():
        bars.append = {
            "symbol": symbol,
            "interval": interval,
            "timestamp": _parse_timestamp(ts),
            "open": _to_decimal(row.get("1. open")),
            "high": _to_decimal(row.get("2. high")),
            "low": _to_decimal(row.get("3. low")),
            "close": _to_decimal(row.get("4. close")),
            "volume": _to_decimal(row.get("5. volume"))
        }
    return bars
        
def parse_indicator_series(symbol: str, interval: str, data: dict[str], series_key: str, value_key: str) -> list[dict[str]]:
    points = list[dict[str]] = []
    raw = data.get(series_key, {})
    for ts, row in raw.items():
        points.append( {
            "symbol": symbol,
            "interval": interval,
            "timestamp": _parse_timestamp(ts),
            "value": data.get(row.get(value_key))
        })

    return points

def parse_macd(symbol: str, interval: str, data: dict[str]) -> list[dict[str]]:
    series_key = "Technical Analysis: MACD"
    points: list[dict[str]] = []
    raw = data.get(series_key, {})
    for ts, row in raw.items():
        points.append( {
            "symbol": symbol,
            "interval": interval,
            "timestamp": _parse_timestamp(ts),
            "macd": _to_decimal(row.get("MACD")),
            "signal": _to_decimal(row.get("MACD_signal")),
            "hist": _to_decimal(row.get("MACD_hist"))
        })
    return points

def parse_fx_rate(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Input: raw JSON from CURRENCY_EXCHANGE_RATE.
    Output: {"from", "to", "rate", "timestamp"}
    """
    raw = data.get("Realtime Currency Exchange Rate", {})
    return {
        "from": raw.get("1. From_Currency Code"),
        "to": raw.get("3. To_Currency Code"),
        "rate": _to_decimal(raw.get("5. Exchange Rate")),
        "timestamp": _parse_timestamp(raw.get("6. Last Refreshed")) if raw.get("6. Last Refreshed") else None,
    }

def parse_company_overview(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Pick a subset of fields you care about.
    """
    return {
        "name": data.get("Name"),
        "description": data.get("Description"),
        "exchange": data.get("Exchange"),
        "sector": data.get("Sector"),
        "industry": data.get("Industry"),
        "market_cap": _to_decimal(data.get("MarketCapitalization")),
        "pe_ratio": _to_decimal(data.get("PERatio")),
        "eps": _to_decimal(data.get("EPS")),
        "dividend_yield": _to_decimal(data.get("DividendYield")),
        "currency": data.get("Currency"),
    }


