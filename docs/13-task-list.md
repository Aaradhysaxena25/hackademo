# CodePilot AI - Detailed Task List

## Milestone 1: Project Setup (Tasks 1-25)

### Task 1: Initialize Django Project
- **Description:** Create Django project named `codepilot` with proper settings structure
- **Priority:** Critical
- **Dependencies:** None
- **Estimated Time:** 1 hour
- **Definition of Done:** Django project created with manage.py, settings split into base/dev/prod

### Task 2: Configure PostgreSQL with pgvector
- **Description:** Set up PostgreSQL database connection with pgvector extension
- **Priority:** Critical
- **Dependencies:** Task 1
- **Estimated Time:** 30 min
- **Definition of Done:** Database connects, pgvector extension enabled, migrations run

### Task 3: Install and Configure Django REST Framework
- **Description:** Install DRF, configure default authentication, pagination, renderers
- **Priority:** Critical
- **Dependencies:** Task 1
- **Estimated Time:** 30 min
- **Definition of Done:** DRF installed, settings configured, browsable API working

### Task 4: Configure Redis Connection
- **Description:** Set up Redis for caching and Celery broker
- **Priority:** Critical
- **Dependencies:** Task 1
- **Estimated Time:** 30 min
- **Definition of Done:** Redis connects, Django cache backend configured

### Task 5: Install and Configure Celery
- **Description:** Set up Celery with Redis broker, configure task discovery
- **Priority:** Critical
- **Dependencies:** Task 4
- **Estimated Time:** 1 hour
- **Definition of Done:** Celery worker starts, test task executes successfully

### Task 6: Create Django App Structure
- **Description:** Create all Django apps: accounts, repositories, indexing, embeddings, chat, ai, github, analytics, notifications, common, core
- **Priority:** Critical
- **Dependencies:** Task 1
- **Estimated Time:** 1 hour
- **Definition of Done:** All apps created, registered in INSTALLED_APPS

### Task 7: Configure Environment Variables
- **Description:** Set up django-environ, create .env.example, configure settings to read from env
- **Priority:** Critical
- **Dependencies:** Task 1
- **Estimated Time:** 30 min
- **Definition of Done:** All secrets in .env, .env.example committed, .env in .gitignore

### Task 8: Set Up Common App - Base Model
- **Description:** Create abstract BaseModel with UUID primary key, created_at, updated_at
- **Priority:** High
- **Dependencies:** Task 6
- **Estimated Time:** 30 min
- **Definition of Done:** BaseModel usable as base for all other models

### Task 9: Set Up Common App - Exception Handler
- **Description:** Create custom DRF exception handler with consistent error format
- **Priority:** High
- **Dependencies:** Task 3
- **Estimated Time:** 1 hour
- **Definition of Done:** All API errors return consistent JSON format

### Task 10: Set Up Common App - Pagination
- **Description:** Create standard pagination classes (page number, cursor)
- **Priority:** Medium
- **Dependencies:** Task 3
- **Estimated Time:** 30 min
- **Definition of Done:** Default pagination configured, cursor pagination available

### Task 11: Initialize React Project with Vite
- **Description:** Create React + TypeScript project using Vite, configure path aliases
- **Priority:** Critical
- **Dependencies:** None
- **Estimated Time:** 30 min
- **Definition of Done:** Vite dev server runs, TypeScript compiles, path aliases work

### Task 12: Install and Configure Tailwind CSS
- **Description:** Set up Tailwind CSS with custom theme, dark mode, font configuration
- **Priority:** Critical
- **Dependencies:** Task 11
- **Estimated Time:** 30 min
- **Definition of Done:** Tailwind classes work, custom colors defined, dark mode toggle works

### Task 13: Install and Configure ShadCN UI
- **Description:** Initialize ShadCN UI, install base components (Button, Input, Card, etc.)
- **Priority:** Critical
- **Dependencies:** Task 12
- **Estimated Time:** 1 hour
- **Definition of Done:** ShadCN components render correctly, theme customized

### Task 14: Set Up React Router
- **Description:** Configure React Router v6 with route structure, lazy loading
- **Priority:** Critical
- **Dependencies:** Task 11
- **Estimated Time:** 1 hour
- **Definition of Done:** All routes defined, lazy loading works, 404 page exists

### Task 15: Set Up React Query
- **Description:** Configure React Query with default options, devtools
- **Priority:** High
- **Dependencies:** Task 11
- **Estimated Time:** 30 min
- **Definition of Done:** QueryClient configured, devtools available in development

### Task 16: Create Axios API Client
- **Description:** Set up Axios instance with base URL, interceptors for auth, error handling
- **Priority:** High
- **Dependencies:** Task 11
- **Estimated Time:** 1 hour
- **Definition of Done:** API client handles auth headers, token refresh, error formatting

### Task 17: Create Docker Compose File
- **Description:** Create docker-compose.yml with all services (DB, Redis, API, Worker, Frontend)
- **Priority:** Critical
- **Dependencies:** Tasks 1-5
- **Estimated Time:** 2 hours
- **Definition of Done:** `docker-compose up` starts entire stack, services communicate

### Task 18: Create Backend Dockerfile
- **Description:** Multi-stage Dockerfile for Django API service
- **Priority:** High
- **Dependencies:** Task 1
- **Estimated Time:** 1 hour
- **Definition of Done:** Docker image builds, container runs, API accessible

### Task 19: Create Frontend Dockerfile (Dev)
- **Description:** Dockerfile for frontend development with hot reload
- **Priority:** Medium
- **Dependencies:** Task 11
- **Estimated Time:** 30 min
- **Definition of Done:** Frontend container runs with hot reload working

### Task 20: Configure CORS
- **Description:** Set up django-cors-headers with proper configuration
- **Priority:** High
- **Dependencies:** Task 1
- **Estimated Time:** 30 min
- **Definition of Done:** Frontend can make requests to backend without CORS errors

### Task 21: Set Up GitHub Actions CI
- **Description:** Create CI workflow for linting, type checking, and tests on PR
- **Priority:** High
- **Dependencies:** Tasks 17-18
- **Estimated Time:** 2 hours
- **Definition of Done:** CI runs on push/PR, reports pass/fail status

### Task 22: Configure Python Linting (Ruff)
- **Description:** Set up Ruff for Python linting and formatting
- **Priority:** Medium
- **Dependencies:** Task 1
- **Estimated Time:** 30 min
- **Definition of Done:** `ruff check` passes, `ruff format` configured

### Task 23: Configure Frontend Linting (ESLint + Prettier)
- **Description:** Set up ESLint and Prettier for TypeScript/React
- **Priority:** Medium
- **Dependencies:** Task 11
- **Estimated Time:** 30 min
- **Definition of Done:** `pnpm lint` passes, formatting consistent

### Task 24: Create .gitignore Files
- **Description:** Create comprehensive .gitignore for Python, Node, IDE, env files
- **Priority:** Low
- **Dependencies:** None
- **Estimated Time:** 15 min
- **Definition of Done:** Sensitive and generated files excluded from git

### Task 25: Create README with Setup Instructions
- **Description:** Write README with project overview, prerequisites, local setup steps
- **Priority:** Medium
- **Dependencies:** Task 17
- **Estimated Time:** 1 hour
- **Definition of Done:** New developer can set up project following README

---

## Milestone 2: Authentication (Tasks 26-55)

### Task 26: Create Custom User Model
- **Description:** Create User model extending AbstractBaseUser with email as username
- **Priority:** Critical
- **Dependencies:** Task 8
- **Estimated Time:** 1 hour
- **Definition of Done:** Custom user model with email login, custom manager, admin registered

### Task 27: Create Profile Model
- **Description:** Create Profile model with OneToOne to User, auto-create via signal
- **Priority:** High
- **Dependencies:** Task 26
- **Estimated Time:** 30 min
- **Definition of Done:** Profile auto-created on user creation, all fields defined

### Task 28: Install and Configure JWT (SimpleJWT)
- **Description:** Install djangorestframework-simplejwt, configure token lifetimes
- **Priority:** Critical
- **Dependencies:** Task 3, Task 26
- **Estimated Time:** 1 hour
- **Definition of Done:** JWT tokens generated on login, validated on protected endpoints

### Task 29: Create Registration Endpoint
- **Description:** POST /auth/register with email, password, name validation
- **Priority:** Critical
- **Dependencies:** Task 26, Task 28
- **Estimated Time:** 2 hours
- **Definition of Done:** New users can register, validation works, tokens returned

### Task 30: Create Login Endpoint
- **Description:** POST /auth/login with email/password, returns JWT pair
- **Priority:** Critical
- **Dependencies:** Task 28
- **Estimated Time:** 1 hour
- **Definition of Done:** Valid credentials return tokens, invalid return 401

### Task 31: Create Token Refresh Endpoint
- **Description:** POST /auth/refresh with refresh token, returns new access token
- **Priority:** Critical
- **Dependencies:** Task 28
- **Estimated Time:** 1 hour
- **Definition of Done:** Valid refresh returns new access, expired returns 401

