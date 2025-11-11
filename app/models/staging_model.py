import uuid
from datetime import datetime

from sqlalchemy import Column, DateTime, Enum, ForeignKey, JSON, String
from sqlalchemy.orm import relationship

from .base import Base, GUID

VALIDATION_STATUSES = ("pending", "passed", "failed", "needs_review")


class StagedData(Base):
    __tablename__ = "staged_data"

    id = Column(GUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    pipeline_run_id = Column(GUID(as_uuid=True), ForeignKey("pipeline_runs.id"), nullable=False)
    document_id = Column(GUID(as_uuid=True), ForeignKey("documents.id"))
    use_case = Column(String, nullable=False)
    payload_type = Column(String, nullable=False)
    payload = Column(JSON, nullable=False)
    validation_status = Column(Enum(*VALIDATION_STATUSES, name="validation_status"), nullable=False)
    issues = Column(JSON)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)

    pipeline_run = relationship("PipelineRun", back_populates="staged_outputs")
    document = relationship("Document", back_populates="staged_outputs")
