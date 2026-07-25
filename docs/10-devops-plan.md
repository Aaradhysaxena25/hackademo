# CodePilot AI - DevOps Plan

## Docker

### Backend Dockerfile
```dockerfile
# backend/Dockerfile
FROM python:3.12-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    git \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements/base.txt requirements/production.txt ./requirements/
RUN pip install --no-cache-dir -r requirements/production.txt

# Copy application code
COPY . .

# Collect static files
RUN python manage.py collectstatic --noinput

# Create non-root user
RUN adduser --disabled-password --gecos '' appuser
USER appuser

EXPOSE 8000

CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "4", "--threads", "2"]
```

### Celery Worker Dockerfile
```dockerfile
# backend/Dockerfile.worker
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    git \
    && rm -rf /var/lib/apt/lists/*

COPY requirements/base.txt requirements/production.txt ./requirements/
RUN pip install --no-cache-dir -r requirements/production.txt

COPY . .

RUN adduser --disabled-password --gecos '' appuser
USER appuser

CMD ["celery", "-A", "config.celery", "worker", "--loglevel=info", "--concurrency=4"]
```

### Frontend Dockerfile
```dockerfile
# frontend/Dockerfile
FROM node:20-alpine AS builder

WORKDIR /app
COPY package.json pnpm-lock.yaml ./
RUN npm install -g pnpm && pnpm install --frozen-lockfile

COPY . .
RUN pnpm build

# Production image
FROM nginx:alpine
COPY --from=builder /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

## Docker Compose

### Development Environment
```yaml
# docker-compose.yml
version: '3.9'

services:
  # PostgreSQL with pgvector
  db:
    image: pgvector/pgvector:pg16
    environment:
      POSTGRES_DB: codepilot
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 5s
      timeout: 5s
      retries: 5

  # Redis
  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 5s
      timeout: 5s
      retries: 5

  # Django API
  api:
    build:
      context: ./backend
      dockerfile: Dockerfile
    command: python manage.py runserver 0.0.0.0:8000
    environment:
      - DJANGO_SETTINGS_MODULE=config.settings.development
      - DATABASE_URL=postgres://postgres:postgres@db:5432/codepilot
      - REDIS_URL=redis://redis:6379/0
      - CELERY_BROKER_URL=redis://redis:6379/1
    ports:
      - "8000:8000"
    volumes:
      - ./backend:/app
      - repo_storage:/app/storage
    depends_on:
      db:
        condition: service_healthy
      redis:
        condition: service_healthy

  # Celery Worker
  celery:
    build:
      context: ./backend
      dockerfile: Dockerfile
    command: celery -A config.celery worker --loglevel=info --concurrency=2
    environment:
      - DJANGO_SETTINGS_MODULE=config.settings.development
      - DATABASE_URL=postgres://postgres:postgres@db:5432/codepilot
      - REDIS_URL=redis://redis:6379/0
      - CELERY_BROKER_URL=redis://redis:6379/1
    volumes:
      - ./backend:/app
      - repo_storage:/app/storage
    depends_on:
      db:
        condition: service_healthy
      redis:
        condition: service_healthy

  # Celery Beat (Scheduler)
  celery-beat:
    build:
      context: ./backend
      dockerfile: Dockerfile
    command: celery -A config.celery beat --loglevel=info
    environment:
      - DJANGO_SETTINGS_MODULE=config.settings.development
      - DATABASE_URL=postgres://postgres:postgres@db:5432/codepilot
      - REDIS_URL=redis://redis:6379/0
      - CELERY_BROKER_URL=redis://redis:6379/1
    volumes:
      - ./backend:/app
    depends_on:
      db:
        condition: service_healthy
      redis:
        condition: service_healthy

  # Frontend (dev server)
  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile.dev
    command: pnpm dev --host
    ports:
      - "5173:5173"
    volumes:
      - ./frontend:/app
      - /app/node_modules
    environment:
      - VITE_API_URL=http://localhost:8000/api/v1

volumes:
  postgres_data:
  redis_data:
  repo_storage:
```

## CI/CD Pipeline

### GitHub Actions Workflow

```yaml
# .github/workflows/ci.yml
name: CI/CD Pipeline

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

env:
  PYTHON_VERSION: '3.12'
  NODE_VERSION: '20'