### Task 32: Create Logout Endpoint
- **Description:** POST /auth/logout blacklists refresh token
- **Priority:** High
- **Dependencies:** Task 28
- **Estimated Time:** 1 hour
- **Definition of Done:** Blacklisted tokens cannot be used for refresh

### Task 33: Create Password Change Endpoint
- **Description:** POST /auth/password/change with old/new password
- **Priority:** High
- **Dependencies:** Task 28
- **Estimated Time:** 1 hour
- **Definition of Done:** Password changes with proper validation

### Task 34: Create User Profile Endpoints
- **Description:** GET/PATCH /users/me for profile retrieval and update
- **Priority:** High
- **Dependencies:** Task 27, Task 28
- **Estimated Time:** 1.5 hours
- **Definition of Done:** Profile readable and updatable, proper serialization

### Task 35: Create Password Validators
- **Description:** Custom validators: min length, uppercase, number, special char
- **Priority:** Medium
- **Dependencies:** Task 29
- **Estimated Time:** 30 min
- **Definition of Done:** Weak passwords rejected with clear error messages

### Task 36: Implement Token Rotation
- **Description:** Issue new refresh token on each refresh, blacklist old one
- **Priority:** High
- **Dependencies:** Task 31
- **Estimated Time:** 1 hour
- **Definition of Done:** Each refresh returns new pair, old refresh blacklisted

### Task 37: Add Rate Limiting to Auth Endpoints
- **Description:** 5 requests/minute for login/register to prevent brute force
- **Priority:** High
- **Dependencies:** Task 29, Task 30
- **Estimated Time:** 1 hour
- **Definition of Done:** 6th request in a minute returns 429

### Task 38: Create Auth Unit Tests
- **Description:** Test registration, login, refresh, logout, password change
- **Priority:** High
- **Dependencies:** Tasks 29-34
- **Estimated Time:** 3 hours
- **Definition of Done:** All auth flows tested, edge cases covered, >90% coverage

### Task 39: Create Frontend Auth Context
- **Description:** React context for auth state, login/logout methods, token storage
- **Priority:** Critical
- **Dependencies:** Task 16
- **Estimated Time:** 2 hours
- **Definition of Done:** Auth state accessible throughout app, tokens persisted

### Task 40: Create Login Page
- **Description:** Login form with email/password, validation, error display
- **Priority:** Critical
- **Dependencies:** Task 13, Task 39
- **Estimated Time:** 2 hours
- **Definition of Done:** Login works end-to-end, validation shown, redirect on success

### Task 41: Create Registration Page
- **Description:** Register form with all fields, password strength indicator
- **Priority:** Critical
- **Dependencies:** Task 13, Task 39
- **Estimated Time:** 2 hours
- **Definition of Done:** Registration works end-to-end, validation, redirect

### Task 42: Create Protected Route Component
- **Description:** HOC/wrapper that redirects to login if not authenticated
- **Priority:** Critical
- **Dependencies:** Task 39, Task 14
- **Estimated Time:** 1 hour
- **Definition of Done:** Unauthenticated users redirected, auth users proceed

### Task 43: Implement Token Refresh in API Client
- **Description:** Axios interceptor that auto-refreshes expired tokens
- **Priority:** Critical
- **Dependencies:** Task 16, Task 39
- **Estimated Time:** 2 hours
- **Definition of Done:** 401 triggers refresh, retries original request, handles failure

### Task 44: Create Forgot Password Page
- **Description:** Email input form for password reset initiation
- **Priority:** Medium
- **Dependencies:** Task 13
- **Estimated Time:** 1 hour
- **Definition of Done:** Form submits, shows confirmation message

### Task 45: Create Password Reset Backend
- **Description:** Generate reset token, send email, validate and reset
- **Priority:** Medium
- **Dependencies:** Task 26
- **Estimated Time:** 2 hours
- **Definition of Done:** Reset email sent, token valid for 1 hour, password changes

### Task 46: Create Frontend Form Validation Utils
- **Description:** Zod schemas for auth forms, reusable validation patterns
- **Priority:** Medium
- **Dependencies:** Task 11
- **Estimated Time:** 1 hour
- **Definition of Done:** All auth forms validated client-side before submit

### Task 47: Create User Menu Component
- **Description:** Dropdown with avatar, name, settings link, logout
- **Priority:** Medium
- **Dependencies:** Task 39, Task 13
- **Estimated Time:** 1 hour
- **Definition of Done:** Menu shows user info, logout works, links navigate

### Task 48: Implement Email Verification
- **Description:** Send verification email on register, verify endpoint
- **Priority:** Medium
- **Dependencies:** Task 29
- **Estimated Time:** 2 hours
- **Definition of Done:** Verification email sent, link activates account

### Task 49: Create Settings Page - Profile Tab
- **Description:** Profile edit form (name, bio, company, avatar)
- **Priority:** Medium
- **Dependencies:** Task 34, Task 13
- **Estimated Time:** 2 hours
- **Definition of Done:** Profile updates save and display correctly

### Task 50: Create Settings Page - Account Tab
- **Description:** Password change form, account deletion option
- **Priority:** Medium
- **Dependencies:** Task 33, Task 13
- **Estimated Time:** 1.5 hours
- **Definition of Done:** Password change works, delete shows confirmation

### Task 51: Create Frontend Auth Tests
- **Description:** Unit tests for auth context, login/register forms
- **Priority:** Medium
- **Dependencies:** Tasks 39-42
- **Estimated Time:** 2 hours
- **Definition of Done:** Auth flow tested, token handling verified

### Task 52: Security Hardening - Auth Headers
- **Description:** Add security headers (CSP, X-Frame-Options, etc.)
- **Priority:** High
- **Dependencies:** Task 20
- **Estimated Time:** 1 hour
- **Definition of Done:** All security headers present in responses

### Task 53: Create Request Logging Middleware
- **Description:** Log all requests with method, path, status, duration
- **Priority:** Medium
- **Dependencies:** Task 1
- **Estimated Time:** 1 hour
- **Definition of Done:** All requests logged with structured format

### Task 54: Create API Versioning
- **Description:** Set up URL-based versioning (v1/) for all endpoints
- **Priority:** High
- **Dependencies:** Task 3
- **Estimated Time:** 30 min
- **Definition of Done:** All endpoints under /api/v1/ namespace

### Task 55: Create Auth Integration Tests
- **Description:** Full flow tests: register → login → access → refresh → logout
- **Priority:** High
- **Dependencies:** Tasks 29-34
- **Estimated Time:** 2 hours
- **Definition of Done:** Full auth lifecycle tested end-to-end

---

## Milestone 3: Repository Management (Tasks 56-85)

### Task 56: Create Repository Model
- **Description:** Repository model with all fields, status choices, manager
- **Priority:** Critical
- **Dependencies:** Task 8, Task 26
- **Estimated Time:** 1 hour
- **Definition of Done:** Model created with proper fields, admin registered

### Task 57: Create RepositoryFile Model
- **Description:** Model for individual files within a repository
- **Priority:** Critical
- **Dependencies:** Task 56
- **Estimated Time:** 30 min
- **Definition of Done:** Model with file_path, language, size, content_hash

### Task 58: Create Branch Model
- **Description:** Model for repository branches with indexing status
- **Priority:** Medium
- **Dependencies:** Task 56
- **Estimated Time:** 30 min
- **Definition of Done:** Branch model linked to repository

### Task 59: Create Repository Serializers
- **Description:** List, detail, create serializers with proper validation
- **Priority:** Critical
- **Dependencies:** Task 56
- **Estimated Time:** 1.5 hours
- **Definition of Done:** All serializers handle input validation and output formatting

### Task 60: Create Repository ViewSet
- **Description:** ModelViewSet with list, create, retrieve, delete actions
- **Priority:** Critical
- **Dependencies:** Task 59
- **Estimated Time:** 2 hours
- **Definition of Done:** Full CRUD via API, proper permissions

### Task 61: Create IsRepositoryOwner Permission
- **Description:** Custom permission class checking user owns the repository
- **Priority:** Critical
- **Dependencies:** Task 56
- **Estimated Time:** 30 min
- **Definition of Done:** Non-owners get 403, owners can access

### Task 62: Create Repository List Filtering
- **Description:** Filter by status, search by name, ordering options
- **Priority:** High
- **Dependencies:** Task 60
- **Estimated Time:** 1 hour
- **Definition of Done:** Filters work via query parameters

### Task 63: Implement File Upload Handling
- **Description:** Accept ZIP/TAR uploads, validate, store temporarily
- **Priority:** Critical
- **Dependencies:** Task 60
- **Estimated Time:** 2 hours
- **Definition of Done:** Files uploaded, validated, stored for processing

### Task 64: Create File Browser Endpoint
- **Description:** GET /repositories/{id}/files with path navigation
- **Priority:** High
- **Dependencies:** Task 57
- **Estimated Time:** 1.5 hours
- **Definition of Done:** Returns directory tree, navigable by path param

### Task 65: Create File Content Endpoint
- **Description:** GET /repositories/{id}/files/{file_id}/content
- **Priority:** High
- **Dependencies:** Task 57
- **Estimated Time:** 1 hour
- **Definition of Done:** Returns file content with metadata

