"""Build a versioned CBO technology occupation mapping."""

from __future__ import annotations

import argparse
from collections import Counter
from dataclasses import dataclass
from pathlib import Path

import pandas as pd

from src.config import settings
from src.logging_config import setup_logging


logger = setup_logging(__name__)


@dataclass(frozen=True)
class TechOccupationRule:
    """One auditable CBO technology classification rule."""

    codigo_cbo: str
    categoria_tech: str
    criterio: str


TECH_OCCUPATION_RULES = [
    TechOccupationRule("123605", "Gestao de Tecnologia", "Diretoria de tecnologia da informacao."),
    TechOccupationRule("142135", "Seguranca da Informacao", "Protecao de dados pessoais e governanca de dados."),
    TechOccupationRule("142505", "Gestao de Tecnologia", "Gestao de infraestrutura de TI."),
    TechOccupationRule("142510", "Gestao de Tecnologia", "Gestao de desenvolvimento de sistemas."),
    TechOccupationRule("142515", "Gestao de Tecnologia", "Gestao de operacao de TI."),
    TechOccupationRule("142520", "Gestao de Tecnologia", "Gestao de projetos de TI."),
    TechOccupationRule("142525", "Seguranca da Informacao", "Gestao de seguranca da informacao."),
    TechOccupationRule("142530", "Gestao de Tecnologia", "Gestao de suporte tecnico de TI."),
    TechOccupationRule("142535", "Gestao de Tecnologia", "Gestao da tecnologia da informacao."),
    TechOccupationRule("203105", "Outras ocupacoes de Tecnologia", "Pesquisa em computacao e informatica."),
    TechOccupationRule("211220", "Dados e Banco de Dados", "Ciencia de dados."),
    TechOccupationRule("212205", "Desenvolvimento de Software", "Engenharia de aplicativos em computacao."),
    TechOccupationRule("212210", "Infraestrutura", "Engenharia de equipamentos em computacao."),
    TechOccupationRule("212215", "Infraestrutura", "Engenharia de sistemas operacionais."),
    TechOccupationRule("212305", "Dados e Banco de Dados", "Administracao de banco de dados."),
    TechOccupationRule("212310", "Redes", "Administracao de redes."),
    TechOccupationRule("212315", "Infraestrutura", "Administracao de sistemas operacionais."),
    TechOccupationRule("212320", "Seguranca da Informacao", "Administracao de seguranca da informacao."),
    TechOccupationRule("212405", "Desenvolvimento de Software", "Analise e desenvolvimento de sistemas."),
    TechOccupationRule("212410", "Redes", "Analise de redes e comunicacao de dados."),
    TechOccupationRule("212415", "Desenvolvimento de Software", "Analise de sistemas de automacao."),
    TechOccupationRule("212420", "Suporte Tecnico", "Analise de suporte computacional."),
    TechOccupationRule("212425", "Cloud e DevOps", "Arquitetura de solucoes de TI."),
    TechOccupationRule("212430", "Desenvolvimento de Software", "Testes de tecnologia da informacao."),
    TechOccupationRule("214350", "Redes", "Engenharia de redes de comunicacao."),
    TechOccupationRule("234120", "Outras ocupacoes de Tecnologia", "Docencia superior em computacao."),
    TechOccupationRule("313220", "Suporte Tecnico", "Manutencao de equipamentos de informatica."),
    TechOccupationRule("313305", "Redes", "Tecnico de comunicacao de dados."),
    TechOccupationRule("313310", "Redes", "Tecnico de rede em telecomunicacoes."),
    TechOccupationRule("317110", "Desenvolvimento de Software", "Desenvolvimento tecnico de sistemas de TI."),
    TechOccupationRule("317205", "Infraestrutura", "Operacao de computador."),
    TechOccupationRule("317210", "Suporte Tecnico", "Suporte ao usuario de TI."),
    TechOccupationRule("372205", "Redes", "Operacao de rede de teleprocessamento."),
    TechOccupationRule("731110", "Infraestrutura", "Montagem de computadores e equipamentos auxiliares."),
    TechOccupationRule("731320", "Redes", "Instalacao e reparo de linhas e aparelhos de telecomunicacoes."),
    TechOccupationRule("731325", "Redes", "Instalacao e reparo de redes e cabos telefonicos."),
    TechOccupationRule("731330", "Redes", "Reparo de aparelhos de telecomunicacoes."),
    TechOccupationRule("732105", "Redes", "Manutencao de linhas telefonicas e comunicacao de dados."),
    TechOccupationRule("732130", "Redes", "Instalacao e reparo de redes telefonicas e comunicacao de dados."),
]


