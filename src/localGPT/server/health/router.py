from typing import Literal

from fastapi import APIRouter
from pydantic import BaseModel, Field

health_router = APIRouter()


class HealthResponse(BaseModel):
    """
    Represents the response for the health check endpoint.

    Attributes:
        status (Literal["ok"]): The status of the health check. Default value is "ok".
    """

    status: Literal["ok"] = Field(default="ok")


@health_router.get("/health", tags=["health"])
def health() -> HealthResponse:
    """
    Returns the health status of the server.

    Returns:
        HealthResponse: HealthResponse object with status "ok"
    """
    return HealthResponse(status="ok")
