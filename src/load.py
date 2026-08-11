"""Load processed Radar Tech Brasil data into PostgreSQL."""

from __future__ import annotations

import argparse
import hashlib
from pathlib import Path

import pandas as pd
from sqlalchemy import Engine, text

from src.config import settings
from src.database import get_engine
from src.logging_config import setup_logging


logger = setup_logging(__name__)


def execute_sql_file(engine: Engine, path: Path) -> None:
    """Execute a SQL file containing DDL statements."""
    sql = path.read_text(encoding="utf-8")
    with engine.begin() as connection:
        for statement in sql.split(";"):
            statement = statement.strip()
            if statement:
                connection.execute(text(statement))
    logger.info("Executed SQL file: %s", path)


def load_dataframe_truncate_append(
    engine: Engine,
    df: pd.DataFrame,
    table_name: str,
    schema: str = "radar",
) -> None:
    """Truncate and reload a table while preserving SQL constraints."""
    with engine.begin() as connection:
        connection.execute(text(f"TRUNCATE TABLE {schema}.{table_name} RESTART IDENTITY CASCADE"))
    df.to_sql(table_name, engine, schema=schema, if_exists="append", index=False, method="multi", chunksize=5000)
    logger.info("Loaded %s rows into %s.%s", len(df), schema, table_name)


def load_dimension_ocupacao(engine: Engine, mapping_path: Path) -> None:
    """Load tech occupation mapping as dim_ocupacao."""
    mapping = pd.read_csv(mapping_path, sep=";", dtype={"codigo_cbo": "string", "familia_cbo": "string"})
    columns = [
        "codigo_cbo",
        "ocupacao",
        "familia_cbo",
        "familia_cbo_titulo",
        "categoria_tech",
        "criterio",
        "versao_mapeamento",
    ]
    load_dataframe_truncate_append(engine, mapping[columns], "dim_ocupacao")


def load_aggregates(engine: Engine, processed_dir: Path) -> None:
    """Load consolidated monthly aggregate CSVs."""
    aggregate_files = {
        "agg_tech_overview_mensal": "agg_tech_overview_mensal.csv",
        "agg_tech_by_category_mensal": "agg_tech_by_category_mensal.csv",
        "agg_tech_by_uf_mensal": "agg_tech_by_uf_mensal.csv",
        "agg_tech_by_occupation_mensal": "agg_tech_by_occupation_mensal.csv",
        "agg_tech_by_age_group_mensal": "agg_tech_by_age_group_mensal.csv",
        "agg_tech_by_education_mensal": "agg_tech_by_education_mensal.csv",
        "agg_tech_by_uf_mensal_enriched": "agg_tech_by_uf_mensal_enriched.csv",
        "agg_tech_by_education_mensal_enriched": "agg_tech_by_education_mensal_enriched.csv",
    }

    for table_name, filename in aggregate_files.items():
        path = processed_dir / filename
        if not path.exists():
            raise FileNotFoundError(f"Missing aggregate file: {path}")
        df = pd.read_csv(path, sep=";", dtype={"competencia": "string", "codigo_cbo": "string"})
        load_dataframe_truncate_append(engine, df, table_name)


def build_row_hash(frame: pd.DataFrame) -> pd.Series:
    """Build a deterministic row hash for fact idempotency."""
    hash_columns = [
        "competencia_mov",
        "codigo_cbo",
        "uf",
        "municipio",
        "saldo_movimentacao",
        "tipo_movimentacao",
        "categoria",
        "idade",
        "salario",
        "competencia_dec",
    ]

    values = frame[hash_columns].astype("string").fillna("").agg("|".join, axis=1)
    return values.map(lambda value: hashlib.sha256(value.encode("utf-8")).hexdigest())


def load_dimensions_for_fact(engine: Engine, tech_path: Path) -> None:
    """Load dimensions needed by the detailed fact table."""
    usecols = ["competencia_mov", "ano", "mes", "ano_mes", "uf", "municipio", "regiao"]
    chunks = pd.read_csv(tech_path, sep=";", usecols=usecols, chunksize=200_000)
    frames = []
    for chunk in chunks:
        frames.append(chunk)
    df = pd.concat(frames, ignore_index=True)

    dim_tempo = (
        df[["competencia_mov", "ano", "mes", "ano_mes"]]
        .drop_duplicates()
        .rename(columns={"competencia_mov": "tempo_id"})
    )
    dim_localidade = df[["uf", "municipio", "regiao"]].drop_duplicates()

    load_dataframe_truncate_append(engine, dim_tempo, "dim_tempo")
    load_dataframe_truncate_append(engine, dim_localidade, "dim_localidade")


