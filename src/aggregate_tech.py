"""Create first analytical aggregates for the enriched tech CAGED dataset."""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

from src.config import settings
from src.logging_config import setup_logging


logger = setup_logging(__name__)


def _valid_salary_mask(df: pd.DataFrame) -> pd.Series:
    return df["salario"].notna() & df["salario"].gt(0) & ~df["flag_salario_extremo"]


def build_overview(df: pd.DataFrame) -> pd.DataFrame:
    """Build one-row KPI overview for tech records."""
    valid_salary = df.loc[_valid_salary_mask(df), "salario"]
    admissions = int((df["tipo_saldo"] == "admissao").sum())
    dismissals = int((df["tipo_saldo"] == "desligamento").sum())

    return pd.DataFrame(
        [
            {
                "total_registros_tech": len(df),
                "total_admissoes": admissions,
                "total_desligamentos": dismissals,
                "saldo_empregos": admissions - dismissals,
                "remuneracao_media": round(float(valid_salary.mean()), 2),
                "remuneracao_mediana": round(float(valid_salary.median()), 2),
                "ocupacoes_analisadas": int(df["codigo_cbo"].nunique()),
                "categorias_tech": int(df["categoria_tech"].nunique()),
            }
        ]
    )


def aggregate_by_category(df: pd.DataFrame) -> pd.DataFrame:
    """Aggregate tech movements by category."""
    salary_df = df.loc[_valid_salary_mask(df)]
    grouped = (
        df.groupby("categoria_tech")
        .agg(
            registros=("codigo_cbo", "size"),
            admissoes=("tipo_saldo", lambda value: int((value == "admissao").sum())),
            desligamentos=("tipo_saldo", lambda value: int((value == "desligamento").sum())),
            ocupacoes=("codigo_cbo", "nunique"),
        )
        .reset_index()
    )
    salary = (
        salary_df.groupby("categoria_tech")["salario"]
        .agg(remuneracao_media="mean", remuneracao_mediana="median")
        .reset_index()
    )
    grouped = grouped.merge(salary, on="categoria_tech", how="left")
    grouped["saldo_empregos"] = grouped["admissoes"] - grouped["desligamentos"]
    return grouped.sort_values("registros", ascending=False)


def aggregate_by_uf(df: pd.DataFrame) -> pd.DataFrame:
    """Aggregate tech movements by UF code."""
    salary_df = df.loc[_valid_salary_mask(df)]
    grouped = (
        df.groupby("uf")
        .agg(
            registros=("codigo_cbo", "size"),
            admissoes=("tipo_saldo", lambda value: int((value == "admissao").sum())),
            desligamentos=("tipo_saldo", lambda value: int((value == "desligamento").sum())),
        )
        .reset_index()
    )
    salary = (
        salary_df.groupby("uf")["salario"]
        .agg(remuneracao_media="mean", remuneracao_mediana="median")
        .reset_index()
    )
    grouped = grouped.merge(salary, on="uf", how="left")
    grouped["saldo_empregos"] = grouped["admissoes"] - grouped["desligamentos"]
    return grouped.sort_values("registros", ascending=False)


def aggregate_by_occupation(df: pd.DataFrame) -> pd.DataFrame:
    """Aggregate tech movements by CBO occupation."""
    salary_df = df.loc[_valid_salary_mask(df)]
    grouped = (
        df.groupby(["codigo_cbo", "ocupacao", "categoria_tech"])
        .agg(
            registros=("codigo_cbo", "size"),
            admissoes=("tipo_saldo", lambda value: int((value == "admissao").sum())),
            desligamentos=("tipo_saldo", lambda value: int((value == "desligamento").sum())),
        )
        .reset_index()
    )
    salary = (
        salary_df.groupby(["codigo_cbo", "ocupacao", "categoria_tech"])["salario"]
        .agg(remuneracao_media="mean", remuneracao_mediana="median")
        .reset_index()
    )
    grouped = grouped.merge(salary, on=["codigo_cbo", "ocupacao", "categoria_tech"], how="left")
    grouped["saldo_empregos"] = grouped["admissoes"] - grouped["desligamentos"]
    return grouped.sort_values("registros", ascending=False)


def aggregate_by_age_group(df: pd.DataFrame) -> pd.DataFrame:
    """Aggregate tech movements by age group."""
    grouped = (
        df.groupby("faixa_etaria")
        .agg(
            registros=("codigo_cbo", "size"),
            admissoes=("tipo_saldo", lambda value: int((value == "admissao").sum())),
            desligamentos=("tipo_saldo", lambda value: int((value == "desligamento").sum())),
        )
        .reset_index()
    )
    grouped["saldo_empregos"] = grouped["admissoes"] - grouped["desligamentos"]
    return grouped


def aggregate_by_education(df: pd.DataFrame) -> pd.DataFrame:
    """Aggregate tech movements by education code."""
    grouped = (
        df.groupby("grau_instrucao")
        .agg(
            registros=("codigo_cbo", "size"),
            admissoes=("tipo_saldo", lambda value: int((value == "admissao").sum())),
            desligamentos=("tipo_saldo", lambda value: int((value == "desligamento").sum())),
        )
        .reset_index()
    )
    grouped["saldo_empregos"] = grouped["admissoes"] - grouped["desligamentos"]
    return grouped.sort_values("grau_instrucao")


def write_aggregates(input_path: Path, output_dir: Path, competence: str = "202606") -> list[Path]:
    """Write first aggregate CSV files for analysis."""
    df = pd.read_csv(input_path, sep=";")
    output_dir.mkdir(parents=True, exist_ok=True)

    outputs = {
        f"agg_tech_overview_{competence}.csv": build_overview(df),
        f"agg_tech_by_category_{competence}.csv": aggregate_by_category(df),
        f"agg_tech_by_uf_{competence}.csv": aggregate_by_uf(df),
        f"agg_tech_by_occupation_{competence}.csv": aggregate_by_occupation(df),
        f"agg_tech_by_age_group_{competence}.csv": aggregate_by_age_group(df),
        f"agg_tech_by_education_{competence}.csv": aggregate_by_education(df),
    }

    written: list[Path] = []
    for filename, aggregate in outputs.items():
        path = output_dir / filename
        aggregate.to_csv(path, sep=";", index=False, encoding="utf-8")
        logger.info("Saved aggregate: %s", path)
        written.append(path)

    return written


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Create analytical aggregates for tech CAGED.")
    parser.add_argument(
        "--input",
        type=Path,
        default=settings.processed_dir / "tech_cagedmov202606.csv",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=settings.processed_dir,
    )
    parser.add_argument("--competence", default="202606")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    write_aggregates(args.input, args.output_dir, competence=args.competence)


if __name__ == "__main__":
    main()
