"""Tests for the health-check API and generated FastAPI interfaces."""

from fastapi.testclient import TestClient

from app.main import create_app


def test_healthcheck() -> None:
    """The liveness endpoint returns the exact documented response."""

    with TestClient(create_app()) as client:
        response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_fastapi_generated_interfaces() -> None:
    """FastAPI exposes its documentation and the health OpenAPI operation."""

    with TestClient(create_app()) as client:
        docs_response = client.get("/docs")
        openapi_response = client.get("/openapi.json")

    assert docs_response.status_code == 200
    assert openapi_response.status_code == 200
    assert "/health" in openapi_response.json()["paths"]
