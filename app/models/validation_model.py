import uuid
from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, JSON, String

from .base import Base, GUID


class ValidationRuleSet(Base):
    __tablename__ = "validation_rulesets"

    id = Column(GUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, unique=True, nullable=False)
    use_case = Column(String, nullable=False)
    description = Column(String)
    config = Column(JSON, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)
