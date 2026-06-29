---
description: Run the safe refactoring pipeline — analyze → plan → refactor → test → verify. Preserves behavior while improving structure.
argument-hint: "<target file, module, or description, e.g. 'apps/api/views.py' or 'extract idea sharing logic'>"
---

You are invoking the **refactor-workflow** pipeline. The workflow file is `.claude/workflows/refactor-workflow.md` — read it first, then execute its phases in order.

Argument: the target to refactor — a file path, module name, or description of what to refactor.

Execution:

1. **Analyze** — invoke the `repo-reviewer` subagent on the target:
   - Read the target file(s) or module.
   - Identify all callers/consumers.
   - Read existing tests for the target code.
   - Map dependencies.
   - Output: dependency graph, test coverage, risk level (low/medium/high).

2. **Plan** — define refactoring steps:
   - List each change as a discrete step.
   - For each step: what changes, what MUST NOT change, which tests validate it.
   - Order from lowest to highest risk.
   - If HIGH risk, propose feature flag or gradual migration.

3. **Refactor** — execute one step at a time:
   - Make the change.
   - `ruff check <changed_files>` — must be clean.
   - `mypy <changed_files>` — must be clean.
   - `pytest -q <related_tests> -x` — must pass.
   - If any check fails, revert that step and report.
   - Commit: `refactor(<scope>): <what changed>`.

4. **Test** — invoke `pytest-runner` on full suite:
   - `pytest -q --durations=10`
   - `ruff check .`
   - `mypy .`

5. **Verify** — invoke `repo-reviewer` on the full diff:
   - No behavior change (same inputs → same outputs)
   - No new dependencies introduced unnecessarily
   - No dead code left behind
   - Code is simpler/cleaner than before

If any phase fails, stop and report. Do not auto-revert — let the user decide.

Project rules enforced:

- Do not add new features during refactoring.
- Do not change database schema.
- Do not change API contracts.
- Do not optimize for performance (that's `/performance-audit`).
- Keep each logical step as its own commit.
