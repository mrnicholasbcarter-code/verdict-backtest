# AGENTS.md Template

## Project overview

Describe the package, runtime, primary users, and safety boundaries.

## Repository map

```text
repo/
├── src/
├── tests/
├── docs/
└── .github/
```

## Agent protocols

- State which skills or swarms to use for broad changes.
- State forbidden edits and sensitive paths.
- State required checks before completion.

## Memory and coordination

- Private write namespace: `<tool>-kalshi-trader`.
- Shared namespace: `shared`.

## Testing checklist

List exact commands agents must run.
