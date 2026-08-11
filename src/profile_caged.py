"""Profile full Novo CAGED files using chunked reads."""

from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import pandas as pd

from src.config import settings
from src.extract import list_caged_files
from src.inspect_caged import read_caged_sample
from src.logging_config import setup_logging
from src.utils import calculate_file_hash, file_size_mb


logger = setup_logging(__name__)

NUMERIC_TEXT_COLUMNS = {"salário", "valorsaláriofixo", "horascontratuais"}
NUMERIC_RANGE_COLUMNS = {"idade", "salário", "valorsaláriofixo", "horascontratuais"}
CATEGORICAL_FREQUENCY_COLUMNS = {
    "competênciamov",
    "competênciadec",
    "indicadordeforadoprazo",
    "região",
    "uf",
    "seção",
    "saldomovimentação",
    "categoria",
    "graudeinstrução",
    "raçacor",
    "sexo",
    "tipoempregador",
    "tipoestabelecimento",
    "tipomovimentação",
    "tipodedeficiência",
    "indtrabintermitente",
    "indtrabparcial",
    "tamestabjan",
    "indicadoraprendiz",
    "origemdainformação",
    "unidadesaláriocódigo",
}


@dataclass
class ColumnProfile:
    """Accumulator for a single column profile."""

    nulls: int = 0
    distinct_values: set[Any] = field(default_factory=set)
    frequencies: Counter[Any] = field(default_factory=Counter)
    min_value: float | None = None
    max_value: float | None = None


def normalize_numeric_series(series: pd.Series) -> pd.Series:
    """Convert Brazilian decimal text to numeric values."""
    if series.name in NUMERIC_TEXT_COLUMNS:
        series = series.astype("string").str.replace(",", ".", regex=False)
    return pd.to_numeric(series, errors="coerce")


def update_min_max(profile: ColumnProfile, values: pd.Series) -> None:
    """Update numeric min and max values for a profile."""
    non_null = values.dropna()
    if non_null.empty:
        return

    current_min = float(non_null.min())
    current_max = float(non_null.max())
    profile.min_value = (
        current_min if profile.min_value is None else min(profile.min_value, current_min)
    )
    profile.max_value = (
        current_max if profile.max_value is None else max(profile.max_value, current_max)
    )


def profile_caged_file(path: Path, chunksize: int = 100_000) -> dict[str, Any]:
    """Profile a complete Novo CAGED file in chunks."""
    sample, sep, encoding = read_caged_sample(path, rows=1000)
    columns = list(sample.columns)
    profiles = defaultdict(ColumnProfile)
    dtypes = {column: str(dtype) for column, dtype in sample.dtypes.items()}
    total_rows = 0
    duplicated_rows = 0

    logger.info("Starting full profile for %s", path.name)
    reader = pd.read_csv(path, sep=sep, encoding=encoding, chunksize=chunksize, low_memory=False)

    for chunk_number, chunk in enumerate(reader, start=1):
        total_rows += len(chunk)
        duplicated_rows += int(chunk.duplicated().sum())

        for column in columns:
            series = chunk[column]
            profile = profiles[column]
            profile.nulls += int(series.isna().sum())
            profile.distinct_values.update(series.dropna().unique().tolist())

            if column in CATEGORICAL_FREQUENCY_COLUMNS:
                profile.frequencies.update(series.dropna().tolist())

            if column in NUMERIC_RANGE_COLUMNS:
                update_min_max(profile, normalize_numeric_series(series))

        if chunk_number % 5 == 0:
            logger.info("Processed %s chunks and %s rows", chunk_number, total_rows)

    logger.info("Finished profile for %s with %s rows", path.name, total_rows)

    return {
        "arquivo": path.name,
        "tamanho_mb": round(file_size_mb(path), 2),
        "hash_sha256": calculate_file_hash(path),
        "separador_detectado": sep,
        "encoding_detectado": encoding,
        "total_linhas": total_rows,
        "duplicadas_na_mesma_particao": duplicated_rows,
        "colunas": columns,
        "tipos_amostra": dtypes,
        "nulos": {column: profiles[column].nulls for column in columns},
        "cardinalidade": {
            column: len(profiles[column].distinct_values) for column in columns
        },
        "min_max": {
            column: {
                "min": profiles[column].min_value,
                "max": profiles[column].max_value,
            }
            for column in NUMERIC_RANGE_COLUMNS
            if column in profiles
        },
        "frequencias_top_20": {
            column: [
                {"valor": value, "quantidade": count}
                for value, count in profiles[column].frequencies.most_common(20)
            ]
            for column in CATEGORICAL_FREQUENCY_COLUMNS
            if column in profiles
        },
    }


def write_profile(profile: dict[str, Any], output_path: Path) -> Path:
    """Write profile as formatted JSON."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(profile, ensure_ascii=False, indent=2, default=str),
        encoding="utf-8",
    )
    logger.info("Saved profile: %s", output_path)
    return output_path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Profile a full Novo CAGED file.")
    parser.add_argument(
        "--file",
        type=Path,
        help="Path to a CAGED .txt file. Defaults to first .txt in data/raw/caged.",
    )
    parser.add_argument(
        "--chunksize",
        type=int,
        default=100_000,
        help="Rows per chunk.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        help="Output JSON path. Defaults to data/processed/profile_<filename>.json.",
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
        settings.processed_dir / f"profile_{path.stem.lower()}.json"
    )
    profile = profile_caged_file(path.resolve(), chunksize=args.chunksize)
    write_profile(profile, output)


if __name__ == "__main__":
    main()

