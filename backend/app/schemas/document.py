from datetime import datetime

from pydantic import BaseModel, ConfigDict


class DocumentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    original_filename: str
    stored_filename: str
    content_type: str
    size_bytes: int
    storage_type: str
    status: str
    created_at: datetime
