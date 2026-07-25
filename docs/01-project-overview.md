# CodePilot AI - Project Overview

## Project Vision

CodePilot AI is an intelligent developer assistant that deeply understands entire codebases and enables developers to interact with their repositories through natural language. By leveraging Large Language Models (LLMs) and Retrieval-Augmented Generation (RAG), it transforms how developers navigate, understand, and maintain their code.

The platform bridges the gap between static code repositories and dynamic, context-aware developer assistance — making codebases conversational, searchable, and self-documenting.

## Target Users

| User Segment | Description |
|---|---|
| Individual Developers | Developers who want to quickly understand unfamiliar codebases, generate docs, or find bugs |
| Development Teams | Teams needing shared context about their codebase for onboarding and knowledge sharing |
| Open Source Maintainers | Maintainers who need to review PRs, explain code to contributors, and maintain documentation |
| Technical Leads | Leads who want analytics, code quality insights, and automated reviews |
| DevOps Engineers | Engineers who want to understand infrastructure code and detect misconfigurations |

## Use Cases

### Primary Use Cases
1. **Code Q&A** — Ask natural language questions about any part of a repository
2. **Semantic Code Search** — Find code by meaning, not just keywords
3. **Documentation Generation** — Auto-generate docs for functions, classes, and modules
4. **Code Explanation** — Get plain-english explanations of complex code
5. **Bug Detection** — Identify potential bugs, anti-patterns, and vulnerabilities
6. **Pull Request Review** — AI-assisted code review with contextual suggestions
7. **Unit Test Generation** — Generate test cases for functions and methods
8. **Repository Analytics** — Visualize code complexity, dependencies, and health metrics

### Secondary Use Cases
9. **Repository Import** — Import repos from GitHub or upload manually
10. **Multi-repo Context** — Query across multiple indexed repositories
11. **Conversation History** — Maintain chat context for iterative exploration
12. **Code Refactoring Suggestions** — Get improvement recommendations

## Functional Requirements

### FR-1: Authentication & Authorization
- FR-1.1: Email/password registration and login
- FR-1.2: JWT-based session management with refresh tokens
- FR-1.3: GitHub OAuth integration for repository access
- FR-1.4: Role-based access control (owner, member, viewer)
- FR-1.5: Account settings management (password change, profile update)

### FR-2: Repository Management
- FR-2.1: Import repositories from GitHub (public and private)
- FR-2.2: Manual repository upload (zip/tar)
- FR-2.3: Repository listing with status indicators
- FR-2.4: Repository deletion with cascade cleanup
- FR-2.5: Re-index repository on demand
- FR-2.6: Branch selection for indexing
- FR-2.7: File browser with syntax highlighting

### FR-3: Code Indexing & Embedding
- FR-3.1: Parse repository file tree
- FR-3.2: Filter out binary files, node_modules, build artifacts
- FR-3.3: Chunk source code intelligently (function-level, class-level)
- FR-3.4: Generate embeddings using Sentence Transformers
- FR-3.5: Store embeddings in pgvector
- FR-3.6: Maintain metadata (file path, language, line numbers)
- FR-3.7: Background processing via Celery

### FR-4: AI Chat
- FR-4.1: Natural language chat interface
- FR-4.2: Context-aware responses using RAG
- FR-4.3: Conversation history and memory
- FR-4.4: Code snippets in responses with syntax highlighting
- FR-4.5: Follow-up questions with context retention
- FR-4.6: Multiple AI provider support (OpenAI, Ollama, HuggingFace)

### FR-5: Semantic Search
- FR-5.1: Natural language code search
- FR-5.2: Search results with file path, line numbers, relevance score
- FR-5.3: Filter by language, file type, directory
- FR-5.4: Search across multiple repositories

### FR-6: Documentation Generation
- FR-6.1: Generate docstrings for functions/classes
- FR-6.2: Generate README files
- FR-6.3: Generate API documentation
- FR-6.4: Export documentation in Markdown format

