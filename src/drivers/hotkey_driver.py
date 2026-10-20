from __future__ import annotations

import logging
from typing import Callable

import keyboard

log = logging.getLogger("everwind.drivers.hotkey")


class HotkeyDriver:
    """Registers feature hotkeys from the config table onto the keyboard hook."""

    def __init__(self):
        self._bindings: dict[str, Callable[[], None]] = {}

    def bind(self, hotkey: str, callback: Callable[[], None]) -> None:
        try:
            keyboard.add_hotkey(hotkey.lower(), callback)
            self._bindings[hotkey] = callback
            log.info("bound hotkey %s", hotkey)
        except Exception as exc:  # noqa: BLE001
            log.warning("failed to bind hotkey %s: %s", hotkey, exc)

    def unbind_all(self) -> None:
        for hk in list(self._bindings):
            keyboard.remove_hotkey(hk)
        self._bindings.clear()