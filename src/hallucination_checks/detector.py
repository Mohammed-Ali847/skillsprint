# src/hallucination_checks/detector.py
import re
from typing import Dict, Any, List, Set
from sqlalchemy.orm import Session
from src.database import models

class HallucinationDetector:
    """Algorithmic factual claim validator checking text grounding against source chunks."""

    STOPWORDS = {
        "the", "and", "for", "with", "that", "this", "from", "must", "shall", "should",
        "have", "will", "are", "all", "each", "any", "not", "under", "per", "their", "into",
        "ensure", "compliance", "master", "key", "guidelines", "regarding", "demonstrate",
        "policy", "rule", "standard", "corporate", "operational", "untitled", "module"
    }

    @classmethod
    def extract_salient_tokens(cls, text: str) -> Set[str]:
        words = re.findall(r'\b[A-Za-z0-9\$\%]{3,}\b', text.lower())
        return {w for w in words if w not in cls.STOPWORDS}

    @classmethod
    def check_plan_grounding(cls, db: Session, plan_dict: Dict[str, Any]) -> Dict[str, Any]:
        hallucination_flags = []
        checked_count = 0

        # Load all active chunks by (doc_code, section_id)
        chunks = db.query(models.DocumentChunk).join(models.DocumentVersion).join(models.Document).filter(
            models.DocumentVersion.is_active == True
        ).all()
        chunk_text_lookup = {}
        for c in chunks:
            key = (c.version.document.doc_code, c.section_id)
            chunk_text_lookup[key] = c.content

        for m in plan_dict.get("modules", []):
            checked_count += 1
            doc_id = m.get("source_doc_id", "")
            sec_id = m.get("source_section_id", "")
            title = m.get("title", "")
            m_code = m.get("module_code", "")

            source_text = chunk_text_lookup.get((doc_id, sec_id))
            if not source_text:
                # If section isn't found in active documents, flag as missing source support
                hallucination_flags.append({
                    "module_code": m_code,
                    "title": title,
                    "source_doc_id": doc_id,
                    "source_section_id": sec_id,
                    "reason": f"Cited section '{sec_id}' does not exist in active approved document '{doc_id}'."
                })
                continue

            source_tokens = cls.extract_salient_tokens(source_text)
            title_tokens = cls.extract_salient_tokens(title)

            # Check if title has any grounding in the source section
            if title_tokens:
                overlap = title_tokens.intersection(source_tokens)
                # If zero salient tokens from the title appear in the source chunk, flag as hallucination
                if len(overlap) == 0:
                    hallucination_flags.append({
                        "module_code": m_code,
                        "title": title,
                        "source_doc_id": doc_id,
                        "source_section_id": sec_id,
                        "overlap_count": 0,
                        "reason": f"Module title has no factual grounding in cited {doc_id} Section {sec_id}."
                    })

        return {
            "items_checked": checked_count,
            "hallucination_count": len(hallucination_flags),
            "hallucination_flags": hallucination_flags,
            "is_clean": len(hallucination_flags) == 0
        }
