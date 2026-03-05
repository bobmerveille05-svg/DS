from __future__ import annotations

import argparse
import shlex
import sys
from pathlib import Path

from . import __version__
from .audit import generate_traceability_audit
from .exporter import export_strategy_zip
from .gates import (
    compute_gate_status,
    gate_id_for_phase,
    init_gate_state,
    load_gate_defs,
)
from .scaffold import read_resource_text, scaffold_project
from .state import (
    init_project,
    load_project,
    load_strategy,
    save_strategy,
    set_current_strategy,
)
from .utils import (
    ensure_dir,
    find_project_root,
    read_text,
    relpath_str,
    sanitize_version,
    slugify,
    utc_today_yyyy_mm_dd,
    write_text,
)


PHASES = {
    1: {"name": "CAPTURE", "agent": "analyst", "artefact": "STRATEGY-SPEC"},
    2: {"name": "LOGIC", "agent": "quant", "artefact": "LOGIC-MODEL"},
    3: {"name": "CODE", "agent": "coder", "artefact": "SOURCE-CODE"},
    4: {"name": "TEST", "agent": "tester", "artefact": "TEST-REPORT"},
    5: {"name": "PROOF", "agent": "auditor", "artefact": "PROOF-CERTIFICATE"},
}


def _get_root_for_command(cmd: str) -> Path:
    found = find_project_root(Path.cwd())
    if found:
        return found.root
    if cmd == "init":
        return Path.cwd().resolve()
    raise FileNotFoundError("BMAD project not initialized. Run: python -m bmad init")


def _templates_dir(root: Path) -> Path:
    return root / "templates"


def _prompts_dir(root: Path) -> Path:
    return root / "prompts"


def _apply_mapping(txt: str, mapping: dict[str, str]) -> str:
    for k, v in mapping.items():
        txt = txt.replace("{{" + k + "}}", v)
    return txt


def _render_template(path: Path, mapping: dict[str, str]) -> str:
    return _apply_mapping(read_text(path), mapping)


def _load_template_text(root: Path, rel_path: str) -> str:
    local = _templates_dir(root) / rel_path
    if local.is_file():
        return read_text(local)
    return read_resource_text(f"templates/{rel_path}")


def _load_prompt_text(project_root: Path | None, name: str) -> str:
    if project_root is not None:
        local = _prompts_dir(project_root) / f"{name}.md"
        if local.is_file():
            return read_text(local)
    return read_resource_text(f"prompts/{name}.md")


def cmd_init(args: argparse.Namespace) -> int:
    root = _get_root_for_command("init")
    ensure_dir(root / "work")
    ensure_dir(root / "exports")
    ensure_dir(root / ".bmad")
    already = (root / ".bmad" / "project.json").is_file()
    init_project(root, bmad_version=__version__)

    if not getattr(args, "no_scaffold", False):
        created = scaffold_project(root, force=bool(getattr(args, "force", False)))
        if created:
            print("Scaffolded:")
            for p in created:
                print(f"- {relpath_str(p, root)}")

    if already:
        print(f"BMAD project already initialized: {root}")
    else:
        print(f"Initialized BMAD project at: {root}")
    return 0


