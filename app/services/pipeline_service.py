from datetime import datetime
from typing import List, Optional
from uuid import UUID

from sqlalchemy.orm import Session

from ..models.pipeline_model import Pipeline
from ..schemas.pipeline_schemas import PipelineCreate, PipelineUpdate


def list_pipelines(db: Session, *, use_case: Optional[str] = None, active_only: bool = True) -> List[Pipeline]:
    query = db.query(Pipeline)
    if use_case:
        query = query.filter(Pipeline.use_case == use_case)
    if active_only:
        query = query.filter(Pipeline.is_active.is_(True))
    return query.order_by(Pipeline.created_at.desc()).all()


def get_pipeline(db: Session, pipeline_id: UUID) -> Optional[Pipeline]:
    return db.query(Pipeline).filter(Pipeline.id == pipeline_id).first()


def create_pipeline(db: Session, payload: PipelineCreate) -> Pipeline:
    pipeline = Pipeline(
        name=payload.name,
        description=payload.description,
        use_case=payload.use_case,
        definition=payload.definition.dict(),
    )
    db.add(pipeline)
    db.commit()
    db.refresh(pipeline)
    return pipeline


def update_pipeline(db: Session, pipeline: Pipeline, payload: PipelineUpdate) -> Pipeline:
    if payload.name is not None:
        pipeline.name = payload.name
    if payload.description is not None:
        pipeline.description = payload.description
    if payload.use_case is not None:
        pipeline.use_case = payload.use_case
    if payload.definition is not None:
        pipeline.definition = payload.definition.dict()
    if payload.is_active is not None:
        pipeline.is_active = payload.is_active

    pipeline.updated_at = datetime.utcnow()
    db.add(pipeline)
    db.commit()
    db.refresh(pipeline)
    return pipeline


def delete_pipeline(db: Session, pipeline: Pipeline) -> None:
    db.delete(pipeline)
    db.commit()
