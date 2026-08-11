"""General utility functions."""

from __future__ import annotations

import hashlib
from pathlib import Path


def file_size_mb(path: Path) -> float:
    """Return file size in megabytes."""
    return path.stat().st_size / (1024 * 1024)


def calculate_file_hash(path: Path, chunk_size: int = 1024 * 1024) -> str:
    """Calculate a SHA-256 hash without loading the full file into memory."""
    digest = hashlib.sha256()
    with path.open("rb") as file:
        for chunk in iter(lambda: file.read(chunk_size), b""):
            digest.update(chunk)
    return digest.hexdigest()

