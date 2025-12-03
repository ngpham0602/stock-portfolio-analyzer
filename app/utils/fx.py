"""
Simple FX helpers to practice functions and conditionals.
"""
from decimal import Decimal
from typing import Protocol


class FxProvider(Protocol):
    def get_fx_rate(self, from_currency: str, to_currency: str) -> dict: ...


def convert(amount: Decimal, from_currency: str, to_currency: str, provider: FxProvider) -> Decimal:
    if from_currency == to_currency:
        return amount
    data = provider.get_fx_rate(from_currency, to_currency)
    rate_str = data.get("Realtime Currency Exchange Rate", {}).get("5. Exchange Rate")
    if rate_str is None:
        raise RuntimeError("FX rate missing in provider response")
    rate = Decimal(rate_str)
    return amount * rate
