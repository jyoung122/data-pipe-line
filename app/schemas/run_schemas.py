from datetime import datetime
from typing import Any, Dict, Optional
from uuid import UUID

from pydantic import BaseModel

from ..models.pipeline_model import RUN_STATUSES


class RunCreate(BaseModel):
    input_ref: Optional[str]
    document_id: Optional[UUID]
    file_path: Optional[str]
    text_payload: Optional[str]

    def validate_payload(self) -> None:
        if not any([self.document_id, self.file_path, self.text_payload]):
            raise ValueError("One of document_id, file_path, or text_payload must be provided")


class RunRead(BaseModel):
    id: UUID
    pipeline_id: UUID
    status: str
    input_ref: Optional[str]
    result_summary: Optional[Dict[str, Any]]
    error_message: Optional[str]
    created_at: datetime
    started_at: Optional[datetime]
    completed_at: Optional[datetime]

    class Config:
        orm_mode = True


class RunListItem(RunRead):
    pass
