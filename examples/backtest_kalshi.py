"""Example backtest for Kalshi bounded-profit fee logic.

The script demonstrates a single-step, one-year Monte-Carlo backtest that
generates synthetic trade data, runs 10k Monte-Carlo paths, prints a few
percentile values and risk-of-ruin, creates an equity-cone PNG and writes
a formatted tear-sheet.

The Kalshi fee model charges 7% of gross profit, capped at 5 cents.
This is unique among backtesters - most assume fixed maker/taker fees.
"""

import numpy as np
import matplotlib.pyplot as plt

from backtest_harness import MonteCarloSimulator, BoundedProfitFeeModel, tearsheet
from backtest_harness.analytics import split_walk_forward

# Kalshi bounded-profit fee model: 7% of gross profit, max 5 cents
FEE_MODEL = BoundedProfitFeeModel(percent_of_profit=0.07, maximum_fee_cents=0.05)

# Trade parameters (realistic Kalshi prediction market scenario)
# Entry price: 50 cents - buying at fair value
# True probability: 55% - we have an edge
ENTRY = 0.50
PAYOUT_WIN = 1.00

# Calculate net return after fees
gross_profit_win = PAYOUT_WIN - ENTRY  # 0.50
fee_on_win = FEE_MODEL.calculate_fee(entry_cents=ENTRY * 100, payout_cents=PAYOUT_WIN * 100)  # 7% of 0.50 = 0.035
net_profit_win = gross_profit_win - fee_on_win  # 0.50 - 0.035 = 0.465
win_return = net_profit_win / ENTRY  # 0.465 / 0.50 = 93%

# Loss: lose the entire entry amount
loss_return = -1.0  # lose 100% of stake

# Win probability: 55% (our edge)
WIN_PROB = 0.55
N_TRADES = 50  # Reduced number of trades for reasonable demo

np.random.seed(42)
draws = np.where(np.random.rand(N_TRADES) < WIN_PROB, win_return, loss_return)

# Run Monte Carlo with 10,000 paths
stats = MonteCarloSimulator.simulate_equity_paths(
    trade_returns_pct=draws,
    starting_equity=1000.0,
    num_simulations=10_000,
    trades_per_sim=len(draws),
)

print("Monte Carlo equity percentiles:")
for key in ["p05_equity", "p50_equity", "p95_equity"]:
    print(f"  {key:>10}: ${stats[key]:,.2f}")
print(f"  Risk of Ruin (<=0.5x initial): {stats['prob_ruin']*100:.2f}%")
print(f"  Numba backend used: {stats.get('used_numba', 'N/A')}")

# Build equity cone from actual simulated paths
paths = MonteCarloSimulator.equity_paths(
    trade_returns_pct=draws,
    starting_equity=1000.0,
    num_simulations=10_000,
    trades_per_sim=len(draws),
)

final = paths[:, -1]
cone_vals = [np.percentile(final, p) for p in [5, 50, 95]]

X = np.arange(len(draws))
plt.figure(figsize=(8, 4))
plt.plot(X, [cone_vals[1]] * len(X), "k-", lw=2, label="Median (P50)")
plt.fill_between(X, [cone_vals[0]] * len(X), [cone_vals[2]] * len(X),
                 color="steelblue", alpha=0.3, label="P5-P95")
plt.title("Equity Cone - Kalshi Backtest (10k Paths)")
plt.xlabel("Trade Number")
plt.ylabel("Equity (USD)")
plt.legend()
plt.tight_layout()
plt.savefig("/home/nick/backtest-harness/examples/equity_cone.png")
plt.close()
print("Saved equity_cone.png to examples/")

# Tear-sheet
sheet = tearsheet(draws, periods_per_year=252)  # Annualized assuming daily frequency
print("\nTear-sheet:")
for k, v in sheet.items():
    print(f"   {k:<12}: {v:.4f}")

# Walk-forward demo
print("\nWalk-forward splits (n_splits=3):")
for i, (train_idx, test_idx) in enumerate(split_walk_forward(draws, n_splits=3)):
    print(f"  Split {i+1}: train {len(train_idx)} / test {len(test_idx)}")