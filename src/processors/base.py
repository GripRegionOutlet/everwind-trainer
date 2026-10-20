from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any


@dataclass
class StateSnapshot:
    """Immutable-ish view of the player state read from the process this tick."""
    player_ptr: int = 0
    health: float = 0.0
    max_health: float = 0.0
    stamina: float = 0.0
    ammo: dict[str, int] = field(default_factory=dict)
    position: tuple[float, float, float] = (0.0, 0.0, 0.0)
    entities: list[dict[str, Any]] = field(default_factory=list)


class Processor(ABC):
    """A processor takes a StateSnapshot and emits write intents."""

    name: str = "processor"

    @abstractmethod
    def process(self, snap: StateSnapshot) -> list[dict[str, Any]]:
        """Return a list of write intents: {address, fmt, value}."""