# Verdict Backtest — Monte Carlo Simulation Engine

[![CI](https://github.com/mrnicholasbcarter-code/verdict-backtest/actions/workflows/ci.yml/badge.svg)](https://github.com/mrnicholasbcarter-code/verdict-backtest/actions/workflows/ci.yml)
[![Lint](https://github.com/mrnicholasbcarter-code/verdict-backtest/actions/workflows/lint.yml/badge.svg)](https://github.com/mrnicholasbcarter-code/verdict-backtest/actions/workflows/lint.yml)
[![Python](https://img.shields.io/badge/python-3.10+-3776ab?logo=python&logoColor=white)](https://www.python.org/)
[![NumPy](https://img.shields.io/badge/numpy-vectorized-013243?logo=numpy)](https://numpy.org/)
[![Numba](https://img.shields.io/badge/numba-JIT-00A3E0?logo=numba)](https://numba.pydata.org/)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)

> Monte Carlo simulation engine for LLM routing strategy validation and prediction market alpha evaluation.

---

## Why This Exists

Traditional backtesters run a single linear equity curve. They tell you what *did* happen, not what *could* happen. This harness resamples the same return distribution into thousands of equity paths, using Numba for the path accumulation. It answers these questions:

- **What's the probability of ruin?** Not a guess. A distribution.
- **What do P5/P50/P95 equity paths look like after 250 trades?**
- **Does the edge survive a bounded-profit fee (Kalshi-style) or a maker-taker fee (Polymarket-style)?**

---

## What ships today

| Component | What it does | Source |
|-----------|--------------|--------|
| `MonteCarloSimulator` | Bootstrap-resamples a per-trade return series into many equity paths. The path accumulation is Numba-parallel (`@njit(parallel=True)`). Reports P5/P50/P95/mean final equity and probability of ruin (final equity below 50% of start). | `monte_carlo.py` |
| Fee models | `FeeModel` protocol, plus `BoundedProfitFeeModel` (percent of profit with a cap, Kalshi-style) and `FlatMakerTakerModel` (basis points, Polymarket-style). | `fee_models.py` |
| `tearsheet` | Total and annual return, volatility, Sharpe, Sortino, max drawdown, Calmar, win rate. | `analytics.py` |
| `split_walk_forward` | Expanding-window walk-forward index splits (no purging or embargo). | `analytics.py` |
| `run_counterfactual` | Seeded, reproducible evaluation. It combines Monte Carlo, tear sheet, walk-forward and optional fees into an evidence bundle with a Verdict provider receipt and `results_hash`. The same arguments give the same hash. | `evidence.py` |
| Evidence adapters | `build_failure_evidence`, `to_verification_result`, `to_evidence_chain_link` for Verdict evidence chains. | `evidence.py` |

Measured throughput: about 110,000 paths/s for 100,000 paths × 250 trades
(Linux x86-64 workstation, CPython 3.13, warm JIT). This is descriptive, not a guarantee.

---

## Quick start

The package (`llm-gate-backtest`, import `backtest_harness`) is not published to PyPI.
Install it from source:

```bash
git clone https://github.com/mrnicholasbcarter-code/verdict-backtest.git
cd verdict-backtest
uv sync --extra dev
uv run pytest -q
uv run --extra viz python examples/backtest_kalshi.py   # MC percentiles, tear sheet, walk-forward, equity-cone PNG
```

```python
from backtest_harness import run_counterfactual

evidence = run_counterfactual(
    run_id="demo",
    trade_returns=[0.04, -0.02, 0.03, -0.05, 0.06, 0.01, -0.03, 0.05, -0.01, 0.02],
    starting_equity=1_000.0,
    seed=42,
    dataset_ref="synthetic:demo-v1",
    num_simulations=5_000,
    trades_per_sim=250,
    walk_forward_splits=3,
    fee_config={"model": "bounded_profit", "percent_of_profit": 0.07, "maximum_fee_cents": 0.05},
    fee_trades=[(50.0, 100.0), (40.0, 100.0)],
)
mc = evidence["results"]["monte_carlo"]
print(f"P50 ${mc['p50_equity']:.2f}  ruin {mc['prob_ruin']:.2%}  hash {evidence['results_hash'][:19]}")
```

---

## Links

- **Verdict Core**: https://github.com/mrnicholasbcarter-code/verdict-core
- **Verdict Edge**: https://github.com/mrnicholasbcarter-code/verdict-strategy
- **Verdict Risk**: https://github.com/mrnicholasbcarter-code/verdict-risk

---

## License

MIT — see [LICENSE](LICENSE)
