"""Application liveness endpoint."""

from typing import Literal

from fastapi import APIRouter, status
from pydantic import BaseModel


class HealthResponse(BaseModel):
    """Response returned when the application is running."""

    status: Literal["ok"] = "ok"


router = APIRouter(tags=["system"])


@router.get(
    "/health",
    response_model=HealthResponse,
    status_code=status.HTTP_200_OK,
)
async def healthcheck() -> HealthResponse:
    """Report application liveness without checking external dependencies."""

    return HealthResponse()
