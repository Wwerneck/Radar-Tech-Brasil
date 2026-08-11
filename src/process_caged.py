"""Create the first processed Novo CAGED dataset."""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

from src.config import settings
from src.extract import list_caged_files
from src.inspect_caged import read_caged_sample
from src.logging_config import setup_logging
from src.transform import transform_caged_chunk


logger = setup_logging(__name__)


def process_caged_file(
    path: Path,
    output_path: Path,
    chunksize: int = 100_000,
    max_rows: int | None = None,
) -> Path:
    """Process a raw Novo CAGED file in chunks and write a CSV output."""
    _, sep, encoding = read_caged_sample(path, rows=1000)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    total_input_rows = 0
    total_output_rows = 0
    wrote_header = False

    logger.info("Starting processing for %s", path.name)
    reader = pd.read_csv(path, sep=sep, encoding=encoding, chunksize=chunksize, low_memory=False)

    for chunk_number, chunk in enumerate(reader, start=1):
        if max_rows is not None:
            remaining = max_rows - total_input_rows
            if remaining <= 0:
                break
            chunk = chunk.head(remaining)

        total_input_rows += len(chunk)
        transformed = transform_caged_chunk(chunk)
        total_output_rows += len(transformed)

        transformed.to_csv(
            output_path,
            mode="w" if not wrote_header else "a",
            header=not wrote_header,
            index=False,
            sep=";",
            encoding="utf-8",
        )
        wrote_header = True

        logger.info(
            "Processed chunk %s: input_rows=%s output_rows=%s",
            chunk_number,
            total_input_rows,
            total_output_rows,
        )

    logger.info("Saved processed file: %s", output_path)
    return output_path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Process a raw Novo CAGED file.")
    parser.add_argument(
        "--file",
        type=Path,
        help="Path to a CAGED .txt file. Defaults to first .txt in data/raw/caged.",
    )
    parser.add_argument("--chunksize", type=int, default=100_000)
    parser.add_argument(
        "--max-rows",
        type=int,
        help="Optional row limit for quick validation runs.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        help="Output CSV path. Defaults to data/processed/processed_<filename>.csv.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    path = args.file

    if path is None:
        txt_files = [file for file in list_caged_files() if file.suffix.lower() == ".txt"]
        if not txt_files:
            raise FileNotFoundError("No CAGED .txt files found in data/raw/caged/.")
        path = txt_files[0]

    output = args.output or (
        settings.processed_dir / f"processed_{path.stem.lower()}.csv"
    )
    process_caged_file(
        path.resolve(),
        output,
        chunksize=args.chunksize,
        max_rows=args.max_rows,
    )


if __name__ == "__main__":
    main()