### Task 66: Implement Repository Deletion Cascade
- **Description:** Delete repo cascades to files, chunks, embeddings, conversations
- **Priority:** High
- **Dependencies:** Task 56
- **Estimated Time:** 1 hour
- **Definition of Done:** All related data cleaned up on delete

### Task 67: Create Reindex Endpoint
- **Description:** POST /repositories/{id}/reindex dispatches new indexing job
- **Priority:** High
- **Dependencies:** Task 60
- **Estimated Time:** 1 hour
- **Definition of Done:** Reindex clears old data, starts fresh indexing

### Task 68: Create Repository Status Machine
- **Description:** Enforce valid status transitions (pending→indexing→ready/failed)
- **Priority:** High
- **Dependencies:** Task 56
- **Estimated Time:** 1 hour
- **Definition of Done:** Invalid transitions raise error

### Task 69: Create Repository Unit Tests
- **Description:** Test models, serializers, permissions, status transitions
- **Priority:** High
- **Dependencies:** Tasks 56-68
- **Estimated Time:** 3 hours
- **Definition of Done:** All repository logic tested

### Task 70: Create Frontend Repository Types
- **Description:** TypeScript interfaces for Repository, File, Branch
- **Priority:** High
- **Dependencies:** Task 11
- **Estimated Time:** 30 min
- **Definition of Done:** All API response types defined

### Task 71: Create Repository API Hooks
- **Description:** React Query hooks: useRepositories, useRepository, useCreateRepo
- **Priority:** High
- **Dependencies:** Task 15, Task 70
- **Estimated Time:** 2 hours
- **Definition of Done:** All CRUD operations available via hooks

### Task 72: Create Repository List Page
- **Description:** Page showing all user repos with status, filters, search
- **Priority:** High
- **Dependencies:** Task 71, Task 13
- **Estimated Time:** 3 hours
- **Definition of Done:** Repos listed with filtering, status badges, pagination

### Task 73: Create Repository Card Component
- **Description:** Card showing repo name, status, languages, last indexed
- **Priority:** Medium
- **Dependencies:** Task 13
- **Estimated Time:** 1 hour
- **Definition of Done:** Card renders all info, responsive, clickable

### Task 74: Create Repository Detail Page
- **Description:** Page with repo info, stats, tabs for files/chat/analytics
- **Priority:** High
- **Dependencies:** Task 71
- **Estimated Time:** 3 hours
- **Definition of Done:** Detail page with all sections, tab navigation

### Task 75: Create Import Page - Upload Tab
- **Description:** Drag-and-drop file upload with progress indicator
- **Priority:** High
- **Dependencies:** Task 71, Task 13
- **Estimated Time:** 3 hours
- **Definition of Done:** Upload works with progress, validation, error handling

### Task 76: Create Import Page - GitHub Tab
- **Description:** GitHub repo picker (implemented after GitHub integration)
- **Priority:** Medium
- **Dependencies:** Task 71
- **Estimated Time:** 2 hours (placeholder until Milestone 8)
- **Definition of Done:** Tab exists with "Connect GitHub" prompt

### Task 77: Create File Browser Component
- **Description:** Tree-view file browser with directory navigation
- **Priority:** High
- **Dependencies:** Task 64, Task 71
- **Estimated Time:** 3 hours
- **Definition of Done:** Navigate directories, show file icons, click to view

### Task 78: Create Repository Progress Indicator
- **Description:** Show indexing progress with percentage and file count
- **Priority:** Medium
- **Dependencies:** Task 13
- **Estimated Time:** 1 hour
- **Definition of Done:** Progress bar animates, shows real-time status

### Task 79: Create Delete Repository Dialog
- **Description:** Confirmation dialog for repository deletion
- **Priority:** Medium
- **Dependencies:** Task 13
- **Estimated Time:** 1 hour
- **Definition of Done:** Confirmation required, delete executes, list refreshes

### Task 80: Create Repository Empty State
- **Description:** Empty state when user has no repositories with CTA
- **Priority:** Low
- **Dependencies:** Task 13
- **Estimated Time:** 30 min
- **Definition of Done:** Attractive empty state with "Import" button

### Task 81: Add File Size Validation
- **Description:** Reject uploads over 500MB with clear error
- **Priority:** High
- **Dependencies:** Task 63
- **Estimated Time:** 30 min
- **Definition of Done:** Large files rejected with appropriate error

### Task 82: Add File Type Validation
- **Description:** Only allow .zip, .tar, .tar.gz file extensions
- **Priority:** High
- **Dependencies:** Task 63
- **Estimated Time:** 30 min
- **Definition of Done:** Invalid file types rejected

### Task 83: Create Repository Integration Tests
- **Description:** Test full CRUD flow, upload, deletion cascade
- **Priority:** High
- **Dependencies:** Tasks 56-68
- **Estimated Time:** 2 hours
- **Definition of Done:** Integration tests cover all flows

### Task 84: Add Repository Quota Check
- **Description:** Limit number of repos per user (free tier: 3)
- **Priority:** Medium
- **Dependencies:** Task 60
- **Estimated Time:** 1 hour
- **Definition of Done:** Exceeding quota returns 403 with upgrade message

### Task 85: Create Frontend Repository Tests
- **Description:** Test list page, card component, upload form
- **Priority:** Medium
- **Dependencies:** Tasks 72-79
- **Estimated Time:** 2 hours
- **Definition of Done:** Key components tested

---

## Milestone 4: Code Indexing (Tasks 86-115)

### Task 86: Create CodeChunk Model
- **Description:** Model for code chunks with content, type, metadata
- **Priority:** Critical
- **Dependencies:** Task 57
- **Estimated Time:** 1 hour
- **Definition of Done:** Model with all fields, indexes, admin

### Task 87: Create IndexingJob Model
- **Description:** Model for tracking indexing jobs with status, progress
- **Priority:** Critical
- **Dependencies:** Task 56
- **Estimated Time:** 1 hour
- **Definition of Done:** Job model tracks progress, status, errors

### Task 88: Create File Filter Service
- **Description:** Service to apply exclusion rules (directories, extensions, binary)
- **Priority:** Critical
- **Dependencies:** Task 6
- **Estimated Time:** 2 hours
- **Definition of Done:** Excludes node_modules, binaries, build dirs correctly

### Task 89: Create Binary File Detector
- **Description:** Detect binary files by checking for null bytes and encoding
- **Priority:** High
- **Dependencies:** Task 88
- **Estimated Time:** 1 hour
- **Definition of Done:** Binary files correctly identified and excluded

### Task 90: Create Language Detector
- **Description:** Detect programming language from file extension and shebang
- **Priority:** High
- **Dependencies:** Task 6
- **Estimated Time:** 1 hour
- **Definition of Done:** 20+ languages detected accurately

### Task 91: Create AST-Based Chunker - Python
- **Description:** Parse Python AST to extract functions and classes as chunks
- **Priority:** Critical
- **Dependencies:** Task 86
- **Estimated Time:** 3 hours
- **Definition of Done:** Python functions/classes extracted with metadata

### Task 92: Create AST-Based Chunker - JavaScript/TypeScript
- **Description:** Parse JS/TS to extract functions, classes, arrow functions
- **Priority:** Critical
- **Dependencies:** Task 86
- **Estimated Time:** 3 hours
- **Definition of Done:** JS/TS constructs extracted as chunks

### Task 93: Create Sliding Window Chunker
- **Description:** Fallback chunking with configurable window size and overlap
- **Priority:** High
- **Dependencies:** Task 86
- **Estimated Time:** 1.5 hours
- **Definition of Done:** Files chunked with correct overlap, line boundaries

### Task 94: Create Metadata Extractor
- **Description:** Extract function names, parameters, return types, docstrings
- **Priority:** High
- **Dependencies:** Tasks 91-92
- **Estimated Time:** 2 hours
- **Definition of Done:** Rich metadata attached to all chunks

### Task 95: Create Indexing Celery Task
- **Description:** Main task that orchestrates full indexing pipeline
- **Priority:** Critical
- **Dependencies:** Tasks 88-94
- **Estimated Time:** 3 hours
- **Definition of Done:** Task processes repo end-to-end, reports progress

### Task 96: Implement Progress Tracking
- **Description:** Update IndexingJob progress as files are processed
- **Priority:** High
- **Dependencies:** Task 87, Task 95
- **Estimated Time:** 1 hour
- **Definition of Done:** Progress updates in real-time, percentage accurate

### Task 97: Implement Error Handling in Indexing
- **Description:** Handle individual file failures without stopping the job
- **Priority:** High
- **Dependencies:** Task 95
- **Estimated Time:** 1.5 hours
- **Definition of Done:** Failed files logged, job continues, summary at end

### Task 98: Create Incremental Re-indexing
- **Description:** Compare file hashes, only re-process changed files
- **Priority:** Medium
- **Dependencies:** Task 95
- **Estimated Time:** 2 hours
- **Definition of Done:** Only modified files re-chunked and re-embedded

