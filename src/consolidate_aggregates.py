"""Consolidate monthly aggregate CSVs into analysis-ready time series."""

from __future__ import annotations

import argparse
from pathlib import Path
import re

import pandas as pd

from src.config import settings
from src.logging_config import setup_logging


logger = setup_logging(__name__)


AGGREGATE_TYPES = [
    "overview",
    "by_category",
    "by_uf",
    "by_occupation",
    "by_age_group",
    "by_education",
]


def extract_competence(path: Path) -> str:
    """Extract competence suffix from aggregate file names."""
    return path.stem.rsplit("_", maxsplit=1)[-1]


def consolidate_aggregate_files(input_dir: Path, output_dir: Path) -> list[Path]:
    """Consolidate all monthly aggregate files by aggregate type."""
    output_dir.mkdir(parents=True, exist_ok=True)
    written: list[Path] = []

    for aggregate_type in AGGREGATE_TYPES:
        paths = [
            path
            for path in sorted(input_dir.glob(f"agg_tech_{aggregate_type}_*.csv"))
            if re.fullmatch(r"\d{6}", extract_competence(path))
        ]
        if not paths:
            logger.warning("No aggregate files found for type %s", aggregate_type)
            continue

        frames = []
        for path in paths:
            frame = pd.read_csv(path, sep=";")
            frame.insert(0, "competencia", extract_competence(path))
            frames.append(frame)

        consolidated = pd.concat(frames, ignore_index=True)
        output_path = output_dir / f"agg_tech_{aggregate_type}_mensal.csv"
        consolidated.to_csv(output_path, sep=";", index=False, encoding="utf-8")
        logger.info("Saved consolidated aggregate: %s", output_path)
        written.append(output_path)

    return written


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Consolidate monthly tech aggregates.")
    parser.add_argument("--input-dir", type=Path, default=settings.processed_dir)
    parser.add_argument("--output-dir", type=Path, default=settings.processed_dir)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    consolidate_aggregate_files(args.input_dir, args.output_dir)


if __name__ == "__main__":
    main()
