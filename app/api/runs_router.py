from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from ..core.db import get_db
from ..schemas.common import APIResponse
from ..schemas.run_schemas import RunListItem, RunRead
from ..services import run_service

router = APIRouter(prefix="/runs", tags=["runs"])


@router.get("", response_model=APIResponse[List[RunListItem]])
def list_runs_endpoint(
    pipeline_id: Optional[UUID] = Query(default=None),
    status: Optional[str] = Query(default=None),
    limit: int = Query(default=50, le=100),
    db: Session = Depends(get_db),
) -> APIResponse[List[RunListItem]]:
    runs = run_service.list_runs(db, pipeline_id=pipeline_id, status=status, limit=limit)
    return APIResponse.ok([RunListItem.from_orm(r) for r in runs])


@router.get("/{run_id}", response_model=APIResponse[RunRead])
def get_run_endpoint(run_id: UUID, db: Session = Depends(get_db)) -> APIResponse[RunRead]:
    run = run_service.get_run(db, run_id)
    if not run:
        raise HTTPException(status_code=404, detail="Run not found")
    return APIResponse.ok(RunRead.from_orm(run))
