"""
Code chunking service for the indexing pipeline.

Splits source files into meaningful chunks for embedding.
Uses AST-based chunking for supported languages, with sliding window fallback.
"""

import ast
import re
from dataclasses import dataclass, field

from .constants import CHUNK_OVERLAP, CHUNK_WINDOW_SIZE, MAX_CHUNK_SIZE


@dataclass
class CodeChunkResult:
    """Represents a code chunk extracted from a file."""

    content: str
    chunk_type: str  # function, class, method, module, block
    symbol_name: str | None = None
    start_line: int = 1
    end_line: int = 1
    metadata: dict = field(default_factory=dict)


def chunk_file(content: str, language: str, file_path: str = "") -> list[CodeChunkResult]:
    """
    Split a source file into meaningful code chunks.

    Uses AST-based chunking for Python. Falls back to sliding window for other languages.

    Args:
        content: File content as string
        language: Detected language identifier
        file_path: Path of the file (for metadata)

    Returns:
        List of CodeChunkResult objects
    """
    if not content.strip():
        return []

    # Try AST-based chunking for supported languages
    if language == "python":
        chunks = _chunk_python_ast(content)
        if chunks:
            return chunks

    if language in ("javascript", "typescript"):
        chunks = _chunk_js_ts(content)
        if chunks:
            return chunks

    # Fallback: sliding window
    return _chunk_sliding_window(content)


def _chunk_python_ast(content: str) -> list[CodeChunkResult]:
    """
    Parse Python code using AST and extract functions/classes as chunks.
    """
    try:
        tree = ast.parse(content)
    except SyntaxError:
        return []  # Fall back to sliding window

    lines = content.split("\n")
    chunks = []

    for node in ast.iter_child_nodes(tree):
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef):
            start = node.lineno
            end = node.end_lineno or start
            chunk_content = "\n".join(lines[start - 1 : end])

            # Extract metadata
            metadata = {
                "parameters": [arg.arg for arg in node.args.args],
                "decorators": [
                    ast.dump(d) if not isinstance(d, ast.Name) else d.id
                    for d in node.decorator_list
                ],
            }

            # Extract docstring
            docstring = ast.get_docstring(node)
            if docstring:
                metadata["docstring"] = docstring[:200]  # Limit length

            chunks.append(
                CodeChunkResult(
                    content=chunk_content,
                    chunk_type="function",
                    symbol_name=node.name,
                    start_line=start,
                    end_line=end,
                    metadata=metadata,
                )
            )

        elif isinstance(node, ast.ClassDef):
            start = node.lineno
            end = node.end_lineno or start
            chunk_content = "\n".join(lines[start - 1 : end])

            # If class is too large, extract methods separately
            if end - start > MAX_CHUNK_SIZE:
                # Add class header
                class_header_end = start
                for child in ast.iter_child_nodes(node):
                    if isinstance(child, ast.FunctionDef | ast.AsyncFunctionDef):
                        class_header_end = child.lineno - 1
                        break

                header_content = "\n".join(lines[start - 1 : class_header_end])
                if header_content.strip():
                    chunks.append(
                        CodeChunkResult(
                            content=header_content,
                            chunk_type="class",
                            symbol_name=node.name,
                            start_line=start,
                            end_line=class_header_end,
                            metadata={"bases": [ast.dump(b) for b in node.bases]},
                        )
                    )

                # Extract methods
                for child in ast.iter_child_nodes(node):
                    if isinstance(child, ast.FunctionDef | ast.AsyncFunctionDef):
                        m_start = child.lineno
                        m_end = child.end_lineno or m_start
                        m_content = "\n".join(lines[m_start - 1 : m_end])
                        chunks.append(
                            CodeChunkResult(
                                content=m_content,
                                chunk_type="method",
                                symbol_name=f"{node.name}.{child.name}",
                                start_line=m_start,
                                end_line=m_end,
                                metadata={
                                    "class_name": node.name,
                                    "parameters": [arg.arg for arg in child.args.args],
                                },
                            )
                        )
            else:
                metadata = {"bases": [ast.dump(b) for b in node.bases]}
                docstring = ast.get_docstring(node)
                if docstring:
                    metadata["docstring"] = docstring[:200]

                chunks.append(
                    CodeChunkResult(
                        content=chunk_content,
                        chunk_type="class",
                        symbol_name=node.name,
                        start_line=start,
                        end_line=end,
                        metadata=metadata,
                    )
                )

    # If no top-level functions/classes found, fall back to sliding window
    if not chunks:
        return []

    return chunks


def _chunk_js_ts(content: str) -> list[CodeChunkResult]:
    """
    Extract functions and classes from JavaScript/TypeScript using regex patterns.
    Not as accurate as AST but handles most common patterns.
    """
    lines = content.split("\n")
    chunks = []

    # Patterns for function/class detection
    patterns = [
        # function declarations
        (r"^(?:export\s+)?(?:async\s+)?function\s+(\w+)", "function"),
        # arrow functions assigned to const/let/var
        (r"^(?:export\s+)?(?:const|let|var)\s+(\w+)\s*=\s*(?:async\s+)?\(", "function"),
        # class declarations
        (r"^(?:export\s+)?(?:abstract\s+)?class\s+(\w+)", "class"),
        # method definitions in objects/classes
        (r"^\s+(?:async\s+)?(\w+)\s*\([^)]*\)\s*{", "method"),
    ]

    current_chunk_start = None
    current_chunk_type = None
    current_symbol = None
    brace_depth = 0
    in_chunk = False

    for i, line in enumerate(lines):
        if not in_chunk:
            for pattern, chunk_type in patterns:
                match = re.match(pattern, line)
                if match:
                    current_chunk_start = i
                    current_chunk_type = chunk_type
                    current_symbol = match.group(1)
                    brace_depth = 0
                    in_chunk = True
                    break

        if in_chunk:
            brace_depth += line.count("{") - line.count("}")
            if brace_depth <= 0 and i > current_chunk_start:
                chunk_content = "\n".join(lines[current_chunk_start : i + 1])
                chunks.append(
                    CodeChunkResult(
                        content=chunk_content,
                        chunk_type=current_chunk_type,
                        symbol_name=current_symbol,
                        start_line=current_chunk_start + 1,
                        end_line=i + 1,
                        metadata={},
                    )
                )
                in_chunk = False

    return chunks


def _chunk_sliding_window(content: str) -> list[CodeChunkResult]:
    """
    Fallback chunking using sliding window with overlap.

    Splits content into fixed-size chunks with overlap to maintain context.
    """
    lines = content.split("\n")
    total_lines = len(lines)
    chunks = []

    if total_lines <= CHUNK_WINDOW_SIZE:
        # Small file: single chunk
        chunks.append(
            CodeChunkResult(
                content=content,
                chunk_type="block",
                symbol_name=None,
                start_line=1,
                end_line=total_lines,
                metadata={"method": "single_file"},
            )
        )
        return chunks

    step = CHUNK_WINDOW_SIZE - CHUNK_OVERLAP
    for i in range(0, total_lines, step):
        end = min(i + CHUNK_WINDOW_SIZE, total_lines)
        chunk_lines = lines[i:end]
        chunk_content = "\n".join(chunk_lines)

        if chunk_content.strip():  # Skip empty chunks
            chunks.append(
                CodeChunkResult(
                    content=chunk_content,
                    chunk_type="block",
                    symbol_name=None,
                    start_line=i + 1,
                    end_line=end,
                    metadata={"method": "sliding_window"},
                )
            )

        if end >= total_lines:
            break

    return chunks
