from pathlib import Path

import pandas as pd

from src.consolidate_aggregates import consolidate_aggregate_files, extract_competence


def test_extract_competence_from_aggregate_filename() -> None:
    assert extract_competence(Path("agg_tech_overview_202606.csv")) == "202606"


def test_consolidate_aggregate_files_adds_competence(tmp_path: Path) -> None:
    pd.DataFrame([{"total_registros_tech": 10}]).to_csv(
        tmp_path / "agg_tech_overview_202605.csv",
        sep=";",
        index=False,
    )
    pd.DataFrame([{"total_registros_tech": 20}]).to_csv(
        tmp_path / "agg_tech_overview_202606.csv",
        sep=";",
        index=False,
    )
    pd.DataFrame([{"competencia": 202606, "total_registros_tech": 20}]).to_csv(
        tmp_path / "agg_tech_overview_mensal.csv",
        sep=";",
        index=False,
    )

    consolidate_aggregate_files(tmp_path, tmp_path)

    result = pd.read_csv(tmp_path / "agg_tech_overview_mensal.csv", sep=";")
    assert result["competencia"].tolist() == [202605, 202606]
    assert result["total_registros_tech"].tolist() == [10, 20]
