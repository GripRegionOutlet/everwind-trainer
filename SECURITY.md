# Security Policy

## Supported Versions

| Version | Supported |
|---------|-----------|
| 2026.x  | ✅        |
| 2025.x  | ❌        |

## Reporting a Vulnerability

Everwind Trainer reads and writes memory of another process. That means
any bug in the reader (`src/ingest/memory_reader.py`) or the offset
resolver (`src/ingest/offset_resolver.py`) can cause the game to crash
or corrupt saves. If you find one of those, **do not open a public
issue** — email the maintainer listed in `pyproject.toml` with:

- Everwind build number
- Which feature was enabled
- A minimal repro (config snippet + log excerpt)

We aim to ack within 72 hours.

## Out of scope

- Anti-cheat detection reports on official servers — that's expected.
- "My account got banned" — use at your own risk, see the README.
- Requests to make the injector signature-evading — PRs welcome but
  we won't discuss specifics in issues.