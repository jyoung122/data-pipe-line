from typing import List

from sqlalchemy.orm import Session

from ..models.document_model import Document, IngestedChunk


def ingest_document(db: Session, document: Document, *, text_payload: str) -> List[IngestedChunk]:
    chunk = IngestedChunk(
        document_id=document.id,
        chunk_index=0,
        content=text_payload,
        metadata={"generated": True},
    )
    db.add(chunk)
    db.commit()
    db.refresh(chunk)
    return [chunk]
