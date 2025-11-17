from pydantic import BaseModel, Field
from datetime import date, datetime
from decimal import Decimal
from typing import Optional, List

class Stock(BaseModel):
    ticker: str = Field(..., description="Stock Symbol (e.g: APPL)")
    name: Optional[str] = None

class Transaction(BaseModel):
    ticker: str
    date: date
    quantity: Decimal
    price: Decimal
    transaction_type: str = Field(..., pattern="^(buy|sell)$")

class Position(BaseModel):
    ticker: str
    quantity: Decimal
    avg_cost: Decimal
    current_price: Optional[Decimal] = None

    @property
    def market_value(self) -> Optional[Decimal]:
        if self.current_price: 
            return (self.current_price - self.avg_cost) * self.quantity
        return None

class Portfolio(BaseModel):
    positions: List[Position] = []
    cash: Decimal = Decimal("100000.0")
    base_currency: str = 'AUD'

    