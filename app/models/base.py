from sqlalchemy import types
from sqlalchemy.dialects.postgresql import UUID as PGUUID  # type: ignore
from sqlalchemy.orm import declarative_base


Base = declarative_base()


try:  # SQLAlchemy 2.0 provides a portable UUID type
    GUID = types.UUID
except AttributeError:  # pragma: no cover - legacy fallback
    class GUID(PGUUID):
        pass
