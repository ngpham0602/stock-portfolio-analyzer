"""
Base interface for any market data provider. Keeping it small so you can
practice inheritance and method overriding.
"""
from abc import ABC, abstractmethod
from typing import Any, Dict


class ProviderError(RuntimeError):
    """Raised when a provider call fails."""


class BaseProvider(ABC):
    @abstractmethod
    def get_daily_price(self, symbol: str, outputsize: str = "compact") -> Dict[str, Any]:
        """Return daily price data for a symbol."""

    @abstractmethod
    def get_fx_rate(self, base: str, quote: str) -> Dict[str, Any]:
        """Return FX rate between two currencies."""
