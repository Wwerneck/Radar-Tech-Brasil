"""Generate documented insights from consolidated aggregate files."""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

from src.config import settings
from src.logging_config import setup_logging


logger = setup_logging(__name__)


def _fmt_int(value: float) -> str:
    return f"{int(value):,}".replace(",", ".")


def _fmt_money(value: float) -> str:
    formatted = f"{float(value):,.2f}"
    return "R$ " + formatted.replace(",", "X").replace(".", ",").replace("X", ".")


def build_insights(processed_dir: Path = settings.processed_dir) -> str:
    """Build a markdown insight report from consolidated aggregates."""
    overview = pd.read_csv(
        processed_dir / "agg_tech_overview_mensal.csv",
        sep=";",
        dtype={"competencia": "string"},
    )
    category = pd.read_csv(
        processed_dir / "agg_tech_by_category_mensal.csv",
        sep=";",
        dtype={"competencia": "string"},
    )
    occupation = pd.read_csv(
        processed_dir / "agg_tech_by_occupation_mensal.csv",
        sep=";",
        dtype={"competencia": "string", "codigo_cbo": "string"},
    )
    uf = pd.read_csv(
        processed_dir / "agg_tech_by_uf_mensal.csv",
        sep=";",
        dtype={"competencia": "string"},
    )

    total_admissions = overview["total_admissoes"].sum()
    total_dismissals = overview["total_desligamentos"].sum()
    total_balance = overview["saldo_empregos"].sum()
    best_month = overview.sort_values("saldo_empregos", ascending=False).iloc[0]
    worst_month = overview.sort_values("saldo_empregos").iloc[0]

    category_total = (
        category.groupby("categoria_tech", as_index=False)
        .agg(
            registros=("registros", "sum"),
            admissoes=("admissoes", "sum"),
            desligamentos=("desligamentos", "sum"),
            saldo_empregos=("saldo_empregos", "sum"),
        )
        .sort_values("registros", ascending=False)
    )
    top_category = category_total.iloc[0]

    occupation_total = (
        occupation.groupby(["codigo_cbo", "ocupacao", "categoria_tech"], as_index=False)
        .agg(registros=("registros", "sum"), saldo_empregos=("saldo_empregos", "sum"))
        .sort_values("registros", ascending=False)
    )
    top_occupation = occupation_total.iloc[0]

    uf_total = (
        uf.groupby("uf", as_index=False)
        .agg(registros=("registros", "sum"), saldo_empregos=("saldo_empregos", "sum"))
        .sort_values("registros", ascending=False)
    )
    top_uf = uf_total.iloc[0]

    lines = [
        "# Insights Iniciais",
        "",
        "## Escopo",
        "",
        f"Período analisado: `{overview['competencia'].min()}` a `{overview['competencia'].max()}`.",
        "",
        "## Insight 1",
        "",
        "O mercado tech mapeado apresentou saldo positivo na janela analisada.",
        "",
        f"Evidência: foram {_fmt_int(total_admissions)} admissões e {_fmt_int(total_dismissals)} desligamentos, com saldo de {_fmt_int(total_balance)} vínculos.",
        "",
        "Possível explicação: as ocupações classificadas como tecnologia mantiveram volume de admissões superior ao de desligamentos na maior parte dos meses.",
        "",
        "Implicação: há sinal de expansão líquida no recorte analisado.",
        "",
        "Limitação: isso não prova causalidade e depende do mapeamento CBO tech `v0.1`.",
        "",
        "## Insight 2",
        "",
        "O saldo mensal não foi uniformemente positivo.",
        "",
        f"Evidência: o maior saldo ocorreu em `{best_month['competencia']}` com {_fmt_int(best_month['saldo_empregos'])}; o menor ocorreu em `{worst_month['competencia']}` com {_fmt_int(worst_month['saldo_empregos'])}.",
        "",
        "Possível explicação: movimentos sazonais e ciclos de contratação podem afetar competências específicas.",
        "",
        "Implicação: análises de tendência devem usar série mensal, não apenas totais acumulados.",
        "",
        "Limitação: a janela possui 12 competências e ainda não incorpora RAIS ou outras fontes.",
        "",
        "## Insight 3",
        "",
        f"A categoria com maior volume foi `{top_category['categoria_tech']}`.",
        "",
        f"Evidência: a categoria somou {_fmt_int(top_category['registros'])} registros e saldo de {_fmt_int(top_category['saldo_empregos'])}.",
        "",
        "Possível explicação: ocupações de maior capilaridade tendem a concentrar mais movimentações formais.",
        "",
        "Implicação: o dashboard deve permitir separar volume de saldo, pois uma categoria grande não necessariamente tem o maior saldo relativo.",
        "",
        "Limitação: categorias dependem da metodologia CBO tech versionada.",
        "",
        "## Insight 4",
        "",
        f"A ocupação com maior volume foi `{top_occupation['ocupacao']}`.",
        "",
        f"Evidência: CBO `{top_occupation['codigo_cbo']}` teve {_fmt_int(top_occupation['registros'])} registros no período.",
        "",
        "Possível explicação: cargos generalistas de análise e desenvolvimento aparecem com alta frequência nos registros formais.",
        "",
        "Implicação: rankings por ocupação são úteis para priorizar análises de salário, localidade e saldo.",
        "",
        "Limitação: CBO não captura stack, senioridade nem modalidade remota.",
        "",
        "## Insight 5",
        "",
        f"A UF com maior volume foi código `{int(top_uf['uf'])}`.",
        "",
        f"Evidência: a UF somou {_fmt_int(top_uf['registros'])} registros e saldo de {_fmt_int(top_uf['saldo_empregos'])}.",
        "",
        "Possível explicação: concentração econômica e populacional pode influenciar a distribuição dos vínculos formais.",
        "",
        "Implicação: a análise geográfica deve comparar volume, saldo e remuneração separadamente.",
        "",
        "Limitação: a tabela atual ainda usa códigos de UF; a próxima melhoria é enriquecer com siglas e regiões nominais.",
        "",
        "## Nota Sobre Remuneração",
        "",
        "Média e mediana salarial usam apenas salários maiores que zero e removem registros marcados com `flag_salario_extremo`.",
    ]
    return "\n".join(lines) + "\n"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate initial markdown insights.")
    parser.add_argument("--output", type=Path, default=settings.project_root / "docs" / "insights_iniciais.md")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    report = build_insights()
    args.output.write_text(report, encoding="utf-8")
    logger.info("Saved insight report: %s", args.output)


if __name__ == "__main__":
    main()
