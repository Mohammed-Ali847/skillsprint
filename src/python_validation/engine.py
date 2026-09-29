# src/python_validation/engine.py
import json, datetime
from typing import Dict, Any
from sqlalchemy.orm import Session
from src.database import models
from src.python_validation.coverage_validator import CoverageValidator
from src.python_validation.traceability_validator import TraceabilityValidator
from src.python_validation.duplicate_detector import DuplicateDetector
from src.python_validation.role_relevance_validator import RoleRelevanceValidator
from src.python_validation.sequence_validator import SequenceValidator
from src.python_validation.status_resolver import StatusResolver
from src.hallucination_checks.detector import HallucinationDetector
from src.contradiction_checks.detector import ContradictionDetector
from src.comparison_engine.comparator import ComparisonEngine

class PythonValidationEngine:
    """Master Pipeline 2 Engine: Orchestrates independent deterministic Python ground-truth validation."""

    @classmethod
    def validate_plan(cls, db: Session, plan_id: int, plan_dict: Dict[str, Any], role_id: int) -> Dict[str, Any]:
        # 1. Run all sub-validators
        cov_res = CoverageValidator.validate_plan_coverage(db, role_id, plan_dict)
        trace_res = TraceabilityValidator.validate_plan_traceability(db, plan_dict)
        halluc_res = HallucinationDetector.check_plan_grounding(db, plan_dict)
        contra_res = ContradictionDetector.scan_plan_contradictions(db, plan_dict)
        dup_res = DuplicateDetector.check_duplicates(plan_dict)
        role_res = RoleRelevanceValidator.validate_role_relevance(db, role_id, plan_dict)
        seq_res = SequenceValidator.validate_learning_sequence(plan_dict)
        
        # 2. Run GenAI vs Python Comparison Matrix (100+ rows)
        comparison_matrix = ComparisonEngine.generate_comparison_matrix(db, role_id, plan_dict)

        # 3. Resolve Overall Status
        overall_status = StatusResolver.resolve_status(
            coverage_score=cov_res["coverage_score"],
            traceability_score=trace_res["traceability_score"],
            has_contradictions=contra_res["has_contradictions"],
            hallucination_count=halluc_res["hallucination_count"],
            duplicate_count=dup_res["duplicate_count"],
            missing_count=cov_res["missing_count"]
        )

        # 4. Consistency score calculation
        consistency_score = 100.0
        if cov_res["missing_count"] > 0:
            consistency_score -= min(cov_res["missing_count"] * 2.0, 30.0)
        if contra_res["contradiction_count"] > 0:
            consistency_score -= min(contra_res["contradiction_count"] * 15.0, 40.0)
        consistency_score = max(round(consistency_score, 1), 0.0)

        # 5. Persist ValidationResult in Database
        val_result = models.ValidationResult(
            plan_id=plan_id,
            run_at=datetime.datetime.utcnow(),
            coverage_score=cov_res["coverage_score"],
            traceability_score=trace_res["traceability_score"],
            consistency_score=consistency_score,
            missing_req_count=cov_res["missing_count"],
            unsupported_count=trace_res["unsupported_count"] + halluc_res["hallucination_count"],
            contradiction_count=contra_res["contradiction_count"],
            duplicate_count=dup_res["duplicate_count"],
            details_json=json.dumps({
                "coverage": cov_res,
                "traceability": trace_res,
                "hallucinations": halluc_res,
                "contradictions": contra_res,
                "duplicates": dup_res,
                "role_relevance": role_res,
                "sequence": seq_res
            }),
            comparison_json=json.dumps(comparison_matrix),
            overall_status=overall_status
        )
        db.add(val_result)

        # Update OnboardingPlan record
        plan_obj = db.query(models.OnboardingPlan).filter(models.OnboardingPlan.id == plan_id).first()
        if plan_obj:
            plan_obj.status = overall_status
            plan_obj.coverage_score = cov_res["coverage_score"]
            plan_obj.traceability_score = trace_res["traceability_score"]
            plan_obj.consistency_score = consistency_score
            
        db.commit()
        db.refresh(val_result)

        return {
            "validation_id": val_result.id,
            "overall_status": overall_status,
            "coverage_score": cov_res["coverage_score"],
            "traceability_score": trace_res["traceability_score"],
            "consistency_score": consistency_score,
            "missing_req_count": cov_res["missing_count"],
            "unsupported_count": trace_res["unsupported_count"] + halluc_res["hallucination_count"],
            "contradiction_count": contra_res["contradiction_count"],
            "duplicate_count": dup_res["duplicate_count"],
            "comparison_matrix_length": len(comparison_matrix),
            "details": {
                "coverage": cov_res,
                "traceability": trace_res,
                "hallucinations": halluc_res,
                "contradictions": contra_res,
                "duplicates": dup_res,
                "role_relevance": role_res,
                "sequence": seq_res
            }
        }