### FR-7: Code Analysis
- FR-7.1: Bug detection with severity levels
- FR-7.2: Code explanation for selected functions
- FR-7.3: Unit test generation
- FR-7.4: Code complexity analysis
- FR-7.5: Dependency analysis

### FR-8: Pull Request Review
- FR-8.1: Fetch PR diffs from GitHub
- FR-8.2: AI-powered review comments
- FR-8.3: Security vulnerability detection
- FR-8.4: Style and best practice suggestions

### FR-9: Analytics
- FR-9.1: Repository size and language breakdown
- FR-9.2: Code complexity metrics
- FR-9.3: Indexing history and status
- FR-9.4: Chat usage statistics
- FR-9.5: Embedding coverage percentage

## Non-Functional Requirements

### NFR-1: Performance
- API response time < 200ms for standard endpoints
- AI chat response time < 5 seconds (streaming)
- Repository indexing: < 5 minutes for repos up to 10,000 files
- Semantic search: < 1 second for results
- Support 1000 concurrent users

### NFR-2: Scalability
- Horizontal scaling for API servers
- Worker pool scaling for indexing tasks
- Vector database partitioning per repository
- Stateless API design for load balancing
- CDN for static frontend assets

### NFR-3: Security
- All data encrypted in transit (TLS 1.3)
- Secrets stored in environment variables (never in code)
- Repository isolation — users can only access their own repos
- Rate limiting on all endpoints
- Input sanitization and validation
- Prompt injection mitigation for AI features
- OWASP Top 10 compliance

### NFR-4: Reliability
- 99.9% uptime target
- Graceful degradation when AI services are unavailable
- Retry logic for external API calls
- Dead letter queue for failed background tasks
- Health check endpoints

### NFR-5: Maintainability
- Modular architecture with clear separation of concerns
- Comprehensive test coverage (>80%)
- API versioning
- Database migration strategy
- Structured logging
- Documentation for all modules

### NFR-6: Usability
- Responsive design (mobile, tablet, desktop)
- Dark mode support
- Keyboard shortcuts
- Loading states and progress indicators
- Error messages with actionable guidance
- Accessibility (WCAG 2.1 AA)

## Scalability Considerations

1. **Vector Storage** — Start with pgvector, architecture supports migration to Qdrant for dedicated vector workloads
2. **Background Processing** — Celery with Redis broker, auto-scaling workers based on queue depth
3. **Caching** — Redis for API response caching, embedding cache, and session storage
4. **Database** — Read replicas for analytics queries, connection pooling
5. **File Storage** — Local first, S3-compatible for production
6. **CDN** — Static assets served via Vercel Edge Network
7. **Rate Limiting** — Token bucket algorithm per user, per endpoint

## Security Considerations

1. **Authentication** — JWT with short-lived access tokens (15 min) and long-lived refresh tokens (7 days)
2. **Repository Isolation** — All queries scoped to user's repositories, no cross-tenant data access
3. **GitHub Token Storage** — Encrypted at rest, never exposed in API responses
4. **Prompt Injection** — System prompts with guardrails, output sanitization
5. **File Upload** — Virus scanning, size limits, type validation
6. **API Security** — CORS, CSRF protection, rate limiting, input validation
7. **Secrets** — Environment variables, never committed to source control

## Architecture Decisions

| Decision | Choice | Rationale |
|---|---|---|
| Frontend Framework | React + TypeScript | Industry standard, strong ecosystem, type safety |
| Build Tool | Vite | Fast builds, excellent DX, ESM-native |
| UI Library | ShadCN + Tailwind | Customizable, accessible, design-system ready |
| Backend Framework | Django + DRF | Batteries included, ORM, admin, migrations |
| Database | PostgreSQL + pgvector | Single database for relational + vector data |
| Task Queue | Celery + Redis | Battle-tested, scalable, monitoring tools |
| AI Framework | LangChain | Unified interface for multiple LLM providers |
| Embeddings | Sentence Transformers | Local inference, no API costs for embeddings |
| Auth | JWT (djangorestframework-simplejwt) | Stateless, scalable, standard |
| Deployment | Docker + Railway/Render | Container-first, easy horizontal scaling |
