from pathlib import Path

import pandas as pd

from src.enrich_aggregates import enrich_education_aggregate, enrich_uf_aggregate


def test_enrich_uf_aggregate_adds_labels(tmp_path: Path) -> None:
    processed = tmp_path / "processed"
    external = tmp_path / "external"
    processed.mkdir()
    external.mkdir()

    pd.DataFrame([{"competencia": 202606, "uf": 35, "registros": 10}]).to_csv(
        processed / "agg_tech_by_uf_mensal.csv", sep=";", index=False
    )
    pd.DataFrame(
        [{"uf": 35, "uf_sigla": "SP", "uf_nome": "Sao Paulo", "regiao_nome": "Sudeste"}]
    ).to_csv(external / "uf_mapping.csv", sep=";", index=False)

    output = enrich_uf_aggregate(processed, external)
    result = pd.read_csv(output, sep=";")

    assert result.loc[0, "uf_sigla"] == "SP"


def test_enrich_education_aggregate_adds_labels(tmp_path: Path) -> None:
    processed = tmp_path / "processed"
    external = tmp_path / "external"
    processed.mkdir()
    external.mkdir()

    pd.DataFrame([{"competencia": 202606, "grau_instrucao": 7, "registros": 10}]).to_csv(
        processed / "agg_tech_by_education_mensal.csv", sep=";", index=False
    )
    pd.DataFrame([{"grau_instrucao": 7, "escolaridade": "Superior completo"}]).to_csv(
        external / "education_mapping.csv", sep=";", index=False
    )

    output = enrich_education_aggregate(processed, external)
    result = pd.read_csv(output, sep=";")

    assert result.loc[0, "escolaridade"] == "Superior completo"

