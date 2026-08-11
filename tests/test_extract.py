from pathlib import Path

from src.extract import list_caged_files


def test_list_caged_files_returns_supported_files(tmp_path: Path) -> None:
    (tmp_path / "CAGED.csv").write_text("a;b\n1;2\n", encoding="utf-8")
    (tmp_path / "CAGED.txt").write_text("a;b\n1;2\n", encoding="utf-8")
    (tmp_path / "ignore.xlsx").write_text("", encoding="utf-8")

    files = list_caged_files(tmp_path)

    assert [file.name for file in files] == ["CAGED.csv", "CAGED.txt"]

