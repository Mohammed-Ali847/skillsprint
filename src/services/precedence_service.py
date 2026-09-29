# src/services/precedence_service.py
from typing import Dict, Any, Tuple
from sqlalchemy.orm import Session
from src.database import models

class PrecedenceService:
    """Deterministic policy precedence hierarchy resolver.
    Hierarchy:
      Level 1: Latest Approved Corporate Policy (DOC-POL-*)
      Level 2: Standard Operating Procedure (DOC-SOP-*)
      Level 3: Frequently Asked Questions (DOC-FAQ-*)
      Level 4: Informal Guidance & General Handbook (DOC-HDB-*)
    """

    PRECEDENCE_RANKS = {
        "POLICY": 1,
        "SOP": 2,
        "FAQ": 3,
        "HANDBOOK": 4,
        "GUIDANCE": 4
    }

    @classmethod
    def resolve_conflict(cls, doc_a: models.Document, ver_a: models.DocumentVersion,
                         doc_b: models.Document, ver_b: models.DocumentVersion) -> Tuple[models.Document, models.DocumentVersion, str]:
        """Determines which document version takes precedence when a contradiction arises."""
        rank_a = ver_a.precedence_level or cls.PRECEDENCE_RANKS.get(doc_a.doc_type, 3)
        rank_b = ver_b.precedence_level or cls.PRECEDENCE_RANKS.get(doc_b.doc_type, 3)

        # Lower numeric value indicates higher authority (1 beats 2, 2 beats 3)
        if rank_a < rank_b:
            rationale = f"{doc_a.doc_type} ({doc_a.doc_code}) has higher authority rank ({rank_a}) than {doc_b.doc_type} ({doc_b.doc_code}, rank {rank_b})."
            return doc_a, ver_a, rationale
        elif rank_b < rank_a:
            rationale = f"{doc_b.doc_type} ({doc_b.doc_code}) has higher authority rank ({rank_b}) than {doc_a.doc_type} ({doc_a.doc_code}, rank {rank_a})."
            return doc_b, ver_b, rationale
        else:
            # Same authority rank: check version effective dates
            if ver_a.effective_date >= ver_b.effective_date:
                rationale = f"Both are {doc_a.doc_type}, but version {ver_a.version_str} ({ver_a.effective_date.date()}) is newer than version {ver_b.version_str} ({ver_b.effective_date.date()})."
                return doc_a, ver_a, rationale
            else:
                rationale = f"Both are {doc_b.doc_type}, but version {ver_b.version_str} ({ver_b.effective_date.date()}) is newer than version {ver_a.version_str} ({ver_a.effective_date.date()})."
                return doc_b, ver_b, rationale
