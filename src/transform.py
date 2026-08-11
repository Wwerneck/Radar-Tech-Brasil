"""Transform Novo CAGED records after real file inspection."""

from __future__ import annotations

import re
import unicodedata
from typing import Iterable

import pandas as pd


CAGED_COLUMN_RENAME = {
    "competênciamov": "competencia_mov",
    "região": "regiao",
    "uf": "uf",
    "município": "municipio",
    "seção": "secao",
    "subclasse": "subclasse",
    "saldomovimentação": "saldo_movimentacao",
    "cbo2002ocupação": "cbo_2002_ocupacao",
    "categoria": "categoria",
    "graudeinstrução": "grau_instrucao",
    "idade": "idade",
    "horascontratuais": "horas_contratuais",
    "raçacor": "raca_cor",
    "sexo": "sexo",
    "tipoempregador": "tipo_empregador",
    "tipoestabelecimento": "tipo_estabelecimento",
    "tipomovimentação": "tipo_movimentacao",
    "tipodedeficiência": "tipo_deficiencia",
    "indtrabintermitente": "ind_trab_intermitente",
    "indtrabparcial": "ind_trab_parcial",
    "salário": "salario",
    "tamestabjan": "tamanho_estabelecimento_jan",
    "indicadoraprendiz": "indicador_aprendiz",
    "origemdainformação": "origem_informacao",
    "competênciadec": "competencia_dec",
    "indicadordeforadoprazo": "indicador_fora_prazo",
    "unidadesaláriocódigo": "unidade_salario_codigo",
    "valorsaláriofixo": "valor_salario_fixo",
}

ANALYTICAL_COLUMNS = list(CAGED_COLUMN_RENAME.values())
INTEGER_COLUMNS = [
    "competencia_mov",
    "regiao",
    "uf",
    "municipio",
    "subclasse",
    "saldo_movimentacao",
    "cbo_2002_ocupacao",
    "categoria",
    "grau_instrucao",
    "idade",
    "raca_cor",
    "sexo",
    "tipo_empregador",
    "tipo_estabelecimento",
    "tipo_movimentacao",
    "tipo_deficiencia",
    "ind_trab_intermitente",
    "ind_trab_parcial",
    "tamanho_estabelecimento_jan",
    "indicador_aprendiz",
    "origem_informacao",
    "competencia_dec",
    "indicador_fora_prazo",
    "unidade_salario_codigo",
]
DECIMAL_COLUMNS = ["horas_contratuais", "salario", "valor_salario_fixo"]
VALID_UF_CODES = {
    11,
    12,
    13,
    14,
    15,
    16,
    17,
    21,
    22,
    23,
    24,
    25,
    26,
    27,
    28,
    29,
    31,
    32,
    33,
    35,
    41,
    42,
    43,
    50,
    51,
    52,
    53,
}


def normalize_column_name(column: str) -> str:
    """Normalize one column name to lowercase ASCII snake_case."""
    normalized = unicodedata.normalize("NFKD", column.strip().lower())
    ascii_text = normalized.encode("ascii", "ignore").decode("ascii")
    ascii_text = re.sub(r"[^a-z0-9]+", "_", ascii_text)
    return ascii_text.strip("_")


def clean_column_names(columns: Iterable[str]) -> list[str]:
    """Return normalized column names without changing source files."""
    return [normalize_column_name(column) for column in columns]


def rename_caged_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Rename known Novo CAGED columns based on the inspected 202606 layout."""
    normalized_lookup = {
        normalize_column_name(source): target
        for source, target in CAGED_COLUMN_RENAME.items()
    }
    rename_map = {
        column: normalized_lookup.get(normalize_column_name(column), normalize_column_name(column))
        for column in df.columns
    }
    return df.rename(columns=rename_map)


def select_analytical_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Select columns approved for the first analytical processing layer."""
    missing = [column for column in ANALYTICAL_COLUMNS if column not in df.columns]
    if missing:
        raise ValueError(f"Missing expected CAGED columns: {missing}")
    return df.loc[:, ANALYTICAL_COLUMNS].copy()


def convert_brazilian_decimal(series: pd.Series) -> pd.Series:
    """Convert numbers stored as Brazilian decimal text to float."""
    normalized = (
        series.astype("string")
        .str.replace(".", "", regex=False)
        .str.replace(",", ".", regex=False)
    )
    return pd.to_numeric(
        normalized,
        errors="coerce",
    )


def convert_data_types(df: pd.DataFrame) -> pd.DataFrame:
    """Convert inspected CAGED columns to analysis-friendly dtypes."""
    result = df.copy()

    for column in INTEGER_COLUMNS:
        if column in result.columns:
            result[column] = pd.to_numeric(result[column], errors="coerce").astype("Int64")

    for column in DECIMAL_COLUMNS:
        if column in result.columns:
            result[column] = convert_brazilian_decimal(result[column])

    if "secao" in result.columns:
        result["secao"] = result["secao"].astype("string").str.strip()

    return result


def classify_saldo_movimentacao(value: object) -> str:
    """Classify CAGED balance movement without translating detailed event codes."""
    if pd.isna(value):
        return "nao_informado"
    if int(value) == 1:
        return "admissao"
    if int(value) == -1:
        return "desligamento"
    return "desconhecido"


def make_age_group(age: object) -> str:
    """Create an initial age group for profiling and dashboard filters."""
    if pd.isna(age):
        return "Nao informado"

    age_int = int(age)
    if age_int <= 20:
        return "Ate 20"
    if age_int <= 25:
        return "21-25"
    if age_int <= 30:
        return "26-30"
    if age_int <= 35:
        return "31-35"
    if age_int <= 40:
        return "36-40"
    if age_int <= 50:
        return "41-50"
    return "51+"


def add_quality_flags(df: pd.DataFrame) -> pd.DataFrame:
    """Add quality flags while preserving all source records."""
    result = df.copy()
    result["flag_idade_ausente"] = result["idade"].isna()
    result["flag_idade_invalida"] = result["idade"].notna() & (
        (result["idade"] < 14) | (result["idade"] > 100)
    )
    result["flag_salario_zero"] = result["salario"].fillna(-1).eq(0)
    result["flag_salario_extremo"] = result["salario"].fillna(0).gt(100_000)
    result["flag_horas_invalidas"] = result["horas_contratuais"].notna() & (
        (result["horas_contratuais"] < 0) | (result["horas_contratuais"] > 60)
    )
    result["flag_uf_invalida"] = ~result["uf"].isin(VALID_UF_CODES)
    result["flag_cbo_invalida"] = ~result["cbo_2002_ocupacao"].astype("string").str.match(
        r"^\d{1,6}$", na=False
    )
    return result


def add_derived_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Add conservative derived attributes for the first processed layer."""
    result = df.copy()
    result["ano"] = (result["competencia_mov"] // 100).astype("Int64")
    result["mes"] = (result["competencia_mov"] % 100).astype("Int64")
    result["ano_mes"] = result["competencia_mov"].astype("string")
    result["tipo_saldo"] = result["saldo_movimentacao"].map(classify_saldo_movimentacao)
    result["faixa_etaria"] = result["idade"].map(make_age_group)
    return result


def transform_caged_chunk(df: pd.DataFrame) -> pd.DataFrame:
    """Transform one Novo CAGED chunk into the first processed layer."""
    renamed = rename_caged_columns(df)
    selected = select_analytical_columns(renamed)
    typed = convert_data_types(selected)
    enriched = add_derived_columns(typed)
    return add_quality_flags(enriched)
