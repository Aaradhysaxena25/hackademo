"""
Tests for the indexing services (parser, chunker, file filter, language detector).
"""

import os
import tempfile

import pytest

from apps.indexing.services.chunker import CodeChunkResult, chunk_file
from apps.indexing.services.file_filter import FileFilter
from apps.indexing.services.language_detector import detect_language
from apps.indexing.services.parser import RepositoryParser


class TestLanguageDetector:
    """Tests for language detection."""

    def test_python_extension(self):
        assert detect_language("main.py") == "python"
        assert detect_language("src/utils.py") == "python"

    def test_javascript_extension(self):
        assert detect_language("app.js") == "javascript"
        assert detect_language("Component.jsx") == "javascript"

    def test_typescript_extension(self):
        assert detect_language("app.ts") == "typescript"
        assert detect_language("Component.tsx") == "typescript"

    def test_other_languages(self):
        assert detect_language("Main.java") == "java"
        assert detect_language("main.go") == "go"
        assert detect_language("lib.rs") == "rust"
        assert detect_language("style.css") == "css"
        assert detect_language("config.yaml") == "yaml"

    def test_special_files(self):
        assert detect_language("Dockerfile") == "dockerfile"
        assert detect_language("Makefile") == "makefile"

    def test_unknown_extension(self):
        assert detect_language("readme.xyz") == "other"


class TestFileFilter:
    """Tests for file filtering."""

    def setup_method(self):
        self.filter = FileFilter()

    def test_skip_node_modules(self):
        assert self.filter.should_skip_directory("node_modules") is True

    def test_skip_git_directory(self):
        assert self.filter.should_skip_directory(".git") is True

    def test_skip_pycache(self):
        assert self.filter.should_skip_directory("__pycache__") is True

    def test_allow_src_directory(self):
        assert self.filter.should_skip_directory("src") is False

    def test_skip_binary_extensions(self):
        assert self.filter.should_skip_file("image.png") is True
        assert self.filter.should_skip_file("app.exe") is True
        assert self.filter.should_skip_file("data.zip") is True

    def test_skip_lock_files(self):
        assert self.filter.should_skip_file("package-lock.json") is True
        assert self.filter.should_skip_file("yarn.lock") is True

    def test_skip_large_files(self):
        assert self.filter.should_skip_file("big.py", file_size=2_000_000) is True

    def test_allow_source_files(self):
        assert self.filter.should_skip_file("main.py", file_size=1000) is False
        assert self.filter.should_skip_file("app.ts", file_size=5000) is False

    def test_skip_minified(self):
        assert self.filter.should_skip_file("bundle.min.js") is True
        assert self.filter.should_skip_file("styles.min.css") is True

    def test_binary_detection_text_file(self):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
            f.write("def hello():\n    print('Hello, world!')\n")
            f.flush()
            assert self.filter.is_binary_file(f.name) is False
        os.unlink(f.name)

    def test_binary_detection_binary_file(self):
        with tempfile.NamedTemporaryFile(mode="wb", suffix=".bin", delete=False) as f:
            f.write(b"\x00\x01\x02\x03\x04\x05")
            f.flush()
            assert self.filter.is_binary_file(f.name) is True
        os.unlink(f.name)


