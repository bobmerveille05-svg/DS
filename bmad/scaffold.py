from __future__ import annotations

import shutil
from importlib import resources
from pathlib import Path

from .utils import ensure_dir


_RESOURCE_PKG = "bmad.resources"


def scaffold_project(
    root: Path, *, force: bool = False, include_docs: bool = True
) -> list[Path]:
    """Copy packaged templates/prompts/docs into a project directory.

    By default, it is non-destructive: existing directories are not overwritten.
    Use force=True to merge/overwrite files.
    """

    targets: list[str] = ["templates", "prompts"]
    if include_docs:
        targets.append("docs")

    created: list[Path] = []
    res_root = resources.files(_RESOURCE_PKG)

    for name in targets:
        src = res_root / name
        dst = root / name
        if dst.exists() and not force:
            continue

        with resources.as_file(src) as src_path:
            ensure_dir(dst.parent)
            shutil.copytree(src_path, dst, dirs_exist_ok=True)
        created.append(dst)

    return created


def read_resource_text(rel_path: str, *, encoding: str = "utf-8") -> str:
    return (resources.files(_RESOURCE_PKG) / rel_path).read_text(encoding=encoding)
