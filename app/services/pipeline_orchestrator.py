from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, List, Optional

from sqlalchemy.orm import Session

from ..core.logging import get_logger
from ..models.document_model import Document
from ..models.pipeline_model import Pipeline, PipelineRun
from ..schemas.document_schemas import DocumentCreate
from . import ingestion_engine, processing_engine, staging_engine, validation_engine
from .document_service import register_document

logger = get_logger(__name__)


def execute_pipeline(
    db: Session,
    *,
    pipeline: Pipeline,
    run: PipelineRun,
    inputs: Dict[str, Any],
) -> Dict[str, Any]:
    chunks: List[str] = []
    document: Optional[Document] = None
    validation_report: Optional[Dict[str, Any]] = None
    llm_output: Optional[Dict[str, Any]] = None

    try:
        for node in pipeline.definition.get("nodes", []):
            node_type = node.get("type")
            config = node.get("config", {})
            logger.info("Executing node", extra={"run_id": str(run.id), "node_type": node_type})

            if node_type == "DocumentIngestionNode":
                if document is None:
                    doc_payload = DocumentCreate(
                        source_type=config.get("source_type", "text_payload"),
                        external_ref=inputs.get("input_ref"),
                        file_name=inputs.get("file_path"),
                        mime_type=None,
                        storage_uri=inputs.get("file_path"),
                        text_payload=inputs.get("text_payload"),
                        metadata={},
                    )
                    document = register_document(db, doc_payload, pipeline_run_id=run.id)
                text_content = inputs.get("text_payload") or "Sample document payload"
                chunk_models = ingestion_engine.ingest_document(db, document=document, text_payload=text_content)
                chunks.extend([chunk.content for chunk in chunk_models])
            elif node_type == "LLMProcessingNode":
                llm_output = processing_engine.process_chunks(
                    mode=config.get("mode", "summarize"),
                    model_name=config.get("model_name", "gpt-mini"),
                    prompt_template_id=config.get("prompt_template_id", "default"),
                    output_schema_id=config.get("output_schema_id", "generic"),
                    chunks=chunks or [inputs.get("text_payload", "")],
                )
            elif node_type == "ValidationNode":
                validation_report = validation_engine.validate_payload(
                    ruleset_name=config.get("ruleset_name", "default"),
                    use_semantic_lookup=config.get("use_semantic_lookup", False),
                    thresholds=config.get("thresholds", {}),
                    payload=llm_output or {},
                )
            elif node_type == "StagingNode":
                staging_engine.stage_payload(
                    db,
                    pipeline_run=run,
                    use_case=pipeline.use_case,
                    document_id=str(document.id) if document else None,
                    payload_type=config.get("payload_type", "generic_structured_output"),
                    payload={"llm_output": llm_output, "validation": validation_report},
                    validation_status=(validation_report or {}).get("status", "pending"),
                    issues={"items": (validation_report or {}).get("issues", [])},
                    write_embeddings=config.get("write_embeddings", False),
                )
            else:
                logger.warning("Unknown node type skipped", extra={"node_type": node_type})

        summary = {
            "chunks": len(chunks),
            "llm": llm_output,
            "validation": validation_report,
        }

        run.result_summary = summary
        run.status = "succeeded"
        run.completed_at = datetime.utcnow()
        db.add(run)
        db.commit()
        db.refresh(run)
        return summary
    except Exception as exc:  # pragma: no cover - defensive fallback
        logger.exception("Pipeline execution failed", extra={"run_id": str(run.id)})
        run.status = "failed"
        run.error_message = str(exc)
        run.completed_at = datetime.utcnow()
        db.add(run)
        db.commit()
        db.refresh(run)
        raise