def cmd_start(args: argparse.Namespace) -> int:
    root = _get_root_for_command("start")
    proj = load_project(root)

    name = (args.name or "").strip() or input("Strategy name: ").strip()
    version = sanitize_version(
        (args.version or "").strip() or input("Version (e.g. 0.1): ").strip()
    )
    author = (args.author or "").strip() or input("Author: ").strip() or "unknown"

    slug = slugify(name)
    folder = f"{slug}_v{version}"

    strategy_dir = (root / "work" / folder).resolve()
    if strategy_dir.exists():
        raise FileExistsError(f"Strategy folder already exists: {strategy_dir}")

    artefacts_dir = strategy_dir / "artefacts"
    code_dir = artefacts_dir / f"SOURCE-CODE-{slug}-v{version}"
    ensure_dir(code_dir)

    mapping = {
        "STRATEGY_NAME": name,
        "VERSION": version,
        "DATE": utc_today_yyyy_mm_dd(),
        "AUTHOR": author,
        "SLUG": slug,
    }

    spec_path = artefacts_dir / f"STRATEGY-SPEC-{slug}-v{version}.md"
    logic_path = artefacts_dir / f"LOGIC-MODEL-{slug}-v{version}.md"
    test_path = artefacts_dir / f"TEST-REPORT-{slug}-v{version}.md"
    proof_path = artefacts_dir / f"PROOF-CERTIFICATE-{slug}-v{version}.md"
    trace_path = artefacts_dir / f"TRACEABILITY-MATRIX-{slug}-v{version}.md"
    audit_path = artefacts_dir / f"AUDIT-TRACEABILITY-{slug}-v{version}.md"

    write_text(
        spec_path,
        _apply_mapping(_load_template_text(root, "STRATEGY-SPEC.template.md"), mapping),
    )
    write_text(
        logic_path,
        _apply_mapping(_load_template_text(root, "LOGIC-MODEL.template.md"), mapping),
    )
    write_text(
        test_path,
        _apply_mapping(_load_template_text(root, "TEST-REPORT.template.md"), mapping),
    )
    write_text(
        proof_path,
        _apply_mapping(
            _load_template_text(root, "PROOF-CERTIFICATE.template.md"), mapping
        ),
    )
    write_text(
        trace_path,
        _apply_mapping(
            _load_template_text(root, "TRACEABILITY-MATRIX.template.md"), mapping
        ),
    )

    # Code skeletons
    mt4_path = code_dir / f"{slug}_v{version}.mq4"
    mt5_path = code_dir / f"{slug}_v{version}.mq5"
    pine_path = code_dir / f"{slug}_v{version}.pine"
    write_text(
        mt4_path,
        _apply_mapping(_load_template_text(root, "code/MT4_EA.template.mq4"), mapping),
    )
    write_text(
        mt5_path,
        _apply_mapping(_load_template_text(root, "code/MT5_EA.template.mq5"), mapping),
    )
    write_text(
        pine_path,
        _apply_mapping(
            _load_template_text(root, "code/TradingView_Strategy.template.pine"),
            mapping,
        ),
    )

    # Strategy state
    gate_defs = load_gate_defs(Path(__file__).resolve().parent)
    gates_state = {
        gate_id: init_gate_state(gdef) for gate_id, gdef in gate_defs.gates.items()
    }
    state = {
        "schema": 1,
        "strategy": {
            "name": name,
            "slug": slug,
            "version": version,
            "author": author,
            "created": utc_today_yyyy_mm_dd(),
        },
        "phase": 1,
        "gates": gates_state,
        "paths": {
            "strategy_spec": relpath_str(spec_path, strategy_dir),
            "logic_model": relpath_str(logic_path, strategy_dir),
            "test_report": relpath_str(test_path, strategy_dir),
            "proof_certificate": relpath_str(proof_path, strategy_dir),
            "traceability_matrix": relpath_str(trace_path, strategy_dir),
            "audit_traceability": relpath_str(audit_path, strategy_dir),
            "code": {
                "mt4": relpath_str(mt4_path, strategy_dir),
                "mt5": relpath_str(mt5_path, strategy_dir),
                "pine": relpath_str(pine_path, strategy_dir),
            },
        },
    }
    ensure_dir(strategy_dir / ".bmad")
    save_strategy(strategy_dir, state)

    # Set as current strategy
    set_current_strategy(root, proj, strategy_dir)

    print("Created strategy workspace:")
    print(f"- {relpath_str(strategy_dir, root)}")
    print("Artefacts:")
    print(f"- {relpath_str(spec_path, root)}")
    print(f"- {relpath_str(logic_path, root)}")
    print(f"- {relpath_str(mt4_path, root)}")
    print(f"- {relpath_str(mt5_path, root)}")
    print(f"- {relpath_str(pine_path, root)}")
    print(f"- {relpath_str(test_path, root)}")
    print(f"- {relpath_str(proof_path, root)}")
    print(f"- {relpath_str(trace_path, root)}")
    return 0


