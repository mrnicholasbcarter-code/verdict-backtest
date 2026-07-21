# Architecture

`verdict-backtest` provides focused primitives that can be composed by larger
trading research systems. The compatible Python import namespace is
`backtest_harness`.

## Core modules

| Module | Responsibility |
| --- | --- |
| `backtest_harness.fee_models` | Protocol and implementations for exchange fee calculations. |
| `backtest_harness.monte_carlo` | Equity-path sampling and risk percentile estimation. |

## Data flow

```mermaid
sequenceDiagram
    participant Data as Historical Data
    participant Replay as Chronological Replay
    participant Strategy as Strategy Logic
    participant Fees as Fee Model
    participant Equity as Equity Curve
    participant MC as Monte Carlo

    Data->>Replay: Ordered ticks/events
    Replay->>Strategy: Current market state only
    Strategy->>Fees: Executed trade details
    Fees-->>Strategy: Realistic fee impact
    Strategy->>Equity: Net return stream
    Equity->>MC: Historical returns
    MC-->>Equity: Percentiles and ruin probability
```

## Ecosystem context

```mermaid
flowchart TD
    PM[prediction-market-sdk] --> BH[verdict-backtest]
    BH --> EM[edge-mining-framework]
    BH --> RE[trade-risk-engine]
    EM --> KT[kalshi-trader]
    RE --> KT
    KT --> UI[trading-cockpit-ui]
    LLM[verdict] --> KT
```

## Design principles

- **Auditability over cleverness**: Backtest assumptions should be inspectable.
- **Determinism in tests**: Randomized simulations must be seeded or monkeypatched.
- **Composable boundaries**: Fee models and simulation utilities should remain easy to use independently.
- **No hidden live trading**: This package must not place orders or call broker APIs.
