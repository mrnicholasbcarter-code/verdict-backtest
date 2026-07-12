import pytest
import numpy as np
from backtest_harness.monte_carlo import MonteCarloSimulator

def test_monte_carlo_positive_drift():
    # Distribution strictly positive
    returns = np.array([0.01, 0.02, 0.05])
    
    stats = MonteCarloSimulator.simulate_equity_paths(
        trade_returns_pct=returns,
        starting_equity=1000.0,
        num_simulations=100,
        trades_per_sim=10
    )
    
    assert stats["prob_ruin"] == 0.0  # Impossible to ruin
    assert stats["p05_equity"] > 1000.0 # Strict growth guaranteed
