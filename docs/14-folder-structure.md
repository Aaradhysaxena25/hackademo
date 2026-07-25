# CodePilot AI - Folder Structure & Coding Standards

## Project Root Structure

```
codepilot-ai/
├── backend/                    # Django backend
├── frontend/                   # React frontend
├── docs/                       # Project documentation
├── .github/                    # GitHub Actions workflows
├── docker-compose.yml          # Development environment
├── docker-compose.prod.yml     # Production override
├── Makefile                    # Common commands
├── README.md                   # Project README
├── .gitignore                  # Git ignore rules
└── .env.example                # Environment template
```

## Backend Structure

```
backend/
├── config/                     # Project configuration
│   ├── __init__.py
│   ├── settings/
│   │   ├── __init__.py
│   │   ├── base.py             # Shared settings
│   │   ├── development.py      # Dev overrides
│   │   ├── production.py       # Prod overrides
│   │   └── testing.py          # Test overrides
│   ├── urls.py                 # Root URL configuration
│   ├── wsgi.py                 # WSGI entry point
│   ├── asgi.py                 # ASGI entry point
│   └── celery.py               # Celery configuration
│
├── apps/                       # Django applications
│   ├── __init__.py
│   ├── accounts/
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── managers.py
│   │   ├── models.py
│   │   ├── permissions.py
│   │   ├── serializers.py
│   │   ├── signals.py
│   │   ├── tokens.py
│   │   ├── urls.py
│   │   ├── validators.py
│   │   ├── views.py
│   │   ├── tests/
│   │   │   ├── __init__.py
│   │   │   ├── test_models.py
│   │   │   ├── test_views.py
│   │   │   └── test_serializers.py
│   │   └── migrations/
│   │
│   ├── repositories/
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── filters.py
│   │   ├── models.py
│   │   ├── permissions.py
│   │   ├── serializers.py
│   │   ├── services.py
│   │   ├── urls.py
│   │   ├── validators.py
│   │   ├── views.py
│   │   ├── tests/
│   │   └── migrations/
│   │
│   ├── indexing/
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── constants.py
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── tasks.py
│   │   ├── urls.py
│   │   ├── views.py
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   ├── chunker.py
│   │   │   ├── file_filter.py
│   │   │   ├── language_detector.py
│   │   │   ├── metadata_extractor.py
│   │   │   └── parser.py
│   │   ├── tests/
│   │   └── migrations/
│   │
│   ├── embeddings/
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── tasks.py
│   │   ├── urls.py
│   │   ├── views.py
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   ├── generator.py
│   │   │   ├── reranker.py
│   │   │   └── search.py
│   │   ├── tests/
│   │   └── migrations/
│   │
│   ├── chat/
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── consumers.py
│   │   ├── models.py
│   │   ├── permissions.py
│   │   ├── routing.py
│   │   ├── serializers.py
│   │   ├── services.py
│   │   ├── urls.py
│   │   ├── views.py
│   │   ├── tests/
│   │   └── migrations/
│   │
│   ├── ai/
│   │   ├── __init__.py
│   │   ├── apps.py
│   │   ├── serializers.py
│   │   ├── tasks.py
│   │   ├── urls.py
│   │   ├── views.py
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   ├── bug_detector.py
│   │   │   ├── code_explainer.py
│   │   │   ├── doc_generator.py
│   │   │   ├── huggingface_provider.py
│   │   │   ├── llm_provider.py
│   │   │   ├── ollama_provider.py
│   │   │   ├── openai_provider.py
│   │   │   ├── pr_reviewer.py
│   │   │   ├── prompt_builder.py
│   │   │   ├── rag_pipeline.py
│   │   │   └── test_generator.py
│   │   ├── prompts/
│   │   │   ├── __init__.py
│   │   │   ├── bugs.py
│   │   │   ├── docs.py
│   │   │   ├── explain.py
│   │   │   ├── review.py
│   │   │   ├── system.py
│   │   │   └── tests.py
│   │   ├── tests/
│   │   └── migrations/
│   │
│   ├── github/
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── tasks.py
│   │   ├── urls.py
│   │   ├── views.py
│   │   ├── webhooks.py
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   ├── api_client.py
│   │   │   ├── oauth.py
│   │   │   ├── pr_fetcher.py
│   │   │   └── repo_cloner.py
│   │   ├── tests/
│   │   └── migrations/
│   │
│   ├── analytics/
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── tasks.py
│   │   ├── urls.py
│   │   ├── views.py
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   ├── aggregator.py
│   │   │   ├── metrics_calculator.py
│   │   │   └── usage_tracker.py
│   │   ├── tests/
│   │   └── migrations/
│   │
│   ├── notifications/
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── consumers.py
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── services/
│   │   ├── tasks.py
│   │   ├── templates/emails/
│   │   ├── urls.py
│   │   ├── views.py
│   │   ├── tests/
│   │   └── migrations/
│   │
│   ├── common/
│   │   ├── __init__.py
│   │   ├── constants.py
│   │   ├── decorators.py
│   │   ├── exceptions.py
│   │   ├── middleware.py
│   │   ├── mixins.py
│   │   ├── models.py
│   │   ├── pagination.py
│   │   ├── permissions.py
│   │   ├── serializers.py
│   │   ├── utils.py
│   │   └── validators.py
│   │
│   └── core/
│       ├── __init__.py
│       ├── enums.py
│       ├── events.py
│       └── interfaces/
│           ├── __init__.py
│           ├── embedding_interface.py
│           ├── llm_interface.py
│           ├── search_interface.py
│           └── storage_interface.py
│
├── requirements/
│   ├── base.txt                # Core dependencies
│   ├── development.txt         # Dev dependencies
│   └── production.txt          # Prod dependencies
│
├── storage/                    # Local file storage (gitignored)
├── scripts/                    # Management scripts
├── fixtures/                   # Test data fixtures
├── pytest.ini                  # Pytest configuration
├── setup.cfg                   # Tool configuration
├── pyproject.toml              # Python project config
├── Dockerfile                  # Production Dockerfile
├── Dockerfile.dev              # Development Dockerfile
└── manage.py                   # Django management
```

