# CodePilot AI - AI/RAG Pipeline Design

## Overview

The AI system is built on Retrieval-Augmented Generation (RAG), combining vector similarity search with LLM generation to provide accurate, context-aware responses about codebases.

## Repository Parsing

### File Discovery
1. Recursively walk the repository directory tree
2. Build a file manifest with paths, sizes, and extensions
3. Apply exclusion rules before processing

### Exclusion Rules
```python
EXCLUDED_DIRECTORIES = [
    "node_modules", ".git", "__pycache__", ".venv", "venv",
    "dist", "build", ".next", ".nuxt", "target", "bin", "obj",
    ".idea", ".vscode", ".DS_Store", "coverage", ".pytest_cache",
    "vendor", "bower_components", ".tox", "eggs", "*.egg-info"
]

EXCLUDED_EXTENSIONS = [
    # Binary
    ".exe", ".dll", ".so", ".dylib", ".bin", ".dat",
    # Media
    ".png", ".jpg", ".jpeg", ".gif", ".svg", ".ico", ".mp4", ".mp3",
    # Archives
    ".zip", ".tar", ".gz", ".rar", ".7z",
    # Compiled
    ".pyc", ".pyo", ".class", ".o", ".obj",
    # Package locks (large, not useful for search)
    "package-lock.json", "yarn.lock", "poetry.lock", "Pipfile.lock",
    # Other
    ".min.js", ".min.css", ".map", ".woff", ".woff2", ".ttf", ".eot"
]

MAX_FILE_SIZE = 1_048_576  # 1MB - skip files larger than this
```

