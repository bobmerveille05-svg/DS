from __future__ import annotations

from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

from .utils import ensure_dir, utc_today_yyyy_mm_dd


def export_strategy_zip(
    *, root: Path, strategy_dir: Path, out_dir: Path | None = None
) -> Path:
    if out_dir is None:
        out_dir = root / "exports"
    ensure_dir(out_dir)

    date_tag = utc_today_yyyy_mm_dd().replace("-", "")
    zip_name = f"{strategy_dir.name}_{date_tag}.zip"
    zip_path = out_dir / zip_name

    with ZipFile(zip_path, "w", compression=ZIP_DEFLATED) as z:
        for p in strategy_dir.rglob("*"):
            if p.is_dir():
                continue
            # Store relative to project root for portable paths.
            arcname = p.relative_to(root)
            z.write(p, arcname.as_posix())

    return zip_path
