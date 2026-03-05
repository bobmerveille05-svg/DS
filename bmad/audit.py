from __future__ import annotations

import re
from pathlib import Path

from .utils import read_text, utc_today_yyyy_mm_dd, write_text


_ID_PATTERNS = [
    r"\bG\d{2}-C\d{2}\b",
    r"\b(?:IND|LONG|SHORT|FLT|P|CL|TU|TS|TF|TR|SC)-\d{1,3}\b",
]


def extract_bmad_ids(text: str) -> list[str]:
    found: set[str] = set()
    for pat in _ID_PATTERNS:
        for m in re.findall(pat, text):
            found.add(m)
    return sorted(found)


def _safe_read(path: Path) -> str:
    if not path or not path.is_file():
        return ""
    try:
        return read_text(path)
    except Exception:
        return ""


def generate_traceability_audit(
    *,
    strategy_name: str,
    version: str,
    out_path: Path,
    spec_path: Path,
    logic_path: Path,
    mt4_path: Path,
    mt5_path: Path,
    pine_path: Path,
    test_path: Path,
    proof_path: Path,
) -> Path:
    spec_txt = _safe_read(spec_path)
    logic_txt = _safe_read(logic_path)
    mt4_txt = _safe_read(mt4_path)
    mt5_txt = _safe_read(mt5_path)
    pine_txt = _safe_read(pine_path)
    test_txt = _safe_read(test_path)
    proof_txt = _safe_read(proof_path)

    ids = extract_bmad_ids(spec_txt)

    def present(haystack: str, needle: str) -> str:
        return "Y" if (needle and haystack and needle in haystack) else "N"

    rows = []
    missing_any = []
    for i in ids:
        r = {
            "id": i,
            "spec": "Y" if i in spec_txt else "N",
            "logic": present(logic_txt, i),
            "mt4": present(mt4_txt, i),
            "mt5": present(mt5_txt, i),
            "pine": present(pine_txt, i),
            "test": present(test_txt, i),
            "proof": present(proof_txt, i),
        }
        rows.append(r)
        if "N" in (r["logic"], r["mt4"], r["mt5"], r["pine"], r["test"], r["proof"]):
            missing_any.append(i)

    total = len(rows)
    missing_count = len(missing_any)

    md = []
    md.append(f"# AUDIT-TRACEABILITY : {strategy_name}")
    md.append("")
    md.append(f"Version: {version}")
    md.append(f"Date: {utc_today_yyyy_mm_dd()}")
    md.append("")
    md.append("Source files:")
    md.append(f"- Spec : {spec_path.as_posix() if spec_path else ''}")
    md.append(f"- Logic: {logic_path.as_posix() if logic_path else ''}")
    md.append(f"- Code (MT4) : {mt4_path.as_posix() if mt4_path else ''}")
    md.append(f"- Code (MT5) : {mt5_path.as_posix() if mt5_path else ''}")
    md.append(f"- Code (Pine): {pine_path.as_posix() if pine_path else ''}")
    md.append(f"- Test : {test_path.as_posix() if test_path else ''}")
    md.append(f"- Proof: {proof_path.as_posix() if proof_path else ''}")
    md.append("")
    md.append("## Coverage matrix")
    md.append("")
    md.append("| ID | SPEC | LOGIC | MT4 | MT5 | PINE | TEST | PROOF |")
    md.append("|----|------|-------|-----|-----|------|------|-------|")

    for r in rows:
        md.append(
            "| {id} | {spec} | {logic} | {mt4} | {mt5} | {pine} | {test} | {proof} |".format(
                **r
            )
        )

    md.append("")
    md.append("## Summary")
    md.append("")
    md.append(f"- IDs found in spec: {total}")
    md.append(f"- IDs missing somewhere downstream: {missing_count}")
    if missing_any:
        md.append("")
        md.append(
            "Missing list (present in spec, missing in >= 1 downstream artefact):"
        )
        for i in missing_any:
            md.append(f"- {i}")

    write_text(out_path, "\n".join(md) + "\n")
    return out_path