## Frontend Structure

```
frontend/
├── public/
│   ├── favicon.ico
│   └── robots.txt
│
├── src/
│   ├── main.tsx                # Entry point
│   ├── App.tsx                 # Root component
│   ├── vite-env.d.ts           # Vite type declarations
│   │
│   ├── assets/                 # Static assets
│   │   ├── images/
│   │   └── fonts/
│   │
│   ├── components/             # Shared components
│   │   ├── ui/                 # ShadCN UI components
│   │   │   ├── button.tsx
│   │   │   ├── card.tsx
│   │   │   ├── input.tsx
│   │   │   ├── dialog.tsx
│   │   │   └── ...
│   │   ├── layout/
│   │   │   ├── AppLayout.tsx
│   │   │   ├── Sidebar.tsx
│   │   │   ├── Navbar.tsx
│   │   │   └── Footer.tsx
│   │   ├── common/
│   │   │   ├── LoadingSkeleton.tsx
│   │   │   ├── EmptyState.tsx
│   │   │   ├── ErrorBoundary.tsx
│   │   │   ├── Badge.tsx
│   │   │   └── ProgressBar.tsx
│   │   └── code/
│   │       ├── CodeBlock.tsx
│   │       ├── MonacoEditor.tsx
│   │       └── SyntaxHighlighter.tsx
│   │
│   ├── pages/                  # Page components
│   │   ├── Landing/
│   │   │   ├── LandingPage.tsx
│   │   │   ├── Hero.tsx
│   │   │   ├── Features.tsx
│   │   │   └── HowItWorks.tsx
│   │   ├── Auth/
│   │   │   ├── LoginPage.tsx
│   │   │   ├── RegisterPage.tsx
│   │   │   └── ForgotPasswordPage.tsx
│   │   ├── Dashboard/
│   │   │   ├── DashboardPage.tsx
│   │   │   ├── StatsCards.tsx
│   │   │   └── RecentActivity.tsx
│   │   ├── Repositories/
│   │   │   ├── RepositoryListPage.tsx
│   │   │   ├── RepositoryDetailPage.tsx
│   │   │   ├── ImportPage.tsx
│   │   │   ├── RepoCard.tsx
│   │   │   └── FileBrowser.tsx
│   │   ├── Chat/
│   │   │   ├── ChatPage.tsx
│   │   │   ├── ConversationList.tsx
│   │   │   ├── MessageList.tsx
│   │   │   ├── MessageBubble.tsx
│   │   │   ├── ChatInput.tsx
│   │   │   └── SourceReference.tsx
│   │   ├── Search/
│   │   │   ├── SearchPage.tsx
│   │   │   ├── SearchInput.tsx
│   │   │   ├── SearchFilters.tsx
│   │   │   └── SearchResultCard.tsx
│   │   ├── CodeViewer/
│   │   │   ├── CodeViewerPage.tsx
│   │   │   ├── AIActions.tsx
│   │   │   └── ChunkOverlay.tsx
│   │   ├── Analytics/
│   │   │   ├── AnalyticsPage.tsx
│   │   │   └── Charts.tsx
│   │   ├── Settings/
│   │   │   ├── SettingsPage.tsx
│   │   │   ├── ProfileTab.tsx
│   │   │   ├── AccountTab.tsx
│   │   │   ├── AIConfigTab.tsx
│   │   │   └── GitHubTab.tsx
│   │   └── NotFound/
│   │       └── NotFoundPage.tsx
│   │
│   ├── hooks/                  # Custom React hooks
│   │   ├── useAuth.ts
│   │   ├── useRepositories.ts
│   │   ├── useConversations.ts
│   │   ├── useSearch.ts
│   │   ├── useTheme.ts
│   │   ├── useDebounce.ts
│   │   └── useWebSocket.ts
│   │
│   ├── services/               # API services
│   │   ├── api.ts              # Axios instance
│   │   ├── auth.ts             # Auth API calls
│   │   ├── repositories.ts    # Repository API calls
│   │   ├── chat.ts             # Chat API calls
│   │   ├── search.ts           # Search API calls
│   │   ├── ai.ts               # AI feature API calls
│   │   └── github.ts           # GitHub API calls
│   │
│   ├── stores/                 # State management
│   │   ├── authStore.ts        # Auth context/store
│   │   ├── themeStore.ts       # Theme state
│   │   └── uiStore.ts          # UI state (sidebar, modals)
│   │
│   ├── types/                  # TypeScript types
│   │   ├── auth.ts
│   │   ├── repository.ts
│   │   ├── chat.ts
│   │   ├── search.ts
│   │   ├── ai.ts
│   │   └── common.ts
│   │
│   ├── utils/                  # Utility functions
│   │   ├── cn.ts               # className utility
│   │   ├── format.ts           # Date, number formatting
│   │   ├── validation.ts       # Zod schemas
│   │   └── constants.ts        # App constants
│   │
│   ├── lib/                    # Library configurations
│   │   └── queryClient.ts      # React Query config
│   │
│   └── styles/
│       └── globals.css         # Global styles + Tailwind
│
├── tests/                      # Test files
│   ├── setup.ts                # Test setup
│   ├── components/
│   ├── hooks/
│   ├── pages/
│   └── utils/
│
├── e2e/                        # Playwright E2E tests
│   ├── auth.spec.ts
│   ├── chat.spec.ts
│   └── repository.spec.ts
│
├── index.html                  # HTML entry point
├── vite.config.ts              # Vite configuration
├── tsconfig.json               # TypeScript config
├── tsconfig.node.json          # Node TypeScript config
├── tailwind.config.ts          # Tailwind configuration
├── postcss.config.js           # PostCSS config
├── eslint.config.js            # ESLint config
├── prettier.config.js          # Prettier config
├── playwright.config.ts        # Playwright config
├── vitest.config.ts            # Vitest config
├── package.json
├── pnpm-lock.yaml
├── Dockerfile                  # Production Dockerfile
├── Dockerfile.dev              # Development Dockerfile
└── nginx.conf                  # Nginx config for prod
```

