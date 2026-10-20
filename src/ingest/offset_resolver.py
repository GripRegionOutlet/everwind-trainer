from __future__ import annotations

import json
import logging
from pathlib import Path

log = logging.getLogger("everwind.ingest.offsets")


class OffsetResolver:
    """Loads versioned offsets and resolves pointer chains against a base address."""

    def __init__(self, offsets_path: str | Path, build: str):
        self.offsets_path = Path(offsets_path)
        self.build = build
        self._table: dict[str, dict] = {}
        self._load()

    def _load(self) -> None:
        if not self.offsets_path.exists():
            log.warning("no offsets file at %s — features will be disabled", self.offsets_path)
            return
        raw = json.loads(self.offsets_path.read_text(encoding="utf-8"))
        builds = raw.get("builds", {})
        if self.build in builds:
            self._table = builds[self.build]
            log.info("loaded %d offsets for build %s", len(self._table), self.build)
        else:
            log.warning("build %s not present in offsets table", self.build)

    def get(self, name: str) -> dict:
        if name not in self._table:
            raise KeyError(f"offset '{name}' missing for build {self.build}")
        return self._table[name]

    def chain(self, name: str) -> tuple[int, list[int]]:
        entry = self.get(name)
        return int(entry["base"], 16), [int(o, 16) for o in entry["offsets"]]