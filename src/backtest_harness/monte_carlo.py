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
        if num_simulations <= 0 or trades_per_sim <= 0 or trade_returns_pct.size == 0:
            return {
                "p05_equity": float(starting_equity),
                "p50_equity": float(starting_equity),
                "p95_equity": float(starting_equity),
                "mean_equity": float(starting_equity),
                "prob_ruin": 0.0
            }

        # Shape: (num_simulations, trades_per_sim)
        simulated_returns = np.random.choice(trade_returns_pct, size=(num_simulations, trades_per_sim), replace=True)
        
        # Convert returns to equity multipliers (+1.0)
        multipliers = 1.0 + simulated_returns
        
        with np.errstate(over='ignore', invalid='ignore'):
            # Compute cumulative paths
            # Use float64 precision and safely handle overflows/nans
            cumulative_paths = starting_equity * np.cumprod(multipliers, axis=1)
            
            # Final equities across all paths
            final_equities = cumulative_paths[:, -1]
            
            # Replace nans (from 0 * inf) with 0.0 since hitting 0 should just stay 0
            final_equities = np.nan_to_num(final_equities, nan=0.0, posinf=np.inf, neginf=-np.inf)
        
        # Determine percentiles ignoring remaining potential nan issues, using nearest to avoid inf-inf=nan
        return {
            "p05_equity": float(np.percentile(final_equities, 5, method='nearest')),
            "p50_equity": float(np.percentile(final_equities, 50, method='nearest')),
            "p95_equity": float(np.percentile(final_equities, 95, method='nearest')),
            "mean_equity": float(np.mean(final_equities)),
            "prob_ruin": float(np.mean(final_equities < (starting_equity * 0.5))) # <50% loss condition
        }
