"""Monte Carlo simulation engine for backtesting.

This module provides a high-performance Monte Carlo simulator using pure NumPy
matrix operations to randomly sample historical outcome distributions across
millions of parallel execution paths, establishing statistical confidence
intervals for trading strategies.
"""

import numpy as np
from numba import njit, prange


@njit(parallel=True, cache=True)
def _cumulative_product_numba(multipliers: np.ndarray, starting_equity: float) -> np.ndarray:
    """Numba-accelerated cumulative product along axis=1.

    Args:
        multipliers: 2D array of shape (num_simulations, trades_per_sim) with
            1 + return values.
        starting_equity: Initial equity value.

    Returns:
        2D array of same shape with cumulative equity paths.
    """
    num_simulations, trades_per_sim = multipliers.shape
    result = np.empty_like(multipliers)
    for i in prange(num_simulations):
        result[i, 0] = starting_equity * multipliers[i, 0]
        for j in range(1, trades_per_sim):
            result[i, j] = result[i, j - 1] * multipliers[i, j]
    return result


class MonteCarloSimulator:
    """Simulates variations of historical returns to establish statistical confidence intervals.

    This simulator uses pure NumPy matrix operations to randomly sample from
    historical return distributions (with replacement) and generate thousands
    of alternate universe equity curves. It computes key risk metrics including
    probability of ruin and percentile outcomes.
    """

    @staticmethod
    def simulate_equity_paths(
        trade_returns_pct: np.ndarray,
        starting_equity: float,
        num_simulations: int = 1000,
        trades_per_sim: int = 250,
    ) -> dict:
        """Randomly samples from historical return distribution to generate equity curves.

        This method creates `num_simulations` independent equity paths, each
        consisting of `trades_per_sim` trades randomly sampled (with replacement)
        from the provided historical returns. It then computes percentiles
        and probability of ruin across all paths.

        Args:
            trade_returns_pct: 1D NumPy array of historical trade returns as
                percentages (e.g., 0.05 for 5% gain, -0.10 for 10% loss).
            starting_equity: Initial equity in base currency units.
            num_simulations: Number of independent Monte Carlo paths to generate
                (default: 1000).
            trades_per_sim: Number of trades per simulation path (default: 250).

        Returns:
            Dictionary containing:
            - p05_equity: 5th percentile final equity (worst-case scenario).
            - p50_equity: 50th percentile (median) final equity.
            - p95_equity: 95th percentile final equity (best-case scenario).
            - mean_equity: Mean final equity across all simulations.
            - prob_ruin: Probability of equity dropping below 50% of starting value.
            - used_numba: Whether Numba acceleration was used.

        Examples:
            >>> import numpy as np
            >>> returns = np.array([0.05, -0.10, 0.02, 0.15, -0.05])
            >>> stats = MonteCarloSimulator.simulate_equity_paths(
            ...     returns, starting_equity=1000.0, num_simulations=5000, trades_per_sim=250
            ... )
            >>> print(f"Risk of Ruin: {stats['prob_ruin'] * 100:.1f}%")
        """
        if num_simulations <= 0 or trades_per_sim <= 0 or trade_returns_pct.size == 0:
            return {
                "p05_equity": float(starting_equity),
                "p50_equity": float(starting_equity),
                "p95_equity": float(starting_equity),
                "mean_equity": float(starting_equity),
                "prob_ruin": 0.0,
                "used_numba": False,
            }

        # Shape: (num_simulations, trades_per_sim)
        simulated_returns = np.random.choice(
            trade_returns_pct, size=(num_simulations, trades_per_sim), replace=True
        )

        # Convert returns to equity multipliers (+1.0)
        multipliers = 1.0 + simulated_returns

        # Use numba accelerated cumulative product
        cumulative_paths = _cumulative_product_numba(multipliers, starting_equity)

        # Final equities across all paths
        final_equities = cumulative_paths[:, -1]

        # Replace nans (from 0 * inf) with 0.0 since hitting 0 should just stay 0
        final_equities = np.nan_to_num(
            final_equities, nan=0.0, posinf=np.inf, neginf=-np.inf
        )

        # Determine percentiles ignoring remaining potential nan issues,
        # using nearest to avoid inf-inf=nan
        return {
            "p05_equity": float(np.percentile(final_equities, 5, method="nearest")),
            "p50_equity": float(np.percentile(final_equities, 50, method="nearest")),
            "p95_equity": float(np.percentile(final_equities, 95, method="nearest")),
            "mean_equity": float(np.mean(final_equities)),
            "prob_ruin": float(
                np.mean(final_equities < (starting_equity * 0.5))
            ),  # <50% loss condition
            "used_numba": True,
        }

    @staticmethod
    def equity_paths(
        trade_returns_pct: np.ndarray,
        starting_equity: float,
        num_simulations: int = 1000,
        trades_per_sim: int = 250,
    ) -> np.ndarray:
        """Generate full equity paths for visualization.

        Returns the complete matrix of equity values at each step for each
        simulation path.

        Args:
            trade_returns_pct: 1D NumPy array of historical trade returns.
            starting_equity: Initial equity in base currency units.
            num_simulations: Number of independent Monte Carlo paths.
            trades_per_sim: Number of trades per simulation path.

        Returns:
            2D array of shape (num_simulations, trades_per_sim) with equity values.
        """
        if num_simulations <= 0 or trades_per_sim <= 0 or trade_returns_pct.size == 0:
            return np.empty((0, trades_per_sim))

        simulated_returns = np.random.choice(
            trade_returns_pct, size=(num_simulations, trades_per_sim), replace=True
        )
        multipliers = 1.0 + simulated_returns
        cumulative_paths = _cumulative_product_numba(multipliers, starting_equity)
        return cumulative_paths