import importlib
from pathlib import Path

from sqlalchemy import select
from sqlalchemy.orm import Session

from conftest import create_test_client


def test_upload_pdf_persists_file_and_metadata(tmp_path: Path) -> None:
    payload = b"%PDF-1.4\n1 0 obj\n<<>>\nendobj\n"

    with create_test_client(tmp_path) as client:
        response = client.post(
            "/documents/upload",
            files={"file": ("sample.pdf", payload, "application/pdf")},
        )

    assert response.status_code == 201
    body = response.json()
    assert body["original_filename"] == "sample.pdf"
    assert body["storage_type"] == "LOCAL"
    assert body["status"] == "UPLOADED"
    assert body["size_bytes"] == len(payload)

    stored_path = tmp_path / "storage" / body["stored_filename"]
    assert stored_path.exists()
    assert stored_path.read_bytes() == payload

    main = importlib.import_module("app.main")
    document_module = importlib.import_module("app.models.document")
    db_module = importlib.import_module("app.db.database")

    with Session(db_module.engine) as session:
        document = session.execute(select(document_module.Document)).scalar_one()
        assert document.original_filename == "sample.pdf"
        assert document.local_path.endswith(body["stored_filename"])


def test_upload_rejects_non_pdf_extension(tmp_path: Path) -> None:
    payload = b"%PDF-1.4\nfake"

    with create_test_client(tmp_path) as client:
        response = client.post(
            "/documents/upload",
            files={"file": ("notes.txt", payload, "application/pdf")},
        )

    assert response.status_code == 415
    assert ".pdf extension" in response.json()["detail"]


def test_upload_rejects_invalid_pdf_signature(tmp_path: Path) -> None:
    with create_test_client(tmp_path) as client:
        response = client.post(
            "/documents/upload",
            files={"file": ("fake.pdf", b"not-a-pdf", "application/pdf")},
        )

    assert response.status_code == 422
    assert "valid PDF signature" in response.json()["detail"]


def test_upload_rejects_file_above_limit(tmp_path: Path) -> None:
    payload = b"%PDF" + b"a" * (10 * 1024 * 1024)

    with create_test_client(tmp_path) as client:
        response = client.post(
            "/documents/upload",
            files={"file": ("large.pdf", payload, "application/pdf")},
        )

    assert response.status_code == 413
    assert "10 MB" in response.json()["detail"]
