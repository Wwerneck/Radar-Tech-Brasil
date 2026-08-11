"""Data extraction helpers for raw public datasets."""

from __future__ import annotations

from pathlib import Path

from src.config import settings


SUPPORTED_CAGED_EXTENSIONS = {".csv", ".txt"}


def list_caged_files(raw_dir: Path | None = None) -> list[Path]:
    """Return available raw Novo CAGED files sorted by name."""
    directory = raw_dir or settings.raw_caged_dir
    if not directory.exists():
        return []
    return sorted(
        path
        for path in directory.iterdir()
        if path.is_file() and path.suffix.lower() in SUPPORTED_CAGED_EXTENSIONS
    )

