"""Check PostgreSQL connectivity for Radar Tech Brasil."""

from __future__ import annotations

from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from src.database import get_engine
from src.logging_config import setup_logging


logger = setup_logging(__name__)


def check_database_connection() -> bool:
    """Return True when PostgreSQL responds to a simple query."""
    try:
        engine = get_engine()
        with engine.connect() as connection:
            result = connection.execute(text("SELECT version()")).scalar_one()
    except SQLAlchemyError as exc:
        logger.error("Database connection failed: %s", exc)
        return False

    logger.info("Database connection OK: %s", result)
    return True


def main() -> None:
    if not check_database_connection():
        raise SystemExit(1)


if __name__ == "__main__":
    main()

