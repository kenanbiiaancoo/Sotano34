"""Mock and Gemini providers for the reduced analysis workflow."""

import re
from typing import Literal, Protocol

from google import genai
from google.genai import types

from app.core.config import Settings
from app.models.analysis import CaseAnalysis, ServiceRecommendation


_SERVICE_ID_PATTERN = re.compile(
    r"^## SERVICE: `([a-z0-9_]+)`\s*$",
    re.MULTILINE,
)


def _load_knowledge(settings: Settings) -> tuple[str, set[str]]:
    """Load controlled knowledge and return its approved service IDs."""

    knowledge_text = settings.atico34_knowledge_path.read_text(encoding="utf-8")
    approved_service_ids = set(_SERVICE_ID_PATTERN.findall(knowledge_text))
    if not approved_service_ids:
        raise ValueError("The knowledge file contains no approved service IDs.")
    return knowledge_text, approved_service_ids


class AnalysisProvider(Protocol):
    """Contract shared by local and external analysis providers."""

    provider_name: Literal["mock", "gemini"]

    def analyze(self, sanitized_text: str) -> CaseAnalysis:
        """Analyze a previously minimized message."""

        ...


class MockAnalysisProvider:
    """Small deterministic provider for the scripted offline demo."""

    provider_name: Literal["mock", "gemini"] = "mock"

    def analyze(self, sanitized_text: str) -> CaseAnalysis:
        """Analyze a minimized message without an external service."""

        normalized_text = sanitized_text.strip()
        if len(normalized_text) <= 80 or len(normalized_text.split()) < 12:
            return CaseAnalysis(
                status="needs_info",
                case_summary="La consulta no contiene contexto suficiente.",
                case_category="other",
                urgency="normal",
                preliminary_diagnosis=(
                    "No es posible realizar un triaje preliminar fiable con "
                    "la información facilitada."
                ),
                possible_solution=(
                    "Solicitar información básica adicional antes de valorar "
                    "servicios o actuaciones."
                ),
                recommended_atico34_services=[],
                missing_information=[
                    "Actividad y sector de la organización.",
                    "Problema concreto u objetivo de la consulta.",
                    "Tipos de datos personales o procesos afectados.",
                ],
                next_questions=[
                    "¿A qué se dedica la organización?",
                    "¿Qué problema concreto necesitan resolver?",
                    "¿Qué datos personales o procesos están implicados?",
                ],
                requires_human_review=False,
            )

        return CaseAnalysis(
            status="completed",
            case_summary=(
                "Clínica de 12 empleados que trata datos de pacientes, dispone "
                "de una web con formulario de citas y necesita una revisión "
                "integral de protección de datos."
            ),
            case_category="data_protection",
            urgency="normal",
            preliminary_diagnosis=(
                "El caso presenta indicios de que conviene revisar la adaptación "
                "al RGPD/LOPDGDD, los riesgos asociados al tratamiento de datos "
                "de pacientes y la información legal del formulario web."
            ),
            possible_solution=(
                "Realizar una revisión profesional del tratamiento de datos, "
                "documentar los riesgos y comprobar los textos y consentimientos "
                "de la web."
            ),
            recommended_atico34_services=[
                ServiceRecommendation(
                    service_id="rgpd_lopdgdd_consulting",
                    service_name="Consultoría / adaptación RGPD y LOPDGDD",
                    rationale=(
                        "La clínica indica que nunca ha realizado una revisión "
                        "completa de protección de datos."
                    ),
                ),
                ServiceRecommendation(
                    service_id="risk_audit_eipd",
                    service_name=(
                        "Auditoría, análisis de riesgos y evaluación de impacto "
                        "(EIPD/DPIA)"
                    ),
                    rationale=(
                        "El tratamiento de datos de pacientes aconseja valorar "
                        "riesgos y la necesidad de una evaluación de impacto."
                    ),
                ),
                ServiceRecommendation(
                    service_id="web_privacy_lssi",
                    service_name=(
                        "Privacidad web / LSSI / textos legales / cookies"
                    ),
                    rationale=(
                        "La web incorpora un formulario de citas que debe revisar "
                        "sus textos, información y consentimientos."
                    ),
                ),
            ],
            missing_information=[],
            next_questions=[],
            requires_human_review=False,
        )


class GeminiAnalysisProvider:
    """Gemini-backed provider using Pydantic structured output."""

    provider_name: Literal["mock", "gemini"] = "gemini"

    def __init__(self, settings: Settings) -> None:
        self._settings = settings
        api_key = settings.gemini_api_key.get_secret_value()
        if not api_key:
            raise ValueError(
                "GEMINI_API_KEY is required when DEMO_MODE is false."
            )
        self._client = genai.Client(api_key=api_key)

    def analyze(self, sanitized_text: str) -> CaseAnalysis:
        """Analyze a minimized message through Gemini."""

        knowledge_text, approved_service_ids = _load_knowledge(self._settings)
        prompt = f"""
You perform preliminary legal-intake triage for an interview demo.
Follow these rules:
- Produce triage and a preliminary diagnosis, never definitive legal advice.
- If information is insufficient, use status "needs_info", recommend no
  services, and return concrete missing information and next questions.
- For ambiguous or high-risk cases, use status "human_review" and explain why
  professional review is required.
- Recommend only service IDs present in the controlled knowledge below.
- Never invent prices, guarantees, legal obligations, or Ático34 services.
- For a completed case, prefer 1 to 3 strongly relevant recommendations.
- Use only the controlled knowledge for company-specific claims.

CONTROLLED ÁTICO34 KNOWLEDGE:
{knowledge_text}

SANITIZED CASE:
{sanitized_text}
""".strip()

        response = self._client.models.generate_content(
            model=self._settings.gemini_model,
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=CaseAnalysis,
            ),
        )
        analysis = response.parsed
        if not isinstance(analysis, CaseAnalysis):
            raise ValueError("Gemini did not return a valid CaseAnalysis.")

        recommended_service_ids = {
            recommendation.service_id
            for recommendation in analysis.recommended_atico34_services
        }
        unknown_service_ids = recommended_service_ids - approved_service_ids
        if unknown_service_ids:
            unknown_ids = ", ".join(sorted(unknown_service_ids))
            raise ValueError(
                f"Gemini returned unknown Ático34 service IDs: {unknown_ids}."
            )
        return analysis


def get_analysis_provider(settings: Settings) -> AnalysisProvider:
    """Select the provider configured for the current application."""

    if settings.demo_mode:
        return MockAnalysisProvider()
    return GeminiAnalysisProvider(settings)