def load_fact_movimentacao_tech(
    engine: Engine,
    tech_path: Path,
    chunksize: int = 100_000,
) -> None:
    """Load detailed tech movement fact from an enriched tech CSV."""
    load_dimensions_for_fact(engine, tech_path)

    with engine.begin() as connection:
        connection.execute(text("TRUNCATE TABLE radar.fato_movimentacao_tech RESTART IDENTITY"))

    ocupacao = pd.read_sql(
        "SELECT ocupacao_id, codigo_cbo FROM radar.dim_ocupacao",
        engine,
        dtype={"codigo_cbo": "string"},
    )
    localidade = pd.read_sql(
        "SELECT localidade_id, uf, municipio FROM radar.dim_localidade",
        engine,
    )

    fact_columns = [
        "row_hash",
        "tempo_id",
        "ocupacao_id",
        "localidade_id",
        "competencia_dec",
        "secao",
        "subclasse",
        "saldo_movimentacao",
        "tipo_saldo",
        "tipo_movimentacao",
        "categoria",
        "grau_instrucao",
        "idade",
        "faixa_etaria",
        "horas_contratuais",
        "raca_cor",
        "sexo",
        "tipo_empregador",
        "tipo_estabelecimento",
        "tipo_deficiencia",
        "ind_trab_intermitente",
        "ind_trab_parcial",
        "indicador_aprendiz",
        "origem_informacao",
        "indicador_fora_prazo",
        "unidade_salario_codigo",
        "salario",
        "valor_salario_fixo",
        "flag_idade_ausente",
        "flag_idade_invalida",
        "flag_salario_zero",
        "flag_salario_extremo",
        "flag_horas_invalidas",
        "flag_uf_invalida",
        "flag_cbo_invalida",
    ]

    total = 0
    for chunk in pd.read_csv(tech_path, sep=";", chunksize=chunksize, dtype={"codigo_cbo": "string"}):
        chunk["codigo_cbo"] = chunk["codigo_cbo"].astype("string").str.zfill(6)
        chunk["row_hash"] = build_row_hash(chunk)
        chunk["tempo_id"] = chunk["competencia_mov"]
        chunk = chunk.merge(ocupacao, on="codigo_cbo", how="left")
        chunk = chunk.merge(localidade, on=["uf", "municipio"], how="left")

        missing_keys = chunk["ocupacao_id"].isna().sum() + chunk["localidade_id"].isna().sum()
        if missing_keys:
            raise ValueError(f"Missing dimension keys while loading fact: {missing_keys}")

        chunk[fact_columns].to_sql(
            "fato_movimentacao_tech",
            engine,
            schema="radar",
            if_exists="append",
            index=False,
            method="multi",
            chunksize=5000,
        )
        total += len(chunk)
        logger.info("Loaded %s fact rows", total)


def load_initial_database(
    mapping_path: Path = settings.external_dir / "cbo_tech_mapping.csv",
    processed_dir: Path = settings.processed_dir,
) -> None:
    """Load the initial dashboard-ready model into PostgreSQL."""
    engine = get_engine()
    execute_sql_file(engine, settings.project_root / "sql" / "create_tables.sql")
    load_dimension_ocupacao(engine, mapping_path)
    load_aggregates(engine, processed_dir)
    execute_sql_file(engine, settings.project_root / "sql" / "views.sql")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Load Radar Tech Brasil data into PostgreSQL.")
    parser.add_argument("--mapping", type=Path, default=settings.external_dir / "cbo_tech_mapping.csv")
    parser.add_argument("--processed-dir", type=Path, default=settings.processed_dir)
    parser.add_argument(
        "--load-fact",
        action="store_true",
        help="Also load detailed fact rows from a tech CAGED CSV.",
    )
    parser.add_argument(
        "--fact-file",
        type=Path,
        default=settings.processed_dir / "tech_cagedmov202606.csv",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    load_initial_database(args.mapping, args.processed_dir)
    if args.load_fact:
        load_fact_movimentacao_tech(get_engine(), args.fact_file)


if __name__ == "__main__":
    main()