---

## Naming Conventions

### Backend (Python/Django)

| Item | Convention | Example |
|---|---|---|
| Files | snake_case | `user_manager.py` |
| Classes | PascalCase | `RepositoryViewSet` |
| Functions | snake_case | `get_user_by_id()` |
| Variables | snake_case | `total_files` |
| Constants | UPPER_SNAKE_CASE | `MAX_FILE_SIZE` |
| Models | PascalCase, singular | `Repository` |
| Serializers | PascalCase + Serializer | `RepositoryCreateSerializer` |
| Views | PascalCase + ViewSet/View | `RepositoryViewSet` |
| URLs | kebab-case | `auth/password/change` |
| Apps | snake_case, plural where applicable | `repositories`, `accounts` |
| Tests | test_ prefix | `test_create_repository` |
| Migrations | auto-generated | `0001_initial.py` |

### Frontend (TypeScript/React)

| Item | Convention | Example |
|---|---|---|
| Files (Components) | PascalCase.tsx | `ChatInput.tsx` |
| Files (Hooks) | camelCase.ts | `useAuth.ts` |
| Files (Utils) | camelCase.ts | `format.ts` |
| Files (Types) | camelCase.ts | `repository.ts` |
| Components | PascalCase | `MessageBubble` |
| Hooks | use + PascalCase | `useRepositories` |
| Functions | camelCase | `formatDate()` |
| Variables | camelCase | `isLoading` |
| Constants | UPPER_SNAKE_CASE | `API_BASE_URL` |
| Types/Interfaces | PascalCase | `Repository`, `ChatMessage` |
| Enums | PascalCase | `RepoStatus` |
| CSS Classes | kebab-case (Tailwind) | `bg-primary-500` |
| Test Files | *.test.tsx | `ChatInput.test.tsx` |
| E2E Files | *.spec.ts | `auth.spec.ts` |

