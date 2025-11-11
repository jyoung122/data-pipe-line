from datetime import datetime
from typing import Any, Dict, Optional
from uuid import UUID

from pydantic import BaseModel, Field

from ..models.document_model import DOCUMENT_SOURCE_TYPES

SOURCE_PATTERN = "^(" + "|".join(DOCUMENT_SOURCE_TYPES) + ")$"


class DocumentCreate(BaseModel):
    source_type: str = Field(regex=SOURCE_PATTERN)
    external_ref: Optional[str]
    file_name: Optional[str]
    mime_type: Optional[str]
    storage_uri: Optional[str]
    text_payload: Optional[str]
    metadata: Optional[Dict[str, Any]]


class DocumentRead(BaseModel):
    id: UUID
    source_type: str
    external_ref: Optional[str]
    file_name: Optional[str]
    mime_type: Optional[str]
    storage_uri: Optional[str]
    metadata: Optional[Dict[str, Any]]
    created_at: datetime

    class Config:
        orm_mode = True
