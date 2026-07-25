# 🚀 CodePilot AI

**AI-powered Repository Assistant** — Chat with your codebase, search semantically, generate documentation, detect bugs, and review pull requests using LLMs and RAG.

![Python](https://img.shields.io/badge/Python-3.12-blue)
![Django](https://img.shields.io/badge/Django-5.1-green)
![React](https://img.shields.io/badge/React-18-61dafb)
![TypeScript](https://img.shields.io/badge/TypeScript-5.7-3178c6)
![License](https://img.shields.io/badge/License-MIT-yellow)

---

## Features

- 💬 **AI Chat** — Ask natural language questions about any repository
- 🔍 **Semantic Search** — Find code by meaning, not just keywords
- 📄 **Documentation Generation** — Auto-generate docs for functions and classes
- 🧪 **Test Generation** — Generate unit tests with framework detection
- 🐛 **Bug Detection** — Identify potential bugs, security issues, and anti-patterns
- 🔗 **GitHub Integration** — Import repos directly from GitHub with OAuth
- 📊 **Repository Analytics** — Language breakdown, complexity metrics, indexing history
- 🌙 **Dark Mode** — Full dark/light theme support

## Tech Stack

| Layer | Technologies |
|-------|-------------|
| **Frontend** | React, TypeScript, Vite, Tailwind CSS, ShadCN UI, React Query, Zustand |
| **Backend** | Django, Django REST Framework, PostgreSQL, JWT Auth, Celery, Redis |
| **AI/ML** | LangChain, Sentence Transformers, OpenAI API, Ollama, RAG |
| **Vector DB** | pgvector (PostgreSQL) — architecture supports Qdrant migration |
| **DevOps** | Docker, GitHub Actions, Vercel, Railway |

## Architecture

```
┌─────────────────────────────────────────────────────┐
│                 React Frontend (Vite)                │
├─────────────────────────────────────────────────────┤
│              Django REST Framework API               │
├───────────┬──────────────┬──────────────────────────┤
│  Celery   │  AI Pipeline │  Embedding Service       │
│  Workers  │  (LangChain) │  (Sentence Transformers) │
├───────────┴──────────────┴──────────────────────────┤
│         PostgreSQL + pgvector  │  Redis              │
└────────────────────────────────┴────────────────────┘
```

## Quick Start

### Prerequisites

- Python 3.12+
- Node.js 20+
- PostgreSQL 16+ (or use SQLite for development)
- Redis (optional, for Celery)

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/codepilot-ai.git
cd codepilot-ai
```

### 2. Backend Setup

```bash
# Create virtual environment
python -m venv .venv

# Activate it
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

# Install dependencies
pip install -r backend/requirements/development.txt

# Copy environment file
cp backend/.env.example backend/.env

# Run migrations
cd backend
python manage.py migrate

# Create admin user (optional)
python manage.py createsuperuser

# Start the server
python manage.py runserver 127.0.0.1:8000
```

### 3. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Start dev server
npm run dev
```

### 4. Open the app

Navigate to `http://localhost:5173`

---

## Project Structure

```
codepilot-ai/
├── backend/                    # Django API
│   ├── config/                 # Project settings (base/dev/prod)
│   ├── apps/
│   │   ├── accounts/           # Auth, users, profiles
│   │   ├── repositories/       # Repository CRUD, file management
│   │   ├── indexing/           # Code parsing, chunking pipeline
│   │   ├── embeddings/         # Vector generation, semantic search
│   │   ├── chat/               # Conversations, messages, RAG
│   │   ├── ai/                 # LLM providers, AI features
│   │   ├── github/             # OAuth, API client, import
│   │   ├── analytics/          # Metrics, usage tracking
│   │   └── common/             # Base models, pagination, utils
│   └── requirements/           # Dependency files
├── frontend/                   # React app
│   ├── src/
│   │   ├── components/         # Shared UI components
│   │   ├── pages/              # Route pages
│   │   ├── services/           # API client
│   │   ├── stores/             # Zustand state
│   │   └── types/              # TypeScript interfaces
│   └── ...
├── docs/                       # Architecture documentation
├── docker-compose.yml          # Local development services
└── Makefile                    # Common commands
```

## API Endpoints

### Authentication
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/accounts/auth/register/` | Register new account |
| POST | `/api/v1/accounts/auth/login/` | Login (returns JWT) |
| POST | `/api/v1/accounts/auth/logout/` | Logout (blacklist token) |
| POST | `/api/v1/accounts/auth/refresh/` | Refresh access token |
| POST | `/api/v1/accounts/auth/password/change/` | Change password |
| GET/PATCH | `/api/v1/accounts/profile/` | User profile |

### Repositories
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET/POST | `/api/v1/repositories/` | List/create repos |
| GET/PATCH/DELETE | `/api/v1/repositories/{id}/` | Repo detail |
| POST | `/api/v1/repositories/{id}/reindex/` | Trigger reindex |
| GET | `/api/v1/repositories/{id}/files/` | Browse files |

### AI Chat
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET/POST | `/api/v1/chat/conversations/` | List/create conversations |
| GET/DELETE | `/api/v1/chat/conversations/{id}/` | Conversation detail |
| POST | `/api/v1/chat/conversations/{id}/messages/` | Send message (RAG) |

### Search & AI Features
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/embeddings/search/` | Semantic code search |
| POST | `/api/v1/ai/explain/` | Explain code |
| POST | `/api/v1/ai/generate-docs/` | Generate documentation |
| POST | `/api/v1/ai/generate-tests/` | Generate unit tests |
| POST | `/api/v1/ai/detect-bugs/` | Detect potential bugs |

### GitHub
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/github/oauth/` | Get OAuth URL |
| POST | `/api/v1/github/callback/` | OAuth callback |
| GET | `/api/v1/github/repos/` | List GitHub repos |
| POST | `/api/v1/github/import/` | Import from GitHub |

## Environment Variables

Create `backend/.env` from the example:

```env
SECRET_KEY=your-secret-key
DEBUG=True
DATABASE_URL=postgres://user:pass@localhost:5432/codepilot  # omit for SQLite
REDIS_URL=redis://localhost:6379/0
CELERY_BROKER_URL=redis://localhost:6379/1
JWT_SECRET_KEY=your-jwt-secret
GITHUB_CLIENT_ID=your-github-client-id
GITHUB_CLIENT_SECRET=your-github-client-secret
OPENAI_API_KEY=sk-your-openai-key
```

## Running Tests

```bash
cd backend

# Run all tests
python -m pytest

# Run with coverage
python -m pytest --cov=apps

# Run specific app tests
python -m pytest apps/accounts/tests/ -v
```

## Docker (Full Stack)

```bash
docker-compose up
```

This starts PostgreSQL, Redis, the Django API, and Celery worker.

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'feat: add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License.

---

Built with ❤️ by [Your Name]
