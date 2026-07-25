# CodePilot AI - Testing Strategy

## Testing Pyramid

```
         ┌─────────────┐
         │   E2E Tests  │  < 10%
         │  (Playwright) │
         ├─────────────┤
         │ Integration   │  ~ 30%
         │    Tests      │
         ├─────────────┤
         │              │
         │  Unit Tests   │  ~ 60%
         │              │
         └──────────────┘
```

## Unit Tests

### Backend Unit Tests (pytest + Django TestCase)

**Target Coverage: 80%+**

#### Models
```python
# tests/test_models.py
class TestRepositoryModel:
    def test_create_repository(self):
        """Repository can be created with valid data."""

    def test_repository_status_transitions(self):
        """Status transitions follow valid state machine."""

    def test_repository_str_representation(self):
        """String representation is meaningful."""

    def test_repository_cascade_delete(self):
        """Deleting repo cascades to files, chunks, embeddings."""
```

#### Serializers
```python
# tests/test_serializers.py
class TestRepositorySerializer:
    def test_valid_github_import(self):
        """Valid GitHub URL passes validation."""

    def test_invalid_github_url(self):
        """Invalid GitHub URL is rejected."""

    def test_name_sanitization(self):
        """HTML/script in name is stripped."""

    def test_size_limit_validation(self):
        """Files exceeding max size are rejected."""
```

#### Services
```python
# tests/test_services.py
class TestChunkingService:
    def test_python_function_chunking(self):
        """Python functions are extracted as individual chunks."""

    def test_class_method_chunking(self):
        """Class methods are separate chunks."""

    def test_sliding_window_fallback(self):
        """Unsupported languages use sliding window."""

    def test_chunk_size_limits(self):
        """Chunks respect maximum size constraints."""

    def test_overlap_in_sliding_window(self):
        """Sliding window chunks have correct overlap."""
```

#### Views
```python
# tests/test_views.py
class TestRepositoryViewSet:
    def test_list_repositories_authenticated(self):
        """Authenticated user sees their repositories."""

    def test_list_repositories_unauthenticated(self):
        """Unauthenticated request returns 401."""

    def test_repository_isolation(self):
        """User cannot see other users' repositories."""

    def test_create_repository_github(self):
        """GitHub import creates repo and dispatches task."""

    def test_delete_repository(self):
        """Owner can delete their repository."""

    def test_delete_repository_not_owner(self):
        """Non-owner gets 403."""
```

### Frontend Unit Tests (Vitest + React Testing Library)

**Target Coverage: 75%+**

#### Component Tests
```typescript
// tests/components/ChatInput.test.tsx
describe('ChatInput', () => {
  it('renders input field and send button', () => {});
  it('disables send when input is empty', () => {});
  it('calls onSend with message content', () => {});
  it('clears input after sending', () => {});
  it('shows loading state when processing', () => {});
  it('supports keyboard shortcut (Enter) to send', () => {});
  it('supports Shift+Enter for newline', () => {});
});

// tests/components/RepoCard.test.tsx
describe('RepoCard', () => {
  it('displays repository name and description', () => {});
  it('shows correct status badge', () => {});
  it('shows language breakdown', () => {});
  it('navigates to repo page on click', () => {});
  it('shows indexing progress when status is indexing', () => {});
});
```

#### Hook Tests
```typescript
// tests/hooks/useAuth.test.ts
describe('useAuth', () => {
  it('provides current user when authenticated', () => {});
  it('returns null user when not authenticated', () => {});
  it('login stores tokens and updates user', () => {});
  it('logout clears tokens and user', () => {});
  it('auto-refreshes token before expiry', () => {});
});
```

#### Utility Tests
```typescript
// tests/utils/api.test.ts
describe('API client', () => {
  it('adds auth header to requests', () => {});
  it('refreshes token on 401 response', () => {});
  it('redirects to login on refresh failure', () => {});
  it('retries failed requests after refresh', () => {});
});
```

---

## Integration Tests

### API Integration Tests
```python
# tests/integration/test_auth_flow.py
class TestAuthenticationFlow:
    def test_full_registration_flow(self):
        """Register → verify email → login → access protected endpoint."""

    def test_token_refresh_flow(self):
        """Login → access expires → refresh → access again."""

    def test_github_oauth_flow(self):
        """Initiate → callback → tokens stored → repos accessible."""

# tests/integration/test_repository_flow.py
class TestRepositoryFlow:
    def test_import_and_index(self):
        """Import repo → task dispatched → job completes → repo ready."""

    def test_import_reindex_flow(self):
        """Import → index → reindex → embeddings updated."""

    def test_search_after_indexing(self):
        """Index repo → search returns relevant results."""

# tests/integration/test_chat_flow.py
class TestChatFlow:
    def test_chat_with_rag(self):
        """Create conversation → send message → RAG retrieves → response generated."""

    def test_conversation_memory(self):
        """Multiple messages maintain context."""

    def test_streaming_response(self):
        """SSE stream delivers tokens correctly."""
```

