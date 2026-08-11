from src.file_manifest import is_complete, update_file_status


def test_update_file_status_marks_entry_complete() -> None:
    manifest = {"files": {}}

    update_file_status(manifest, "process:202606", "complete", {"rows": 10})

    assert is_complete(manifest, "process:202606")
    assert manifest["files"]["process:202606"]["metadata"]["rows"] == 10

