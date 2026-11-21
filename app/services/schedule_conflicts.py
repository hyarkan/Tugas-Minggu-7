"""Detektor konflik: acuan kuadratik dan sweep per sumber daya."""
from collections import defaultdict
from dataclasses import dataclass
from datetime import time
from itertools import combinations
from typing import Literal

@dataclass(frozen=True)
class Conflict:
    type: Literal["room_conflict", "lecturer_conflict"]
    affected: tuple[int, int]

@dataclass(frozen=True)
class ScheduleSlot:
    id: int
    hari: int
    jam_mulai: time
    jam_selesai: time
    ruangan_kode: str
    dosen_id: int

def _pair(a, b):
    return tuple(sorted((a.id, b.id)))

def _overlap(a, b):
    return a.hari == b.hari and a.jam_mulai < b.jam_selesai and b.jam_mulai < a.jam_selesai

def detect_naive(jadwal):
    result = set()
    for a, b in combinations(jadwal, 2):
        if _overlap(a, b):
            if a.ruangan_kode == b.ruangan_kode:
                result.add(Conflict("room_conflict", _pair(a, b)))
            if a.dosen_id == b.dosen_id:
                result.add(Conflict("lecturer_conflict", _pair(a, b)))
    return sorted(result, key=lambda x: (x.affected, x.type))

def detect_schedule_conflict(jadwal):
    result = set()
    for typ, field in (("room_conflict", "ruangan_kode"), ("lecturer_conflict", "dosen_id")):
        groups = defaultdict(list)
        for item in jadwal:
            groups[(item.hari, getattr(item, field))].append(item)
        for items in groups.values():
            active = []
            for item in sorted(items, key=lambda x: (x.jam_mulai, x.jam_selesai, x.id)):
                active = [old for old in active if old.jam_selesai > item.jam_mulai]
                for old in active:
                    result.add(Conflict(typ, _pair(old, item)))
                active.append(item)
    return sorted(result, key=lambda x: (x.affected, x.type))