### Database Integration Tests
```python
# tests/integration/test_pgvector.py
class TestVectorSearch:
    def test_embedding_storage(self):
        """Embeddings stored and retrievable."""

    def test_cosine_similarity_search(self):
        """Similar vectors return higher scores."""

    def test_repository_scoped_search(self):
        """Search only returns results from specified repo."""

    def test_hnsw_index_performance(self):
        """Search completes within acceptable time for 10K vectors."""
```

---

## API Tests

### Endpoint Contract Tests
```python
# tests/api/test_repositories_api.py
class TestRepositoriesAPI:
    """Test API contract (request/response shapes, status codes, headers)."""

    def test_list_returns_paginated_response(self):
        """GET /repositories returns {count, next, previous, results}."""

    def test_create_returns_201_with_id(self):
        """POST /repositories returns 201 with repository id."""

    def test_rate_limit_headers_present(self):
        """Responses include X-RateLimit-* headers."""

    def test_invalid_json_returns_400(self):
        """Malformed JSON body returns clear 400 error."""

    def test_unauthorized_returns_401(self):
        """Missing/invalid token returns 401 with error detail."""

    def test_not_found_returns_404(self):
        """Non-existent resource returns 404."""

    def test_rate_exceeded_returns_429(self):
        """Exceeding rate limit returns 429 with retry_after."""
```

### OpenAPI Schema Validation
```python
# tests/api/test_schema.py
class TestAPISchema:
    def test_all_endpoints_documented(self):
        """All registered URLs have OpenAPI documentation."""

    def test_response_matches_schema(self):
        """Actual responses match declared schema shapes."""
```

---

## Frontend Tests

### Component Tests (React Testing Library)
```typescript
describe('Dashboard', () => {
  it('shows loading skeleton while fetching', () => {});
  it('renders repository list on success', () => {});
  it('shows error state on fetch failure', () => {});
  it('shows empty state when no repos', () => {});
  it('navigates to import page from CTA', () => {});
});
```

### E2E Tests (Playwright)
```typescript
// e2e/auth.spec.ts
test.describe('Authentication', () => {
  test('user can register with email', async ({ page }) => {
    await page.goto('/register');
    await page.fill('[name="email"]', 'test@example.com');
    await page.fill('[name="password"]', 'SecurePass123!');
    await page.fill('[name="first_name"]', 'Test');
    await page.fill('[name="last_name"]', 'User');
    await page.click('button[type="submit"]');
    await expect(page).toHaveURL('/app/dashboard');
  });

  test('user can login', async ({ page }) => {
    await page.goto('/login');
    await page.fill('[name="email"]', 'existing@example.com');
    await page.fill('[name="password"]', 'password');
    await page.click('button[type="submit"]');
    await expect(page).toHaveURL('/app/dashboard');
  });
});

// e2e/chat.spec.ts
test.describe('AI Chat', () => {
  test('user can send message and receive response', async ({ page }) => {
    await loginAsUser(page);
    await page.goto('/app/repositories/test-repo/chat');
    await page.fill('[data-testid="chat-input"]', 'How does auth work?');
    await page.click('[data-testid="send-button"]');
    await expect(page.locator('[data-testid="assistant-message"]')).toBeVisible();
  });
});
```

---

## AI Evaluation

### RAG Quality Metrics
```python
# tests/ai/test_rag_quality.py
class TestRAGQuality:
    """Evaluate RAG pipeline on curated test cases."""

    # Test dataset: known questions + expected source files
    TEST_CASES = [
        {
            "query": "How does user authentication work?",
            "expected_files": ["src/middleware/auth.py", "src/utils/jwt.py"],
            "min_relevance": 0.7
        },
        {
            "query": "What database models exist?",
            "expected_files": ["src/models/user.py", "src/models/repo.py"],
            "min_relevance": 0.6
        }
    ]

    def test_retrieval_recall(self):
        """At least one expected file appears in top-5 results."""

    def test_retrieval_precision(self):
        """Top-3 results have relevance > threshold."""

    def test_response_groundedness(self):
        """Response content is grounded in retrieved context."""

    def test_response_relevance(self):
        """Response answers the question asked."""

    def test_no_hallucination(self):
        """Response doesn't reference non-existent files/functions."""
```

### LLM Response Quality
```python
class TestLLMResponseQuality:
    def test_code_blocks_have_language(self):
        """Code blocks in responses have syntax highlighting language."""

    def test_file_paths_exist(self):
        """Referenced file paths exist in the repository."""

    def test_line_numbers_valid(self):
        """Referenced line numbers are within file bounds."""

    def test_response_length_reasonable(self):
        """Responses are between 50-2000 tokens."""

    def test_system_prompt_not_leaked(self):
        """System prompt content doesn't appear in responses."""
```

