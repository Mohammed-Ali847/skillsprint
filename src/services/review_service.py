# src/services/review_service.py
import datetime
from typing import Dict, Any, List, Optional
from sqlalchemy.orm import Session
from src.database import models

class ReviewService:
    """Manages the Reviewer Workflow: triage queue, approval, rejection, edits, overrides, and audit trails."""

    @classmethod
    def get_review_queue(cls, db: Session) -> List[Dict[str, Any]]:
        """Returns all onboarding plans requiring manual review or flagged with warnings/unsupported claims."""
        flagged_plans = db.query(models.OnboardingPlan).filter(
            models.OnboardingPlan.status.in_([
                "UNSUPPORTED", "CONTRADICTION_DETECTED", "INCOMPLETE",
                "MANUAL_REVIEW_REQUIRED", "VERIFIED_WITH_WARNING"
            ])
        ).order_by(models.OnboardingPlan.created_at.desc()).all()

        queue = []
        for p in flagged_plans:
            last_val = db.query(models.ValidationResult).filter(
                models.ValidationResult.plan_id == p.id
            ).order_by(models.ValidationResult.run_at.desc()).first()

            queue.append({
                "plan_id": p.id,
                "title": p.title,
                "employee_code": p.employee.employee_code if p.employee else "N/A",
                "employee_name": p.employee.full_name if p.employee else "N/A",
                "role_name": p.role.name if p.role else "N/A",
                "status": p.status,
                "coverage_score": p.coverage_score,
                "traceability_score": p.traceability_score,
                "consistency_score": p.consistency_score,
                "created_at": p.created_at.isoformat() if p.created_at else None,
                "validation_id": last_val.id if last_val else None,
                "missing_count": last_val.missing_req_count if last_val else 0,
                "unsupported_count": last_val.unsupported_count if last_val else 0,
                "contradiction_count": last_val.contradiction_count if last_val else 0
            })
        return queue

    @classmethod
    def process_decision(
        cls,
        db: Session,
        plan_id: int,
        reviewer_id: int,
        action: str,  # APPROVE, REJECT, EDIT, REGENERATE, OVERRIDE
        notes: str,
        override_status: Optional[str] = None
    ) -> Dict[str, Any]:
        plan = db.query(models.OnboardingPlan).filter(models.OnboardingPlan.id == plan_id).first()
        if not plan:
            raise ValueError(f"Plan {plan_id} not found.")

        original_status = plan.status
        new_status = original_status

        if action == "APPROVE":
            new_status = "APPROVED"
        elif action == "REJECT":
            new_status = "REJECTED"
        elif action == "OVERRIDE":
            if not override_status:
                raise ValueError("Override status is required for override action.")
            new_status = override_status
        elif action == "REGENERATE":
            new_status = "DRAFT"

        plan.status = new_status

        # Create ReviewAction record
        review_record = models.ReviewAction(
            plan_id=plan.id,
            reviewer_id=reviewer_id,
            action=action,
            notes=notes,
            original_status=original_status,
            override_status=new_status,
            created_at=datetime.datetime.utcnow()
        )
        db.add(review_record)

        # Log in immutable AuditLog
        audit_log = models.AuditLog(
            user_id=reviewer_id,
            action=f"REVIEW_{action}",
            entity_type="OnboardingPlan",
            entity_id=str(plan.id),
            payload_before=f"status: {original_status}",
            payload_after=f"status: {new_status} | notes: {notes}",
            timestamp=datetime.datetime.utcnow()
        )
        db.add(audit_log)

        db.commit()
        db.refresh(plan)

        return {
            "plan_id": plan.id,
            "action": action,
            "original_status": original_status,
            "new_status": new_status,
            "notes": notes,
            "timestamp": review_record.created_at.isoformat()
        }
