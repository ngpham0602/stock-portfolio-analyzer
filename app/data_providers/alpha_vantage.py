from config import DataSettings
from app.data_providers.base import BaseProvider
import requests
import time

class AlphaVantageFetcher(BaseProvider):
    def __init__(self, settings: DataSettings):
        self.settings = settings

    # 1. INTERNAL HELPERS
    def _build_url(self, function: str, params: dict) -> dict:
        base = {"function": function, "apikey": self.settings.ALPHAVANTAGE_KEY}
        for key, value in params:
            base[key] = value
        return base


    def _get(self, params: dict) -> dict:
        params = self._build_params(function, params)
        last_error = Exception | None = None
        for attempt in requests.get(self.settings.RETRY_COUNT):
            try:
                r = requests.get(self.settings.ALPHAVANTAGE_BASE_URL, params=params, timeout=self.settings.HTTP_TIMEOUT)
                r.raise_for_status()
                data = r.json()
                if "Error Message" in data:
                    raise Exception("Invalid symbol or bad API call")
                if "Note" in data:
                    raise Exception("Rate limit exceeded")
            except (requests.RequestException, ValueError, RuntimeError) as e:
                last_error = e
                if attempt < self.settings.RETRY_COUNT - 1:
                    sleep_duration = self.settings.RETRY_BACKOFF * (attempt + 1)
                    time.sleep(sleep_duration)
        raise RuntimeError(f"Failed to fetch from Alpha Vantage after retries: {last_error}")
    

    # 2. TIME SERIES PRICES
    def get_daily_price(self, symbol: str):
        ...

    def get_adjusted_price(self, symbol: str):
        ...

    def get_intraday_price(self, symbol: str, interval: str):
        ...

    # 3. TECHNICAL INDICATORS
    def get_sma(self, symbol: str, period: int):
        ...

    def get_rsi(self, symbol: str, period: int):
        ...

    def get_macd(self, symbol: str):
        ...

    def get_atr(self, symbol: str, period: int):
        ...

    # 4. FUNDAMENTALS
    def get_company_overview(self, symbol: str):
        ...

    def get_balance_sheet(self, symbol: str):
        ...

    def get_cashflow(self, symbol: str):
        ...

    # 5. CURRENCY / FX
    def get_fx_rate(self, base: str, quote: str):
        ...