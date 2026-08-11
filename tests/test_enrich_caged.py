import pandas as pd

from src.enrich_caged import enrich_caged_chunk, read_cbo_tech_mapping


def test_read_cbo_tech_mapping_normalizes_codes(tmp_path) -> None:
    path = tmp_path / "mapping.csv"
    pd.DataFrame(
        [
            {
                "codigo_cbo": "212405",
                "ocupacao": "Analista de desenvolvimento de sistemas",
                "familia_cbo": "2124",
                "familia_cbo_titulo": "Analistas de tecnologia da informação",
                "categoria_tech": "Desenvolvimento de Software",
                "criterio": "Analise e desenvolvimento de sistemas.",
                "versao_mapeamento": "v0.1",
            }
        ]
    ).to_csv(path, sep=";", index=False)

    result = read_cbo_tech_mapping(path)

    assert result.loc[0, "codigo_cbo"] == "212405"


def test_enrich_caged_chunk_filters_only_mapped_tech_occupations() -> None:
    chunk = pd.DataFrame(
        [
            {"cbo_2002_ocupacao": 212405, "salario": 5000},
            {"cbo_2002_ocupacao": 514320, "salario": 1800},
        ]
    )
    mapping = pd.DataFrame(
        [
            {
                "codigo_cbo": "212405",
                "ocupacao": "Analista de desenvolvimento de sistemas",
                "familia_cbo": "2124",
                "familia_cbo_titulo": "Analistas de tecnologia da informação",
                "categoria_tech": "Desenvolvimento de Software",
                "criterio": "Analise e desenvolvimento de sistemas.",
                "versao_mapeamento": "v0.1",
            }
        ]
    )

    result = enrich_caged_chunk(chunk, mapping)

    assert len(result) == 1
    assert result.loc[0, "codigo_cbo"] == "212405"
    assert result.loc[0, "categoria_tech"] == "Desenvolvimento de Software"

