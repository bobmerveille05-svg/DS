---
lane: "doing"
shell_pid: "21263"
---
Title: WP02 — Foundational Platform
Lane: planned
assignee: ""
agent: ""

Goal: Implement core services — model routing, token/cost logging, agent orchestration hooks.

Steps for agent:
- Scaffold a model-provider adapter interface and an example adapter (mock or simple provider).
- Implement token/cost logging API with storage (file/DB stub) and an aggregation endpoint.
- Expose an orchestration API that can start/stop/inspect agent runs (HTTP or CLI hooks).
- Add integration tests validating routing decisions and cost aggregation.

Acceptance criteria:
- Model routing selects provider by configuration and returns deterministic responses for test adapters.
- Token/cost events are stored and queryable via API.
- Orchestration API can start a sample agent run (mock) and return lifecycle events.

Testing notes:
- Include unit tests for adapter selection.
- Add integration test that simulates an agent run and asserts cost entries are created.
