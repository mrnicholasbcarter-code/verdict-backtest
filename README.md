# Quantitative Backtest Harness

An event-driven backtester specifically written to handle the quirks of prediction markets and binary options, which break most standard equity/forex testing frameworks.

### Features
- **High-Fidelity Fee Models:** Natively implements percentage-of-profit fees, bounded fee ceilings, and maker/taker differentials.
- **Strict Chronological Replay:** Eliminates lookahead bias by streaming historical ticks through the identical risk gates used in production.
- **Monte Carlo Inference:** Shuffles historical path progressions to evaluate strategy robustness and return the 5th and 95th percentile expected equity curves.
