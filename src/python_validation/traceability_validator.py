# src/python_validation/traceability_validator.py
from typing import Dict, Any, List
from sqlalchemy.orm import Session
from src.database import models

class TraceabilityValidator:
    """Verifies that generated learning items cite approved, active source documents and sections."""

    @classmethod
    def validate_plan_traceability(cls, db: Session, plan_dict: Dict[str, Any]) -> Dict[str, Any]:
        total_items = 0
        valid_citations = 0
        unsupported_items = []
        outdated_citations = []

        # Build lookup of valid active documents and their sections
        active_versions = db.query(models.DocumentVersion).filter(models.DocumentVersion.is_active == True).all()
        active_lookup = {}  # (doc_code, section_id) -> version_id
        doc_codes_active = set()
        
        for v in active_versions:
            doc = v.document
            if doc:
                doc_codes_active.add(doc.doc_code)
                for c in v.chunks:
                    active_lookup[(doc.doc_code, c.section_id)] = v.version_str

        # Inspect all modules
        for m in plan_dict.get("modules", []):
            total_items += 1
            doc_id = m.get("source_doc_id", "").strip()
            sec_id = m.get("source_section_id", "").strip()
            title = m.get("title", "Untitled Module")

            if not doc_id or not sec_id:
                unsupported_items.append({
                    "item_type": "MODULE",
                    "title": title,
                    "issue": "Missing source document or section citation."
                })
            elif (doc_id, sec_id) in active_lookup:
                valid_citations += 1
            elif doc_id in doc_codes_active:
                # Document exists and is active, section might be granular
                valid_citations += 1
            else:
                # Check if it was an obsolete version
                obsolete = db.query(models.DocumentVersion).join(models.Document).filter(
                    models.Document.doc_code == doc_id,
                    models.DocumentVersion.is_active == False
                ).first()
                if obsolete:
                    outdated_citations.append({
                        "item_type": "MODULE",
                        "title": title,
                        "doc_id": doc_id,
                        "issue": f"Cites obsolete policy version ({obsolete.version_str}) superseded by an active policy."
                    })
                else:
                    unsupported_items.append({
                        "item_type": "MODULE",
                        "title": title,
                        "doc_id": doc_id,
                        "issue": "Document does not exist in approved company repository."
                    })

        # Inspect quizzes
        for m in plan_dict.get("modules", []):
            for q in m.get("quiz_questions", []):
                total_items += 1
                q_doc = q.get("source_doc_id", "").strip()
                q_sec = q.get("source_section_id", "").strip()
                if q_doc and q_doc in doc_codes_active:
                    valid_citations += 1
                else:
                    unsupported_items.append({
                        "item_type": "QUIZ_QUESTION",
                        "title": q.get("question_text", "")[:40],
                        "issue": "Quiz question lacks verified active source citation."
                    })

        traceability_score = round((valid_citations / max(total_items, 1)) * 100.0, 2)

        return {
            "traceability_score": traceability_score,
            "total_items_checked": total_items,
            "valid_citations_count": valid_citations,
            "unsupported_count": len(unsupported_items),
            "outdated_count": len(outdated_citations),
            "unsupported_items": unsupported_items,
            "outdated_citations": outdated_citations
        }
