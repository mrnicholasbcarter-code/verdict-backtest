from typing import Protocol

class FeeModel(Protocol):
    def calculate_fee(self, entry_cents: float, payout_cents: float) -> float:
        ...

class BoundedProfitFeeModel:
    """
    Models traditional prediction market structures (e.g., Kalshi).
    Charges a percentage of the gross profit, strictly capped at a maximum ceiling.
    """
    def __init__(self, percent_of_profit: float = 0.07, maximum_fee_cents: float = 0.05):
        self.pct = percent_of_profit
        self.max_fee = maximum_fee_cents

    def calculate_fee(self, entry_cents: float, payout_cents: float) -> float:
        gross_profit = payout_cents - entry_cents
        if gross_profit <= 0:
            return 0.0
            
        calculated = gross_profit * self.pct
        return min(calculated, self.max_fee)

class FlatMakerTakerModel:
    """
    Standard crypto/CLOB model (e.g., Polymarket).
    """
    def __init__(self, maker_bps: float = 0.0, taker_bps: float = 0.001):
        self.maker = maker_bps
        self.taker = taker_bps
        
    def calculate_fee(self, trade_volume: float, is_maker: bool) -> float:
        rate = self.maker if is_maker else self.taker
        return trade_volume * rate
