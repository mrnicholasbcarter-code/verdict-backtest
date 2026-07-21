# Contributing

Thanks for improving `verdict-backtest`. The released distribution is
`verdict-backtest`; the compatible Python namespace remains
`backtest_harness`. This repo is intentionally small, auditable, and
test-first.

## Local setup

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -U pip
python -m pip install -e '.[dev]'
```

## Development workflow

1. Open an issue or comment on an existing one for non-trivial changes.
2. Create a focused branch.
3. Add or update tests for behavior changes.
4. Run validation locally.
5. Open a PR using the template.

## Required checks

```bash
python -m pytest
python -m compileall src tests
python -m build
```

## Pull request expectations

- Keep changes scoped and reviewable.
- Explain strategy/backtesting assumptions in the PR body.
- Include before/after examples for API or behavior changes.
- Do not include secrets, market-data dumps, broker credentials, or personal account information.

## Code style

- Python 3.10+.
- Prefer explicit types and short docstrings for public APIs.
- Keep modules focused.
- Validate inputs at package boundaries.
- Avoid nondeterministic tests unless randomness is seeded or mocked.
