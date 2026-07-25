# CodePilot AI - API Specification

Base URL: `/api/v1/`

All responses follow the format:
```json
{
  "status": "success" | "error",
  "data": { ... },
  "message": "Human readable message",
  "errors": [ ... ]
}
```

## Authentication Endpoints

### POST /auth/register
Register a new user account.

| Field | Value |
|---|---|
| Purpose | Create a new user account |
| Method | POST |
| URL | /api/v1/auth/register |
| Authentication | None |

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "SecurePass123!",
  "first_name": "John",
  "last_name": "Doe"
}
```

**Validation:**
- email: valid email format, unique
- password: min 8 chars, 1 uppercase, 1 number, 1 special char
- first_name: 1-100 chars
- last_name: 1-100 chars

**Success Response (201):**
```json
{
  "status": "success",
  "data": {
    "user": {
      "id": "uuid",
      "email": "user@example.com",
      "first_name": "John",
      "last_name": "Doe"
    },
    "access_token": "eyJ...",
    "refresh_token": "eyJ..."
  }
}
```

**Errors:**
- 400: Validation errors (weak password, invalid email)
- 409: Email already registered

---

### POST /auth/login
Authenticate and receive tokens.

| Field | Value |
|---|---|
| Purpose | User login |
| Method | POST |
| URL | /api/v1/auth/login |
| Authentication | None |

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "SecurePass123!"
}
```

**Success Response (200):**
```json
{
  "status": "success",
  "data": {
    "access_token": "eyJ...",
    "refresh_token": "eyJ...",
    "user": {
      "id": "uuid",
      "email": "user@example.com",
      "first_name": "John",
      "last_name": "Doe"
    }
  }
}
```

**Errors:**
- 401: Invalid credentials
- 403: Account deactivated / unverified

---

### POST /auth/refresh
Refresh access token.

| Field | Value |
|---|---|
| Purpose | Get new access token |
| Method | POST |
| URL | /api/v1/auth/refresh |
| Authentication | None (refresh token in body) |

**Request Body:**
```json
{
  "refresh_token": "eyJ..."
}
```

**Success Response (200):**
```json
{
  "status": "success",
  "data": {
    "access_token": "eyJ..."
  }
}
```

**Errors:**
- 401: Invalid/expired refresh token

---

### POST /auth/logout
Blacklist refresh token.

| Field | Value |
|---|---|
| Purpose | Invalidate refresh token |
| Method | POST |
| URL | /api/v1/auth/logout |
| Authentication | Bearer Token |

**Request Body:**
```json
{
  "refresh_token": "eyJ..."
}
```

**Success Response (200):**
```json
{
  "status": "success",
  "message": "Successfully logged out"
}
```

---

### POST /auth/password/change
Change user password.

| Field | Value |
|---|---|
| Purpose | Change password |
| Method | POST |
| URL | /api/v1/auth/password/change |
| Authentication | Bearer Token |

**Request Body:**
```json
{
  "old_password": "OldPass123!",
  "new_password": "NewPass456!"
}
```

**Success Response (200):**
```json
{
  "status": "success",
  "message": "Password changed successfully"
}
```

**Errors:**
- 400: Old password incorrect, new password too weak

---

### GET /auth/github
Initiate GitHub OAuth flow.

| Field | Value |
|---|---|
| Purpose | Start GitHub OAuth |
| Method | GET |
| URL | /api/v1/auth/github |
| Authentication | Bearer Token |

**Response (302):** Redirect to GitHub authorization URL

---

### POST /auth/github/callback
Handle GitHub OAuth callback.

| Field | Value |
|---|---|
| Purpose | Complete GitHub OAuth |
| Method | POST |
| URL | /api/v1/auth/github/callback |
| Authentication | Bearer Token |

**Request Body:**
```json
{
  "code": "github_oauth_code",
  "state": "csrf_state"
}
```

**Success Response (200):**
```json
{
  "status": "success",
  "data": {
    "github_username": "octocat",
    "connected": true
  }
}
```

---

## User Endpoints

### GET /users/me
Get current user profile.

| Field | Value |
|---|---|
| Purpose | Get authenticated user info |
| Method | GET |
| URL | /api/v1/users/me |
| Authentication | Bearer Token |
| Permissions | Authenticated |

