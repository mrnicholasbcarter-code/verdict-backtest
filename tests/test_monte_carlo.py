import numpy as np

from backtest_harness.monte_carlo import MonteCarloSimulator


def test_simulate_equity_paths_returns_expected_keys_for_flat_returns() -> None:
    returns = np.array([0.0])

    stats = MonteCarloSimulator.simulate_equity_paths(
        returns,
        starting_equity=100.0,
        num_simulations=5,
        trades_per_sim=3,
    )

    assert stats == {
        "p05_equity": 100.0,
        "p50_equity": 100.0,
        "p95_equity": 100.0,
        "mean_equity": 100.0,
        "prob_ruin": 0.0,
    }