class TestChunker:
    """Tests for code chunking."""

    def test_python_function_chunking(self):
        code = '''def hello():
    """Say hello."""
    print("Hello, world!")


def goodbye(name):
    """Say goodbye."""
    print(f"Goodbye, {name}!")
'''
        chunks = chunk_file(code, "python")
        assert len(chunks) == 2
        assert chunks[0].chunk_type == "function"
        assert chunks[0].symbol_name == "hello"
        assert chunks[1].symbol_name == "goodbye"

    def test_python_class_chunking(self):
        code = '''class Animal:
    """Base animal class."""

    def __init__(self, name):
        self.name = name

    def speak(self):
        pass
'''
        chunks = chunk_file(code, "python")
        assert len(chunks) >= 1
        assert any(c.chunk_type == "class" for c in chunks)

    def test_python_metadata_extraction(self):
        code = '''def greet(name: str, greeting: str = "Hello") -> str:
    """Greet someone."""
    return f"{greeting}, {name}!"
'''
        chunks = chunk_file(code, "python")
        assert len(chunks) == 1
        assert chunks[0].metadata.get("parameters") == ["name", "greeting"]
        assert "docstring" in chunks[0].metadata

    def test_sliding_window_fallback(self):
        # Generate a file too large for a single chunk
        lines = [f"line {i}" for i in range(100)]
        code = "\n".join(lines)
        chunks = chunk_file(code, "other")
        assert len(chunks) > 1
        assert all(c.chunk_type == "block" for c in chunks)

    def test_small_file_single_chunk(self):
        code = "line 1\nline 2\nline 3\n"
        chunks = chunk_file(code, "other")
        assert len(chunks) == 1

    def test_empty_file(self):
        chunks = chunk_file("", "python")
        assert chunks == []

    def test_javascript_function_chunking(self):
        code = '''function hello() {
    console.log("Hello");
}

const goodbye = (name) => {
    console.log(`Goodbye, ${name}`);
}
'''
        chunks = chunk_file(code, "javascript")
        assert len(chunks) >= 1

    def test_chunk_has_correct_lines(self):
        code = '''# comment

def first():
    pass

def second():
    return True
'''
        chunks = chunk_file(code, "python")
        assert chunks[0].start_line == 3
        assert chunks[1].start_line == 6


class TestRepositoryParser:
    """Tests for repository parsing."""

    def setup_method(self):
        self.parser = RepositoryParser()

    def test_parse_simple_repo(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create some source files
            os.makedirs(os.path.join(tmpdir, "src"))
            with open(os.path.join(tmpdir, "src", "main.py"), "w") as f:
                f.write("def main():\n    pass\n")
            with open(os.path.join(tmpdir, "README.md"), "w") as f:
                f.write("# My Project\n")

            manifest = self.parser.parse(tmpdir)
            assert len(manifest) == 2
            paths = {entry.path for entry in manifest}
            assert "src/main.py" in paths
            assert "README.md" in paths

    def test_excludes_node_modules(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            os.makedirs(os.path.join(tmpdir, "node_modules", "pkg"))
            with open(os.path.join(tmpdir, "node_modules", "pkg", "index.js"), "w") as f:
                f.write("module.exports = {}")
            with open(os.path.join(tmpdir, "app.js"), "w") as f:
                f.write("console.log('hi')")

            manifest = self.parser.parse(tmpdir)
            assert len(manifest) == 1
            assert manifest[0].name == "app.js"

    def test_excludes_binary_files(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            with open(os.path.join(tmpdir, "main.py"), "w") as f:
                f.write("print('hello')")
            with open(os.path.join(tmpdir, "data.bin"), "wb") as f:
                f.write(b"\x00\x01\x02\x03")

            manifest = self.parser.parse(tmpdir)
            assert len(manifest) == 1
            assert manifest[0].name == "main.py"

    def test_detects_language(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            with open(os.path.join(tmpdir, "app.ts"), "w") as f:
                f.write("const x: number = 1;")

            manifest = self.parser.parse(tmpdir)
            assert manifest[0].language == "typescript"

    def test_computes_hash_and_lines(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            with open(os.path.join(tmpdir, "test.py"), "w") as f:
                f.write("line1\nline2\nline3\n")

            manifest = self.parser.parse(tmpdir)
            assert manifest[0].line_count == 3
            assert len(manifest[0].content_hash) == 64  # SHA-256

    def test_empty_directory(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            manifest = self.parser.parse(tmpdir)
            assert manifest == []

    def test_invalid_path_raises(self):
        with pytest.raises(ValueError):
            self.parser.parse("/nonexistent/path")
