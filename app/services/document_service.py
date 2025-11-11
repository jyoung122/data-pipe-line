from typing import Optional
from uuid import UUID

from sqlalchemy.orm import Session

from ..models.document_model import Document, DOCUMENT_SOURCE_TYPES
from ..schemas.document_schemas import DocumentCreate


def register_document(db: Session, payload: DocumentCreate, pipeline_run_id: Optional[UUID] = None) -> Document:
    if payload.source_type not in DOCUMENT_SOURCE_TYPES:
        raise ValueError("Unsupported source type")

    document = Document(
        pipeline_run_id=pipeline_run_id,
        source_type=payload.source_type,
        external_ref=payload.external_ref,
        file_name=payload.file_name,
        mime_type=payload.mime_type,
        storage_uri=payload.storage_uri,
        metadata=payload.metadata,
    )
    db.add(document)
    db.commit()
    db.refresh(document)
    return document
