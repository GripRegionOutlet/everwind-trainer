from __future__ import annotations

from src.processors.base import Processor, StateSnapshot


class HealthProcessor(Processor):
    """Implements godmode + infinite stamina by pinning values each tick."""

    name = "health"

    def __init__(self, health_addr: int, stamina_addr: int,
                 godmode: bool = False, inf_stamina: bool = False):
        self.health_addr = health_addr
        self.stamina_addr = stamina_addr
        self.godmode = godmode
        self.inf_stamina = inf_stamina

    def process(self, snap: StateSnapshot) -> list[dict]:
        intents: list[dict] = []
        if self.godmode and snap.max_health > 0 and snap.health < snap.max_health:
            intents.append({"address": self.health_addr, "fmt": "<f", "value": snap.max_health})
        if self.inf_stamina and snap.stamina < 100.0:
            intents.append({"address": self.stamina_addr, "fmt": "<f", "value": 100.0})
        return intents