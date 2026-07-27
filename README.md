# 🚀 CodePilot AI

**AI-powered Repository Assistant** — Chat with your codebase, search semantically, generate documentation, detect bugs, and review pull requests using LLMs and RAG.

![Python](https://img.shields.io/badge/Python-3.12-blue)
![Django](https://img.shields.io/badge/Django-5.1-green)
![React](https://img.shields.io/badge/React-18-61dafb)
![TypeScript](https://img.shields.io/badge/TypeScript-5.7-3178c6)
![Tests](https://img.shields.io/badge/Tests-157%20passing-brightgreen)
![License](https://img.shields.io/badge/License-MIT-yellow)

---

## Features

- 💬 **AI Chat** — Ask natural language questions about any repository
- 🔍 **Semantic Search** — Find code by meaning, not just keywords
- 📄 **Documentation Generation** — Auto-generate docs for functions and classes
- 🧪 **Test Generation** — Generate unit tests with framework auto-detection
- 🐛 **Bug Detection** — Identify potential bugs, security issues, and anti-patterns
- 🔗 **GitHub Integration** — Import repos directly from GitHub with OAuth
- 📊 **Repository Analytics** — Language breakdown, complexity metrics, indexing history
- 🌙 **Dark Mode** — Full dark/light theme support
- 🔐 **JWT Auth** — Secure token-based authentication with refresh rotation

## Tech Stack

| Layer | Technologies |
|-------|-------------|
| **Frontend** | React 18, TypeScript, Vite, Tailwind CSS, ShadCN UI, React Query, Zustand |
| **Backend** | Django 5.1, Django REST Framework, JWT Auth, Celery, Redis |
| **AI/ML** | Groq (free dev) / OpenAI (prod), Sentence Transformers, RAG Pipeline |
| **Database** | PostgreSQL + pgvector (prod) / SQLite (dev) |
| **DevOps** | Docker, GitHub Actions CI, Vercel, Railway |

## Architecture

```
┌─────────────────────────────────────────────────────┐
│              React Frontend (Vite + TS)              │
├─────────────────────────────────────────────────────┤
│              Django REST Framework API               │
├───────────┬──────────────┬──────────────────────────┤
│  Celery   │  RAG Pipeline│  Embedding Service       │
│  Workers  │  (Groq/GPT)  │  (Sentence Transformers) │
├───────────┴──────────────┴──────────────────────────┤
│     PostgreSQL + pgvector    │    Redis (Celery)     │
└──────────────────────────────┴──────────────────────┘
```

---

## Quick Start

### Prerequisites

- Python 3.12+
- Node.js 20+
- (Optional) Redis — for background tasks
- (Optional) PostgreSQL — defaults to SQLite for dev

### 1. Clone

```bash
git clone https://github.com/yourusername/codepilot-ai.git
cd codepilot-ai
```

### 2. Backend Setup

```bash
# Create virtual environment
python -m venv .venv

# Activate
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

# Install dependencies
pip install -r backend/requirements/development.txt

# Configure environment
cp backend/.env.example backend/.env
# Edit .env with your keys (see Configuration section below)

# Run migrations
cd backend
python manage.py migrate

# Start server
python manage.py runserver 127.0.0.1:8000
```

### 3. Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

### 4. Open the app

Navigate to **http://localhost:5173**

---

## Configuration

Edit `backend/.env` — here's what you need:

### Minimum (app works with just these):

```env
SECRET_KEY=any-random-string-here
JWT_SECRET_KEY=another-random-string
LLM_PROVIDER=groq
GROQ_API_KEY=gsk_your_key_here
```

### Get Your Free Groq Key (2 minutes):

1. Go to [console.groq.com/keys](https://console.groq.com/keys)
2. Sign up (free, no credit card)
3. Click "Create API Key"
4. Paste into `GROQ_API_KEY`

That's it — you now have free AI chat with your code.

### Full Configuration Reference:

| Variable | Required | Description |
|----------|----------|-------------|
| `SECRET_KEY` | ✅ | Django secret key (any random string) |
| `JWT_SECRET_KEY` | ✅ | JWT signing key (any random string) |
| `LLM_PROVIDER` | ✅ | `groq` (free), `openai` (paid), `ollama` (local), `mock` (no AI) |
| `GROQ_API_KEY` | For Groq | Free at [console.groq.com](https://console.groq.com/keys) |
| `OPENAI_API_KEY` | For OpenAI | Paid at [platform.openai.com](https://platform.openai.com/api-keys) |
| `GITHUB_CLIENT_ID` | For GitHub import | [github.com/settings/developers](https://github.com/settings/developers) |
| `GITHUB_CLIENT_SECRET` | For GitHub import | Same as above |
| `DATABASE_URL` | For PostgreSQL | Omit to use SQLite |
| `REDIS_URL` | For background tasks | `redis://localhost:6379/0` |

### Switching from Development to Production:

```env
# Just change these two lines:
LLM_PROVIDER=openai
OPENAI_API_KEY=sk-your-production-key
```

---

## Project Structure

```
codepilot-ai/
├── backend/                    # Django API (11 apps)
│   ├── config/                 # Settings (base/dev/prod), URLs, Celery
│   ├── apps/
│   │   ├── accounts/           # Auth, JWT, email verification
│   │   ├── repositories/       # Repo CRUD, file upload, browsing
│   │   ├── indexing/           # Code parsing, AST chunking, job tracking
│   │   ├── embeddings/         # Vector generation, semantic search
│   │   ├── chat/               # Conversations, RAG chat, SSE streaming
│   │   ├── ai/                 # LLM providers (Groq/OpenAI/Ollama), AI features
│   │   ├── github/             # OAuth, API client, repo import
│   │   ├── analytics/          # Usage metrics, activity tracking
│   │   ├── notifications/      # In-app notifications
│   │   ├── common/             # Base models, pagination, health check
│   │   └── core/               # Shared enums and constants
│   ├── requirements/           # base.txt, development.txt, production.txt
│   ├── ARCHITECTURE.md         # Detailed app-by-app documentation
│   └── Dockerfile              # Production image
├── frontend/                   # React SPA
│   ├── src/
│   │   ├── components/         # UI components (ShadCN-based)
│   │   ├── pages/              # Landing, Auth, Dashboard, Chat, Search, Settings
│   │   ├── services/           # API client with auth interceptors
│   │   ├── hooks/              # React Query hooks
│   │   ├── stores/             # Zustand (auth, theme)
│   │   └── types/              # TypeScript interfaces
│   └── ...
├── docs/                       # Architecture documentation
├── .github/workflows/ci.yml    # GitHub Actions (lint + test + build)
├── docker-compose.yml          # Local dev (PostgreSQL + Redis)
└── Makefile                    # Convenience commands
```

---

## API Endpoints

### Authentication
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/accounts/auth/register/` | Register (returns JWT) |
| POST | `/api/v1/accounts/auth/login/` | Login (returns JWT) |
| POST | `/api/v1/accounts/auth/logout/` | Logout (blacklist token) |
| POST | `/api/v1/accounts/auth/refresh/` | Refresh access token |
| POST | `/api/v1/accounts/auth/verify/send/` | Send verification email |
| POST | `/api/v1/accounts/auth/verify/` | Verify email |

### Repositories
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET/POST | `/api/v1/repositories/` | List / create repos |
| POST | `/api/v1/repositories/upload/` | Upload ZIP + auto-index |
| GET/PATCH/DELETE | `/api/v1/repositories/{id}/` | Repo detail |
| POST | `/api/v1/repositories/{id}/reindex/` | Trigger reindex |
| GET | `/api/v1/repositories/{id}/files/` | Browse files |

### AI Chat
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET/POST | `/api/v1/chat/conversations/` | List / create conversations |
| POST | `/api/v1/chat/conversations/{id}/messages/` | Send message (sync) |
| POST | `/api/v1/chat/conversations/{id}/messages/stream/` | Send message (SSE streaming) |

### Search & AI Features
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/embeddings/search/` | Semantic code search |
| POST | `/api/v1/ai/explain/` | Explain code |
| POST | `/api/v1/ai/generate-docs/` | Generate documentation |
| POST | `/api/v1/ai/generate-tests/` | Generate unit tests |
| POST | `/api/v1/ai/detect-bugs/` | Detect bugs |

### GitHub
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/github/oauth/` | Get OAuth URL |
| POST | `/api/v1/github/callback/` | OAuth callback |
| GET | `/api/v1/github/repos/` | List GitHub repos |
| POST | `/api/v1/github/import/` | Import from GitHub |

### System
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/health/` | Health check (no auth) |
| GET | `/api/v1/analytics/dashboard/` | User stats |

---

## Running Tests

```bash
cd backend

# Run all tests (157 tests)
python -m pytest

# Run with coverage
python -m pytest --cov=apps

# Run specific app
python -m pytest apps/accounts/tests/ -v

# Run with output
python -m pytest -s
```

## Linting

```bash
cd backend
ruff check . --exclude "migrations/"
ruff format .
```

## Docker (Full Stack)

```bash
docker-compose up
```

Starts: PostgreSQL (pgvector), Redis, Django API, Celery worker.

---

## AI Provider Comparison

| Provider | Cost | Speed | Quality | Best For |
|----------|------|-------|---------|----------|
| **Groq** | Free | Very fast (800 tok/s) | Good | Development, testing |
| **OpenAI** | $0.15-2.50/1M tokens | Fast | Excellent | Production |
| **Ollama** | Free (local) | Depends on GPU | Varies | Offline, privacy |
| **Mock** | Free | Instant | N/A | CI, testing |

---

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit (`git commit -m 'feat: add amazing feature'`)
4. Push (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Commit Convention
```
feat: new feature
fix: bug fix
docs: documentation
style: formatting
refactor: code restructuring
test: adding tests
chore: maintenance
```

---

## License

MIT License — see [LICENSE](LICENSE) for details.

---

Built with ❤️ using Django, React, and AI
