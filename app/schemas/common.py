from typing import Generic, Optional, TypeVar

from pydantic import BaseModel

T = TypeVar("T")


class APIResponse(BaseModel, Generic[T]):
    success: bool
    data: Optional[T]
    error: Optional[str]

    @classmethod
    def ok(cls, data: Optional[T] = None) -> "APIResponse[T]":
        return cls(success=True, data=data, error=None)

    @classmethod
    def fail(cls, message: str) -> "APIResponse[T]":
        return cls(success=False, data=None, error=message)
