from __future__ import annotations

import struct
from typing import Any

import pymem
import pymem.memory


class MemoryReader:
    """Thin typed wrapper over pymem reads with pointer-chain support."""

    def __init__(self, process: pymem.Pymem):
        self._pm = process

    def read(self, address: int, size: int) -> bytes:
        return pymem.memory.read_bytes(self._pm.process_handle, address, size)

    def read_i32(self, address: int) -> int:
        return struct.unpack("<i", self.read(address, 4))[0]

    def read_f32(self, address: int) -> float:
        return struct.unpack("<f", self.read(address, 4))[0]

    def read_u64(self, address: int) -> int:
        return struct.unpack("<Q", self.read(address, 8))[0]

    def read_pointer_chain(self, base: int, offsets: list[int]) -> int:
        addr = base
        for off in offsets[:-1]:
            addr = self.read_u64(addr + off)
            if addr == 0:
                raise ValueError(f"null pointer while resolving chain at 0x{base:x}")
        return addr + offsets[-1]

    def read_struct(self, address: int, layout: dict[str, tuple[str, int]]) -> dict[str, Any]:
        out: dict[str, Any] = {}
        for name, (fmt, size) in layout.items():
            raw = self.read(address, size)
            out[name] = struct.unpack(fmt, raw)[0]
        return out