import uuid
from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Enum, ForeignKey, JSON, String, Text
from sqlalchemy.orm import relationship

from .base import Base, GUID


PIPELINE_USE_CASES = ("invoice_processing", "foia_request", "generic")
RUN_STATUSES = ("queued", "running", "succeeded", "failed")


class Pipeline(Base):
    __tablename__ = "pipelines"

    id = Column(GUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, unique=True, nullable=False)
    description = Column(Text)
    use_case = Column(Enum(*PIPELINE_USE_CASES, name="pipeline_use_case"), nullable=False)
    definition = Column(JSON, nullable=False)
    is_active = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)

    runs = relationship("PipelineRun", back_populates="pipeline", cascade="all, delete-orphan")


class PipelineRun(Base):
    __tablename__ = "pipeline_runs"

    id = Column(GUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    pipeline_id = Column(GUID(as_uuid=True), ForeignKey("pipelines.id"), nullable=False)
    status = Column(Enum(*RUN_STATUSES, name="pipeline_run_status"), nullable=False, default="queued")
    input_ref = Column(String)
    result_summary = Column(JSON)
    error_message = Column(Text)
    logs_location = Column(String)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)
    started_at = Column(DateTime(timezone=True))
    completed_at = Column(DateTime(timezone=True))

    pipeline = relationship("Pipeline", back_populates="runs")
    documents = relationship("Document", back_populates="pipeline_run")
    staged_outputs = relationship("StagedData", back_populates="pipeline_run")
