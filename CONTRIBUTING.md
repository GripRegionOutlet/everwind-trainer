# Contributing to Everwind Trainer

Thanks for wanting to help out. A few ground rules before you open a PR.

## Setup

1. Install Python 3.11+ (64-bit — the game process is x64, 32-bit won't attach).
2. `pip install -r requirements.txt`
3. Drop your locally dumped offset table into `offsets/current.json` (see `offsets/README` inside that folder — do not commit offsets you didn't dump yourself).
4. Run `python -m src.main --dry-run` first — this validates the pipeline without writing memory.

## Code layout

- `src/ingest/` — anything that reads from the game (proc scan, module walker, memory reader).
- `src/processors/` — logic that transforms ingested snapshots into trainer state (godmode, inf stamina, etc).
- `src/drivers/` — output side. Each driver writes back to the process or to an overlay.
- `src/jobs/` — the worker loop that wires ingest → process → drive.

If you're adding a new cheat feature, you almost always want:
- one processor in `src/processors/`
- one driver if it needs to write memory
- an entry in `src/config/features.yaml`

## Style

- Black formatting, 100 char lines.
- Type hints on public functions.
- No hardcoded offsets — pull from `offsets/current.json` or the resolver.

## Testing

`pytest tests/ -v` — the process tests run against a mock memory backend and don't need the game running.

## PRs

Squash your commits. Describe what offsets changed if applicable. Don't bump the version — maintainers do that at release.