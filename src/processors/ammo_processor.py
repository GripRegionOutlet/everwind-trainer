from __future__ import annotations

from src.processors.base import Processor, StateSnapshot


class AmmoProcessor(Processor):
    """Refills magazine or reserve, depending on options."""

    name = "ammo"

    def __init__(self, magazine_addr: int, reserve_addr: int,
                 reserve_only: bool = True, magazine_size: int = 30):
        self.magazine_addr = magazine_addr
        self.reserve_addr = reserve_addr
        self.reserve_only = reserve_only
        self.magazine_size = magazine_size

    def process(self, snap: StateSnapshot) -> list[dict]:
        intents: list[dict] = []
        mag = snap.ammo.get("magazine", 0)
        reserve = snap.ammo.get("reserve", 0)
        if not self.reserve_only and mag < self.magazine_size:
            intents.append({"address": self.magazine_addr, "fmt": "<i", "value": self.magazine_size})
        if reserve < 999:
            intents.append({"address": self.reserve_addr, "fmt": "<i", "value": 999})
        return intents