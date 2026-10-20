from __future__ import annotations

from typing import Any

from src.processors.base import Processor, StateSnapshot


class EspProcessor(Processor):
    """Computes screen-space boxes for players. Does no writes itself — emits overlay draw calls."""

    name = "esp"

    def __init__(self, max_distance: float = 300.0, color: str = "#ff3355"):
        self.max_distance = max_distance
        self.color = color

    def process(self, snap: StateSnapshot) -> list[dict[str, Any]]:
        draws: list[dict[str, Any]] = []
        px, py, pz = snap.position
        for ent in snap.entities:
            if ent.get("team") == "self":
                continue
            ex, ey, ez = ent.get("pos", (0.0, 0.0, 0.0))
            dist = ((ex - px) ** 2 + (ey - py) ** 2 + (ez - pz) ** 2) ** 0.5
            if dist > self.max_distance:
                continue
            draws.append({
                "kind": "box",
                "world_pos": (ex, ey, ez),
                "label": ent.get("name", "player"),
                "distance": round(dist, 1),
                "color": self.color,
            })
        return draws