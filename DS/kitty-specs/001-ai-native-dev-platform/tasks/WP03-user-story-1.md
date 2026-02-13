Title: WP03 — Convert description → tested PR (MVP)
Lane: planned
assignee: ""
agent: ""

Goal: Given a short feature description, generate an implementation PR containing code + tests.

Steps for agent:
- Define expected artifact structure for an LLM-driven PR (worktree layout, branch name, commit message, PR body).
- Implement the sequence: parse description → produce implementation plan → create worktree → apply changes → open PR.
- Create tests that assert the PR contains new tests and they pass under CI.
- Add monitoring: each PR should include metadata about token usage and agent name.

Acceptance criteria:
- A demo description produces a PR branch in the repo with code + tests.
- CI passes for that PR in the target branch.
- PR body contains token/cost summary (mock data acceptable for initial implementation).

Testing notes:
- Use a dry-run mode that writes the patch to a temp worktree and validates file changes without pushing.
- Ensure idempotency for repeated runs of the same description.
