"""Tests for the local demo workflow."""

from fastapi.testclient import TestClient

from app.core.config import Settings
from app.main import create_app
from app.services.privacy import sanitize_text


CLINIC_MESSAGE = (
    "Hola, soy Marta de Clínica Ejemplo. Somos 12 empleados y tratamos datos "
    "de pacientes. Tenemos web con formulario de citas y nunca hemos hecho una "
    "revisión completa de protección de datos. Mi email es marta@example.com y "
    "mi teléfono es +34 612 345 678."
)


def test_privacy_minimizes_contact_identifiers() -> None:
    """The basic privacy layer replaces the four supported identifier types."""

    original = (
        "Contacta con marta@example.com o +34 612 345 678. "
        "DNI 12345678Z e IBAN ES91 2100 0418 4502 0005 1332."
    )

    sanitized = sanitize_text(original)

    assert "[EMAIL]" in sanitized
    assert "[PHONE]" in sanitized
    assert "[ID]" in sanitized
    assert "[IBAN]" in sanitized
    assert "marta@example.com" not in sanitized
    assert "+34 612 345 678" not in sanitized


def test_mock_demo_returns_structured_completed_case() -> None:
    """The complete clinic example returns the public contract from mock mode."""

    settings = Settings(demo_mode=True, _env_file=None)
    approved_ids = {
        "rgpd_lopdgdd_consulting",
        "risk_audit_eipd",
        "web_privacy_lssi",
    }

    with TestClient(create_app(settings)) as client:
        response = client.post(
            "/api/demo/messages",
            json={"text": CLINIC_MESSAGE},
        )

    assert response.status_code == 200
    body = response.json()
    assert body["provider"] == "mock"
    assert body["analysis"]["status"] == "completed"
    assert body["analysis"]["recommended_atico34_services"]
    assert any(
        recommendation["service_id"] in approved_ids
        for recommendation in body["analysis"]["recommended_atico34_services"]
    )
    assert "marta@example.com" not in body["sanitized_text"]
    assert "+34 612 345 678" not in body["sanitized_text"]


def test_dashboard_is_served() -> None:
    """The root route serves the static Legal Intake AI dashboard."""

    settings = Settings(demo_mode=True, _env_file=None)

    with TestClient(create_app(settings)) as client:
        response = client.get("/")

    assert response.status_code == 200
    assert "Legal Intake AI" in response.text
