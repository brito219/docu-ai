from fastapi import APIRouter, Depends, File, UploadFile, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from app.db.database import get_db
from app.models.document import Document, DocumentStatus, StorageType
from app.schemas.document import DocumentResponse
from app.services.file_service import build_storage_path, save_pdf_file, validate_pdf_upload


router = APIRouter(prefix="/documents", tags=["documents"])


@router.post("/upload", response_model=DocumentResponse, status_code=status.HTTP_201_CREATED)
async def upload_document(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
) -> Document:
    payload = await file.read()
    validate_pdf_upload(file, payload)

    stored_filename, target_path = build_storage_path(file.filename)
    save_pdf_file(target_path, payload)

    document = Document(
        original_filename=file.filename,
        stored_filename=stored_filename,
        content_type=file.content_type or "application/pdf",
        size_bytes=len(payload),
        storage_type=StorageType.LOCAL.value,
        local_path=str(target_path),
        status=DocumentStatus.UPLOADED.value,
    )

    try:
        db.add(document)
        db.commit()
        db.refresh(document)
    except SQLAlchemyError:
        db.rollback()
        if target_path.exists():
            target_path.unlink()
        raise

    return document