### Task 99: Create Archive Extraction Service
- **Description:** Extract ZIP/TAR archives safely (zip bomb protection)
- **Priority:** High
- **Dependencies:** Task 63
- **Estimated Time:** 2 hours
- **Definition of Done:** Archives extracted safely with size ratio limits

### Task 100: Create Temp File Cleanup Task
- **Description:** Celery task to clean up temporary extraction directories
- **Priority:** Medium
- **Dependencies:** Task 95
- **Estimated Time:** 1 hour
- **Definition of Done:** Temp dirs cleaned after processing or on failure

### Task 101: Create Indexing Status WebSocket
- **Description:** Send progress updates to frontend via WebSocket
- **Priority:** Medium
- **Dependencies:** Task 96
- **Estimated Time:** 2 hours
- **Definition of Done:** Frontend receives real-time progress updates

### Task 102: Create Indexing Job Endpoint
- **Description:** GET /indexing/jobs/{id} for polling job status
- **Priority:** High
- **Dependencies:** Task 87
- **Estimated Time:** 1 hour
- **Definition of Done:** Returns progress, status, timing information

### Task 103: Add AST Chunker - Java
- **Description:** Parse Java to extract classes and methods
- **Priority:** Medium
- **Dependencies:** Task 91
- **Estimated Time:** 2 hours
- **Definition of Done:** Java classes/methods extracted as chunks

### Task 104: Add AST Chunker - Go
- **Description:** Parse Go to extract functions and structs
- **Priority:** Medium
- **Dependencies:** Task 91
- **Estimated Time:** 2 hours
- **Definition of Done:** Go functions/structs extracted as chunks

### Task 105: Create Chunking Unit Tests
- **Description:** Test all chunkers with various input files
- **Priority:** High
- **Dependencies:** Tasks 91-93
- **Estimated Time:** 3 hours
- **Definition of Done:** All chunkers tested with real code samples

### Task 106: Create File Filter Unit Tests
- **Description:** Test exclusion rules, binary detection, language detection
- **Priority:** High
- **Dependencies:** Tasks 88-90
- **Estimated Time:** 2 hours
- **Definition of Done:** All filter rules tested

### Task 107: Create Indexing Integration Tests
- **Description:** Test full pipeline with sample repositories
- **Priority:** High
- **Dependencies:** Task 95
- **Estimated Time:** 3 hours
- **Definition of Done:** End-to-end indexing tested with assertions

### Task 108: Create Sample Test Repository
- **Description:** Create a small multi-language repo for testing
- **Priority:** Medium
- **Dependencies:** None
- **Estimated Time:** 1 hour
- **Definition of Done:** Test repo with Python, JS, Go files

### Task 109: Optimize Chunk Storage (Bulk Create)
- **Description:** Use bulk_create for chunks and files for performance
- **Priority:** Medium
- **Dependencies:** Task 95
- **Estimated Time:** 1 hour
- **Definition of Done:** Bulk operations used, insert time reduced

### Task 110: Create IndexingLog Model
- **Description:** Model for detailed logging during indexing
- **Priority:** Low
- **Dependencies:** Task 87
- **Estimated Time:** 30 min
- **Definition of Done:** Logs stored per job for debugging

### Task 111: Implement Max File Count Limit
- **Description:** Limit repos to 50,000 files to prevent abuse
- **Priority:** Medium
- **Dependencies:** Task 95
- **Estimated Time:** 30 min
- **Definition of Done:** Over-limit repos rejected with message

### Task 112: Create Chunk Type Constants
- **Description:** Define chunk type enum (function, class, method, module, block)
- **Priority:** Low
- **Dependencies:** Task 86
- **Estimated Time:** 15 min
- **Definition of Done:** Constants defined, used throughout

### Task 113: Add Docstring Extraction
- **Description:** Extract docstrings from functions/classes during chunking
- **Priority:** Medium
- **Dependencies:** Task 91
- **Estimated Time:** 1 hour
- **Definition of Done:** Docstrings stored in chunk metadata

### Task 114: Add Import Statement Tracking
- **Description:** Track imports per file for dependency analysis
- **Priority:** Low
- **Dependencies:** Task 94
- **Estimated Time:** 1 hour
- **Definition of Done:** Imports stored in file/chunk metadata

### Task 115: Create Indexing Admin Views
- **Description:** Django admin for IndexingJob with status filters
- **Priority:** Low
- **Dependencies:** Task 87
- **Estimated Time:** 30 min
- **Definition of Done:** Admin shows jobs with filtering, progress display

---

## Milestone 5: Embeddings & Search (Tasks 116-140)

### Task 116: Install Sentence Transformers
- **Description:** Install sentence-transformers, download all-MiniLM-L6-v2 model
- **Priority:** Critical
- **Dependencies:** Task 1
- **Estimated Time:** 30 min
- **Definition of Done:** Model loads and generates embeddings

### Task 117: Create Embedding Model with pgvector
- **Description:** Model with VECTOR(384) column, repository_id, chunk_id
- **Priority:** Critical
- **Dependencies:** Task 2, Task 86
- **Estimated Time:** 1 hour
- **Definition of Done:** Embeddings stored as vectors in PostgreSQL

### Task 118: Create Embedding Generation Service
- **Description:** Service that takes chunks and returns embeddings
- **Priority:** Critical
- **Dependencies:** Task 116
- **Estimated Time:** 2 hours
- **Definition of Done:** Chunks converted to 384-dim embeddings

### Task 119: Implement Context Augmentation
- **Description:** Prepend file path + language + symbol name before embedding
- **Priority:** High
- **Dependencies:** Task 118
- **Estimated Time:** 1 hour
- **Definition of Done:** Augmented text improves retrieval relevance

### Task 120: Implement Batch Embedding Generation
- **Description:** Process chunks in batches of 32 for efficiency
- **Priority:** High
- **Dependencies:** Task 118
- **Estimated Time:** 1 hour
- **Definition of Done:** Batch processing works, progress reported per batch

### Task 121: Create HNSW Vector Index
- **Description:** Create HNSW index on embedding column for fast ANN search
- **Priority:** Critical
- **Dependencies:** Task 117
- **Estimated Time:** 1 hour
- **Definition of Done:** Index created, queries use index, search fast

### Task 122: Create Vector Similarity Search Service
- **Description:** Service that searches embeddings by cosine similarity
- **Priority:** Critical
- **Dependencies:** Task 117, Task 121
- **Estimated Time:** 2 hours
- **Definition of Done:** Search returns top-K similar chunks with scores

### Task 123: Implement Repository-Scoped Search
- **Description:** Filter vector search by repository_id
- **Priority:** Critical
- **Dependencies:** Task 122
- **Estimated Time:** 30 min
- **Definition of Done:** Search only returns results from specified repo

### Task 124: Create Search API Endpoint
- **Description:** POST /search with query, repo_ids, filters, limit
- **Priority:** Critical
- **Dependencies:** Task 122
- **Estimated Time:** 2 hours
- **Definition of Done:** Search endpoint returns formatted results

### Task 125: Implement Search Filters
- **Description:** Filter by language, file type, chunk type
- **Priority:** High
- **Dependencies:** Task 124
- **Estimated Time:** 1.5 hours
- **Definition of Done:** All filter combinations work correctly

### Task 126: Create Result Re-Ranking Service
- **Description:** Re-rank top results by metadata relevance (symbol match, recency)
- **Priority:** Medium
- **Dependencies:** Task 122
- **Estimated Time:** 2 hours
- **Definition of Done:** Re-ranked results more relevant than raw similarity

### Task 127: Implement Query Embedding Generation
- **Description:** Generate embedding for user search queries using same model
- **Priority:** Critical
- **Dependencies:** Task 118
- **Estimated Time:** 30 min
- **Definition of Done:** Query embedded with same model, returns vector

### Task 128: Create Embedding Generation Celery Task
- **Description:** Integrate embedding generation into indexing pipeline
- **Priority:** Critical
- **Dependencies:** Task 120, Task 95
- **Estimated Time:** 2 hours
- **Definition of Done:** Embeddings generated as part of indexing workflow

### Task 129: Implement Embedding Cache
- **Description:** Cache query embeddings in Redis (TTL 1 hour)
- **Priority:** Medium
- **Dependencies:** Task 127
- **Estimated Time:** 1 hour
- **Definition of Done:** Repeated queries use cached embeddings

### Task 130: Create Search Result Cache
- **Description:** Cache search results in Redis (TTL 5 min)
- **Priority:** Medium
- **Dependencies:** Task 124
- **Estimated Time:** 1 hour
- **Definition of Done:** Repeated searches return cached results

### Task 131: Implement Cache Invalidation on Reindex
- **Description:** Clear all caches for a repo when re-indexed
- **Priority:** Medium
- **Dependencies:** Tasks 129-130
- **Estimated Time:** 30 min
- **Definition of Done:** Reindex clears related caches

### Task 132: Create Embedding Unit Tests
- **Description:** Test generation, storage, dimensions, normalization
- **Priority:** High
- **Dependencies:** Task 118
- **Estimated Time:** 2 hours
- **Definition of Done:** Embedding pipeline fully tested

