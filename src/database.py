"""Database connection helpers."""

from __future__ import annotations

from sqlalchemy import Engine, create_engine

from src.config import settings


def get_engine() -> Engine:
    """Create a SQLAlchemy engine from environment-based settings."""
    return create_engine(settings.database_url, pool_pre_ping=True)

