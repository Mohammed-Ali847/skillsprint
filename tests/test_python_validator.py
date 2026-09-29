import pytest
from src.database import models
from src.python_validation.coverage_validator import CoverageValidator
from src.python_validation.traceability_validator import TraceabilityValidator
from src.hallucination_checks.detector import HallucinationDetector
from src.contradiction_checks.detector import ContradictionDetector
from src.python_validation.duplicate_detector import DuplicateDetector
from src.python_validation.role_relevance_validator import RoleRelevanceValidator
from src.python_validation.sequence_validator import SequenceValidator
from src.python_validation.status_resolver import StatusResolver
from src.comparison_engine.comparator import ComparisonEngine
from src.python_validation.engine import PythonValidationEngine

def test_coverage_validator_calculation(db_session):
    role = db_session.query(models.Role).first()
    assert role is not None

    role_reqs = db_session.query(models.RoleRequirement).filter(
        models.RoleRequirement.role_id == role.id,
        models.RoleRequirement.is_mandatory == True
    ).all()
    assert len(role_reqs) > 0

    # Pick first 2 mandatory requirements
    first_two_codes = [rr.requirement.req_code for rr in role_reqs[:2] if rr.requirement]

    plan_dict = {
        "modules": [
            {"requirement_code": first_two_codes[0], "title": "Module 1", "source_doc_id": "DOC-POL-01", "source_section_id": "1.0"},
            {"requirement_code": first_two_codes[1], "title": "Module 2", "source_doc_id": "DOC-POL-01", "source_section_id": "1.0"},
        ],
        "checklists": []
    }

    result = CoverageValidator.validate_plan_coverage(db_session, role.id, plan_dict)
    assert result["total_mandatory"] == len(role_reqs)
    assert result["covered_count"] == 2
    expected_score = round((2 / len(role_reqs)) * 100.0, 2)
    assert result["coverage_score"] == expected_score
    assert result["missing_count"] == len(role_reqs) - 2

def test_traceability_validator(db_session):
    plan_dict = {
        "modules": [
            {
                "title": "Clean Active Module",
                "source_doc_id": "DOC-POL-01",
                "source_section_id": "1.1",
                "quiz_questions": []
            },
            {
                "title": "Unsupported Ghost Document",
                "source_doc_id": "DOC-GHOST-99",
                "source_section_id": "99.9",
                "quiz_questions": []
            }
        ]
    }
    result = TraceabilityValidator.validate_plan_traceability(db_session, plan_dict)
    assert result["total_items_checked"] == 2
    assert result["valid_citations_count"] >= 1
    assert result["unsupported_count"] >= 1
    assert result["traceability_score"] < 100.0

def test_hallucination_detector_tokens():
    tokens = HallucinationDetector.extract_salient_tokens("Employees must strictly rotate their credentials every 90 days")
    assert "rotate" in tokens
    assert "credentials" in tokens
    assert "the" not in tokens
    assert "must" not in tokens

def test_contradiction_detector_known_benchmarks(db_session):
    contradictory_plan = {
        "modules": [
            {
                "module_code": "MOD-TEST-01",
                "title": "Password Lifecycle",
                "purpose": "Users must rotate credentials every 180 days according to legacy rules.",
                "learning_objectives": ["Understand 180 days password rotation"],
                "quiz_questions": []
            },
            {
                "module_code": "MOD-TEST-02",
                "title": "Support Refund Policy",
                "purpose": "Support agents can directly issue $500 refunds without tier 2 signoff.",
                "learning_objectives": ["Process $500 refunds quickly"],
                "quiz_questions": []
            }
        ]
    }
    result = ContradictionDetector.scan_plan_contradictions(db_session, contradictory_plan)
    assert result["has_contradictions"] is True
    assert result["contradiction_count"] >= 2
    contra_ids = [c["contradiction_id"] for c in result["contradictions"]]
    assert "CONT-001" in contra_ids
    assert "CONT-002" in contra_ids

