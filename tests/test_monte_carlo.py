import numpy as np
import pytest

from backtest_harness.monte_carlo import MonteCarloSimulator


class TestMonteCarloSimulator:
    def test_positive_drift_no_ruin(self):
        returns = np.array([0.01, 0.02, 0.05, 0.03])
        stats = MonteCarloSimulator.simulate_equity_paths(
            trade_returns_pct=returns,
            starting_equity=1000.0,
            num_simulations=100,
            trades_per_sim=10,
        )
        assert stats["prob_ruin"] == pytest.approx(0.0)
        assert stats["p05_equity"] > 1000.0

    def test_negative_drift_high_ruin(self):
        returns = np.array([-0.30, -0.25, -0.20, -0.35])
        stats = MonteCarloSimulator.simulate_equity_paths(
            trade_returns_pct=returns,
            starting_equity=1000.0,
            num_simulations=200,
            trades_per_sim=50,
        )
        assert stats["prob_ruin"] > 0.5

    def test_output_keys_present(self):
        returns = np.array([0.01, -0.01])
        stats = MonteCarloSimulator.simulate_equity_paths(
            trade_returns_pct=returns, starting_equity=1000.0, num_simulations=50, trades_per_sim=10
        )
        assert "prob_ruin" in stats
        assert "p05_equity" in stats
        assert "p50_equity" in stats
        assert "p95_equity" in stats

    def test_single_trade_simulation(self):
        returns = np.array([0.10])
        stats = MonteCarloSimulator.simulate_equity_paths(
            trade_returns_pct=returns, starting_equity=1000.0, num_simulations=10, trades_per_sim=1
        )
        assert stats["p50_equity"] == pytest.approx(1100.0, rel=0.01)

    def test_array_boundaries_and_empty(self):
        # Empty array
        res = MonteCarloSimulator.simulate_equity_paths(np.array([]), 1000.0, 10, 10)
        assert res["prob_ruin"] == 0.0
        assert res["p50_equity"] == 1000.0

        # Zero num_simulations
        res2 = MonteCarloSimulator.simulate_equity_paths(np.array([0.1]), 1000.0, 0, 10)
        assert res2["prob_ruin"] == 0.0

        # Zero trades_per_sim
        res3 = MonteCarloSimulator.simulate_equity_paths(np.array([0.1]), 1000.0, 10, 0)
        assert res3["prob_ruin"] == 0.0

    def test_extreme_arrays(self):
        # All 0s
        res_zeros = MonteCarloSimulator.simulate_equity_paths(np.zeros(10), 1000.0, 10, 10)
        assert not np.isnan(res_zeros["prob_ruin"])
        assert res_zeros["p50_equity"] == 1000.0

        # Extreme negatives (-100%, -200%)
        res_neg = MonteCarloSimulator.simulate_equity_paths(
            np.array([-1.0, -2.0, -5.0]), 1000.0, 10, 10
        )
        assert not np.isnan(res_neg["prob_ruin"])
        assert not np.isnan(res_neg["p50_equity"])

        # Very large positives (should not raise NA/nan due to inf)
        res_pos = MonteCarloSimulator.simulate_equity_paths(
            np.array([1000.0, 10000.0]), 1000.0, 10, 250
        )
        assert not np.isnan(res_pos["prob_ruin"])
        assert not np.isnan(res_pos["p50_equity"])
        assert res_pos["prob_ruin"] == 0.0
