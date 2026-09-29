# src/reports/report_generator.py
import datetime
from typing import Dict, Any, List
from sqlalchemy.orm import Session
from src.database import models

class ReportGenerator:
    """Aggregates enterprise compliance, coverage, progress, and validation telemetry into structured reports."""

    @classmethod
    def generate_compliance_report(cls, db: Session) -> Dict[str, Any]:
        employees = db.query(models.Employee).all()
        plans = db.query(models.OnboardingPlan).all()
        roles = db.query(models.Role).all()

        total_employees = len(employees)
        verified_plans = len([p for p in plans if p.status in ["VERIFIED", "APPROVED"]])
        flagged_plans = len([p for p in plans if p.status in ["UNSUPPORTED", "CONTRADICTION_DETECTED", "INCOMPLETE"]])

        avg_coverage = round(sum(p.coverage_score for p in plans) / max(len(plans), 1), 1)
        avg_traceability = round(sum(p.traceability_score for p in plans) / max(len(plans), 1), 1)

        role_stats = []
        for r in roles:
            r_emps = [e for e in employees if e.role_id == r.id]
            role_stats.append({
                "role_code": r.code,
                "role_name": r.name,
                "headcount": len(r_emps),
                "mandatory_req_count": len([rr for rr in r.role_requirements if rr.is_mandatory])
            })

        return {
            "report_name": "Executive Onboarding Compliance & Verification Audit Report",
            "generated_at": datetime.datetime.utcnow().isoformat(),
            "summary": {
                "total_employees": total_employees,
                "total_onboarding_plans": len(plans),
                "verified_plans": verified_plans,
                "flagged_plans_requiring_review": flagged_plans,
                "average_mandatory_coverage": avg_coverage,
                "average_source_traceability": avg_traceability
            },
            "role_breakdown": role_stats,
            "recent_plans": [
                {
                    "plan_id": p.id,
                    "employee": p.employee.full_name if p.employee else "N/A",
                    "role": p.role.name if p.role else "N/A",
                    "status": p.status,
                    "coverage_score": p.coverage_score,
                    "traceability_score": p.traceability_score
                } for p in plans[:10]
            ]
        }
