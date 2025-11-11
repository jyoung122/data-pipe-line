from datetime import datetime
from typing import Any, Dict, List, Optional
from uuid import UUID

from pydantic import BaseModel, Field

from ..models.pipeline_model import PIPELINE_USE_CASES

USE_CASE_PATTERN = "^(" + "|".join(PIPELINE_USE_CASES) + ")$"


class PipelineDefinition(BaseModel):
    nodes: List[Dict[str, Any]] = Field(default_factory=list)
    edges: List[Dict[str, Any]] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)


class PipelineCreate(BaseModel):
    name: str
    description: Optional[str]
    use_case: str = Field(regex=USE_CASE_PATTERN)
    definition: PipelineDefinition


class PipelineUpdate(BaseModel):
    name: Optional[str]
    description: Optional[str]
    use_case: Optional[str]
    definition: Optional[PipelineDefinition]
    is_active: Optional[bool]


class PipelineSummary(BaseModel):
    id: UUID
    name: str
    use_case: str
    description: Optional[str]
    is_active: bool
    created_at: datetime

    class Config:
        orm_mode = True


class PipelineRead(PipelineSummary):
    updated_at: datetime
    definition: PipelineDefinition
