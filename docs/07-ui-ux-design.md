# CodePilot AI - UI/UX Design

## Design System

### Color Palette
```
Primary:       #6366F1 (Indigo 500)
Primary Dark:  #4F46E5 (Indigo 600)
Secondary:     #06B6D4 (Cyan 500)
Success:       #10B981 (Emerald 500)
Warning:       #F59E0B (Amber 500)
Error:         #EF4444 (Red 500)

Light Mode:
  Background:  #FFFFFF
  Surface:     #F9FAFB
  Border:      #E5E7EB
  Text:        #111827
  Muted:       #6B7280

Dark Mode:
  Background:  #0F172A
  Surface:     #1E293B
  Border:      #334155
  Text:        #F8FAFC
  Muted:       #94A3B8
```

### Typography
- Font Family: Inter (UI), JetBrains Mono (Code)
- Scale: 12px, 14px, 16px, 18px, 20px, 24px, 30px, 36px

### Spacing
- Base unit: 4px
- Scale: 4, 8, 12, 16, 20, 24, 32, 40, 48, 64, 80, 96

---

## Page Wireframes

### Landing Page
```
┌─────────────────────────────────────────────────────────────┐
│  🚀 CodePilot AI          Features  Pricing  Docs  [Login]  │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│         Chat with your codebase.                             │
│         Understand any repository in seconds.                │
│                                                              │
│         [Get Started Free]  [View Demo →]                    │
│                                                              │
│         ┌───────────────────────────────┐                    │
│         │   > How does auth work?       │                    │
│         │   ─────────────────────────── │                    │
│         │   The authentication system   │                    │
│         │   uses JWT tokens stored...   │                    │
│         │   📄 src/auth/middleware.py   │                    │
│         └───────────────────────────────┘                    │
│                                                              │
├─────────────────────────────────────────────────────────────┤
│  Features                                                    │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐    │
│  │ 💬 Chat  │  │ 🔍 Search│  │ 📄 Docs  │  │ 🐛 Bugs  │    │
│  │ Ask any  │  │ Semantic │  │ Auto-gen │  │ Detect   │    │
│  │ question │  │ code     │  │ docs for │  │ bugs &   │    │
│  │ about    │  │ search   │  │ your     │  │ issues   │    │
│  │ your code│  │ by       │  │ entire   │  │ before   │    │
│  │          │  │ meaning  │  │ codebase │  │ they hit │    │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘    │
├─────────────────────────────────────────────────────────────┤
│  How it works                                                │
│  1. Connect GitHub  →  2. Import Repo  →  3. Start Chatting │
├─────────────────────────────────────────────────────────────┤
│  Footer: © 2024 CodePilot AI | Privacy | Terms | GitHub     │
└─────────────────────────────────────────────────────────────┘
```

### Dashboard
```
┌─────────────────────────────────────────────────────────────┐
│  ☰  CodePilot AI          🔍 Search...      🔔  👤 John    │
├────────────┬────────────────────────────────────────────────┤
│            │                                                 │
│  Dashboard │  Welcome back, John                             │
│  ─────────│                                                 │
│  📦 Repos  │  Quick Stats                                    │
│  💬 Chat   │  ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐          │
│  🔍 Search │  │  5   │ │ 12K  │ │  28  │ │ 156  │          │
│  📊 Analytics│  │ Repos│ │Chunks│ │ Chats│ │Search│          │
│  ⚙️ Settings│  └──────┘ └──────┘ └──────┘ └──────┘          │
│            │                                                 │
│            │  Your Repositories                              │
│            │  ┌─────────────────────────────────────────┐   │
│            │  │ 📦 my-project         ● Ready            │   │
│            │  │    Python · 342 files · Indexed 2h ago   │   │
│            │  ├─────────────────────────────────────────┤   │
│            │  │ 📦 api-service         ● Ready            │   │
│            │  │    TypeScript · 128 files · Indexed 1d   │   │
│            │  ├─────────────────────────────────────────┤   │
│            │  │ 📦 frontend-app        ⟳ Indexing 65%     │   │
│            │  │    React · 256 files · ETA: 2 min        │   │
│            │  └─────────────────────────────────────────┘   │
│            │                                                 │
│            │  [+ Import Repository]                          │
│            │                                                 │
│            │  Recent Conversations                            │
│            │  • "How does auth work?" - my-project - 2h ago │
│            │  • "Find all API endpoints" - api-service - 1d │
│            │                                                 │
└────────────┴────────────────────────────────────────────────┘
```

