import uuid
from datetime import datetime

from sqlalchemy import Column, Date, DateTime, Enum, ForeignKey, JSON, String, Text
from sqlalchemy.orm import relationship

from .base import Base, GUID

CONTRACT_STATUSES = ("active", "expired", "terminated")


class Vendor(Base):
    __tablename__ = "vendors"

    id = Column(GUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    external_id = Column(String)
    name = Column(String, nullable=False)
    metadata = Column(JSON)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)

    contracts = relationship("Contract", back_populates="vendor", cascade="all, delete-orphan")


class Contract(Base):
    __tablename__ = "contracts"

    id = Column(GUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    vendor_id = Column(GUID(as_uuid=True), ForeignKey("vendors.id"), nullable=False)
    title = Column(String, nullable=False)
    status = Column(Enum(*CONTRACT_STATUSES, name="contract_status"), nullable=False)
    effective_date = Column(Date)
    expiration_date = Column(Date)
    storage_uri = Column(String)
    raw_text = Column(Text)
    metadata = Column(JSON)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)

    vendor = relationship("Vendor", back_populates="contracts")
