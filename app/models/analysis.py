"""Structured contracts for the reduced demo workflow."""

from typing import Literal

from pydantic import BaseModel, Field


class DemoMessageRequest(BaseModel):
    """Message submitted through the local demo form."""

    text: str = Field(min_length=20, max_length=5000)


class ServiceRecommendation(BaseModel):
    """An Ático34 service recommended for the submitted case."""

    service_id: str
    service_name: str
    rationale: str


class CaseAnalysis(BaseModel):
    """Structured preliminary analysis of a submitted case."""

    status: Literal["completed", "needs_info", "human_review"]
    case_summary: str
    case_category: str
    urgency: Literal["low", "normal", "high"]
    preliminary_diagnosis: str
    possible_solution: str
    recommended_atico34_services: list[ServiceRecommendation]
    missing_information: list[str]
    next_questions: list[str]
    requires_human_review: bool


class DemoMessageResponse(BaseModel):
    """API response containing the sanitized input and its analysis."""

    provider: Literal["mock", "gemini"]
    sanitized_text: str
    analysis: CaseAnalysis