def _format_gate_progress(gate_def: dict, gate_state: dict) -> str:
    checklist = gate_def.get("checklist") or []
    required = [c for c in checklist if c.get("required")]
    items = (gate_state or {}).get("items") or {}
    done = sum(1 for c in required if items.get(c.get("id", ""), False))
    total = len(required)
    return f"{done}/{total}"


def cmd_status(args: argparse.Namespace) -> int:
    root = _get_root_for_command("status")
    proj = load_project(root)
    strategy_dir = (
        Path(root / (proj.get("current_strategy") or "")).resolve()
        if proj.get("current_strategy")
        else None
    )

    print(f"Project root: {root}")
    if not strategy_dir or not strategy_dir.is_dir():
        print("Current strategy: (none)")
        return 0

    state = load_strategy(strategy_dir)
    strat = state.get("strategy") or {}
    phase = int(state.get("phase", 1))
    phase_info = PHASES.get(phase, {"name": "?", "agent": "?", "artefact": "?"})

    print(
        f"Current strategy: {strat.get('name', '')} v{strat.get('version', '')} ({relpath_str(strategy_dir, root)})"
    )
    print(
        f"Phase: {phase} {phase_info['name']} (agent: {phase_info['agent']}, artefact: {phase_info['artefact']})"
    )

    gate_defs = load_gate_defs(Path(__file__).resolve().parent)
    print("Gates:")
    for gid in ["GATE-01", "GATE-02", "GATE-03", "GATE-04"]:
        gdef = gate_defs.gates.get(gid)
        if not gdef:
            continue
        gstate = (state.get("gates") or {}).get(gid) or {}
        status = gstate.get("status", "PENDING")
        progress = _format_gate_progress(gdef, gstate)
        print(f"- {gid} {gdef.get('name', '')}: {status} ({progress} required true)")
    return 0


def _load_current_strategy(root: Path) -> tuple[Path, dict, dict]:
    proj = load_project(root)
    rel = proj.get("current_strategy")
    if not rel:
        raise FileNotFoundError("No current strategy set. Run: python -m bmad start")
    strategy_dir = (root / rel).resolve()
    state = load_strategy(strategy_dir)
    return strategy_dir, proj, state


def _recompute_gate_pass_if_complete(*, gate_def: dict, gate_state: dict) -> dict:
    # Only auto-promote to PASS when complete.
    # Never auto-demote to FAIL; keep PENDING unless user explicitly fails it.
    gate_state = dict(gate_state)
    status = gate_state.get("status", "PENDING")
    items = gate_state.get("items") or {}
    computed = compute_gate_status(gate_def, items)
    if computed == "PASS":
        gate_state["status"] = "PASS"
    else:
        if status == "PASS":
            gate_state["status"] = "PENDING"
    return gate_state


def cmd_gate_show(args: argparse.Namespace) -> int:
    root = _get_root_for_command("gate")
    strategy_dir, _proj, state = _load_current_strategy(root)
    phase = int(state.get("phase", 1))
    gid = gate_id_for_phase(phase)
    if not gid:
        print(f"No gate for phase {phase}.")
        return 0

    gate_defs = load_gate_defs(Path(__file__).resolve().parent)
    gdef = gate_defs.gates.get(gid)
    if not gdef:
        raise KeyError(f"Missing gate definition: {gid}")

    gates_state = state.get("gates") or {}
    gstate = gates_state.get(gid) or {}
    status = gstate.get("status", "PENDING")
    progress = _format_gate_progress(gdef, gstate)

    print(f"Gate: {gid} - {gdef.get('name', '')}")
    print(f"Status: {status} ({progress} required true)")
    print("Checklist:")
    items = gstate.get("items") or {}
    notes = gstate.get("notes") or {}
    for c in gdef.get("checklist") or []:
        item_id = c.get("id", "")
        required = bool(c.get("required"))
        q = c.get("question", "")
        val = "true" if items.get(item_id, False) else "false"
        note = (notes.get(item_id) or "").strip()
        req = "required" if required else "optional"
        if note:
            print(f"- {item_id} ({req}) = {val} :: {q} | note: {note}")
        else:
            print(f"- {item_id} ({req}) = {val} :: {q}")
    return 0