def test_contradiction_detector_clean_plan(db_session):
    clean_plan = {
        "modules": [
            {
                "module_code": "MOD-CLEAN-01",
                "title": "Password Rotation Rules",
                "purpose": "Passwords must be changed every 90 days using MFA.",
                "learning_objectives": ["Comply with 90-day password rotation"],
                "quiz_questions": []
            }
        ]
    }
    result = ContradictionDetector.scan_plan_contradictions(db_session, clean_plan)
    assert result["has_contradictions"] is False
    assert result["contradiction_count"] == 0

def test_sequence_validator():
    # Module 2 depends on Module 1, but Module 2 is scheduled in Week 1 while Module 1 is scheduled in First 30 Days
    invalid_plan = {
        "modules": [
            {"module_code": "MOD-2", "stage": "Week 1", "prerequisite_module_code": "MOD-1", "difficulty": "Intermediate"},
            {"module_code": "MOD-1", "stage": "First 30 Days", "difficulty": "Beginner"},
        ]
    }
    result = SequenceValidator.validate_learning_sequence(invalid_plan)
    assert result["is_valid_sequence"] is False
    assert result["sequence_issue_count"] >= 1
    assert result["sequence_issues"][0]["type"] == "INVALID_PREREQUISITE_SEQUENCE"

def test_duplicate_detector():
    plan_with_dups = {
        "modules": [
            {"module_code": "MOD-1", "requirement_code": "REQ-SEC-001", "title": "Security Training"},
            {"module_code": "MOD-2", "requirement_code": "REQ-SEC-001", "title": "Security Training"},
        ]
    }
    result = DuplicateDetector.check_duplicates(plan_with_dups)
    assert result["has_duplicates"] is True
    assert result["duplicate_count"] >= 1

def test_status_resolver_states():
    # Contradiction detected
    status1 = StatusResolver.resolve_status(
        coverage_score=100.0, traceability_score=100.0,
        has_contradictions=True, hallucination_count=0, duplicate_count=0, missing_count=0
    )
    assert status1 == "CONTRADICTION_DETECTED"

    # Incomplete
    status2 = StatusResolver.resolve_status(
        coverage_score=60.0, traceability_score=100.0,
        has_contradictions=False, hallucination_count=0, duplicate_count=0, missing_count=8
    )
    assert status2 == "INCOMPLETE"

    # Verified with Warning (Traceability < 100%)
    status_warn = StatusResolver.resolve_status(
        coverage_score=100.0, traceability_score=92.0,
        has_contradictions=False, hallucination_count=0, duplicate_count=0, missing_count=0
    )
    assert status_warn == "VERIFIED_WITH_WARNING"

    # Verified Clean (100% coverage, 100% traceability, 0 issues)
    status3 = StatusResolver.resolve_status(
        coverage_score=100.0, traceability_score=100.0,
        has_contradictions=False, hallucination_count=0, duplicate_count=0, missing_count=0
    )
    assert status3 == "VERIFIED"

def test_comparison_engine_matrix(db_session):
    role = db_session.query(models.Role).first()
    plan_dict = {
        "modules": [
            {
                "module_code": "MOD-001",
                "title": "Information Security Fundamentals",
                "requirement_code": "REQ-SEC-001",
                "source_doc_id": "DOC-POL-01",
                "source_section_id": "1.1",
                "genai_claimed_status": "VERIFIED"
            }
        ],
        "checklists": []
    }
    matrix = ComparisonEngine.generate_comparison_matrix(db_session, role.id, plan_dict)
    assert isinstance(matrix, list)
    assert len(matrix) >= 100  # SRS requires at least 100 requirement rows
    first_row = matrix[0]
    assert "requirement_id" in first_row
    assert "python_expected" in first_row
    assert "genai_result" in first_row
    assert "validation_status" in first_row
