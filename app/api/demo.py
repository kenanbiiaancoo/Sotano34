"""Local demo API routes."""

from fastapi import APIRouter, HTTPException, Request, status

from app.core.config import Settings
from app.models.analysis import DemoMessageRequest, DemoMessageResponse
from app.services.analysis import get_analysis_provider
from app.services.privacy import sanitize_text


router = APIRouter(tags=["demo"])


@router.post(
    "/api/demo/messages",
    response_model=DemoMessageResponse,
    status_code=status.HTTP_200_OK,
)
def analyze_demo_message(
    message: DemoMessageRequest,
    request: Request,
) -> DemoMessageResponse:
    """Analyze one local demo message through the configured provider."""

    sanitized_text = sanitize_text(message.text)
    try:
        settings: Settings = request.app.state.settings
        provider = get_analysis_provider(settings)
        analysis = provider.analyze(sanitized_text)
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="The analysis service is temporarily unavailable.",
        ) from exc

    return DemoMessageResponse(
        provider=provider.provider_name,
        sanitized_text=sanitized_text,
        analysis=analysis,
    )
