# Quantitative Backtest Harness

Event-driven backtesting primitives for prediction markets and binary options. The package models exchange-specific fees, replays strategy paths without lookahead bias, and stress-tests outcome distributions with Monte Carlo simulation.

## Why this exists

Standard equity and crypto backtesters often misprice prediction-market strategies because binary contracts have bounded payouts, unusual fee schedules, and path-dependent liquidity. `backtest-harness` keeps those mechanics explicit so strategy results are easier to audit before they touch production trading systems.

## Features

- **High-fidelity fee models** for percentage-of-profit caps and maker/taker fees.
- **Strict chronological replay orientation** for avoiding lookahead bias in strategy evaluation.
- **Monte Carlo inference** for 5th, 50th, and 95th percentile terminal equity estimates.
- **Small composable API** designed for agent-driven extension and review.

## Quickstart

```bash
git clone https://github.com/<owner>/backtest-harness.git
cd backtest-harness
python -m venv .venv
source .venv/bin/activate
python -m pip install -U pip
python -m pip install -e '.[dev]'
python -m pytest
```

## Minimal examples

### Fee modeling

```python
from backtest_harness.fee_models import BoundedProfitFeeModel, FlatMakerTakerModel

kalshi_like = BoundedProfitFeeModel(percent_of_profit=0.07, maximum_fee_cents=0.05)
assert kalshi_like.calculate_fee(entry_cents=40, payout_cents=100) == 0.05

clob = FlatMakerTakerModel(maker_bps=0.0, taker_bps=0.001)
assert clob.calculate_fee(trade_volume=1_000, is_maker=False) == 1.0
```

### Monte Carlo robustness

```python
import numpy as np
from backtest_harness.monte_carlo import MonteCarloSimulator

returns = np.array([0.03, -0.02, 0.01, 0.04, -0.01])
stats = MonteCarloSimulator.simulate_equity_paths(
    returns,
    starting_equity=10_000,
    num_simulations=1_000,
    trades_per_sim=250,
)
print(stats["p05_equity"], stats["p50_equity"], stats["p95_equity"])
```

## System flow

```mermaid
flowchart LR
    A[Historical market data] --> B[Chronological replay]
    B --> C[Strategy signals]
    C --> D[Fee models]
    D --> E[Equity curve]
    E --> F[Monte Carlo simulator]
    F --> G[Risk percentiles and ruin probability]
```

## Documentation

- [Architecture](docs/ARCHITECTURE.md)
- [Release process](docs/RELEASES.md)
- [Contributing](CONTRIBUTING.md)
- [Security policy](SECURITY.md)
- [Agent context](AGENTS.md)

## Development

```bash
python -m pip install -e '.[dev]'
python -m pytest
python -m compileall src tests
python -m build
```

## Release automation

Pushing a tag like `v0.1.1` runs `.github/workflows/release.yml`, builds distributions, generates changelog notes from merged PRs/commits, and publishes a GitHub Release artifact.

## License

MIT.
