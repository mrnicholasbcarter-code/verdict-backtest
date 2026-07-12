# AI Agent Constraints & Architectural Context (.claude.md)

**Target Ecosystem:** Statistical Validation & Portfolio Math
**Language:** Python 3.10+
**Primary Directive:** Mathematical rigor and Numpy optimization.

## Design Philosophy
- **NO PANDAS.** We use raw `numpy` arrays (`np.ndarray`) for Monte Carlo simulations. The overhead of DataFrame indexing kills simulation throughput at 10,000+ paths.
- **Pure Functions.** The `FeeModel` classes must remain pure.

## Safe Evaluation Parameters
When generating new simulated distributions or updating the `simulate_equity_paths` method, agents must ensure the returning dict strictly contains `prob_ruin`, `p05_equity`, `p50_equity`, and `p95_equity`. 

If generating PRs, add tests utilizing `pytest.approx()` to `tests/test_monte_carlo.py` to bound floating-point instability.
