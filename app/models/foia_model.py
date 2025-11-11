import uuid
from datetime import datetime

from sqlalchemy import Column, DateTime, JSON, String, Text

from .base import Base, GUID


class FOIAKnowledgeSource(Base):
    __tablename__ = "foia_knowledge_sources"

    id = Column(GUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String, nullable=False)
    category = Column(String, nullable=False)
    storage_uri = Column(String)
    raw_text = Column(Text)
    metadata = Column(JSON)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)
