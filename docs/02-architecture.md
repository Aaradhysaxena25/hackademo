# CodePilot AI - Software Architecture

## System Architecture Overview

```mermaid
graph TB
    subgraph "Client Layer"
        FE[React Frontend<br/>Vite + TypeScript]
    end

    subgraph "CDN / Edge"
        CDN[Vercel Edge Network]
    end

    subgraph "API Layer"
        API[Django REST Framework<br/>JWT Auth]
        WS[WebSocket Server<br/>Django Channels]
    end

    subgraph "Background Processing"
        CW[Celery Workers]
        CB[Celery Beat<br/>Scheduler]
    end

    subgraph "AI Layer"
        LC[LangChain Pipeline]
        EMB[Embedding Service<br/>Sentence Transformers]
        LLM[LLM Provider<br/>OpenAI / Ollama]
    end

    subgraph "Data Layer"
        PG[(PostgreSQL<br/>+ pgvector)]
        RD[(Redis<br/>Cache + Broker)]
        FS[File Storage<br/>Local / S3]
    end

    subgraph "External Services"
        GH[GitHub API]
    end

    FE --> CDN
    CDN --> API
    FE --> WS
    API --> PG
    API --> RD
    API --> CW
    CW --> LC
    CW --> EMB
    CW --> PG
    CW --> FS
    LC --> LLM
    LC --> PG
    CB --> CW
    API --> GH
    CW --> GH
```

## Frontend Architecture

```mermaid
graph TB
    subgraph "React Application"
        subgraph "Routing Layer"
            RR[React Router v6]
        end

        subgraph "Page Components"
            LP[Landing Page]
            DB[Dashboard]
            RP[Repository Page]
            CP[Chat Page]
            SP[Settings Page]
            AP[Analytics Page]
        end

        subgraph "Feature Components"
            CV[Code Viewer<br/>Monaco Editor]
            CI[Chat Interface]
            SR[Search Results]
            FB[File Browser]
            PR[PR Review]
        end

        subgraph "Shared Components"
            UI[ShadCN UI<br/>Components]
            LY[Layout Components]
            FM[Form Components]
        end

        subgraph "State Management"
            RQ[React Query<br/>Server State]
            CTX[React Context<br/>App State]
            ZS[Zustand<br/>UI State]
        end

        subgraph "Services"
            AX[Axios Instance<br/>API Client]
            WSC[WebSocket Client]
            AUTH[Auth Service]
        end
    end

    RR --> LP & DB & RP & CP & SP & AP
    DB --> FB & SR
    RP --> CV & CI
    CP --> CI
    AP --> SR
    UI --> LP & DB & RP & CP & SP & AP
    RQ --> AX
    AX --> AUTH
```

### Frontend Design Decisions
- **State Management**: React Query for server state (caching, sync), Zustand for UI state (sidebar, theme), React Context for auth
- **Code Splitting**: Route-level lazy loading for optimal bundle size
- **API Layer**: Centralized Axios instance with interceptors for auth, error handling, retry
- **Styling**: Tailwind CSS utility classes + ShadCN component library for consistency
- **Forms**: React Hook Form + Zod for validation

## Backend Architecture

```mermaid
graph TB
    subgraph "Django Project: codepilot"
        subgraph "Core"
            SETTINGS[Settings<br/>base / dev / prod]
            URLS[URL Configuration]
            MW[Middleware Stack]
        end

        subgraph "Apps"
            ACC[accounts<br/>Auth, Users, OAuth]
            REPO[repositories<br/>Repos, Files, Branches]
            IDX[indexing<br/>Parsing, Chunking]
            EMB[embeddings<br/>Vectors, Search]
            CHAT[chat<br/>Conversations, Messages]
            AI[ai<br/>LLM, Prompts, RAG]
            GH[github<br/>OAuth, API, Webhooks]
            ANLY[analytics<br/>Metrics, Stats]
            NOTIF[notifications<br/>Email, In-app]
            COMMON[common<br/>Utils, Mixins, Base]
        end

        subgraph "Middleware"
            AUTH_MW[JWT Authentication]
            CORS_MW[CORS]
            RATE_MW[Rate Limiting]
            LOG_MW[Request Logging]
        end
    end

    URLS --> ACC & REPO & IDX & EMB & CHAT & AI & GH & ANLY & NOTIF
    MW --> AUTH_MW & CORS_MW & RATE_MW & LOG_MW
```

