"""Basic data minimization helpers for the interview demo."""

import re


_EMAIL_PATTERN = re.compile(
    r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b",
    re.IGNORECASE,
)
_IBAN_PATTERN = re.compile(
    r"\b[A-Z]{2}\d{2}(?:[ -]?[A-Z0-9]){11,30}\b",
    re.IGNORECASE,
)
_ID_PATTERN = re.compile(
    r"\b(?:\d{8}|[XYZ]\d{7})[- ]?[A-Z]\b",
    re.IGNORECASE,
)
_PHONE_PATTERN = re.compile(
    r"(?<!\w)\+?(?:\d[ .()-]?){8,14}\d(?!\w)",
)


def sanitize_text(text: str) -> str:
    """Minimize direct identifiers without claiming full anonymization."""

    sanitized = _EMAIL_PATTERN.sub("[EMAIL]", text)
    sanitized = _IBAN_PATTERN.sub("[IBAN]", sanitized)
    sanitized = _ID_PATTERN.sub("[ID]", sanitized)
    return _PHONE_PATTERN.sub("[PHONE]", sanitized)