def cmd_gate_set(args: argparse.Namespace) -> int:
    root = _get_root_for_command("gate")
    strategy_dir, _proj, state = _load_current_strategy(root)
    phase = int(state.get("phase", 1))
    gid = gate_id_for_phase(phase)
    if not gid:
        print(f"No gate for phase {phase}.")
        return 0

    item_id = args.item_id.strip()
    value = args.value.strip().lower()
    if value not in ("true", "false"):
        raise ValueError("Value must be true or false")
    bool_value = value == "true"

    gate_defs = load_gate_defs(Path(__file__).resolve().parent)
    gdef = gate_defs.gates.get(gid)
    if not gdef:
        raise KeyError(f"Missing gate definition: {gid}")

    gates_state = dict(state.get("gates") or {})
    gstate = dict(gates_state.get(gid) or {})
    items = dict(gstate.get("items") or {})
    notes = dict(gstate.get("notes") or {})
    if item_id not in items:
        raise KeyError(f"Unknown checklist item for {gid}: {item_id}")

    items[item_id] = bool_value
    if args.note is not None:
        notes[item_id] = args.note

    gstate["items"] = items
    gstate["notes"] = notes
    gstate = _recompute_gate_pass_if_complete(gate_def=gdef, gate_state=gstate)
    gates_state[gid] = gstate
    state["gates"] = gates_state
    save_strategy(strategy_dir, state)

    print(f"Set {gid} {item_id} = {value}")
    return 0


def cmd_gate_fail(args: argparse.Namespace) -> int:
    root = _get_root_for_command("gate")
    strategy_dir, _proj, state = _load_current_strategy(root)
    phase = int(state.get("phase", 1))
    gid = gate_id_for_phase(phase)
    if not gid:
        print(f"No gate for phase {phase}.")
        return 0

    gates_state = dict(state.get("gates") or {})
    gstate = dict(gates_state.get(gid) or {})
    gstate["status"] = "FAIL"
    gates_state[gid] = gstate
    state["gates"] = gates_state
    save_strategy(strategy_dir, state)
    print(f"Marked {gid} as FAIL")
    return 0


def cmd_gate_reset(args: argparse.Namespace) -> int:
    root = _get_root_for_command("gate")
    strategy_dir, _proj, state = _load_current_strategy(root)
    phase = int(state.get("phase", 1))
    gid = gate_id_for_phase(phase)
    if not gid:
        print(f"No gate for phase {phase}.")
        return 0

    gates_state = dict(state.get("gates") or {})
    gstate = dict(gates_state.get(gid) or {})
    gstate["status"] = "PENDING"
    gates_state[gid] = gstate
    state["gates"] = gates_state
    save_strategy(strategy_dir, state)
    print(f"Reset {gid} status to PENDING")
    return 0


