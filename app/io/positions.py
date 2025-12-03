"""
Utilities for loading positions from CSV. Uses lists, dicts, loops, conditionals,
and file I/O so you can practice core skills.
"""
import csv
from decimal import Decimal
from pathlib import Path
from typing import List

from app.model import Position, Portfolio


def load_positions_csv(csv_path: Path) -> List[Position]:
    positions: List[Position] = []
    with csv_path.open("r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                ticker = row.get("ticker", "").strip().upper()
                quantity = Decimal(row.get("quantity", "0"))
                avg_cost = Decimal(row.get("avg_cost", "0"))
            except (ValueError, TypeError) as err:
                # Skip bad rows but keep going
                continue
            if not ticker:
                continue
            positions.append(Position(ticker=ticker, quantity=quantity, avg_cost=avg_cost))
    return positions


def build_portfolio(csv_path: Path, cash: Decimal = Decimal("0"), base_currency: str = "AUD") -> Portfolio:
    pos = load_positions_csv(csv_path)
    return Portfolio(positions=pos, cash=cash, base_currency=base_currency)
