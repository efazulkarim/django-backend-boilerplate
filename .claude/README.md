# `.claude/` — Engineering Automation for Claude Code

> This directory turns Claude Code into an AI pair programmer that knows your stack, follows your conventions, and automates your workflow.

## Quick Start

```bash
# Open Claude Code in this project
claude

# Claude automatically:
# 1. Reads CLAUDE.md (knows your stack, conventions, rules)
# 2. Runs session-start hook (shows branch, commits, migration status)
# 3. Applies rules on every response (API format, auth, pagination)

# Try these commands:
/add-endpoint POST /ideas/           # Build a new API endpoint
/test                                # Run tests
/review                              # Review your diff
/commit                              # Write a conventional commit
/migrate add_idea_priority           # Create a migration
/schema-change add is_archived to ideas  # Schema change
/security-audit                      # Security scan
/seed                                # Generate test data
/deploy-check                        # Pre-deployment verification
/performance-audit                   # Find N+1 queries
/refactor apps/api/views.py          # Safe refactoring
/lint                                # Run ruff
/sync-skills                         # Verify skills are in sync
```

## Directory Structure

```
.claude/
├── CLAUDE.md              ← Project constitution (loaded every session)
├── settings.json          ← Permissions, hooks, plugins
├── .mcp.json              ← MCP server configs (Neon, GitHub, Context7, Playwright)
│
├── skills/                ← Reference docs Claude reads before acting
│   ├── django-models/     ← Django ORM patterns, abstract base classes
│   ├── drf-views/         ← DRF ViewSets, serializers, URL patterns
│   ├── django-migrations/ ← makemigrations, RunPython, apps.get_model()
│   ├── django-settings/   ← 4-file settings inheritance
│   ├── django-auth/       ← DRF Token auth, allauth, permissions
│   ├── pytest-django/     ← Test fixtures, markers, patterns
│   ├── celery-tasks/      ← Task templates, beat schedules, testing
│   ├── redis-caching/     ← Cache-aside, view caching, cache warming
│   ├── llm-provider-fallback/ ← LLM provider chain patterns
│   ├── polar-payments/    ← Polar payment integration
│   ├── stripe-payments/   ← Stripe payment integration
│   ├── neon-postgres/     ← Neon-specific patterns
│   ├── security-and-hardening/ ← Security middleware, DRF throttling
│   ├── test-driven-development/ ← TDD workflow patterns
│   └── caveman/           ← Deliberate thinking mode
│
├── agents/                ← Subagent definitions for delegation
│   ├── drf-view-builder.md      ← Builds views, serializers, URLs
│   ├── django-migrator.md       ← Creates safe, reversible migrations
│   ├── repo-reviewer.md         ← Reviews code against project rules
│   ├── security-auditor.md      ← Audits auth, secrets, CORS
│   ├── pytest-runner.md         ← Runs and analyzes test results
│   ├── llm-service-expert.md    ← Reviews LLM service code
│   ├── data-seed.md             ← Generates realistic test data
│   ├── deploy-check.md          ← Pre-deployment verification
│   └── query-optimizer.md       ← Finds N+1 queries, missing indexes
│
├── rules/                 ← Validation constraints (always-active)
│   ├── api-response.md          ← JSON responses, correct status codes
│   ├── auth-security.md         ← Token auth, no secrets in code
│   ├── database-migrations.md   ← Reversible, non-destructive
│   ├── layered-architecture.md  ← Views → Services → Models
│   ├── llm-providers.md         ← Provider fallback chain order
│   ├── error-handling.md        ← Consistent error shapes, status codes
│   ├── logging.md               ← Structured logging, Sentry
│   └── pagination.md            ← Page-number vs cursor, filtering
│
├── commands/              ← User-invocable slash commands
│   ├── add-endpoint.md          ← /add-endpoint <path method>
│   ├── commit.md                ← /commit
│   ├── deploy-check.md          ← /deploy-check
│   ├── lint.md                  ← /lint
│   ├── migrate.md               ← /migrate <slug>
│   ├── performance-audit.md     ← /performance-audit
│   ├── refactor.md              ← /refactor <target>
│   ├── review.md                ← /review [path]
│   ├── schema-change.md         ← /schema-change <description>
│   ├── security-audit.md        ← /security-audit [path]
│   ├── seed.md                  ← /seed [app_name]
│   ├── sync-skills.md           ← /sync-skills
│   └── test.md                  ← /test [pattern]
│
├── workflows/             ← Multi-phase orchestration pipelines
│   ├── add-endpoint.md          ← Analyze → Plan → Build → Test → Review
│   ├── db-schema-change.md      ← Design → Apply → Test → Audit
│   ├── security-review.md       ← Scan → Verify → Report
│   ├── refactor-workflow.md     ← Analyze → Plan → Refactor → Test → Verify
│   ├── data-migration-workflow.md ← Design → Validate → Migrate → Verify → RollbackReady
│   └── performance-audit.md     ← Scan → Measure → Fix → Verify
│
├── templates/             ← Output format templates
│   ├── pr-description.md        ← PR with migrations, test plan
│   ├── commit-message.md        ← Conventional commits format
│   ├── api-doc.md               ← API endpoint documentation
│   ├── issue.md                 ← GitHub issue format
│   └── adr.md                   ← Architecture Decision Record
│
└── hooks/                 ← Automated JS scripts (pre/post tool use)
    ├── pre-tool-use-secret-guard.js  ← Prevents credential leaks
    ├── post-tool-use-ruff.js         ← Auto-lints Python files
    ├── post-tool-use-mypy.js         ← Type-checks Python files
    ├── session-start-load-context.js ← Shows project state on session start
    └── stop-pytest-smoke.js          ← Runs unit tests on session end
```

