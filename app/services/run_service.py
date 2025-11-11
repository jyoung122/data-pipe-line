from datetime import datetime
from typing import Dict, List, Optional
from uuid import UUID

from sqlalchemy.orm import Session

from ..core.logging import get_logger
from ..models.pipeline_model import Pipeline, PipelineRun
from ..schemas.run_schemas import RunCreate
from .pipeline_orchestrator import execute_pipeline

logger = get_logger(__name__)


def create_run(db: Session, pipeline: Pipeline, payload: RunCreate) -> PipelineRun:
    payload.validate_payload()

    run = PipelineRun(
        pipeline_id=pipeline.id,
        status="queued",
        input_ref=payload.input_ref,
        created_at=datetime.utcnow(),
    )
    db.add(run)
    db.commit()
    db.refresh(run)

    run.status = "running"
    run.started_at = datetime.utcnow()
    db.add(run)
    db.commit()
    db.refresh(run)

    inputs: Dict[str, Optional[str]] = {
        "input_ref": payload.input_ref,
        "text_payload": payload.text_payload,
        "file_path": payload.file_path,
        "document_id": str(payload.document_id) if payload.document_id else None,
    }
    summary = execute_pipeline(db, pipeline=pipeline, run=run, inputs=inputs)  # synchronous for POC
    logger.info("Run completed", extra={"run_id": str(run.id), "summary": summary})
    return run


def get_run(db: Session, run_id: UUID) -> Optional[PipelineRun]:
    return db.query(PipelineRun).filter(PipelineRun.id == run_id).first()


def list_runs(db: Session, *, pipeline_id: Optional[UUID] = None, status: Optional[str] = None, limit: int = 50) -> List[PipelineRun]:
    query = db.query(PipelineRun)
    if pipeline_id:
        query = query.filter(PipelineRun.pipeline_id == pipeline_id)
    if status:
        query = query.filter(PipelineRun.status == status)
    return query.order_by(PipelineRun.created_at.desc()).limit(limit).all()
