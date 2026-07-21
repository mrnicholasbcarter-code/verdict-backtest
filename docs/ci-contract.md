# CI dependency contract

The backtest package declares two optional extras: `dev` for tests, Ruff,
mypy, and Code Review Graph, and `viz` for optional plotting. CI installs
`.[dev]` for the test matrix and `.[dev,viz]` for lint/typecheck. It does not
request undeclared `test` or `all` extras and does not fall back to tools that
are unavailable to a later shell step.

The package gate is complete only when the matrix tests, lint, format,
typecheck, build, and `twine check` run in the environment that installed the
declared dependencies. The package job also installs the wheel and source
distribution into isolated environments and imports `backtest_harness` from
each artifact, catching package-boundary regressions that editable installs can
hide.