def cmd_gate_interactive(args: argparse.Namespace) -> int:
    root = _get_root_for_command("gate")
    strategy_dir, _proj, state = _load_current_strategy(root)
    phase = int(state.get("phase", 1))
    gid = gate_id_for_phase(phase)
    if not gid:
        print(f"No gate for phase {phase}.")
        return 0

    gate_defs = load_gate_defs(Path(__file__).resolve().parent)
    gdef = gate_defs.gates.get(gid)
    if not gdef:
        raise KeyError(f"Missing gate definition: {gid}")

    gates_state = dict(state.get("gates") or {})
    gstate = dict(gates_state.get(gid) or {})
    items = dict(gstate.get("items") or {})
    notes = dict(gstate.get("notes") or {})

    print(f"Interactive gate checklist: {gid} - {gdef.get('name', '')}")
    print("Answer y/n to set, enter to skip, or 'q' to quit.")

    for c in gdef.get("checklist") or []:
        item_id = c.get("id", "")
        q = c.get("question", "")
        cur = "y" if items.get(item_id, False) else "n"
        while True:
            ans = input(f"{item_id} [{cur}] {q} (y/n/enter/q): ").strip().lower()
            if ans == "":
                break
            if ans == "q":
                print("Stopped.")
                gstate["items"] = items
                gstate["notes"] = notes
                gstate = _recompute_gate_pass_if_complete(
                    gate_def=gdef, gate_state=gstate
                )
                gates_state[gid] = gstate
                state["gates"] = gates_state
                save_strategy(strategy_dir, state)
                return 0
            if ans in ("y", "n"):
                items[item_id] = ans == "y"
                break
            print("Invalid input. Use y, n, enter, or q.")

    gstate["items"] = items
    gstate["notes"] = notes
    gstate = _recompute_gate_pass_if_complete(gate_def=gdef, gate_state=gstate)
    gates_state[gid] = gstate
    state["gates"] = gates_state
    save_strategy(strategy_dir, state)

    status = gstate.get("status", "PENDING")
    print(f"Gate status: {status}")
    if status != "PASS":
        missing = []
        for c in gdef.get("checklist") or []:
            if not c.get("required"):
                continue
            iid = c.get("id")
            if iid and not items.get(iid, False):
                missing.append(iid)
        if missing:
            print("Missing required items:")
            for iid in missing:
                print(f"- {iid}")
    return 0


def cmd_phase_next(args: argparse.Namespace) -> int:
    root = _get_root_for_command("phase")
    strategy_dir, _proj, state = _load_current_strategy(root)
    phase = int(state.get("phase", 1))
    if phase >= 5:
        print("Already at Phase 5 (PROOF). No next phase.")
        return 0

    gid = gate_id_for_phase(phase)
    if not gid:
        raise RuntimeError(f"Missing gate mapping for phase: {phase}")

    gates_state = state.get("gates") or {}
    gstate = gates_state.get(gid) or {}
    if gstate.get("status") != "PASS":
        print(f"Cannot advance. {gid} is not PASS.")
        print("Run: python -m bmad gate  (or: python -m bmad gate show)")
        return 2

    state["phase"] = phase + 1
    save_strategy(strategy_dir, state)
    new_phase = int(state["phase"])
    print(f"Advanced to Phase {new_phase} {PHASES.get(new_phase, {}).get('name', '')}")
    return 0


def cmd_rollback(args: argparse.Namespace) -> int:
    root = _get_root_for_command("rollback")
    strategy_dir, _proj, state = _load_current_strategy(root)
    phase = int(state.get("phase", 1))
    if phase <= 1:
        print("Already at Phase 1.")
        return 0

    new_phase = phase - 1
    state["phase"] = new_phase

    # Invalidate the gate that leads out of the new current phase.
    gid = gate_id_for_phase(new_phase)
    if gid:
        gates_state = dict(state.get("gates") or {})
        gstate = dict(gates_state.get(gid) or {})
        if gstate.get("status") == "PASS":
            gstate["status"] = "PENDING"
        gates_state[gid] = gstate
        state["gates"] = gates_state

    save_strategy(strategy_dir, state)
    print(
        f"Rolled back to Phase {new_phase} {PHASES.get(new_phase, {}).get('name', '')}"
    )
    return 0


