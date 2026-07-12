"""Backtest Harness - Monte Carlo Simulation Engine & Fee Evaluator.

A high-performance Monte Carlo simulation engine for predictive market backtesting
with built-in fee models for Kalshi (bounded profit) and Polymarket (flat maker-taker).

Example:
    >>> import numpy as np
    >>> from backtest_harness import MonteCarloSimulator, BoundedProfitFeeModel
    >>>
    >>> # Simulate equity paths
    >>> returns = np.array([0.05, -0.10, 0.02, 0.15, -0.05])
    >>> stats = MonteCarloSimulator.simulate_equity_paths(
    ...     trade_returns_pct=returns,
    ...     starting_equity=1000.0,
    ...     num_simulations=5000,
    ...     trades_per_sim=250
    ... )
    >>> print(f"Risk of Ruin: {stats['prob_ruin'] * 100:.1f}%")
    >>>
    >>> # Calculate Kalshi-style fees
    >>> fee_model = BoundedProfitFeeModel(percent_of_profit=0.07, maximum_fee_cents=0.05)
    >>> fee = fee_model.calculate_fee(entry_cents=50.0, payout_cents=100.0)
"""

from backtest_harness.fee_models import (
    BoundedProfitFeeModel,
    FlatMakerTakerModel,
    FeeModel,
)
from backtest_harness.monte_carlo import MonteCarloSimulator

__version__ = "0.1.0"

__all__ = [
    "MonteCarloSimulator",
    "BoundedProfitFeeModel",
    "FlatMakerTakerModel",
    "FeeModel",
]
