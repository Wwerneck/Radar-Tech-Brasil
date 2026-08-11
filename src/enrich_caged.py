"""Enrich processed CAGED data with the versioned CBO tech mapping."""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

from src.config import settings
from src.logging_config import setup_logging


logger = setup_logging(__name__)

TECH_MAPPING_COLUMNS = [
    "codigo_cbo",
    "ocupacao",
    "familia_cbo",
    "familia_cbo_titulo",
    "categoria_tech",
    "criterio",
    "versao_mapeamento",
]


def read_cbo_tech_mapping(path: Path) -> pd.DataFrame:
    """Read the versioned CBO tech mapping."""
    mapping = pd.read_csv(path, sep=";", dtype={"codigo_cbo": "string"})
    missing = [column for column in TECH_MAPPING_COLUMNS if column not in mapping.columns]
    if missing:
        raise ValueError(f"Missing mapping columns: {missing}")

    mapping = mapping[TECH_MAPPING_COLUMNS].copy()
    mapping["codigo_cbo"] = mapping["codigo_cbo"].astype("string").str.zfill(6)
    return mapping


def enrich_caged_chunk(chunk: pd.DataFrame, mapping: pd.DataFrame) -> pd.DataFrame:
    """Return only CAGED records whose CBO is classified as technology."""
    result = chunk.copy()
    result["codigo_cbo"] = result["cbo_2002_ocupacao"].astype("string").str.zfill(6)
    enriched = result.merge(mapping, on="codigo_cbo", how="inner")
    return enriched


def enrich_caged_with_tech_mapping(
    processed_caged_path: Path,
    mapping_path: Path,
    output_path: Path,
    chunksize: int = 200_000,
) -> Path:
    """Create a tech-only enriched CAGED CSV in chunks."""
    mapping = read_cbo_tech_mapping(mapping_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    input_rows = 0
    output_rows = 0
    wrote_header = False

    logger.info("Starting CAGED tech enrichment for %s", processed_caged_path.name)
    for chunk_number, chunk in enumerate(
        pd.read_csv(processed_caged_path, sep=";", chunksize=chunksize),
        start=1,
    ):
        input_rows += len(chunk)
        enriched = enrich_caged_chunk(chunk, mapping)
        output_rows += len(enriched)

        enriched.to_csv(
            output_path,
            sep=";",
            index=False,
            encoding="utf-8",
            mode="w" if not wrote_header else "a",
            header=not wrote_header,
        )
        wrote_header = True

        logger.info(
            "Enriched chunk %s: input_rows=%s tech_rows=%s",
            chunk_number,
            input_rows,
            output_rows,
        )

    logger.info("Saved enriched tech dataset with %s rows: %s", output_rows, output_path)
    return output_path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Enrich processed CAGED with CBO tech mapping.")
    parser.add_argument(
        "--processed-caged",
        type=Path,
        default=settings.processed_dir / "processed_cagedmov202606.csv",
    )
    parser.add_argument(
        "--mapping",
        type=Path,
        default=settings.external_dir / "cbo_tech_mapping.csv",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=settings.processed_dir / "tech_cagedmov202606.csv",
    )
    parser.add_argument("--chunksize", type=int, default=200_000)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    enrich_caged_with_tech_mapping(
        args.processed_caged,
        args.mapping,
        args.output,
        chunksize=args.chunksize,
    )


if __name__ == "__main__":
    main()

