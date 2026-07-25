"""
Constants for the indexing pipeline.
"""

# Directories to skip during indexing
EXCLUDED_DIRECTORIES = {
    "node_modules",
    ".git",
    "__pycache__",
    ".venv",
    "venv",
    "env",
    ".env",
    "dist",
    "build",
    ".next",
    ".nuxt",
    "target",
    "bin",
    "obj",
    ".idea",
    ".vscode",
    ".vs",
    ".DS_Store",
    "coverage",
    ".pytest_cache",
    ".mypy_cache",
    ".tox",
    ".cache",
    "vendor",
    "bower_components",
    ".terraform",
    ".parcel-cache",
    ".turbo",
    "eggs",
    "*.egg-info",
    "htmlcov",
    ".nyc_output",
    "Debug",
    "Release",
}

# File extensions to skip
EXCLUDED_EXTENSIONS = {
    # Binary
    ".exe", ".dll", ".so", ".dylib", ".bin", ".dat", ".o", ".obj",
    # Media
    ".png", ".jpg", ".jpeg", ".gif", ".svg", ".ico", ".mp4", ".mp3",
    ".wav", ".webp", ".bmp", ".tiff",
    # Archives
    ".zip", ".tar", ".gz", ".rar", ".7z", ".bz2",
    # Compiled
    ".pyc", ".pyo", ".class", ".wasm",
    # Package locks (too large, not useful for search)
    ".lock",
    # Fonts
    ".woff", ".woff2", ".ttf", ".eot", ".otf",
    # Maps
    ".map",
    # Database
    ".sqlite", ".sqlite3", ".db",
}

# Specific files to skip
EXCLUDED_FILES = {
    "package-lock.json",
    "yarn.lock",
    "pnpm-lock.yaml",
    "poetry.lock",
    "Pipfile.lock",
    "composer.lock",
    "Gemfile.lock",
    "Cargo.lock",
    ".gitignore",
    ".gitattributes",
    ".editorconfig",
    "thumbs.db",
    ".ds_store",
}

# Max file size for indexing (1MB)
MAX_FILE_SIZE = 1_048_576

# Max total files per repository
MAX_FILES_PER_REPO = 50_000

# Chunking settings
CHUNK_WINDOW_SIZE = 50  # lines
CHUNK_OVERLAP = 10  # lines
MAX_CHUNK_SIZE = 500  # lines

# Language extension mapping
LANGUAGE_EXTENSIONS = {
    ".py": "python",
    ".js": "javascript",
    ".jsx": "javascript",
    ".ts": "typescript",
    ".tsx": "typescript",
    ".java": "java",
    ".go": "go",
    ".rs": "rust",
    ".c": "c",
    ".h": "c",
    ".cpp": "cpp",
    ".hpp": "cpp",
    ".cc": "cpp",
    ".rb": "ruby",
    ".php": "php",
    ".cs": "csharp",
    ".kt": "kotlin",
    ".kts": "kotlin",
    ".swift": "swift",
    ".scala": "scala",
    ".r": "r",
    ".R": "r",
    ".html": "html",
    ".htm": "html",
    ".css": "css",
    ".scss": "scss",
    ".sass": "sass",
    ".less": "less",
    ".sql": "sql",
    ".sh": "shell",
    ".bash": "shell",
    ".zsh": "shell",
    ".ps1": "powershell",
    ".yaml": "yaml",
    ".yml": "yaml",
    ".json": "json",
    ".xml": "xml",
    ".md": "markdown",
    ".rst": "restructuredtext",
    ".toml": "toml",
    ".ini": "ini",
    ".cfg": "ini",
    ".dockerfile": "dockerfile",
    ".tf": "terraform",
    ".lua": "lua",
    ".dart": "dart",
    ".ex": "elixir",
    ".exs": "elixir",
    ".erl": "erlang",
    ".hs": "haskell",
    ".vue": "vue",
    ".svelte": "svelte",
}
