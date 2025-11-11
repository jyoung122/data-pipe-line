from typing import Any, Dict, Optional

from sqlalchemy.orm import Session

from ..core.milvus_client import get_milvus_client
from ..models.pipeline_model import PipelineRun
from ..models.staging_model import StagedData


def stage_payload(
    db: Session,
    *,
    pipeline_run: PipelineRun,
    use_case: str,
    document_id: Optional[str],
    payload_type: str,
    payload: Dict[str, Any],
    validation_status: str,
    issues: Optional[Dict[str, Any]] = None,
    write_embeddings: bool = False,
) -> StagedData:
    staged = StagedData(
        pipeline_run_id=pipeline_run.id,
        document_id=document_id,
        use_case=use_case,
        payload_type=payload_type,
        payload=payload,
        validation_status=validation_status,
        issues=issues,
    )
    db.add(staged)
    db.commit()
    db.refresh(staged)

    if write_embeddings:
        client = get_milvus_client()
        embedding = [float(len((payload.get("llm_output") or {}).get("result", "")))] * client.embedding_dim
        client.insert_embedding(
            use_case=use_case,
            source_type=payload_type,
            source_id=str(staged.id),
            pipeline_id=str(pipeline_run.pipeline_id),
            pipeline_run_id=str(pipeline_run.id),
            embedding=embedding,
            metadata={"payload": payload},
        )

    return staged
