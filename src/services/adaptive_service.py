# src/services/adaptive_service.py
import datetime
from typing import Dict, Any, List
from sqlalchemy.orm import Session
from src.database import models

class AdaptiveService:
    """Identifies employee weak areas and synthesizes targeted adaptive learning recommendations."""

    @classmethod
    def generate_remediation(cls, db: Session, employee_id: int, module: models.LearningModule, score: float):
        weak_topic = module.requirement.competency if (module and module.requirement) else (module.title if module else "Core Standard")
        
        reason = f"Learner scored {score}% (below 75% threshold) on quiz for '{module.title if module else 'module'}'. Immediate remediation recommended."
        
        # Check if recommendation already active
        existing = db.query(models.AdaptiveRecommendation).filter(
            models.AdaptiveRecommendation.employee_id == employee_id,
            models.AdaptiveRecommendation.weak_topic == weak_topic,
            models.AdaptiveRecommendation.status == "ACTIVE"
        ).first()

        if not existing:
            rec = models.AdaptiveRecommendation(
                employee_id=employee_id,
                reason=reason,
                weak_topic=weak_topic,
                recommended_module_id=module.id if module else None,
                recommendation_type="REVISION_MODULE" if score >= 50.0 else "MANAGER_REVIEW",
                status="ACTIVE",
                created_at=datetime.datetime.utcnow()
            )
            db.add(rec)
            db.commit()

    @classmethod
    def get_employee_recommendations(cls, db: Session, employee_id: int) -> List[Dict[str, Any]]:
        recs = db.query(models.AdaptiveRecommendation).filter(
            models.AdaptiveRecommendation.employee_id == employee_id
        ).order_by(models.AdaptiveRecommendation.created_at.desc()).all()

        results = []
        for r in recs:
            results.append({
                "id": r.id,
                "weak_topic": r.weak_topic,
                "reason": r.reason,
                "recommendation_type": r.recommendation_type,
                "status": r.status,
                "module_title": r.recommended_module.title if r.recommended_module else "General Policy",
                "created_at": r.created_at.isoformat() if r.created_at else None
            })
        return results
