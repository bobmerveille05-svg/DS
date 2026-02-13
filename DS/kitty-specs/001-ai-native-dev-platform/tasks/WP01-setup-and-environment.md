Title: WP01 — Setup & Environment
Lane: planned
assignee: ""
agent: ""

Goal: Establish project skeleton and shared tooling.

Steps for agent:
- Initialize repository layout (src/, tests/, docs/, tasks/).
- Add CI workflow that runs linting and tests on push/PR.
- Add pre-commit + formatter (e.g., black/prettier + isort or equivalent) and ensure CI enforces them.
- Provide a local quickstart (`docs/quickstart.md`) describing how to run tests and start the dev environment.

Acceptance criteria:
- `make test` (or equivalent) runs and exits 0 on a clean checkout.
- CI workflow triggers on PR with lint + tests.
- README contains badge and quickstart snippet.

Testing notes:
- Add minimal smoke test to ensure the service starts.
- Ensure CI includes `pytest -q` or matching test command.
