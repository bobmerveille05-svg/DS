from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from .utils import read_json


@dataclass(frozen=True)
class GateDefs:
    gates: dict


def load_gate_defs(package_dir: Path) -> GateDefs:
    # package_dir is bmad/ directory
    data_path = package_dir / "data" / "gates.json"
    data = read_json(data_path)
    gates = data.get("gates") or {}
    return GateDefs(gates=gates)


def gate_id_for_phase(phase: int) -> str | None:
    # Gates exist for phases 1..4, bridging to the next phase.
    mapping = {
        1: "GATE-01",
        2: "GATE-02",
        3: "GATE-03",
        4: "GATE-04",
    }
    return mapping.get(phase)


def compute_gate_status(gate_def: dict, items_state: dict[str, bool]) -> str:
    checklist = gate_def.get("checklist") or []
    required_items = [c for c in checklist if c.get("required")]
    if not required_items:
        return "PASS"

    for item in required_items:
        item_id = item.get("id")
        if not item_id:
            continue
        if not bool(items_state.get(item_id, False)):
            return "FAIL"
    return "PASS"


def init_gate_state(gate_def: dict) -> dict:
    checklist = gate_def.get("checklist") or []
    items = {}
    notes = {}
    for c in checklist:
        item_id = c.get("id")
        if not item_id:
            continue
        items[item_id] = False
        notes[item_id] = ""

    return {
        "status": "PENDING",
        "items": items,
        "notes": notes,
    }