### Repository Page
```
┌─────────────────────────────────────────────────────────────┐
│  ← Back   my-project                    [⟳ Reindex] [🗑️]   │
├────────────┬────────────────────────────────────────────────┤
│            │                                                 │
│  Overview  │  Repository: my-project                         │
│  Files     │  Source: GitHub · main branch                   │
│  Chat      │  Status: ● Ready                                │
│  Search    │                                                 │
│  Docs      │  Stats                                          │
│  Analytics │  ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐          │
│  Bugs      │  │ 342  │ │1,205 │ │28.5K │ │ 98%  │          │
│  Tests     │  │Files │ │Chunks│ │Lines │ │Cover │          │
│            │  └──────┘ └──────┘ └──────┘ └──────┘          │
│            │                                                 │
│            │  Languages                                      │
│            │  ████████████████░░░░░ Python 65%               │
│            │  ██████░░░░░░░░░░░░░░ JavaScript 25%            │
│            │  ██░░░░░░░░░░░░░░░░░░ HTML 10%                  │
│            │                                                 │
│            │  Recent Activity                                │
│            │  • Indexed 2 hours ago (45 seconds)             │
│            │  • 3 conversations today                        │
│            │  • 12 searches this week                        │
│            │                                                 │
└────────────┴────────────────────────────────────────────────┘
```

### Repository Import
```
┌─────────────────────────────────────────────────────────────┐
│  Import Repository                                           │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌───────────────────┐  ┌───────────────────┐               │
│  │  🐙 From GitHub   │  │  📁 Upload Files  │               │
│  │  (Selected)       │  │                   │               │
│  └───────────────────┘  └───────────────────┘               │
│                                                              │
│  ─────────────────────────────────────────────               │
│                                                              │
│  🔍 Search repositories...                                   │
│                                                              │
│  Your GitHub Repositories:                                   │
│  ┌─────────────────────────────────────────────────────┐    │
│  │ ☐ user/my-project        Python    ⭐ 42   2.1MB    │    │
│  │ ☐ user/api-service       TypeScript ⭐ 15  800KB    │    │
│  │ ☐ user/frontend-app      React      ⭐ 8   1.5MB    │    │
│  │ ☑ user/cli-tool          Go         ⭐ 3   500KB    │    │
│  │ ─ user/legacy-app        (Already imported)          │    │
│  └─────────────────────────────────────────────────────┘    │
│                                                              │
│  Branch: [main ▼]                                            │
│                                                              │
│  [Cancel]                            [Import Selected (1)]   │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### AI Chat
```
┌─────────────────────────────────────────────────────────────┐
│  💬 Chat · my-project                          [New Chat]    │
├────────────┬────────────────────────────────────────────────┤
│            │                                                 │
│ Conversations│                                               │
│ ──────────  │  ┌─ User ──────────────────────────────────┐  │
│ • How does  │  │ How does the authentication middleware   │  │
│   auth work?│  │ work in this project?                    │  │
│ • Find API  │  └─────────────────────────────────────────┘  │
│   endpoints │                                                │
│ • Explain   │  ┌─ CodePilot ─────────────────────────────┐  │
│   database  │  │ The authentication middleware in this     │  │
│   schema    │  │ project uses JWT tokens. Here's how it    │  │
│            │  │ works:                                     │  │
│            │  │                                            │  │
│            │  │ ```python                                  │  │
│            │  │ # src/middleware/auth.py (lines 15-45)     │  │
│            │  │ class JWTAuthMiddleware:                   │  │
│            │  │     def __call__(self, request):           │  │
│            │  │         token = self.get_token(request)    │  │
│            │  │         ...                                │  │
│            │  │ ```                                        │  │
│            │  │                                            │  │
│            │  │ 📎 Sources:                                │  │
│            │  │ • src/middleware/auth.py:15-45 (92%)       │  │
│            │  │ • src/utils/jwt.py:8-30 (87%)             │  │
│            │  └────────────────────────────────────────────┘  │
│            │                                                 │
│            │  ┌─────────────────────────────────────────┐   │
│            │  │ Ask about this repository...          [→]│   │
│            │  └─────────────────────────────────────────┘   │
│            │                                                 │
└────────────┴────────────────────────────────────────────────┘
```

### Repository Analytics
```
┌─────────────────────────────────────────────────────────────┐
│  📊 Analytics · my-project                                   │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Overview                                                    │
│  ┌────────────┐ ┌────────────┐ ┌────────────┐ ┌──────────┐ │
│  │   342      │ │   450      │ │    85      │ │   3.2    │ │
│  │   Files    │ │  Functions │ │   Classes  │ │  Avg CC  │ │
│  └────────────┘ └────────────┘ └────────────┘ └──────────┘ │
│                                                              │
│  Language Distribution          Code Complexity              │
│  ┌──────────────────────┐      ┌──────────────────────┐    │
│  │    [Pie Chart]        │      │    [Bar Chart]        │    │
│  │    Python: 65%        │      │    Low: 280           │    │
│  │    JS: 25%            │      │    Medium: 140        │    │
│  │    HTML: 10%          │      │    High: 30           │    │
│  └──────────────────────┘      └──────────────────────┘    │
│                                                              │
│  Indexing History                                            │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  Date        | Type    | Status  | Duration | Files   │   │
│  │  Jan 15      | Full    | ✓       | 45s      | 342     │   │
│  │  Jan 10      | Full    | ✓       | 42s      | 338     │   │
│  │  Jan 5       | Incr.   | ✓       | 8s       | 12      │   │
│  └──────────────────────────────────────────────────────┘   │
│                                                              │
│  Chat Usage (Last 30 days)                                   │
│  ┌──────────────────────────────────────────────────────┐   │
│  │    [Line Chart - Messages per day]                    │   │
│  └──────────────────────────────────────────────────────┘   │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### Settings Page
```
┌─────────────────────────────────────────────────────────────┐
│  ⚙️ Settings                                                 │
├────────────┬────────────────────────────────────────────────┤
│            │                                                 │
│  Profile   │  Profile Settings                               │
│  Account   │  ─────────────────                              │
│  AI Config │  First Name: [John          ]                   │
│  GitHub    │  Last Name:  [Doe           ]                   │
│  API Keys  │  Email:      [john@example.com] (verified ✓)   │
│  Billing   │  Bio:        [Full-stack developer...]          │
│            │  Company:    [Acme Inc       ]                   │
│            │  Avatar:     [Upload] current: 👤               │
│            │                                                 │
│            │  [Save Changes]                                 │
│            │                                                 │
│            │  ─────────────────                              │
│            │  AI Configuration                               │
│            │  LLM Provider: [OpenAI ▼]                       │
│            │  Model:        [gpt-4o-mini ▼]                  │
│            │  API Key:      [sk-•••••••••••]                 │
│            │  Temperature:  [0.1 ───●──── 1.0]              │
│            │                                                 │
│            │  ─────────────────                              │
│            │  GitHub Connection                              │
│            │  Status: ✓ Connected as @octocat               │
│            │  [Disconnect GitHub]                             │
│            │                                                 │
└────────────┴────────────────────────────────────────────────┘
```