jobs:
  # Backend Tests
  backend-test:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: pgvector/pgvector:pg16
        env:
          POSTGRES_DB: test_codepilot
          POSTGRES_USER: postgres
          POSTGRES_PASSWORD: postgres
        ports:
          - 5432:5432
        options: --health-cmd pg_isready --health-interval 10s --health-timeout 5s --health-retries 5
      redis:
        image: redis:7-alpine
        ports:
          - 6379:6379
        options: --health-cmd "redis-cli ping" --health-interval 10s --health-timeout 5s --health-retries 5

    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: ${{ env.PYTHON_VERSION }}
          cache: 'pip'

      - name: Install dependencies
        working-directory: ./backend
        run: |
          pip install -r requirements/development.txt

      - name: Run linting
        working-directory: ./backend
        run: |
          ruff check .
          ruff format --check .

      - name: Run type checking
        working-directory: ./backend
        run: |
          mypy apps/

      - name: Run tests
        working-directory: ./backend
        env:
          DATABASE_URL: postgres://postgres:postgres@localhost:5432/test_codepilot
          REDIS_URL: redis://localhost:6379/0
          DJANGO_SETTINGS_MODULE: config.settings.testing
        run: |
          pytest --cov=apps --cov-report=xml --cov-report=term-missing

      - name: Upload coverage
        uses: codecov/codecov-action@v3
        with:
          file: ./backend/coverage.xml
          flags: backend

  # Frontend Tests
  frontend-test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up Node.js
        uses: actions/setup-node@v4
        with:
          node-version: ${{ env.NODE_VERSION }}

      - name: Install pnpm
        run: npm install -g pnpm

      - name: Install dependencies
        working-directory: ./frontend
        run: pnpm install --frozen-lockfile

      - name: Run linting
        working-directory: ./frontend
        run: pnpm lint

      - name: Run type checking
        working-directory: ./frontend
        run: pnpm type-check

      - name: Run tests
        working-directory: ./frontend
        run: pnpm test -- --coverage

      - name: Build
        working-directory: ./frontend
        run: pnpm build

  # Security Scan
  security:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Run Trivy vulnerability scanner
        uses: aquasecurity/trivy-action@master
        with:
          scan-type: 'fs'
          scan-ref: '.'
          severity: 'HIGH,CRITICAL'

      - name: Python safety check
        working-directory: ./backend
        run: |
          pip install safety
          safety check -r requirements/base.txt

  # Deploy (only on main)
  deploy-backend:
    needs: [backend-test, frontend-test, security]
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main' && github.event_name == 'push'
    steps:
      - uses: actions/checkout@v4

      - name: Deploy to Railway
        uses: railway/deploy@v1
        with:
          service: codepilot-api
        env:
          RAILWAY_TOKEN: ${{ secrets.RAILWAY_TOKEN }}

  deploy-frontend:
    needs: [backend-test, frontend-test, security]
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main' && github.event_name == 'push'
    steps:
      - uses: actions/checkout@v4

      - name: Deploy to Vercel
        uses: amondnet/vercel-action@v25
        with:
          vercel-token: ${{ secrets.VERCEL_TOKEN }}
          vercel-org-id: ${{ secrets.VERCEL_ORG_ID }}
          vercel-project-id: ${{ secrets.VERCEL_PROJECT_ID }}
          vercel-args: '--prod'
          working-directory: ./frontend
```

## Environment Variables

### Development (.env.example)
```bash
# Django
SECRET_KEY=your-secret-key-change-in-production
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DJANGO_SETTINGS_MODULE=config.settings.development

# Database
DATABASE_URL=postgres://postgres:postgres@localhost:5432/codepilot

# Redis
REDIS_URL=redis://localhost:6379/0
CELERY_BROKER_URL=redis://localhost:6379/1

# JWT
JWT_SECRET_KEY=your-jwt-secret-key
JWT_ACCESS_TOKEN_LIFETIME=15
JWT_REFRESH_TOKEN_LIFETIME=10080

# GitHub OAuth
GITHUB_CLIENT_ID=your-github-client-id
GITHUB_CLIENT_SECRET=your-github-client-secret
GITHUB_CALLBACK_URL=http://localhost:5173/auth/github/callback

# AI
OPENAI_API_KEY=sk-your-openai-key
OLLAMA_BASE_URL=http://localhost:11434
DEFAULT_LLM_PROVIDER=openai
DEFAULT_LLM_MODEL=gpt-4o-mini
EMBEDDING_MODEL=all-MiniLM-L6-v2

# Storage
STORAGE_BACKEND=local
STORAGE_LOCAL_PATH=./storage

