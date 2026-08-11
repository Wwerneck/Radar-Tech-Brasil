"""Download public source files used by Radar Tech Brasil."""

from __future__ import annotations

import argparse
import shutil
from dataclasses import dataclass
from ftplib import FTP
from pathlib import Path
from urllib.error import URLError
from urllib.request import Request, urlopen

from src.config import settings
from src.logging_config import setup_logging


logger = setup_logging(__name__)


@dataclass(frozen=True)
class SourceFile:
    """Public source file metadata."""

    name: str
    url: str
    destination: Path


CBO_SOURCES = [
    SourceFile(
        name="CBO2002 Ocupacao",
        url=(
            "https://www.gov.br/trabalho-e-emprego/pt-br/assuntos/cbo/"
            "servicos/downloads/cbo2002-ocupacao.csv"
        ),
        destination=settings.raw_cbo_dir / "cbo2002_ocupacao.csv",
    ),
    SourceFile(
        name="CBO2002 Familia",
        url=(
            "https://www.gov.br/trabalho-e-emprego/pt-br/assuntos/cbo/"
            "servicos/downloads/cbo2002-familia.csv"
        ),
        destination=settings.raw_cbo_dir / "cbo2002_familia.csv",
    ),
    SourceFile(
        name="Estrutura CBO",
        url=(
            "https://www.gov.br/trabalho-e-emprego/pt-br/assuntos/cbo/"
            "servicos/downloads/estrutura-cbo.zip"
        ),
        destination=settings.raw_cbo_dir / "estrutura_cbo.zip",
    ),
]


def download_file(source: SourceFile, overwrite: bool = False) -> Path:
    """Download one source file, preserving existing files by default."""
    source.destination.parent.mkdir(parents=True, exist_ok=True)

    if source.destination.exists() and not overwrite:
        logger.info("Skipping existing file: %s", source.destination)
        return source.destination

    request = Request(source.url, headers={"User-Agent": "radar-tech-brasil/0.1"})
    logger.info("Downloading %s from %s", source.name, source.url)

    try:
        with urlopen(request, timeout=120) as response:
            with source.destination.open("wb") as output:
                shutil.copyfileobj(response, output)
    except URLError as exc:
        raise RuntimeError(f"Could not download {source.url}: {exc}") from exc

    logger.info("Saved file: %s", source.destination)
    return source.destination


def download_cbo(overwrite: bool = False) -> list[Path]:
    """Download the official CBO files needed for initial occupation enrichment."""
    return [download_file(source, overwrite=overwrite) for source in CBO_SOURCES]


def download_caged_mov(year_month: str, overwrite: bool = False) -> Path:
    """Download one Novo CAGED movement file from the official MTE FTP."""
    if len(year_month) != 6 or not year_month.isdigit():
        raise ValueError("year_month must use the YYYYMM format.")

    year = year_month[:4]
    filename = f"CAGEDMOV{year_month}.7z"
    destination = settings.raw_caged_dir / filename
    destination.parent.mkdir(parents=True, exist_ok=True)

    if destination.exists() and not overwrite:
        logger.info("Skipping existing file: %s", destination)
        return destination

    remote_dir = f"/pdet/microdados/NOVO CAGED/{year}/{year_month}"
    logger.info("Downloading %s from ftp.mtps.gov.br%s", filename, remote_dir)

    with FTP("ftp.mtps.gov.br", timeout=120, encoding="latin1") as ftp:
        ftp.login()
        ftp.cwd(remote_dir)
        with destination.open("wb") as output:
            ftp.retrbinary(f"RETR {filename}", output.write)

    logger.info("Saved file: %s", destination)
    return destination


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Download public project sources.")
    parser.add_argument(
        "--source",
        choices=["cbo", "caged-mov"],
        default="cbo",
        help="Source group to download.",
    )
    parser.add_argument(
        "--year-month",
        help="Novo CAGED competence in YYYYMM format. Required for caged-mov.",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Replace existing local files.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.source == "cbo":
        download_cbo(overwrite=args.overwrite)
    elif args.source == "caged-mov":
        if not args.year_month:
            raise ValueError("--year-month is required for --source caged-mov")
        download_caged_mov(args.year_month, overwrite=args.overwrite)


if __name__ == "__main__":
    main()
