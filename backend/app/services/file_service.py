from pathlib import Path
from uuid import uuid4

from fastapi import HTTPException, UploadFile, status

from app.core.config import get_settings


ALLOWED_CONTENT_TYPES = {"application/pdf", "application/x-pdf", "application/octet-stream"}


def validate_pdf_upload(file: UploadFile, payload: bytes) -> None:
    settings = get_settings()

    if not file.filename:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No file was uploaded.")

    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail="The uploaded file must use the .pdf extension.",
        )

    if file.content_type not in ALLOWED_CONTENT_TYPES:
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail="The uploaded file does not use an allowed PDF content type.",
        )

    if not payload:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="The uploaded file is empty.")

    if len(payload) > settings.max_upload_size_bytes:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"The uploaded file exceeds the {settings.max_upload_size_mb} MB limit.",
        )

    if not payload.startswith(b"%PDF"):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="The uploaded content does not match a valid PDF signature.",
        )


def build_storage_path(original_filename: str) -> tuple[str, Path]:
    file_suffix = Path(original_filename).suffix.lower() or ".pdf"
    stored_filename = f"{uuid4()}{file_suffix}"
    settings = get_settings()
    target_path = settings.local_storage_path / stored_filename
    return stored_filename, target_path


def save_pdf_file(target_path: Path, payload: bytes) -> None:
    target_path.parent.mkdir(parents=True, exist_ok=True)
    target_path.write_bytes(payload)
