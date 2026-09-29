# src/python_validation/status_resolver.py
from typing import Dict, Any

class StatusResolver:
    """Calculates overall plan verification status following the SRS state machine."""

    @staticmethod
    def resolve_status(
        coverage_score: float,
        traceability_score: float,
        has_contradictions: bool,
        hallucination_count: int,
        duplicate_count: int,
        missing_count: int
    ) -> str:
        # Precedence order of statuses
        if has_contradictions:
            return "CONTRADICTION_DETECTED"
        if hallucination_count > 0:
            return "UNSUPPORTED"
        if missing_count > 0 or coverage_score < 100.0:
            return "INCOMPLETE"
        if traceability_score < 100.0 or duplicate_count > 0:
            return "VERIFIED_WITH_WARNING"
        if coverage_score >= 100.0 and traceability_score >= 100.0:
            return "VERIFIED"
        return "MANUAL_REVIEW_REQUIRED"