### Backend Design Decisions
- **App Separation**: Each Django app has a single responsibility, clear boundaries
- **Serializers**: Input validation and output formatting via DRF serializers
- **Permissions**: Custom permission classes per endpoint
- **Pagination**: Cursor-based pagination for large datasets
- **Versioning**: URL-based API versioning (v1/)
- **Error Handling**: Centralized exception handler with consistent error format

## Database Architecture

```mermaid
graph TB
    subgraph "PostgreSQL"
        subgraph "Core Tables"
            U[users]
            P[profiles]
        end

        subgraph "Repository Tables"
            R[repositories]
            F[repository_files]
            B[branches]
        end

        subgraph "AI Tables"
            E[embeddings<br/>pgvector]
            CH[chunks]
            CONV[conversations]
            MSG[messages]
        end

        subgraph "Integration Tables"
            GHT[github_tokens]
            PRR[pull_requests]
        end

        subgraph "Analytics Tables"
            RM[repo_metrics]
            UL[usage_logs]
        end
    end

    U --> P
    U --> R
    R --> F
    R --> B
    R --> E
    F --> CH
    CH --> E
    U --> CONV
    CONV --> MSG
    R --> CONV
    U --> GHT
    R --> PRR
    R --> RM
    U --> UL
```

## Authentication Architecture

```mermaid
sequenceDiagram
    participant C as Client
    participant API as Django API
    participant DB as PostgreSQL
    participant GH as GitHub OAuth

    Note over C,GH: Email/Password Login
    C->>API: POST /api/v1/auth/login
    API->>DB: Verify credentials
    DB-->>API: User record
    API-->>C: {access_token, refresh_token}

    Note over C,GH: Token Refresh
    C->>API: POST /api/v1/auth/refresh
    API->>API: Verify refresh token
    API-->>C: {new_access_token}

    Note over C,GH: GitHub OAuth
    C->>API: GET /api/v1/auth/github
    API-->>C: Redirect to GitHub
    C->>GH: Authorize
    GH-->>C: Callback with code
    C->>API: POST /api/v1/auth/github/callback
    API->>GH: Exchange code for token
    GH-->>API: Access token
    API->>DB: Store encrypted token
    API-->>C: {access_token, refresh_token}
```

## AI Pipeline Architecture

```mermaid
graph TB
    subgraph "Query Pipeline"
        UQ[User Query]
        QE[Query Embedding]
        VS[Vector Search<br/>pgvector]
        CTX[Context Assembly]
        PM[Prompt Construction]
        LLM[LLM Inference]
        RS[Response Stream]
    end

    subgraph "Indexing Pipeline"
        RI[Repository Import]
        FP[File Parser]
        CK[Code Chunker]
        ME[Metadata Extractor]
        EG[Embedding Generator]
        ST[Vector Storage]
    end

    UQ --> QE --> VS --> CTX --> PM --> LLM --> RS

    RI --> FP --> CK --> ME --> EG --> ST
```

## RAG Pipeline

```mermaid
graph LR
    subgraph "Retrieval"
        Q[Query] --> QE[Embed Query]
        QE --> SIM[Similarity Search<br/>Top-K Chunks]
        SIM --> RR[Re-Rank Results]
    end

    subgraph "Augmentation"
        RR --> CTX[Build Context<br/>Code + Metadata]
        CTX --> SYS[System Prompt<br/>+ Instructions]
        SYS --> FP[Final Prompt]
    end

    subgraph "Generation"
        FP --> LLM[LLM<br/>OpenAI / Ollama]
        LLM --> STR[Stream Response]
        STR --> POST[Post-Process<br/>Format Code]
    end
```

## Repository Indexing Pipeline

