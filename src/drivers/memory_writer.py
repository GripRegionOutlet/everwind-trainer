from __future__ import annotations

import logging
import struct

import pymem
import pymem.memory

log = logging.getLogger("everwind.drivers.memory")


class MemoryWriter:
    """Applies write intents emitted by processors. Honours dry-run mode."""

    def __init__(self, process: pymem.Pymem, dry_run: bool = False):
        self._pm = process
        self.dry_run = dry_run

    def apply(self, intents: list[dict]) -> int:
        applied = 0
        for intent in intents:
            addr = intent["address"]
            fmt = intent["fmt"]
            value = intent["value"]
            if self.dry_run:
                log.debug("[dry-run] would write %s -> 0x%x", value, addr)
                applied += 1
                continue
            try:
                data = struct.pack(fmt, value)
                pymem.memory.write_bytes(self._pm.process_handle, addr, data, len(data))
                applied += 1
            except Exception as exc:  # noqa: BLE001
                log.warning("write failed at 0x%x: %s", addr, exc)
        return applied