def cmd_audit(args: argparse.Namespace) -> int:
    root = _get_root_for_command("audit")
    strategy_dir, _proj, state = _load_current_strategy(root)
    strat = state.get("strategy") or {}
    paths = state.get("paths") or {}

    def p(rel: str) -> Path:
        return (strategy_dir / rel).resolve() if rel else Path()

    out_path = p(paths.get("audit_traceability", ""))
    spec_path = p(paths.get("strategy_spec", ""))
    logic_path = p(paths.get("logic_model", ""))
    test_path = p(paths.get("test_report", ""))
    proof_path = p(paths.get("proof_certificate", ""))
    code = paths.get("code") or {}
    mt4_path = p(code.get("mt4", ""))
    mt5_path = p(code.get("mt5", ""))
    pine_path = p(code.get("pine", ""))

    generate_traceability_audit(
        strategy_name=strat.get("name", ""),
        version=strat.get("version", ""),
        out_path=out_path,
        spec_path=spec_path,
        logic_path=logic_path,
        mt4_path=mt4_path,
        mt5_path=mt5_path,
        pine_path=pine_path,
        test_path=test_path,
        proof_path=proof_path,
    )

    print(f"Wrote audit report: {relpath_str(out_path, root)}")
    return 0


def cmd_export(args: argparse.Namespace) -> int:
    root = _get_root_for_command("export")
    strategy_dir, _proj, _state = _load_current_strategy(root)
    zip_path = export_strategy_zip(root=root, strategy_dir=strategy_dir)
    print(f"Exported: {relpath_str(zip_path, root)}")
    return 0


def cmd_agent(args: argparse.Namespace) -> int:
    name = args.name.strip().lower()
    found = find_project_root(Path.cwd())
    project_root = found.root if found else None
    try:
        print(_load_prompt_text(project_root, name))
    except FileNotFoundError:
        raise FileNotFoundError(f"Unknown agent prompt: {name}")
    return 0


def cmd_show(args: argparse.Namespace) -> int:
    root = _get_root_for_command("show")
    strategy_dir, _proj, state = _load_current_strategy(root)
    paths = state.get("paths") or {}

    which = args.which
    rel = ""
    if which == "spec":
        rel = paths.get("strategy_spec", "")
    elif which == "logic":
        rel = paths.get("logic_model", "")
    elif which == "test":
        rel = paths.get("test_report", "")
    elif which == "proof":
        rel = paths.get("proof_certificate", "")
    elif which == "trace":
        rel = paths.get("traceability_matrix", "")
    elif which == "audit":
        rel = paths.get("audit_traceability", "")
    elif which == "code":
        platform = (args.platform or "").strip().lower()
        if platform not in ("mt4", "mt5", "pine"):
            raise ValueError("--platform must be one of: mt4, mt5, pine")
        rel = (paths.get("code") or {}).get(platform, "")
    else:
        raise ValueError(f"Unknown show target: {which}")

    p = (strategy_dir / rel).resolve() if rel else None
    if not p or not p.exists():
        print("Not found.")
        return 1

    print(relpath_str(p, root))
    if args.print:
        print("\n---\n")
        print(read_text(p))
    return 0


