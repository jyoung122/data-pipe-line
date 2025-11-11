from __future__ import annotations

import json
from typing import Any, Dict, List, Optional

from .config import get_settings


class MilvusStubClient:
    """Minimal in-memory stand-in when Milvus is unavailable."""

    def __init__(self) -> None:
        self._store: List[Dict[str, Any]] = []

    def insert(self, record: Dict[str, Any]) -> None:
        self._store.append(record)

    def query(self, *, limit: int = 5, **kwargs: Any) -> List[Dict[str, Any]]:
        return list(reversed(self._store))[:limit]


class MilvusClient:
    def __init__(self) -> None:
        settings = get_settings()
        self.collection = settings.milvus_collection
        self.embedding_dim = settings.milvus_embedding_dim
        self._client = None

        if settings.milvus_uri:
            try:
                from pymilvus import Collection, FieldSchema, CollectionSchema, DataType, connections

                connections.connect(alias="default", uri=str(settings.milvus_uri))
                fields = [
                    FieldSchema(name="id", dtype=DataType.INT64, is_primary=True, auto_id=True),
                    FieldSchema(name="use_case", dtype=DataType.VARCHAR, max_length=64),
                    FieldSchema(name="source_type", dtype=DataType.VARCHAR, max_length=64),
                    FieldSchema(name="source_id", dtype=DataType.VARCHAR, max_length=64),
                    FieldSchema(name="pipeline_id", dtype=DataType.VARCHAR, max_length=64, is_primary=False),
                    FieldSchema(name="pipeline_run_id", dtype=DataType.VARCHAR, max_length=64),
                    FieldSchema(name="embedding", dtype=DataType.FLOAT_VECTOR, dim=self.embedding_dim),
                    FieldSchema(name="metadata", dtype=DataType.VARCHAR, max_length=2048),
                ]
                schema = CollectionSchema(fields, description="Pipeline chunk embeddings")
                self._client = Collection(name=self.collection, schema=schema, using="default", shards_num=1)
            except Exception:  # pragma: no cover - optional dependency
                self._client = MilvusStubClient()
        else:
            self._client = MilvusStubClient()

    def insert_embedding(
        self,
        *,
        use_case: str,
        source_type: str,
        source_id: str,
        pipeline_id: Optional[str],
        pipeline_run_id: Optional[str],
        embedding: List[float],
        metadata: Optional[Dict[str, Any]] = None,
    ) -> None:
        if self._client is None:
            return

        record = {
            "use_case": use_case,
            "source_type": source_type,
            "source_id": source_id,
            "pipeline_id": pipeline_id,
            "pipeline_run_id": pipeline_run_id,
            "embedding": embedding,
            "metadata": json.dumps(metadata or {}),
        }

        if hasattr(self._client, "insert"):
            self._client.insert(record)  # type: ignore[arg-type]
        else:  # pragma: no cover
            self._client.insert([record])

    def sample(self, limit: int = 5) -> List[Dict[str, Any]]:
        if self._client is None:
            return []
        if hasattr(self._client, "query"):
            return self._client.query(limit=limit)
        return []


_milvus_client: Optional[MilvusClient] = None


def get_milvus_client() -> MilvusClient:
    global _milvus_client
    if _milvus_client is None:
        _milvus_client = MilvusClient()
    return _milvus_client
