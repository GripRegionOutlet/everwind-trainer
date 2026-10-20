from __future__ import annotations

import logging
import time

from src.config.loader import TrainerConfig
from src.drivers.hotkey_driver import HotkeyDriver
from src.drivers.memory_writer import MemoryWriter
from src.drivers.overlay_driver import OverlayDriver
from src.ingest.memory_reader import MemoryReader
from src.ingest.offset_resolver import OffsetResolver
from src.ingest.process_scanner import ProcessScanner
from src.processors.ammo_processor import AmmoProcessor
from src.processors.base import StateSnapshot
from src.processors.health_processor import HealthProcessor

log = logging.getLogger("everwind.jobs.loop")


class TrainerLoop:
    """The worker: ingest → process → drive, every `tick_ms` milliseconds."""

    def __init__(self, config: TrainerConfig, process_name: str, dry_run: bool = False):
        self.config = config
        self.process_name = process_name
        self.dry_run = dry_run
        self._running = False
        self._scanner = ProcessScanner(process_name)
        self._writer: MemoryWriter | None = None
        self._reader: MemoryReader | None = None
        self._overlay = OverlayDriver()
        self._hotkeys = HotkeyDriver()
        self._processors = []

    def _build_pipeline(self) -> None:
        handle = self._scanner.attach()
        self._reader = MemoryReader(handle.process)
        self._writer = MemoryWriter(handle.process, dry_run=self.dry_run)
        resolver = OffsetResolver("offsets/current.json", build="2026.4")

        if self.config.features.get("godmode") or self.config.features.get("infinite_stamina"):
            try:
                h_base, h_chain = resolver.chain("player_health")
                s_base, s_chain = resolver.chain("player_stamina")
                self._processors.append(HealthProcessor(
                    health_addr=self._reader.read_pointer_chain(h_base, h_chain),
                    stamina_addr=self._reader.read_pointer_chain(s_base, s_chain),
                    godmode=self.config.features.get("godmode").enabled
                        if self.config.features.get("godmode") else False,
                    inf_stamina=self.config.features.get("infinite_stamina").enabled
                        if self.config.features.get("infinite_stamina") else False,
                ))
            except KeyError as exc:
                log.warning("health/stamina offsets missing: %s", exc)

        if self.config.features.get("infinite_ammo"):
            try:
                m_base, m_chain = resolver.chain("weapon_magazine")
                r_base, r_chain = resolver.chain("weapon_reserve")
                self._processors.append(AmmoProcessor(
                    magazine_addr=self._reader.read_pointer_chain(m_base, m_chain),
                    reserve_addr=self._reader.read_pointer_chain(r_base, r_chain),
                ))
            except KeyError as exc:
                log.warning("ammo offsets missing: %s", exc)

    def _snapshot(self) -> StateSnapshot:
        return StateSnapshot()  # populated by per-feature readers in full builds

    def run(self) -> None:
        self._build_pipeline()
        if self.config.overlay_enabled:
            self._overlay.connect()
        self._running = True
        tick = self.config.tick_ms / 1000.0
        log.info("trainer loop started (tick=%.0fms, dry_run=%s)",
                 self.config.tick_ms, self.dry_run)
        while self._running:
            snap = self._snapshot()
            for proc in self._processors:
                intents = proc.process(snap)
                if intents and self._writer is not None:
                    self._writer.apply(intents)
            time.sleep(tick)

    def stop(self) -> None:
        self._running = False
        self._hotkeys.unbind_all()
        self._scanner.detach()