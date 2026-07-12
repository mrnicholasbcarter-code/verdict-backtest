# AGENTS.md

## Project overview

`backtest-harness` is a small Python package for event-driven prediction-market backtesting. It focuses on fee realism, chronological replay, and Monte Carlo robustness checks for binary-option strategies.

## Repository map

```text
backtest-harness/
├── src/backtest_harness/
│   ├── fee_models.py      # Fee model protocols and concrete fee calculators
│   └── monte_carlo.py     # Monte Carlo equity-path simulation utilities
├── tests/                 # Pytest regression tests
├── docs/                  # Architecture, release, and maintainer documentation
├── templates/             # Reusable docs/config templates for ecosystem repos
├── .github/               # Issue/PR templates and CI/release workflows
├── pyproject.toml         # Package metadata and tool configuration
└── README.md              # Developer-facing landing page
```

## Agent protocols

1. Prefer small, typed, test-backed changes in `src/backtest_harness`.
2. Keep public APIs stable unless a task explicitly requires a breaking change.
3. Do not commit secrets, `.env` files, credentials, notebook outputs, or large market-data captures.
4. Do not add generated artifacts to source control unless they are required documentation outputs.
5. Use `/swarm-orchestration` or a hierarchical swarm for broad changes touching 3+ areas such as source, tests, docs, and CI.
6. Use `/security-audit` for changes involving credentials, broker APIs, order execution, file loading, or path handling.
7. Use `/performance-analysis` for simulation hot paths, large arrays, or benchmark regressions.

## Memory and coordination

- Codex/Jcode-owned memory writes should use the `codex-kalshi-trader` namespace.
- Cross-tool findings intended for all agents may be written to `shared`.
- Read/search may fan out across `codex-kalshi-trader`, `shared`, `project-docs`, `tradememory`, `claude-mem`, `claude-memory`, and `lessons`.
- Record reusable patterns, not transient logs.

## Testing enforcement checklist

Before claiming completion, agents must run the narrowest relevant checks and report them:

```bash
python -m pytest
python -m compileall src tests
python -m build
```

For docs-only changes, at minimum inspect links and ensure Markdown examples remain accurate. For workflow changes, validate YAML syntax or explain why external GitHub validation was not available locally.

## Code standards

- Python 3.10+.
- Keep modules focused and under 500 lines when practical.
- Validate user-controlled inputs at boundaries.
- Prefer deterministic simulations in tests by seeding or monkeypatching randomness.
- Public functions and classes should have concise docstrings.
- Avoid hidden network calls in tests.
