import pandas as pd

from src.aggregate_tech import build_overview


def test_build_overview_uses_valid_salary_for_compensation_metrics() -> None:
    df = pd.DataFrame(
        [
            {
                "tipo_saldo": "admissao",
                "salario": 5000,
                "flag_salario_extremo": False,
                "codigo_cbo": "212405",
                "categoria_tech": "Desenvolvimento de Software",
            },
            {
                "tipo_saldo": "desligamento",
                "salario": 0,
                "flag_salario_extremo": False,
                "codigo_cbo": "317210",
                "categoria_tech": "Suporte Tecnico",
            },
            {
                "tipo_saldo": "admissao",
                "salario": 200000,
                "flag_salario_extremo": True,
                "codigo_cbo": "212405",
                "categoria_tech": "Desenvolvimento de Software",
            },
        ]
    )

    result = build_overview(df)

    assert result.loc[0, "total_registros_tech"] == 3
    assert result.loc[0, "total_admissoes"] == 2
    assert result.loc[0, "total_desligamentos"] == 1
    assert result.loc[0, "saldo_empregos"] == 1
    assert result.loc[0, "remuneracao_media"] == 5000
    assert result.loc[0, "remuneracao_mediana"] == 5000