---

## Repository Indexing Tests

```python
# tests/indexing/test_pipeline.py
class TestIndexingPipeline:
    def test_python_file_chunking(self):
        """Python file produces function-level chunks."""

    def test_javascript_file_chunking(self):
        """JavaScript file produces function-level chunks."""

    def test_binary_file_excluded(self):
        """Binary files are not processed."""

    def test_node_modules_excluded(self):
        """node_modules directory is skipped."""

    def test_large_file_excluded(self):
        """Files > 1MB are skipped."""

    def test_embedding_dimensions(self):
        """Generated embeddings have correct dimensions (384)."""

    def test_embedding_normalization(self):
        """Embeddings are L2 normalized (unit vectors)."""

    def test_incremental_reindex(self):
        """Only changed files are reprocessed."""

    def test_indexing_job_progress(self):
        """Job progress updates correctly during processing."""

    def test_indexing_failure_recovery(self):
        """Failed files don't stop entire job."""
```

---

## Performance Tests

### API Load Testing (Locust)
```python
# tests/performance/locustfile.py
from locust import HttpUser, task, between

class CodePilotUser(HttpUser):
    wait_time = between(1, 3)

    def on_start(self):
        """Login and get token."""
        response = self.client.post("/api/v1/auth/login", json={
            "email": "loadtest@example.com",
            "password": "testpass"
        })
        self.token = response.json()["data"]["access_token"]
        self.headers = {"Authorization": f"Bearer {self.token}"}

    @task(3)
    def list_repositories(self):
        self.client.get("/api/v1/repositories", headers=self.headers)

    @task(2)
    def semantic_search(self):
        self.client.post("/api/v1/search", json={
            "query": "authentication middleware",
            "repository_ids": ["test-repo-id"]
        }, headers=self.headers)

    @task(1)
    def send_chat_message(self):
        self.client.post("/api/v1/conversations/test-conv/messages", json={
            "content": "How does the auth system work?"
        }, headers=self.headers)
```

### Performance Targets
| Endpoint | Target p95 | Target p99 |
|---|---|---|
| GET /repositories | < 100ms | < 200ms |
| POST /search | < 500ms | < 1000ms |
| POST /messages (non-streaming) | < 3000ms | < 5000ms |
| POST /repositories (import start) | < 200ms | < 500ms |
| GET /files | < 150ms | < 300ms |

### Vector Search Performance
```python
class TestVectorSearchPerformance:
    """Benchmark vector search at scale."""

    @pytest.mark.parametrize("num_vectors", [1000, 10000, 100000])
    def test_search_latency(self, num_vectors):
        """Search completes within target latency at different scales."""
        # Insert num_vectors random embeddings
        # Run 100 search queries
        # Assert p95 < target
        targets = {1000: 50, 10000: 100, 100000: 200}  # ms
```

---

## Load Testing

### Scenarios
1. **Normal Load** — 100 concurrent users, steady state for 10 minutes
2. **Peak Load** — 500 concurrent users, ramp up over 5 minutes
3. **Spike Test** — 0 → 1000 users in 30 seconds
4. **Endurance** — 200 concurrent users for 1 hour

### Success Criteria
- Error rate < 1%
- p95 response time within targets
- No memory leaks (stable memory over endurance test)
- Database connection pool doesn't exhaust
- Redis memory stable
- Celery queue doesn't grow unboundedly

---

## Test Tooling

| Category | Tool |
|---|---|
| Backend Unit/Integration | pytest + pytest-django |
| Backend Coverage | pytest-cov |
| Backend API Testing | DRF test client |
| Backend Factories | factory_boy |
| Backend Mocking | pytest-mock, responses |
| Frontend Unit | Vitest |
| Frontend Component | React Testing Library |
| Frontend E2E | Playwright |
| Performance | Locust |
| Security | Trivy, safety, bandit |
| Linting (Python) | ruff |
| Linting (TS) | ESLint + Prettier |
| Type Checking | mypy (Python), tsc (TypeScript) |

## Test Fixtures & Factories

```python
# tests/factories.py
import factory
from apps.accounts.models import User
from apps.repositories.models import Repository

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    email = factory.Sequence(lambda n: f'user{n}@example.com')
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    password = factory.PostGenerationMethodCall('set_password', 'testpass123')
    is_active = True
    is_verified = True

class RepositoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Repository

    user = factory.SubFactory(UserFactory)
    name = factory.Sequence(lambda n: f'repo-{n}')
    source_type = 'github'
    status = 'ready'
    total_files = 100
    total_chunks = 500
```
