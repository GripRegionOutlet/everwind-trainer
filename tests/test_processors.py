from src.processors.base import StateSnapshot
from src.processors.health_processor import HealthProcessor
from src.processors.ammo_processor import AmmoProcessor


def test_godmode_writes_max_health_when_damaged():
    proc = HealthProcessor(health_addr=0x1000, stamina_addr=0x2000, godmode=True)
    snap = StateSnapshot(health=40.0, max_health=100.0, stamina=80.0)
    intents = proc.process(snap)
    assert len(intents) == 1
    assert intents[0]["address"] == 0x1000
    assert intents[0]["value"] == 100.0


def test_godmode_noop_when_full():
    proc = HealthProcessor(health_addr=0x1000, stamina_addr=0x2000, godmode=True)
    snap = StateSnapshot(health=100.0, max_health=100.0)
    assert proc.process(snap) == []


def test_ammo_reserve_only_skips_magazine():
    proc = AmmoProcessor(magazine_addr=0x10, reserve_addr=0x20, reserve_only=True)
    snap = StateSnapshot(ammo={"magazine": 5, "reserve": 10})
    intents = proc.process(snap)
    assert all(i["address"] == 0x20 for i in intents)


def test_ammo_fills_magazine_when_not_reserve_only():
    proc = AmmoProcessor(magazine_addr=0x10, reserve_addr=0x20,
                        reserve_only=False, magazine_size=30)
    snap = StateSnapshot(ammo={"magazine": 3, "reserve": 999})
    intents = proc.process(snap)
    assert any(i["address"] == 0x10 and i["value"] == 30 for i in intents)