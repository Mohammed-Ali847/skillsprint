# src/security/prompt_defense.py
import re
from typing import Tuple

class PromptDefense:
    """Isolates untrusted document text and sanitizes inputs to neutralize prompt injection."""

    BOUNDARY_START = "<UNTRUSTED_COMPANY_DOCUMENT_DATA>"
    BOUNDARY_END = "</UNTRUSTED_COMPANY_DOCUMENT_DATA>"

    @classmethod
    def wrap_evidence(cls, text: str) -> str:
        """Wraps source content in explicit isolation boundary tags and strips injection escapes."""
        sanitized = text.replace("</UNTRUSTED_COMPANY_DOCUMENT_DATA>", "[STRIPPED_CLOSING_TAG]")
        sanitized = sanitized.replace("<system>", "[STRIPPED_SYSTEM_TAG]").replace("</system>", "[STRIPPED_SYSTEM_TAG]")
        return f"{cls.BOUNDARY_START}\n{sanitized}\n{cls.BOUNDARY_END}"

    @classmethod
    def sanitize_user_input(cls, user_text: str) -> str:
        """Sanitizes user profile or prompt fields."""
        cleaned = re.sub(r'[\r\n]+', ' ', user_text)
        return cleaned.strip()
