"""Inspect raw Novo CAGED files before defining transformation rules."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Iterable

import pandas as pd

from src.config import settings
from src.extract import list_caged_files
from src.logging_config import setup_logging
from src.utils import calculate_file_hash, file_size_mb


logger = setup_logging(__name__)


def _read_sample(path: Path, rows: int, sep: str, encoding: str) -> pd.DataFrame:
    return pd.read_csv(path, sep=sep, encoding=encoding, nrows=rows, low_memory=False)


def read_caged_sample(
    path: Path,
    rows: int = 1000,
    separators: Iterable[str] = (";", ",", "\t"),
    encodings: Iterable[str] = ("utf-8", "latin1", "cp1252"),
) -> tuple[pd.DataFrame, str, str]:
    """Read a sample using a small set of likely delimiters and encodings."""
    errors: list[str] = []

    for encoding in encodings:
        for sep in separators:
            try:
                df = _read_sample(path, rows, sep, encoding)
            except UnicodeDecodeError as exc:
                errors.append(f"encoding={encoding}, sep={sep!r}: {exc}")
                continue
            except pd.errors.ParserError as exc:
                errors.append(f"encoding={encoding}, sep={sep!r}: {exc}")
                continue

            if len(df.columns) > 1:
                return df, sep, encoding

    detail = " | ".join(errors[:5]) if errors else "no valid tabular structure found"
    raise ValueError(f"Could not read {path.name}. Details: {detail}")


def build_profile(path: Path, rows: int = 1000) -> dict[str, object]:
    """Build a compact data profile for a raw Novo CAGED file sample."""
    df, sep, encoding = read_caged_sample(path, rows=rows)

    return {
        "arquivo": path.name,
        "tamanho_mb": round(file_size_mb(path), 2),
        "hash_sha256": calculate_file_hash(path),
        "separador_detectado": sep,
        "encoding_detectado": encoding,
        "linhas_amostra": len(df),
        "colunas": list(df.columns),
        "tipos": {column: str(dtype) for column, dtype in df.dtypes.items()},
        "valores_nulos": df.isna().sum().to_dict(),
        "cardinalidade": df.nunique(dropna=True).to_dict(),
        "exemplos": df.head(5).to_dict(orient="records"),
    }


def print_profile(profile: dict[str, object]) -> None:
    """Print a readable profile to standard output."""
    for key, value in profile.items():
        print(f"\n## {key}")
        print(value)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Inspect a raw Novo CAGED file before creating transformations."
    )
    parser.add_argument(
        "--file",
        type=Path,
        help="Path to a specific CAGED .csv or .txt file. Defaults to first file in data/raw/caged.",
    )
    parser.add_argument(
        "--rows",
        type=int,
        default=settings.caged_sample_rows,
        help="Number of rows to sample.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    path = args.file

    if path is None:
        files = list_caged_files()
        if not files:
            raise FileNotFoundError(
                "No CAGED files found. Add a .csv or .txt file to data/raw/caged/."
            )
        path = files[0]

    path = path.resolve()
    logger.info("Inspecting file: %s", path)
    profile = build_profile(path, rows=args.rows)
    print_profile(profile)


if __name__ == "__main__":
    main()