### Task 133: Create Search Unit Tests
- **Description:** Test search endpoint, filters, ranking
- **Priority:** High
- **Dependencies:** Task 124
- **Estimated Time:** 2 hours
- **Definition of Done:** Search functionality fully tested

### Task 134: Create Search Performance Tests
- **Description:** Benchmark search at 1K, 10K, 100K vectors
- **Priority:** Medium
- **Dependencies:** Task 122
- **Estimated Time:** 2 hours
- **Definition of Done:** Performance within targets at each scale

### Task 135: Create Frontend Search Page
- **Description:** Search input, filter panel, results list
- **Priority:** High
- **Dependencies:** Task 124, Task 13
- **Estimated Time:** 3 hours
- **Definition of Done:** Search works end-to-end, results clickable

### Task 136: Create Search Input Component
- **Description:** Search input with debounced queries, clear button
- **Priority:** Medium
- **Dependencies:** Task 13
- **Estimated Time:** 1 hour
- **Definition of Done:** Debounced input, clear functionality

### Task 137: Create Search Filters Component
- **Description:** Language, file type, chunk type filter checkboxes
- **Priority:** Medium
- **Dependencies:** Task 13
- **Estimated Time:** 1.5 hours
- **Definition of Done:** Filters apply to search results

### Task 138: Create Search Result Card
- **Description:** Card showing code snippet, file path, relevance score
- **Priority:** Medium
- **Dependencies:** Task 13
- **Estimated Time:** 1 hour
- **Definition of Done:** Results display clearly with all metadata

### Task 139: Implement Multi-Repository Search
- **Description:** Search across multiple repos simultaneously
- **Priority:** Medium
- **Dependencies:** Task 123
- **Estimated Time:** 1 hour
- **Definition of Done:** Search works across selected repos

### Task 140: Create Embedding Coverage Metric
- **Description:** Calculate percentage of chunks with embeddings
- **Priority:** Low
- **Dependencies:** Task 117
- **Estimated Time:** 30 min
- **Definition of Done:** Coverage percentage displayed in repo analytics

---

## Milestone 6: AI Chat - RAG (Tasks 141-175)

### Task 141: Create Conversation Model
- **Description:** Model with user, repository, title, status, message_count
- **Priority:** Critical
- **Dependencies:** Task 26, Task 56
- **Estimated Time:** 1 hour
- **Definition of Done:** Conversation model with all fields

### Task 142: Create Message Model
- **Description:** Model with conversation, role, content, sources, token_count
- **Priority:** Critical
- **Dependencies:** Task 141
- **Estimated Time:** 1 hour
- **Definition of Done:** Message model stores all chat data

### Task 143: Create LLM Provider Interface
- **Description:** Abstract base class for LLM providers with generate method
- **Priority:** Critical
- **Dependencies:** Task 6
- **Estimated Time:** 1 hour
- **Definition of Done:** Interface defined with sync and async generate methods

### Task 144: Create OpenAI Provider
- **Description:** Implement LLM interface for OpenAI API (gpt-4o-mini)
- **Priority:** Critical
- **Dependencies:** Task 143
- **Estimated Time:** 2 hours
- **Definition of Done:** OpenAI calls work, streaming supported

### Task 145: Create Ollama Provider
- **Description:** Implement LLM interface for Ollama local models
- **Priority:** High
- **Dependencies:** Task 143
- **Estimated Time:** 2 hours
- **Definition of Done:** Ollama calls work, streaming supported

### Task 146: Create Prompt Builder Service
- **Description:** Service that constructs system + context + history + query prompts
- **Priority:** Critical
- **Dependencies:** Task 143
- **Estimated Time:** 2 hours
- **Definition of Done:** Prompts constructed correctly with token budgeting

### Task 147: Create System Prompt Templates
- **Description:** Define system prompts for chat, explain, docs, tests, bugs
- **Priority:** Critical
- **Dependencies:** Task 146
- **Estimated Time:** 2 hours
- **Definition of Done:** All system prompts defined with clear instructions

### Task 148: Create RAG Pipeline Service
- **Description:** Orchestrate: embed query → search → build context → generate
- **Priority:** Critical
- **Dependencies:** Task 122, Task 146, Task 144
- **Estimated Time:** 4 hours
- **Definition of Done:** Full RAG pipeline works end-to-end

### Task 149: Create Conversation CRUD Endpoints
- **Description:** GET/POST /conversations, GET/DELETE /conversations/{id}
- **Priority:** Critical
- **Dependencies:** Task 141
- **Estimated Time:** 2 hours
- **Definition of Done:** Conversations created, listed, archived

### Task 150: Create Message Send Endpoint
- **Description:** POST /conversations/{id}/messages - triggers RAG and returns response
- **Priority:** Critical
- **Dependencies:** Task 142, Task 148
- **Estimated Time:** 3 hours
- **Definition of Done:** Messages processed through RAG, response saved and returned

### Task 151: Implement SSE Streaming
- **Description:** Stream LLM tokens via Server-Sent Events
- **Priority:** High
- **Dependencies:** Task 150
- **Estimated Time:** 3 hours
- **Definition of Done:** Tokens stream to client in real-time

### Task 152: Implement Conversation Memory
- **Description:** Include last N messages as context in prompts
- **Priority:** High
- **Dependencies:** Task 150
- **Estimated Time:** 1.5 hours
- **Definition of Done:** Follow-up questions maintain context

### Task 153: Implement Token Counting
- **Description:** Count tokens in prompts and responses, stay within budget
- **Priority:** High
- **Dependencies:** Task 146
- **Estimated Time:** 1.5 hours
- **Definition of Done:** Token counts accurate, budget enforced

### Task 154: Implement Context Window Management
- **Description:** Truncate/summarize context to fit within token limits
- **Priority:** High
- **Dependencies:** Task 153
- **Estimated Time:** 2 hours
- **Definition of Done:** Long contexts handled without exceeding limits

### Task 155: Create Source Reference Formatting
- **Description:** Format source chunks as references in responses
- **Priority:** Medium
- **Dependencies:** Task 150
- **Estimated Time:** 1 hour
- **Definition of Done:** Sources include file path, lines, relevance score

### Task 156: Implement Auto Title Generation
- **Description:** Generate conversation title from first message
- **Priority:** Medium
- **Dependencies:** Task 149
- **Estimated Time:** 1 hour
- **Definition of Done:** Titles auto-generated, meaningful, short

### Task 157: Create Conversation Permission
- **Description:** IsConversationOwner permission class
- **Priority:** High
- **Dependencies:** Task 141
- **Estimated Time:** 30 min
- **Definition of Done:** Only conversation owner can access messages

### Task 158: Create Message History Endpoint
- **Description:** GET /conversations/{id}/messages with pagination
- **Priority:** High
- **Dependencies:** Task 142
- **Estimated Time:** 1 hour
- **Definition of Done:** Returns paginated message history

### Task 159: Implement LLM Provider Selection
- **Description:** User can choose provider from profile settings
- **Priority:** Medium
- **Dependencies:** Tasks 144-145
- **Estimated Time:** 1 hour
- **Definition of Done:** Provider switches based on user preference

### Task 160: Implement Response Post-Processing
- **Description:** Validate code blocks, file paths, format sources
- **Priority:** Medium
- **Dependencies:** Task 150
- **Estimated Time:** 1.5 hours
- **Definition of Done:** Responses well-formatted with valid references

### Task 161: Create Chat Unit Tests
- **Description:** Test conversation CRUD, message flow, permissions
- **Priority:** High
- **Dependencies:** Tasks 149-150
- **Estimated Time:** 3 hours
- **Definition of Done:** All chat logic tested

### Task 162: Create RAG Pipeline Tests
- **Description:** Test retrieval quality, prompt construction, response generation
- **Priority:** High
- **Dependencies:** Task 148
- **Estimated Time:** 3 hours
- **Definition of Done:** RAG pipeline tested with sample data

### Task 163: Create Frontend Chat Types
- **Description:** TypeScript interfaces for Conversation, Message, Source
- **Priority:** High
- **Dependencies:** Task 11
- **Estimated Time:** 30 min
- **Definition of Done:** All chat-related types defined

### Task 164: Create Chat API Hooks
- **Description:** useConversations, useMessages, useSendMessage hooks
- **Priority:** High
- **Dependencies:** Task 163, Task 15
- **Estimated Time:** 2 hours
- **Definition of Done:** All chat operations available via hooks

### Task 165: Create Chat Page Layout
- **Description:** Split layout with conversation list and message area
- **Priority:** High
- **Dependencies:** Task 13
- **Estimated Time:** 2 hours
- **Definition of Done:** Layout responsive, sidebar/main split

### Task 166: Create Conversation List Component
- **Description:** Sidebar listing conversations with title and timestamp
- **Priority:** High
- **Dependencies:** Task 164
- **Estimated Time:** 1.5 hours
- **Definition of Done:** Conversations listed, clickable, active highlighted

