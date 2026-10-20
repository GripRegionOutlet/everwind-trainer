import json
from pathlib import Path

from src.ingest.offset_resolver import OffsetResolver


def _write_offsets(tmp_path: Path) -> Path:
    p = tmp_path / "current.json"
    p.write_text(json.dumps({
        "builds": {
            "2026.4": {
                "player_health": {"base": "0xDEADBEEF", "offsets": ["0x10", "0x8", "0x40"]},
                "weapon_reserve": {"base": "0xCAFEBABE", "offsets": ["0x20", "0x4"]},
            }
        }
    }))
    return p


def test_chain_parses_hex_and_list(tmp_path):
    p = _write_offsets(tmp_path)
    r = OffsetResolver(p, build="2026.4")
    base, offsets = r.chain("player_health")
    assert base == 0xDEADBEEF
    assert offsets == [0x10, 0x8, 0x40]


def test_unknown_build_gives_empty_table(tmp_path):
    p = _write_offsets(tmp_path)
    r = OffsetResolver(p, build="2099.1")
    assert r._table == {}
</｜｜DSML｜｜ parameter>
</｜｜DSML｜｜ invoke>
</｜｜DSML｜｜ calls>