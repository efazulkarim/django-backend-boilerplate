---
description: Run pre-deployment verification. Checks settings, migrations, security, static files, and dependencies.
argument-hint: "[optional: 'prod' or 'staging']"
---

You are invoking the **deploy-check** agent. Read `.claude/agents/deploy-check.md` first, then execute its checklist.

Argument: optional environment target (`prod`, `staging`). Defaults to `prod`.

Execution:

1. **Settings** — verify production settings:
   - `DEBUG = False` in target settings
   - `SECRET_KEY` from env, not hardcoded
   - `ALLOWED_HOSTS` set (not `['*']`)
   - `DATABASES` using env vars
   - `SECURE_SSL_REDIRECT = True`
   - `SESSION_COOKIE_SECURE = True`
   - `CSRF_COOKIE_SECURE = True`
   - `CACHES` configured (not in-memory default)

2. **Migrations** — verify database state:
   - `python manage.py migrate --check` — no pending migrations
   - `python manage.py showmigrations --plan` — all applied
   - Check for destructive migrations on populated tables

3. **Security** — verify no obvious issues:
   - No hardcoded secrets in source (grep for API keys, tokens)
   - `.env` in `.gitignore`
   - CORS `allowed_origins` not `*`
   - DRF permissions on all views
   - Rate limiting configured

4. **Static files** — verify collectstatic works:
   - `python manage.py collectstatic --noinput --dry-run`
   - WhiteNoise or CDN configured

5. **Dependencies** — verify lockfile:
   - `pyproject.toml` has pinned versions
   - `uv lock` is up to date

6. **Health checks** — verify endpoints exist:
   - `/health/` returns 200
   - Checks DB connectivity

7. **Logging** — verify production logging:
   - JSON format or structured logging
   - Sentry DSN set (if applicable)
   - Log level is INFO or WARNING

8. **Celery** (if applicable):
   - Broker URL configured
   - Result backend configured
   - Beat schedule documented

Report format:

```
## Deploy readiness: <environment>

### BLOCKER (N)
- file:line — problem. fix.

### WARNING (N)
- file:line — problem. fix.

### INFO (N)
- suggestion.

### Summary
BLOCKERS: N — deploy will fail or has security issues
WARNINGS: N — deploy may have issues
INFOS: N — recommended improvements
READY: yes / no
```

If BLOCKERS exist, ask "Apply the BLOCKER fixes? (y/n)". On `y`, apply and re-run the check.

Hard rules:

- Never modify production settings directly.
- Never suggest disabling security features.
- Never skip BLOCKER findings.
- Always provide the exact code fix, not just a description.
