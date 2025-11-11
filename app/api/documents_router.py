from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..core.db import get_db
from ..schemas.common import APIResponse
from ..schemas.document_schemas import DocumentCreate, DocumentRead
from ..services.document_service import register_document

router = APIRouter(prefix="/documents", tags=["documents"])


@router.post("", response_model=APIResponse[DocumentRead])
def register_document_endpoint(payload: DocumentCreate, db: Session = Depends(get_db)) -> APIResponse[DocumentRead]:
    document = register_document(db, payload)
    return APIResponse.ok(DocumentRead.from_orm(document))