def cmd_shell(args: argparse.Namespace) -> int:
    print("BMAD shell. Type /help for commands. Type exit to quit.")
    while True:
        try:
            line = input("bmad> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("")
            return 0
        if not line:
            continue
        if line.lower() in ("exit", "quit"):
            return 0
        if line.strip() in ("/help", "help"):
            print("Try: /status, /gate, /phase next, /rollback, /audit, /export")
            continue

        argv = shlex.split(line)
        if argv and argv[0].startswith("/"):
            argv[0] = argv[0][1:]
        try:
            rc = main(["bmad"] + argv)
        except SystemExit as e:
            rc = int(e.code or 0)
        if rc not in (0, None):
            print(f"(exit {rc})")


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="bmad", add_help=True)
    p.add_argument("--version", action="version", version=f"bmad {__version__}")

    sub = p.add_subparsers(dest="cmd", required=True)

    sp = sub.add_parser("init", help="Initialize BMAD project in current directory")
    sp.add_argument(
        "--force",
        action="store_true",
        help="Overwrite/merge scaffold files (templates/prompts/docs)",
    )
    sp.add_argument(
        "--no-scaffold",
        action="store_true",
        help="Do not copy templates/prompts/docs into the project",
    )
    sp.set_defaults(_fn=cmd_init)

    sp = sub.add_parser("start", help="Create a new strategy workspace under work/")
    sp.add_argument("--name", help="Strategy name")
    sp.add_argument("--version", dest="version", help="Strategy version (e.g. 0.1)")
    sp.add_argument("--author", help="Author")
    sp.set_defaults(_fn=cmd_start)

    sp = sub.add_parser("status", help="Show current strategy, phase, and gates")
    sp.set_defaults(_fn=cmd_status)

    sp = sub.add_parser("rollback", help="Rollback to previous phase")
    sp.set_defaults(_fn=cmd_rollback)

    sp = sub.add_parser("audit", help="Generate traceability audit report")
    sp.set_defaults(_fn=cmd_audit)

    sp = sub.add_parser(
        "export", help="Export current strategy workspace to exports/*.zip"
    )
    sp.set_defaults(_fn=cmd_export)

    sp = sub.add_parser("agent", help="Print an agent prompt")
    sp.add_argument(
        "name",
        choices=["orchestrator", "analyst", "quant", "coder", "tester", "auditor"],
    )
    sp.set_defaults(_fn=cmd_agent)

    sp = sub.add_parser(
        "show", help="Print path (and optionally contents) of an artefact"
    )
    sp.add_argument(
        "which", choices=["spec", "logic", "code", "test", "proof", "trace", "audit"]
    )
    sp.add_argument("--platform", help="For 'code': mt4|mt5|pine")
    sp.add_argument("--print", action="store_true", help="Print the file content")
    sp.set_defaults(_fn=cmd_show)

    sp = sub.add_parser("shell", help="Interactive shell with slash-style commands")
    sp.set_defaults(_fn=cmd_shell)

    # phase
    sp = sub.add_parser("phase", help="Phase operations")
    phase_sub = sp.add_subparsers(dest="phase_cmd", required=True)
    s2 = phase_sub.add_parser(
        "next", help="Advance to next phase (requires current gate PASS)"
    )
    s2.set_defaults(_fn=cmd_phase_next)

    # gate
    sp = sub.add_parser("gate", help="Gate operations")
    gate_sub = sp.add_subparsers(dest="gate_cmd", required=False)
    sp.set_defaults(_fn=cmd_gate_interactive)
    s2 = gate_sub.add_parser("show", help="Show current gate checklist")
    s2.set_defaults(_fn=cmd_gate_show)
    s2 = gate_sub.add_parser("set", help="Set a checklist item true/false")
    s2.add_argument("item_id", help="Checklist item id, e.g. G01-C01")
    s2.add_argument("value", help="true|false")
    s2.add_argument("--note", help="Optional note/evidence")
    s2.set_defaults(_fn=cmd_gate_set)
    s2 = gate_sub.add_parser("fail", help="Mark current gate as FAIL")
    s2.set_defaults(_fn=cmd_gate_fail)
    s2 = gate_sub.add_parser("reset", help="Reset current gate status to PENDING")
    s2.set_defaults(_fn=cmd_gate_reset)

    return p


def main(argv: list[str] | None = None) -> int:
    if argv is None:
        argv = sys.argv
    else:
        argv = list(argv)

    if len(argv) >= 2 and isinstance(argv[1], str) and argv[1].startswith("/"):
        argv[1] = argv[1][1:]
    parser = build_parser()
    ns = parser.parse_args(argv[1:])
    fn = getattr(ns, "_fn", None)
    if not fn:
        parser.print_help()
        return 2

    try:
        return int(fn(ns) or 0)
    except FileNotFoundError as e:
        print(str(e))
        return 2
    except (ValueError, KeyError, FileExistsError) as e:
        print(f"Error: {e}")
        return 2
