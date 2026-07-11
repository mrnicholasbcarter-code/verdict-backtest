import numpy as np

class MonteCarloSimulator:
    """
    Simulates variations of historical returns to establish statistical confidence intervals.
    """
    @staticmethod
    def simulate_equity_paths(
        trade_returns_pct: np.ndarray, 
        starting_equity: float, 
        num_simulations: int = 1000, 
        trades_per_sim: int = 250
    ) -> dict:
        """
        Randomly samples from the historical return distribution (with replacement)
        to generate thousands of alternate universe equity curves.
        """
        # Shape: (num_simulations, trades_per_sim)
        simulated_returns = np.random.choice(trade_returns_pct, size=(num_simulations, trades_per_sim), replace=True)
        
        # Convert returns to equity multipliers (+1.0)
        multipliers = 1.0 + simulated_returns
        
        # Compute cumulative paths
        cumulative_paths = starting_equity * np.cumprod(multipliers, axis=1)
        
        # Final equities across all paths
        final_equities = cumulative_paths[:, -1]
        
        return {
            "p05_equity": np.percentile(final_equities, 5),
            "p50_equity": np.percentile(final_equities, 50),
            "p95_equity": np.percentile(final_equities, 95),
            "mean_equity": np.mean(final_equities),
            "prob_ruin": np.mean(final_equities < (starting_equity * 0.5)) # <50% loss condition
        }