### Task 167: Create Message Bubble Component
- **Description:** Message display with role styling, code blocks, sources
- **Priority:** High
- **Dependencies:** Task 13
- **Estimated Time:** 2 hours
- **Definition of Done:** User/assistant messages styled differently, code highlighted

### Task 168: Create Chat Input Component
- **Description:** Text input with send button, keyboard shortcuts
- **Priority:** High
- **Dependencies:** Task 13
- **Estimated Time:** 1.5 hours
- **Definition of Done:** Input sends messages, supports Enter/Shift+Enter

### Task 169: Create Code Block Component
- **Description:** Syntax-highlighted code block with copy button and language label
- **Priority:** High
- **Dependencies:** Task 13
- **Estimated Time:** 1.5 hours
- **Definition of Done:** Code renders with highlighting, copy works

### Task 170: Create Source Reference Component
- **Description:** Clickable source links showing file path and relevance
- **Priority:** Medium
- **Dependencies:** Task 13
- **Estimated Time:** 1 hour
- **Definition of Done:** Sources displayed, clickable to code viewer

### Task 171: Implement Streaming Message Display
- **Description:** Show tokens appearing in real-time during generation
- **Priority:** High
- **Dependencies:** Task 151, Task 167
- **Estimated Time:** 3 hours
- **Definition of Done:** Tokens appear smoothly, typing indicator shown

### Task 172: Create New Conversation Button
- **Description:** Button to start a new conversation with repo selector
- **Priority:** Medium
- **Dependencies:** Task 164
- **Estimated Time:** 1 hour
- **Definition of Done:** New conversations created, repo selected

### Task 173: Create Repository Selector for Chat
- **Description:** Dropdown to select which repo to chat about
- **Priority:** Medium
- **Dependencies:** Task 71
- **Estimated Time:** 1 hour
- **Definition of Done:** Repo selection changes chat context

### Task 174: Create Chat Loading States
- **Description:** Skeleton while loading, typing indicator during generation
- **Priority:** Medium
- **Dependencies:** Task 13
- **Estimated Time:** 1 hour
- **Definition of Done:** Loading states shown appropriately

### Task 175: Create Chat Frontend Tests
- **Description:** Test message display, input, streaming
- **Priority:** Medium
- **Dependencies:** Tasks 165-171
- **Estimated Time:** 2 hours
- **Definition of Done:** Chat UI components tested

---

## Milestone 7: AI Features (Tasks 176-200)

### Task 176: Create Code Explanation Endpoint
- **Description:** POST /ai/explain with chunk_id and detail level
- **Priority:** High
- **Dependencies:** Task 148
- **Estimated Time:** 2 hours
- **Definition of Done:** Explains code clearly with context

### Task 177: Create Explanation Prompt Template
- **Description:** System prompt for code explanation with formatting rules
- **Priority:** High
- **Dependencies:** Task 147
- **Estimated Time:** 1 hour
- **Definition of Done:** Explanation prompts produce clear results

### Task 178: Create Documentation Generation Endpoint
- **Description:** POST /ai/generate-docs with repo/chunk IDs and format
- **Priority:** High
- **Dependencies:** Task 148
- **Estimated Time:** 2 hours
- **Definition of Done:** Generates markdown documentation

### Task 179: Create Documentation Prompt Template
- **Description:** System prompt for doc generation (docstrings, README, API docs)
- **Priority:** High
- **Dependencies:** Task 147
- **Estimated Time:** 1 hour
- **Definition of Done:** Docs prompts produce well-structured output

### Task 180: Create Unit Test Generation Endpoint
- **Description:** POST /ai/generate-tests with chunk_id and framework
- **Priority:** High
- **Dependencies:** Task 148
- **Estimated Time:** 2 hours
- **Definition of Done:** Generates runnable test code

### Task 181: Create Test Generation Prompt Template
- **Description:** System prompt for test generation with framework support
- **Priority:** High
- **Dependencies:** Task 147
- **Estimated Time:** 1 hour
- **Definition of Done:** Tests generated with correct framework syntax

### Task 182: Create Bug Detection Endpoint
- **Description:** POST /ai/detect-bugs with repo/file scope
- **Priority:** High
- **Dependencies:** Task 148
- **Estimated Time:** 2 hours
- **Definition of Done:** Detects and categorizes potential bugs

### Task 183: Create Bug Detection Prompt Template
- **Description:** System prompt for bug detection with severity classification
- **Priority:** High
- **Dependencies:** Task 147
- **Estimated Time:** 1 hour
- **Definition of Done:** Bug reports include severity, description, suggestion

### Task 184: Create PR Review Endpoint
- **Description:** POST /ai/review-pr with repo and PR number
- **Priority:** High
- **Dependencies:** Task 148
- **Estimated Time:** 3 hours
- **Definition of Done:** Reviews PR diff with AI-powered suggestions

### Task 185: Create PR Review Prompt Template
- **Description:** System prompt for code review with focus areas
- **Priority:** High
- **Dependencies:** Task 147
- **Estimated Time:** 1 hour
- **Definition of Done:** Reviews cover bugs, style, security, performance

### Task 186: Create AI Feature Rate Limiting
- **Description:** Separate rate limits for AI features (20/min)
- **Priority:** High
- **Dependencies:** Task 37
- **Estimated Time:** 1 hour
- **Definition of Done:** AI endpoints rate-limited independently

### Task 187: Create AI Feature Serializers
- **Description:** Input/output serializers for all AI endpoints
- **Priority:** High
- **Dependencies:** Tasks 176-184
- **Estimated Time:** 2 hours
- **Definition of Done:** All AI inputs validated, outputs formatted

### Task 188: Create Frontend AI Action Buttons
- **Description:** Explain, Docs, Tests, Bugs buttons on code viewer
- **Priority:** High
- **Dependencies:** Task 13
- **Estimated Time:** 1.5 hours
- **Definition of Done:** Buttons trigger correct endpoints, show results

### Task 189: Create AI Response Modal
- **Description:** Modal showing AI-generated content (explanation, docs, tests)
- **Priority:** High
- **Dependencies:** Task 13
- **Estimated Time:** 2 hours
- **Definition of Done:** Modal displays formatted response, copy button

### Task 190: Create AI Feature Loading States
- **Description:** Loading indicators while AI generates responses
- **Priority:** Medium
- **Dependencies:** Task 188
- **Estimated Time:** 1 hour
- **Definition of Done:** Users see progress during generation

### Task 191: Create Documentation Viewer Page
- **Description:** Page displaying generated documentation with navigation
- **Priority:** Medium
- **Dependencies:** Task 178
- **Estimated Time:** 2 hours
- **Definition of Done:** Docs displayed with markdown rendering

### Task 192: Create Bug Report Display
- **Description:** Component showing detected bugs with severity indicators
- **Priority:** Medium
- **Dependencies:** Task 182
- **Estimated Time:** 1.5 hours
- **Definition of Done:** Bugs shown with severity colors, file links

### Task 193: Create Test Output Display
- **Description:** Component showing generated tests with syntax highlighting
- **Priority:** Medium
- **Dependencies:** Task 180
- **Estimated Time:** 1 hour
- **Definition of Done:** Tests displayed with copy functionality

### Task 194: Create AI Feature Unit Tests (Backend)
- **Description:** Test all AI endpoints with mocked LLM responses
- **Priority:** High
- **Dependencies:** Tasks 176-184
- **Estimated Time:** 3 hours
- **Definition of Done:** All AI features tested with mocked provider

### Task 195: Create Prompt Injection Tests
- **Description:** Test that injection attempts are blocked
- **Priority:** High
- **Dependencies:** Task 146
- **Estimated Time:** 2 hours
- **Definition of Done:** Common injection patterns handled

### Task 196: Create AI Response Caching
- **Description:** Cache AI responses for identical inputs (30 min TTL)
- **Priority:** Medium
- **Dependencies:** Tasks 176-184
- **Estimated Time:** 1.5 hours
- **Definition of Done:** Repeated requests use cache

### Task 197: Implement AI Feature Error Handling
- **Description:** Handle LLM timeouts, rate limits, invalid responses
- **Priority:** High
- **Dependencies:** Tasks 144-145
- **Estimated Time:** 2 hours
- **Definition of Done:** All error cases handled gracefully

### Task 198: Create HuggingFace Provider
- **Description:** Implement LLM interface for HuggingFace Inference API
- **Priority:** Low
- **Dependencies:** Task 143
- **Estimated Time:** 2 hours
- **Definition of Done:** HuggingFace provider functional

### Task 199: Create AI Settings Page
- **Description:** Settings UI for LLM provider, model, API key, temperature
- **Priority:** Medium
- **Dependencies:** Task 49
- **Estimated Time:** 2 hours
- **Definition of Done:** Settings saved and used for AI requests

### Task 200: Create AI Feature Frontend Tests
- **Description:** Test action buttons, modals, response displays
- **Priority:** Medium
- **Dependencies:** Tasks 188-193
- **Estimated Time:** 2 hours
- **Definition of Done:** AI UI components tested

---

## Milestone 8: GitHub Integration (Tasks 201-225)

