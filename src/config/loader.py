from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml


@dataclass
class FeatureConfig:
    name: str
    enabled: bool = False
    hotkey: str | None = None
    options: dict[str, Any] = field(default_factory=dict)


@dataclass
class TrainerConfig:
    tick_ms: int = 50
    features: dict[str, FeatureConfig] = field(default_factory=dict)
    overlay_enabled: bool = True
    safe_mode: bool = True


def load_config(path: str | Path) -> TrainerConfig:
    raw = yaml.safe_load(Path(path).read_text(encoding="utf-8"))
    features = {
        key: FeatureConfig(
            name=key,
            enabled=bool(val.get("enabled", False)),
            hotkey=val.get("hotkey"),
            options=val.get("options", {}) or {},
        )
        for key, val in (raw.get("features") or {}).items()
    }
    return TrainerConfig(
        tick_ms=int(raw.get("tick_ms", 50)),
        features=features,
        overlay_enabled=bool(raw.get("overlay_enabled", True)),
        safe_mode=bool(raw.get("safe_mode", True)),
    )