---

## Coding Standards

### Python / Django

```python
# 1. Imports ordered: stdlib → third-party → Django → local
import uuid
from datetime import timedelta

from celery import shared_task
from rest_framework import serializers, status
from rest_framework.response import Response

from django.conf import settings
from django.db import models

from apps.common.models import BaseModel
from apps.repositories.models import Repository

# 2. Type hints on all function signatures
def generate_embeddings(chunks: list[CodeChunk], batch_size: int = 32) -> list[np.ndarray]:
    """Generate embeddings for a list of code chunks."""
    ...

# 3. Docstrings on all public classes and functions
class RepositoryViewSet(ModelViewSet):
    """
    ViewSet for repository CRUD operations.
    
    Supports list, create, retrieve, and delete actions.
    All operations scoped to authenticated user's repositories.
    """
    ...

# 4. No logic in views - delegate to services
class RepositoryViewSet(ModelViewSet):
    def perform_create(self, serializer):
        repo = repository_service.create_repository(
            user=self.request.user,
            **serializer.validated_data
        )
        return repo

# 5. Explicit is better than implicit
# Bad
def process(data):
    ...

# Good
def process_repository_files(repository: Repository, file_paths: list[str]) -> ProcessingResult:
    ...
```

### TypeScript / React

```typescript
// 1. Explicit return types on exported functions
export function useRepositories(): UseRepositoriesReturn {
  ...
}

// 2. Interface over type for object shapes
interface Repository {
  id: string;
  name: string;
  status: RepoStatus;
  totalFiles: number;
}

// 3. Props interface named ComponentNameProps
interface ChatInputProps {
  onSend: (message: string) => void;
  isLoading: boolean;
  placeholder?: string;
}

// 4. Destructure props
export function ChatInput({ onSend, isLoading, placeholder }: ChatInputProps) {
  ...
}

// 5. Custom hooks for logic extraction
// Bad: logic in component
function ChatPage() {
  const [messages, setMessages] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  // 50 lines of data fetching logic...
}

// Good: logic in hook
function ChatPage() {
  const { messages, isLoading, sendMessage } = useChat(conversationId);
  // Clean render logic only
}

// 6. Error boundaries around feature sections
<ErrorBoundary fallback={<ChatError />}>
  <ChatPage />
</ErrorBoundary>
```