**Success Response (200):**
```json
{
  "status": "success",
  "data": {
    "id": "uuid",
    "email": "user@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "profile": {
      "avatar_url": "https://...",
      "bio": "Full-stack developer",
      "company": "Acme Inc",
      "preferred_llm": "openai",
      "settings": {}
    },
    "github_connected": true,
    "github_username": "octocat",
    "created_at": "2024-01-01T00:00:00Z"
  }
}
```

---

### PATCH /users/me
Update user profile.

| Field | Value |
|---|---|
| Purpose | Update profile |
| Method | PATCH |
| URL | /api/v1/users/me |
| Authentication | Bearer Token |
| Permissions | Authenticated |

**Request Body:**
```json
{
  "first_name": "John",
  "profile": {
    "bio": "Updated bio",
    "preferred_llm": "ollama"
  }
}
```

**Success Response (200):** Updated user object

---

## Repository Endpoints

### GET /repositories
List user's repositories.

| Field | Value |
|---|---|
| Purpose | List repositories |
| Method | GET |
| URL | /api/v1/repositories |
| Authentication | Bearer Token |
| Permissions | Authenticated |

**Query Parameters:**
- `status`: filter by status (pending/indexing/ready/failed)
- `search`: search by name
- `page`: page number
- `page_size`: items per page (default 20, max 100)
- `ordering`: field to sort by (-created_at, name, -last_indexed_at)

**Success Response (200):**
```json
{
  "status": "success",
  "data": {
    "count": 15,
    "next": "/api/v1/repositories?page=2",
    "previous": null,
    "results": [
      {
        "id": "uuid",
        "name": "my-project",
        "description": "A cool project",
        "source_type": "github",
        "github_url": "https://github.com/user/repo",
        "status": "ready",
        "total_files": 342,
        "total_chunks": 1205,
        "languages": {"Python": 65, "JavaScript": 25, "HTML": 10},
        "last_indexed_at": "2024-01-15T10:30:00Z",
        "created_at": "2024-01-01T00:00:00Z"
      }
    ]
  }
}
```

---

### POST /repositories
Create/import a repository.

| Field | Value |
|---|---|
| Purpose | Import repository |
| Method | POST |
| URL | /api/v1/repositories |
| Authentication | Bearer Token |
| Permissions | Authenticated |

**Request Body (GitHub Import):**
```json
{
  "source_type": "github",
  "github_url": "https://github.com/user/repo",
  "branch": "main"
}
```

**Request Body (Upload):**
Multipart form data with zip/tar file.

**Success Response (201):**
```json
{
  "status": "success",
  "data": {
    "id": "uuid",
    "name": "repo",
    "status": "pending",
    "indexing_job_id": "uuid"
  },
  "message": "Repository import started"
}
```

**Errors:**
- 400: Invalid URL, unsupported file type
- 403: No GitHub connection / insufficient permissions
- 409: Repository already imported
- 413: Upload too large (max 500MB)

---

### GET /repositories/{id}
Get repository details.

| Field | Value |
|---|---|
| Purpose | Repository detail |
| Method | GET |
| URL | /api/v1/repositories/{id} |
| Authentication | Bearer Token |
| Permissions | Repository Owner |

**Success Response (200):**
```json
{
  "status": "success",
  "data": {
    "id": "uuid",
    "name": "my-project",
    "description": "A cool project",
    "source_type": "github",
    "github_url": "https://github.com/user/repo",
    "default_branch": "main",
    "status": "ready",
    "total_files": 342,
    "total_chunks": 1205,
    "total_size_bytes": 5242880,
    "languages": {"Python": 65, "JavaScript": 25, "HTML": 10},
    "branches": [
      {"name": "main", "is_indexed": true, "indexed_at": "2024-01-15T10:30:00Z"}
    ],
    "last_indexed_at": "2024-01-15T10:30:00Z",
    "metrics": {
      "total_functions": 450,
      "total_classes": 85,
      "avg_complexity": 3.2,
      "embedding_coverage": 98.5
    },
    "created_at": "2024-01-01T00:00:00Z"
  }
}
```

---

### DELETE /repositories/{id}
Delete a repository and all associated data.

| Field | Value |
|---|---|
| Purpose | Delete repository |
| Method | DELETE |
| URL | /api/v1/repositories/{id} |
| Authentication | Bearer Token |
| Permissions | Repository Owner |

**Success Response (204):** No content

---

### POST /repositories/{id}/reindex
Trigger re-indexing.

