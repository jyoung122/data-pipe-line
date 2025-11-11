from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from ..core.db import get_db
from ..schemas.common import APIResponse
from ..schemas.pipeline_schemas import (
    PipelineCreate,
    PipelineRead,
    PipelineSummary,
    PipelineUpdate,
)
from ..schemas.run_schemas import RunCreate, RunRead
from ..services import pipeline_service, run_service

router = APIRouter(prefix="/pipelines", tags=["pipelines"])


@router.post("", response_model=APIResponse[PipelineRead])
def create_pipeline_endpoint(payload: PipelineCreate, db: Session = Depends(get_db)) -> APIResponse[PipelineRead]:
    pipeline = pipeline_service.create_pipeline(db, payload)
    return APIResponse.ok(PipelineRead.from_orm(pipeline))


@router.get("", response_model=APIResponse[List[PipelineSummary]])
def list_pipelines_endpoint(
    use_case: Optional[str] = Query(default=None),
    active_only: bool = Query(default=True),
    db: Session = Depends(get_db),
) -> APIResponse[List[PipelineSummary]]:
    pipelines = pipeline_service.list_pipelines(db, use_case=use_case, active_only=active_only)
    return APIResponse.ok([PipelineSummary.from_orm(p) for p in pipelines])


@router.get("/{pipeline_id}", response_model=APIResponse[PipelineRead])
def get_pipeline_endpoint(pipeline_id: UUID, db: Session = Depends(get_db)) -> APIResponse[PipelineRead]:
    pipeline = pipeline_service.get_pipeline(db, pipeline_id)
    if not pipeline:
        raise HTTPException(status_code=404, detail="Pipeline not found")
    return APIResponse.ok(PipelineRead.from_orm(pipeline))


@router.put("/{pipeline_id}", response_model=APIResponse[PipelineRead])
def update_pipeline_endpoint(
    pipeline_id: UUID,
    payload: PipelineUpdate,
    db: Session = Depends(get_db),
) -> APIResponse[PipelineRead]:
    pipeline = pipeline_service.get_pipeline(db, pipeline_id)
    if not pipeline:
        raise HTTPException(status_code=404, detail="Pipeline not found")
    pipeline = pipeline_service.update_pipeline(db, pipeline, payload)
    return APIResponse.ok(PipelineRead.from_orm(pipeline))


@router.delete("/{pipeline_id}", response_model=APIResponse[dict])
def delete_pipeline_endpoint(pipeline_id: UUID, db: Session = Depends(get_db)) -> APIResponse[dict]:
    pipeline = pipeline_service.get_pipeline(db, pipeline_id)
    if not pipeline:
        raise HTTPException(status_code=404, detail="Pipeline not found")
    pipeline_service.delete_pipeline(db, pipeline)
    return APIResponse.ok({"id": str(pipeline_id), "deleted": True})


@router.post("/{pipeline_id}/run", response_model=APIResponse[RunRead])
def run_pipeline_endpoint(
    pipeline_id: UUID,
    payload: RunCreate,
    db: Session = Depends(get_db),
) -> APIResponse[RunRead]:
    pipeline = pipeline_service.get_pipeline(db, pipeline_id)
    if not pipeline:
        raise HTTPException(status_code=404, detail="Pipeline not found")
    try:
        run = run_service.create_run(db, pipeline, payload)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    return APIResponse.ok(RunRead.from_orm(run))
