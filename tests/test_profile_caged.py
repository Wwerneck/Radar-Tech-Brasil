import pandas as pd

from src.profile_caged import normalize_numeric_series


def test_normalize_numeric_series_converts_brazilian_decimal_text() -> None:
    series = pd.Series(["2125,86", "0,00", None], name="salário")

    result = normalize_numeric_series(series)

    assert result.tolist()[:2] == [2125.86, 0.0]
    assert pd.isna(result.iloc[2])

