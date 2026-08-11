"""Centralized project configuration."""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv


PROJECT_ROOT = Path(__file__).resolve().parents[1]
load_dotenv(PROJECT_ROOT / ".env")


@dataclass(frozen=True)
class Settings:
    """Runtime settings loaded from environment variables."""

    project_root: Path = PROJECT_ROOT
    data_dir: Path = PROJECT_ROOT / "data"
    raw_caged_dir: Path = PROJECT_ROOT / "data" / "raw" / "caged"
    raw_cbo_dir: Path = PROJECT_ROOT / "data" / "raw" / "cbo"
    processed_dir: Path = PROJECT_ROOT / "data" / "processed"
    external_dir: Path = PROJECT_ROOT / "data" / "external"
    logs_dir: Path = PROJECT_ROOT / "logs"
    log_level: str = os.getenv("LOG_LEVEL", "INFO")
    caged_sample_rows: int = int(os.getenv("CAGED_SAMPLE_ROWS", "1000"))
    db_host: str = os.getenv("DB_HOST", "localhost")
    db_port: int = int(os.getenv("DB_PORT", "5432"))
    db_name: str = os.getenv("DB_NAME", "radar_tech")
    db_user: str = os.getenv("DB_USER", "postgres")
    db_password: str = os.getenv("DB_PASSWORD", "")

    @property
    def database_url(self) -> str:
        """Return a SQLAlchemy-compatible PostgreSQL URL."""
        return (
            f"postgresql+psycopg://{self.db_user}:{self.db_password}"
            f"@{self.db_host}:{self.db_port}/{self.db_name}"
        )


settings = Settings()

