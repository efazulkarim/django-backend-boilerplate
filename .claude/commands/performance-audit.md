---
description: Run the performance audit pipeline — scan → measure → fix → verify. Finds N+1 queries, missing indexes, and slow endpoints.
argument-hint: "[optional: app_name or specific file path]"
---

You are invoking the **performance-audit** workflow. The workflow file is `.claude/workflows/performance-audit.md` — read it first, then execute its phases in order.

Argument: optional scope (app name, file path, or `all`). Defaults to `all`.

Execution:

1. **Scan** — invoke the `query-optimizer` subagent. It performs static analysis:
   - N+1 query detection (loops accessing related objects without prefetch)
   - Missing index detection (filter/order_by on unindexed fields)
   - Serializer inefficiency (SerializerMethodField that executes queries)
   - View-level issues (unbounded querysets, count + list)

2. **Measure** — for each HIGH/MEDIUM issue:
   - Count queries using `django.db.connection.queries`
   - Run `EXPLAIN ANALYZE` on slow queries
   - Benchmark endpoint latency

3. **Fix** — apply fixes for all HIGH and MEDIUM issues:
   - `select_related()` for FK and OneToOne
   - `prefetch_related()` for M2M and reverse FK
   - `annotate()` for computed fields
   - `Meta.indexes` for filtered/ordered fields
   - Pagination for unbounded querysets

4. **Verify** — re-run measurements, compare before/after:
   ```
   Endpoint: GET /ideas/
   Before: 47 queries, 230ms avg
   After:  3 queries, 18ms avg
   Improvement: 93% fewer queries, 92% faster
   ```

If any phase fails, stop and report.

Project rules enforced:

- Never change business logic (only query patterns).
- Never remove fields from querysets that consumers need.
- Always verify fixes with before/after measurements.
- Always run the full test suite after changes.
- Run `ruff check` and `mypy .` after each fix.