## How It Works

### Session Lifecycle

```
┌─────────────────────────────────────────────────────────────────┐
│  SESSION START                                                  │
│  ├── Hook: session-start-load-context.js fires                  │
│  │   → Shows: Django backend, Python 3.12, branch, apps,       │
│  │     migration status                                         │
│  ├── CLAUDE.md loaded into system prompt                        │
│  │   → Stack, architecture, conventions, commands, rules        │
│  └── claude-mem provides cross-session memories                 │
│                                                                  │
│  EVERY TOOL CALL                                                │
│  ├── PreToolUse: secret-guard checks for leaked credentials     │
│  └── PostToolUse: ruff lints, mypy type-checks edited files     │
│                                                                  │
│  ON-DEMAND                                                      │
│  ├── Skills: loaded when relevant to the task                   │
│  ├── Rules: always considered, enforced in responses            │
│  ├── Commands: loaded when you type /command                    │
│  ├── Workflows: loaded when you invoke a pipeline               │
│  └── Agents: loaded when Claude delegates work                  │
│                                                                  │
│  SESSION END                                                    │
│  ├── Hook: stop-pytest-smoke.js fires                           │
│  │   → Runs unit tests if code was changed                      │
│  └── claude-mem saves conversation learnings                    │
└─────────────────────────────────────────────────────────────────┘
```

### Memory System

Three layers of memory work together:

