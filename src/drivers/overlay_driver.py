from __future__ import annotations

import logging
from typing import Any

log = logging.getLogger("everwind.drivers.overlay")


class OverlayDriver:
    """Placeholder overlay bridge. In 2026 builds the actual rendering lives
    in the companion `everwind-overlay` process; we just hand it draw calls
    over a local named pipe."""

    def __init__(self, pipe_name: r"\\.\pipe\everwind_overlay"):
        self.pipe_name = pipe_name
        self._connected = False

    def connect(self) -> bool:
        # Real impl uses win32file.CreateFile on the named pipe; stubbed for tests.
        log.info("overlay pipe target: %s", self.pipe_name)
        self._connected = True
        return True

    def submit(self, draws: list[dict[str, Any]]) -> None:
        if not self._connected:
            return
        for d in draws:
            log.debug("overlay draw: %s", d.get("label", d.get("kind")))