| Field | Value |
|---|---|
| Purpose | Re-index repository |
| Method | POST |
| URL | /api/v1/repositories/{id}/reindex |
| Authentication | Bearer Token |
| Permissions | Repository Owner |

**Success Response (202):**
```json
{
  "status": "success",
  "data": {
    "indexing_job_id": "uuid"
  },
  "message": "Re-indexing started"
}
```

---

### GET /repositories/{id}/files
Browse repository files.

| Field | Value |
|---|---|
| Purpose | File browser |
| Method | GET |
| URL | /api/v1/repositories/{id}/files |
| Authentication | Bearer Token |
| Permissions | Repository Owner |

**Query Parameters:**
- `path`: directory path (default: root)
- `search`: filename search

**Success Response (200):**
```json
{
  "status": "success",
  "data": {
    "path": "/src",
    "items": [
      {
        "name": "main.py",
        "type": "file",
        "language": "Python",
        "size_bytes": 2048,
        "line_count": 85
      },
      {
        "name": "utils",
        "type": "directory",
        "children_count": 5
      }
    ]
  }
}
```

---

### GET /repositories/{id}/files/{file_id}/content
Get file content.

| Field | Value |
|---|---|
| Purpose | View file content |
| Method | GET |
| URL | /api/v1/repositories/{id}/files/{file_id}/content |
| Authentication | Bearer Token |
| Permissions | Repository Owner |

**Success Response (200):**
```json
{
  "status": "success",
  "data": {
    "file_path": "/src/main.py",
    "language": "Python",
    "content": "import os\n...",
    "line_count": 85,
    "chunks": [
      {"id": "uuid", "type": "function", "name": "main", "start_line": 10, "end_line": 45}
    ]
  }
}
```

---

## Chat Endpoints

### GET /conversations
List conversations.

| Field | Value |
|---|---|
| Purpose | List user conversations |
| Method | GET |
| URL | /api/v1/conversations |
| Authentication | Bearer Token |
| Permissions | Authenticated |

**Query Parameters:**
- `repository_id`: filter by repository
- `page`, `page_size`: pagination
- `ordering`: -updated_at (default)

**Success Response (200):**
```json
{
  "status": "success",
  "data": {
    "count": 8,
    "results": [
      {
        "id": "uuid",
        "title": "How does auth work?",
        "repository": {"id": "uuid", "name": "my-project"},
        "message_count": 6,
        "updated_at": "2024-01-15T10:30:00Z"
      }
    ]
  }
}
```

---

### POST /conversations
Create a new conversation.

| Field | Value |
|---|---|
| Purpose | Start new chat |
| Method | POST |
| URL | /api/v1/conversations |
| Authentication | Bearer Token |
| Permissions | Authenticated |

**Request Body:**
```json
{
  "repository_id": "uuid",
  "title": "Optional title"
}
```

**Success Response (201):**
```json
{
  "status": "success",
  "data": {
    "id": "uuid",
    "title": null,
    "repository_id": "uuid",
    "messages": []
  }
}
```

---

### POST /conversations/{id}/messages
Send a message and get AI response.

| Field | Value |
|---|---|
| Purpose | Send message to AI |
| Method | POST |
| URL | /api/v1/conversations/{id}/messages |
| Authentication | Bearer Token |
| Permissions | Conversation Owner |

**Request Body:**
```json
{
  "content": "How does the authentication middleware work?",
  "stream": true
}
```

**Success Response (200) - Non-streaming:**
```json
{
  "status": "success",
  "data": {
    "user_message": {
      "id": "uuid",
      "role": "user",
      "content": "How does the authentication middleware work?",
      "created_at": "2024-01-15T10:30:00Z"
    },
    "assistant_message": {
      "id": "uuid",
      "role": "assistant",
      "content": "The authentication middleware...",
      "sources": [
        {
          "file_path": "/src/middleware/auth.py",
          "start_line": 15,
          "end_line": 45,
          "chunk_type": "function",
          "relevance_score": 0.92
        }
      ],
      "token_count": 350,
      "created_at": "2024-01-15T10:30:01Z"
    }
  }
}
```

**Streaming Response:** Server-Sent Events (SSE)
```
data: {"type": "start", "message_id": "uuid"}
data: {"type": "chunk", "content": "The "}
data: {"type": "chunk", "content": "authentication "}
data: {"type": "chunk", "content": "middleware..."}
data: {"type": "sources", "sources": [...]}
data: {"type": "done", "token_count": 350}
```

