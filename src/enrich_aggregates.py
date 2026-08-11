"""Enrich aggregate CSVs with local domain mapping tables."""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

from src.config import settings
from src.logging_config import setup_logging


logger = setup_logging(__name__)


def enrich_uf_aggregate(processed_dir: Path, external_dir: Path) -> Path:
    """Add UF acronym, UF name and region name to the monthly UF aggregate."""
    aggregate_path = processed_dir / "agg_tech_by_uf_mensal.csv"
    mapping_path = external_dir / "uf_mapping.csv"
    output_path = processed_dir / "agg_tech_by_uf_mensal_enriched.csv"

    aggregate = pd.read_csv(aggregate_path, sep=";")
    mapping = pd.read_csv(mapping_path, sep=";")
    enriched = aggregate.merge(mapping, on="uf", how="left")
    enriched.to_csv(output_path, sep=";", index=False, encoding="utf-8")
    logger.info("Saved enriched UF aggregate: %s", output_path)
    return output_path


def enrich_education_aggregate(processed_dir: Path, external_dir: Path) -> Path:
    """Add education labels to the monthly education aggregate."""
    aggregate_path = processed_dir / "agg_tech_by_education_mensal.csv"
    mapping_path = external_dir / "education_mapping.csv"
    output_path = processed_dir / "agg_tech_by_education_mensal_enriched.csv"

    aggregate = pd.read_csv(aggregate_path, sep=";")
    mapping = pd.read_csv(mapping_path, sep=";")
    enriched = aggregate.merge(mapping, on="grau_instrucao", how="left")
    enriched.to_csv(output_path, sep=";", index=False, encoding="utf-8")
    logger.info("Saved enriched education aggregate: %s", output_path)
    return output_path


def enrich_domain_aggregates(
    processed_dir: Path = settings.processed_dir,
    external_dir: Path = settings.external_dir,
) -> list[Path]:
    """Enrich all domain-dependent aggregate CSVs."""
    return [
        enrich_uf_aggregate(processed_dir, external_dir),
        enrich_education_aggregate(processed_dir, external_dir),
    ]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Enrich aggregate CSVs with domain labels.")
    parser.add_argument("--processed-dir", type=Path, default=settings.processed_dir)
    parser.add_argument("--external-dir", type=Path, default=settings.external_dir)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    enrich_domain_aggregates(args.processed_dir, args.external_dir)


if __name__ == "__main__":
    main()

