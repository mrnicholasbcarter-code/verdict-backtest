# Release Process

This repository uses tag-triggered GitHub Releases.

## Versioning

Use semantic versioning:

- `MAJOR` for breaking API changes.
- `MINOR` for backward-compatible features.
- `PATCH` for bug fixes and documentation corrections.

## Cutting a release

```bash
git checkout master
git pull --ff-only
python -m pytest
python -m build
git tag vX.Y.Z
git push origin vX.Y.Z
```

The release workflow will:

1. Run tests.
2. Build source and wheel distributions.
3. Generate release notes.
4. Publish a GitHub Release with distribution artifacts.

## Changelog discipline

Use conventional commit prefixes where practical: `feat`, `fix`, `docs`, `test`, `chore`, `refactor`, and `perf`.