---

## Git Workflow

### Branch Strategy: GitHub Flow (simplified)

```
main          ─────●─────────●─────────●─── (production)
                   │         │         │
feature/auth  ────┘         │         │
feature/repos  ─────────────┘         │
feature/chat   ────────────────────────┘
```

### Branch Naming
```
feature/{milestone}-{description}   → feature/auth-login-endpoint
bugfix/{issue-number}-{description} → bugfix/42-token-refresh
hotfix/{description}                → hotfix/cors-header
chore/{description}                 → chore/update-deps
docs/{description}                  → docs/api-specification
```

### Commit Conventions (Conventional Commits)
```
feat: add repository import endpoint
fix: resolve token refresh race condition
docs: update API specification
style: format with ruff
refactor: extract embedding service
test: add indexing pipeline tests
chore: update dependencies
perf: optimize vector search query
ci: add deployment workflow
```

### Commit Message Format
```
<type>(<scope>): <description>

[optional body]

[optional footer]
```

Examples:
```
feat(auth): add JWT token refresh with rotation

Implement refresh token rotation where each refresh
issues a new token pair and blacklists the old refresh token.

Closes #15

---

fix(indexing): handle empty files without crashing

Files with zero bytes were causing a division by zero
in the progress calculation.

Fixes #23
```

### PR Rules
1. All PRs require at least one review
2. CI must pass (lint + tests)
3. Branch must be up to date with main
4. PR description must include: what, why, testing done
5. No direct pushes to main

---

## Documentation Standards

### Code Documentation
- All public functions and classes have docstrings
- Complex algorithms have inline comments explaining "why", not "what"
- API endpoints documented with request/response examples
- README per Django app explaining responsibilities

### Project Documentation (in /docs)
- Architecture Decision Records (ADRs) for significant choices
- API changelog for breaking changes
- Deployment runbook for operations team
- Troubleshooting guide for common issues

### ADR Format
```markdown
# ADR-001: Use pgvector for vector storage

## Status
Accepted

## Context
We need vector storage for code embeddings (384 dimensions, ~100K vectors per repo).

## Decision
Use pgvector extension within PostgreSQL.

## Consequences
- Positive: Single database, simpler ops, transactions with relational data
- Negative: May need migration to Qdrant at scale (>10M vectors)
- Mitigation: Abstract vector storage behind interface
```

---

## Risk Analysis

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| LLM API downtime | Medium | High | Fallback to Ollama, graceful degradation |
| pgvector performance at scale | Low | High | Monitor query times, Qdrant migration path |
| GitHub API rate limits | Medium | Medium | Caching, exponential backoff, queue system |
| Large repo OOM during indexing | Medium | Medium | Streaming processing, chunk limits, memory monitoring |
| Prompt injection attacks | High | Medium | Input sanitization, output validation, guardrails |
| Token costs spiral | Medium | High | Usage limits, caching, local models for embeddings |
| Data breach (GitHub tokens) | Low | Critical | Encryption at rest, minimal permissions, audit logging |
| Celery task failures | Medium | Medium | Retry logic, dead letter queue, alerting |

---

## Future Enhancements

### Phase 2 (Post-Launch)
- Multi-user workspaces and team features
- Real-time collaborative chat
- Custom AI model fine-tuning per repo
- VS Code extension
- CLI tool for local usage
- Webhook integrations (Slack, Discord)
- GitLab / Bitbucket support

### Phase 3 (Scale)
- Dedicated vector database (Qdrant)
- Multi-tenant architecture
- Enterprise SSO (SAML)
- Self-hosted option
- Custom embedding model training
- Cross-repository knowledge graph
- Code generation features
- Automated PR creation from chat
