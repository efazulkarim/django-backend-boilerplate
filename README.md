# Django Backend Boilerplate

A production-ready Django API with Celery, Temporal, and WebSockets.

## Features

- Django 6.0 with Python 3.12+
- Django REST Framework (DRF) with OpenAPI 3.0 (drf-spectacular)
- Django-allauth for authentication (session-based)
- Celery for background tasks (configured with RabbitMQ broker in production)
- Temporal for durable workflows
- Django Channels for WebSockets (Redis channel layer)
- PostgreSQL database (with Prometheus query metrics backend in production)
- Redis for caching (production-ready `django-redis` with connection pool) and sessions
- Sentry for error tracking
- Robust Health Checks (checks DB, Cache, and Celery broker)
- Structured JSON logging with request ID trace correlation across HTTP calls and Celery tasks
- Prometheus Metrics Exporter (`/metrics`) for system observability

## Prerequisites

- Python 3.12+
- Docker & Docker Compose
- Node.js 20+ (not required for API-only setup)

## Quick Start

1. **Install dependencies**:

   ```bash
   # Using uv (recommended)
   pip install uv
   uv sync --extra dev

   # Or using pip
   pip install -r requirements-dev.txt
   ```

2. **Start services**:

   ```bash
   # Start local development services (Postgres, Redis, RabbitMQ, Mailpit, Temporal, Flower)
   docker compose up -d

   # Or start the full production stack
   docker compose -f docker-compose.prod.yml up -d
   ```

3. **Configure environment**:

   ```bash
   cp .env.example .env
   # Edit .env with your settings
   ```

4. **Run migrations**:

   ```bash
   python manage.py migrate
   ```

5. **Create superuser**:

   ```bash
   python manage.py createsuperuser
   ```

6. **Start development server**:
   ```bash
   python manage.py runserver
   ```

## Services

- Django API: http://localhost:8000
- Admin: http://localhost:8000/admin/
- API Docs (Swagger): http://localhost:8000/api/schema/swagger/
- Mailpit (email testing): http://localhost:8025
- Flower (Celery): http://localhost:5555
- RabbitMQ Management: http://localhost:15672 (guest/guest)
- Temporal UI: http://localhost:8088
- Prometheus Metrics: http://localhost:8000/metrics
- Health Check: http://localhost:8000/health/
- Readiness Check: http://localhost:8000/health/ready/

## Project Structure

```
my-api-project/
├── apps/              # Django applications
│   ├── core/          # Core functionality (health checks)
│   ├── users/         # User authentication
│   └── api/           # REST API endpoints
├── config/            # Django settings
│   └── settings/      # Split settings (base/dev/test/prod)
├── temporal_app/       # Temporal workflows & activities
├── tests/             # Test suite
├── Dockerfile         # Production image
├── docker-compose.yml # Development services
├── manage.py          # Django management
└── pyproject.toml     # Dependencies
```

## Development

### Run Tests

```bash
pytest
```

### Lint & Format

```bash
ruff check .
ruff format .
mypy .
```

### Celery Worker

```bash
celery -A config.celery worker -l INFO
```

### Celery Beat (Scheduler)

```bash
celery -A config.celery beat -l INFO
```

### Temporal Worker

```bash
python temporal_app/run_temporal_worker.py
```

## Documentation

See the `docs/` directory for detailed documentation on:

- API development
- Testing
- Deployment
- Celery & Temporal
- WebSockets

## License

MIT