```mermaid
graph TB
    subgraph "Ingestion"
        UP[Upload / GitHub Clone]
        VAL[Validate Repository]
        EXT[Extract Files]
    end

    subgraph "Processing"
        FL[File Filter<br/>Ignore binaries, node_modules]
        LP[Language Detection]
        CK[Code Chunking<br/>AST-based]
        MD[Metadata Extraction<br/>Functions, Classes, Imports]
    end

    subgraph "Embedding"
        BT[Batch Processing]
        EG[Embedding Generation<br/>Sentence Transformers]
        NM[Normalize Vectors]
    end

    subgraph "Storage"
        PG[(pgvector)]
        META[(Metadata Tables)]
        IDX[Create Indexes<br/>HNSW / IVFFlat]
    end

    UP --> VAL --> EXT --> FL --> LP --> CK --> MD --> BT --> EG --> NM --> PG
    MD --> META
    PG --> IDX
```

## Background Task Pipeline

```mermaid
graph TB
    subgraph "Task Producers"
        API[API Endpoints]
        SCH[Celery Beat<br/>Scheduled Tasks]
        WH[Webhooks]
    end

    subgraph "Message Broker"
        RD[(Redis)]
    end

    subgraph "Task Consumers"
        W1[Worker 1<br/>Indexing]
        W2[Worker 2<br/>Embeddings]
        W3[Worker 3<br/>AI Tasks]
        W4[Worker 4<br/>GitHub Sync]
    end

    subgraph "Task Types"
        T1[index_repository]
        T2[generate_embeddings]
        T3[process_chat_query]
        T4[sync_github_repo]
        T5[generate_documentation]
        T6[review_pull_request]
    end

    API --> RD
    SCH --> RD
    WH --> RD
    RD --> W1 & W2 & W3 & W4
    W1 --> T1
    W2 --> T2
    W3 --> T3 & T5 & T6
    W4 --> T4
```

## GitHub Integration Architecture

```mermaid
sequenceDiagram
    participant U as User
    participant API as CodePilot API
    participant GH as GitHub API
    participant CW as Celery Worker

    U->>API: POST /repos/import {github_url}
    API->>API: Validate URL, check permissions
    API->>CW: Dispatch clone_repository task
    API-->>U: 202 Accepted {task_id}

    CW->>GH: Clone repository
    GH-->>CW: Repository files
    CW->>CW: Parse & chunk files
    CW->>CW: Generate embeddings
    CW->>API: Update repo status: "ready"

    U->>API: GET /repos/{id}/status
    API-->>U: {status: "ready", files: 342}
```

## Deployment Architecture

```mermaid
graph TB
    subgraph "Production"
        subgraph "Frontend - Vercel"
            VE[Vercel Edge<br/>CDN + SSR]
        end

        subgraph "Backend - Railway/Render"
            LB[Load Balancer]
            API1[API Server 1]
            API2[API Server 2]
            CW1[Celery Worker 1]
            CW2[Celery Worker 2]
        end

        subgraph "Data - Managed Services"
            NP[(Neon PostgreSQL<br/>+ pgvector)]
            UR[(Upstash Redis)]
            S3[(S3 Storage)]
        end
    end

    subgraph "Development"
        DC[docker-compose<br/>All services local]
    end

    VE --> LB
    LB --> API1 & API2
    API1 & API2 --> NP & UR
    CW1 & CW2 --> NP & UR & S3
```

## Component Communication

| From | To | Protocol | Purpose |
|---|---|---|---|
| Frontend | API | HTTPS REST | All CRUD operations |
| Frontend | API | WebSocket | Chat streaming, notifications |
| API | PostgreSQL | TCP | Data persistence |
| API | Redis | TCP | Caching, session store |
| API | Celery | Redis (AMQP) | Task dispatching |
| Celery | PostgreSQL | TCP | Read/write data |
| Celery | GitHub API | HTTPS | Clone repos, fetch PRs |
| Celery | LLM Provider | HTTPS | AI inference |
| Celery | Sentence Transformers | Local | Embedding generation |