### Language Detection
- Primary: File extension mapping (.py → Python, .ts → TypeScript)
- Fallback: First-line shebang analysis (#!/usr/bin/env python)
- Supported languages: Python, JavaScript, TypeScript, Java, Go, Rust, C, C++, Ruby, PHP, C#, Kotlin, Swift, HTML, CSS, SQL, Shell, YAML, JSON, Markdown

## Chunking Strategy

### Approach: Hybrid AST + Sliding Window

For supported languages, use AST-based chunking to extract meaningful code units. Fall back to sliding window for unsupported languages or when AST parsing fails.

### AST-Based Chunking (Primary)
```
Source File
    ├── Module-level docstring → Module chunk
    ├── Import statements → Imports chunk
    ├── Class definition → Class chunk
    │   ├── Class docstring → included in class chunk
    │   ├── Method 1 → Method chunk
    │   ├── Method 2 → Method chunk
    │   └── Method 3 → Method chunk
    ├── Function definition → Function chunk
    ├── Function definition → Function chunk
    └── Top-level code → Block chunk
```

### Chunk Size Guidelines
| Chunk Type | Target Size | Max Size |
|---|---|---|
| Function/Method | Natural boundary | 500 lines |
| Class (without methods) | Declaration + docstring | 100 lines |
| Module header | Imports + docstring | 50 lines |
| Block (sliding window) | 50 lines | 100 lines |

### Sliding Window Chunking (Fallback)
- Window size: 50 lines
- Overlap: 10 lines (ensures context continuity)
- Respects line boundaries (never splits mid-line)

### Chunk Schema
```python
@dataclass
class CodeChunk:
    content: str              # The actual code
    file_path: str           # Full file path
    language: str            # Detected language
    chunk_type: str          # function | class | method | module | block
    symbol_name: str | None  # Function/class name if applicable
    start_line: int          # Start line in original file
    end_line: int            # End line in original file
    metadata: dict           # Additional context
```

## Metadata Extraction

For each chunk, extract:

```python
metadata = {
    "file_path": "/src/auth/middleware.py",
    "language": "Python",
    "chunk_type": "function",
    "symbol_name": "authenticate_request",
    "start_line": 15,
    "end_line": 45,
    "imports": ["jwt", "django.http"],
    "decorators": ["@require_auth"],
    "parameters": ["request", "token"],
    "return_type": "HttpResponse",
    "docstring": "Validates JWT token and attaches user to request",
    "complexity": 4,
    "dependencies": ["validate_token", "get_user_by_id"],
    "repository_id": "uuid",
    "file_id": "uuid"
}
```

## Embedding Generation

### Model Selection
- **Primary**: `all-MiniLM-L6-v2` (384 dimensions, fast, good quality)
- **Alternative**: `all-mpnet-base-v2` (768 dimensions, higher quality, slower)
- **Code-specific**: `microsoft/codebert-base` for code-only embeddings

### Embedding Process
```
Code Chunk
    ↓
Preprocessing (normalize whitespace, remove excessive comments)
    ↓
Context Augmentation (prepend file path + language + symbol name)
    ↓
Tokenization (model tokenizer, max 512 tokens)
    ↓
Embedding Generation (Sentence Transformers)
    ↓
Normalization (L2 normalize for cosine similarity)
    ↓
Storage (pgvector)
```

### Context-Augmented Input
Before embedding, prepend contextual information:
```
"File: src/auth/middleware.py | Language: Python | Function: authenticate_request\n\n{actual_code}"
```

This improves retrieval accuracy by embedding contextual information alongside the code.

### Batch Processing
- Batch size: 32 chunks per batch
- Use GPU if available (CUDA), fallback to CPU
- Progress tracking per batch
- Retry failed batches up to 3 times

## Storage

### pgvector Configuration
```sql
-- Enable extension
CREATE EXTENSION IF NOT EXISTS vector;

-- Embedding table with vector column
CREATE TABLE embeddings (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    chunk_id UUID REFERENCES code_chunks(id) ON DELETE CASCADE,
    repository_id UUID REFERENCES repositories(id) ON DELETE CASCADE,
    embedding VECTOR(384) NOT NULL,
    model_name VARCHAR(100) NOT NULL DEFAULT 'all-MiniLM-L6-v2',
    dimensions INTEGER NOT NULL DEFAULT 384,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- HNSW index for fast approximate nearest neighbor search
CREATE INDEX ON embeddings
    USING hnsw (embedding vector_cosine_ops)
    WITH (m = 16, ef_construction = 64);
```

### Index Strategy
- **Small repos (<1000 chunks)**: Exact search (no index needed)
- **Medium repos (1K-100K chunks)**: HNSW index (m=16, ef_construction=64)
- **Large repos (>100K chunks)**: HNSW with higher parameters or partition by repository

## Retrieval

### Query Processing Pipeline
```
User Query: "How does authentication work?"
    ↓
Query Preprocessing
  - Expand abbreviations
  - Add context from conversation history
    ↓
Query Embedding (same model as indexing)
    ↓
Vector Similarity Search
  - Search within repository scope
  - Top-K retrieval (K=10)
  - Cosine similarity threshold > 0.5
    ↓
Re-Ranking
  - Cross-encoder re-ranking (top 20 → top 5)
  - Boost recent files
  - Boost exact symbol name matches
    ↓
Context Assembly
  - Selected chunks with metadata
  - Surrounding context (±5 lines)
  - File path breadcrumbs
```

### Similarity Search Query
```sql
SELECT
    c.content,
    c.file_path,
    c.symbol_name,
    c.chunk_type,
    c.start_line,
    c.end_line,
    c.language,
    1 - (e.embedding <=> query_embedding) AS similarity
FROM embeddings e
JOIN code_chunks c ON e.chunk_id = c.id
WHERE e.repository_id = :repo_id
    AND 1 - (e.embedding <=> query_embedding) > 0.5
ORDER BY e.embedding <=> query_embedding
LIMIT 10;
```

## Prompt Construction

### System Prompt Template
```
You are CodePilot AI, an intelligent code assistant. You help developers understand
their codebase by providing accurate, detailed answers based on the actual source code.

Rules:
1. Only answer based on the provided code context. If the answer is not in the context, say so.
2. Include relevant file paths and line numbers in your response.
3. Use code blocks with proper syntax highlighting.
4. Be concise but thorough.
5. If you reference multiple files, organize your response clearly.
6. Do not fabricate code that doesn't exist in the repository.

Repository: {repository_name}
Languages: {languages}
```

### Context Prompt Template
```
Relevant code context:

---
File: {file_path} (lines {start_line}-{end_line})
Language: {language}
Type: {chunk_type} | Name: {symbol_name}

```{language}
{code_content}
```

Relevance: {similarity_score}
---

[Repeat for each retrieved chunk]
```

### User Prompt Template
```
Conversation history:
{last_3_messages}

Current question: {user_query}
```

### Full Prompt Assembly
```
[System Prompt]
[Context Prompt - Retrieved Chunks]
[Conversation History - Last 3 exchanges]
[User Query]
```

## LLM Response

### Provider Abstraction
```python
class LLMProvider(ABC):
    @abstractmethod
    async def generate(self, messages: list, stream: bool) -> AsyncGenerator[str, None]:
        pass

class OpenAIProvider(LLMProvider):
    model = "gpt-4o-mini"  # Default, configurable
    max_tokens = 2048
    temperature = 0.1  # Low for factual code responses

class OllamaProvider(LLMProvider):
    model = "codellama:13b"
    base_url = "http://localhost:11434"

class HuggingFaceProvider(LLMProvider):
    model = "codellama/CodeLlama-13b-hf"
```

### Response Streaming
- Use Server-Sent Events (SSE) for real-time streaming
- Stream tokens as they are generated
- Send source references after generation completes
- Handle timeouts and connection drops gracefully

### Response Post-Processing
1. Extract code blocks and verify syntax highlighting language tags
2. Validate file path references exist in the repository
3. Format source attributions with clickable links
4. Calculate and store token usage

## Conversation Memory

### Short-term Memory (Per Conversation)
- Store last N messages (configurable, default 10)
- Include in prompt as conversation history
- Summarize older messages if context window is limited

### Memory Management
```
Total context budget: 8000 tokens (for gpt-4o-mini)
  - System prompt: ~200 tokens
  - Code context: ~4000 tokens (5-8 chunks)
  - Conversation history: ~2000 tokens (last 3 exchanges)
  - User query: ~200 tokens
  - Response budget: ~1600 tokens
```

### Conversation Summarization
When conversation exceeds memory window:
1. Summarize older messages into a single context paragraph
2. Keep last 3 full message pairs
3. Store summary as metadata for future reference

## Caching

### Embedding Cache
- Cache computed embeddings for identical queries (Redis, TTL: 1 hour)
- Key: `emb:{model}:{hash(query)}`

### Search Result Cache
- Cache search results for repeated queries within same repository
- Key: `search:{repo_id}:{hash(query)}`
- TTL: 5 minutes (invalidated on re-index)

### LLM Response Cache
- Cache full responses for identical query + context combinations
- Key: `llm:{hash(system+context+query)}`
- TTL: 30 minutes
- Disabled for streaming responses

### Cache Invalidation
- Repository re-index invalidates all caches for that repository
- User preference changes (model, temperature) bypass cache
- Manual cache clear available via admin endpoint

## Rate Limiting

### Per-User Limits
| Resource | Free Tier | Pro Tier |
|---|---|---|
| Chat messages | 50/day | 500/day |
| Repositories | 3 | 25 |
| Indexing jobs | 5/day | 50/day |
| Search queries | 100/day | 1000/day |
| AI features (docs, tests, bugs) | 20/day | 200/day |

### Implementation
- Token bucket algorithm per user per feature
- Redis-backed counters with TTL
- Graceful degradation (queue requests instead of hard reject)
- Rate limit headers in all responses

### AI-Specific Limits
- Max input tokens: 8000 per request
- Max output tokens: 2048 per response
- Max concurrent AI requests per user: 3
- Timeout: 30 seconds per request
