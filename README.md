# Verdict Backtest — Monte Carlo Simulation Engine

[![CI](https://github.com/verdict/verdict-backtest/actions/workflows/ci.yml/badge.svg)](https://github.com/verdict/verdict-backtest/actions/workflows/ci.yml)
[![Lint](https://github.com/verdict/verdict-backtest/actions/workflows/lint.yml/badge.svg)](https://github.com/verdict/verdict-backtest/actions/workflows/lint.yml)
[![Python](https://img.shields.io/badge/python-3.10+-3776ab?logo=python&logoColor=white)](https://www.python.org/)
[![NumPy](https://img.shields.io/badge/numpy-vectorized-013243?logo=numpy)](https://numpy.org/)
[![Numba](https://img.shields.io/badge/numba-JIT-00A3E0?logo=numba)](https://numba.pydata.org/)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)

> Monte Carlo simulation engine for LLM routing strategy validation and prediction market alpha evaluation.

---

## Why This Exists

Traditional backtesters run a single linear equity curve. They tell you what *did* happen, not what *could* happen. This harness uses Numba-accelerated Monte Carlo simulation to generate thousands of parallel equity paths from the same return distribution, answering the questions that matter:

- **What's the probability of ruin?** Not a guess. A distribution.
- **What do P5/P50/P95 equity paths look like after 250 trades?**
- **Does the edge survive after Kalshi's 7% bounded-profit fee or Polymarket's maker-taker spread?**

---

## Features

| Feature | Description |
|---------|-------------|
| **Monte Carlo Engine** | Numba `@njit(parallel=True)` for millions of equity paths per second |
| **Fee Models** | Pluggable `FeeModel` protocol. Ships with Kalshi bounded-profit and Polymarket flat maker-taker |
| **Tearsheet Analytics** | Sharpe, Sortino, Calmar, max drawdown, win rate, total return, VaR/CVaR |
| **Walk-Forward Validation** | Expanding/rolling window with purging/embargoing |
| **Edge Mining Integration** | Native `verdict-edge` signal evaluation under friction |
| **Reproducible** | Deterministic seeds, versioned configs, artifact hashing |

---

## Quick Start

```bash
# Install
pipx install verdict-backtest

# Run a quick backtest
verdict-backtest run --config config/kalshi_default.yaml --paths 10000 --seed 42
```

## Configuration

```yaml
# config/kalshi_default.yaml
engine:
  paths: 50000
  trades: 250
  seed: 42

strategy:
  win_rate: 0.58
  avg_win: 0.012
  avg_loss: -0.008
  fee_model: "kalshi_bounded"

validation:
  walk_forward:
    window: 100
    step: 25
    purge: 5
    embargo: 5
```

---

## Links

- **Verdict Core**: https://github.com/verdict/verdict-core
- **Verdict Edge**: https://github.com/verdict/verdict-edge
- **Verdict Risk**: https://github.com/verdict/verdict-risk
- **RuVector**: https://github.com/ruvnet/ruvector

---

## License

MIT — see [LICENSE](LICENSE)