### Authentication (Login/Register)
```
┌─────────────────────────────────────────────────────────────┐
│                                                              │
│              🚀 CodePilot AI                                  │
│                                                              │
│         ┌─────────────────────────────┐                      │
│         │                             │                      │
│         │  Welcome back               │                      │
│         │  Sign in to your account    │                      │
│         │                             │                      │
│         │  Email                      │                      │
│         │  ┌───────────────────────┐  │                      │
│         │  │ john@example.com      │  │                      │
│         │  └───────────────────────┘  │                      │
│         │                             │                      │
│         │  Password                   │                      │
│         │  ┌───────────────────────┐  │                      │
│         │  │ ••••••••••            │  │                      │
│         │  └───────────────────────┘  │                      │
│         │  [Forgot password?]         │                      │
│         │                             │                      │
│         │  [      Sign In       ]     │                      │
│         │                             │                      │
│         │  ───── or continue with ─── │                      │
│         │                             │                      │
│         │  [🐙 Sign in with GitHub]   │                      │
│         │                             │                      │
│         │  Don't have an account?     │                      │
│         │  [Create one →]             │                      │
│         │                             │                      │
│         └─────────────────────────────┘                      │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### Code Viewer
```
┌─────────────────────────────────────────────────────────────┐
│  📄 src/middleware/auth.py · my-project                      │
├─────────────────────────────────────────────────────────────┤
│  src / middleware / auth.py                                   │
│  ┌───────────────────────────────────────────────────────┐  │
│  │  1  │ import jwt                                       │  │
│  │  2  │ from django.conf import settings                 │  │
│  │  3  │ from django.http import JsonResponse             │  │
│  │  4  │                                                  │  │
│  │  5  │ class JWTAuthMiddleware:                         │  │
│  │  6  │     """JWT authentication middleware."""          │  │
│  │  7  │                                                  │  │
│  │  8  │     def __init__(self, get_response):            │  │
│  │  9  │         self.get_response = get_response         │  │
│  │ 10  │                                                  │  │
│  │ 11  │     def __call__(self, request):                 │  │
│  │ 12  │         token = self.get_token(request)          │  │
│  │ 13  │         if token:                                │  │
│  │ 14  │             try:                                 │  │
│  │ 15  │                 payload = jwt.decode(            │  │
│  │     │                          ...                     │  │
│  └───────────────────────────────────────────────────────┘  │
│                                                              │
│  Actions:                                                    │
│  [💬 Ask AI] [📄 Generate Docs] [🧪 Generate Tests] [🐛 Bugs]│
│                                                              │
│  Chunks in this file:                                        │
│  • JWTAuthMiddleware (class, lines 5-45)                    │
│  • __call__ (method, lines 11-35)                           │
│  • get_token (method, lines 37-45)                          │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## Component Hierarchy

```
App
├── Layout
│   ├── Navbar
│   │   ├── Logo
│   │   ├── SearchBar
│   │   ├── NotificationBell
│   │   └── UserMenu
│   ├── Sidebar
│   │   ├── NavItem
│   │   └── RepoSelector
│   └── MainContent
│       └── <Outlet /> (React Router)
│
├── Pages
│   ├── LandingPage
│   │   ├── Hero
│   │   ├── Features
│   │   ├── HowItWorks
│   │   └── Footer
│   ├── AuthPage
│   │   ├── LoginForm
│   │   └── RegisterForm
│   ├── DashboardPage
│   │   ├── StatsCards
│   │   ├── RepoList
│   │   └── RecentActivity
│   ├── RepositoryPage
│   │   ├── RepoHeader
│   │   ├── RepoStats
│   │   ├── FileBrowser
│   │   └── RepoTabs
│   ├── ChatPage
│   │   ├── ConversationList
│   │   ├── MessageList
│   │   ├── MessageBubble
│   │   ├── CodeBlock
│   │   ├── SourceReference
│   │   └── ChatInput
│   ├── SearchPage
│   │   ├── SearchInput
│   │   ├── SearchFilters
│   │   └── SearchResults
│   ├── AnalyticsPage
│   │   ├── MetricsCards
│   │   ├── Charts
│   │   └── IndexingHistory
│   ├── CodeViewerPage
│   │   ├── MonacoEditor
│   │   ├── ChunkOverlay
│   │   └── AIActions
│   └── SettingsPage
│       ├── ProfileForm
│       ├── AIConfigForm
│       ├── GitHubConnection
│       └── APIKeyManager
│
├── Shared Components
│   ├── Button
│   ├── Input
│   ├── Card
│   ├── Modal
│   ├── Toast
│   ├── Skeleton
│   ├── Badge
│   ├── Avatar
│   ├── ProgressBar
│   ├── Tooltip
│   ├── Dropdown
│   ├── Tabs
│   ├── DataTable
│   └── EmptyState
│
└── Providers
    ├── AuthProvider
    ├── ThemeProvider
    ├── QueryClientProvider
    └── ToastProvider
```

## Routing Structure

```typescript
const routes = [
  // Public routes
  { path: "/", element: <LandingPage /> },
  { path: "/login", element: <LoginPage /> },
  { path: "/register", element: <RegisterPage /> },

  // Protected routes (require auth)
  {
    path: "/app",
    element: <AppLayout />,
    children: [
      { path: "dashboard", element: <DashboardPage /> },
      { path: "repositories", element: <RepositoryListPage /> },
      { path: "repositories/import", element: <ImportPage /> },
      { path: "repositories/:id", element: <RepositoryPage /> },
      { path: "repositories/:id/files", element: <FileBrowserPage /> },
      { path: "repositories/:id/files/:fileId", element: <CodeViewerPage /> },
      { path: "repositories/:id/chat", element: <ChatPage /> },
      { path: "repositories/:id/analytics", element: <AnalyticsPage /> },
      { path: "chat", element: <ChatPage /> },
      { path: "chat/:conversationId", element: <ChatPage /> },
      { path: "search", element: <SearchPage /> },
      { path: "settings", element: <SettingsPage /> },
      { path: "settings/:tab", element: <SettingsPage /> },
    ],
  },

  // Catch-all
  { path: "*", element: <NotFoundPage /> },
];
```

## State Management Strategy

| State Type | Solution | Examples |
|---|---|---|
| Server State | React Query | Repositories, conversations, messages, user data |
| Auth State | React Context | Current user, tokens, login status |
| UI State | Zustand | Sidebar open/closed, theme, active filters |
| Form State | React Hook Form | Login, register, settings forms |
| URL State | React Router | Current page, query params, filters |

## Dark Mode

- Implemented via Tailwind `dark:` variants
- System preference detection on first visit
- User preference stored in localStorage + profile settings
- Smooth transitions between modes
- All colors defined as CSS variables for easy theming

## Responsive Layout

| Breakpoint | Layout |
|---|---|
| Mobile (<640px) | Sidebar hidden, bottom nav, stacked layout |
| Tablet (640-1024px) | Collapsed sidebar (icons only), 2-column |
| Desktop (>1024px) | Full sidebar, 3-column where applicable |

### Mobile Adaptations
- Chat: Full-screen conversation view
- Code viewer: Horizontal scroll for code, actions in bottom sheet
- File browser: Full-width tree view
- Dashboard: Stacked cards, horizontal scroll for stats
