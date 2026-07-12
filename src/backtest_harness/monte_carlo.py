"""Monte Carlo simulation engine for backtesting.

This module provides a high-performance Monte Carlo simulator using pure NumPy
matrix operations to randomly sample historical outcome distributions across
millions of parallel execution paths, establishing statistical confidence
intervals for trading strategies.
"""

import numpy as np


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
            }

        # Shape: (num_simulations, trades_per_sim)
        simulated_returns = np.random.choice(
            trade_returns_pct, size=(num_simulations, trades_per_sim), replace=True
        )

        # Convert returns to equity multipliers (+1.0)
        multipliers = 1.0 + simulated_returns

        with np.errstate(over="ignore", invalid="ignore"):
            # Compute cumulative paths
            # Use float64 precision and safely handle overflows/nans
            cumulative_paths = starting_equity * np.cumprod(multipliers, axis=1)

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
        }