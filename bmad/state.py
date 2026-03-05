from __future__ import annotations

from pathlib import Path

from .utils import ensure_dir, read_json, utc_today_yyyy_mm_dd, write_json


PROJECT_SCHEMA = 1
STRATEGY_SCHEMA = 1


def bmad_dir(root: Path) -> Path:
    return root / ".bmad"


def project_file(root: Path) -> Path:
    return bmad_dir(root) / "project.json"


def load_project(root: Path) -> dict:
    path = project_file(root)
    if not path.is_file():
        raise FileNotFoundError(f"Project not initialized: missing {path}")
    return read_json(path)


def init_project(root: Path, *, bmad_version: str, force: bool = False) -> dict:
    """Initialize (or reuse) a BMAD project in `root`.

    If the project already exists and force=False, this is non-destructive:
    it keeps the existing `project.json` and only updates `bmad_version`.
    """

    ensure_dir(bmad_dir(root))
    path = project_file(root)

    if path.is_file() and not force:
        proj = read_json(path)
        if proj.get("bmad_version") != bmad_version:
            proj = dict(proj)
            proj["bmad_version"] = bmad_version
            write_json(path, proj)
        return proj

    proj = {
        "schema": PROJECT_SCHEMA,
        "bmad_version": bmad_version,
        "created": utc_today_yyyy_mm_dd(),
        "current_strategy": None,
    }
    write_json(path, proj)
    return proj


def save_project(root: Path, proj: dict) -> None:
    write_json(project_file(root), proj)


def get_current_strategy_dir(root: Path, proj: dict) -> Path:
    rel = proj.get("current_strategy")
    if not rel:
        raise FileNotFoundError("No current strategy set. Run: python -m bmad start")
    strategy_dir = (root / rel).resolve()
    if not strategy_dir.is_dir():
        raise FileNotFoundError(f"Current strategy directory not found: {strategy_dir}")
    return strategy_dir


def set_current_strategy(root: Path, proj: dict, strategy_dir: Path) -> dict:
    proj = dict(proj)
    proj["current_strategy"] = str(strategy_dir.relative_to(root))
    save_project(root, proj)
    return proj


def strategy_bmad_dir(strategy_dir: Path) -> Path:
    return strategy_dir / ".bmad"


def strategy_state_file(strategy_dir: Path) -> Path:
    return strategy_bmad_dir(strategy_dir) / "state.json"


def load_strategy(strategy_dir: Path) -> dict:
    path = strategy_state_file(strategy_dir)
    if not path.is_file():
        raise FileNotFoundError(f"Missing strategy state file: {path}")
    return read_json(path)


def save_strategy(strategy_dir: Path, state: dict) -> None:
    ensure_dir(strategy_bmad_dir(strategy_dir))
    write_json(strategy_state_file(strategy_dir), state)
