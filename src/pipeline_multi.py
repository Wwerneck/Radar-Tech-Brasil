"""Run the first multi-competence CAGED tech pipeline."""

from __future__ import annotations

import argparse
import subprocess
from pathlib import Path

from src.aggregate_tech import write_aggregates
from src.cbo_mapping import build_cbo_tech_mapping
from src.config import settings
from src.download_sources import download_caged_mov
from src.enrich_caged import enrich_caged_with_tech_mapping
from src.file_manifest import is_complete, read_manifest, update_file_status, write_manifest
from src.logging_config import setup_logging
from src.process_caged import process_caged_file
from src.utils import calculate_file_hash, file_size_mb


logger = setup_logging(__name__)

DEFAULT_COMPETENCES = [
    "202507",
    "202508",
    "202509",
    "202510",
    "202511",
    "202512",
    "202601",
    "202602",
    "202603",
    "202604",
    "202605",
    "202606",
]


def extract_7z(archive_path: Path, output_dir: Path, overwrite: bool = False) -> Path:
    """Extract a CAGED 7z archive with Windows tar/libarchive."""
    txt_path = output_dir / archive_path.name.replace(".7z", ".txt")
    if txt_path.exists() and not overwrite:
        logger.info("Skipping existing extracted file: %s", txt_path)
        return txt_path

    output_dir.mkdir(parents=True, exist_ok=True)
    logger.info("Extracting %s", archive_path)
    subprocess.run(
        ["tar", "-xf", str(archive_path), "-C", str(output_dir)],
        check=True,
    )
    return txt_path


def run_competence(
    competence: str,
    manifest: dict,
    manifest_path: Path,
    overwrite: bool = False,
    skip_download: bool = False,
) -> dict[str, Path]:
    """Run download, extract, process, enrich and aggregate for one competence."""
    archive = settings.raw_caged_dir / f"CAGEDMOV{competence}.7z"
    raw_txt = settings.raw_caged_dir / f"CAGEDMOV{competence}.txt"
    processed = settings.processed_dir / f"processed_cagedmov{competence}.csv"
    tech = settings.processed_dir / f"tech_cagedmov{competence}.csv"

    if not skip_download and (overwrite or not is_complete(manifest, f"download:{competence}")):
        archive = download_caged_mov(competence, overwrite=overwrite)
        update_file_status(
            manifest,
            f"download:{competence}",
            "complete",
            {"path": str(archive), "size_mb": round(file_size_mb(archive), 2)},
        )
        write_manifest(manifest_path, manifest)

    if overwrite or not is_complete(manifest, f"extract:{competence}"):
        raw_txt = extract_7z(archive, settings.raw_caged_dir, overwrite=overwrite)
        update_file_status(
            manifest,
            f"extract:{competence}",
            "complete",
            {
                "path": str(raw_txt),
                "size_mb": round(file_size_mb(raw_txt), 2),
                "sha256": calculate_file_hash(raw_txt),
            },
        )
        write_manifest(manifest_path, manifest)

    if overwrite or not is_complete(manifest, f"process:{competence}"):
        process_caged_file(raw_txt, processed, chunksize=100_000)
        update_file_status(
            manifest,
            f"process:{competence}",
            "complete",
            {"path": str(processed), "size_mb": round(file_size_mb(processed), 2)},
        )
        write_manifest(manifest_path, manifest)

    if overwrite or not is_complete(manifest, f"enrich:{competence}"):
        enrich_caged_with_tech_mapping(
            processed,
            settings.external_dir / "cbo_tech_mapping.csv",
            tech,
            chunksize=200_000,
        )
        update_file_status(
            manifest,
            f"enrich:{competence}",
            "complete",
            {"path": str(tech), "size_mb": round(file_size_mb(tech), 2)},
        )
        write_manifest(manifest_path, manifest)

    if overwrite or not is_complete(manifest, f"aggregate:{competence}"):
        write_aggregates(tech, settings.processed_dir, competence=competence)
        update_file_status(manifest, f"aggregate:{competence}", "complete", {"path": str(tech)})
        write_manifest(manifest_path, manifest)

    return {"archive": archive, "raw_txt": raw_txt, "processed": processed, "tech": tech}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run multi-competence CAGED tech pipeline.")
    parser.add_argument(
        "--competences",
        nargs="+",
        default=DEFAULT_COMPETENCES,
        help="Competences in YYYYMM format.",
    )
    parser.add_argument("--overwrite", action="store_true")
    parser.add_argument(
        "--skip-download",
        action="store_true",
        help="Use existing local archives instead of downloading.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    manifest_path = settings.processed_dir / "manifest.json"
    manifest = read_manifest(manifest_path)

    if not (settings.external_dir / "cbo_tech_mapping.csv").exists():
        mapping = build_cbo_tech_mapping(
            settings.raw_cbo_dir / "cbo2002_ocupacao.csv",
            settings.raw_cbo_dir / "cbo2002_familia.csv",
            settings.processed_dir / "processed_cagedmov202606.csv",
        )
        mapping.to_csv(
            settings.external_dir / "cbo_tech_mapping.csv",
            sep=";",
            index=False,
            encoding="utf-8",
        )

    for competence in args.competences:
        logger.info("Running competence %s", competence)
        run_competence(
            competence,
            manifest,
            manifest_path,
            overwrite=args.overwrite,
            skip_download=args.skip_download,
        )


if __name__ == "__main__":
    main()
