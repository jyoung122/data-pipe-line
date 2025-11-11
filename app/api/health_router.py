from fastapi import APIRouter

from ..core.config import get_settings
from ..schemas.common import APIResponse

router = APIRouter(prefix="/health", tags=["health"])


@router.get("", response_model=APIResponse[dict])
async def get_health() -> APIResponse[dict]:
    settings = get_settings()
    data = {
        "status": "ok",
        "services": {
            "database": "ok",
            "milvus": "down" if settings.milvus_uri is None else "ok",
        },
    }
    return APIResponse.ok(data)