def read_cbo_table(path: Path) -> pd.DataFrame:
    """Read an official CBO CSV preserving leading zeros."""
    return pd.read_csv(path, sep=";", encoding="latin1", dtype={"CODIGO": "string"})


def count_caged_cbo_occurrences(processed_caged_path: Path) -> Counter[str]:
    """Count CBO occurrences in a processed CAGED CSV."""
    counter: Counter[str] = Counter()
    for chunk in pd.read_csv(
        processed_caged_path,
        sep=";",
        usecols=["cbo_2002_ocupacao"],
        chunksize=300_000,
    ):
        counter.update(chunk["cbo_2002_ocupacao"].astype("string").str.zfill(6).tolist())
    return counter


def build_cbo_tech_mapping(
    cbo_occupation_path: Path,
    cbo_family_path: Path,
    processed_caged_path: Path | None = None,
) -> pd.DataFrame:
    """Build the first auditable CBO tech mapping."""
    occupations = read_cbo_table(cbo_occupation_path).rename(
        columns={"CODIGO": "codigo_cbo", "TITULO": "ocupacao"}
    )
    families = read_cbo_table(cbo_family_path).rename(
        columns={"CODIGO": "familia_cbo", "TITULO": "familia_cbo_titulo"}
    )
    rules = pd.DataFrame([rule.__dict__ for rule in TECH_OCCUPATION_RULES])

    mapping = rules.merge(occupations, on="codigo_cbo", how="left")
    mapping["familia_cbo"] = mapping["codigo_cbo"].str[:4]
    mapping = mapping.merge(families, on="familia_cbo", how="left")
    mapping["fonte"] = "CBO2002 oficial MTE"
    mapping["versao_mapeamento"] = "v0.2"
    mapping["incluido"] = True
    mapping["status_revisao"] = "revisado_conservador"

    if processed_caged_path is not None and processed_caged_path.exists():
        counts = count_caged_cbo_occurrences(processed_caged_path)
        mapping["registros_caged_202606"] = mapping["codigo_cbo"].map(counts).fillna(0).astype(int)

    missing = mapping[mapping["ocupacao"].isna()]
    if not missing.empty:
        raise ValueError(f"CBO codes not found in official occupation table: {missing['codigo_cbo'].tolist()}")

    return mapping[
        [
            "codigo_cbo",
            "ocupacao",
            "familia_cbo",
            "familia_cbo_titulo",
            "categoria_tech",
            "criterio",
            "fonte",
            "versao_mapeamento",
            "incluido",
            "status_revisao",
        ]
        + (["registros_caged_202606"] if "registros_caged_202606" in mapping.columns else [])
    ].sort_values(["categoria_tech", "codigo_cbo"])


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build CBO tech mapping CSV.")
    parser.add_argument(
        "--output",
        type=Path,
        default=settings.external_dir / "cbo_tech_mapping.csv",
    )
    parser.add_argument(
        "--processed-caged",
        type=Path,
        default=settings.processed_dir / "processed_cagedmov202606.csv",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    mapping = build_cbo_tech_mapping(
        settings.raw_cbo_dir / "cbo2002_ocupacao.csv",
        settings.raw_cbo_dir / "cbo2002_familia.csv",
        args.processed_caged,
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    mapping.to_csv(args.output, sep=";", index=False, encoding="utf-8")
    logger.info("Saved CBO tech mapping with %s occupations: %s", len(mapping), args.output)


if __name__ == "__main__":
    main()