# Encryption
ENCRYPTION_KEY=your-fernet-encryption-key

# Frontend
VITE_API_URL=http://localhost:8000/api/v1
VITE_WS_URL=ws://localhost:8000/ws
```

### Production (Railway/Render Environment)
```bash
SECRET_KEY=<generated-production-key>
DEBUG=False
ALLOWED_HOSTS=api.codepilot.ai
DJANGO_SETTINGS_MODULE=config.settings.production
DATABASE_URL=<neon-postgres-url>
REDIS_URL=<upstash-redis-url>
CELERY_BROKER_URL=<upstash-redis-url>/1
JWT_SECRET_KEY=<production-jwt-key>
GITHUB_CLIENT_ID=<production-github-id>
GITHUB_CLIENT_SECRET=<production-github-secret>
OPENAI_API_KEY=<production-openai-key>
ENCRYPTION_KEY=<production-encryption-key>
CORS_ALLOWED_ORIGINS=https://codepilot.ai,https://app.codepilot.ai
SENTRY_DSN=<sentry-dsn>
```

## Logging

### Configuration
```python
# config/settings/base.py
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'json': {
            '()': 'pythonjsonlogger.jsonlogger.JsonFormatter',
            'format': '%(asctime)s %(levelname)s %(name)s %(message)s',
        },
        'verbose': {
            'format': '{asctime} {levelname} {name} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'json' if not DEBUG else 'verbose',
        },
    },
    'root': {
        'level': 'INFO',
        'handlers': ['console'],
    },
    'loggers': {
        'django': {'level': 'WARNING'},
        'django.request': {'level': 'ERROR'},
        'apps': {'level': 'INFO'},
        'celery': {'level': 'INFO'},
    },
}
```

### Structured Log Format
```json
{
  "asctime": "2024-01-15T10:30:00.000Z",
  "levelname": "INFO",
  "name": "apps.indexing.tasks",
  "message": "Repository indexing completed",
  "repository_id": "uuid",
  "duration_ms": 4500,
  "total_files": 342,
  "total_chunks": 1205
}
```

## Monitoring

### Health Check Endpoints
```python
# /api/v1/health/
{
    "status": "healthy",
    "version": "1.0.0",
    "checks": {
        "database": "ok",
        "redis": "ok",
        "celery": "ok",
        "storage": "ok"
    },
    "uptime_seconds": 86400
}
```

### Monitoring Stack
- **Error Tracking**: Sentry (Python SDK + React SDK)
- **APM**: Sentry Performance Monitoring
- **Uptime**: UptimeRobot / Better Uptime
- **Logs**: Railway/Render built-in log streaming
- **Metrics**: Custom metrics via Prometheus (future)

### Key Metrics to Track
- API response times (p50, p95, p99)
- Error rate by endpoint
- Celery task queue depth
- Celery task duration
- Database connection pool usage
- Redis memory usage
- Embedding generation latency
- LLM API latency
- Active users (DAU/WAU)

## Testing

### Test Configuration
```python
# config/settings/testing.py
from .base import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'test_codepilot',
    }
}

# Speed up tests
PASSWORD_HASHERS = ['django.contrib.auth.hashers.MD5PasswordHasher']
CELERY_TASK_ALWAYS_EAGER = True
CELERY_TASK_EAGER_PROPAGATES = True
```

### pytest Configuration
```ini
# pytest.ini
[pytest]
DJANGO_SETTINGS_MODULE = config.settings.testing
python_files = tests.py test_*.py
python_classes = Test*
python_functions = test_*
addopts = -v --tb=short --strict-markers
markers =
    slow: marks tests as slow
    integration: marks integration tests
    ai: marks AI-related tests
```

## Deployment Strategy

### Blue-Green Deployment
1. Deploy new version alongside existing
2. Run health checks on new deployment
3. Switch traffic to new version
4. Keep old version for quick rollback (5 minutes)

### Database Migrations
1. Migrations run before new code deploys
2. All migrations must be backward compatible
3. Add columns as nullable → deploy code → backfill → add constraint
4. Never drop columns in the same deploy as code removal

### Rollback Plan
1. Revert deployment via Railway/Render dashboard
2. Rollback database migrations if needed (rare)
3. Post-mortem for any production incident

### Deployment Checklist
- [ ] All tests passing in CI
- [ ] Security scan clean
- [ ] Database migrations reviewed
- [ ] Environment variables updated
- [ ] Feature flags configured
- [ ] Monitoring alerts set up
- [ ] Rollback plan documented