### Task 201: Create GitHub Connection Model
- **Description:** Model for storing encrypted GitHub OAuth tokens
- **Priority:** Critical
- **Dependencies:** Task 26
- **Estimated Time:** 1 hour
- **Definition of Done:** Model with encrypted token storage

### Task 202: Create PullRequest Model
- **Description:** Model for storing PR review data
- **Priority:** High
- **Dependencies:** Task 56
- **Estimated Time:** 30 min
- **Definition of Done:** PR model with review fields

### Task 203: Implement GitHub OAuth Flow - Initiate
- **Description:** GET /auth/github redirects to GitHub authorization
- **Priority:** Critical
- **Dependencies:** Task 201
- **Estimated Time:** 2 hours
- **Definition of Done:** User redirected to GitHub with correct scopes

### Task 204: Implement GitHub OAuth Flow - Callback
- **Description:** POST /auth/github/callback exchanges code for token
- **Priority:** Critical
- **Dependencies:** Task 203
- **Estimated Time:** 2 hours
- **Definition of Done:** Token received, encrypted, stored

### Task 205: Create Token Encryption Service
- **Description:** Fernet encryption for GitHub access tokens at rest
- **Priority:** Critical
- **Dependencies:** Task 7
- **Estimated Time:** 1 hour
- **Definition of Done:** Tokens encrypted/decrypted correctly

### Task 206: Create GitHub API Client
- **Description:** Wrapper for GitHub API with auth, pagination, rate limiting
- **Priority:** Critical
- **Dependencies:** Task 205
- **Estimated Time:** 2 hours
- **Definition of Done:** API client handles auth, pagination, errors

### Task 207: Create List GitHub Repos Endpoint
- **Description:** GET /github/repos returns user's GitHub repositories
- **Priority:** High
- **Dependencies:** Task 206
- **Estimated Time:** 1.5 hours
- **Definition of Done:** Lists repos with name, language, size, private status

### Task 208: Create Repository Clone Service
- **Description:** Clone GitHub repos using authenticated git commands
- **Priority:** Critical
- **Dependencies:** Task 206
- **Estimated Time:** 3 hours
- **Definition of Done:** Public and private repos cloned successfully

### Task 209: Create GitHub Import Flow
- **Description:** Connect repo import endpoint to GitHub clone + index pipeline
- **Priority:** Critical
- **Dependencies:** Task 208, Task 95
- **Estimated Time:** 2 hours
- **Definition of Done:** GitHub URL → clone → index → ready

### Task 210: Create PR Diff Fetcher
- **Description:** Fetch PR diff from GitHub API for code review
- **Priority:** High
- **Dependencies:** Task 206
- **Estimated Time:** 2 hours
- **Definition of Done:** PR diffs fetched with file changes

### Task 211: Create GitHub Disconnect Endpoint
- **Description:** DELETE /github/disconnect removes token and connection
- **Priority:** Medium
- **Dependencies:** Task 201
- **Estimated Time:** 1 hour
- **Definition of Done:** Disconnect cleans up token, updates status

### Task 212: Create GitHub Webhook Handler
- **Description:** Handle push events for auto-reindex
- **Priority:** Medium
- **Dependencies:** Task 206
- **Estimated Time:** 2 hours
- **Definition of Done:** Push events trigger incremental reindex

### Task 213: Implement GitHub Rate Limit Handling
- **Description:** Respect GitHub API rate limits, queue requests if needed
- **Priority:** High
- **Dependencies:** Task 206
- **Estimated Time:** 1.5 hours
- **Definition of Done:** Rate limits respected, retries on limit

### Task 214: Create GitHub Unit Tests
- **Description:** Test OAuth flow, API client, clone service (mocked)
- **Priority:** High
- **Dependencies:** Tasks 203-209
- **Estimated Time:** 3 hours
- **Definition of Done:** All GitHub features tested with mocks

### Task 215: Create Frontend GitHub Connection UI
- **Description:** Settings page section for GitHub connect/disconnect
- **Priority:** High
- **Dependencies:** Task 49
- **Estimated Time:** 2 hours
- **Definition of Done:** Connect button, status display, disconnect

### Task 216: Create GitHub Repo Picker
- **Description:** Component listing GitHub repos for import selection
- **Priority:** High
- **Dependencies:** Task 207, Task 76
- **Estimated Time:** 3 hours
- **Definition of Done:** Repos listed, searchable, selectable for import

### Task 217: Create GitHub Import Progress
- **Description:** Show clone + index progress for GitHub imports
- **Priority:** Medium
- **Dependencies:** Task 78
- **Estimated Time:** 1 hour
- **Definition of Done:** Progress shown for clone and index phases

### Task 218: Handle GitHub Private Repo Permissions
- **Description:** Check repo access before import, clear error on failure
- **Priority:** High
- **Dependencies:** Task 208
- **Estimated Time:** 1 hour
- **Definition of Done:** Permission errors handled gracefully

### Task 219: Create Sparse Clone for Large Repos
- **Description:** Use sparse checkout for repos > 100MB
- **Priority:** Medium
- **Dependencies:** Task 208
- **Estimated Time:** 2 hours
- **Definition of Done:** Large repos clone only relevant files

### Task 220: Create GitHub Integration Tests
- **Description:** Test full flow: connect → list → import → index
- **Priority:** High
- **Dependencies:** Tasks 203-209
- **Estimated Time:** 2 hours
- **Definition of Done:** Integration flow tested

### Task 221: Create Frontend GitHub Tests
- **Description:** Test GitHub connection UI, repo picker
- **Priority:** Medium
- **Dependencies:** Tasks 215-216
- **Estimated Time:** 1.5 hours
- **Definition of Done:** GitHub UI components tested

### Task 222: Handle GitHub Token Expiry
- **Description:** Detect expired tokens, prompt re-authorization
- **Priority:** Medium
- **Dependencies:** Task 204
- **Estimated Time:** 1 hour
- **Definition of Done:** Expired tokens detected, user notified

### Task 223: Create Already Imported Indicator
- **Description:** Show which GitHub repos are already imported
- **Priority:** Low
- **Dependencies:** Task 216
- **Estimated Time:** 30 min
- **Definition of Done:** Already-imported repos marked in picker

### Task 224: Create Branch Selector for GitHub Import
- **Description:** Allow selecting specific branch to import
- **Priority:** Medium
- **Dependencies:** Task 216
- **Estimated Time:** 1 hour
- **Definition of Done:** Branch dropdown works for import

### Task 225: GitHub Connection Status API
- **Description:** Include github_connected in user profile response
- **Priority:** Low
- **Dependencies:** Task 34, Task 201
- **Estimated Time:** 30 min
- **Definition of Done:** Profile shows GitHub connection status

---

## Milestone 9-12: Frontend Pages (Tasks 226-290)

### Task 226: Create App Layout Component
- **Description:** Main layout with sidebar, navbar, and content area
- **Priority:** Critical
- **Dependencies:** Task 13, Task 14
- **Estimated Time:** 3 hours
- **Definition of Done:** Layout responsive, sidebar collapsible

### Task 227: Create Sidebar Navigation
- **Description:** Sidebar with nav links, icons, active state
- **Priority:** Critical
- **Dependencies:** Task 226
- **Estimated Time:** 2 hours
- **Definition of Done:** Navigation works, active item highlighted

### Task 228: Create Navbar Component
- **Description:** Top bar with logo, search, notifications, user menu
- **Priority:** High
- **Dependencies:** Task 226
- **Estimated Time:** 2 hours
- **Definition of Done:** Navbar functional with all elements

### Task 229: Create Theme Toggle
- **Description:** Dark/light mode toggle with persistence
- **Priority:** High
- **Dependencies:** Task 12
- **Estimated Time:** 1 hour
- **Definition of Done:** Theme toggles, persists in localStorage

### Task 230: Create Dashboard Page
- **Description:** Overview with stats cards, repo list, recent activity
- **Priority:** High
- **Dependencies:** Task 226, Task 71
- **Estimated Time:** 3 hours
- **Definition of Done:** Dashboard shows all sections with real data

### Task 231: Create Stats Card Component
- **Description:** Reusable stat card (number, label, icon, trend)
- **Priority:** Medium
- **Dependencies:** Task 13
- **Estimated Time:** 30 min
- **Definition of Done:** Cards display stats clearly

### Task 232: Create Recent Activity Component
- **Description:** List of recent chats, searches, imports
- **Priority:** Medium
- **Dependencies:** Task 164
- **Estimated Time:** 1.5 hours
- **Definition of Done:** Activity list shows recent items

### Task 233: Create Monaco Editor Integration
- **Description:** Set up Monaco Editor for code viewing
- **Priority:** High
- **Dependencies:** Task 11
- **Estimated Time:** 3 hours
- **Definition of Done:** Monaco renders code with syntax highlighting

### Task 234: Create Code Viewer Page
- **Description:** Full page code viewer with Monaco, line numbers, actions
- **Priority:** High
- **Dependencies:** Task 233, Task 65
- **Estimated Time:** 3 hours
- **Definition of Done:** Code displays, navigable, AI actions available

