import uuid
from datetime import datetime

from sqlalchemy import Column, DateTime, Enum, ForeignKey, Integer, JSON, String, Text, UniqueConstraint
from sqlalchemy.orm import relationship

from .base import Base, GUID

DOCUMENT_SOURCE_TYPES = (
    "file_upload",
    "file_path",
    "email",
    "text_payload",
    "external_system",
)


class Document(Base):
    __tablename__ = "documents"

    id = Column(GUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    pipeline_run_id = Column(GUID(as_uuid=True), ForeignKey("pipeline_runs.id"))
    source_type = Column(Enum(*DOCUMENT_SOURCE_TYPES, name="document_source_type"), nullable=False)
    external_ref = Column(String)
    file_name = Column(String)
    mime_type = Column(String)
    storage_uri = Column(String)
    metadata = Column(JSON)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)

    pipeline_run = relationship("PipelineRun", back_populates="documents")
    chunks = relationship("IngestedChunk", back_populates="document", cascade="all, delete-orphan")
    staged_outputs = relationship("StagedData", back_populates="document")


class IngestedChunk(Base):
    __tablename__ = "ingested_chunks"

    id = Column(Integer, primary_key=True, autoincrement=True)
    document_id = Column(GUID(as_uuid=True), ForeignKey("documents.id"), nullable=False)
    chunk_index = Column(Integer, nullable=False)
    content = Column(Text, nullable=False)
    metadata = Column(JSON)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)

    document = relationship("Document", back_populates="chunks")

    __table_args__ = (
        UniqueConstraint("document_id", "chunk_index", name="uq_document_chunk_index"),
        {
            "sqlite_autoincrement": True,
        },
    )