| Layer | What | How | When |
|---|---|---|---|
| **CLAUDE.md** | Project constitution | Auto-loaded | Every session |
| **memory/** | Explicit facts (your control) | MEMORY.md index loaded | Every session |
| **claude-mem** | Auto-extracted learnings | Plugin-managed | Every session |

Memory files are stored at:
```
~/.claude/projects/d--Backend-django-backend-boiletplate/memory/
```

### Hooks

| Hook | Trigger | What it does |
|---|---|---|
| `pre-tool-use-secret-guard.js` | Before Write/Edit | Scans for API keys, tokens, passwords |
| `post-tool-use-ruff.js` | After Write/Edit | Runs `ruff check --fix` on edited Python files |
| `post-tool-use-mypy.js` | After Write/Edit | Runs `mypy` on edited Python files |
| `session-start-load-context.js` | Session start | Shows branch, commit, app count, migration status |
| `stop-pytest-smoke.js` | Session end | Runs `pytest -q -m unit` if code was changed |

### MCP Servers

| Server | Purpose | What it enables |
|---|---|---|
| **Neon** | Production PostgreSQL | Run SQL, manage branches, check slow queries |
| **GitHub** | Repository operations | PRs, issues, code search, file operations |
| **Context7** | Library documentation | Up-to-date docs for any library |
| **Playwright** | Browser testing | E2E tests, screenshots, accessibility checks |

### Plugins

| Plugin | What it does |
|---|---|
| `caveman` | Deliberate thinking mode (forces planning before coding) |
| `code-review` | Code review workflows |
| `feature-dev` | Feature development workflows |
| `frontend-design` | UI/UX design assistance |
| `hookify` | Helps create new hooks |
| `pr-review-toolkit` | PR review tools |
| `security-guidance` | Security best practices |
| `commit-commands` | Commit message formatting |
| `agent-sdk-dev` | Agent development tools |
| `claude-mem` | Cross-session memory (auto-extraction) |

## Commands Reference

### Build & Code

| Command | Description | Example |
|---|---|---|
| `/add-endpoint` | Build a new API endpoint | `/add-endpoint POST /ideas/{id}/share` |
| `/migrate` | Create a migration | `/migrate add_idea_priority` |
| `/schema-change` | Schema change with audit | `/schema-change add is_archived to ideas` |
| `/seed` | Generate test data | `/seed` or `/seed api` |
| `/refactor` | Safe refactoring | `/refactor apps/api/views.py` |

### Quality

| Command | Description | Example |
|---|---|---|
| `/test` | Run tests | `/test` or `/test test_ideas.py` |
| `/lint` | Run ruff | `/lint` or `/lint --fix` |
| `/review` | Review diff | `/review` or `/review apps/api/` |
| `/security-audit` | Security scan | `/security-audit` |
| `/performance-audit` | Find slow queries | `/performance-audit` or `/performance-audit api` |
| `/deploy-check` | Pre-deploy verification | `/deploy-check` or `/deploy-check prod` |

### Git

| Command | Description | Example |
|---|---|---|
| `/commit` | Conventional commit | `/commit` |

### Maintenance

| Command | Description | Example |
|---|---|---|
| `/sync-skills` | Verify skills are in sync | `/sync-skills` |

## Rules (Always Active)

These rules are enforced on every response, no command needed:

| Rule | What it enforces |
|---|---|
| `api-response.md` | JSON responses, correct status codes, Content-Type headers |
| `auth-security.md` | Token auth, no secrets in code, `os.environ` only in settings |
| `database-migrations.md` | Reversible, non-destructive, `apps.get_model()` in RunPython |
| `layered-architecture.md` | Views → Services → Models, no DB calls in views |
| `llm-providers.md` | Provider fallback chain: OpenRouter > ApiFreeLLM > GLM > Vultr |
| `error-handling.md` | Consistent error shapes, proper status codes, no bare Exception |
| `logging.md` | Structured logging, no secrets in logs, Sentry integration |
| `pagination.md` | All list endpoints paginated, cursor for real-time feeds |

## Skills Reference

Skills are loaded when relevant. Each contains code templates, patterns, and anti-patterns:

| Skill | Loaded when | Contains |
|---|---|---|
| `django-models` | Creating/editing models | TimestampedModel, SoftDeleteModel, Meta.indexes |
| `drf-views` | Creating/editing views | ViewSet template, serializers, URL patterns |
| `django-migrations` | Creating migrations | RunPython, apps.get_model(), two-step NOT NULL |
| `django-settings` | Editing settings | 4-file inheritance, env vars, REST_FRAMEWORK |
| `django-auth` | Working with auth | Token auth, allauth, custom permissions |
| `pytest-django` | Writing tests | Fixtures, markers, mock patterns |
| `celery-tasks` | Creating background tasks | Task templates, beat schedules, queue routing |
| `redis-caching` | Adding caching | Cache-aside, view caching, cache warming |
| `llm-provider-fallback` | Working with LLMs | Provider chain, fallback logic |
| `polar-payments` | Adding Polar payments | Webhook handling, checkout flow |
| `stripe-payments` | Adding Stripe payments | Webhook handling, checkout flow |
| `neon-postgres` | Neon-specific work | Branching, connection pooling |
| `security-and-hardening` | Security work | Middleware, throttling, CORS |
| `test-driven-development` | TDD workflow | Red-green-refactor patterns |
| `caveman` | Deliberate thinking | Planning before coding |

## Agents

Agents are delegated to for specific tasks:

| Agent | Invoked by | What it does |
|---|---|---|
| `drf-view-builder` | `/add-endpoint` workflow | Builds views, serializers, URLs |
| `django-migrator` | `/migrate`, `/schema-change` | Creates safe migrations |
| `repo-reviewer` | `/review`, `/refactor` | Reviews code against rules |
| `security-auditor` | `/security-audit`, `/deploy-check` | Audits security |
| `pytest-runner` | `/test`, workflows | Runs and analyzes tests |
| `llm-service-expert` | LLM-related tasks | Reviews LLM service code |
| `data-seed` | `/seed` | Generates test data |
| `deploy-check` | `/deploy-check` | Pre-deployment checklist |
| `query-optimizer` | `/performance-audit` | Finds N+1 queries, missing indexes |

## Workflows

Multi-phase pipelines that compose agents:

| Workflow | Command | Phases |
|---|---|---|
| `add-endpoint` | `/add-endpoint` | Analyze → Plan → Build → Test → Review |
| `db-schema-change` | `/schema-change` | Design → Apply → Test → Audit |
| `security-review` | `/security-audit` | Scan → Verify → Report |
| `refactor-workflow` | `/refactor` | Analyze → Plan → Refactor → Test → Verify |
| `data-migration-workflow` | `/schema-change` (data) | Design → Validate → Migrate → Verify → RollbackReady |
| `performance-audit` | `/performance-audit` | Scan → Measure → Fix → Verify |

## Customization

### Adding a new skill

1. Create `.claude/skills/<name>/SKILL.md`
2. Add entry to `skills.json`
3. Run `/sync-skills` to verify

### Adding a new rule

1. Create `.claude/rules/<name>.md`
2. Reference it in `CLAUDE.md` under "What NOT to do" or conventions

### Adding a new command

1. Create `.claude/commands/<name>.md` with YAML frontmatter:
   ```yaml
   ---
   description: What this command does
   argument-hint: "[optional args]"
   ---
   ```
2. The command is automatically available as `/<name>`

### Adding a new hook

1. Create `.claude/hooks/<name>.js`
2. Add to `settings.json` under the appropriate trigger:
   - `PreToolUse` — before tool calls
   - `PostToolUse` — after tool calls
   - `SessionStart` — when session begins
   - `Stop` — when session ends

### Adding a new agent

1. Create `.claude/agents/<name>.md`
2. Define identity, what it does, how it works, hard rules
3. Reference it in commands or workflows

### Adding a new workflow

1. Create `.claude/workflows/<name>.md` with YAML frontmatter:
   ```yaml
   ---
   name: <name>
   description: What this workflow does
   phases: [Phase1, Phase2, Phase3]
   ---
   ```
2. Each phase should have clear goals and exit criteria
3. Reference it in a command

## File Counts

| Category | Count |
|---|---|
| Skills | 15 |
| Agents | 9 |
| Rules | 8 |
| Commands | 13 |
| Hooks | 5 |
| Templates | 5 |
| Workflows | 6 |
| Config | 3 (CLAUDE.md, settings.json, .mcp.json) |
| **Total** | **65** |

## Adapting for Other Frameworks

This `.claude` setup follows a universal architecture. To adapt for another framework:

1. **Replace CLAUDE.md** — new stack, architecture, conventions
2. **Replace skills/** — framework-specific patterns
3. **Replace agents/** — framework-specific builders
4. **Replace rules/** — framework-specific constraints
5. **Replace commands/** — framework-specific commands
6. **Replace hooks/** — framework-specific tools (eslint instead of ruff, etc.)
7. **Update settings.json** — new tool permissions
8. **Update .mcp.json** — relevant MCP servers

The structure stays the same. Only the content changes.

See the [Stack Mapping Cheat Sheet](#stack-mapping) for framework equivalences.

### Stack Mapping

| Concept | Django | Express.js | FastAPI | Next.js |
|---|---|---|---|---|
| Routes | `urls.py` | `routes/*.ts` | `routers/*.py` | `app/` |
| Views | `views.py` | `controllers/*.ts` | `routers/*.py` | `page.tsx` |
| Models | `models.py` | `models/*.ts` | `models.py` | N/A (API routes) |
| Serializers | `serializers.py` | `schemas/*.ts` (Zod) | `schemas.py` | N/A |
| Services | `services.py` | `services/*.ts` | `services/*.py` | `lib/` |
| Auth | DRF Token + allauth | JWT middleware | OAuth2 + JWT | NextAuth |
| Migrations | `makemigrations` | `migrate-mongo` | Alembic | Prisma |
| Tests | pytest + django | Jest + supertest | pytest | Vitest |
| Lint | ruff | eslint + prettier | ruff | eslint |
| Types | mypy + django-stubs | TypeScript | mypy | TypeScript |
