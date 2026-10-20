from __future__ import annotations

import logging
import time
from dataclasses import dataclass

import pymem
import pymem.process

log = logging.getLogger("everwind.ingest.scanner")


@dataclass
class ProcessHandle:
    pid: int
    base_address: int
    process: pymem.Pymem


class ProcessScanner:
    """Locates the Everwind process and resolves the main module base."""

    def __init__(self, process_name: str = "Everwind.exe", retries: int = 30):
        self.process_name = process_name
        self.retries = retries
        self._handle: ProcessHandle | None = None

    def attach(self) -> ProcessHandle:
        for attempt in range(1, self.retries + 1):
            try:
                pm = pymem.Pymem(self.process_name)
                module = pymem.process.module_from_name(pm.process_handle, self.process_name)
                if module is None:
                    raise RuntimeError("main module not found")
                log.info("attached to %s pid=%d base=0x%x",
                         self.process_name, pm.process_id, module.lpBaseOfDll)
                self._handle = ProcessHandle(
                    pid=pm.process_id,
                    base_address=module.lpBaseOfDll,
                    process=pm,
                )
                return self._handle
            except Exception as exc:  # noqa: BLE001
                log.debug("attach attempt %d/%d failed: %s", attempt, self.retries, exc)
                time.sleep(1.0)
        raise RuntimeError(f"could not attach to {self.process_name} after {self.retries}s")

    @property
    def handle(self) -> ProcessHandle:
        if self._handle is None:
            raise RuntimeError("not attached; call attach() first")
        return self._handle

    def detach(self) -> None:
        self._handle = None