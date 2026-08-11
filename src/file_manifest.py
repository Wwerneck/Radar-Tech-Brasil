"""Manifest helpers for idempotent file-based processing."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def read_manifest(path: Path) -> dict[str, Any]:
    """Read a JSON manifest, returning an empty manifest when it does not exist."""
    if not path.exists():
        return {"files": {}}
    return json.loads(path.read_text(encoding="utf-8"))


def write_manifest(path: Path, manifest: dict[str, Any]) -> None:
    """Write a JSON manifest using UTF-8."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")


def update_file_status(
    manifest: dict[str, Any],
    key: str,
    status: str,
    metadata: dict[str, Any] | None = None,
) -> None:
    """Update one manifest entry."""
    manifest.setdefault("files", {})[key] = {
        "status": status,
        "updated_at": datetime.now(timezone.utc).isoformat(),
        "metadata": metadata or {},
    }


def is_complete(manifest: dict[str, Any], key: str) -> bool:
    """Return whether a manifest entry is marked complete."""
    return manifest.get("files", {}).get(key, {}).get("status") == "complete"

