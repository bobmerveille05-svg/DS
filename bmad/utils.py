from __future__ import annotations

import json
import re
import unicodedata
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path


def utc_today_yyyy_mm_dd() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d")


def slugify(value: str) -> str:
    """Best-effort ASCII slug for directory/file names."""
    value = value.strip()
    if not value:
        return "strategy"

    # Remove accents, keep ASCII.
    value = (
        unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode("ascii")
    )

    value = value.lower()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    value = value.strip("-")
    return value or "strategy"


def sanitize_version(version: str) -> str:
    version = version.strip()
    if not version:
        return "0.1"
    version = version.replace(" ", "")
    version = version.replace("/", "-")
    version = version.replace("\\", "-")
    # Keep dots for readability, but remove anything unsafe.
    version = re.sub(r"[^0-9A-Za-z._-]", "-", version)
    return version


def ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def write_text(path: Path, content: str) -> None:
    ensure_dir(path.parent)
    path.write_text(content, encoding="utf-8", newline="\n")


def read_json(path: Path) -> dict:
    return json.loads(read_text(path))


def write_json(path: Path, data: dict) -> None:
    write_text(path, json.dumps(data, indent=2, sort_keys=True) + "\n")


def relpath_str(path: Path, start: Path) -> str:
    try:
        return str(path.relative_to(start))
    except Exception:
        return str(path)


@dataclass(frozen=True)
class FoundProjectRoot:
    root: Path


def find_project_root(start: Path) -> FoundProjectRoot | None:
    """Search upward for a `.bmad/project.json`."""
    cur = start.resolve()
    for candidate in [cur, *cur.parents]:
        if (candidate / ".bmad" / "project.json").is_file():
            return FoundProjectRoot(root=candidate)
    return None