### Task 235: Create Breadcrumb Navigation
- **Description:** File path breadcrumbs for code viewer
- **Priority:** Medium
- **Dependencies:** Task 234
- **Estimated Time:** 1 hour
- **Definition of Done:** Breadcrumbs navigable for each path segment

### Task 236: Create Landing Page
- **Description:** Public landing page with hero, features, CTA
- **Priority:** High
- **Dependencies:** Task 13
- **Estimated Time:** 4 hours
- **Definition of Done:** Professional landing page, responsive

### Task 237: Create Landing Page - Hero Section
- **Description:** Hero with headline, subheading, CTA buttons, demo visual
- **Priority:** High
- **Dependencies:** Task 236
- **Estimated Time:** 2 hours
- **Definition of Done:** Eye-catching hero with clear value prop

### Task 238: Create Landing Page - Features Section
- **Description:** Feature grid with icons and descriptions
- **Priority:** Medium
- **Dependencies:** Task 236
- **Estimated Time:** 1.5 hours
- **Definition of Done:** Features displayed attractively

### Task 239: Create Landing Page - How It Works
- **Description:** 3-step process visualization
- **Priority:** Medium
- **Dependencies:** Task 236
- **Estimated Time:** 1 hour
- **Definition of Done:** Clear steps with visuals

### Task 240: Create Landing Page - Footer
- **Description:** Footer with links, social, copyright
- **Priority:** Low
- **Dependencies:** Task 236
- **Estimated Time:** 30 min
- **Definition of Done:** Footer rendered, links work

### Task 241: Create 404 Not Found Page
- **Description:** Friendly 404 page with navigation back
- **Priority:** Low
- **Dependencies:** Task 14
- **Estimated Time:** 30 min
- **Definition of Done:** 404 displayed for unknown routes

### Task 242: Create Loading Skeleton Components
- **Description:** Skeleton loaders for cards, lists, text blocks
- **Priority:** Medium
- **Dependencies:** Task 13
- **Estimated Time:** 1.5 hours
- **Definition of Done:** Skeletons used throughout app

### Task 243: Create Toast Notification System
- **Description:** Toast notifications for success/error/info messages
- **Priority:** High
- **Dependencies:** Task 13
- **Estimated Time:** 1 hour
- **Definition of Done:** Toasts appear and auto-dismiss

### Task 244: Create Error Boundary Component
- **Description:** React error boundary with fallback UI
- **Priority:** High
- **Dependencies:** Task 11
- **Estimated Time:** 1 hour
- **Definition of Done:** Errors caught, fallback displayed

### Task 245: Create Analytics Page
- **Description:** Repository analytics with charts and metrics
- **Priority:** Medium
- **Dependencies:** Task 13, Task 71
- **Estimated Time:** 3 hours
- **Definition of Done:** Charts render with real data

### Task 246: Create Language Pie Chart
- **Description:** Pie/donut chart for language breakdown
- **Priority:** Medium
- **Dependencies:** Task 245
- **Estimated Time:** 1.5 hours
- **Definition of Done:** Chart renders correctly, responsive

### Task 247: Create Complexity Bar Chart
- **Description:** Bar chart for code complexity distribution
- **Priority:** Low
- **Dependencies:** Task 245
- **Estimated Time:** 1 hour
- **Definition of Done:** Chart displays complexity data

### Task 248: Create Indexing History Table
- **Description:** Table showing indexing job history
- **Priority:** Medium
- **Dependencies:** Task 245
- **Estimated Time:** 1 hour
- **Definition of Done:** Table with date, status, duration, file count

### Task 249: Create Notification Bell Component
- **Description:** Bell icon with unread count, dropdown list
- **Priority:** Medium
- **Dependencies:** Task 228
- **Estimated Time:** 1.5 hours
- **Definition of Done:** Bell shows count, dropdown lists notifications

### Task 250: Create Keyboard Shortcuts
- **Description:** Cmd+K for search, Cmd+N for new chat, etc.
- **Priority:** Low
- **Dependencies:** Task 226
- **Estimated Time:** 1.5 hours
- **Definition of Done:** Shortcuts work, help modal available

### Tasks 251-290: Additional frontend polish tasks
(Tasks continue with similar granularity covering responsive design fixes, accessibility improvements, animation polish, dark mode refinements, mobile navigation, empty states, error states for each page, and comprehensive frontend testing)

---

## Milestone 13: Analytics (Tasks 291-310)

### Task 291: Create RepoMetrics Model
- **Description:** Model for calculated repository metrics
- **Priority:** Medium
- **Dependencies:** Task 56
- **Estimated Time:** 30 min
- **Definition of Done:** Model stores all calculated metrics

### Task 292: Create UsageLog Model
- **Description:** Model for tracking user actions
- **Priority:** Medium
- **Dependencies:** Task 26
- **Estimated Time:** 30 min
- **Definition of Done:** Actions logged with metadata

### Task 293: Create Metrics Calculation Service
- **Description:** Calculate complexity, coverage, counts per repository
- **Priority:** Medium
- **Dependencies:** Task 291
- **Estimated Time:** 2 hours
- **Definition of Done:** Metrics calculated accurately

### Task 294: Create Periodic Metrics Task
- **Description:** Celery Beat task to recalculate metrics daily
- **Priority:** Medium
- **Dependencies:** Task 293
- **Estimated Time:** 1 hour
- **Definition of Done:** Metrics auto-updated daily

### Task 295: Create Analytics Endpoint
- **Description:** GET /repositories/{id}/analytics with all metrics
- **Priority:** Medium
- **Dependencies:** Task 293
- **Estimated Time:** 1.5 hours
- **Definition of Done:** Returns comprehensive analytics data

### Task 296: Create Usage Tracking Middleware
- **Description:** Log user actions (search, chat, AI features) automatically
- **Priority:** Medium
- **Dependencies:** Task 292
- **Estimated Time:** 1.5 hours
- **Definition of Done:** Actions tracked without explicit logging calls

### Tasks 297-310: Analytics tests, frontend charts, and dashboard integration tasks

---

## Milestone 14: DevOps (Tasks 311-340)

### Task 311: Create Production Dockerfile
- **Description:** Optimized multi-stage Dockerfile for production
- **Priority:** High
- **Dependencies:** Task 18
- **Estimated Time:** 2 hours
- **Definition of Done:** Small image, non-root user, all deps included

### Task 312: Create Celery Worker Dockerfile
- **Description:** Separate Dockerfile for Celery workers
- **Priority:** High
- **Dependencies:** Task 311
- **Estimated Time:** 1 hour
- **Definition of Done:** Worker image builds and runs

### Task 313: Configure Railway Deployment
- **Description:** Set up Railway project with backend service
- **Priority:** High
- **Dependencies:** Task 311
- **Estimated Time:** 2 hours
- **Definition of Done:** Backend deploys to Railway on push

### Task 314: Configure Vercel Deployment
- **Description:** Set up Vercel project for frontend
- **Priority:** High
- **Dependencies:** Task 11
- **Estimated Time:** 1 hour
- **Definition of Done:** Frontend deploys to Vercel on push

### Task 315: Configure Neon PostgreSQL
- **Description:** Set up production database on Neon
- **Priority:** High
- **Dependencies:** None
- **Estimated Time:** 1 hour
- **Definition of Done:** Production DB accessible, pgvector enabled

### Task 316: Configure Upstash Redis
- **Description:** Set up production Redis on Upstash
- **Priority:** High
- **Dependencies:** None
- **Estimated Time:** 30 min
- **Definition of Done:** Production Redis accessible

### Tasks 317-340: CI/CD workflow refinement, health checks, Sentry, logging, environment management, deployment automation, rollback procedures

---

## Milestone 15-16: Testing & Polish (Tasks 341-380)

### Tasks 341-360: Comprehensive test writing (unit, integration, E2E, performance)
### Tasks 361-380: UI polish, accessibility, performance optimization, documentation finalization

---

## Task Summary

| Milestone | Tasks | Critical | High | Medium | Low |
|---|---|---|---|---|---|
| 1. Project Setup | 25 | 8 | 7 | 7 | 3 |
| 2. Authentication | 30 | 7 | 12 | 9 | 2 |
| 3. Repository Management | 30 | 5 | 13 | 9 | 3 |
| 4. Code Indexing | 30 | 5 | 10 | 12 | 3 |
| 5. Embeddings & Search | 25 | 7 | 8 | 8 | 2 |
| 6. AI Chat (RAG) | 35 | 8 | 14 | 10 | 3 |
| 7. AI Features | 25 | 0 | 14 | 9 | 2 |
| 8. GitHub Integration | 25 | 5 | 10 | 7 | 3 |
| 9-12. Frontend | 65 | 3 | 20 | 30 | 12 |
| 13. Analytics | 20 | 0 | 5 | 12 | 3 |
| 14. DevOps | 30 | 0 | 15 | 12 | 3 |
| 15-16. Testing & Polish | 40 | 0 | 10 | 20 | 10 |
| **TOTAL** | **380** | **48** | **138** | **145** | **49** |

**Total Estimated Development Time:** ~480 hours (12 weeks at 40hr/week)