---

### GET /conversations/{id}/messages
Get conversation history.

| Field | Value |
|---|---|
| Purpose | Get messages |
| Method | GET |
| URL | /api/v1/conversations/{id}/messages |
| Authentication | Bearer Token |
| Permissions | Conversation Owner |

**Success Response (200):**
```json
{
  "status": "success",
  "data": {
    "messages": [
      {
        "id": "uuid",
        "role": "user",
        "content": "...",
        "created_at": "..."
      },
      {
        "id": "uuid",
        "role": "assistant",
        "content": "...",
        "sources": [...],
        "created_at": "..."
      }
    ]
  }
}
```

---

## Search Endpoints

### POST /search
Semantic code search.

| Field | Value |
|---|---|
| Purpose | Search code semantically |
| Method | POST |
| URL | /api/v1/search |
| Authentication | Bearer Token |
| Permissions | Authenticated |

**Request Body:**
```json
{
  "query": "function that validates email addresses",
  "repository_ids": ["uuid1", "uuid2"],
  "filters": {
    "languages": ["Python", "JavaScript"],
    "file_types": [".py", ".js"],
    "chunk_types": ["function", "class"]
  },
  "limit": 10
}
```

**Success Response (200):**
```json
{
  "status": "success",
  "data": {
    "results": [
      {
        "chunk_id": "uuid",
        "repository": {"id": "uuid", "name": "my-project"},
        "file_path": "/src/validators.py",
        "symbol_name": "validate_email",
        "chunk_type": "function",
        "content": "def validate_email(email: str)...",
        "start_line": 25,
        "end_line": 40,
        "language": "Python",
        "relevance_score": 0.94
      }
    ],
    "total": 15,
    "query_time_ms": 120
  }
}
```

---

## AI Feature Endpoints

### POST /ai/explain
Explain a code chunk.

| Field | Value |
|---|---|
| Purpose | Get code explanation |
| Method | POST |
| URL | /api/v1/ai/explain |
| Authentication | Bearer Token |
| Permissions | Authenticated |

**Request Body:**
```json
{
  "chunk_id": "uuid",
  "detail_level": "detailed"
}
```

**Success Response (200):**
```json
{
  "status": "success",
  "data": {
    "explanation": "This function validates...",
    "complexity": "medium",
    "key_concepts": ["regex", "validation", "error handling"]
  }
}
```

---

### POST /ai/generate-docs
Generate documentation.

| Field | Value |
|---|---|
| Purpose | Generate documentation |
| Method | POST |
| URL | /api/v1/ai/generate-docs |
| Authentication | Bearer Token |
| Permissions | Authenticated |

**Request Body:**
```json
{
  "repository_id": "uuid",
  "target": "function",
  "chunk_ids": ["uuid1", "uuid2"],
  "format": "markdown"
}
```

**Success Response (200):**
```json
{
  "status": "success",
  "data": {
    "documentation": "## validate_email\n\n...",
    "format": "markdown"
  }
}
```

---

### POST /ai/generate-tests
Generate unit tests.

| Field | Value |
|---|---|
| Purpose | Generate test cases |
| Method | POST |
| URL | /api/v1/ai/generate-tests |
| Authentication | Bearer Token |
| Permissions | Authenticated |

**Request Body:**
```json
{
  "chunk_id": "uuid",
  "framework": "pytest",
  "coverage_types": ["happy_path", "edge_cases", "error_cases"]
}
```

**Success Response (200):**
```json
{
  "status": "success",
  "data": {
    "tests": "import pytest\n\ndef test_validate_email_valid()...",
    "test_count": 5,
    "framework": "pytest"
  }
}
```

---

### POST /ai/detect-bugs
Detect potential bugs.

| Field | Value |
|---|---|
| Purpose | Bug detection |
| Method | POST |
| URL | /api/v1/ai/detect-bugs |
| Authentication | Bearer Token |
| Permissions | Authenticated |

**Request Body:**
```json
{
  "repository_id": "uuid",
  "scope": "file",
  "file_id": "uuid"
}
```

**Success Response (200):**
```json
{
  "status": "success",
  "data": {
    "issues": [
      {
        "severity": "high",
        "type": "potential_null_reference",
        "file_path": "/src/utils.py",
        "line": 42,
        "description": "Variable 'result' may be None before access",
        "suggestion": "Add null check before accessing result.value"
      }
    ],
    "summary": {
      "high": 1,
      "medium": 3,
      "low": 5
    }
  }
}
```

