# src/services/extraction_service.py
import re
from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from src.database import models

class RequirementExtractionService:
    """Extracts, categorizes, and classifies policy requirements from document sections."""

    CATEGORIES = [
        "MUST_KNOW", "MUST_COMPLETE", "MUST_DEMONSTRATE", "MUST_ACKNOWLEDGE",
        "RECOMMENDED", "OPTIONAL", "NOT_APPLICABLE"
    ]

    # Keyword rules for deterministic classification
    CATEGORY_PATTERNS = {
        "MUST_COMPLETE": [r"\bmust complete\b", r"\bmust submit\b", r"\bmust configure\b", r"\bmust enroll\b", r"\bmust report\b", r"\bmust execute\b"],
        "MUST_DEMONSTRATE": [r"\bmust demonstrate\b", r"\bmust verify\b", r"\bmust enforce\b", r"\bmust apply\b", r"\bmust maintain\b", r"\bmust show\b"],
        "MUST_ACKNOWLEDGE": [r"\bmust acknowledge\b", r"\bstrictly prohibited\b", r"\bforbidden\b", r"\bgrounds for termination\b", r"\bzero tolerance\b"],
        "MUST_KNOW": [r"\bmust understand\b", r"\bmust know\b", r"\bmust identify\b", r"\bmust recognize\b", r"\bmust adhere\b"],
        "RECOMMENDED": [r"\brecommended\b", r"\bshould\b", r"\bencouraged\b", r"\bguideline\b", r"\bbest practice\b"],
        "OPTIONAL": [r"\boptional\b", r"\bmay choose\b", r"\beligible for\b", r"\bat discretion\b"]
    }

    @classmethod
    def classify_requirement(cls, text: str) -> Dict[str, Any]:
        """Classifies text into requirement category, mandatory status, and default priority."""
        text_lower = text.lower()
        matched_cat = "MUST_KNOW"
        is_mandatory = True
        priority = "High"
        
        for cat, patterns in cls.CATEGORY_PATTERNS.items():
            for p in patterns:
                if re.search(p, text_lower):
                    matched_cat = cat
                    break
            if matched_cat != "MUST_KNOW":
                break
                
        if matched_cat in ["RECOMMENDED", "OPTIONAL", "NOT_APPLICABLE"]:
            is_mandatory = False
            priority = "Medium" if matched_cat == "RECOMMENDED" else "Low"
        elif "critical" in text_lower or "immediate" in text_lower or "termination" in text_lower:
            priority = "Critical"
            
        return {
            "category": matched_cat,
            "is_mandatory": is_mandatory,
            "priority": priority,
            "confidence": 0.94 if matched_cat in ["MUST_ACKNOWLEDGE", "MUST_COMPLETE"] else 0.88
        }

    @classmethod
    def extract_from_chunk(cls, db: Session, chunk: models.DocumentChunk, doc: models.Document, ver: models.DocumentVersion) -> List[models.Requirement]:
        """Extracts individual sentences as candidate requirements and stores them."""
        sentences = re.split(r'(?<=[.!?])\s+', chunk.content.strip())
        extracted = []
        
        for idx, s in enumerate(sentences):
            s_clean = s.strip()
            if len(s_clean.split()) < 5:
                continue
                
            # Filter for sentences that contain normative modal verbs
            if any(w in s_clean.lower() for w in ["must", "required", "prohibited", "should", "shall", "mandatory", "forbidden"]):
                classification = cls.classify_requirement(s_clean)
                req_code = f"REQ-EXT-{doc.doc_code}-{chunk.section_id}-{idx+1}"
                
                # Check for existing
                existing = db.query(models.Requirement).filter(models.Requirement.req_code == req_code).first()
                if not existing:
                    req_obj = models.Requirement(
                        req_code=req_code,
                        document_id=doc.id,
                        version_id=ver.id,
                        section_id=chunk.section_id,
                        requirement_text=s_clean,
                        category=classification["category"],
                        is_mandatory=classification["is_mandatory"],
                        competency=chunk.section_heading or "Operational Standard",
                        default_priority=classification["priority"],
                        default_due_stage="Week 1"
                    )
                    db.add(req_obj)
                    extracted.append(req_obj)
                    
        db.commit()
        return extracted
