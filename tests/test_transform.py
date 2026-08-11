import pandas as pd

from src.transform import (
    clean_column_names,
    convert_brazilian_decimal,
    make_age_group,
    normalize_column_name,
    transform_caged_chunk,
)


def test_normalize_column_name_strips_and_lowercases() -> None:
    assert normalize_column_name(" CBO Ocupacao ") == "cbo_ocupacao"


def test_clean_column_names_normalizes_list() -> None:
    assert clean_column_names([" Competencia ", "Salario Mensal"]) == [
        "competencia",
        "salario_mensal",
    ]


def test_normalize_column_name_removes_accents() -> None:
    assert normalize_column_name("salário") == "salario"


def test_convert_brazilian_decimal() -> None:
    result = convert_brazilian_decimal(pd.Series(["1.500,25", "0,00", None]))

    assert result.iloc[0] == 1500.25
    assert result.iloc[1] == 0
    assert pd.isna(result.iloc[2])


def test_make_age_group() -> None:
    assert make_age_group(20) == "Ate 20"
    assert make_age_group(25) == "21-25"
    assert make_age_group(None) == "Nao informado"


def test_transform_caged_chunk_adds_derived_columns_and_flags() -> None:
    raw = pd.DataFrame(
        [
            {
                "competênciamov": 202606,
                "região": 3,
                "uf": 99,
                "município": 355030,
                "seção": " J ",
                "subclasse": 6201501,
                "saldomovimentação": 1,
                "cbo2002ocupação": 212405,
                "categoria": 101,
                "graudeinstrução": 9,
                "idade": None,
                "horascontratuais": "44,00",
                "raçacor": 1,
                "sexo": 1,
                "tipoempregador": 0,
                "tipoestabelecimento": 1,
                "tipomovimentação": 97,
                "tipodedeficiência": 0,
                "indtrabintermitente": 0,
                "indtrabparcial": 0,
                "salário": "0,00",
                "tamestabjan": 4,
                "indicadoraprendiz": 0,
                "origemdainformação": 1,
                "competênciadec": 202606,
                "indicadordeforadoprazo": 0,
                "unidadesaláriocódigo": 5,
                "valorsaláriofixo": "0,00",
            }
        ]
    )

    result = transform_caged_chunk(raw)

    assert result.loc[0, "tipo_saldo"] == "admissao"
    assert result.loc[0, "faixa_etaria"] == "Nao informado"
    assert bool(result.loc[0, "flag_idade_ausente"])
    assert bool(result.loc[0, "flag_salario_zero"])
    assert bool(result.loc[0, "flag_uf_invalida"])
