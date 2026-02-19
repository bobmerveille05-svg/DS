#!/usr/bin/env python3
"""
spec-to-atlas.py
Convertit tasks.md (spec-kit) → atlas-phases.md (Atlas)
"""

import re
import sys
import argparse
from pathlib import Path
from datetime import datetime


def parse_tasks(tasks_md: str) -> list[dict]:
    """Parse tasks.md et extrait les tâches groupées par user story."""
    phases = []
    current_phase = None
    current_tasks = []

    for line in tasks_md.split('\n'):
        if line.startswith('## ') or line.startswith('### '):
            if current_phase and current_tasks:
                phases.append({'name': current_phase, 'tasks': current_tasks})
            current_phase = line.strip('#').strip()
            current_tasks = []
        elif re.match(r'\s*[-*]\s*\[.\]', line) or re.match(r'\s*\d+\.', line):
            task_text = re.sub(r'\s*[-*]\s*\[.\]\s*', '', line).strip()
            task_text = re.sub(r'\s*\d+\.\s*', '', task_text).strip()
            if task_text:
                parallelizable = '[P]' in task_text
                task_text = task_text.replace('[P]', '').strip()
                file_match = re.search(r'`([^`]+\.[a-z]+)`', task_text)
                file_path = file_match.group(1) if file_match else '{{FILE_PATH}}'
                agent = detect_agent(task_text)
                current_tasks.append({
                    'text': task_text,
                    'file': file_path,
                    'parallel': parallelizable,
                    'agent': agent,
                })

    if current_phase and current_tasks:
        phases.append({'name': current_phase, 'tasks': current_tasks})

    return phases


def detect_agent(task_text: str) -> str:
    """Détermine le bon agent selon le contenu de la tâche."""
    task_lower = task_text.lower()
    frontend_keywords = [
        'ui', 'component', 'css', 'html', 'style', 'layout',
        'frontend', 'responsive', 'button', 'form', 'page', 'view',
    ]
    if any(kw in task_lower for kw in frontend_keywords):
        return 'Frontend-Engineer-subagent'
    return 'Sisyphus-subagent'


def detect_parallelizable(phase: dict) -> bool:
    """Détecte si une phase peut être parallélisée."""
    agents = set(task['agent'] for task in phase['tasks'])
    has_parallel_tasks = any(task['parallel'] for task in phase['tasks'])
    return len(agents) > 1 or has_parallel_tasks


def generate_atlas_phases(feature_id: str, feature_name: str, phases: list[dict]) -> str:
    """Génère le fichier atlas-phases.md."""
    output = [
        f"# Atlas Phases — {feature_name}",
        f"\n> Généré automatiquement depuis tasks.md le {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        "\n## Source Artifacts",
        f"- Spec: `.specify/specs/{feature_id}/spec.md`",
        f"- Plan: `.specify/specs/{feature_id}/plan.md`",
        f"- Tasks: `.specify/specs/{feature_id}/tasks.md`",
        "- Constitution: `.specify/memory/constitution.md`",
        "\n---\n",
        "## Phases\n",
    ]

    for i, phase in enumerate(phases, 1):
        parallelizable = detect_parallelizable(phase)
        parallel_label = " [PARALLEL]" if parallelizable else ""
        tasks_by_agent: dict[str, list] = {}
        for task in phase['tasks']:
            agent = task['agent']
            tasks_by_agent.setdefault(agent, []).append(task)

        output.append(f"### Phase {i}: {phase['name']}{parallel_label}")
        output.append(f"**Parallélisable:** {'Oui' if parallelizable else 'Non'}")
        if len(tasks_by_agent) == 1:
            output.append(f"**Agent principal:** {list(tasks_by_agent.keys())[0]}")
        else:
            output.append(f"**Agents:** {', '.join(tasks_by_agent.keys())}")
        output.append("")

        for agent, tasks in tasks_by_agent.items():
            if len(tasks_by_agent) > 1:
                output.append(f"#### {agent} Tasks")
            for j, task in enumerate(tasks, 1):
                output.append(f"- [ ] {i}.{j} {task['text']} → `{task['file']}`")

        output.append("\n#### Tests TDD requis")
        for task in phase['tasks']:
            output.append(f"- [ ] Test: {task['text'][:50]}...")

        output.append("\n#### Validation")
        if parallelizable:
            output.append(f"- Agent: Code-Review-subagent x{len(tasks_by_agent)} (parallel)")
        else:
            output.append("- Agent: Code-Review-subagent")

        output.append(f"- Commit: `feat({feature_id}): {phase['name'].lower()}`")
        output.append("\n---\n")

    return '\n'.join(output)


def main() -> None:
    parser = argparse.ArgumentParser(description='Convert spec-kit tasks.md to Atlas atlas-phases.md')
    parser.add_argument('feature_id', help='Feature ID (e.g., 001-photo-albums)')
    parser.add_argument('--specs-dir', default='.specify/specs', help='Path to specs directory')
    args = parser.parse_args()

    feature_id = args.feature_id
    feature_dir = Path(args.specs_dir) / feature_id
    tasks_file = feature_dir / 'tasks.md'
    if not tasks_file.exists():
        print(f"❌ tasks.md not found: {tasks_file}")
        sys.exit(1)

    tasks_md = tasks_file.read_text()
    feature_name = feature_id.replace('-', ' ').title()
    name_match = re.search(r'^#\s+(.+)$', tasks_md, re.MULTILINE)
    if name_match:
        feature_name = name_match.group(1).strip()

    print(f"📋 Parsing tasks for: {feature_name}")
    phases = parse_tasks(tasks_md)
    print(f"✅ Found {len(phases)} phases")
    atlas_content = generate_atlas_phases(feature_id, feature_name, phases)

    output_file = feature_dir / 'atlas-phases.md'
    output_file.write_text(atlas_content)

    print(f"✅ Generated: {output_file}")
    print("\n🚀 Next step in VS Code:")
    print(f"   @Atlas implement from .specify/specs/{feature_id}/atlas-phases.md")


if __name__ == '__main__':
    main()