---

### POST /ai/review-pr
Review a pull request.

| Field | Value |
|---|---|
| Purpose | AI code review |
| Method | POST |
| URL | /api/v1/ai/review-pr |
| Authentication | Bearer Token |
| Permissions | Authenticated + GitHub Connected |

**Request Body:**
```json
{
  "repository_id": "uuid",
  "pr_number": 42
}
```

**Success Response (202):**
```json
{
  "status": "success",
  "data": {
    "review_id": "uuid",
    "status": "processing"
  },
  "message": "PR review started"
}
```

---

## Analytics Endpoints

### GET /repositories/{id}/analytics
Get repository analytics.

| Field | Value |
|---|---|
| Purpose | Repository metrics |
| Method | GET |
| URL | /api/v1/repositories/{id}/analytics |
| Authentication | Bearer Token |
| Permissions | Repository Owner |

**Success Response (200):**
```json
{
  "status": "success",
  "data": {
    "language_breakdown": {"Python": 65, "JavaScript": 25, "HTML": 10},
    "total_files": 342,
    "total_lines": 28500,
    "total_functions": 450,
    "total_classes": 85,
    "avg_complexity": 3.2,
    "embedding_coverage": 98.5,
    "indexing_history": [
      {"date": "2024-01-15", "status": "completed", "duration_seconds": 45}
    ],
    "chat_stats": {
      "total_conversations": 12,
      "total_messages": 86,
      "avg_response_time_ms": 2500
    }
  }
}
```

---

## GitHub Endpoints

### GET /github/repos
List available GitHub repositories.

| Field | Value |
|---|---|
| Purpose | List GitHub repos for import |
| Method | GET |
| URL | /api/v1/github/repos |
| Authentication | Bearer Token |
| Permissions | GitHub Connected |

**Query Parameters:**
- `page`, `per_page`: pagination
- `search`: filter by name

**Success Response (200):**
```json
{
  "status": "success",
  "data": {
    "repositories": [
      {
        "full_name": "user/repo",
        "description": "A project",
        "language": "Python",
        "private": false,
        "default_branch": "main",
        "already_imported": false
      }
    ]
  }
}
```

---

## Indexing Endpoints

### GET /indexing/jobs/{id}
Get indexing job status.

| Field | Value |
|---|---|
| Purpose | Check indexing progress |
| Method | GET |
| URL | /api/v1/indexing/jobs/{id} |
| Authentication | Bearer Token |
| Permissions | Repository Owner |

**Success Response (200):**
```json
{
  "status": "success",
  "data": {
    "id": "uuid",
    "repository_id": "uuid",
    "status": "running",
    "job_type": "full",
    "progress_percent": 65.5,
    "total_files": 342,
    "processed_files": 224,
    "failed_files": 2,
    "started_at": "2024-01-15T10:30:00Z"
  }
}
```

---

## Common Error Responses

### 400 Bad Request
```json
{
  "status": "error",
  "message": "Validation failed",
  "errors": [
    {"field": "email", "message": "Invalid email format"},
    {"field": "password", "message": "Must be at least 8 characters"}
  ]
}
```

### 401 Unauthorized
```json
{
  "status": "error",
  "message": "Authentication required",
  "errors": [{"code": "token_expired", "message": "Access token has expired"}]
}
```

### 403 Forbidden
```json
{
  "status": "error",
  "message": "Permission denied",
  "errors": [{"code": "not_owner", "message": "You do not own this repository"}]
}
```

### 404 Not Found
```json
{
  "status": "error",
  "message": "Resource not found"
}
```

### 429 Too Many Requests
```json
{
  "status": "error",
  "message": "Rate limit exceeded",
  "errors": [{"code": "rate_limited", "retry_after": 60}]
}
```

### 500 Internal Server Error
```json
{
  "status": "error",
  "message": "An unexpected error occurred",
  "errors": [{"code": "internal_error", "reference": "err_abc123"}]
}
```

## Rate Limiting

| Endpoint Category | Limit |
|---|---|
| Authentication | 5 requests/minute |
| Standard API | 100 requests/minute |
| AI Features | 20 requests/minute |
| Search | 30 requests/minute |
| File Upload | 5 requests/hour |

Rate limit headers included in all responses:
```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1705312200
```
