import time
from typing import Dict, Any

import requests

from app.config import DataSettings
from app.data_providers.base import BaseProvider, ProviderError

class AlphaVantageFetcher(BaseProvider):
    def __init__(self, settings: DataSettings):
        self.settings = settings

    # 1. INTERNAL HELPERS
    def _build_url(self, function: str, extra_params: dict) -> dict:
        base = {"function": function, "apikey": self.settings.ALPHAVANTAGE_KEY}
        base.update(extra_params)
        return base


    def _get(self, function: str, extra_params: dict) -> dict:
        params = self._build_url(function, extra_params)
        last_error: Exception | None = None
        for attempt in range(self.settings.RETRY_COUNT):
            try:
                r = requests.get(self.settings.ALPHAVANTAGE_BASE_URL, params=params, timeout=self.settings.HTTP_TIMEOUT)
                r.raise_for_status()
                data = r.json()
                if "Error Message" in data:
                    raise ProviderError(f"Invalid symbol or bad API call for {extra_params.get('symbol', '')}")
                if "Note" in data:
                    raise ProviderError("Rate limit exceeded; retrying with backoff")
                return data
            except (requests.RequestException, ValueError, RuntimeError) as e:
                last_error = e
                if attempt < self.settings.RETRY_COUNT - 1:
                    sleep_duration = self.settings.RETRY_BACKOFF * (attempt + 1)
                    time.sleep(sleep_duration)
        raise ProviderError(f"Failed to fetch from Alpha Vantage after retries: {last_error}")
    

    # 2. TIME SERIES PRICES
    def get_daily_price(self, symbol: str, outputsize: str = "compact"):
        function = "TIME_SERIES_DAILY_ADJUSTED"
        extra_params = {
            "symbol": symbol, 
            "outputsize": outputsize
        }
        data = self._get(function, extra_params)
        return data

    def get_adjusted_price(self, symbol: str, outputsize: str = "compact"):
        function = "TIME_SERIES_ADJUSTED"
        extra_params = {
            "symbol": symbol, 
            "outputsize": outputsize
        }
        data = self._get(function, extra_params)
        return data

    def get_intraday_price(self, symbol: str, interval: str):
        function = "TIME_SERIES_INTRADAY"
        extra_params = {
            "symbol": symbol,
            "interval": interval,
            "outputsize": "compact"
        }
        data = self._get(function, extra_params)
        return data

    # 3. TECHNICAL INDICATORS
    def get_sma(self, symbol: str, period: int, interval: str = "daily", series_type: str = "close"):
        function = "SMA"
        extra_params = {
            "symbol": symbol,
            "interval": interval,
            "series_type": series_type,
            "time_period": period
        }
        return self._get(function, extra_params)
        

    def get_rsi(self, symbol: str, period: int, interval: str = "daily", series_type: str = "close"):
        function = "RSI"
        extra_params = {
            "symbol": symbol,
            "interval": interval,
            "series_type": series_type,
            "time_period": period
        }
        return self._get(function, extra_params)

    def get_macd(self, symbol: str, fastperiod: int, slowperiod: int, signalperiod: int, interval: str = "daily", series_type: str = "close"):
        function = "MACD"
        extra_params = {
            "symbol": symbol,
            "interval": interval,
            "series_type": series_type,
            "fast_period": fastperiod,
            "slow_period": slowperiod,
            "signal_period": signalperiod
        }
        return self._get(function, extra_params)

    def get_atr(self, symbol: str, period: int, interval: str = "daily"):
        function = "ATR"
        extra_params = {
            "symbol": symbol,
            "interval": interval,
            "time_period": period
        }
        return self._get(function, extra_params)

    # 4. FUNDAMENTALS
    def get_company_overview(self, symbol: str):
        function = "OVERVIEW"
        extra_params = {
            "symbol": symbol
        }
        return self._get(function, extra_params)

    def get_balance_sheet(self, symbol: str):
        function = "BALANCE_SHEET"
        extra_params = {
            "symbol": symbol
        }
        return self._get(function, extra_params)

    def get_cashflow(self, symbol: str):
        function = "CASH_FLOW"
        extra_params = {
            "symbol": symbol
        }
        return self._get(function, extra_params)
        

    # 5. CURRENCY / FX
    def get_fx_rate(self, from_currency: str, to_currency: str):
        function = "CURRENCY_EXCHANGE_RATE"
        extra_params = {
            "from_currency": from_currency,
            "to_currency": to_currency
        }
        return self._get(function, extra_params)


if __name__ == "__main__":
    settings = DataSettings()
    fetcher = AlphaVantageFetcher(settings)
    result = fetcher.get_daily_price("AAPL")
    print(result.keys())
