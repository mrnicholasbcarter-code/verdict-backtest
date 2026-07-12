"""Fee models for predictive markets.

This module provides fee calculation models for different prediction market
platforms, including Kalshi's bounded profit fee model and flat maker-taker
models used by platforms like Polymarket.
"""

from typing import Protocol


class FeeModel(Protocol):
    """Protocol defining the interface for fee calculation models."""

    def calculate_fee(self, entry_cents: float, payout_cents: float) -> float:
        """Calculate the fee for a given trade.

        Args:
            entry_cents: Entry price in cents.
            payout_cents: Payout price in cents.

        Returns:
            The calculated fee in cents.
        """
        ...


class BoundedProfitFeeModel:
    """Models traditional prediction market structures (e.g., Kalshi).

    Charges a percentage of the gross profit, strictly capped at a maximum ceiling.
    This model reflects Kalshi's fee structure: 7% of gross profit, capped at 5 cents.

    Attributes:
        percent_of_profit: Percentage of gross profit charged as fee (default 0.07 = 7%).
        maximum_fee_cents: Maximum fee cap in cents (default 0.05 = 5 cents).
    """

    def __init__(self, percent_of_profit: float = 0.07, maximum_fee_cents: float = 0.05):
        """Initialize the bounded profit fee model.

        Args:
            percent_of_profit: Percentage of gross profit to charge (default 7%).
            maximum_fee_cents: Maximum fee cap in cents (default 5 cents).
        """
        self.pct = percent_of_profit
        self.max_fee = maximum_fee_cents

    def calculate_fee(self, entry_cents: float, payout_cents: float) -> float:
        """Calculate fee based on entry and payout prices.

        Args:
            entry_cents: Entry price in cents.
            payout_cents: Payout price in cents.

        Returns:
            The fee in cents, capped at maximum_fee_cents.
        """
        gross_profit = payout_cents - entry_cents
        if gross_profit <= 0:
            return 0.0

        calculated = gross_profit * self.pct
        return min(calculated, self.max_fee)


class FlatMakerTakerModel:
    """Standard crypto/CLOB model (e.g., Polymarket orderbook).

    Charges a flat basis-point rate on trade volume, with different rates
    for makers (liquidity providers) and takers (liquidity consumers).

    Attributes:
        maker_bps: Maker fee in basis points (default 0.0).
        taker_bps: Taker fee in basis points (default 0.001 = 10 bps).
    """

    def __init__(self, maker_bps: float = 0.0, taker_bps: float = 0.001):
        """Initialize the flat maker-taker fee model.

        Args:
            maker_bps: Fee rate for makers in basis points (default 0 bps).
            taker_bps: Fee rate for takers in basis points (default 10 bps).
        """
        self.maker = maker_bps
        self.taker = taker_bps

    def calculate_fee(self, trade_volume: float, is_maker: bool) -> float:
        """Calculate fee based on trade volume and maker/taker status.

        Args:
            trade_volume: Trade volume in base currency units.
            is_maker: True if the order provides liquidity (maker), False if taker.

        Returns:
            The calculated fee in base currency units.
        """
        rate = self.maker if is_maker else self.taker
        return trade_volume * rate