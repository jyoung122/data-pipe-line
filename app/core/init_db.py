from ..models import document_model  # noqa: F401
from ..models import foia_model  # noqa: F401
from ..models import invoice_model  # noqa: F401
from ..models import pipeline_model  # noqa: F401
from ..models import staging_model  # noqa: F401
from ..models import validation_model  # noqa: F401
from ..models.base import Base
from .db import sync_engine


def create_all_tables() -> None:
    Base.metadata.create_all(bind=sync_engine)
