from __future__ import annotations


def parse_hex(value: str | int) -> int:
    if isinstance(value, int):
        return value
    return int(value, 16) if value.startswith("0x") else int(value)


def fmt_hex(value: int) -> str:
    return f"0x{value:x}"


def add_offsets(base: int, *offsets: int) -> int:
    total = base
    for off in offsets:
        total += off
    return total